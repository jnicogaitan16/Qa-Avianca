# Plan de trabajo

## IaAgent QA Platform

Iniciativa nueva de QA para Avianca Refunds, con análisis de seguridad

Fecha: 05 de octubre de 2026  
Documento para presentación al equipo

IaAgent es una iniciativa nueva del equipo de QA de Avianca sobre el producto Refund. El trabajo vive en Azure DevOps: el PBI, los comentarios, el pull request, el Test Plan y el caso de prueba. En cada PBI la IA entra siempre. Analiza el material y redacta el borrador del Test Plan, de los casos y de los comentarios. QA lo revisa y lo publica en Azure. Ese paso no se salta.

Fuentes de este plan: `docs/manual-general.md`, `base_conocimiento/lineamientos-qa.md`, `base_conocimiento/manual-aplicacion-sr.md`, `base_conocimiento/manual-aplicacion-avr.md`, `base_conocimiento/manual-aplicacion-pi.md`, `base_conocimiento/manual-aplicacion-ror.md`. Donde el lineamiento no describe un paso, el plan lo dice y no lo inventa.

---

## 1. El producto

Refund son cuatro aplicaciones internas. Tres mueven el caso. La cuarta guarda reglas para la capa media.

```
SR crea el caso especial (VIP, masivos, valores faltantes)
        ↓ Mozart / APIM
AVR sigue el caso, timeout 30 min, correos NTC
        ↓
PI ejecuta el pago ya aprobado (voucher, transferencia, ACM, SAP)

ROR → reglas, EMD y homologación → APIM → orquestadores
```

| Aplicación | Qué hace | Front QA | Base QA |
|---|---|---|---|
| SR — Special Refund | Ingreso del caso especial. Sin lógica de negocio de reembolso. Consulta APIM para datos, cálculo y creación. El caso queda en Mozart | `https://specialrefundqa.avtest.ink/` | No documentada |
| AVR — AV Refund | Seguimiento de lo que sale de Mozart. Purge Refund a los 30 minutos. Correos NTC | `azwappavrefsftuseqa…/auth` | `az-sqla-avref-use-qa` |
| PI — Payment Integrator | Pago cuando Mozart ya envió la solicitud aprobada. Maestras de banco, moneda y forma de pago. Interfaces a SAP | `azwapppiccustfrontuseqa…/auth` | `az-sqla-piccust-use-qa` |
| ROR — Refund Orchestration Rules | Parámetros, reglas, EMD y homologaciones. Los orquestadores las consultan por APIM. No radica ni paga | `azwappsorqrulesfrontuseqa…/auth` | `az-sqla-orqrules-use-qa` |

Mozart (Accelya), SAP4HANA y el APIM de Avianca aparecen en los flujos. No son fronts del equipo. El pasajero pide el reembolso por avianca.com, MyAvianca, LifeMiles, AVIAJAR, AVC o Trade. El clic a clic de esas páginas no está en los manuales.

Autenticación de las cuatro apps: Azure AD, correo Microsoft. Ambientes de trabajo: **DEV, QA, PRE y POST**.

---

## 2. De dónde sale el caso de prueba

El caso queda en Azure DevOps, en el Test Plan de la aplicación, ligado al PBI. Antes de publicarlo, la IA analiza el PBI y genera el borrador. Sin ese paso el caso no pasa a Ready.

La tarea de los lineamientos es **QA - Análisis y Diseño Caso Prueba**: se analiza el alcance del PBI, se diseñan los casos y se cargan al Test Plan. La tarea anterior, **QA - Recibir PBI**, es la sesión en la que desarrollo entrega a QA y al usuario. Esta iniciativa mete la IA en el medio de esas dos tareas y de los comentarios que QA deja después.

| Insumo | Qué se lee en Azure | Qué dice el lineamiento |
|---|---|---|
| PBI | Descripción, criterios de aceptación, Area, Iteration, Application Name (SR, AVR, PI o ROR) | Sí. El diseño sale del alcance del PBI. En un PBI de automatización también están Priority, Effort y Business Value |
| Comentarios de desarrollo | Hilo del PBI y, si hay corrección, los comentarios del bug | Parcial. Al resolver un bug, desarrollo y QA dejan comentario. En el re-test, QA pide qué cambió en base de datos o en la interfaz. Al abrir un impedimento, se comenta en el PBI. No hay un paso que diga «leer todos los comentarios antes de diseñar» |
| Diff del pull request | Pestaña Files del pull request de la rama PBI | No está en el lineamiento de diseño de casos. Sí está la rama PBI → Release → Master, y que el pull request lo aprueba un líder Avianca |
| Riesgo | Un puntaje o una matriz para priorizar casos | No está. Ni los lineamientos ni el manual general definen cómo se calcula |
| Caso de prueba | Test Plan de la app, carpeta del PBI, Related work | Sí. Formato `PBI-XXXXX #TC Título del escenario` |
| APIs del módulo | `docs/proyectos/apis-por-modulo.md` | Insumo de esta iniciativa. Dice qué endpoint se prueba o se valida. El archivo nace vacío: el path se escribe cuando está confirmado en swagger o en el manual |

### Cómo queda el ciclo en esta iniciativa

La IA participa en los cuatro puntos de salida: el análisis, el Test Plan, los casos y los comentarios. QA no publica en Azure un texto que la IA no haya redactado antes.

1. Abrir el PBI en el tablero y extraer alcance, criterios de aceptación, aplicación y sprint.
2. Leer los comentarios que desarrollo dejó en el PBI. Si el PBI volvió de una corrección, leer también el comentario del bug y la explicación de si cambió la base o la interfaz.
3. En CodeReview, abrir el pull request de la rama PBI y leer el diff. Ese paso lo adopta esta iniciativa. El lineamiento todavía no lo escribe como insumo del caso.
4. Abrir `docs/proyectos/apis-por-modulo.md` en el módulo del PBI. Esa fila dice qué endpoint entra al caso. Si la fila sigue vacía, el caso marca el endpoint como pendiente y no inventa el path.
5. Pasar a la IA el material ya filtrado, según la sección 5, más la fila del catálogo. La IA devuelve cuatro cosas, y las cuatro se piden en el mismo trabajo:
   - el análisis del alcance, con lo que el PBI cubre y lo que deja afuera;
   - la carpeta del Test Plan (aplicación, sprint, suite QA y carpeta `PBI-XXXXX`);
   - un caso por escenario, con el nombre `PBI-XXXXX #TC Título del escenario`, los pasos, el resultado esperado y el endpoint del catálogo cuando el PBI lo toca;
   - el comentario que QA va a dejar en el PBI, en el bug o en el impedimento.
6. El riesgo no se calcula con una fórmula propia. Hasta que el equipo la deje escrita, la IA ordena los casos con lo que el PBI ya trae (alcance, criterios y, en automatización, Priority y Effort). No se inventa una escala paralela.
7. QA revisa el borrador contra el manual de la aplicación y lo carga en Azure. El caso nace en Design. Pasa a Ready cuando el diseño está cerrado. Related work apunta al PBI. El comentario se publica en el work item que corresponda. Si el caso llama un endpoint, ese path es el de `apis-por-modulo.md`.

Si la IA no intervino, el caso no se da por diseñado y el comentario no se publica. El filtro de la sección 5 no es una forma de saltarse la IA: es la condición para usarla.

Plantillas del repo para el formato que la IA debe respetar: `prompts/plantillas/01-criterios-aceptacion.md`, `02-test-plan-suite-case.md` y `03-ejecucion-qa.md`.

---

## 3. Cómo se trabaja en Azure DevOps

El tablero, el Test Plan, el bug y el impedimento viven en Azure DevOps. Cada PBI del sprint nace con sus tareas de QA creadas, estimadas y asignadas.

### Estados del PBI

```
Committed → CodeReview → QA → Build → UAT → Ready4Deployment → DONE
```

No se saltan casillas. El bug recorre el mismo camino. Para devolver un hallazgo: QA → Committed → CodeReview → QA.

### Tareas por PBI

| Tarea | Qué se hace |
|---|---|
| QA - Recibir PBI | El desarrollador entrega a QA y al usuario |
| QA - Análisis y Diseño Caso Prueba | La IA analiza el PBI y redacta la carpeta del Test Plan y los casos. QA los revisa y los carga en Azure |
| QA - Preparación de data | Armar la data en el ambiente |
| QA - Ejecución Caso Prueba | Ejecutar en QA el caso, y el endpoint que el catálogo `apis-por-modulo.md` indique para ese módulo. Si falla, el bug se abre el mismo día |
| QA - Re test Caso de Prueba | Pedir a desarrollo qué cambió (base o interfaz). La IA redacta el comentario del re-test. QA lo publica y vuelve a probar |
| QA - Acompañamiento UAT-PRE | Entregar al usuario y acompañar |
| QA - Cargue de Evidencias UAT-PRE | Test Plan, PDF y adjunto en el PBI |
| QA - Documentación QA | Actualizar el manual si el PBI lo pide |
| QA - Acompañamiento pruebas UAT-POST | Acompañar en POST |
| QA - Cargue de Evidencias UAT-POST | Test Plan, PDF y adjunto en el PBI |

Ceremonias del sprint, también como tareas: Sprint Planning, Sprint Review, Refinamiento funcional, Retrospectiva, Daily (15 minutos) y Seguimiento QA.

### Test Plan, suite y caso

El Test Plan es de la aplicación. No se crea uno nuevo por PBI. Area Path e Iteration Path van según el tablero.

```
Test Plan [SR]
  └── SR / Sprint
        ├── QA
        │     └── PBI-XXXXX
        ├── UAT PRE
        └── UAT POST
```

El dibujo de `docs/manual-general.md` deja la carpeta del PBI bajo UAT POST. El lineamiento pide la subcarpeta del PBI para ejecutar y generar el PDF, dentro de la jerarquía del sprint. En la fase de diseño y ejecución la carpeta va en **QA**. UAT PRE y UAT POST se usan cuando prueba el usuario. Si el PBI no sale en el sprint, la carpeta se mueve al siguiente.

| Campo del caso | Convención |
|---|---|
| Nombre | `PBI-XXXXX #TC Título del escenario` |
| State | Design → Ready → Closed al cerrar el UAT |
| Tag | SR, AVR, PI o ROR |
| Related work | El PBI. Es obligatorio |
| Steps | Paso a paso con datos concretos, salidos del PBI y de los criterios |
| Evidencias | Capturas con fecha y hora de la ejecución |

### Bug, impedimento y UAT

El bug se abre el mismo día. Título: `PBI-XXXXX Breve descripción`. Activity: Development, Deployment, Requirements o Testing. Environment: DEV, QA, PRE o POST. Application Name: SR, AVR, PI o ROR. Severity de Azure: 1 Critical, 2 High, 3 Medium, 4 Low. Siempre ligado al PBI. En el cuerpo: pasos, URL o ambiente, esperado contra actual, evidencias con fecha y hora, y correo a desarrollo. El texto del bug y el comentario que QA deja en el PBI los redacta la IA. QA los revisa y los publica.

Al cerrar la corrección hay comentario de desarrollo y de QA. QA pide si el arreglo tocó base de datos o interfaz antes del re-test. Un cambio de alcance cierra el PBI y abre otro. Un incidente es un work item INC, separado del bug. La escala F-S-V (donde 4 es crítica) no se mezcla con la Severity de Azure.

Si no se puede probar por ambiente, permisos, data o usuario, el PBI pasa a **Build** y se abre un impedimento `PBI-XXXXX Breve descripción`. El comentario del impedimento lo redacta la IA y QA lo publica en el PBI. Máximo 5 días. Si va a durar más, se escala con los líderes. Al cerrarse el impedimento, el PBI vuelve al estado anterior.

UAT: QA entrega y el usuario prueba. El correo va al usuario de UAT y al equipo de pruebas. Asunto: `[Tablero] - Certificación y prueba UAT PRE PBI XXXXX - [Descripción]`. El adjunto trae la información del PBI. Los casos de QA se envían solo si el usuario los pide. VoBo y evidencias (Word o Excel) en 4 días hábiles. Después se cargan en el Test Plan, se genera el PDF y se adjunta al PBI.

### Automatización

| Pieza | Convención |
|---|---|
| UI | Selenium, Java, JUnit, data-driven. Código en inglés |
| API | Newman corre colecciones. No reemplaza a Selenium en UI |
| Repo | `[App]- Test` |
| Pipeline | `[App]-AUTOTESTF-CI` |
| Ramas | PBI → Release → Master. El pull request lo aprueba un líder Avianca |
| Ejecución | Ambiente QA, agente QA del cliente, con reporte y logs |
| En el Test Plan | Suite `Automatización_QA`, carpetas por módulo |
| PBI | Type `1. Automatización` (no impacta TTM). Lleva Priority, Effort y Business Value |
| Caso | `PBI-XXX Automatización # del caso: titulo` |
| Evidencias de automatización | SharePoint `EvidenciasAutomatizacionesFuncionalesQA`, carpeta por gerencia y aplicativo |

Permisos de repos y pipelines: los pide el equipo a los Champions del dominio.

---

## 4. Alcance por aplicación

Cada bloque se trabaja con PBIs del tablero de esa aplicación. Cada PBI sigue la sección 2 y la sección 3: la IA analiza el material filtrado, QA publica el Test Plan, los casos y los comentarios en Azure, y la verificación usa la base que el manual sí nombra.

### Accesos

Condición para empezar a ejecutar. Manual general, primera semana.

- Entrar a las cuatro apps en QA con Azure AD. ROR no está expuesto a internet: hace falta la red de Avianca.
- Tablero de Azure DevOps, repos `*-Test`, pipelines, SQL de QA y swaggers.
- Leer `lineamientos-qa.md` y el manual general.
- Seguir un valor faltante de punta a punta con las consultas de la sección 11 del manual general.

El servidor SQL de SR no está documentado. AVR, PI y ROR sí: `az-sqla-avref-use-qa`, `az-sqla-piccust-use-qa`, `az-sqla-orqrules-use-qa`.

### Valores faltantes

Único recorrido escrito de punta a punta entre SR, PI y AVR. Es el primer flujo que se diseña en el Test Plan.

1. Radicar en SR: Procesos → Formulario Captura Reembolsos Faltantes. Estado: Pendiente de Autorización. Tablas `SR_MISSING_VALUE_REFUNDS_VF` y `SR_MISSING_VALUE_REFUND_STATUS_LOG_VF`.
2. Aprobar. Coordinador si el monto es de hasta 3500 USD. Gerente si pasa de 3500. TRM en `SR_EXCHANGE_RATES` y umbral en `MST_APPROVAL_RANGE`. Con varios tiquetes, el envío a PI espera a que todos estén aprobados.
3. PI recibe en `PIC_PAYMENT_REQUEST_VF` y `PIC_PAYMENT_DETAIL_VF`. Paga con FOP KR (voucher) o NC (ACM). Notifica a SR. Estado en SR: Pagado.
4. AVR envía NTC23 si FOP es KR, o NTC24 si FOP es NC. Registro en `AVR_CONTROL_NOTIFICATIONS`.

Si el envío a PI falla, la solicitud vuelve a Pendiente de Autorización.

Datos al radicar: número de solicitud (alfanumérico, máximo 32), tiquete de 13 dígitos con placa 134, 202, 133 o 547, PNR de 6 caracteres, IATA de 8 dígitos, moneda desde GetCurrencyList, valor faltante con máximo 2 decimales y no mayor al total de la venta, forma de pago KR o NC (`MVR_FOP_LIST`), razón desde `MST_MISSING_REASONS`.

Estados del listado: Pendiente de Autorización, Autorizado, En progreso, Pagado, REJECTED. El relato de envío a PI también dice «En proceso». El caso de prueba verifica el literal que quede en la base. No se elige uno de los dos.

Referencia de casos ya escritos en el repo: `paquetes/vf-valores-faltantes/`.

### Solicitud individual en SR

Cinco pantallas. El canal es interno (casos especiales). El pasajero común entra por la web o la app, y ese front no está detallado aquí.

1. Inicio: reserva, tiquete o EMD. GetInfoTicket. Si no hay datos, código 1110 y el mensaje de PNR y apellidos. Ahí se puede seguir con el formulario manual.
2. Pasajeros: fecha de solicitud (no posterior a hoy), tiquetes, titular. GetRefundInfo. Si el canal es LifeMiles, viajero frecuente de 11 dígitos. Si la reserva es corporativa, aparece el código corporativo.
3. Solicitud: detalle de pago y forma de pago. Tarjeta de crédito salta a la confirmación. Transferencia bancaria (CR) pasa a datos bancarios. Excepción (el manual muestra Defunción, o titular menor de edad) va a revisión y fuerza transferencia.
4. Datos bancarios: país y campos según las maestras de PI (`CUR_CURRENCY_COUNTRY`, `MST_SCREEN_FIELD_BANK`), vía GetMasterInfo. Certificado bancario opcional en el flujo del manual.
5. Confirmación: forma de pago, reserva, número de caso y total. Verificar en Mozart y en `AVR_INFORMATION_PASSENGER` y `AVR_INFORMATION_ADDITIONAL_PASSENGER`.

### Cargue masivo en SR

Archivo CSV o XLSX. Menú Procesos → Solicitudes masivas de reembolso. La Function `az-fapp-sprefprocess-use-qa` procesa la carga. Estados: N (no procesado), I (en proceso), C (exitoso), E (reintento), F (fallido). Tope de reintentos: parámetro `MAX_RETRIES_MASS_SENDING`, documentado como máximo 5 en el manual general. Columnas de entrada que el manual nombra, entre otras: Apply_ard, Booking, TktNumber, Channel, RequestDate, Exception, FrequentFlyerNumber, Email, Name, LastName, Fop. Con `Apply_ard = Y` la consulta busca tiquetes en otras bases, entre ellas Amadeus.

### Seguimiento en AVR

- El orquestador deja un registro del caso calculado (id, fecha y hora, estado). Si el cliente acepta o rechaza, el registro se elimina.
- A los 30 minutos sin esa acción, Purge Refund pide a Mozart el cierre por time out. El manual usa dos textos: «en validación por el cliente» y «en evaluación». Se confirma el literal en base.
- Catálogo NTC en AVR §10.4. En este alcance importan, con el disparador que el manual sí escribe: NTC19 cuando hay cash sin datos bancarios, NTC23 y NTC24 en valores faltantes. El resto del catálogo se prueba cuando el PBI nombre esa notificación. No se asigna un código NTC a un motivo que el manual no ate.
- Consulta tu Reembolso y adjuntos en Blob Storage, según AVR §10.1 y §10.2.
- Inactivación de usuario a los 90 días, aviso a los 80. Function del proceso de SR: `az-fapp-sprefprocess-use-qa`. En AVR el mismo criterio de 90 días está en el ingreso al sistema.

### Pago en PI

Cuando el caso ya está aprobado, Mozart envía la solicitud de pago y recibe el cambio de estado. SAP4HANA ejecuta el cash a cuenta bancaria.

Alcance de prueba por módulo, en el orden del manual:

- Plantillas de pago: tarjeta de crédito, voucher, BAC, Cardinal, Credibanco, Cielo, Redeban, Santander y otros pagos manuales.
- Cargue de resultados y de rechazados. Reapertura bancaria.
- Gestión de pago: autorizar, generar voucher, enviar notificación.
- Gestión de pago ACM. Envío a SAP de cash (CR) y de ACM (NC), incluido ACM de valores faltantes.
- Maestras que SR consume en datos bancarios: Datos bancarios, Moneda por país, Formas de pago, Bancos, Tipos de cuenta, Países.
- APIs que el manual nombra para la cadena: Payment Refund Request, GetCurrencyList en APIM, Bank_Data_Information, Check Payment Status, MissingModules (valores faltantes de SR a PI).

El path REST que el manual no escribe no se inventa. Se prueba por el nombre de la API y el swagger.

### Reglas en ROR

ROR no entra en la cadena de radicación ni de pago. El alcance comprueba que el orquestador puede leer lo que negocio parametriza.

- Maestra EMD: Maestras → Documento misceláneo. Crear, consultar y modificar.
- `ListHomologation` lee `master.MS_HOMOLOGATION_REFERENCE_VALUES`. Campo `ReferenceValueOrig` vacío trae todos los registros. Con valor, uno.
- `EmdGetRfisc` consulta por `Emdcode`. El relato usa `master.MST_EMD`. Una nota escribe `Master.MST.EMD`. Se verifica el objeto en la base antes de dejar el caso en Ready.
- Swagger: `azwappsorqrulesextsuseqa…/Swagger`. El path REST no está en el manual.
- Inactivación: SP `[rfd].[ROR_DEACTIVITY_USER]` sobre `az-sqla-orqrules-use-qa`. Aviso a los 80 días con `[rfd].[ROR_USERS_FOR_NOTIFICACION_OF_INACTIVITY]`. Log en `[rfd].[LOGS_TRANSACTION]`.
- El reporte de auditoría del manual ejecuta `[rfd].[AVR_SP_USER_DATA_QUERY]`. Se usa ese nombre literal. No se inventa un SP con prefijo ROR.

### Automatización de lo ya estable

Solo flujos que ya pasaron por QA manual y quedaron asociados a un PBI. Prioridad de negocio: valores faltantes de punta a punta, y después la solicitud individual hasta la confirmación en Mozart.

- UI en Selenium, dentro del repo `[App]- Test` y del pipeline `[App]-AUTOTESTF-CI`.
- API de valores faltantes, NTC y ROR con Newman, en el pipeline, sin sustituir la UI.
- Ejecución en QA, con reporte y logs.
- Casos en la suite `Automatización_QA`.

---

## 5. Análisis de seguridad

Se revisa lo que los manuales ya fijan como control. No se abre un ejercicio de intrusión ni se documentan pasos de ataque. Donde el manual dice que el historial de pruebas de seguridad es N/A, el plan lo deja así.

| Control | Dónde está | Qué se verifica en QA |
|---|---|---|
| Ingreso con Azure AD | Las cuatro apps, sección de ingreso | Sin sesión Microsoft no entra al front |
| Inactivación a los 90 días y aviso a los 80 | SR, AVR, PI y ROR | El parámetro `USER_INACTIVITY_DAYS` y el aviso `PRE_INACTIVATION_NOTIFICATION`. En ROR, los SP de la sección de reglas |
| ROR fuera de internet | Manual ROR §2.6 | El front solo responde en la red de Avianca |
| APIM con la autenticación definida | PI, GetCurrencyList | El llamado sigue el token que el manual describe para APIM. No se publica otro mecanismo |
| Secretos en Key Vault | Arquitectura de SR, AVR, PI y ROR | El secreto no queda en el caso de prueba, en el Excel ni en el repositorio |
| Ambientes | Manual general §2 | La ejecución de este plan usa DEV, QA, PRE y POST |
| Retención de logs | App Insights: 90 días en SR, AVR y PI; 30 días en ROR | Un hallazgo de log viejo se contrasta contra esa retención antes de reportarlo como defecto |
| Retención de datos | SR 1 año. AVR 3 años más 2 de histórica. PI 24 meses en la transaccional. ROR 1 año | La data de prueba no se arma sobre registros que el proceso de historia ya debía depurar |
| Evidencia | Lineamientos de bug y de caso | La captura lleva fecha y hora. No se adjunta un secreto, un token ni un certificado bancario real |

### Qué no se le entrega a una IA

La IA se usa en todos los PBI. Los lineamientos no hablan de esa herramienta, así que esta regla es de la iniciativa. El texto que se le entrega sale del tenant y puede quedar en el historial de la herramienta. Por eso el filtro va antes del análisis, no en lugar del análisis.

El riesgo es concreto. Un diff, un `appsettings`, un pipeline o un comentario de desarrollo puede traer una llave de Key Vault, un token de APIM, un PAT de Azure DevOps, una cadena de conexión o un certificado bancario. También puede traer datos del pasajero que el caso de reembolso usa: PNR, tiquete, correo, nombre y cuenta. Los manuales ya dicen que el secreto vive en Key Vault y que no va en el caso, en el Excel ni en el repositorio. Mostrárselo a una IA lo saca de ese control.

Antes de pegar algo del repo o del pull request:

| Se puede usar como contexto | No se pega |
|---|---|
| Alcance del PBI, criterios de aceptación y el nombre del caso | Secretos, tokens, PAT, cadenas de conexión y contenido de Key Vault |
| Un diff recortado al método o a la pantalla que el PBI cambia, ya revisado | El diff completo de la rama, ni archivos de configuración, ni variables del pipeline |
| Nombres de tablas y estados que ya están en el manual | Resultados de SQL con datos de un pasajero, ni certificados bancarios, ni adjuntos del caso |
| La estructura del Test Plan y el formato `PBI-XXXXX #TC` | Capturas donde se lean credenciales, tokens o datos bancarios |

Si el diff o el comentario trae una de esas piezas, se saca antes de continuar. No se pide a la IA que «ignore» el secreto que ya quedó en el mensaje. Si hizo falta para entender el cambio, se describe el efecto (qué pantalla o qué estado cambió) y se deja el valor afuera.

La sección de historial de pruebas de performance y seguridad de ROR está en N/A. SR declara la misma sección. Esos capítulos no se rellenan con un alcance inventado.

---

## 6. Orden de salida y criterio de cierre

El orden es el del manual general: primero el valor faltante de punta a punta, después el resto de SR, y en paralelo el módulo de PI o de ROR que el PBI del sprint nombre.

Un PBI se cierra cuando:

1. La IA analizó el PBI, los comentarios de desarrollo y, si hubo pull request, el diff ya filtrado. Sin ese análisis el PBI no se cierra.
2. Los casos que publicó QA salieron de ese borrador. Están en el Test Plan de la aplicación, en la carpeta del PBI, con Related work. Los comentarios de QA en el PBI, en el bug o en el impedimento también salieron de la IA.
3. La ejecución en QA tiene evidencias con fecha y hora.
4. Los defectos abiertos recorrieron el tablero, o quedaron devueltos a Committed con evidencia.
5. El UAT-PRE tiene VoBo, PDF en el PBI y, cuando aplique, el UAT-POST.
6. Si el PBI lo pide, el manual de la aplicación quedó actualizado.

---

## 7. Contradicciones que este plan no resuelve

Se confirman en la pantalla o en la base. No se elige una versión de memoria.

| Tema | Qué dicen las fuentes | Qué hace el caso |
|---|---|---|
| Propósito de SR | El §5 copia el texto de AVR (recibe información de Mozart). La identificación dice canal de casos especiales, sin lógica de negocio de reembolso | Se usa la identificación |
| Pago | El alcance de AVR abre diciendo que administra el pago ya aprobado. PI §2.1 y el componente Mozart de PI describen la ejecución del pago | El pago se prueba en PI. En AVR se prueban timeout y NTC |
| Estado de VF hacia PI | El listado dice «En progreso». El relato de envío dice «En proceso» | Se verifica el literal persistido |
| ROR presentado como SR | El §1.1 y el §9 dicen Special Refund. La URL es `orqrules` y la base es `az-sqla-orqrules-use-qa` | Se trata como ROR |
| Tabla EMD | `master.MST_EMD` y `Master.MST.EMD` | Se confirma el objeto en la base |
| SP de auditoría en ROR | El manual escribe `[rfd].[AVR_SP_USER_DATA_QUERY]` | Se usa ese literal |
| Severity | Azure: 1 = Critical. F-S-V: 4 = Crítica | En el work item de Azure se usa la escala 1 a 4 de los lineamientos |

---

## Calibración

| Afirmación | Fuente buscada | Resultado | Acción |
|---|---|---|---|
| Cadena SR → Mozart/APIM → AVR → PI, y ROR al lado | `docs/manual-general.md` §1 y mapa de productos | CONFIRMADO | Sección 1 |
| El caso sale del alcance del PBI y se carga al Test Plan | `lineamientos-qa.md`, tarea Análisis y Diseño | CONFIRMADO | Sección 2 |
| Comentarios de desarrollo y QA al resolver el bug. En el re-test se pregunta si cambió la base o la interfaz | `lineamientos-qa.md` y `prompts/plantillas/03-ejecucion-qa.md` | CONFIRMADO | Sección 2 |
| Leer el diff del pull request antes de diseñar el caso | `lineamientos-qa.md` | SIN RESPALDO | La iniciativa lo adopta. El lineamiento solo exige la rama PBI y el pull request aprobado por un líder |
| Fórmula para calcular el riesgo del caso | `lineamientos-qa.md` y `docs/manual-general.md` | SIN RESPALDO | No se inventa escala. Se usa el alcance del PBI y, en automatización, Priority y Effort |
| Estados del tablero, tareas, bug, impedimento, UAT y Selenium | `lineamientos-qa.md` y manual general §5 a §10 | CONFIRMADO | Sección 3 |
| VF, roles 3500 USD, NTC23 y NTC24 | Manual SR §7.2.4, manual AVR §10.4, manual general §3 | CONFIRMADO | Valores faltantes |
| «En progreso» y «En proceso» | Manual SR | CONTRADICCIÓN | El caso verifica el literal |
| Front de ROR no expuesto a internet. Inactivación a 90 días | Manual ROR §2.6 y §9.1 | CONFIRMADO | Reglas y seguridad |
| Historial de pruebas de seguridad de ROR en N/A | Manual ROR §11 | CONFIRMADO | No se inventa alcance |
| La IA analiza cada PBI y redacta Test Plan, casos y comentarios | `lineamientos-qa.md` | SIN RESPALDO | Regla de esta iniciativa, sección 2. El lineamiento exige el caso en el Test Plan y el comentario en el work item. No menciona la IA |
| El caso usa el endpoint de `docs/proyectos/apis-por-modulo.md` | Ese archivo | SIN RESPALDO | El catálogo está creado y vacío. El path se escribe cuando se confirme en swagger o en el manual |
| Pegar el repo o el diff en una IA sin filtrar | `lineamientos-qa.md` y manuales de las cuatro apps | SIN RESPALDO | El uso de la IA es obligatorio. El filtro de la sección 5 también. El secreto sigue en Key Vault y fuera del caso, del Excel y del repositorio |

---
Validación: PASÓ CON ADVERTENCIAS
Fuentes del producto: `docs/manual-general.md`, `base_conocimiento/lineamientos-qa.md`, `manual-aplicacion-sr.md`, `manual-aplicacion-avr.md`, `manual-aplicacion-pi.md`, `manual-aplicacion-ror.md`
