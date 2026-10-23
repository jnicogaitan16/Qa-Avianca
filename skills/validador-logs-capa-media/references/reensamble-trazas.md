# Reensamble de trazas

El archivo llega intercalado. Cada transacción se reconstruye sola.

## Clave

Elegir la regla del dialecto. No mezclar ids de pods distintos aunque el `refund-request` coincida: son evidencias del mismo radicado, no la misma traza.

### Dialecto A

1. La clave de negocio es el id de la línea `received request` (en la muestra, los dos ids vienen iguales: `97FF7B7CBEE7718-0000000000005C69`).
2. Toda línea cuyo id primario o id secundario sea esa clave entra a la traza.
3. Una línea con id nuevo y mensaje `building log message` queda en espera. Entra a la traza cuando una línea vecina trae ese id junto a la clave de negocio (`5C6A` enlazado a `5C68` en `Sending to amqp queue`).
4. Prohibido atribuir un `response:` al request que quedó más arriba en el archivo si el id no coincide.

### Dialecto B

1. La clave es el único id de la línea `Request:`.
2. Entran las líneas con ese id (`Request RTS:`, `Rest getInfoRTS`, `Response getInfoRTS`, `Validando response`, `Response :::`).
3. El AMQ de esta muestra usa **el id siguiente** (`…0001` y luego `…0002`) y no repite el id de negocio en la misma línea. Se enlaza solo si el `Body a enviar` queda inmediatamente después del cierre de esa traza y no se cruzó otro `Request:`. Confianza **MEDIA**. Si otro request empezó antes del AMQ, el body de cola queda sin dueño: no se lo asigna al de arriba.
4. El rótulo no gana al cuerpo. `Consuming Service Mozart...` seguido de `Request RTS:` y `Rest getInfoRTS` se lee como salto hacia RTS. El texto "Mozart" es INCONSISTENCIA de rótulo. No se afirma que la llamada fue a Mozart.

## Orden dentro de la traza

Ordenar por timestamp. Si dos líneas tienen el mismo timestamp, conservar el orden en que aparecen en el archivo. No reordenar por "lo que el flujo debería hacer".

## Cadena vista en Consult refund (muestra, no contrato)

En el fragmento ancla, una traza numérica muestra estos pasos, no siempre todos:

1. `Start route - Consult refund orquestator Main Process`
2. `received request` + JSON de canal
3. `request type is requestNumber`
4. `consult refund by request number: <número>`
5. Una de estas dos frases, según lo que la línea imprima. No se intercambian:
   - `numeric request number, consulting in mozart service` → en la ancla de octubre 2026 la URL es `consultrefundtktmozart`
   - `alphanumeric request number, consulting in RTS service` → en la traza `BOGWE851790` del 2026-10-21 la URL es `ws-refund-checkrefundrts` `/checkrefundrts`. El body de ese salto puede ir sin `pnr` y sin `ticket`. El `Request RTS` con `station` / `controlNumber` está en el otro pod, no aquí
6. `consuming url:` + `request body:`
7. `response:` de ese consumo
8. `mapping to refund response`
9. `enrich payload with payment information`
10. `Exists ticket with allowed refund status and description: true|false`
11. `is fop in restricted list: true|false`
12. `Omiting pic web service consume` cuando el fragmento no llama a PIC
13. `enrich payload with pax information`
14. `consuming url:` hacia `consultrefundpaxinfo` + `request body:`
15. Otro `response:` (contrato distinto al del paso 7)
16. `infoTicketList:` (dump Java) y, o bien `no tickets to translate`, o bien `getting Translations` → `Request translation` → `Rest Code` → `Response getTranslation`
17. `Response AMQ:` + `Sending to amqp queue LOG_REFUND` + `Message sent successfully to amq queue`
18. Bloque entre `******************` con timings

Si el pod o el mensaje no es este, no se rellena la cadena con estos pasos. Se listan los que el log imprimió.

## Cadena vista en check refund RTS (muestra, no contrato)

1. `Request:` + JSON de canal (a veces `refund-request`; a veces `info-ticket[].tkt-number`)
2. `Consuming Service Mozart...` (rótulo; ver regla de arriba)
3. `Request RTS:` + JSON `document` / `station` / `controlNumber` / `status`
4. `Rest getInfoRTS duró …` y `Rest Code`
5. `Response getInfoRTS` + JSON
6. `Validando response...`
7. O bien `ERROR` + `Response :::` con el código de canal, o bien una o más tandas `Consumiendo servicio Traductor` / `Request traductor` / `Response getTranslation` y después `Response :::`
8. En el id siguiente: `Body a enviar` hacia `LOG_REFUND` y `Mensaje enviado a la cola satisfactoriamente`

La URL de `getInfoRTS` no viene impresa. No se inventa el host. El nombre del salto es el que dice la línea (`getInfoRTS`), no el rótulo Mozart.

Tres `Request traductor` seguidos, con el mismo texto de log y bodies distintos, son tres saltos. El arranque puede listar `getRefundGeneralStatusTranslation`, `getSummaryStatusTranslation` y `getTicketsTranslation`. Mientras la línea de negocio no diga cuál `direct:` usó, no se asigna.

## Dos response no son un duplicado

El primer `response:` de la traza cuelga del `consuming url` anterior (en la muestra, Mozart). El segundo `response:` cuelga del consumo de pax. Compararlos como si fueran el mismo contrato produce un falso Fail. Se cotejan como saltos distintos y, además, se señala qué campos cambiaron de nombre o de tipo entre ellos.

## Timings

Las líneas `total routing timing average`, `mozart http service timing average`, `rts http service timing average` y `pax http service timing average` dicen **average**. Se reportan como promedio impreso, no como duración de esa correlation id.

Si el promedio nombra un servicio (`rts`) y la traza no tiene un `consuming url` hacia ese servicio, la clase es INCONSISTENCIA observada entre el texto del timing y las URL de la traza. No se concluye que la llamada ocurrió ni que no ocurrió: el fragmento no la muestra. Clase del salto faltante: HUECO. Clase del texto que la nombra sin URL: INCONSISTENCIA observada.

## Cierre

La traza está cerrada en el fragmento solo si hay un mensaje explícito de fin (`Message sent successfully`, el bloque de timings, o el que el pod use). Si el id arranca y el archivo se corta antes, la traza queda **abierta** y todo lo no visto es HUECO.
