# Azure DevOps REST API - Referencia

> Resumen basado en documentacion oficial de Microsoft (learn.microsoft.com).
> Fecha de consulta: 2026-09-22.

## Tabla de contenidos

1. [Estructura general de la API](#estructura-general-de-la-api)
2. [Autenticacion con PAT (Personal Access Token)](#autenticacion-con-pat-personal-access-token)
3. [Otros metodos de autenticacion](#otros-metodos-de-autenticacion)
4. [Versionado de la API](#versionado-de-la-api)
5. [Endpoints de Work Items](#endpoints-de-work-items)
6. [Endpoints de Queries (WIQL)](#endpoints-de-queries-wiql)
7. [Endpoints de Git / Pull Requests](#endpoints-de-git--pull-requests)
8. [Endpoints de Build / Pipelines](#endpoints-de-build--pipelines)
9. [Endpoints de Projects](#endpoints-de-projects)
10. [Respuestas y paginacion](#respuestas-y-paginacion)
11. [Errores comunes](#errores-comunes)

---

## Estructura general de la API

Todas las llamadas a la REST API de Azure DevOps siguen este patron:

```
VERB https://dev.azure.com/{organization}[/{project}]/_apis/{area}/{resource}?api-version={version}
```

**Componentes:**

| Componente | Descripcion |
|------------|-------------|
| `{organization}` | Nombre de la organizacion en Azure DevOps Services |
| `{project}` | Nombre o ID del proyecto (opcional para algunos endpoints) |
| `_apis` | Prefijo fijo de la API |
| `{area}` | Area funcional: `wit`, `git`, `build`, `pipelines`, `release`, etc. |
| `{resource}` | Recurso especifico dentro del area |
| `api-version` | Version de la API (obligatorio) |

**Para Azure DevOps Server (on-premises):**

```
VERB https://{server}:{port}/tfs/{collection}[/{project}]/_apis/{area}/{resource}?api-version={version}
```

Puerto por defecto: 8080. Coleccion por defecto: `DefaultCollection`.

---

## Autenticacion con PAT (Personal Access Token)

El PAT es el metodo mas simple y comun para autenticarse con la REST API.

### Crear un PAT

1. Ir a Azure DevOps > click en el icono de usuario (esquina superior derecha).
2. Seleccionar **Personal access tokens**.
3. Click en **+ New Token**.
4. Configurar:
   - **Name**: Nombre descriptivo.
   - **Organization**: Organizacion a la que aplica (o All accessible organizations).
   - **Expiration**: Fecha de expiracion (maximo 1 anio).
   - **Scopes**: Permisos especificos (ej. Work Items Read & Write, Code Read, Build Read & Execute).
5. Click en **Create**.
6. **Copiar el token inmediatamente** (no se puede recuperar despues).

### Usar PAT con curl

El PAT se envia como autenticacion HTTP Basic. El usuario puede estar vacio; la contrasena es el token. El valor se codifica en Base64 como `:{PAT}`:

```bash
# Metodo 1: usando -u (curl codifica automaticamente)
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/_apis/projects?api-version=7.1"

# Metodo 2: header Authorization con Base64
# Codificar ":{PAT}" en Base64:
TOKEN=$(echo -n ":{PAT}" | base64)

curl -H "Authorization: Basic ${TOKEN}" \
  "https://dev.azure.com/{org}/_apis/projects?api-version=7.1"
```

### Scopes comunes para PAT

| Scope | Permite |
|-------|---------|
| `vso.work` | Leer work items, queries, boards |
| `vso.work_write` | Leer y escribir work items, queries |
| `vso.code` | Leer repositorios, branches, commits |
| `vso.code_write` | Leer/escribir codigo, crear PRs |
| `vso.code_manage` | Administrar repos (crear, eliminar) |
| `vso.build` | Leer builds |
| `vso.build_execute` | Leer y ejecutar builds |
| `vso.release` | Leer releases |
| `vso.release_execute` | Leer y ejecutar releases |
| `vso.project` | Leer proyectos |

### Buenas practicas con PAT

- **Minimo privilegio**: Asignar solo los scopes necesarios.
- **Expiracion corta**: Renovar frecuentemente.
- **No hardcodear**: Almacenar en variables de entorno o secret stores.
- **Revocar inmediatamente** si se compromete.
- **Un PAT por integracion**: Facilita auditoria y revocacion selectiva.

---

## Otros metodos de autenticacion

| Metodo | Caso de uso | Descripcion |
|--------|------------|-------------|
| **PAT** | Scripts, herramientas CLI, integraciones simples | Token personal, facil de usar |
| **OAuth 2.0** | Aplicaciones web interactivas | Flujo de autorizacion con consent del usuario |
| **MSAL (Microsoft Authentication Library)** | Aplicaciones cliente interactivas | Autenticacion via Microsoft Entra ID |
| **Service Principal** | Automatizacion sin usuario, CI/CD | Identidad de aplicacion en Entra ID |
| **Managed Identity** | Servicios en Azure (VMs, App Service) | Identidad gestionada por Azure, sin secretos |
| **SSH** | Operaciones Git | Autenticacion por clave publica/privada |

---

## Versionado de la API

La version se especifica en el query parameter `api-version`:

```
api-version=7.1
api-version=7.1-preview.1
```

### Tabla de compatibilidad Server/API

| Server Version | REST API Version |
|---------------|-----------------|
| Azure DevOps Services | 7.2 (latest) |
| Azure DevOps Server 2022.1 | 7.1 |
| Azure DevOps Server 2022 | 7.0 |
| Azure DevOps Server 2020 | 6.0 |
| Azure DevOps Server 2019 | 5.0 |

**Recomendacion**: Usar la version mas reciente compatible con tu servidor. Para Azure DevOps Services, usar `7.1` o `7.2`.

---

## Endpoints de Work Items

### Obtener un work item por ID

```bash
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{id}?api-version=7.1"
```

**Con expansion de campos:**

```bash
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{id}?\$expand=all&api-version=7.1"
```

Opciones de `$expand`: `None`, `Relations`, `Fields`, `Links`, `All`.

### Obtener multiples work items por IDs

```bash
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/wit/workitems?ids=1,2,3,4,5&api-version=7.1"
```

### Crear un work item

```bash
curl -u ":{PAT}" \
  -X POST \
  -H "Content-Type: application/json-patch+json" \
  -d '[
    {
      "op": "add",
      "path": "/fields/System.Title",
      "value": "Mi nueva tarea"
    },
    {
      "op": "add",
      "path": "/fields/System.AssignedTo",
      "value": "usuario@org.com"
    },
    {
      "op": "add",
      "path": "/fields/System.AreaPath",
      "value": "MiProyecto\\MiArea"
    },
    {
      "op": "add",
      "path": "/fields/Microsoft.VSTS.Common.Priority",
      "value": 2
    }
  ]' \
  "https://dev.azure.com/{org}/{project}/_apis/wit/workitems/\$Task?api-version=7.1"
```

**Notas:**
- El tipo se especifica en la URL con `$` prefix: `$Task`, `$Bug`, `$User%20Story`, `$Epic`, `$Feature`.
- El body es un JSON Patch Document (array de operaciones).
- Operaciones: `add`, `replace`, `remove`, `test`.
- Content-Type: `application/json-patch+json`.

### Actualizar un work item

```bash
curl -u ":{PAT}" \
  -X PATCH \
  -H "Content-Type: application/json-patch+json" \
  -d '[
    {
      "op": "replace",
      "path": "/fields/System.State",
      "value": "Active"
    },
    {
      "op": "replace",
      "path": "/fields/System.Title",
      "value": "Titulo actualizado"
    }
  ]' \
  "https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{id}?api-version=7.1"
```

### Eliminar un work item

```bash
# Mover a papelera (soft delete)
curl -u ":{PAT}" \
  -X DELETE \
  "https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{id}?api-version=7.1"

# Eliminar permanentemente
curl -u ":{PAT}" \
  -X DELETE \
  "https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{id}?destroy=true&api-version=7.1"
```

### Agregar un link padre-hijo

```bash
curl -u ":{PAT}" \
  -X PATCH \
  -H "Content-Type: application/json-patch+json" \
  -d '[
    {
      "op": "add",
      "path": "/relations/-",
      "value": {
        "rel": "System.LinkTypes.Hierarchy-Reverse",
        "url": "https://dev.azure.com/{org}/{project}/_apis/wit/workItems/{parentId}",
        "attributes": {
          "comment": "Linking to parent"
        }
      }
    }
  ]' \
  "https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{childId}?api-version=7.1"
```

---

## Endpoints de Queries (WIQL)

### Ejecutar una query WIQL

```bash
curl -u ":{PAT}" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.WorkItemType] = '\''Bug'\'' AND [System.State] = '\''Active'\'' AND [System.AssignedTo] = @Me ORDER BY [System.CreatedDate] DESC"
  }' \
  "https://dev.azure.com/{org}/{project}/_apis/wit/wiql?api-version=7.1"
```

**Nota**: WIQL devuelve solo IDs y URLs. Para obtener los campos completos, usar los IDs retornados con el endpoint de work items.

### Obtener queries guardadas

```bash
# Listar queries en Shared Queries
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/wit/queries/Shared%20Queries?api-version=7.1&\$depth=2"
```

### Ejecutar una query guardada por ID

```bash
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/wit/wiql/{queryId}?api-version=7.1"
```

---

## Endpoints de Git / Pull Requests

### Listar repositorios

```bash
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/git/repositories?api-version=7.1"
```

### Listar pull requests

```bash
# PRs activos en un repositorio
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/git/repositories/{repoId}/pullrequests?searchCriteria.status=active&api-version=7.1"
```

### Crear un pull request

```bash
curl -u ":{PAT}" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "sourceRefName": "refs/heads/feature/my-feature",
    "targetRefName": "refs/heads/main",
    "title": "Add new feature",
    "description": "Description of the changes",
    "reviewers": [
      {
        "id": "{reviewer-guid}"
      }
    ]
  }' \
  "https://dev.azure.com/{org}/{project}/_apis/git/repositories/{repoId}/pullrequests?api-version=7.1"
```

### Completar un pull request

```bash
curl -u ":{PAT}" \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "lastMergeSourceCommit": {
      "commitId": "{lastMergeSourceCommitId}"
    },
    "completionOptions": {
      "mergeStrategy": "squash",
      "deleteSourceBranch": true,
      "mergeCommitMessage": "Merged PR: Add new feature",
      "transitionWorkItems": true
    }
  }' \
  "https://dev.azure.com/{org}/{project}/_apis/git/repositories/{repoId}/pullrequests/{prId}?api-version=7.1"
```

**Valores de mergeStrategy:**
- `noFastForward`: Merge commit (default).
- `squash`: Squash merge.
- `rebase`: Rebase and fast-forward.
- `rebaseMerge`: Semi-linear merge.

### Listar branches

```bash
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/git/repositories/{repoId}/refs?filter=heads/&api-version=7.1"
```

### Obtener commits

```bash
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/git/repositories/{repoId}/commits?\$top=10&api-version=7.1"
```

---

## Endpoints de Build / Pipelines

### Listar builds

```bash
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/build/builds?\$top=10&api-version=7.1"
```

### Obtener un build por ID

```bash
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/build/builds/{buildId}?api-version=7.1"
```

### Encolar un build (ejecutar pipeline)

```bash
curl -u ":{PAT}" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "definition": {
      "id": {definitionId}
    },
    "sourceBranch": "refs/heads/main",
    "parameters": "{\"system.debug\":\"true\"}"
  }' \
  "https://dev.azure.com/{org}/{project}/_apis/build/builds?api-version=7.1"
```

### Listar definiciones de pipeline

```bash
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/build/definitions?api-version=7.1"
```

### Pipelines API (nueva)

```bash
# Listar pipelines
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/pipelines?api-version=7.1"

# Ejecutar un pipeline
curl -u ":{PAT}" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "resources": {
      "repositories": {
        "self": {
          "refName": "refs/heads/main"
        }
      }
    }
  }' \
  "https://dev.azure.com/{org}/{project}/_apis/pipelines/{pipelineId}/runs?api-version=7.1"
```

### Obtener logs de un build

```bash
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/build/builds/{buildId}/logs?api-version=7.1"

# Obtener un log especifico
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/build/builds/{buildId}/logs/{logId}?api-version=7.1"
```

### Obtener artefactos de un build

```bash
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/build/builds/{buildId}/artifacts?api-version=7.1"
```

---

## Endpoints de Projects

### Listar proyectos

```bash
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/_apis/projects?api-version=7.1"
```

### Obtener un proyecto

```bash
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/_apis/projects/{projectId}?api-version=7.1"
```

### Listar teams de un proyecto

```bash
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/_apis/projects/{projectId}/teams?api-version=7.1"
```

---

## Respuestas y paginacion

### Formato de respuesta

Todas las respuestas son JSON. Las listas retornan un objeto con:

```json
{
  "count": 2,
  "value": [
    { ... },
    { ... }
  ]
}
```

### Paginacion

- Usar `$top` para limitar resultados (ej. `$top=50`).
- Usar `$skip` para saltar resultados (ej. `$skip=50`).
- Usar `continuationToken` cuando la API lo provee en el header de respuesta.
- Algunas APIs usan el header `x-ms-continuationtoken` para indicar que hay mas resultados.

```bash
# Primera pagina
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/wit/wiql?api-version=7.1&\$top=200"

# Pagina siguiente (con continuationToken del header de respuesta)
curl -u ":{PAT}" \
  "https://dev.azure.com/{org}/{project}/_apis/wit/wiql?api-version=7.1&\$top=200&continuationToken={token}"
```

---

## Errores comunes

| Codigo HTTP | Significado | Causa comun |
|-------------|-------------|-------------|
| 400 Bad Request | Solicitud mal formada | JSON invalido, campos faltantes, tipo de work item incorrecto |
| 401 Unauthorized | No autenticado | PAT expirado, invalido o mal codificado |
| 403 Forbidden | Sin permisos | PAT sin el scope necesario, usuario sin permisos en el proyecto |
| 404 Not Found | Recurso no encontrado | ID inexistente, URL mal formada, proyecto/repo incorrecto |
| 409 Conflict | Conflicto | Actualizacion concurrente, revision desactualizada |
| 429 Too Many Requests | Rate limiting | Demasiadas solicitudes. Respetar headers `Retry-After` |

### Troubleshooting

1. **Verificar PAT**: Asegurarse de que el token no este expirado y tenga los scopes correctos.
2. **Verificar URL**: Confirmar organization, project y resource path.
3. **Verificar api-version**: Usar la version compatible con el servidor.
4. **Verificar Content-Type**: Usar `application/json-patch+json` para work items, `application/json` para otros.
5. **Verificar encoding**: El PAT debe codificarse como `:{PAT}` en Base64 para el header Authorization.

---

## Fuentes

- https://learn.microsoft.com/en-us/rest/api/azure/devops (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/create (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/create (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/rest/api/azure/devops/build/builds (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/rest/api/azure/devops/pipelines (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/integrate/get-started/authentication/pats (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/integrate/get-started/authentication/authentication-guidance (consultado 2026-09-22)
