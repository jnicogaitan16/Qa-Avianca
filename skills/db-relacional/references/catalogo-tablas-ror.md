# Catálogo de tablas — ROR (Refund Orchestration Rules)

Fuente: `base_conocimiento/manual-aplicacion-ror.md`. Servidor QA: `az-sqla-orqrules-use-qa`.

Solo objetos nombrados en el manual. Si falta columna, `SELECT * … WHERE` + ⚠️.

---

## Servidor y esquemas

| Dato | Valor documentado |
|---|---|
| SQL QA | `az-sqla-orqrules-use-qa` |
| Esquemas | `[rfd]`, `[master]`, `[adm]` |
| Retención DB | 1 año |
| Diseño | Transaccional de **baja actualización, alta consulta** |

No hay Functions Azure nombradas en el manual ROR (el despliegue va por Mauro).

---

## Tablas

| Objeto | Uso documentado | Columnas / filtro citados |
|---|---|---|
| `[adm].[MST_USER]` | Usuarios; inactivación y reporte | `email`, `FIRST_NAME`, `LAST_NAME`, `last_login_date`. Ordenar por `last_login_date` para confirmar deshabilitados |
| `[master].[MST_PARAMETERS]` | Parámetros de inactivación | `parameter_code` ∈ `PRE_INACTIVATION_NOTIFICATION`, `SUBJECT_EMAIL_INACTIVATION_NOTIFICATION`, `TEMPLANE_NAME_INACTIVATION_NOTIFICATION`, `USER_INACTIVITY_DAYS` |
| `[rfd].[LOGS_TRANSACTION]` | Log de inactivación | `created_user = 'ROR_DEACTIVITY_USER'`; ordenar por `created_DATE` |
| `[master].[MS_HOMOLOGATION_REFERENCE_VALUES]` | Homologaciones (API ListHomologation) | `REFERENCE_VALUE_ORIG` (request swagger: `ReferenceValueOrig`) |
| `[master].[MST_EMD]` | Maestra EMD / TM.EMD | Campos de UI: Código, Nombre ES/EN/PT, Rfisc, Libro, Tipo, Descripción, Reembolso. ⚠️ Una nota escribe `Master.MST.EMD` |

Campos del reporte de usuarios (salida del SP, no lista de columnas SQL): username, nombre del responsable, número de identificación, estado (activo / bloqueado / inactivo u otro), roles, fecha de creación, última modificación, último acceso, tipo (directo o tercero). Metadatos del informe: query usada, número de registros, fecha/hora de generación.

---

## Stored procedures

| SP | Qué hace el manual |
|---|---|
| `[rfd].[ROR_DEACTIVITY_USER]` | Inactiva usuarios sin login en 90 días (PBI 982297) |
| `[rfd].[ROR_USERS_FOR_NOTIFICACION_OF_INACTIVITY]` | Notifica a los que cumplen 80 días sin ingreso |
| `[rfd].[AVR_SP_USER_DATA_QUERY]` | Reporte auditoría de usuarios (PBI 1151866). ⚠️ El prefijo es AVR; está citado así en el manual ROR |

```sql
USE [az-sqla-orqrules-use-qa];
GO
DECLARE @return_value int;
EXEC @return_value = [rfd].[ROR_DEACTIVITY_USER];
SELECT 'Return Value' = @return_value;
GO
```

```sql
USE [az-sqla-orqrules-use-qa];
GO
DECLARE @return_value int;
EXEC @return_value = [rfd].[ROR_USERS_FOR_NOTIFICACION_OF_INACTIVITY];
SELECT 'Return Value' = @return_value;
GO
```

```sql
EXEC [rfd].[AVR_SP_USER_DATA_QUERY];
```

---

## Queries de verificación (QA)

Usuarios próximos a inactivar (80 días):

```sql
SELECT [email], [FIRST_NAME] + ' ' + [LAST_NAME], [last_login_date] AS [NAME]
FROM [adm].[MST_USER]
WHERE DATEDIFF(DAY, [last_login_date], GETDATE()) = 80;
```

Usuarios deshabilitados / último login:

```sql
SELECT *
FROM [adm].[MST_USER]
ORDER BY last_login_date ASC;
```

Log de inactivación:

```sql
SELECT *
FROM [rfd].[LOGS_TRANSACTION]
WHERE created_user = 'ROR_DEACTIVITY_USER'
ORDER BY created_DATE ASC;
```

Cierre API ListHomologation:

```sql
SELECT *
FROM [master].[MS_HOMOLOGATION_REFERENCE_VALUES]
-- si se filtró: WHERE REFERENCE_VALUE_ORIG = @valor
;
```

Cierre API EmdGetRfisc / maestra UI:

```sql
SELECT *
FROM [master].[MST_EMD]
-- filtrar por el código EMD de la prueba (campo UI «Código» / request «Emdcode»)
;
```

---

## Qué no inventar

- Prefijo `ROR_*` en tablas transaccionales (el log se llama `LOGS_TRANSACTION`, no `ROR_LOGS_TRANSACTION`).
- `ROR_SP_USER_DATA_QUERY` — el manual nombra el SP de AVR.
- Columnas de `MST_EMD` o de homologación más allá de las citadas.
- Linked server desde ROR hacia SR/AVR/PI.
- Host SQL PRE/POST.
