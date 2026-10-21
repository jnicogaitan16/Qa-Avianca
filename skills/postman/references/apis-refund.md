# Catálogo de APIs Refund

Solo endpoints y hosts que aparecen en `base_conocimiento/`. Si falta path o body, marcar **no verificado** y abrir swagger.

Swaggers QA documentados:

| App | URL |
|---|---|
| SR backend (Emd) | `https://azwappsprefbknduseqa.az-asev3-use-qa.appserviceenvironment.net/externalservices/swagger/index.html` |
| AVR external | `https://azwappavrefsextsuseqa.az-asev3-use-qa.appserviceenvironment.net/Swagger/index.html` |
| PI backend | `https://azwapppiccustbknduseqa.az-asev3-use-qa.appserviceenvironment.net/swagger/index.html` |
| PI external | `https://azwapppiccustextsuseqa.az-asev3-use-qa.appserviceenvironment.net/Swagger/index.html` |
| ROR external | `https://azwappsorqrulesextsuseqa.az-asev3-use-qa.appserviceenvironment.net/Swagger/index.html` |

---

## SR — Special Refund

Front QA: `https://specialrefundqa.avtest.ink/`

| API | Qué hace | Persistencia / nota |
|---|---|---|
| **EmdEndpoints** | Inserta EMDs de aeropuertos | Tabla `Master.EMD_NUMBER`. PBI 737197 |
| **GetInfoTicket** | Datos básicos del tiquete | Consumo vía APIM. Si código **1110**: información no encontrada |
| **GetRefundInfo** | Datos del reembolso en pantallas 2–3 | Tickets/EMD, estado, razón |
| **SendRefundInfo** | Envía la solicitud (pantallas 2–4) | Incluye FOP distinta de CR y caso CR + certificación bancaria |
| **GetMasterInfo** | Maestras para formularios (bancos, etc.) | Cruza con tablas PI (`CUR_CURRENCY_COUNTRY`, `MST_SCREEN_FIELD_BANK`) |
| **LoadMassive** | Procesa agrupaciones del cargue masivo | Function `az-fapp-sprefprocess-use-qa` cada 10 min. Tabla `[rfd].[SP_REF_LOAD_MASSIVE_REQUEST]`. Validar **antes** de llamar |
| **GetCurrencyList** | Monedas (VF consume PI) | `https://api-avianca-qa.avtest.ink/API_Refund_PIC/api/GetCurrencyList` y también PI external `/api/GetCurrencyList` |
| **MissingValueRefundStatus/Update** | PI notifica a SR el pago/estado VF | Actualiza `[rfd].[SR_MISSING_VALUE_REFUNDS_VF]` |

Paths REST de GetInfoTicket / GetRefundInfo / SendRefundInfo / LoadMassive: **no verificados** (el manual nombra el servicio, no el path). Usar swagger SR.

---

## AVR — AV Refund

Front QA: `https://azwappavrefsftuseqa.az-asev3-use-qa.appserviceenvironment.net/auth`

| API | Método / path documentado | Contrato |
|---|---|---|
| **SaveSupport** | `…/SaveSupport` | Adjunto base64 + radicado. Max **1 MB**. Formatos: jpg, png, pdf, msg, docx, xlsx. Varios docs por solicitud. Blob `azstaccavrefuseqa` / `soportes-excepciones` |
| **GetRefundRTS** | `GET/POST` `{{baseUrl}}/api/v1/GetRefundRTS` | Filtros: Station + Control Number; Station + Control Number + Document; o Document. Status autorizado/rechazado. Si el tkt está varias veces, devolver el **autorizado** |
| **SendGrid / NTC** | Path REST **no documentado** (solo swagger SendgridEndpoints) | Tipos NTC19, NTC23, NTC24. Campo `notifaction-type` (así en el manual). La solicitud debe existir en AVR. Colección importable: `paquetes/vf-valores-faltantes/postman/` — rellenar `{{sendgridPath}}` cuando exista swagger |

### NTC 19 — Completa tus datos bancarios

```json
{
  "notifaction-type": "NTC19",
  "refund-request": "173192",
  "pnr": "CFN9AC",
  "owner-first-name": "Nikita",
  "owner-last-name": "Ward",
  "email-reservation": "PRUEBASSMTP10@GMAIL.COM",
  "info-tkt": []
}
```

### NTC 23 — Pago VF voucher (KR)

Disparo cuando `[rfd].[PIC_PAYMENT_REQUEST_VF]` y `[rfd].[PIC_PAYMENT_DETAIL_VF]` quedan en estado **P** y FOP **KR**.

Campos documentados del request: `notifaction-type`, `language`, `refund-request`, `refund-status`, `refund-reject-reason`, `pnr`, nombres, `frequent-flyer-num`, `email-reservation`, `subchannel`, `info-tkt[]` (document, document-type, fare-amount, fare-currency, refcal-fare-amount, refcal-currency, penalty, …).

NTC 24: mismo patrón, FOP **NC** (ACM).

---

## PI — Payment Integrator

Front QA: `https://azwapppiccustfrontuseqa.az-asev3-use-qa.appserviceenvironment.net/auth`

| API | Qué hace | Tablas / nota |
|---|---|---|
| **PaymentRequestEndPoint / PaymentOutput** | Recibe solicitud de pago desde Mozart | Canales BSP, LM, TC; control de TKT duplicados |
| **Payment Refund Request** | Solicitud de reembolso a PIC | |
| **GetCurrencyList** | Lista de monedas | Fuente `[master].[MST_CURRENCY]`. APIM: `/API_Refund_PIC/api/GetCurrencyList` |
| **PicTempControl/create** | Carga solicitudes en tabla de control para agrupar | |
| **ControlRequest/Reject** | Rechaza solicitudes en tabla temporal | |
| **GetChargeback** | Consulta contracargos (evitar doble pago) | |
| **Insert Refund Status** | Inserta/actualiza estado de reembolso | |
| **Comprobante de Pago** | Diseño comprobante TR y CR | |
| **Bank_Data_Information** | Datos bancarios / IBAN | `[rfd].[PIC_BANK_DATA_INFORMATION]`, maestras país/banco/cuenta |
| **Check Payment Status** | Estado de pago (+ campo IP) | `[rfd].[PIC_PAYMENT_REQUEST]`, `[rfd].[PIC_PAYMENT_DETAIL]`, `[rfd].[PIC_FOP_PAYMENT_REQUEST]`, `[rfd].[PIC_VOUCHER]` |
| **MissingModules / VF** | Recibe valores faltantes desde SR | `[rfd].[PIC_PAYMENT_REQUEST_VF]`, `[rfd].[PIC_PAYMENT_DETAIL_VF]` |

Voucher Qwikcilver (createVoucher):

- DEV: `https://api-payments-dev.avtest.ink/api_qwikcilver_in/createVoucher`
- QA: `https://api-payments-qa.avtest.ink/api_qwikcilver_in/createVoucher`
- PRD: `https://api-payments.avianca.com/api_qwikcilver_in/createVoucher`

---

## Encadenamiento entre productos

```
SR VF aprueba
  → PI MissingModules / tablas VF
  → PI paga (KR/NC/…)
  → PI → SR MissingValueRefundStatus/Update  (estado Pagado)
  → AVR SendGrid NTC23 (KR) o NTC24 (NC)
```

Una colección de VF debe tener requests en **SR + PI + AVR**, no un solo producto.

---

## ROR — Refund Orchestration Rules

Front QA (no expuesto a internet): `https://azwappsorqrulesfrontuseqa.az-asev3-use-qa.appserviceenvironment.net/auth`

Swagger QA: `https://azwappsorqrulesextsuseqa.az-asev3-use-qa.appserviceenvironment.net/Swagger/index.html`

| API | Qué hace | Persistencia / nota |
|---|---|---|
| **ListHomologation** | Consulta homologaciones (mapeos ARO). Vacío = todos; con valor = un registro | Tabla `[master].[MS_HOMOLOGATION_REFERENCE_VALUES]`. Campo swagger `ReferenceValueOrig` = columna `REFERENCE_VALUE_ORIG`. PBI 659052 |
| **EmdGetRfisc** | Consulta un EMD por código | Tabla `[master].[MST_EMD]` (una nota escribe `Master.MST.EMD`). Campo swagger `Emdcode`. PBI 696040 / 778915 |

Paths REST de ListHomologation y EmdGetRfisc: **no verificados** (el manual nombra la API y el swagger, no el path). Abrir swagger ROR; no inventar `/api/…`.

ROR **no** entra en el encadenamiento VF. Es maestra/homologación para la capa media (APIM).

---

## Qué no inventar

- Subscription key header de APIM (nombre no documentado)
- Bodies de GetRefundInfo / SendRefundInfo / LoadMassive / PaymentOutput
- Hosts PRE/POST
- Timeouts por defecto de los servicios

Si el usuario pide el body: abrir swagger y, si no hay acceso, listar solo los campos que el manual sí nombra.
