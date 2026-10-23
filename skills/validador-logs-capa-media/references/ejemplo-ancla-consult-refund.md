# Ancla: fragmento Consult refund (2026-10-20)

Muestra parcial del pod `ws-refund-orchconsultrefund`. Sirve para calibrar el método. **No es el contrato** del orquestador, de Mozart, de pax ni de la traducción. Otro log puede no traer estos pasos.

Datos de persona, correos, tarjetas y cuentas de esa muestra no se copian aquí.

## Cómo se reensambla

En el mismo segundo arrancan varias claves (`…5C65` a `…5C69`). Cada una tiene su `received request`. El `response` de `5C69` aparece en el archivo antes que el de `5C65`. Se agrupa por id, no por cercanía.

Entrada vista en esas trazas: `refund-request` numérico, `pnr` null, `ticket` null, `channel` 6, `lang` "ES". El log dice `request type is requestNumber` y `numeric request number, consulting in mozart service`. La URL impresa es `consultrefundtktmozart`. Este fragmento no muestra un request a `GetRefundRTS`.

## Hechos que el método debe marcar (clase incluida)

| Hecho | Clase en esta muestra | Por qué |
|---|---|---|
| Entrada `ticket: null` y body hacia Mozart `ticket: ""`; el body agrega `level: 2` y no lleva `pnr` | INCONSISTENCIA observada de representación | No hay oráculo en la muestra que exija conservar null |
| Primer `response` usa `response-msn`; el `response` de pax de la misma traza usa `response-msg` | INCONSISTENCIA de nombre entre saltos | Son dos saltos. No se unifican |
| En el primer response, `document` es string; en el response de pax, `document` es array de objetos | INCONSISTENCIA de tipo entre saltos | Mismo nombre, otro tipo. No es un duplicado del mismo response |
| Dentro de `document[]` de pax, unos ítems traen `emd-code` y `emd-description` y otros no | INCONSISTENCIA de esquema del array | Se listan las claves que no comparten todos los ítems |
| `info-consultrefund.info-success[]` existe en el primer response. El nodo `info-success` del response de pax es otro objeto | HECHO | No se afirma que sean el mismo nodo porque el nombre coincida |
| Trazas con `infoTicketList: []` y el texto `no tickets to translate` | HECHO del paso en que se imprimió | No se niega con documentos aparecidos en un salto anterior |
| La traza que sí arma `infoTicketList` con documentos manda a traducción `ticket: ""` | INCONSISTENCIA entre el dump y el body de traducción | El dump tiene números de documento y el body no los copia |
| El body de traducción usa `lan`, no `lang` | INCONSISTENCIA de nombre frente a la entrada | Solo es defecto si el oráculo exige `lang` en ese body |
| `Response getTranslation` devuelve `status` traducido a un texto | HECHO | No se equipara con `ListHomologation`: el log no usa ese nombre |
| `Response AMQ` trae `ticket: "LOGIC"` (o `LOGIC` repetido) y `refund-amount: null` | HECHO | `original-ticket` en el response previo es `LOGIC`. Defecto solo si el oráculo dice que AMQ.ticket es el número de documento |
| El bloque de timings incluye `rts http service timing average` y la traza no imprime URL hacia RTS | INCONSISTENCIA observada + HUECO | "average" no es la duración de ese id. La llamada RTS no está en el fragmento |
| `Exists ticket … : false` se imprime antes del response de pax | HECHO ordenado | No se contradice con `infoTicketList` posterior sin un oráculo que los ate |
| Líneas `[dd.trace …] Failed to connect to localhost:8126` | RUIDO | Fuera de la traza de refund |
| La última línea del pegado queda cortada | Fragmento parcial | Lo que seguiría es HUECO |

## Cómo se usaría con un PBI

Si el usuario dice que este log cierra el `#TC` de mapeo hacia `GetRefundRTS`:

- El fragmento muestra consulta numérica hacia Mozart, no el body `station` / `controlNumber` / `document` / `status`.
- Esas afirmaciones quedan en HUECO. No pasan a Fail por ausencia.
- `channel` 6 e `lang` ES se confirman solo en la entrada impresa, no en un body RTS que aquí no está.

Si el usuario pasa un `esperado` para el body de traducción (`ticket` igual al número de documento), la fila del dump contra `ticket: ""` pasa a INCONSISTENCIA contra el oráculo.
