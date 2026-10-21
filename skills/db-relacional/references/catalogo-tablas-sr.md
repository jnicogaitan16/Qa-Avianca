# Catálogo de tablas — SR (Special Refund)

Fuente: `base_conocimiento/manual-aplicacion-sr.md`. Solo objetos citados ahí.

---

## Transaccionales `[rfd]`

| Tabla | Para qué sirve en QA | Campos / notas documentadas |
|---|---|---|
| `SP_REF_LOAD_MASSIVE_REQUEST` | Cargue masivo: filas a enviar a LoadMassive | `PROCESSED`, `ERROR_REASON`, `LOADED_BY`, `CREATED_DATE`, `send_attempt` |
| `SP_REF_LOGS_TRANSACTION` | Log de procesos / inactivación / cambios masivo | `created_user`, `created_DATE` |
| `SR_MISSING_VALUE_REFUNDS_VF` | Caso VF (cabecera) | `STATUS`, `APPROVAL_DATE`. Estados: Pendiente de autorización, Autorizado, En progreso, Pagado, `REJECTED` |
| `SR_MISSING_VALUE_REFUND_STATUS_LOG_VF` | Historial de estados VF | Se inserta una línea por cambio de estado |
| `SR_EXCHANGE_RATES` | TRM para umbral Coordinador/Gerente | Conversión a USD vs `MST_APPROVAL_RANGE` |
| `PIC_PAYMENT_REQUEST_VF` | Destino en PI al aprobar todos los TKT | El manual SR dice que **al pasar a PI** se escriben estas tablas |
| `PIC_PAYMENT_DETAIL_VF` | Detalle de pago VF en PI | Junto con la anterior |
| `AVR_INFORMATION_PASSENGER` | Pasajeros (BD AVR) | SR consulta `az-sqla-avref-use-qa` |
| `AVR_INFORMATION_ADDITIONAL_PASSENGER` | Pasajeros adicionales | Igual |

## Maestras `[master]` / `[adm]`

| Tabla | Uso |
|---|---|
| `MST_PARAMETERS` | Inactivación, FOP VF (`MVR_FOP_LIST`), CPG (`MVR_CPG_FILTER_LIST`), estados masivo (`MVR_FINAL_STATUSES`, `MVR_SEND_FAILED_STATUS`, `MVR_PIC_SEND_SUCCESS_STATUS`) |
| `MST_CHANNEL` | Canal de solicitud VF |
| `MST_MISSING_REASONS` | Razón del faltante. `UPDATED_DATE` al modificar |
| `MST_APPROVAL_RANGE` | 0–3500 USD Coordinador; >3500 Gerente |
| `MST_USER` | Usuarios / last_login_date |
| `Master.EMD_NUMBER` | Destino de API EmdEndpoints |
| `CUR_CURRENCY_COUNTRY` | Moneda en PI (SR la consulta) |
| `MST_SCREEN_FIELD_BANK` | Campos bancarios en PI |

## Stored procedure

```sql
EXEC [rfd].[SR_SP_USER_DATA_QUERY];
```

---

## Queries documentadas (copiar y filtrar)

```sql
-- Parámetros VF
SELECT *
FROM [master].[MST_PARAMETERS]
WHERE parameter_code IN (
  'MVR_FINAL_STATUSES',
  'MVR_SEND_FAILED_STATUS',
  'MVR_PIC_SEND_SUCCESS_STATUS'
);

-- Masivo
SELECT PROCESSED, ERROR_REASON, LOADED_BY, CREATED_DATE
FROM [rfd].[SP_REF_LOAD_MASSIVE_REQUEST]
WHERE LOADED_BY = @usuario  -- ajustar
ORDER BY CREATED_DATE DESC;

-- VF por solicitud
SELECT *
FROM [rfd].[SR_MISSING_VALUE_REFUNDS_VF]
WHERE /* filtrar por número de solicitud / tiquete documentados en UI */;

SELECT *
FROM [rfd].[SR_MISSING_VALUE_REFUND_STATUS_LOG_VF]
WHERE /* misma clave */;
```

Estados VF (manual §7.2.4.4):

1. **Pendiente de Autorización** — registrado
2. **Autorizado** — aprobado; espera TKT hermanos
3. **En progreso** — enviado a PI *(el relato §7.2.4.2.1 dice **En proceso** al enviar a PI — CONTRADICCIÓN; verificar literal en BD)*
4. **Pagado** — PI notificó a SR
5. Fallo de envío a PI → vuelve a **Pendiente de Autorización**
6. Rechazo → `STATUS = REJECTED` + `APPROVAL_DATE`

Roles de **aprobación** documentados: Coordinador (0–3500 USD), Gerente (>3500). El rol de quien **radica** no está nombrado (solo “usuario que radica”, precargado).

---

## ⚠️ No verificado

- Nombre del servidor SQL de SR
- PK exacta de `SR_MISSING_VALUE_REFUNDS_VF` (el manual habla de número de solicitud + tiquete en UI)
- Lista completa de columnas de masivo más allá de las citadas
