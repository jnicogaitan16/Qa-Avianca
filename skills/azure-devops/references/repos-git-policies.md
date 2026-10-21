# Azure DevOps Repos Git y Branch Policies - Referencia

> Resumen basado en documentacion oficial de Microsoft (learn.microsoft.com).
> Fecha de consulta: 2026-09-22.

## Tabla de contenidos

1. [Branch policies - Vista general](#branch-policies---vista-general)
2. [Minimum number of reviewers](#minimum-number-of-reviewers)
3. [Check for linked work items](#check-for-linked-work-items)
4. [Check for comment resolution](#check-for-comment-resolution)
5. [Limit merge types](#limit-merge-types)
6. [Build validation](#build-validation)
7. [Status checks](#status-checks)
8. [Automatically included reviewers](#automatically-included-reviewers)
9. [Pull requests](#pull-requests)
10. [Draft pull requests](#draft-pull-requests)
11. [Auto-complete](#auto-complete)
12. [Completar un pull request](#completar-un-pull-request)
13. [Merge types (estrategias de merge)](#merge-types-estrategias-de-merge)
14. [Revert de un pull request](#revert-de-un-pull-request)
15. [PR templates](#pr-templates)
16. [Estrategia de branching recomendada](#estrategia-de-branching-recomendada)

---

## Branch policies - Vista general

Las branch policies protegen ramas criticas (como `main`) y aseguran calidad antes de hacer merge. Cuando se activan en una rama, los push directos se rechazan y los cambios deben entrar via pull request.

### Como configurar branch policies

1. Ir a **Project Settings > Repos > Repositories**.
2. Seleccionar el repositorio.
3. Seleccionar la rama (ej. `main`).
4. Configurar las policies deseadas.

**Alternativa**: tambien se puede navegar desde **Repos > Branches**, click en los tres puntos de la rama y seleccionar **Branch policies**.

### Resumen de policies disponibles

| Policy | Default | Descripcion |
|--------|---------|-------------|
| Require a minimum number of reviewers | Off | Exige aprobacion de N revisores en PRs. |
| Check for linked work items | Off | Verifica que el PR tenga work items vinculados. |
| Check for comment resolution | Off | Verifica que todos los comentarios esten resueltos. |
| Limit merge types | Off | Restringe los tipos de merge permitidos al completar PRs. |
| Build validation | Off | Ejecuta builds de validacion antes de permitir merge. |
| Status checks | Off | Requiere que servicios externos reporten status exitoso. |
| Automatically included reviewers | Off | Asigna revisores automaticamente segun paths de codigo modificados. |

---

## Minimum number of reviewers

Garantiza que un numero minimo de personas revisen y aprueben el PR antes de completarlo.

### Opciones de configuracion

| Opcion | Descripcion |
|--------|-------------|
| **Minimum number of reviewers** | Cantidad minima de aprobaciones requeridas (ej. 1, 2, 3...). |
| **Allow requestors to approve their own changes** | Si esta deshabilitado, el creador del PR no puede aprobar su propio PR. |
| **Prohibit the most recent pusher from approving their own changes** | El ultimo usuario que hizo push no puede aprobar (evita auto-aprobacion tras cambios). |
| **Allow completion even if some reviewers vote "Wait" or "Reject"** | Permite completar aunque haya votos negativos (no recomendado). |
| **When new changes are pushed, reset all approval votes** | Reinicia los votos cuando se hacen nuevos pushes al source branch. |
| **Reset all votes (does not reset votes to reject or wait)** | Reinicia solo votos de aprobacion, mantiene rechazos. |
| **Reset only the votes of approvers whose files were changed** | Reinicia solo los votos de quienes revisaron archivos que cambiaron. |

---

## Check for linked work items

Promueve la trazabilidad exigiendo que los PRs tengan al menos un work item vinculado.

**Modos:**
- **Required**: El PR no puede completarse sin work items vinculados.
- **Optional**: Se muestra advertencia pero se permite completar.

---

## Check for comment resolution

Controla si los comentarios de revision deben resolverse antes de completar el PR.

**Modos:**
- **Required**: Todos los comentarios deben estar resueltos.
- **Optional**: Los comentarios no resueltos generan advertencia pero no bloquean.

---

## Limit merge types

Controla que tipos de merge estan disponibles al completar PRs. Se pueden habilitar uno o mas de los siguientes:

| Merge type | Descripcion | Historial resultante |
|------------|-------------|---------------------|
| **Merge (no fast-forward)** | Crea un merge commit de dos padres. Preserva todos los commits del source branch. | No lineal, todos los commits visibles. |
| **Squash merge** | Combina todos los commits del source en un unico commit nuevo en el target. No conserva historial individual. | Lineal, un solo commit. |
| **Rebase and fast-forward** | Reaplica los commits del source sobre el HEAD del target y hace fast-forward. El source branch se modifica durante el rebase. | Lineal, commits individuales preservados pero re-escritos. |
| **Semi-linear merge (Rebase with merge commit)** | Reaplica commits del source sobre el target y crea un merge commit de dos padres. | Semi-lineal, commits preservados + merge commit. |

**Recomendacion:** Definir la estrategia segun las necesidades del equipo. Squash es popular para mantener un historial limpio en `main`. Merge (no-ff) preserva contexto completo.

---

## Build validation

Ejecuta un pipeline de validacion automaticamente cuando se crea o actualiza un PR.

### Configuracion

1. En Branch policies, seleccionar **+ Add build policy**.
2. Configurar:
   - **Build pipeline**: Seleccionar el pipeline a ejecutar.
   - **Trigger**: `Automatic` (se ejecuta con cada push) o `Manual` (el usuario lo dispara).
   - **Policy requirement**: `Required` (debe pasar para merge) u `Optional` (informativo).
   - **Build expiration**: Tiempo tras el cual un build valido expira y debe re-ejecutarse:
     - Immediately (con cada cambio).
     - After N hours.
     - Never.
   - **Display name**: Nombre descriptivo de la policy.
   - **Path filter**: Ejecutar solo si cambian archivos en paths especificos.

Se pueden agregar multiples build policies a una misma rama (ej. build + tests + lint).

---

## Status checks

Permiten que servicios externos (ej. SonarQube, security scans) publiquen un status en el PR que debe ser exitoso para completar el merge.

### Configuracion

1. En Branch policies, seleccionar **+ Add status policy**.
2. Configurar:
   - **Status to check**: El genre/name del status publicado por el servicio externo.
   - **Policy requirement**: Required u Optional.
   - **Applicability**: Para la rama especifica o cualquier rama.

---

## Automatically included reviewers

Asigna revisores automaticamente cuando un PR modifica archivos en paths especificos.

### Configuracion

1. En Branch policies, seleccionar **+ Add automatic reviewer**.
2. Configurar:
   - **Reviewers**: Usuarios o grupos a asignar.
   - **Path filter**: Paths que disparan la asignacion (ej. `/src/api/*`).
   - **Required / Optional**: Si el revisor es obligatorio o sugerido.
   - **Activity feed message**: Mensaje opcional que aparece en el PR.

**Ejemplo de uso**: Asignar al equipo de seguridad cuando se modifican archivos en `/src/auth/`.

---

## Pull requests

### Crear un pull request

**Desde el portal web:**
1. Ir a **Repos > Pull requests > New pull request**.
2. Seleccionar source branch y target branch.
3. Completar titulo, descripcion (admite Markdown).
4. Agregar revisores, vincular work items, agregar tags.
5. Click en **Create**.

**Desde la linea de comandos (Azure CLI):**

```bash
az repos pr create \
  --repository MyRepo \
  --source-branch feature/my-feature \
  --target-branch main \
  --title "Add new feature" \
  --description "Description of changes" \
  --reviewers "user@org.com" \
  --work-items 123 456 \
  --open
```

**Desde Visual Studio:**
1. Menu **Git > Manage Branches**.
2. Click derecho en la rama > **Create Pull Request**.
3. Completar datos y crear.

**Despues de push:**
- Azure DevOps muestra un banner en la pagina de Pull Requests y en Files invitando a crear un PR desde la rama recien pusheada.

### Elementos de un pull request

| Elemento | Descripcion |
|----------|-------------|
| **Title** | Titulo descriptivo del cambio. |
| **Description** | Descripcion detallada. Admite Markdown. Se puede usar PR templates. |
| **Reviewers** | Revisores opcionales u obligatorios. Se pueden agregar usuarios o grupos. |
| **Work items** | Work items vinculados. Se pueden transicionar automaticamente al completar el PR. |
| **Tags/Labels** | Etiquetas para clasificacion. Comparten pool con work item tags (limite 150,000). |
| **Files** | Pestana con diff de los archivos modificados. |
| **Commits** | Lista de commits incluidos en el PR. |
| **Attachments** | Archivos adjuntos en la descripcion. Drag-and-drop soportado. |

### Votacion en pull requests

| Voto | Valor numerico | Significado |
|------|---------------|-------------|
| Approve | 10 | Aprobado |
| Approve with suggestions | 5 | Aprobado con sugerencias |
| No vote | 0 | Sin voto |
| Wait for author | -5 | Esperar cambios del autor |
| Reject | -10 | Rechazado |

---

## Draft pull requests

Los draft PRs indican trabajo en progreso (WIP).

**Diferencias con PRs publicados:**
- Las build validation policies **no se ejecutan automaticamente** (se pueden ejecutar manualmente).
- La votacion esta **deshabilitada**.
- Los revisores obligatorios **no se agregan automaticamente**.
- Solo se envian notificaciones a revisores agregados explicitamente.
- Aparecen con badge **Draft** en la lista de PRs.

### Crear draft PR

- En el portal: Al crear el PR, seleccionar la flecha junto a "Create" y elegir **Create as draft**.
- CLI: `az repos pr create --draft true`.

### Publicar draft PR

- Click en **Publish** en la parte superior derecha del PR.
- Publicar asigna revisores requeridos, evalua policies y habilita votacion.

### Convertir PR publicado a draft

- Click en **Mark as draft** en el PR. Esto **elimina todos los votos existentes**.

---

## Auto-complete

Configura el PR para completarse automaticamente cuando todas las policies se satisfagan.

### Como configurar

1. En el PR, seleccionar **Set auto-complete** del dropdown de **Complete**.
2. Configurar opciones de merge y post-completado.
3. El PR espera a que todas las policies requeridas pasen.

**Opciones en el panel de auto-complete:**
- Se puede elegir esperar por policies opcionales ademas de las requeridas.
- Se puede cancelar con **Cancel auto-complete**.

**Notas:**
- Solo esta disponible cuando hay branch policies configuradas.
- PRs en auto-complete muestran badge **Auto-complete** en la lista.
- Se recibe notificacion por email al completarse o si hay conflictos.

---

## Completar un pull request

### Pasos

1. Verificar que todas las policies se satisfacen (revisores, builds, status checks).
2. Click en **Complete** (o usar auto-complete).
3. Seleccionar **Merge type** (ver seccion siguiente).
4. Configurar opciones post-completado:
   - **Complete associated work items after merging**: Transicionar work items vinculados.
   - **Delete source branch after merging**: Eliminar la rama fuente.
   - **Customize merge commit message**: Personalizar mensaje del merge commit.
   - **Override branch policies and enable merge**: Bypass de policies (requiere permiso especial: **Exempt from policy enforcement**).
5. Click en **Complete merge**.

---

## Merge types (estrategias de merge)

Al completar un PR se selecciona una de estas estrategias:

### Merge (no fast-forward) - Default

```
main:    A---B-------M
              \     /
feature:       C---D
```

- Crea un merge commit `M` con dos padres.
- Preserva todo el historial de commits del feature branch.
- **Ideal para**: Equipos que quieren trazabilidad completa.

### Squash merge

```
main:    A---B---S
              \
feature:       C---D   (estos commits se "aplastan" en S)
```

- Combina todos los commits del source branch en un solo commit `S`.
- El historial del feature branch no se preserva en main.
- **Ideal para**: Mantener historial limpio en main. Cada PR = un commit.

### Rebase and fast-forward

```
main:    A---B---C'---D'
              \
feature:       C---D     (C' y D' son rewrites sobre B)
```

- Reaplica cada commit del source sobre el HEAD del target.
- Fast-forward: no crea merge commit.
- El source branch se modifica durante el rebase.
- **Ideal para**: Historial lineal con commits individuales visibles.

### Semi-linear merge (Rebase with merge commit)

```
main:    A---B---C'---D'---M
              \            /
feature:       C'---D'
```

- Rebase + merge commit de dos padres.
- Combina las ventajas de rebase (linealidad) con merge commit (punto de referencia).
- **Ideal para**: Historial semi-lineal, comun en proyectos open source.

### Restricciones de rebase durante PR completion

No se puede hacer rebase si:
- Una policy en la rama target prohibe estrategias de rebase.
- La rama source tiene policies (rebase la modificaria sin pasar por aprobacion).
- Se uso la extension de Merge Conflict para resolver conflictos.

En estos casos, alternativas: rebase local + push, o squash merge.

---

## Revert de un pull request

Para deshacer los cambios de un PR ya completado:

1. Abrir el PR completado.
2. Click en **Revert**.
3. Seleccionar target branch y nombre de la rama de revert.
4. Click en **Revert**.
5. Se crea un nuevo PR con un commit que revierte todos los cambios.
6. Completar el PR de revert para aplicar la reversion.

**Nota**: La rama de revert contiene un solo commit que revierte todos los cambios del PR original (no un commit de reversion por cada commit original).

---

## PR templates

Los PR templates agregan texto automatico a la descripcion de nuevos PRs.

### Crear un template por defecto

- Crear un archivo en el repo en una de estas ubicaciones:
  - `pull_request_template.md` (raiz del repo)
  - `.azuredevops/pull_request_template.md`
  - `docs/pull_request_template.md`

### Templates por rama

- Crear archivos en `.azuredevops/pull_request_template/branches/` con nombre de la rama (ej. `main.md`).

### Templates adicionales

- Crear archivos en `.azuredevops/pull_request_template/` con nombres descriptivos.
- Al crear un PR, seleccionar **Add a template** y elegir de la lista.

---

## Estrategia de branching recomendada

Microsoft recomienda una estrategia simple basada en tres conceptos:

1. **Usar feature branches** para todas las nuevas funcionalidades y bug fixes.
2. **Merge feature branches a main** mediante pull requests.
3. **Mantener main en alta calidad** y siempre en estado deployable.

### Branch permissions adicionales

- Se pueden configurar permisos granulares por rama: quien puede push, force push, crear/eliminar ramas.
- Se puede requerir que los nombres de ramas sigan un patron (folders): ej. `feature/`, `bugfix/`, `release/`.
- Se pueden bloquear ramas (**Lock branch**) para prevenir cambios temporalmente.

---

## Fuentes

- https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies-overview (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/repos/git/pull-requests (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/repos/git/complete-pull-requests (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/repos/git/pull-request-templates (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/repos/git/merging-with-squash (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/repos/git/git-branching-guidance (consultado 2026-09-22)
