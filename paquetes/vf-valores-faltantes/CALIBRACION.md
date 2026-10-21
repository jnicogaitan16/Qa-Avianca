# Calibración — paquete VF

Barrido E contra `manual-aplicacion-sr.md` §7.2.4–7.2.4.4 y `manual-aplicacion-avr.md` §10.4.2–10.4.3.

| Afirmación | Fuente buscada | Resultado | Acción |
|---|---|---|---|
| Rol QA / Analista para radicar | SR §7.2.4.1 “Usuario que radica” | **SIN RESPALDO** | Eliminado. Radica usuario autenticado; rol no nombrado |
| Coordinador 0–3500 USD / Gerente >3500 | SR §7.2.4.2 | **CONFIRMADO** | Casos TC03–TC05 |
| Fecha de Venta mandatoria YYYY-MM-DD | SR tabla de campos §7.2.4.1 | **CONFIRMADO** | Agregada a TC01 |
| Valor faltante ≤ Total venta | SR §7.2.4.1 | **CONFIRMADO** | TC02 negativo |
| Mensaje Guardar | SR §7.2.4.1 | **SIN RESPALDO** | ⚠️ en feature; no se inventa texto |
| Mensajes Aprobar | SR §7.2.4.2.1 | **CONFIRMADO** | Textos literales en TC03 |
| `APPROVAL_DATE = NULL` al radicar | SR (solo se cita el campo al aprobar/rechazar) | **SIN RESPALDO** | No es esperado oficial |
| `LANG_CODE`, `SEND_DATE`, `NOTIF.REFUND_REQUEST` | AVR joins NTC | **SIN RESPALDO** | Fuera del SQL |
| Join NTC por TEMPLATE_ID + NOTIF_TYPE_CODE | AVR / PI queries | **CONFIRMADO** | SQL post-pago |
| En progreso vs En proceso | §7.2.4.4 vs §7.2.4.2.1 | **CONTRADICCIÓN** | Tester anota literal de BD |
| Estados Autorizado, Pagado, REJECTED, Pendiente de Autorización | SR §7.2.4.4 / rechazo | **CONFIRMADO** | |
| Path SendGrid | AVR “swagger SendgridEndpoints” | **SIN RESPALDO** | `{{sendgridPath}}` vacío; pre-request bloquea |
| Path MissingValueRefundStatus/Update | SR §7.2.4.3 nombra el servicio | **SIN RESPALDO** | Sin request en la colección |
| Path MissingModules | PI TOC | **SIN RESPALDO** | Sin request |
| Body NTC23/24 completo | AVR §10.4.2–10.4.3 | **CONFIRMADO** | JSON en la colección (`notifaction-type`, `bank-acount`, `acm-num`) |
| GetCurrencyList + currency-code | SR §7.2.4.1; PI APIM | **CONFIRMADO** | Requests 00-Setup |
| SQL Server SR | — | **SIN RESPALDO** | No se nombra host |

📋 Validación: **PASÓ CON ADVERTENCIAS** (E ejecutada; inventos quitados).
