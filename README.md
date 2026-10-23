# Asistente QA Avianca

Lee un Work Item de Azure DevOps, lo contrasta con los manuales del producto y deja la carpeta de casos. Cuando llega un log de OpenShift, ese log se pega en el chat y se coteja contra el caso: request, response y cada campo. No escribe en Azure DevOps y no envía el PBI a un modelo externo.

El informe para presentación está en `docs/informe-qa-avianca.docx`. El markdown del mismo texto queda en `docs/informe-qa-avianca.md`.

## Activar el entorno

En PowerShell, desde esta carpeta:

```powershell
.\.venv\Scripts\Activate.ps1
python scripts/install_deps.py
```

`install_deps.py` solo corre si `QA_INSTALL_DEPS=true` en `.env`. Instala `pypdf` dentro de `.venv`. El PAT no se instala ni se imprime. La única variable que lo contiene es `TOKEN-AZURE`. `AZDO_WI_PAT_VAR` apunta a ese nombre. No se copia el valor.

## Leer un PBI

```powershell
Corre PBI 1330194
```

Hace lo mismo que `python -m pbi 1330194`.

El número es el del Work Item. Empieza por el proyecto Integration y, si ahí no está, recorre los demás proyectos de `aviancavsts`. Solo hace GET. En la terminal el recorrido es:

```text
paso 1 lectura del PBI: cumplido
paso 2 documentos adjuntos: cumplido
paso 3 análisis del PBI: cumplido
paso 4 base de conocimiento: cumplido
paso 5 enmascarado: cumplido
paso 6 casos de prueba: cumplido
paso 7 notificación: cumplido
Proceso completo
paso 8 consumo de tokens: cumplido
tokens usados: 0
tokens estimados de la ejecución: 905
pasos cumplidos: 8
```

Si un paso falla, la terminal muestra `paso N …: falló`, `Proceso incompleto` y el consumo de esa ejecución. No imprime `Proceso completo`. Si el PBI no trae adjuntos, el paso 2 lo dice y sigue. Si hay un enlace a un commit o a un pull request, se lee el cambio y el último commit pesa más. Si el enlace no está o no se puede leer, se avisa y se sigue. `tokens usados: 0` es el consumo de un modelo: el comando no llama a uno. `tokens estimados de la ejecución` es el texto leído en esa corrida (PBI, adjuntos, manuales, paquete enmascarado y casos) dividido entre 4. No es una factura. El Excel no se genera. La lectura de un log de OpenShift no entra en el comando.

Cada PBI queda en una sola carpeta, `test-cases/PBI-<id>/`. El caso y el Excel están en la raíz de esa carpeta. La lectura local queda en `lectura/` y no se versiona:

| Archivo | Para qué sirve |
|---|---|
| `work_item_context.md` | Lectura local completa. No sale de la máquina. |
| `source_manifest.json` | Qué se recuperó, qué manual se revalidó y qué faltó. |
| `envio_ia.md` | Único texto elegible para que la IA redacte casos. Ya va enmascarado. |
| `mascara_reporte.md` | Cuántos datos se taparon y si el archivo quedó sin fugas. No repite los valores. |
| `mascara.json` | Mapa token a valor. Local. No forma parte del envío. |
| `QA_Revalidacion.md` | Comentarios leídos y huecos. Un comentario no es un criterio. |

Los casos se trabajan en `test-cases/PBI-<id>/casos-de-prueba.md`: la tabla `#`, el nombre `PBI-<id> #TC …`, los pasos, el resultado esperado, el resultado de ejecución y la matriz de riesgos. Durante la ejecución se corrige ese markdown. Un caso se crea o se elimina ahí, desde el chat. El tope de trabajo es 10 casos, anclados en el requisito.

La matriz no asigna probabilidad ni impacto. Esos valores no están en `lineamientos-qa.md` ni en el manual general. Cada fila cita el riesgo que ya viene en el Work Item y mide si hay un caso que lo cubre, si es un hueco o si queda fuera de este comando.

El Excel es solo la presentación. No se regenera cuando cambia el markdown y no se guarda en el proyecto. Se escribe en OneDrive, en `QA nico/Test cases`, con el nombre `PBI-<id>.xlsx`, cuando se pide. La primera hoja conserva las cuatro columnas del caso. La segunda hoja se llama `matriz de riesgos` y trae la tabla de esa sección:

```powershell
Genera doc PBI 1330194
```

Ese archivo reemplaza el `PBI-1330194.xlsx` que ya esté en esa carpeta. El markdown del caso sigue en el proyecto.

## Orden de trabajo

1. Revalidar `base_conocimiento/` (SR, AVR, PI, ROR y lineamientos).
2. Leer el Work Item y sus adjuntos. El WB, si viene en CSV, XML, Word `.docx` o Excel, es el insumo principal junto con la descripción.
3. Enmascarar. Si `mascara_reporte.md` no queda elegible, el comando se detiene y no genera casos.
4. Si no hay markdown, el comando lo escribe con los comportamientos del requisito y la matriz de riesgos. Un comentario no es criterio. No se inventa URL, tabla ni escala de riesgo. Un caso que no corresponda se corrige en el chat. El Excel espera a que se pida.
5. El log de OpenShift se trabaja después, en el chat, nombrando el PBI.

## Log de OpenShift

Se pega el log en el chat y se nombra el caso, por ejemplo `PBI-1330194 #TC …`. Ese pegado es la única evidencia de la validación. No se reutiliza un log anterior ni el archivo enmascarado. El validador de logs:

- separa el ruido de arranque de la traza de negocio
- reúne la traza por correlation id
- compara el request del canal con el body del salto siguiente
- compara ese body con el response del mismo salto
- trata `null`, `""`, la clave ausente y `[]` como cuatro hechos distintos
- no completa un JSON cortado ni declara un fallo si el caso no exige ese campo

El oráculo es la columna Resultado esperado de ese caso. El manual solo entra si el caso ya lo cita o si se pide el cotejo contra el manual.

## Enmascarado

Antes de que un texto del PBI o del log quede en `envio_ia.md`, se sustituyen:

| Dato | Token |
|---|---|
| Correo | `MAIL-01` |
| Tiquete de 13 dígitos | `TKT-01` |
| Número de 10 a 12 dígitos, o de 14 o más | `NUM-01` |
| PNR junto a la etiqueta PNR, o entre `>> >>` | `PNR-01` |
| Valor de `firstName`, `lastName`, `middleName`, `secondLastName` o `identificationNumber` | `NOM-01` |

Se conservan nombres de campo, correlation id, códigos de error y la diferencia entre null y vacío. Sin eso no se puede cotejar la estructura.

La comprobación está en `mascara_reporte.md`: cuenta por tipo de token y si quedó alguna fuga. Si hay fuga, el archivo no es elegible y no debe usarse como entrada de la IA. Los valores originales no se imprimen en ese reporte ni en la consola. El PAT no entra en ninguno de estos archivos.

`AZDO_WI_LLM_ENABLED` permanece en false. Este proyecto no llama a la API de GPT.

## Estructura

```
base_conocimiento/     manuales SR, AVR, PI, ROR y lineamientos
skills/                qa-funcional, postman, validador de logs, orquestador y el resto
test-cases/PBI-<id>/          casos. El Excel va a OneDrive, QA nico/Test cases
test-cases/PBI-<id>/lectura/ lectura, máscara y revalidación (no se versiona)
pbi/                   Corre PBI y el cliente del comando
agent/                 cliente de solo lectura hacia Azure DevOps
scripts/corre.cmd      Corre PBI <id>
scripts/genera.cmd     Genera doc PBI <id>
scripts/exportar_casos.py
.env                   TOKEN-AZURE y la configuración. No se versiona.
```

Con el entorno activo, el uso es `Corre PBI <id>` y `Genera doc PBI <id>`. `python -m pbi <id>` sigue haciendo la misma lectura. El paquete `agent` es el cliente interno. Los `.cmd` se copian a `.venv/Scripts` al instalar dependencias, porque esa carpeta ya está en el PATH de la sesión.

## Límites

Adjunto máximo 25 MB y 100 MB en total. Un CSV o XML grande guarda columnas, conteo y una muestra, no el archivo entero. Una imagen o un PDF sin texto queda para revisión visual. No hay escritura en Azure DevOps: no se crean casos, comentarios ni adjuntos en el tablero.

## Errores de lectura

| HTTP | Qué significa |
|---|---|
| 401 | El PAT no fue aceptado. Revisar la credencial de aviancavsts sin pegarla en el chat. |
| 403 | Sin permiso de lectura. No es un ítem inexistente. |
| 404 | El ID no está en Integration ni en los demás proyectos. |
| 429 o 5xx | Reintento corto y después un error controlado. |
