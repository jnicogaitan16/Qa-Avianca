# QA-Avianca

Informe de la iniciativa de asistencia a pruebas de reembolsos.

Fecha: 23 de octubre de 2026.  
Ámbito: equipo de QA. Productos Special Refund (SR), AV Refund (AVR), Payment Integrator (PI) y Refund Orchestration Rules (ROR).  
Organización de Azure DevOps: `aviancavsts`.

Este documento describe qué se construyó, para qué le sirve al equipo, qué fuentes consulta y qué controles tiene el tratamiento de datos. No reemplaza el manual de un producto ni un cierre de sprint. El estado de cada caso sigue en su markdown.

---

## 1. Para qué sirve

QA-Avianca deja armado, en la máquina del analista, el paquete de un Product Backlog Item antes de ejecutar:

- la lectura del Work Item, de sus adjuntos y de los enlaces que sí se pueden leer;
- el contraste con los manuales del producto y con los lineamientos de QA;
- un borrador de casos anclado en el requisito, no en un comentario;
- una matriz de riesgos que dice qué está cubierto, qué es un hueco y qué queda fuera;
- un Excel de presentación, solo cuando se pide, con los casos y esa matriz.

El analista corrige el markdown durante la ejecución: agrega un caso, elimina uno que no corresponde y escribe el resultado. El tablero de Azure DevOps no se modifica.

El segundo uso es el cotejo de un log de OpenShift. El log se pega en el chat, se nombra el caso y se compara, en la misma traza, el request, el body del salto siguiente y el response. Esa lectura no forma parte del comando que abre el PBI.

## 2. Qué se trabajó

La iniciativa queda operable con dos comandos, el entorno virtual activo:

```text
Corre PBI 1330194
Genera doc PBI 1330194
```

`Corre PBI` lee el Work Item y, si todavía no hay markdown, escribe `test-cases/PBI-<id>/casos-de-prueba.md`. `Genera doc PBI` arma el Excel desde ese markdown. Los comandos largos anteriores siguen funcionando y hacen lo mismo.

El recorrido de `Corre PBI` es obligatorio y se imprime en la terminal. Si un paso no puede cumplirse, se ve `paso N …: falló`, `Proceso incompleto` y el consumo de esa corrida. No se imprime `Proceso completo`.

| Paso | Qué hace | Si no hay dato |
|---|---|---|
| 1. Lectura del PBI | GET del Work Item. Empieza por Integration y, si el ID no está, recorre los demás proyectos de la organización. | Se detiene. Sin lectura no hay casos. |
| 2. Adjuntos | Extrae el workbook o el documento adjunto: CSV, XML, Word o Excel, dentro de los límites de tamaño. | Avisa y sigue. Un PBI sin adjunto no se bloquea. |
| 3. Análisis | Separa los comportamientos que el requisito nombra. | Si no hay descripción ni criterios, se detiene. Un relato que no usa una palabra clave ya no corta el flujo. |
| 4. Base de conocimiento | Lee los cinco manuales locales y los compara con el texto del PBI. | Si un manual exigido no está revalidado, se detiene. |
| 5. Enmascarado | Sustituye datos personales y comprueba que no queden fugas en el texto elegible. | Si la comprobación no queda elegible, se detiene y no escribe casos. |
| 6. Casos | Escribe la tabla y la matriz solo si el markdown no existe. | Un archivo ya existente no se reescribe. |
| 7. Notificación | `Proceso completo` únicamente si los pasos anteriores cumplieron. | `Proceso incompleto`. |
| 8. Tokens | Siempre, también cuando el proceso queda incompleto. | Ver la sección de consumo. |

También quedó definido el ciclo de corrección: el borrador se ajusta en el chat, sobre el markdown. El Excel no se regenera en cada cambio. Se pide con `Genera doc PBI` cuando la presentación está lista.

La presentación tiene dos hojas. La primera conserva cuatro columnas: nombre del caso, pasos (un paso por fila), resultado esperado y resultado de ejecución. La segunda se llama `matriz de riesgos` y trae la tabla de esa sección.

Se usó el flujo sobre Work Items de Integration y de UnidadesSoporteF, entre ellos 1321233, 1330194, 1338371 y 1365790. El detalle de cada ejecución permanece en `test-cases/PBI-<id>/casos-de-prueba.md`. Este informe no lo convierte en un acta.

## 3. En qué ayuda al equipo de QA

El criterio de un caso deja de depender de la memoria de una sola ejecución. El nombre sigue el lineamiento del equipo: `PBI-<id> #TC` más el título. El estado de diseño arranca en Design. El resultado de una ejecución no corrida queda en `Sin ejecutar.` La evidencia se pide con fecha y hora.

El borrador se arma con tres prácticas, no con un modelo externo:

- diseño funcional a partir del comportamiento que el requisito nombra, con técnica de caja negra solo cuando el texto la sostiene;
- una petición HTTP solo si el catálogo o el manual traen la URL; si no está, el caso no inventa el request;
- un caso de traza solo cuando el propio requisito habla de un log. El cotejo del log ocurre después, con el pegado de esa conversación.

La matriz evita una escala que el equipo no tiene documentada. No calcula probabilidad ni impacto. No mezcla la severidad de Azure con el modelo F-S-V. F-S-V mide un defecto ya observado. La matriz mide el diseño:

| Medición | Significado |
|---|---|
| Cubierto por el caso N | El riesgo citado en el requisito tiene un caso. |
| Hueco | Falta un dato y no se inventa: columna, mensaje, URL o una regla que vive en otro PBI no leído. |
| Fuera de este comando | El tema existe en un manual, pero este PBI no lo pide. Ejemplo: una notificación o un envío a SAP que el requisito no nombra. |
| Contradicción | El manual y el PBI no dicen lo mismo. El oráculo del caso es el PBI, y la diferencia queda escrita. |

Eso le sirve al equipo en la revisión con desarrollo y en la presentación al liderazgo: se ve qué se va a probar, qué no se pudo cerrar y qué se dejó fuera a propósito.

El tiempo que se ahorra está en la primera lectura: localizar el Work Item, bajar el adjunto, no copiar un saludo ni un tiquete al caso, y no volver a buscar en cuatro manuales la misma tabla. El juicio de si el caso corresponde sigue siendo del analista. Un caso que no corresponde se elimina en el markdown. Un comentario del Work Item no se convierte en criterio de aceptación.

## 4. Qué consume

Todo el acceso remoto es de lectura. No hay push, no hay comentario en el Work Item y no se publican casos en el tablero.

### Azure DevOps

Organización `aviancavsts`, por HTTPS, contra `dev.azure.com`. El comando solo usa GET. La credencial vive en `.env`, en la variable `TOKEN-AZURE`. El programa la nombra por `AZDO_WI_PAT_VAR` y no imprime el valor, no lo copia al paquete y no lo escribe en los archivos de salida.

El proyecto de arranque es Integration. Si el ID responde 404 ahí, se listan los proyectos de la organización y se busca en el resto. 1365790, por ejemplo, se resolvió en UnidadesSoporteF. Un 401 es credencial no aceptada. Un 403 es falta de permiso de lectura, no un ítem inexistente.

De cada Work Item se leen identificación, tipo, estado, revisión, título, descripción, criterios de aceptación, comentarios, relaciones y adjuntos. El comentario se guarda como dato. No entra al resultado esperado.

### Repositorios Git enlazados

Si el Work Item trae un enlace `vstfs` o HTTPS a un commit o a un pull request, se leen el mensaje y las rutas de archivo. No se descarga el contenido de los archivos. El commit más reciente pesa más que los anteriores. Si el enlace no está, o la API no devuelve cambios, la terminal lo dice y el comando sigue. En 1365790 se leyeron 10 commits y el último, del 23 de octubre de 2026, correspondía al PR 130605: el mensaje habla del tamaño de un modal en la pantalla `control-and-payment-acm`. Ese mensaje no se usó como oráculo de las tablas de Valores Faltantes.

Una página wiki enlazada se lee si la API la devuelve. Si no hay enlace, el conteo queda en cero y no bloquea.

No se clona un repositorio de aplicación. No se lee un remoto que el Work Item no enlaza.

### Documentación local

Estas fuentes están en el propio proyecto. No salen a buscarse en internet durante `Corre PBI`.

| Fuente | Uso |
|---|---|
| `base_conocimiento/manual-aplicacion-sr.md` | Special Refund |
| `base_conocimiento/manual-aplicacion-avr.md` | AV Refund |
| `base_conocimiento/manual-aplicacion-pi.md` | Payment Integrator |
| `base_conocimiento/manual-aplicacion-ror.md` | Refund Orchestration Rules |
| `base_conocimiento/lineamientos-qa.md` | Nombre del caso, estados Design, Ready y Closed, evidencia |
| `skills/` | Diseño de casos, catálogo de APIs, catálogo de tablas y reglas del cotejo de logs |
| `docs/proyectos/apis-por-modulo.md` | Fila de catálogo cuando el requisito nombra un módulo. Si la fila no trae URL, no se arma un request |

El manual se revalida por presencia y se lee. Una afirmación que no está en el requisito, en el manual o en el catálogo se marca como no verificada. No se completa con una tabla vecina ni con la URL de la fila de al lado.

### Lo que no se consume

No hay llamada a la API de GPT. `AZDO_WI_LLM_ENABLED` permanece en false. `tokens usados: 0` significa eso: el comando no tiene una factura de modelo. `tokens estimados de la ejecución` es el tamaño del texto leído en esa corrida, pasado a una cuenta local de caracteres. En una corrida que abre los cinco manuales el número sube, sobre todo por el manual de PI. No es un cobro.

El análisis que se conversa en el editor usa el paquete ya enmascarado. No es una segunda integración con una API de pago.

## 5. Riesgos

### 5.1 Datos que procesa la IA, y cómo se enmascaran

El texto que puede salir de la máquina, o que la asistencia usa para redactar casos, pasa antes por una sustitución. El archivo elegible es uno: `test-cases/PBI-<id>/lectura/envio_ia.md`. El Work Item completo, con los valores originales, queda en `work_item_context.md`, dentro de esa misma carpeta `lectura/`, y no se envía.

La sustitución es por reglas, sobre el texto de la descripción, los criterios, los comentarios y el texto extraído de los adjuntos. El mismo valor recibe siempre el mismo token, para poder ver si un campo llegó de un lado al otro sin leer el dato.

| Dato detectado | Queda como | Ejemplo de forma, no un dato real |
|---|---|---|
| Correo | `MAIL-01` | una dirección con `@` |
| Tiquete de 13 dígitos | `TKT-01` | el número de documento de 13 dígitos |
| Número de 10 a 12 dígitos, o de 14 o más | `NUM-01` | cuenta u otro identificador largo |
| PNR junto a la palabra PNR, o seis caracteres entre `>> >>` | `PNR-01` | el localizador etiquetado |
| Valor JSON de `firstName`, `lastName`, `middleName`, `secondLastName` o `identificationNumber` | `NOM-01` | el nombre dentro de esa clave |

Después de sustituir, el comando busca si algún valor original sigue presente en `envio_ia.md`. El resultado se escribe en `mascara_reporte.md`: conteo por tipo y la frase `Elegible para análisis de IA: sí` o `no`. Ese reporte no repite los valores. Si hay una fuga, el paso 5 falla, no se generan casos y el archivo no debe usarse como entrada.

El mapa token a valor vive en `mascara.json`. Es local. No se versiona, no se imprime y no forma parte del envío. La carpeta `lectura/` de cada PBI está fuera del repositorio por la misma razón. `.env` tampoco se versiona.

Se conservan, porque sin ellos no hay prueba: nombres de campo, correlation id, códigos de error cortos y la diferencia entre `null`, cadena vacía, clave ausente y arreglo vacío. Un código de negocio de menos de 10 dígitos no entra en la regla de números largos. Un número de solicitud de 8 dígitos tampoco: es la clave del caso, no un tiquete.

El PAT no entra en el paquete, ni en el reporte, ni en la consola.

### 5.2 Lo que el enmascarado no cubre

La regla no es un producto de prevención de pérdida de datos. Un nombre escrito en prosa, fuera de esas claves JSON, no se sustituye. Un identificador con un formato nuevo, que no sea correo, tiquete de 13 dígitos, número largo ni PNR etiquetado, puede quedar visible. Por eso la elegibilidad se comprueba contra lo que sí se detectó, y el analista no debe adjuntar `work_item_context.md` ni `mascara.json` a un correo, a un chat externo ni a un tablero.

El log que se pega en el chat para cotejar una ejecución es otra vía. Ese pegado es la evidencia de esa validación y no se reescribe con los tokens. No se reutiliza un log anterior ni `envio_ia.md` para decidir si un campo llegó. Quien pega el log es responsable de no reenviarlo fuera de la sesión de trabajo.

Un comentario del Work Item entra al paquete enmascarado como dato. No autoriza un resultado esperado.

### 5.3 Riesgo funcional

El borrador puede dejar un caso de más o partir mal un requisito si el texto no nombra la acción. El control es el markdown: se corrige antes de ejecutar y antes de `Genera doc PBI`. El Excel que ya estaba abierto no cambia solo.

La matriz no dice la probabilidad de un fallo en producción. Decir que un riesgo está cubierto significa que existe un caso, no que la prueba ya pasó.

Cuando el manual y el PBI se contradicen, el informe del caso lo escribe y no elige en silencio. En la pantalla de Gestión de pago ACM, el manual dice que Finalizar cancela la edición. El PBI 1365790, para un registro de Valores Faltantes, pide estado F y razón Finalizado. El oráculo de ese registro es el PBI. Probar con la frase del manual marcaría un fallo inexistente, o daría por bueno un comportamiento que el requisito ya cambió.

No se inventa la URL de un botón, el nombre físico de una columna ni el texto de un mensaje que el PBI no trae. Esos puntos quedan como hueco.

### 5.4 Riesgo de acceso

La credencial permite leer lo que el PAT ya puede leer en `aviancavsts`. El programa no amplía ese permiso y no lo usa para escribir. Quien opere el comando necesita un PAT de lectura, guardado solo en `.env`. Pegarlo en el chat o en un informe anula el control.

La lectura de commits muestra rutas de archivo. No debe usarse para traer secretos del repositorio: el comando no descarga el archivo. Si un mensaje de commit trajera un secreto, ese texto sí viajaría al paquete y quedaría sujeto a las mismas reglas de enmascarado, que no detectan cualquier secreto.

## 6. Límites conscientes

- Adjunto máximo 25 MB, y 100 MB sumando los de un mismo Work Item. Un CSV o XML grande guarda columnas, conteo y una muestra, no el archivo entero.
- Una imagen, o un PDF sin texto, queda para revisión visual. No se convierte en casos.
- No se crean casos, comentarios ni adjuntos en Azure DevOps.
- El Excel no es la fuente. La fuente es el markdown. Si el markdown está incompleto, el Excel también lo está.
- El cotejo de OpenShift no corre dentro de `Corre PBI`.
- El tope de trabajo del borrador es 10 casos, anclados en el requisito.

## 7. Cómo se presenta un PBI

1. Activar el entorno: `.\.venv\Scripts\Activate.ps1`.
2. `Corre PBI <id>`. Confirmar en la terminal el proyecto, la revisión, los adjuntos, los manuales, los commits y las wiki leídas.
3. Revisar `test-cases/PBI-<id>/casos-de-prueba.md` y `test-cases/PBI-<id>/lectura/mascara_reporte.md`. Si la elegibilidad no es sí, no se usa `envio_ia.md`.
4. Corregir en el markdown el caso que no corresponda. Escribir el resultado de ejecución ahí.
5. Cuando la presentación haga falta: `Genera doc PBI <id>`. El Excel queda en OneDrive, carpeta `QA nico/Test cases`, con el nombre `PBI-<id>.xlsx`. Tiene la hoja del PBI y la hoja `matriz de riesgos`. Reemplaza el archivo del mismo nombre. No se copia dentro del proyecto.

## 8. Cierre

QA-Avianca no sustituye al analista ni escribe en el tablero. Reduce la preparación del caso a una lectura repetible, deja dicha la diferencia entre el requisito y el manual, y separa el dato personal del texto con el que se diseña la prueba. El control está en la elegibilidad del enmascarado, en no inventar lo que la fuente no dice, y en que el Excel salga del markdown solo cuando el equipo lo pide.
