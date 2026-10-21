# PBI-1338371 — Casos de prueba: Ajuste WB/mapeo Capa Media → GetRefundRTS (Paso 4 Consult a Refund)

- **Carpeta:** PBI-1338371
- **State:** Design
- **Related work:** PBI 1338371, PBI 849436, PBI 696154, PBI 788917, PBI 696222, PBI 766356, PBI 812967
- **Evidencias:** Con fecha y hora en cada ejecución
- **Excel:** `test-cases/PBI-1338371/PBI-1338371-casos-de-prueba.xlsx`
- **Servicio bajo prueba:** Capa Media (ESB Orquestador Consult a Refund, Paso 4) que consume AVR `GetRefundRTS`
- **Servicio AVR (QA):** `POST https://azwappavrefsextsuseqa.az-asev3-use-qa.appserviceenvironment.net/api/v1/GetRefundRTS`
- **Traducciones (#788917):** API `ListHomologation` — Swagger ROR QA. El log observa `getTranslation` (⚠️ no es el nombre del PBI ni del manual).
- **WB:** `IWB_Channel-6_4-Consult_Refund-Consult_Refund-Payment_RTS_V2.xlsx`
- **Tags:** AVR, ROR, ESB
- **Técnicas ISTQB:** partición de equivalencia (`lang`, `channel`) + tabla de decisión (homologación R / A / C)

---

## Alcance de este PBI (delta)

El PBI **no crea** Consult a Refund ni GetRefundRTS. Ajusta el **WB y el mapeo** del servicio de Capa Media que ya obtiene una solicitud RTS vía AVR (#849436), Paso 4 del orquestador (#696154).

Lo que sí cambia (texto del PBI):

1. Request y response de Capa Media: nombres de campos y **campos nuevos en la respuesta**, según el WB V2.
2. Traducir por #788917: `refund-status-descrip`, `fop-description`, `refcal-refund-reason-descrip`, `refcal-refund-reject-descrip`.
3. Para `refund-status-descrip`, el valor enviado a ROR es el **ESTADO_CAPA MEDIA**: R→R, A→A, **P→C**.

**Nota del PBI (corte de alcance):** *«La funcionalidad no tiene cambios adicionales. Las demás características se mantienen de acuerdo con lo definido en los PBIs relacionados.»*

Eso descarta re-probar prioridad de radicaciones, sumas de `summarize-payment`, Blob, reintentos, cola de logs y el mapeo BD campo-a-campo que ya cubre GetRefundRTS.

### Contrato request WB (pegado 2026-10-20)

| ESB | AVR `GetRefundRTS` | Valores WB | Mandatoriedad WB |
|---|---|---|---|
| `refund-request` | `station` = 5 primeros; `controlNumber` = desde el 6.º | string concatenado | Y (si consulta por n.º de solicitud, `station` y `controlNumber` mandatorios en AVR) |
| `pnr` | *(sin mapeo a GetRefundRTS)* | string, longitud 6 | — |
| `ticket` | `document` | string, longitud 13 | Columna **Y**. Comentario: "Opcional si tiene PNR". ⚠️ CONTRADICCIÓN en el WB |
| `channel` | *(no mapea a GetRefundRTS)* | int **1, 10, 4, 6** | — |
| `lang` | *(no mapea a GetRefundRTS; va al traductor)* | **"EN","ES"** | — |
| — | `status` | se envía vacío | Opcional; no se usa |

El **response WB no está** en el repo: los esperados de salida se limitan a lo que el PBI nombra (los 4 `*-descrip`, homologación) y a `1120`/`info-success` ya vistos en logs. No se inventan nombres de campos del WB response.

### Homologación (Nota 2 del PBI)

| ESTADO_AVIANCA | ESTADO_RTS | ESTADO_CAPA MEDIA | ESTADO_ZENDESK | ESTADO_CANAL |
|---|---|---|---|---|
| RECHAZADO | RECHAZADO (R) | R | Resuelto | Solicitud rechazada |
| Autorizado | Aceptado (A) | A | Abierto | Solicitud en proceso de pago |
| PAGO EXITOSO | PAGADO (P) | C | Resuelto | Pago exitoso |

El PBI pega "PAGO EXISTOSO"; se usa **PAGO EXITOSO** (tabla de canal). La homologación aplica al **valor enviado a ROR** para traducir `refund-status-descrip`, no a redefinir la lógica AVR de `REF_STA_DET`.

---

## Casos de prueba (este PBI)

| # | Nombre del caso de prueba | Pasos | Resultado | Resultado ejecución |
|---|---|---|---|---|
| 1 | PBI-1338371 #TC Mapeo request Capa Media → GetRefundRTS | 1. POST ESB Consult a Refund: `refund-request` = STATION+CTL_NUM sin guion (solicitud existente), `ticket`="", `pnr` null/omitido, `channel` ∈ {1,10,4,6}, `lang`: "ES".<br>2. En RTS verificar: `station` = 5 chars, `controlNumber` = resto, `document` = null, `status` = "".<br>3. POST: mismo `refund-request` + `ticket` de 13 dígitos de esa solicitud. En RTS: `station` + `controlNumber` + `document` poblado (`ticket` ESB → `document` AVR).<br>4. Guardar ambas respuestas con fecha y hora. Un `channel` representativo basta (partición válida WB). `pnr` no se espera en GetRefundRTS. | Capa Media rutea a RTS. Primer POST: parseo 5+resto, `status` vacío, `1120` + nodo `info-success`. Segundo POST: `document` = ticket enviado. No se re-prueban las 3 combinaciones de filtro AVR (eso es #849436). | **Parcial.** Parseo también en canal: `BOGWE851922` → `BOGWE-851922` (`channel=1`, `lang=EN`, `1120`). Sigue sin POST con `ticket` y sin body RTS de este radicado (`status`/`document`). |
| 2 | PBI-1338371 #TC Homologación R / A / C y traducción de los 4 campos | 1. Identificar en AVR una solicitud `REF_STA_DET='R'`, una `'A'` y una `'P'` (tabla de decisión: 3 reglas del PBI).<br>2. POST cada una con `lang`: "ES" y `channel` válido.<br>3. En el request al traductor (#788917) verificar el `status` enviado: R→`"R"`, A→`"A"`, P→**`"C"`** (no `"P"`).<br>4. En el response a canal: los 4 campos `refund-status-descrip`, `fop-description`, `refcal-refund-reason-descrip`, `refcal-refund-reject-descrip` vienen del traductor cuando el valor origen existe; si el origen viene vacío, el `*-descrip` queda vacío.<br>5. Opcional: `SELECT * FROM [master].[MS_HOMOLOGATION_REFERENCE_VALUES] WHERE REFERENCE_VALUE_ORIG IN ('R','A','C')`.<br>6. Guardar las tres respuestas con fecha y hora. | Cada regla de homologación se cubre una vez (ISTQB tabla de decisión). `refund-status-descrip` corresponde al ESTADO_CAPA MEDIA enviado a ROR, en español. Los otros tres `*-descrip` se traducen vía #788917. El PBI no redefine si el `refund-status` del canal queda raw (`P`) o homologado (`C`): se registra lo que devuelva Capa Media. | **Parcial.** Canal `BOGWE-851922`: `refund-status=C`, `refund-status-descrip=Successful payment` (EN). Los 4 `*-descrip` vienen; `fop-description` queda `UATP` (igual al raw). Reject **sí** viene en un C (`There is a bank claim`). Sin log RTS de este POST (no se ve el `status` enviado a ROR). **Sin R ni A.** |
| 3 | PBI-1338371 #TC Parámetro lang EN vs ES | 1. Misma solicitud `REF_STA_DET='P'` (o `'A'`) con FOP y razón poblados.<br>2. POST `lang`: "ES" → guardar los 4 `*-descrip` y los raw (`refund-status`, `fop`, `refcal-refund-reason`, `refcal-refund-reject`).<br>3. POST la misma solicitud con `lang`: "EN" → guardar los mismos campos.<br>4. Guardar ambas respuestas con fecha y hora. `lang=PT` no es valor WB: no es caso de este TC. | Particiones válidas WB: EN y ES (un representante cada una). Los `*-descrip` cambian de idioma. Los raw no cambian. | **Parcial.** Mismo `BOGWE1843964`: ES `Pago exitoso` / `Cancelación de vuelo` vs EN `Successful payment` / `Flight cancellations`. Raw `KR` y `Flight cancellations` no cambian. `fop-description=Voucher` igual en ES y EN (ese FOP no distingue idioma en el log). `lang=PT` (ej3) traduce pero está fuera del WB. |
| 4 | PBI-1338371 #TC Campos nuevos del response (los 4 `*-descrip`) vs WB | 1. Usar un POST exitoso del TC2 (lang ES).<br>2. Verificar que existen en el response: `refund-status-descrip`, `fop-description`, `refcal-refund-reason-descrip`, `refcal-refund-reject-descrip`.<br>3. No se recorre header / info-payment / summarize-payment campo a campo (eso es #849436). Cuando se pegue la tabla **response** del WB, completar solo nombres **nuevos o renombrados** de esa hoja. | Los 4 campos de la Nota 1 están en el response de Capa Media. El resto de nombres espera el WB response. | **Pass.** Response Capa Media `BOGWE851922` (`lang=EN`): están `refund-status-descrip`, `fop-description`, `refcal-refund-reason-descrip` y `refcal-refund-reject-descrip`. El resto de nombres (`info-tiquete`, `response-msn`, `total-payment`, `pax-firstname`) no se juzga: WB response no pegado. |
| 5 | PBI-1338371 #TC Traductor ROR no disponible — la consulta no se cae | 1. Consulta válida (mismo body del TC1 paso 1) con el traductor indisponible o sin homologación para el valor.<br>2. Guardar respuesta con fecha y hora. | Riesgo de la Nota 1 (dependencia nueva). El PBI no define el fallback: se registra el comportamiento. Hipótesis a confirmar: `response-code` de consulta sigue 1120 y los `*-descrip` vacíos; no se toma como esperado oficial hasta verlo. | **No ejecutado.** |

---

## Fuera de alcance de PBI-1338371

No se diseñan ni se cierran en este PBI. La nota del PBI los deja en los relacionados. Un hallazgo incidental no convierte el tema en caso de **este** PBI.

| Tema (antes en la suite de 11) | Por qué no va aquí | PBI / fuente que sí lo cubre |
|---|---|---|
| Tres combinaciones Station+Ctl / +Document / solo Document | Filtros de GetRefundRTS, no un cambio de este WB | #849436 + AVR §10.2 líneas 517–520 |
| Prioridad si el tkt está radicado más de una vez (último P / último R) | Lógica AVR existente | #849436 + AVR §10.2 líneas 524–537 |
| Mapeo completo header / tickets / payment vs BD | GetRefundRTS ya mapea esas columnas | #849436 + AVR §10.2 líneas 583–636 |
| Agrupación `summarize-payment`, SUM `VAL_AUT`/`FAR_AMT`/`TAX_AMT_ADJ`, Blob `comprobantes-de-pago` | Funcionalidad que el PBI dice que **se mantiene** | #849436 + AVR §10.2 líneas 638–659 |
| Constantes `CHANNEL_RTS`/`DOCUMENT_TYPE_RTS`, `is-commission`, `ORIGINAL_TICKET`, pax | Derivados AVR existentes | AVR §10.2 líneas 540–543, 603, 611 |
| Probar `channel` 1, 10, 4 y 6 por separado | Una sola partición válida (int del conjunto WB); un representante cubre EP | WB request de este PBI — cubierto en TC1 con un valor |
| Request inválido, tkt inexistente, sin `AVR_DAT_PAYMENT_HISTORY`, `1110` | Manejo de error del flujo ya definido | #696154 / #849436 |
| Reintento AVR (máx. 1) y campos de cola `LOG_REFUND` | El PBI 1338371 no los menciona | #696222 |
| `response-message` concatenado con `\|` como caso propio | Es formato WB; se mira al pasar en TC1/TC4, no justifica un TC de negativos | WB V2 (response no pegado) |

**Hallazgo incidental (no es TC de 1338371):** en los logs, `authorized-value` ≈ `refcal-refund-amount` × n líneas de impuesto (BOGWE ×4, WBATC ×2, BOGFF ×6). El esperado SUM(`VAL_AUT`) es de AVR §10.2, no de este PBI. Si se reporta, el related work es **#849436**, no 1338371.

---

## Datos mínimos para cerrar lo que falta

| Qué | Para qué |
|---|---|
| Un POST con `ticket` de 13 dígitos (mismo radicado BOGWE o WBATC) | Cierra TC1 mapeo `ticket`→`document` |
| Un radicado `REF_STA_DET='R'` y uno `'A'`, `lang=ES` | Cierra reglas R y A del TC2 |
| Pegar la tabla **response** del WB V2 | Cierra TC4 (solo campos nuevos/renombrados) |
| Traductor caído o valor sin homologación | Cierra TC5 |

Queries (solo cierre de este PBI):

```sql
-- Elegir data R / A / P
SELECT STATION, CTL_NUM, REF_STA_DET
FROM [rfd].[AVR_DAT_REQUEST_DET]
WHERE REF_STA_DET IN ('R','A','P');

-- Homologación ROR (opcional TC2)
SELECT *
FROM [master].[MS_HOMOLOGATION_REFERENCE_VALUES]
WHERE REFERENCE_VALUE_ORIG IN ('R', 'A', 'C');
```

---

## Calibración

| Afirmación | Fuente buscada | Resultado | Acción |
|---|---|---|---|
| Este PBI ajusta WB/mapeo Capa Media → AVR GetRefundRTS (Paso 4) | Texto PBI 1338371 pegado por el usuario | CONFIRMADO | Suite recortada al delta |
| «La funcionalidad no tiene cambios adicionales» | Texto PBI 1338371 | CONFIRMADO | TC3/7/8/9/10/11 de la suite anterior → fuera de alcance |
| 4 campos `*-descrip` vía #788917 | Nota 1 del PBI | CONFIRMADO | TC2 y TC4 |
| Homologación P→C (valor a ROR) | Nota 2 del PBI | CONFIRMADO | TC2 tabla de decisión, 3 reglas |
| `lang` EN/ES | WB request PBI | CONFIRMADO | TC3. Un representante por partición (ISTQB EP) |
| `channel` 1,10,4,6 | WB request PBI | CONFIRMADO | Un valor en TC1; no 4 TCs |
| `ticket` ESB → `document` AVR | WB request PBI | CONFIRMADO | TC1 paso 3 |
| Parseo `refund-request` 5+resto | WB request PBI | CONFIRMADO | TC1 |
| `status` vacío | WB request PBI | CONFIRMADO | TC1 |
| `pnr` mapea a GetRefundRTS | WB request (lado AVR vacío) | SIN RESPALDO | No se espera en body RTS |
| Tres filtros AVR (Station+Ctl / +Doc / Doc) | AVR §10.2 517–520 | CONFIRMADO como **AVR**, no como delta 1338371 | Fuera de alcance |
| Prioridad multi-radicación | AVR §10.2 524–537 | CONFIRMADO como AVR | Fuera de alcance |
| SUM `authorized-value` = VAL_AUT | AVR §10.2 | CONFIRMADO como AVR | Hallazgo incidental; no TC de este PBI |
| Reintentos / cola logs | PBI #696222 (citado, no pegado) | TOMADO DEL PBI relacionado | Fuera de alcance |
| Path REST `ListHomologation` | `manual-aplicacion-ror.md` | ⚠️ SIN RESPALDO de path — swagger + nombre | No se inventa path |
| `getTranslation` | log RTS | SIN RESPALDO en manual/PBI | Se registra como observado |
| Fallback si ROR cae | PBI 1338371 | SIN RESPALDO | TC5: registrar comportamiento, no esperado oficial |
| Tabla response WB | WB V2 response | SIN RESPALDO | TC4 limitado a los 4 campos de la Nota 1 |
| Nombre `PBI-XXXXX #TC Título` | `lineamientos-qa.md` | CONFIRMADO | 5 casos |
| Un Case = un escenario | `prompts/plantillas/02-test-plan-suite-case.md` | CONFIRMADO | 5 escenarios de **este** PBI |
| Los 4 `*-descrip` en response Capa Media `BOGWE851922` | Nota 1 del PBI vs JSON canal | CONFIRMADO | TC4 **Pass** |
| `info-tiquete` / `response-msn` / `total-payment` / `pax-firstname` | AVR §10.2 usa `info-tickets` / `response-message` / `summarize-payment` / `pax-first-name` | CONTRADICCIÓN canal vs AVR; WB response SIN RESPALDO | No Fail de TC4 |
| `authorized-value` 11099998 vs `refcal-refund-amount` 1585714 × 7 impuestos | AVR §10.2 SUM VAL_AUT | CONFIRMADO el desvío | Incidental; no TC de 1338371 |

---

**Fuentes técnicas:** `skills/qa-funcional/references/tecnicas-diseno-casos.md` (EP + tabla de decisión), `skills/db-relacional/references/catalogo-tablas-avr.md`, `skills/db-relacional/references/catalogo-tablas-ror.md`, `skills/postman/references/apis-refund.md`  
**Fuentes del producto:** `base_conocimiento/manual-aplicacion-avr.md` §10.2, `base_conocimiento/manual-aplicacion-ror.md`, `base_conocimiento/lineamientos-qa.md`  
**Fuente del contrato:** texto PBI 1338371 (usuario) + WB request pegado 2026-10-20  
**Skills involucrados:** qa-funcional, db-relacional, postman, orquestador-validador
