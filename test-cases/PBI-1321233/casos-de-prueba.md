# PBI-1321233 — Casos de prueba: appcode

- **Carpeta:** PBI-1321233
- **State:** Design
- **Related work:** PBI 1321233
- **Evidencias:** Con fecha y hora en cada ejecución
- **URL QA:** `https://ws-refund-orchsendpayinfoandsupportfiles-ssf-npci-refund.apps.aroqa.avtest.ink/refund/orchsendpayinfoandsupport`

---

## Casos de prueba

| # | Nombre del caso de prueba | Pasos | Resultado esperado |
|---|---|---|---|
| 1 | PBI-1321233 #TC appcode entero se procesa | 1. Armar el request base de QA.<br>2. Dejar `appcode` inmediatamente después de `channel`.<br>3. Enviar `appcode` como número: `2`.<br>4. Guardar la respuesta con fecha y hora. | El endpoint procesa el request. El valor entero `2` se acepta. |
| 2 | PBI-1321233 #TC appcode string el error se controla | 1. Mismo request del caso anterior.<br>2. Cambiar solo el tipo: `appcode` como texto `"2"`.<br>3. Enviar.<br>4. Guardar la respuesta con fecha y hora. | El endpoint devuelve un error controlado. Ese envío no queda como exitoso. El texto y el código HTTP de la respuesta no están en el PBI ni en el manual: se registran tal como los devuelva el servicio. |
| 3 | PBI-1321233 #TC appcode vacío | 1. Mismo request base.<br>2. Enviar `appcode` como cadena vacía: `""`.<br>3. Guardar la respuesta. | El campo no es mandatorio. El servicio acepta el request con `appcode` vacío y el resto del body sigue su flujo. |
| 4 | PBI-1321233 #TC appcode null | 1. Mismo request base.<br>2. Enviar `appcode` en null.<br>3. Guardar la respuesta. | El servicio acepta el request con `appcode` en null y el resto del body sigue su flujo. |
| 5 | PBI-1321233 #TC appcode no enviado | 1. Mismo request base.<br>2. Quitar la propiedad `appcode` del body.<br>3. Enviar y guardar la respuesta. | El servicio acepta el request sin el campo y el resto del body sigue su flujo. |
| 6 | PBI-1321233 #TC appcode longitud 2 | 1. Mismo request base.<br>2. Enviar `appcode` como número de dos dígitos: `10`.<br>3. Guardar la respuesta. | Cabe en la longitud 2 del PBI. El endpoint lo procesa igual que el entero `2`. Aún no está ejecutado. |
| 7 | PBI-1321233 #TC appcode longitud mayor a 2 | 1. Mismo request base.<br>2. Enviar `appcode` como número de tres dígitos: `100`.<br>3. Guardar la respuesta. | Supera la longitud 2. El endpoint devuelve un error controlado y el envío no queda como exitoso. Aún no está ejecutado. El texto del error se registra tal como lo devuelva el servicio. |
| 8 | PBI-1321233 #TC demás campos del request no cambian | 1. Enviar el request del caso del entero `2`, con el resto de campos del body del PBI (`channel`, `identificationCode`, `fileAttachments` y los demás).<br>2. Revisar que la respuesta no falle por ninguno de esos campos.<br>3. Guardar la respuesta. | La nota del PBI se cumple: lo demás del servicio no cambia. El request se procesa y el único agregado de este ajuste es `appcode`. |
| 9 | PBI-1321233 #TC log mapea appcode a APP_CODE | 1. Ejecutar de nuevo el caso del entero `2`.<br>2. Abrir el log del componente que atendió esa URL en QA.<br>3. Buscar el valor enviado y el campo `APP_CODE` del servicio Bank Data Information del PI.<br>4. Adjuntar el extracto del log con fecha y hora. | Pendiente de ejecución. El valor recibido en `appcode` queda mapeado directo a `APP_CODE`, con el mismo valor enviado. La ruta del log y el texto exacto no están en el manual ni en el catálogo. |
| 10 | PBI-1321233 #TC log del error cuando appcode es string | 1. Ejecutar de nuevo el caso del string `"2"`.<br>2. Abrir el mismo log de QA.<br>3. Buscar el error de esa ejecución y si hubo mapeo hacia `APP_CODE`.<br>4. Adjuntar el extracto con fecha y hora. | Pendiente de ejecución. El log deja el error controlado del string y no deja un mapeo exitoso de ese valor hacia `APP_CODE`. |

---

## Calibración

| Afirmación | Fuente buscada | Resultado | Acción |
|---|---|---|---|
| Nombre `PBI-XXXXX #TC Título del escenario` | `base_conocimiento/lineamientos-qa.md` | CONFIRMADO | Usado en los diez casos |
| Carpeta por PBI, state Design, Related work, evidencias con fecha y hora | `lineamientos-qa.md` | CONFIRMADO | Quedó en el encabezado |
| URL QA del orquestador | `docs/proyectos/apis-por-modulo.md`, fila Send pay info and suport files | CONFIRMADO | Es el target de los casos |
| `appcode` VARCHAR 2, no mandatorio, después de `channel`, mapeo a `APP_CODE` | PBI 1321233. Sin coincidencias en `manual-aplicacion-pi.md` | SIN RESPALDO en el manual | Se toma del PBI, no del manual |
| Entero funciona y string devuelve error controlado | Ejecución observada. No está en el manual ni en el catálogo | SIN RESPALDO | Resultado observado de los casos 1 y 2 |
| Ejemplo del PBI `appcode: 2` numérico, tipo declarado VARCHAR | Texto del PBI | CONTRADICCIÓN | Los dos literales quedan visibles; el caso 1 usa el ejemplo numérico |

---

**Fuentes técnicas:** `skills/qa-funcional/references/tecnicas-diseno-casos.md`, `prompts/plantillas/02-test-plan-suite-case.md`
**Fuentes del producto:** `base_conocimiento/lineamientos-qa.md`, `base_conocimiento/manual-aplicacion-pi.md`, `docs/proyectos/apis-por-modulo.md`, PBI 1321233
**Skills:** qa-funcional, postman, orquestador-validador
