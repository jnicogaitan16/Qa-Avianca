# Azure DevOps Boards y Work Items - Referencia

> Resumen basado en documentacion oficial de Microsoft (learn.microsoft.com).
> Fecha de consulta: 2026-09-22.

## Tabla de contenidos

1. [Procesos disponibles](#procesos-disponibles)
2. [Tipos de work items](#tipos-de-work-items)
3. [Jerarquia de work items](#jerarquia-de-work-items)
4. [Campos clave](#campos-clave)
5. [Estados y workflow](#estados-y-workflow)
6. [Queries (consultas)](#queries-consultas)
7. [Tipos de queries](#tipos-de-queries)
8. [Macros en queries](#macros-en-queries)
9. [Shared Queries y permisos](#shared-queries-y-permisos)
10. [Personalizacion de work items](#personalizacion-de-work-items)
11. [Tags (etiquetas)](#tags-etiquetas)
12. [Templates de work items](#templates-de-work-items)
13. [Operaciones practicas frecuentes](#operaciones-practicas-frecuentes)

---

## Procesos disponibles

Al crear un proyecto en Azure DevOps se elige un proceso que determina los tipos de work items disponibles:

| Proceso | Backlog item principal | Notas |
|---------|----------------------|-------|
| **Agile** | User Story | El mas usado. Incluye User Story, Task, Bug, Feature, Epic. |
| **Basic** | Issue | Simplificado. Incluye Issue, Task, Epic. Sin Feature ni Bug dedicado. |
| **Scrum** | Product Backlog Item (PBI) | Sigue terminologia Scrum. PBI, Task, Bug, Feature, Epic. |
| **CMMI** | Requirement | Para entornos que requieren Capability Maturity Model Integration. |

---

## Tipos de work items

### Epic

- Representa una iniciativa estrategica o un cuerpo grande de trabajo.
- Agrupa Features.
- Aparece en el portfolio backlog de Epics.
- Campos destacados: Title, State, Area Path, Iteration Path, Priority, Business Value.

### Feature

- Representa una funcionalidad de negocio entregable.
- Agrupa User Stories / PBIs / Requirements (segun el proceso).
- Aparece en el portfolio backlog de Features.
- Campos destacados: Title, State, Target Date, Priority, Value Area.
- **Nota**: no disponible en el proceso Basic.

### User Story (Agile) / Issue (Basic) / PBI (Scrum) / Requirement (CMMI)

- Es la unidad principal de valor para el cliente.
- Se descompone en Tasks.
- Aparece en el product backlog y en el board (Kanban).
- Campos destacados: Title, State, Story Points (Agile) / Effort (Scrum) / Size (CMMI), Acceptance Criteria, Priority.

### Task

- Unidad de trabajo tecnico asignable a un miembro del equipo.
- Hijo de un User Story / PBI / Requirement.
- Aparece en Sprint backlogs y Taskboards.
- Campos destacados: Title, State, Assigned To, Remaining Work, Original Estimate, Activity.

### Bug

- Representa un defecto en el codigo o producto.
- Configurable por equipo: puede tratarse como Requirement (aparece en product backlog) o como Task (aparece en sprint backlog).
- Campos destacados: Title, State, Repro Steps, System Info, Priority, Severity, Found In (build), Integrated In (build).
- Configuracion: Project Settings > Team configuration > Working with bugs.
- **Nota**: no existe como tipo separado en el proceso Basic (se usa Issue).

---

## Jerarquia de work items

```
Epic
  └── Feature
        └── User Story / PBI / Requirement / Issue
              └── Task
```

La relacion padre-hijo se establece mediante **Parent/Child links**. Esta jerarquia controla como aparecen los items en los backlogs de portfolio.

**Categorias y backlogs:**

| Categoria | Work item type | Backlog / Board que controla |
|-----------|---------------|------------------------------|
| Epic | Epic | Portfolio backlog de Epics |
| Feature | Feature | Portfolio backlog de Features |
| Requirement | User Story / Issue / PBI / Requirement | Product backlog y boards, Sprint backlog |
| Task | Task | Sprint backlog y Taskboard |
| Bug | Bug | Configurable por equipo |

---

## Campos clave

### Campos comunes a todos los work items

| Campo | Descripcion |
|-------|-------------|
| **Title** | Unico campo obligatorio. Max 255 caracteres. |
| **ID** | Asignado automaticamente por el sistema. Unico en la organizacion. |
| **Assigned To** | Persona responsable. Solo un asignado a la vez. |
| **State** | Estado actual del workflow (ej. New, Active, Closed). |
| **Reason** | Razon del ultimo cambio de estado. Se actualiza automaticamente. |
| **Area Path** | Agrupa por producto, funcionalidad o equipo. |
| **Iteration Path** | Agrupa por sprint o entrega temporal. |
| **Priority** | 1 (critica) a 4 (baja). |
| **Description** | Campo de texto enriquecido con la descripcion del item. |
| **Tags** | Etiquetas personalizadas para filtrado. |

### Campos especificos por tipo

| Tipo | Campos notables |
|------|-----------------|
| User Story | Story Points, Acceptance Criteria, Value Area |
| PBI (Scrum) | Effort, Acceptance Criteria, Business Value |
| Bug | Repro Steps, System Info, Severity, Found In, Integrated In |
| Task | Remaining Work, Original Estimate, Completed Work, Activity |
| Epic/Feature | Target Date, Business Value, Time Criticality |

---

## Estados y workflow

Cada tipo de work item tiene un conjunto de estados que varian segun el proceso:

### Agile - User Story

```
New --> Active --> Resolved --> Closed
                                 |
                              Removed
```

### Basic - Issue

```
To Do --> Doing --> Done
```

### Scrum - PBI

```
New --> Approved --> Committed --> Done
                                   |
                                Removed
```

### CMMI - Requirement

```
Proposed --> Active --> Resolved --> Closed
```

**Reglas importantes:**
- Un work item solo puede estar en un estado a la vez.
- Los estados determinan si el item aparece en el backlog (los estados de categoria Completed/Removed ocultan items).
- Se puede arrastrar tarjetas en el board para cambiar estado.

---

## Queries (consultas)

Las queries permiten crear listas filtradas de work items para triaje, actualizaciones masivas, reportes y compartir con el equipo.

### Como crear una query

1. Ir a **Boards > Queries**.
2. Seleccionar **+ New query**.
3. En el editor de queries, agregar clausulas con:
   - **Campo** (Field): ej. `Work Item Type`, `State`, `Assigned To`.
   - **Operador**: ej. `=`, `<>`, `Contains`, `In`, `Was Ever`.
   - **Valor**: ej. `Bug`, `Active`, `@Me`.
4. Combinar clausulas con **AND** / **OR**.
5. Agrupar clausulas con parentesis logicos para consultas complejas.
6. Ejecutar con **Run Query**.
7. Guardar en **My Queries** (privada) o **Shared Queries** (compartida).

### Operadores disponibles

| Operador | Uso |
|----------|-----|
| `=`, `<>` | Igualdad / desigualdad |
| `>`, `<`, `>=`, `<=` | Comparacion numerica o de fecha |
| `Contains`, `Does Not Contain` | Busqueda en texto |
| `Contains Words` | Busqueda por palabras (full-text) |
| `In`, `Not In` | Valor dentro de un conjunto |
| `Was Ever` | El campo tuvo ese valor en algun momento del historial |
| `Is Empty`, `Is Not Empty` | Campos HTML/rich text vacios o con contenido |
| `=[Field]`, `<>[Field]` | Comparacion entre dos campos |

---

## Tipos de queries

| Tipo | Icono | Uso |
|------|-------|-----|
| **Flat list** | Lista plana | Listar items para actualizacion masiva, triaje, graficos. Maximo recomendado: 1000 items para graficos. |
| **Work items and direct links** | Relaciones directas | Encontrar items relacionados, dependencias, items huerfanos (sin padre). Exporta a Excel como lista plana. |
| **Tree of work items** | Arbol | Ver jerarquias padre-hijo. Ideal para visualizar descomposicion de Epics > Features > Stories > Tasks. |

---

## Macros en queries

Las macros permiten filtros dinamicos sin valores fijos:

| Macro | Descripcion |
|-------|-------------|
| `@Me` | Usuario autenticado actual |
| `@Today` | Fecha de hoy. Admite operaciones: `@Today - 7` (hace 7 dias) |
| `@Project` | Proyecto actual |
| `@CurrentIteration` | Iteracion/sprint actual del equipo |
| `@CurrentIteration +/- n` | Iteraciones relativas al sprint actual |
| `@Follows` | Work items que el usuario sigue |
| `@MyRecentActivity` | Items que el usuario modifico recientemente |
| `@RecentMentions` | Items donde el usuario fue mencionado |
| `@StartOfDay`, `@StartOfWeek`, `@StartOfMonth`, `@StartOfYear` | Inicio del periodo. Admite +/- offset |
| `@TeamAreas` | Area paths asignados al equipo |
| `[Any]` | Cualquier valor (ej. `Work Item Type = [Any]`) |

**Nota**: `@CurrentIteration`, `@Follows`, `@MyRecentActivity`, `@RecentMentions`, `@TeamAreas` solo funcionan en el portal web; no se admiten en Excel, notificaciones ni REST API directamente.

---

## Shared Queries y permisos

### My Queries vs Shared Queries

| Aspecto | My Queries | Shared Queries |
|---------|-----------|----------------|
| Visibilidad | Solo el creador | Todos los miembros del proyecto con acceso |
| Ubicacion | Carpeta personal | Carpetas compartidas del proyecto |
| Permisos requeridos | Acceso Basic | Permiso **Contribute** en la carpeta de Shared Queries |

### Gestionar permisos de queries

- Navegar a **Boards > Queries > Shared Queries**.
- Click derecho en carpeta o query > **Security**.
- Asignar permisos: Read, Contribute, Delete, Manage Permissions.
- Se puede restringir por usuario o grupo de seguridad.

### Favoritos

- Marcar queries como favoritas para acceso rapido.
- Disponible tanto en My Queries como en Shared Queries.
- Las queries favoritas aparecen en el selector rapido del menu Queries.

---

## Personalizacion de work items

### En Azure DevOps Services (cloud) - Inherited Process

1. Ir a **Organization Settings > Process**.
2. Crear un proceso heredado del proceso base (ej. hereda de Agile).
3. Dentro del proceso personalizado:
   - **Agregar campos** personalizados a tipos de work items existentes.
   - **Crear nuevos tipos** de work items.
   - **Modificar el layout** del formulario (agrupaciones, paginas).
   - **Agregar/modificar estados** del workflow.
   - **Ocultar tipos** de work items que no se usen.
   - **Agregar reglas** (ej. campo obligatorio cuando State = Active).
4. Asociar el proyecto al proceso personalizado.

### En Azure DevOps Server (on-premises) - XML Process

- Se personaliza editando XML de definicion de proceso.
- Usa `witadmin` o la interfaz de Process Template Manager.
- Mayor flexibilidad pero requiere mas conocimiento tecnico.

---

## Tags (etiquetas)

- Las tags son etiquetas de texto libre que se agregan a cualquier work item.
- Se usan para filtrar backlogs, boards y resultados de queries.
- No hay limite de tags por work item (practicamente).
- Para crear nuevas definiciones de tags, se necesita el permiso **Create tag definition**.
- Las tags se comparten entre work items y pull requests dentro de la organizacion (limite combinado: 150,000 tags unicas).
- Operadores en queries: `Contains` y `Does Not Contain`.

---

## Templates de work items

- Permiten crear work items con campos prellenados.
- Util para tareas repetitivas (ej. template de bug con Area Path y campos estandar).
- Se crean desde el menu **Actions > Templates** en un work item, o desde **Team Settings > Templates**.
- Cada equipo puede tener sus propios templates.
- Se aplican al crear un nuevo work item o al actualizar items existentes en bulk.

---

## Operaciones practicas frecuentes

### Crear un work item

1. **Desde el board**: Click en **+ New Item** en la columna correspondiente.
2. **Desde el backlog**: Click en **+ New Work Item** en la parte superior.
3. **Desde una query**: Click en **+ New Work Item**.
4. **Mediante REST API**: `POST /_apis/wit/workitems/$<type>` (ver referencia REST API).

### Actualizacion masiva (bulk update)

1. Ejecutar una query flat-list.
2. Seleccionar multiples items con Ctrl/Shift + click.
3. Click derecho > **Edit** o usar la barra de herramientas para cambiar campos comunes.
4. Alternativa: exportar a Excel, modificar y publicar cambios.

### Vincular work items

- **Parent/Child**: Jerarquia (Epic > Feature > Story > Task).
- **Related**: Items relacionados sin jerarquia.
- **Predecessor/Successor**: Dependencias de orden.
- **Tested By / Tests**: Enlace a test cases.
- Se vinculan desde la pestana **Links** del work item o al crear un nuevo item vinculado desde el menu **Actions > New Linked Work Item**.

### Discusion y @mentions

- Usar la seccion **Discussion** para agregar comentarios con formato enriquecido.
- `@usuario` para mencionar y notificar.
- `#ID` para vincular a otro work item.
- `!ID` para vincular a un pull request.

### Charts a partir de queries

- Solo se pueden crear charts (pie, bar, pivot, trend) de queries flat-list.
- La query debe devolver maximo 1000 items.
- Los charts se pueden agregar a dashboards.
- Widgets disponibles: Chart for Work Items, Query Results, Query Tile.

---

## Fuentes

- https://learn.microsoft.com/en-us/azure/devops/boards/work-items/about-work-items (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/boards/queries/about-managed-queries (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/agile-process (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/choose-process (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/boards/queries/query-operators-variables (consultado 2026-09-22)
- https://learn.microsoft.com/en-us/azure/devops/organizations/settings/work/customize-process (consultado 2026-09-22)
