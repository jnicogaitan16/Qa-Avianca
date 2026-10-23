# Cotejo de campos, textos y arrays

Se aplica a cada path del oráculo y a cada diferencia entre saltos de la misma traza.

## Hechos de un campo

Para cada path anotar:

| Hecho | Valores posibles |
|---|---|
| Presencia | presente, ausente |
| Tipo | object, array, string, number, boolean, null |
| Valor | literal, o longitud si es dato personal |
| Representación vacía | `null`, `""`, clave ausente, `[]` |

Esos cuatro vacíos no se tratan como el mismo resultado. Si el oráculo dice `null` y el log trae `""`, es INCONSISTENCIA. Si el oráculo dice "vacío" sin literal, se dejan los dos literales y no se elige uno.

## Path

Notación con punto y corchetes: `info-consultrefund.info-success[0].info-taxes[1].tax-code`.

- Si el array tiene N elementos, un path sin índice obliga a mirar **todos** los elementos.
- Un campo presente en unos elementos y ausente en otros es INCONSISTENCIA de esquema dentro del array. Se listan las claves que no comparten todos los ítems.
- El orden de un array solo se juzga cuando el oráculo exige un orden. Si no, el orden no es defecto.

## Entre saltos

Recorrer la cadena de la traza y, para cada campo que aparece en más de un salto, registrar:

| Qué cambió | Ejemplo visto en la muestra ancla (no es la regla del servicio) |
|---|---|
| El rótulo del paso no coincide con el body | `Consuming Service Mozart...` y la línea siguiente es `Request RTS` / `getInfoRTS`. Manda el body y el nombre Rest |
| Se agregó una clave | el body hacia Mozart añade `level` y no trae `pnr` |
| `null` pasó a `""` | `ticket: null` en la entrada y `ticket: ""` en el body |
| El mismo concepto cambió de nombre | `response-msn` en un response y `response-msg` en el siguiente; `lang` en la entrada y `lan` en el body de traducción |
| El mismo nombre cambió de tipo | `document` string en el primer response y array de objetos en el response de pax |
| Un array del response no alimenta el paso siguiente | `infoTicketList` con documentos y el body de traducción con `ticket: ""` |
| El mensaje de cola no lleva el documento | `Response AMQ` con `ticket: "LOGIC"` mientras `original-ticket` es `LOGIC` y `document` trae el número |

Cada fila se clasifica con la tabla del SKILL. Sin oráculo, la fila queda como hecho o INCONSISTENCIA observada. No se promueve a bug.

## Arrays

Comprobar, en este orden:

1. El path existe y el tipo es array.
2. Longitud. `[]`, null y clave ausente se distinguen.
3. Esquema común de los ítems (mismas claves). Las claves extra de un ítem se listan, no se ignoran.
4. Tipos internos estables (`info-taxes[]`, `refund-fops[]`, `document[]`, `documents-conj[]`).
5. Si el oráculo da un valor, que ese valor esté en el ítem indicado. Si no indica índice, que esté en al menos uno, y decir en cuál.
6. Cruces de longitud: N documentos en un salto, N entradas en el dump, N tokens en un campo concatenado del AMQ. Si las longitudes no coinciden, INCONSISTENCIA, citando los dos conteos. No inventar el elemento que falta.

Un array pretty-print o un dump anidado cuenta como el array. No hace falta que quepa en una línea.

## Textos

- Comparación literal, con mayúsculas y espacios. `Success` y `success` son literales distintos. Si el oráculo no fija la caja, se reportan los dos y no se elige.
- Un código (`1120`, `G1`, `U`, `A`, `C`) se copia como string si llegó entre comillas y como número si llegó sin comillas.
- Una frase de log (`no tickets to translate`, `Omiting pic web service consume`) es un hecho del texto. Una falta de ortografía del log no es un defecto funcional.
- El flag `Exists ticket with allowed refund status and description` se lee en el paso en que se imprimió. No se contradice con una lista que el log imprime **después**, salvo que el oráculo diga que miran lo mismo. La lista de estados permitidos no se inventa: si el log no la imprime, es HUECO.

## Qué no es inconsistencia

- Dos trazas distintas con datos distintos.
- Un campo de más en el response que el oráculo no menciona.
- Ruido Datadog.
- Un promedio de timing distinto de la resta de timestamps de la traza.
- El nombre camelCase del dump frente al kebab-case del JSON, cuando el valor es el mismo.
