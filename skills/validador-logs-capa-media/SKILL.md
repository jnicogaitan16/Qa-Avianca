---
name: validador-logs-capa-media
description: >
  Coteja logs de capa media (OpenShift, pods ws-refund-*, Camel, AMQ) contra un PBI o contra parámetros explícitos. Reensambla trazas por correlation id aunque vengan intercaladas, parsea JSON y dumps Java, y detecta inconsistencias de campos, tipos, null, strings vacíos y arrays. Se activa cuando el usuario pega un log, pide validar una respuesta de capa media, comparar saltos (request, body downstream, response), revisar arrays o estructuras, o cotejar un log con un PBI. No responde directo: el draft pasa por orquestador-validador. No inventa contratos que no estén en el PBI, en los parámetros o en el manual citado.
---

# Validador de logs de capa media

## Propósito

Leer un log de capa media, rearmar cada transacción y cotejar datos, textos, campos y arrays contra un oráculo. El oráculo es, en este orden:

1. Los parámetros que el usuario pasa en este mensaje (gana sobre todo lo demás).
2. El PBI o el caso de `test-cases/` que el usuario nombra.
3. El manual o el catálogo solo si el usuario pide cotejar contra esa fuente, o si el caso del PBI ya la cita.

Sin oráculo, el skill igual lee el log y reporta hechos e inconsistencias **internas** (el mismo dato cambia de tipo, de nombre o de valor entre saltos). Eso no es un Fail de caso ni un bug.

Este skill **no responde directo al usuario**. Genera un draft para `orquestador-validador`.

## Cuándo se activa

- El usuario pega un log de OpenShift, de un pod `ws-refund-*`, de Camel o de AMQ.
- Pide validar una respuesta, un request, un body downstream o un array.
- Pide cotejar el log con un PBI, un caso, un JSON esperado o una lista de campos.
- Pregunta por qué un campo se pierde, cambia de tipo, llega vacío, null o deja de ser array.

No se activa para diseñar el caso (eso es `qa-funcional`), armar el request (`postman`) ni escribir el SELECT (`db-relacional`). Si el hallazgo ya contradice el esperado del PBI y piden el bug, el draft deja los hechos y el orquestador activa `qa-funcional`.

## Reglas

0. El log pegado en este mensaje es la única evidencia de este cotejo. No se reutiliza un log anterior, ni `envio_ia.md`, ni un token de la máscara para decidir si un campo llegó. La máscara solo aplica al archivo que podría salir de la máquina. Aquí se leen los valores tal como vienen en el pegado: el mismo correlation id, el request, el body downstream y el response de esa traza.
1. Leer `references/` antes de clasificar. El mapa está al final.
2. El log manda sobre la memoria. Un patrón de la muestra ancla no es contrato de otro pod ni de otro día.
3. No completar un JSON truncado ni un salto que el fragmento no muestra.
4. No declarar bug ni Fail porque dos saltos se vean distintos. Hace falta un oráculo que exija que sean iguales.
5. No equiparar nombres que el log no equipara (`getTranslation` no es `ListHomologation`; `response-msn` no es `response-msg`).
6. En el entregable, redactar email, nombre de persona, tarjeta y cuenta. Conservar `refund-request`, PNR, número de documento, correlation id, códigos y nombres de campo: son la clave del cotejo. Si el defecto es justamente ese dato personal, describir forma y longitud, no el valor.
7. Un fragmento se etiqueta **parcial** si la última línea está cortada, si una traza no tiene cierre, o si el usuario dice que pegó una parte.

## Procedimiento

```
- [ ] 1. Separar ruido de líneas de negocio
- [ ] 2. Parsear cada línea y unir JSON multilínea
- [ ] 3. Reensamblar por correlation id (no leer el archivo como una sola transacción)
- [ ] 4. Extraer el JSON o el dump de cada salto
- [ ] 5. Cargar el oráculo (parámetros, PBI, o ninguno)
- [ ] 6. Cotejar campos, tipos, null / "" / ausente, y arrays
- [ ] 7. Clasificar cada hallazgo
- [ ] 8. Redactar y entregar el draft
```

### 1. Ruido y dialecto

Identificar el dialecto en `references/formato-linea.md` antes de agrupar. Un pod no se lee con la gramática de otro.

Líneas `[dd.trace …]`, el banner de arranque, Key Vault y `Routes startup` van a **ruido**. No se mezclan con la traza. Se mencionan en una línea (cuántas y de qué tipo). Solo se analizan si el usuario pregunta por el arranque o por el agente. Un `ERROR` durante la validación del response es negocio.

### 2. Parseo

Cada línea de negocio aporta timestamp, hilo, nivel, logger, los ids que el dialecto tenga (uno o dos) y el mensaje. El JSON que sigue en líneas sin prefijo de log, aunque arranque en la línea siguiente o deje un blanco al cerrar, pertenece al rótulo anterior. Un dump `Clase(campo=valor, …)` no es JSON: se parsea como texto y se marca representación Java.

Detalle: `references/reensamble-trazas.md`.

### 3. Reensamble

Agrupar por el id de `received request`, `Start route` o `Request:`, según el dialecto. Varias trazas se intercalan; el orden de lectura del archivo no es el orden de una transacción. Dentro de la traza, ordenar por timestamp y, si empatan, por el orden del archivo.

El id de un hilo AMQ puede ser distinto del id de negocio. En el dialecto A el enlace es la línea que trae los dos ids. En el dialecto B el enlace del AMQ es el id siguiente, con la confianza que fija `reensamble-trazas.md`. No fusionar dos pods por compartir `refund-request`. El rótulo del paso no gana al body ni al nombre `Rest` de la línea siguiente.

### 4. Saltos

Un salto es un mensaje con cuerpo (request recibido, request body, response, dump, AMQ). El cuerpo se cuelga del **último paso nombrado en esa misma línea o en la línea previa de la misma traza**, no de "la respuesta" en abstracto. La misma traza puede tener dos `response:` con contratos distintos.

### 5. Oráculo

| Situación | Qué se usa como verdad | Qué no se hace |
|---|---|---|
| El usuario pasa campos, tipos, valores, paths o un JSON esperado | Eso, literal | No se suaviza ni se completa con el manual |
| El usuario nombra `PBI-XXXX` o un `#TC` | Solo las afirmaciones de ese caso en `test-cases/PBI-XXXX/casos-de-prueba.md` | No se arrastran los PBI relacionados ni el fuera de alcance |
| Pide cotejar contra el manual | La sección citada, rebuscada en este turno | No se cita de memoria |
| No pasa oráculo | Solo consistencia interna entre saltos | No se inventa el esperado |

Esquema de parámetros y cómo leer un caso: `references/oraculos.md`.

### 6. Cotejo

Aplicar `references/cotejo-estructuras.md` a cada path del oráculo y a cada diferencia interna entre saltos de la misma traza.

Comparar al menos, cuando existan en el fragmento:

- entrada del canal contra el body del salto siguiente
- body enviado contra campos del response de **ese** salto
- arrays del response contra el dump o el mensaje posterior (`infoTicketList`, traducción, AMQ)
- el valor que el oráculo nombra, en el salto que el oráculo nombra

`null`, `""`, clave ausente y clave presente con array vacío son cuatro hechos distintos. No se colapsan.

El cotejo se hace en local, contra el caso. Si un resumen del log va a salir de la máquina, se usa el mismo enmascarado que `python -m pbi`: correos, tiquetes de 13 dígitos, números largos, PNR etiquetado y nombres en campos de persona. Nombres de campo, correlation id, códigos de error y la diferencia null / vacío se conservan, porque sin eso no hay cotejo. El archivo revisable es `test-cases/PBI-<id>/lectura/envio_ia.md`.

### 7. Clasificación

| Clase | Cuándo | Efecto en un caso de prueba |
|---|---|---|
| CONFIRMADO | El hecho está en el log y coincide con el oráculo | Apoya Pass de **esa** afirmación |
| INCONSISTENCIA | Dos literales del mismo log se contradicen, o el log contradice el oráculo | Si hay oráculo, esa afirmación no pasa. Si no hay oráculo, queda observada |
| HUECO | El fragmento no trae el salto o el campo | No es Fail. La afirmación sigue abierta |
| RUIDO | Infraestructura fuera de la transacción | Fuera del cotejo de negocio |
| HIPOTESIS | Una causa posible que el log no dice | No se usa como esperado ni como bug |

La palabra `average` en un timing es un promedio. No es la duración de esa correlation id salvo que la línea lo diga.

### 8. Draft

```
## Draft de respuesta

Fragmento: completo | parcial
Trazas reensambladas: N
Oráculo: parámetros | PBI-XXXX #TC … | ninguno (solo consistencia interna)

### Por traza
- Id:
- refund-request / ticket / channel / lang: (los que estén)
- Cadena de saltos, en orden, una línea por salto (nombre + URL si la hay)
- Cotejo: path | salto | visto | oráculo | clase

### Inconsistencias
Solo las que cambian el resultado. Cada una con los dos literales y el id.

### Huecos
Qué afirmación no se puede cerrar con este fragmento.

### Ruido
Conteo, sin pegar las líneas.

---
**Metadata del draft:**
- Skill: validador-logs-capa-media
- Referencias: [lista]
- Oráculo: [archivo o "parámetros del mensaje"]
- Confianza: ALTA si el oráculo y el log cubren el path | MEDIA si el fragmento es parcial | BAJA si el id no cierra
- Items no verificados: [lista]
```

No pegar el log completo de vuelta. Citar la línea o el path que sostiene el hallazgo.

## Límites

- Hay una ancla por dialecto: `ejemplo-ancla-consult-refund.md` (`ws-refund-orchconsultrefund`, 2026-10-20) y `ejemplo-ancla-checkrefundrts.md` (`ws-refund-checkrefundrts`, 2026-09-24). Enseñan el método. Ninguna es contrato del otro pod.
- Este skill no llama a OpenShift ni ejecuta el servicio.
- No redacta el bug de Azure. Deja hechos para `qa-funcional` si el oráculo queda contradicho.
- No inventa el SELECT ni el path HTTP que el log no imprimió.

## Archivos

```
validador-logs-capa-media/
├── SKILL.md
└── references/
    ├── formato-linea.md
    ├── reensamble-trazas.md
    ├── cotejo-estructuras.md
    ├── oraculos.md
    ├── ejemplo-ancla-consult-refund.md
    └── ejemplo-ancla-checkrefundrts.md
```
