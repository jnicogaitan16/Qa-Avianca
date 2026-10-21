# Esquemas y reglas SQL para QA — Refund

Motor documentado: **Azure SQL**. Cuatro bases lógicas (SR, AVR, PI, ROR), no un único catálogo.

---

## Servidores y Functions (QA)

| Producto | SQL Server (QA) | Functions documentadas |
|---|---|---|
| AVR | `az-sqla-avref-use-qa` | `az-fapp-avrefpurge-use-qa` (inactivación + Purge) |
| PI | `az-sqla-piccust-use-qa` | `az-fapp-picpaystatus-use-qa`, `az-fapp-picsap-use-qa`, `az-fapp-picvalidpaystat-use-qa`, `az-fapp-picretrypayment-use-qa` |
| SR | ⚠️ nombre SQL **no verificado** | `az-fapp-sprefprocess-use-qa` (inactivación + Load File cada 10 min), `az-fapp-sprefhistmaint-use-qa` |
| ROR | `az-sqla-orqrules-use-qa` | ⚠️ Functions **no verificadas** (despliegue por Mauro) |

Consultas cruzadas documentadas desde PI hacia AVR:

```sql
-- Ejemplo de patrón documentado en PI
JOIN [az-sqla-avref-use-qa].[rfd].[AVR_TEMPLATE_CONFIGURATION] CONF
  ON NOTIF.TEMPLATE_ID = CONF.TEMPLATE_ID
```

No inventar linked servers.

---

## Esquemas

| Esquema | Uso en los manuales |
|---|---|
| `[rfd]` | Transaccional de reembolsos/pagos/logs |
| `[master]` | Maestras y parámetros (`MST_*`) |
| `[adm]` | Usuarios, roles, menús |

Prefijos de tablas transaccionales:

- SR: `SP_REF_*`, `SR_*`
- AVR: `AVR_*`
- PI: `PIC_*`
- ROR: el log documentado es `[rfd].[LOGS_TRANSACTION]` (sin prefijo `ROR_`). SPs: `ROR_DEACTIVITY_USER`, `ROR_USERS_FOR_NOTIFICACION_OF_INACTIVITY`. El SP de auditoría citado es `[rfd].[AVR_SP_USER_DATA_QUERY]` (⚠️ prefijo AVR).

Tablas `AVR_*` y `PIC_*` pueden consultarse **desde el otro producto** cuando el manual lo dice (pasajeros AVR desde SR/PI; VF PI desde SR/AVR).

---

## Reglas de scripts entregables

1. Un script = una pregunta de prueba (“¿quedó Pagado?”).
2. `WHERE` obligatorio en tablas de hecho.
3. Preferir columnas nombradas en el manual; si no hay lista, `SELECT *` + `WHERE` + nota.
4. No commitear datos personales reales; usar radicados de QA.
5. `EXEC` de SPs de consulta de usuarios está documentado. No inventar parámetros.

SPs de auditoría (mismo patrón, distinto nombre):

```sql
EXEC [rfd].[SR_SP_USER_DATA_QUERY];   -- SR
EXEC [rfd].[AVR_SP_USER_DATA_QUERY];  -- AVR (también citado en el manual ROR)
EXEC [rfd].[PIC_SP_USER_DATA_QUERY];  -- PI
```

SPs PI de interfaz (solo mencionar si el caso es SAP; no ejecutar a ciegas):

- `[rfd].[PIC_SEND_SAP_INTERFACE]`
- `[rfd].[PIC_RETURN_SAP_INTERFACE]`
- `[rfd].[PIC_AZFHISTMAINT_DATA_DELETE]`

---

## Inactivación de usuarios (SR, AVR, PI, ROR)

Parámetros en `[master].[MST_PARAMETERS]`:

`PRE_INACTIVATION_NOTIFICATION`, `SUBJECT_EMAIL_INACTIVATION_NOTIFICATION`, `TEMPLANE_NAME_INACTIVATION_NOTIFICATION`, `USER_INACTIVITY_DAYS`

```sql
SELECT [email], [FIRST_NAME] + ' ' + [LAST_NAME], [last_login_date]
FROM [adm].[MST_USER]
WHERE DATEDIFF(DAY, [last_login_date], GETDATE()) = 80;
```

Logs:

- SR: `[rfd].[SP_REF_LOGS_TRANSACTION]` `created_user = 'SP_DEACTIVITY_USER'`
- AVR: `[rfd].[AVR_LOGS_TRANSACTION]` `created_user = 'AVR_DEACTIVITY_USER'`
- PI: `[rfd].[PIC_LOGS_TRANSACTION]` (mismo PBI 982297)
- ROR: `[rfd].[LOGS_TRANSACTION]` `created_user = 'ROR_DEACTIVITY_USER'`; SPs `[rfd].[ROR_DEACTIVITY_USER]` y `[rfd].[ROR_USERS_FOR_NOTIFICACION_OF_INACTIVITY]`

---

## Retención (manuales)

| Recurso | Retención |
|---|---|
| SR Files Processed / DB SR | 1 año |
| Log App Insights (SR, AVR, PI) | 90 días |
| Log App Insights ROR | 30 días |
| ROR DB | 1 año |
| AVR DB operacional | 3 años |
| AVR Hist | 2 años |
| PI DB | 24 meses |
| PI Hist | años 2–5; se puebla desde el mes 25 |

---

## Anti-patrones

- Inventar `STATUS = 'SUCCESS'` si el manual dice `P`, `Pagado`, `REJECTED`, `I`.
- Usar `SP_REF_*` en la base PI o `PIC_*` en SR sin que el flujo lo cruce.
- Scripts de “limpieza” de QA no pedidos.
