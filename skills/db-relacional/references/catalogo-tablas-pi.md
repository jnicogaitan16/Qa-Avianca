# Catálogo de tablas — PI (Payment Integrator)

Fuente: `base_conocimiento/manual-aplicacion-pi.md`. Servidor QA: `az-sqla-piccust-use-qa`.

---

## Pago (núcleo)

| Tabla | Uso QA | Campos / notas |
|---|---|---|
| `PIC_PAYMENT_REQUEST` | Cabecera de pago | `SOURCE`, `SUB_CHANNEL`, `REFUND_CURRENCY`, estado (doc. **I** = en proceso) |
| `PIC_PAYMENT_DETAIL` | Intentos / detalle | `REFUND_REQUEST`, `NUMBER_RETRIES`, FOP, razones |
| `PIC_FOP_PAYMENT_REQUEST` | Forma de pago del request | `FOP` (TR, KR, …), `REFUND_AMOUNT`, `IP`, flag dummy **Y** |
| `PIC_SALE_REPOSITORY` | Venta origen | `CHANNEL`, `PSP` |
| `PIC_SALE_REPOSITORY_HISTORY` | Réplica histórica | Sin validaciones extra (manual) |
| `PIC_VOUCHER` | Voucher generado | `EXPIRE_DATE`, `ACTIVATION_DATE` |
| `PIC_BANK_DATA_INFORMATION` | Datos bancarios / IBAN | `BANK_ACCOUNT_NO`, `BANK_CODE` |
| `PIC_SUPPORT_FILE` | Adjuntos del pago | |
| `PIC_PAYMENT_REQUEST_VF` | VF desde SR | Estado **P** pagado |
| `PIC_PAYMENT_DETAIL_VF` | Detalle VF | FOP KR / NC |

## Plantillas, tesorería, rechazos

| Tabla | Uso |
|---|---|
| `PIC_TEMPLATE_CONFIG_DOWNLOAD` | Config de plantillas de pago |
| `PIC_CONTROL_DOWNLOAD_TEMPLATE_MANUAL_PAYMENT` | Control de descargas |
| `PIC_LOG_EVENT_FILE` | Eventos de archivo (`created_date`) |
| `PIC_LOG_RECORDS_CONTAINET_FILE` | Registros contenidos en archivo |
| `PIC_TEMP_TREASURY` | Staging de cargue tesorería |
| `CODES_REJECTION_REASON` | Motivos de rechazo |
| `TEMP_SECOND_FORM_OF_PAYMENT_RULES` | 2ª FOP / Ley DOT (`SALE_CHANNEL`) |
| `PIC_PARAM_STATUS_RETRIES` | Reintentos vs estado |

## SAP

| Tabla / SP | Uso |
|---|---|
| `PIC_SAP_INTERFACE_OUT` | Salida cash / bancaria a SAP |
| `PIC_SAP_ACM_INTERFACE_OUT` | ACM; `TRX_NUMBER`; estado **I** en proceso |
| `PIC_SEND_SAP_INTERFACE` | SP envío |
| `PIC_RETURN_SAP_INTERFACE` | SP retorno SAP |
| `PIC_AZFHISTMAINT_DATA_DELETE` | SP limpieza histórica |

## Logs y auditoría

| Tabla / SP | Uso |
|---|---|
| `PIC_LOGS_TRANSACTION` | Log general (`log_msn`, `created_user`) |
| `PIC_SP_USER_DATA_QUERY` | SP reporte usuarios |

## Maestras `[master]` / `[adm]`

`MST_PARAMETERS`, `MST_PAYMENT_PROCESS_WAY`, `MST_PAYMENT_PROCESSOR`, `MST_PAYMENT_PROVIDER`, `MST_PAYMENT_RETRIES`, `MST_CHANNEL`, `MST_CHANNEL_FOP_ADDITIONAL`, `MST_FRANCHISE`, `MST_MANUAL_TEMPLATES_PAY_PROCC`, `MST_IATA_ACM`, `MST_BANK`, `MST_SCREEN_FIELD_BANK`, `MST_IDENTIFICATION_TYPE`, `MST_TYPE_PERSON`, `MST_ACCOUNT_TYPE`, `MST_COUNTRY`, `MST_STATE`, `MST_CITY`, `MST_CURRENCY`, `MST_INTERNAL_EMAILS`, `MST_USER`, `MST_ROL`, `MST_MENU`

---

## Queries documentadas (filtrar)

```sql
-- Trio clásico post-plantilla / cargue
SELECT * FROM [rfd].[PIC_FOP_PAYMENT_REQUEST] WHERE /* refund / tkt */;
SELECT * FROM [rfd].[PIC_PAYMENT_REQUEST]      WHERE /* misma clave */;
SELECT * FROM [rfd].[PIC_SALE_REPOSITORY]      WHERE /* misma clave */;

SELECT * FROM [rfd].[PIC_PAYMENT_DETAIL] WHERE REFUND_REQUEST = @req;

-- VF
SELECT * FROM [rfd].[PIC_PAYMENT_REQUEST_VF];
SELECT * FROM [rfd].[PIC_PAYMENT_DETAIL_VF];

-- Rechazos
SELECT * FROM [az-sqla-piccust-use-qa].[rfd].[CODES_REJECTION_REASON];

-- Tesorería
SELECT * FROM [rfd].[PIC_TEMP_TREASURY];
SELECT * FROM [rfd].[PIC_LOG_EVENT_FILE] ORDER BY created_date DESC;

-- SAP ACM
SELECT * FROM [rfd].[PIC_SAP_ACM_INTERFACE_OUT];

-- 2ª FOP
SELECT * FROM [rfd].[TEMP_SECOND_FORM_OF_PAYMENT_RULES]
WHERE SALE_CHANNEL IN (/* canal */);

-- Parámetros
SELECT * FROM [master].[MST_PARAMETERS] WHERE parameter_code IN (/* código del caso */);
```

Estados vistos en el manual (no es lista cerrada):

- **I** — en proceso (request / SAP ACM)
- **P** — pagado (VF + NTC)
- **V**, **T** — casos que toma `az-fapp-picsap-use-qa` hacia SAP
- FOP: **TR** tarjeta, **KR** voucher/credits, **CR** cash/transferencia, **NC** ACM

---

## ⚠️ No verificado

- Diccionario completo de estados de `PIC_PAYMENT_REQUEST`
- PK unificada (`REFUND_REQUEST` vs agrupación de tiquetes)
- Columnas no citadas en el capítulo de APIs / tablas
