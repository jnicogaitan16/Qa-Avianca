# Azure DevOps Pipelines YAML - Referencia

> Resumen basado en documentacion oficial de Microsoft (learn.microsoft.com).
> Fecha de consulta: 2026-09-22.

## Tabla de contenidos

1. [Estructura general de un pipeline YAML](#estructura-general-de-un-pipeline-yaml)
2. [Trigger (disparadores)](#trigger-disparadores)
3. [Pool (agentes)](#pool-agentes)
4. [Stages (etapas)](#stages-etapas)
5. [Jobs (trabajos)](#jobs-trabajos)
6. [Steps (pasos)](#steps-pasos)
7. [Variables](#variables)
8. [Variable Groups](#variable-groups)
9. [Parameters (parametros de runtime)](#parameters-parametros-de-runtime)
10. [Templates y reutilizacion](#templates-y-reutilizacion)
11. [Approvals y Checks (gates de aprobacion)](#approvals-y-checks-gates-de-aprobacion)
12. [Deployment jobs y environments](#deployment-jobs-y-environments)
13. [Resources](#resources)
14. [Expresiones y condiciones](#expresiones-y-condiciones)
15. [Buenas practicas](#buenas-practicas)

---

## Estructura general de un pipeline YAML

Un pipeline YAML tiene la siguiente estructura jerarquica:

```yaml
trigger:          # Cuando se dispara el pipeline
  branches:
    include:
      - main

pool:             # Pool de agentes por defecto
  vmImage: 'ubuntu-latest'

variables:        # Variables globales
  buildConfiguration: 'Release'

stages:           # Lista de stages
- stage: Build
  jobs:
  - job: BuildJob
    steps:
    - script: echo "Building..."
- stage: Deploy
  dependsOn: Build
  jobs:
  - job: DeployJob
    steps:
    - script: echo "Deploying..."
```

**Jerarquia simplificada:**

```
Pipeline
  ├── trigger / pr / schedules
  ├── pool
  ├── variables
  ├── parameters
  ├── resources
  └── stages[]
       └── jobs[]
            └── steps[]
```

**Nota:** Si un pipeline tiene solo un stage, se puede omitir la clave `stages` y escribir directamente `jobs`. Si tiene solo un job, se puede omitir `jobs` y escribir directamente `steps`.

---

## Trigger (disparadores)

### CI trigger (push)

```yaml
# Disparar en push a ramas especificas
trigger:
  branches:
    include:
      - main
      - release/*
    exclude:
      - feature/experimental
  paths:
    include:
      - src/**
    exclude:
      - docs/**
  tags:
    include:
      - v*
```

```yaml
# Desactivar CI trigger
trigger: none
```

### PR trigger

```yaml
# Disparar en pull requests hacia ramas especificas
pr:
  branches:
    include:
      - main
  paths:
    include:
      - src/**
```

```yaml
# Desactivar PR trigger
pr: none
```

**Nota:** En Azure DevOps Services, los PR triggers para repositorios Azure Repos se configuran mediante branch policies (Build validation), no en YAML.

### Scheduled trigger

```yaml
schedules:
- cron: '0 2 * * Mon-Fri'    # Formato cron (UTC)
  displayName: 'Nightly build'
  branches:
    include:
      - main
  always: true                # Ejecutar aunque no haya cambios
```

### Pipeline resource trigger

```yaml
resources:
  pipelines:
  - pipeline: upstream-build
    source: 'OtroPipeline'
    trigger:
      branches:
        include:
          - main
```

---

## Pool (agentes)

### Microsoft-hosted agents

```yaml
pool:
  vmImage: 'ubuntu-latest'    # Tambien: 'windows-latest', 'macOS-latest'
```

### Self-hosted agents

```yaml
pool:
  name: 'MiPoolPrivado'
  demands:
    - Agent.OS -equals Linux
    - docker
```

El pool puede definirse a nivel de pipeline, stage o job. El nivel mas especifico sobreescribe al mas general.

---

## Stages (etapas)

Un stage agrupa jobs relacionados y permite modelar entornos (Build, Test, Deploy).

```yaml
stages:
- stage: Build
  displayName: 'Build Stage'
  jobs:
  - job: BuildJob
    steps:
    - script: dotnet build

- stage: Test
  displayName: 'Test Stage'
  dependsOn: Build              # Dependencia explicita
  condition: succeeded()        # Solo si Build fue exitoso
  jobs:
  - job: TestJob
    steps:
    - script: dotnet test

- stage: Deploy
  dependsOn:
    - Build
    - Test                      # Depende de multiples stages
  condition: |
    and(
      succeeded('Build'),
      succeeded('Test'),
      eq(variables['Build.SourceBranch'], 'refs/heads/main')
    )
  jobs:
  - job: DeployJob
    steps:
    - script: echo "Deploying to production"
```

**Propiedades clave de stage:**
- `stage`: Nombre identificador (sin espacios).
- `displayName`: Nombre visible en la UI.
- `dependsOn`: Stages que deben completarse antes.
- `condition`: Expresion booleana para ejecucion condicional.
- `variables`: Variables de scope de stage.
- `lockBehavior`: `sequential` o `runLatest` (para exclusive locks).

---

## Jobs (trabajos)

Un job es una coleccion de steps que se ejecutan en un agente.

```yaml
jobs:
- job: BuildApp
  displayName: 'Build Application'
  pool:
    vmImage: 'ubuntu-latest'
  timeoutInMinutes: 60
  cancelTimeoutInMinutes: 5
  strategy:
    matrix:
      linux:
        imageName: 'ubuntu-latest'
      windows:
        imageName: 'windows-latest'
    maxParallel: 2
  steps:
  - script: echo "Building on $(imageName)"
```

### Deployment jobs

Jobs especiales para despliegues con tracking en environments:

```yaml
jobs:
- deployment: DeployWeb
  displayName: 'Deploy to Production'
  environment: 'production'
  strategy:
    runOnce:
      deploy:
        steps:
        - script: echo "Deploying..."
    # Otras estrategias: rolling, canary
```

**Estrategias de deployment:**
- `runOnce`: Ejecuta los steps una vez.
- `rolling`: Despliega incrementalmente a un conjunto de maquinas.
- `canary`: Despliega a un porcentaje de instancias progresivamente.

---

## Steps (pasos)

Los steps son la unidad minima de ejecucion. Tipos principales:

### script

```yaml
steps:
- script: echo "Hello World"
  displayName: 'Run a one-line script'
```

### bash

```yaml
- bash: |
    echo "This runs in bash"
    ls -la
  displayName: 'Run bash script'
```

### powershell / pwsh

```yaml
- powershell: Write-Host "Windows PowerShell"
- pwsh: Write-Host "PowerShell Core (cross-platform)"
```

### task

```yaml
- task: DotNetCoreCLI@2
  displayName: 'dotnet build'
  inputs:
    command: 'build'
    projects: '**/*.csproj'
```

### checkout

```yaml
- checkout: self          # Checkout del repo actual
  clean: true
  fetchDepth: 1           # Shallow clone
```

### download / publish

```yaml
- publish: $(Build.ArtifactStagingDirectory)
  artifact: 'drop'
  displayName: 'Publish artifact'

- download: current       # Descargar artifact del pipeline actual
  artifact: 'drop'
```

### template (reference a steps template)

```yaml
- template: templates/build-steps.yml
  parameters:
    configuration: Release
```

---

## Variables

### Formas de definir variables

**1. Sintaxis de mapping (name/value):**

```yaml
variables:
  buildConfiguration: 'Release'
  buildPlatform: 'Any CPU'
```

**2. Sintaxis completa (name/value con detalles):**

```yaml
variables:
- name: buildConfiguration
  value: 'Release'
- name: secret
  value: $(mySecret)     # Referencia a variable secreta
```

**3. En la UI del pipeline (Pipeline Settings > Variables):**
- Permite marcar como **secret** (no se muestra en logs).
- Se puede restringir a ramas especificas con "Let users override this value at queue time".

### Scopes de variables

| Scope | Definicion | Disponibilidad |
|-------|------------|----------------|
| Pipeline (root) | `variables:` a nivel raiz | Todos los stages, jobs y steps |
| Stage | `variables:` dentro de un stage | Jobs y steps de ese stage |
| Job | `variables:` dentro de un job | Steps de ese job |

### Sintaxis de referencia

| Sintaxis | Cuando se usa | Ejemplo |
|----------|--------------|---------|
| Macro: `$(var)` | En la mayoria de inputs de tasks y scripts | `echo $(buildConfiguration)` |
| Template expression: `${{ variables.var }}` | En tiempo de compilacion del YAML | `${{ variables.buildConfiguration }}` |
| Runtime expression: `$[variables.var]` | En condiciones evaluadas en runtime | `condition: eq($[variables.deploy], 'true')` |

### Variables predefinidas importantes

| Variable | Descripcion |
|----------|-------------|
| `Build.SourceBranch` | Rama que disparo el build (ej. `refs/heads/main`) |
| `Build.SourceBranchName` | Nombre corto de la rama (ej. `main`) |
| `Build.BuildId` | ID unico del build |
| `Build.BuildNumber` | Numero de build formateado |
| `Build.Repository.Name` | Nombre del repositorio |
| `System.DefaultWorkingDirectory` | Directorio de trabajo por defecto |
| `Build.ArtifactStagingDirectory` | Directorio para artefactos antes de publicar |
| `Agent.OS` | Sistema operativo del agente |
| `Build.Reason` | Razon del build: Manual, IndividualCI, PullRequest, Schedule |

### Variables secretas

- Las variables marcadas como **secret** no se imprimen en logs (se reemplazan por `***`).
- No se pueden referenciar con template expressions `${{ }}` (solo en runtime).
- Se deben pasar explicitamente a scripts como variables de entorno:

```yaml
steps:
- script: echo "Token is available"
  env:
    MY_SECRET: $(secretVariable)
```

---

## Variable Groups

Permiten compartir variables entre multiples pipelines.

### Crear un variable group

1. Ir a **Pipelines > Library > + Variable group**.
2. Asignar nombre y agregar variables (clave-valor).
3. Opcionalmente vincular a Azure Key Vault para secretos.
4. Asignar permisos de acceso a pipelines.

### Referenciar en YAML

```yaml
variables:
- group: 'my-variable-group'
- name: localVar
  value: 'local-value'
```

### Vincular a Azure Key Vault

1. En el variable group, activar "Link secrets from an Azure key vault".
2. Seleccionar la suscripcion y el Key Vault.
3. Autorizar y seleccionar los secretos a vincular.
4. Los secretos se inyectan automaticamente como variables secretas en runtime.

---

## Parameters (parametros de runtime)

Los parametros permiten inputs personalizados al ejecutar un pipeline:

```yaml
parameters:
- name: environment
  displayName: 'Target Environment'
  type: string
  default: 'dev'
  values:
    - dev
    - staging
    - production

- name: runTests
  displayName: 'Run tests?'
  type: boolean
  default: true

steps:
- script: echo "Deploying to ${{ parameters.environment }}"
- ${{ if eq(parameters.runTests, true) }}:
  - script: dotnet test
```

**Tipos de parametros soportados:** `string`, `number`, `boolean`, `object`, `step`, `stepList`, `job`, `jobList`, `stage`, `stageList`.

Los parametros se resuelven en **tiempo de compilacion** del YAML (no en runtime), por lo que se usan con `${{ }}`.

---

## Templates y reutilizacion

### Tipos de templates

| Tipo | Descripcion |
|------|-------------|
| **Step template** | Reutiliza una secuencia de steps |
| **Job template** | Reutiliza jobs completos |
| **Stage template** | Reutiliza stages completos |
| **Variable template** | Reutiliza definiciones de variables |
| **Extends template** | Define la estructura obligatoria del pipeline (seguridad) |

### Include template (insercion)

```yaml
# templates/build-steps.yml
parameters:
- name: configuration
  type: string
  default: 'Release'

steps:
- script: dotnet build --configuration ${{ parameters.configuration }}
- script: dotnet test
```

```yaml
# azure-pipelines.yml
steps:
- template: templates/build-steps.yml
  parameters:
    configuration: 'Debug'
```

### Extends template (seguridad)

```yaml
# templates/required-template.yml
parameters:
- name: buildSteps
  type: stepList
  default: []

stages:
- stage: Build
  pool:
    vmImage: 'ubuntu-latest'
  jobs:
  - job: BuildJob
    steps:
    - script: echo "Pre-build check"
    - ${{ each step in parameters.buildSteps }}:
      - ${{ step }}
    - script: echo "Post-build signing"
```

```yaml
# azure-pipelines.yml
trigger:
- main

extends:
  template: templates/required-template.yml
  parameters:
    buildSteps:
      - script: npm install
      - script: npm build
```

### Templates de otros repositorios

```yaml
resources:
  repositories:
  - repository: templates
    type: git
    name: 'MiProyecto/TemplatesRepo'
    ref: refs/tags/v1.0

stages:
- template: stages/deploy.yml@templates
  parameters:
    environment: 'production'
```

### Limites de templates

- Maximo 100 archivos YAML incluidos (directa o indirectamente).
- Maximo 100 niveles de anidamiento.
- Maximo 20 MB de memoria al parsear YAML.

---

## Approvals y Checks (gates de aprobacion)

Las aprobaciones y checks se configuran sobre **resources** (environments, service connections, agent pools, variable groups, secure files, repositories), **no en el YAML**.

### Categorias de checks (orden de ejecucion)

1. **Static checks**: Branch control, Required template, Evaluate artifact.
2. **Pre-check approvals**: Aprobaciones previas.
3. **Dynamic checks**: Approval, Invoke Azure Function, Invoke REST API, Business Hours, Query Azure Monitor Alerts.
4. **Post-check approvals**: Aprobaciones posteriores.
5. **Exclusive lock**: Bloqueo exclusivo.

### Tipos de checks

| Check | Descripcion |
|-------|-------------|
| **Approval** | Aprobacion manual por uno o mas usuarios/grupos. Se puede configurar timeout, y si el aprobador puede aprobar su propio run. Admite **deferred approvals** (aprobar para ejecutar en un momento futuro). |
| **Branch control** | Verifica que los recursos vinculados fueron construidos desde ramas permitidas y con proteccion habilitada. |
| **Business hours** | Restringe despliegues a ventanas horarias especificas. |
| **Invoke Azure Function** | Llama a una Azure Function; el check pasa si la funcion retorna exito. |
| **Invoke REST API** | Llama a un endpoint REST externo periodicamente hasta obtener respuesta exitosa. |
| **Query Azure Monitor Alerts** | Verifica que no hay alertas activas en Azure Monitor tras un despliegue. |
| **Required template** | Fuerza que el pipeline use un template YAML especifico (`extends`). Si no lo usa, el pipeline falla. |
| **Evaluate artifact** | Evalua artefactos contra politicas personalizadas (solo imagenes de contenedor). |
| **Exclusive lock** | Solo permite un run del pipeline a la vez en el resource. `lockBehavior`: `runLatest` (default) o `sequential`. |

### Configurar una aprobacion

1. Ir a **Pipelines > Environments** (o el recurso correspondiente).
2. Seleccionar el environment.
3. Pestana **Approvals and checks** > **+** > **Approvals**.
4. Agregar aprobadores (usuarios o grupos).
5. Configurar timeout y opciones.
6. Guardar.

### Bypass de checks

- Solo usuarios con permiso de administrador del recurso pueden hacer bypass.
- Seleccionar **Bypass check** cuando el recurso esta esperando revision.
- El bypass se registra en el panel de checks (auditoria).

---

## Deployment jobs y environments

### Environments

Un environment representa un destino de despliegue (ej. `development`, `staging`, `production`).

```yaml
- deployment: DeployWeb
  environment: 'production'
  strategy:
    runOnce:
      deploy:
        steps:
        - script: echo "Deploy to production"
```

- Los environments registran historial de despliegues.
- Se les pueden asignar approvals y checks.
- Pueden tener recursos asociados (Kubernetes, VMs).

---

## Resources

Define recursos externos que el pipeline consume:

```yaml
resources:
  pipelines:                    # Otros pipelines
  - pipeline: myBuild
    source: 'BuildPipeline'
    trigger: true

  repositories:                 # Otros repositorios
  - repository: templates
    type: git
    name: 'Proyecto/Repo'

  containers:                   # Imagenes de contenedor
  - container: myContainer
    image: 'myregistry/myimage:latest'

  packages:                     # Paquetes NuGet/npm
  - package: myPackage
    type: npm
    connection: 'npmConnection'
    name: 'my-package'
    version: 1.0.0
```

---

## Expresiones y condiciones

### Condiciones comunes

```yaml
# Ejecutar solo si el stage anterior fue exitoso
condition: succeeded()

# Ejecutar siempre (incluso si algo fallo)
condition: always()

# Ejecutar solo si algo fallo
condition: failed()

# Condicion personalizada
condition: |
  and(
    succeeded(),
    eq(variables['Build.SourceBranch'], 'refs/heads/main'),
    ne(variables['Build.Reason'], 'PullRequest')
  )
```

### Funciones de expresion mas usadas

| Funcion | Descripcion |
|---------|-------------|
| `eq(a, b)` | Igualdad |
| `ne(a, b)` | Desigualdad |
| `and(a, b)` | AND logico |
| `or(a, b)` | OR logico |
| `not(a)` | Negacion |
| `contains(a, b)` | a contiene b |
| `startsWith(a, b)` | a empieza con b |
| `succeeded()` | Stage/job previo exitoso |
| `failed()` | Stage/job previo fallido |
| `always()` | Siempre ejecutar |
| `canceled()` | Si fue cancelado |

---

## Buenas practicas

1. **Usar templates** para logica reutilizable entre pipelines.
2. **Usar `extends` templates** para enforcing de seguridad y estandares.
3. **Variables secretas** siempre en variable groups o Key Vault, nunca en YAML.
4. **Aprovals en environments** para despliegues a produccion.
5. **Branch control** para asegurar que solo ramas protegidas despliegan.
6. **Parametros tipados** en lugar de variables cuando se necesita input del usuario.
7. **Required template check** para garantizar que todos los pipelines sigan el esquema corporativo.
8. **Pin templates a refs/tags** especificos para evitar cambios no controlados.
9. **Usar `condition`** para evitar ejecuciones innecesarias.
10. **Timeouts** en jobs y approvals para evitar pipelines colgados.

---

## Fuentes

- https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/pipelines/process/variables (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/pipelines/process/templates (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/pipelines/process/approvals (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/pipelines/process/environments (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/pipelines/process/expressions (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/pipelines/process/template-parameters (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/pipelines/library/variable-groups (consultado 2026-09-22)
