# Formato de línea observado

No hay una sola gramática. El primer paso es decir qué dialecto es el fragmento. Si una línea no calza en ninguno, se conserva en "no parseadas". No se descarta y no se fuerza al molde del otro pod.

| Dialecto | Cómo se reconoce | Ids por línea |
|---|---|---|
| A — orquestador Consult refund | Logger `ws-refund-orchconsultrefund`. Mensajes `received request`, `consuming url` | Dos |
| B — check refund RTS | `CamelLogEipName` o el campo AMQ `pod` = `ws-refund-checkrefundrts`. El logger de negocio viene truncado `ws-refund-`. Mensajes `Request:`, `Request RTS:`, `Response getInfoRTS` | Uno |

El pod no se deduce solo del logger. En el dialecto B el logger está cortado; el nombre sale del arranque (`camel.main.globalOptions.CamelLogEipName`) o de `"pod"` en el body AMQ.

## Dialecto A — línea de negocio

```
YYYY-MM-DD HH:mm:ss,SSS [hilo] NIVEL  logger - idPrimario - idSecundario - mensaje
```

| Pieza | Hecho en la muestra | Regla de lectura |
|---|---|---|
| Timestamp | `2026-10-20 00:00:01,741` con coma en los milisegundos, sin zona | Se copia tal cual. No se convierte a UTC |
| Hilo | `executor-thread`, `Camel (camel-1)`, `AmqpProvider :(` | El hilo no es la clave de la traza |
| Nivel | `INFO` en negocio | Un `WARN` o `ERROR` de negocio sí entra al cotejo |
| Logger | `ws-refund-orchconsultrefund` o `JmsConnection` | Identifica el pod o la librería, no el salto |
| Ids | Dos tokens separados por ` - ` | Pueden ser iguales, uno vacío, o uno de hilo y otro de negocio |
| Mensaje | Texto y, a veces, JSON en la misma línea | El JSON embebido se extrae del primer `{` al cierre balanceado |

Id secundario vacío, como en `5C6A -  - building log message`, es un hecho: esa línea todavía no está anclada al id de negocio. La línea siguiente que trae los dos ids hace de enlace.

## Dialecto B — línea de negocio

```
YYYY-MM-DD HH:mm:ss,SSS [hilo] NIVEL  logger - id - mensaje
```

| Pieza | Hecho en la muestra `ws-refund-checkrefundrts` (2026-09-24) | Regla |
|---|---|---|
| Timestamp | `2026-09-24 12:21:21,311`, coma en milisegundos, sin zona | Se copia tal cual |
| Hilo | `main`, `executor-thread`, `Camel (camel-1)`, `AmqpProvider :(` | El hilo no es la clave |
| Logger | `ws-refund-`, `AzureKeyva`, `CamelBoots`, `quarkus`, `JmsConnect` | `ws-refund-` no es otro aplicativo: es el mismo pod truncado |
| Id | Un solo token | No inventar un id secundario |
| Mensaje | A veces solo el rótulo (`Request:`, `Request RTS:`, `Response getInfoRTS`) | El JSON va en las líneas siguientes |

El JSON del dialecto B suele empezar en la línea de abajo, con espacios delante, y dejar una línea en blanco después del `}`. Esas líneas no tienen prefijo de log: pertenecen al rótulo anterior. No abrir otra traza por el blanco.

## Arranque

Banner de Quarkus, `AzureKeyva` recuperando llaves, resumen de Camel y la lista `Routes startup` son **ruido de arranque**. No entran a una traza de negocio.

- La lista de rutas (`direct://getInfoRTS`, `direct://getTranslation`, `direct://getTicketsTranslation`, …) prueba que esas rutas existían al iniciar. No prueba cuál atendió un request.
- Si una línea trajera el valor de una llave o un password, no se copia. En la muestra solo aparece el nombre de la llave.

Un `ERROR` de negocio (`BNS-03`, una excepción durante `Validando response`) sí entra a la traza. La ortografía del nombre de la clase no es un defecto funcional.

## JSON que ocupa varias líneas

Si las líneas siguientes no traen el prefijo `YYYY-MM-DD HH:mm:ss,SSS [` y continúan llaves o comillas, pertenecen al mensaje anterior. Caso visto: `Response getTranslation {` y el objeto en las líneas de abajo, hasta la `}` que cierra.

No cortar el objeto en la primera línea.

## Dump Java

```
infoTicketList: [InfoTiquete(document=2022489408706, paxFirstname=..., infoTaxes=[InfoTaxes(taxCode=DG, ...)], infoPayment=[InfoPayment(fop=CR, ...)])]
```

No es JSON. Reglas:

- El nombre antes de `(` es el tipo (`InfoTiquete`, `InfoTaxes`, `InfoPayment`).
- Los pares son `campo=valor`.
- `null` sin comillas es null. Un valor vacío entre comas (`penaltyType=,`) es string vacío.
- Listas anidadas usan `[...]`.
- Los nombres suelen ir en camelCase (`paxFirstname`). El JSON del mismo flujo usa kebab-case (`pax-firstname`). Son representaciones distintas. Se cotejan los **valores**. La diferencia de nombre se reporta como representación, no como campo ausente, salvo que el oráculo exija el nombre JSON dentro del dump.

## Ruido Datadog

```
[dd.trace YYYY-MM-DD HH:mm:ss:SSS +0000] [dd-trace-processor] WARN datadog.trace.agent.common.writer.ddagent.DDAgentApi - Error while sending ...
```

| Diferencia con la línea de negocio | Uso |
|---|---|
| Prefijo `[dd.trace`, milisegundos con `:`, zona `+0000` | No es la hora de la transacción de refund |
| No trae correlation id de negocio | No se une a ninguna traza |
| Texto "Will not log warnings for 5 minutes" | Un aviso cada cinco minutos es coherente con esa frase. No es una inconsistencia de negocio |

El conteo `Total / Received / Sent / Failed` se resume en ruido. No se traduce a un defecto del orquestador de reembolsos.

## Línea cortada

Una última línea que termina a mitad de un id, de un JSON o de una palabra marca el fragmento como **parcial**. Los saltos que habrían ido después no se dan por ausentes: son HUECO.
