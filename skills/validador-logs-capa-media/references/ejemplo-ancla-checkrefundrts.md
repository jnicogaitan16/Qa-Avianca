# Ancla: fragmento check refund RTS (2026-09-24)

Muestra del pod `ws-refund-checkrefundrts`. El logger de las líneas de negocio sale truncado (`ws-refund-`). El nombre del pod está en el arranque (`CamelLogEipName`) y en el body AMQ (`pod`). Sirve para calibrar el dialecto B. **No es el contrato** de GetRefundRTS ni del orquestador Consult refund.

No se copian correos, nombres, tarjetas ni cuentas de la muestra.

## Qué no se mezcla

`BOGWE1843964` puede aparecer también en un log de `ws-refund-orchconsultrefund`. Mismo radicado, otra traza, otro pod, otra fecha. No se pegan los saltos de un pod en el id del otro.

El banner, Key Vault y `Routes startup` son ruido. Las rutas `direct://getInfoRTS`, `direct://getTranslation`, `direct://getTicketsTranslation` y las de estado general o summary quedan como hecho de arranque. Un request no se asigna a una de ellas si la línea de negocio no la nombra.

## Cadena de la traza que consulta por número (`…0007`)

Hora de la línea `Request:`: `2026-09-24 12:21:21,311`.

1. Entrada: `refund-request` `BOGWE1843964`, `channel` 10, `lang` `ES`. No vienen las claves `ticket` ni `pnr`.
2. Rótulo `Consuming Service Mozart...`.
3. `Request RTS:` `station` `BOGWE` (5), `controlNumber` `1843964`, `document` null, `status` `""`.
4. `Rest getInfoRTS`, `Rest Code 200`. El host no está impreso.
5. `Response getInfoRTS`: `response-code` `INF-SV-0000`, `refund-request` `BOGWE-1843964`, `info-tickets[].refund-status` `P`, `channel` `RTS`, `fist-name` presente.
6. Tres `Request traductor` con el mismo rótulo. Bodies distintos: `status` `G7`; luego `ticket` `C` y `status` `C`; luego los dos documentos con `status` `C`, `refund-reason` `Flight cancellations`, `fop` `KR`.
7. `Response :::` de canal: `response-code` `1120`, nodo `info-success`, `refund-status` `C`, `refund-status-descrip` `Pago exitoso`.
8. Id siguiente `…0008`, confianza MEDIA: AMQ `channel` `"99"`, `ticket` `BOGWE1843964`, `message` `success`.

## Hechos que el método debe marcar

| Hecho | Clase en esta muestra | Por qué |
|---|---|---|
| Rótulo Mozart y cuerpo `Request RTS` / `getInfoRTS` | INCONSISTENCIA de rótulo | Manda el body. No se dice que llamó a Mozart |
| `BOGWE1843964` → `station` `BOGWE` + `controlNumber` `1843964`, `document` null, `status` `""` | CONFIRMADO contra el paso 2 del TC de mapeo, si ese es el oráculo | Un representante. No repite el caso para otro radicado solo por no estar en este archivo |
| La entrada no trae la clave `ticket` | HECHO distinto de `ticket: ""` | Si el caso pide `""`, se deja la diferencia. No se reescribe el body RTS |
| `getInfoRTS` devuelve `refund-status` `P` y el `Request traductor` manda `status` `C` | HECHO del salto, relevante si el caso pide P→C hacia el traductor | El log dice `getTranslation`, no `ListHomologation`. No se equiparan |
| `Response :::` trae `1120` y el nodo `info-success` | CONFIRMADO si el esperado del primer POST nombra esos dos | Es este pod y este radicado. No se copia a otro JSON que no los traiga |
| Consultas solo con `info-ticket[].tkt-number` (`…0003`, `…0005`): `document` = tiquete, `station` null, `controlNumber` null | HECHO del filtro "solo document" | Fuera del paso que pide el mismo `refund-request` más el tiquete. No cierra ese paso |
| Esas consultas y `HVCMD2279` (`…0001`) vuelven `Rest Code 400`, `INF-SV-0001`, y el canal `1110` / `Failed` | HECHO del camino de error | Fuera de alcance si el caso lo deja en el PBI del error. No es Fail del mapeo feliz |
| AMQ del éxito lleva `channel` `"99"` y el del error lleva `"10"` | INCONSISTENCIA observada entre trazas de este pod | La cola no es el esperado del mapeo RTS salvo que el caso la nombre |
| `Response getInfoRTS` usa `response-message` y números entre comillas (`penalty-amount` `"0"`); `Response :::` cambia tipos (`0.0`) y `sale-total` a notación científica del mismo valor | INCONSISTENCIA de representación entre saltos | No se recorre campo a campo si el caso lo deja fuera de alcance |
| `authorized-value` `481480` frente a dos `refcal-refund-amount` `120370` | HECHO ya tratado como incidental de otro PBI | No abre un caso de 1338371 |
| La traza `…0009` se corta en `Rest Code 400` | Fragmento parcial de esa traza | El response que seguiría es HUECO. Las trazas ya cerradas con "Mensaje enviado a la cola" no quedan parciales por eso |
