# Catálogo de tablas — AVR (AV Refund)

Fuente: `base_conocimiento/manual-aplicacion-avr.md`. Servidor QA: `az-sqla-avref-use-qa`.

---

## Transaccionales `[rfd]`

| Tabla | Para qué sirve en QA | Campos documentados |
|---|---|---|
| `AVR_DAT_REQUEST_ENC` | Encabezado de solicitud | `STATION`, `CTL_NUM`, `REF_EMA`, `AGE_NAM`, `CLA_NAM`, `CLA_MID`, `CLA_LNA`, `LM_NUMBER`, `BANK_ACCOUNT_NUM`, `BANK_NAME`, `ACC_TYP` |
| `AVR_DAT_REQUEST_DET` | Detalle por documento | `car_num_cod`, `doc_num`, `FAR_AMT`, `CUR_COD`, `SALE_TOTAL`, `SALE_CURR_CODE`, `SER_CHA_AMT`, `AGT_COM_AMT`, `CURR_COD_PROC`, `REQ_DAT`, `REF_REA`, `VAL_AUT`, `REF_STA_DET`, `MET_PAY_FOP`, `CARD_NUMBER`, `CARD_EXP_DATE`, `CARD_APV_CODE`, `CARD_FRA_CODE`, `VOU_NUMBER` |
| `AVR_DAT_REQUEST_TAXES` | Impuestos | `TAX_COD`, `TAX_AMT_ADJ` |
| `AVR_DAT_PAYMENT_HISTORY` | Histórico de pago | `DATE_REG` |
| `AVR_DAT_PROCESS_HISTORY` | Histórico de proceso | (citada, sin columnas) |
| `AVR_INFORMATION_PASSENGER` | Owner / reserva | `PNR`, `REFUND_REQUEST` |
| `AVR_INFORMATION_ADDITIONAL_PASSENGER` | Pax adicionales | `NAME_PAX`, `LAST_NAME_PAX`, `TOUR_CODE`, `ORIGINAL_TICKET`, `REFUND_REQUEST` |
| `AVR_TYPE_OF_NOTIFICATIONS` | Tipos NTC | `NOTIF_TYPE_CODE`, `NOTIF_TYPE_NAME` |
| `AVR_TEMPLATE_CONFIGURATION` | Plantillas SendGrid | `TEMPLATE_ID`, `NOTIF_TYPE_CODE` |
| `AVR_SUBJECT_TABLE` | Asuntos por idioma | Textos NTC23/24 |
| `AVR_CONTROL_NOTIFICATIONS` | Envíos realizados | `TEMPLATE_ID` (join a templates) |
| `AVR_LOGS_TRANSACTION` | Logs / inactivación | `created_user`, `created_DATE` |
| `PIC_PAYMENT_REQUEST_VF` | Trigger NTC23/24 | Estado final **P**, FOP KR o NC |
| `PIC_PAYMENT_DETAIL_VF` | Igual | Junto a la anterior |

## Maestras

| Tabla | Uso |
|---|---|
| `MST_PARAMETERS` | Inactivación; `purge_time`; `purge_scope_days` |
| `MST_TAX_CODE` | Impuestos (menú Maestras) |
| `MST_USER` | Usuarios |

## Stored procedure

```sql
EXEC [rfd].[AVR_SP_USER_DATA_QUERY];
```

---

## Queries documentadas

```sql
-- Consulta tu Reembolso / existencia de solicitud
SELECT * FROM [rfd].[AVR_DAT_REQUEST_ENC]  WHERE /* STATION + CTL_NUM */;
SELECT * FROM [rfd].[AVR_DAT_REQUEST_DET]  WHERE /* documento / request */;
SELECT * FROM [rfd].[AVR_DAT_REQUEST_TAXES];
SELECT * FROM [rfd].[AVR_DAT_PAYMENT_HISTORY];
SELECT * FROM [rfd].[AVR_DAT_PROCESS_HISTORY];
SELECT * FROM [rfd].[AVR_INFORMATION_PASSENGER] WHERE REFUND_REQUEST = @req;
SELECT * FROM [rfd].[AVR_INFORMATION_ADDITIONAL_PASSENGER] WHERE REFUND_REQUEST = @req;

-- Notificaciones
SELECT * FROM [rfd].[AVR_TYPE_OF_NOTIFICATIONS];
SELECT * FROM [rfd].[AVR_TEMPLATE_CONFIGURATION];
SELECT * FROM [rfd].[AVR_SUBJECT_TABLE];

SELECT *
FROM [rfd].[AVR_CONTROL_NOTIFICATIONS] NOTIF
JOIN [az-sqla-avref-use-qa].[rfd].[AVR_TEMPLATE_CONFIGURATION] CONF
  ON NOTIF.TEMPLATE_ID = CONF.TEMPLATE_ID
JOIN [az-sqla-avref-use-qa].[rfd].[AVR_TYPE_OF_NOTIFICATIONS] TYP
  ON CONF.[NOTIF_TYPE_CODE] = TYP.[NOTIF_TYPE_CODE];

-- Purge
SELECT * FROM [master].[MST_PARAMETERS] WHERE parameter_code = 'purge_time';
SELECT * FROM [master].[MST_PARAMETERS] WHERE parameter_code = 'purge_scope_days';
```

`refund-request` de APIs NTC = concatenación `STATION` + `CTL_NUM` (con guion, según mapeo GetRefundRTS).

Purge: casos sin update de cliente; timeout **30 minutos** (arquitectura). Function `az-fapp-avrefpurge-use-qa`.

---

## NTC relevantes a VF

| Código | Nombre | Condición documentada |
|---|---|---|
| NTC19 | Completa tus datos bancarios | Cash sin datos bancarios |
| NTC23 | Pago exitoso VF voucher | VF en PI estado P + FOP KR |
| NTC24 | Pago exitoso VF ACM | VF en PI estado P + FOP NC |

---

## ⚠️ No verificado

- Lista completa de `REF_STA_DET`
- PK de ENC (se infiere STATION + CTL_NUM)
- Tabla física de Purge (el proceso existe; el nombre de tabla de timeout no está explícito más allá del registro que envía el orquestador)
- Columnas `LANG_CODE`, `SEND_DATE`, `AVR_CONTROL_NOTIFICATIONS.REFUND_REQUEST`: **no usar** hasta confirmarlas en BD. El join documentado solo cita `TEMPLATE_ID` y `NOTIF_TYPE_CODE`.
