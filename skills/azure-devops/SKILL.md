---
name: azure-devops
description: >
  Skill para consultas sobre Azure DevOps: Boards (work items, queries), Pipelines YAML (stages, gates, aprobaciones), Repos Git (branch policies, pull requests) y REST API (autenticacion PAT, endpoints). Se activa cuando el usuario pregunta sobre configuracion, uso o troubleshooting de cualquier servicio de Azure DevOps. IMPORTANTE: antes de responder, consulta siempre references/ correspondiente.
---

# Skill: Azure DevOps

## Proposito

Este skill proporciona respuestas fundamentadas sobre los servicios principales de Azure DevOps, basandose en documentacion oficial de Microsoft resumida y verificada en los archivos de referencia.

---

## Reglas obligatorias

### 1. Consultar antes de responder

**Antes de responder sobre cualquier comportamiento de Azure DevOps, consulta primero el archivo en `references/` correspondiente al tema.** Si la duda no esta cubierta en los archivos de referencia, dilo explicitamente en vez de adivinar. Ejemplo:

> "Este punto no esta cubierto en la referencia actual. Te recomiendo consultar la documentacion oficial en [URL] para obtener informacion precisa."

### 2. No responder directo al usuario

**Este skill NO responde directo al usuario.** Genera un draft que sera validado por el orquestador-validador antes de entregarse. El draft debe:

- Incluir la fuente de referencia consultada.
- Marcar claramente cualquier dato que no provenga de las referencias con `[NO VERIFICADO]`.
- Ser factico y basado en la documentacion, no en suposiciones.

### 3. Precision tecnica

- Usar terminologia oficial de Microsoft.
- Mantener los terminos tecnicos en ingles cuando no existe traduccion estandar aceptada (ej. "pull request", "pipeline", "branch policy", "work item", "merge", "squash").
- Incluir ejemplos de codigo o configuracion YAML cuando sea pertinente.
- Citar la seccion relevante del archivo de referencia.

### 4. Consultar base_conocimiento/ para contexto del producto

Si el usuario pide **Newman en el pipeline**, este skill redacta el YAML y el orquestador activa tambien `postman` (comando `newman run` y coleccion). `Application Name` del Bug/PBI: SR, AVR, PI o ROR.

Cuando la pregunta se refiere al producto (SR, AVR, PI, ROR) o a procesos del equipo, consultar `base_conocimiento/` en la raíz del proyecto:
- `base_conocimiento/lineamientos-qa.md` — Cómo se usan Test Plans, Bugs, pipelines de automatización en el equipo
- `base_conocimiento/manual-aplicacion-sr.md` — Azure Functions, pipelines y BD de Special Refund
- `base_conocimiento/manual-aplicacion-avr.md` — APIs y procesos de AV Refund
- `base_conocimiento/manual-aplicacion-pi.md` — Payment Integrator
- `base_conocimiento/manual-aplicacion-ror.md` — Refund Orchestration Rules

### 5. Scope del skill

Este skill cubre:
- Azure DevOps Services (cloud) y Azure DevOps Server (on-premises).
- Servicios: Boards, Pipelines, Repos, REST API.

Este skill **NO** cubre:
- Azure Portal (recursos de infraestructura Azure).
- GitHub (aunque tenga integraciones con Azure DevOps).
- Herramientas de terceros no documentadas en las referencias.
- Configuracion de agentes self-hosted a nivel de infraestructura.

---

## Cuando se activa

Este skill debe activarse cuando el usuario pregunte sobre:

| Tema | Ejemplos de preguntas |
|------|----------------------|
| Boards / Work items | "Como creo un Epic en Azure DevOps?", "Que campos tiene un Bug?", "Como configuro una query compartida?", "Que procesos hay disponibles?" |
| Pipelines YAML | "Como estructuro un pipeline YAML?", "Como configuro aprobaciones?", "Como uso variable groups?", "Como hago un template reutilizable?" |
| Repos / Branch policies | "Como configuro reviewers minimos en una rama?", "Que tipos de merge hay?", "Como funciona auto-complete?", "Como hago un draft PR?" |
| REST API | "Como me autentico con PAT?", "Como creo un work item via API?", "Como ejecuto un pipeline por REST?", "Cual es el endpoint para PRs?" |
| Troubleshooting | "Mi pipeline falla con error X", "No puedo hacer merge a main", "La query no devuelve resultados esperados", "El PAT no funciona" |

---

## Mapa de temas a archivos de referencia

### Boards y Work Items

**Archivo:** `references/boards-y-work-items.md`

Cubre:
- Tipos de work items: Epic, Feature, User Story, Task, Bug.
- Procesos: Agile, Basic, Scrum, CMMI.
- Jerarquia y categorias de work items.
- Campos clave comunes y especificos por tipo.
- Estados y workflow por proceso.
- Queries: creacion, tipos (flat, tree, direct links), operadores, macros.
- Shared Queries, permisos y favoritos.
- Personalizacion (Inherited Process, XML Process).
- Tags, templates de work items.
- Operaciones practicas: crear, bulk update, vincular, charts.

### Pipelines YAML

**Archivo:** `references/pipelines-yaml.md`

Cubre:
- Estructura jerarquica: pipeline > stages > jobs > steps.
- Triggers: CI (push), PR, scheduled, pipeline resource.
- Pool: Microsoft-hosted y self-hosted agents.
- Stages: dependencias, condiciones.
- Jobs: regulares y deployment jobs.
- Steps: script, bash, powershell, task, checkout, template.
- Variables: definicion, scopes, sintaxis (macro, template, runtime), secretas, predefinidas.
- Variable Groups y vinculacion con Azure Key Vault.
- Parameters de runtime.
- Templates: include, extends, templates en otros repos.
- Approvals y Checks: tipos, configuracion, orden de ejecucion, bypass.
- Environments y deployment strategies (runOnce, rolling, canary).
- Resources: pipelines, repositories, containers, packages.
- Expresiones y condiciones.

### Repos Git y Branch Policies

**Archivo:** `references/repos-git-policies.md`

Cubre:
- Branch policies: configuracion y tipos.
- Minimum reviewers: opciones de reset de votos, auto-aprobacion.
- Check for linked work items.
- Check for comment resolution.
- Limit merge types: merge, squash, rebase, semi-linear.
- Build validation: trigger, expiracion, path filters.
- Status checks de servicios externos.
- Automatically included reviewers.
- Pull requests: creacion (portal, CLI, Visual Studio), elementos, votacion.
- Draft PRs: crear, publicar, diferencias con PRs regulares.
- Auto-complete.
- Completar PRs: merge types, opciones post-completado.
- Revert de PRs.
- PR templates.
- Estrategia de branching recomendada.

### REST API

**Archivo:** `references/rest-api.md`

Cubre:
- Estructura de URLs de la API.
- Autenticacion con PAT: creacion, uso con curl, scopes, buenas practicas.
- Otros metodos de autenticacion: OAuth, MSAL, Service Principal, Managed Identity.
- Versionado de la API y compatibilidad con servidores.
- Endpoints de Work Items: get, create, update, delete, links.
- Endpoints de Queries/WIQL.
- Endpoints de Git/Pull Requests: listar repos, crear/completar PRs, branches, commits.
- Endpoints de Build/Pipelines: listar/obtener/encolar builds, definiciones, logs, artefactos.
- Endpoints de Projects y Teams.
- Respuestas JSON, paginacion.
- Errores comunes y troubleshooting.

---

## Formato de respuesta esperado

Al generar un draft, seguir esta estructura:

```
### Respuesta

[Contenido de la respuesta basado en las referencias]

### Fuente de referencia

- Archivo consultado: `references/{archivo}.md`
- Seccion relevante: [nombre de la seccion]

### Notas

- [Cualquier advertencia, limitacion o dato no verificado]
```

---

## Actualizacion de referencias

Las referencias fueron compiladas a partir de documentacion oficial de Microsoft en learn.microsoft.com el 2026-09-22. Si la pregunta del usuario se refiere a una funcionalidad muy reciente o en preview que no aparece en las referencias, indicarlo explicitamente:

> "Esta funcionalidad podria ser mas reciente que la ultima actualizacion de las referencias (2026-09-22). Recomiendo verificar directamente en learn.microsoft.com."

---

## Limites

- Maximo ~4 temas de referencia disponibles. Si la consulta sale del scope, derivar al usuario a la documentacion oficial.
- Las referencias son resumenes; no contienen el 100% de la documentacion original. Para detalles exhaustivos, referir a la URL de la fuente.
- Este skill no ejecuta llamadas a la API ni interactua con instancias reales de Azure DevOps.
