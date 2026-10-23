# Oráculos: parámetros y PBI

El cotejo no arranca hasta decir cuál de estas tres situaciones aplica.

## 1. Parámetros del mensaje

El usuario puede pasar prosa o un bloque. Se respetan sus palabras. Campos reconocidos:

```yaml
traza: ""                 # correlation id, completo o sufijo único
refund-request: ""
ticket: ""
pod: ""
saltar_ruido: true
saltos:                     # opcional; si viene, solo se juzgan estos
  - entrada
  - body-downstream
  - response
  - dump
  - traduccion
  - amq
esperado:
  - salto: entrada
    path: refund-request
    tipo: string
    valor: "RFOPS48657"     # ausente = solo presencia y tipo
    obligatorio: true
  - salto: response
    path: info-success
    tipo: array
    min_items: 1
```

Reglas:

- `valor` presente: igualdad literal.
- `tipo` presente y `valor` ausente: se juzga el tipo y la presencia.
- `min_items` / `max_items`: solo la longitud.
- Un path que el usuario no listó no se usa para dar Pass o Fail. Puede aparecer como inconsistencia interna si los saltos se contradicen.
- Si el usuario pega un JSON esperado, cada hoja del JSON es un `esperado` de presencia, tipo y valor. Las claves que el JSON esperado no trae no se exigen.

## 2. PBI o caso

1. Abrir `test-cases/PBI-XXXX/casos-de-prueba.md`. Si no existe, decirlo y no inventar el esperado.
2. Si nombró un `#TC`, usar solo esa fila (pasos, resultado esperado, resultado de ejecución).
3. Si nombró el PBI entero, recorrer cada caso y marcar cuál toca el log. Un caso cuyo disparador no aparece en el fragmento es HUECO de ese caso, no un Fail.
4. Respetar la sección "Fuera de alcance" de ese archivo. Un hallazgo de un tema fuera de alcance se anota aparte y no cierra ni tumba el caso.
5. Si el caso cita un manual (§, tabla, campo), abrir ese archivo y buscar el string. No confirmar de memoria. El resultado de esa búsqueda entra a la calibración del orquestador.
6. El estado de ejecución ya escrito en el caso (Parcial, Pass) no sustituye al log. El log de este turno manda.

## 3. Sin oráculo

Se entrega la cadena de saltos y las inconsistencias internas. La frase de cierre es: no hay oráculo; esto no cierra un caso ni abre un bug.

## Qué pedirle al usuario si falta y el log no se puede aislar

Solo si hay varias trazas y el usuario no dijo cuál importa:

- correlation id, `refund-request` o ticket
- el caso o la lista de campos

Si pegó un solo request reconocible, se analiza ese y se listan las otras trazas por id, sin cotejarlas a fondo.

## Paso al bug

Si una afirmación del caso queda en INCONSISTENCIA contra el oráculo, el draft dice:

- caso
- path y salto
- literal esperado
- literal visto
- id y timestamp de la línea

No rellena severidad, Activity ni el título del bug. Eso lo hace `qa-funcional` con `lineamientos-qa.md` cuando el usuario pida reportarlo.

## Paso a SQL o a la colección

Si el caso pide un cierre en BD o un body HTTP que el log no trae, el draft lo marca HUECO y nombra el skill (`db-relacional` o `postman`). No escribe el SELECT ni el path que la fuente no tiene.
