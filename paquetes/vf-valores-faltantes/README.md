# Paquete VF — SR → PI → AVR NTC (calibrado)

Flujo de **Valores Faltantes**. Entregable para ejecutar **a mano en UI QA**. Los `SELECT` cierran el paso; no disparan el flujo.

| Pieza | Archivo | Se ejecuta en |
|---|---|---|
| Casos Gherkin | `gherkin/vf.feature` | UI SR / PI / correo |
| SQL de cierre | `sql/verificacion-vf.sql` | Azure SQL **después** de cada paso UI |
| Colección | `postman/Refund-VF-GetCurrencyList-NTC.postman_collection.json` | Postman/Newman — solo APIs con contrato |
| Environment | `postman/Refund-QA.postman_environment.json` | QA |
| Calibración | `CALIBRACION.md` | Lectura (qué se rebuscó) |

## Orden de ejecución

1. UI SR: radicar VF (`specialrefundqa.avtest.ink`).
2. Correr bloque SQL «Post-radicación».
3. UI SR: aprobar o rechazar (Coordinador / Gerente).
4. Correr bloque SQL «Post-aprobación» o «Post-rechazo».
5. Esperar/gestionar pago en PI (no hay path documentado para dispararlo por API).
6. Correr bloque SQL «Post-pago».
7. Opcional: Newman `GetCurrencyList` + NTC **solo** si ya llenaste `{{sendgridPath}}` y la solicitud existe en AVR.

## No hacer

- No usar `LANG_CODE`, `SEND_DATE` ni `NOTIF.REFUND_REQUEST` en SQL.
- No inventar requests de radicar/aprobar/MissingModules.
- No asumir el literal `En progreso` vs `En proceso`: ver ambos en BD.

## Pendiente (swagger / DBA)

Cuando tengas paths, actualizar `skills/postman/references/apis-refund.md` y `{{sendgridPath}}` en el environment.
