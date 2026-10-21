Lineamientos QA
Calidad y Automatización de Pruebas
Junio 2024
V. 10.
Lineamientos QA
Agenda
01 Documentación Test Plan
02 Documentación Test Suite
03 Documentación Test Cases
04 Documentación de Bugs
05
Documentación Impedimentos
06
Reporte Tareas QA en VSTS
07
Evidencias Usuarios
08
09
Automatización- Manejo de
Información Azure DevOps
Automatización- Lineamientos
Documentación de Test Plan
Al definir el nombre del Test Plan, se debe incluir el nombre de la aplicación, esto es para efectos de mayor organización y mejor lectura
de cualquier integrante de su equipo. Ejemplo: “Test Plan [TIS]”.
El Area Path y la Iteration Path, es de acuerdo al tablero.
Documentación de Test Suite
Crear las Test Suite por reléase o sprint para poder utilizar el tablero de manera estándar y saber en el despliegue que PBI´s estuvieron
comprometidas y que contenga de manera jerárquica los diferentes Test Suites para cada responsable (Ejemplo: QA, UAT PRE, UAT
POST)
Documentación de Test Case
❑ Crear una subcarpeta por PBI para ejecutar y así generar los .pdf correspondientes.
• Si en el sprint actual no se libera el PBI, se hace necesario que se mueva la carpeta o el test case al sprint siguiente con el fin de
visualizar en el tablero la información actualizada de las ejecuciones.
Documentación de Test Case
❑ Nombre del caso: Ingrese el nombre del caso siguiendo el formato “PBI-XXXXX #TC Titulo del escenario”
❑ Asignación del caso: Seleccione del listado de usuarios la persona que realizará la ejecución.
❑ Add tag: Seleccione del listado de aplicaciones la aplicación que documentará.
❑ State: Inicialmente aparece en Design. Una vez termine de diseñar el caso, se debe cambiar a Ready. Una vez finalizada la
prueba en estado UAT se debe cambiar a Closed.
❑ Area: Seleccione el tablero al cual pertenece el caso de prueba.
❑ Iteration: Seleccione el tablero y Sprint donde se ejecutará este caso de prueba.
❑ Related work: Especifique el PBI relacionado al caso de prueba (esto es muy importante ya que servirá para documentar
correctamente las pruebas ejecutadas previo a salir a producción).
❑ Steps: Ingrese el paso a paso a seguir para ejecutar el caso de prueba.
❑ Adjuntar evidencias (Prints) con fecha y hora correspondiente a la ejecución del caso.
Documentación de Bugs
1. 2. 3. 4. 5. 6. 7. El BUG debe ser creado inmediatamente se encuentre el defecto el cual debe contener Una Entrada con lo siguiente:
El campo Titulo va con el nombramiento de los Bugs acorde a la estructura “PBI-XXXXX Breve descripción” para determinar
a qué PBI está relacionado y poderlo relacionar de manera ágil en el tablero de indicadores
En el campo Activity se debe indicar de quien es responsabilidad el Bug (development, design, deployment, requirements,
testing, etc). Se definió lo siguiente:
• Development --> Si el bug lo inyectó el equipo de desarrollo
• Deployment --> Si el bug se generó por un mal despliegue en ambiente
• Requirements --> Si el bug es por una definición errónea o incompleta del PBI donde se originó el bug.
• Testing --> si el bug es por un entendimiento errado del caso de prueba o bug encontrado en UAT.
El campo Enviroment, es donde se encontró el bug (DEV , QA, PRE, POST
El campo Area, se debe especificar cual es el tablero al que pertenece el bug
El campo Iteration, se debe especificar cual es el tablero y el Sprint donde se encontró el bug
El campo Aplicaction Name, se debe indicar la aplicación, en la que se encontró el bug, por ejemplo : RTS.
El campo Severity 4 - low, 3 - Medium, 2 - High, 1 - critical según el grado del bug.
“El BUG debe ser creado inmediatamente se encuentre el defecto”
Documentación de Bugs
En el bug se debe evidenciar el proceso y se debe mostrar el resultado obtenido con imágenes: Dentro de este ítem debe
indicarse el proceso realizado para la detección del bug encontrado, indicando en detalle porque se considera un bug “Detalle
de los datos para generar el bug” para lo cual se debe considerar:
8. 9. Adjuntar evidencias con fecha y hora visibles
Indicar los pasos para replicar el error
10. Indicar la URL de pruebas, o el ambiente en que se ejecutaron las pruebas
11. Enviar un correo al equipo de desarrollo con los bugs encontrados para seguimiento del equipo y obtener fechas de
solución o hacer el seguimiento en VSTS.
Nota: Los PBIs, podrán tener múltiples bugs, todo dependerá del QA que se encuentre realizando las pruebas, si desea crear
un bug para cada hallazgo o un bug general, siempre y cuando todos los hallazgos correspondan a la misma activity.
▪ Después de creado el BUG y asignado este deberá ser tratado como si fuese un PBI, debe moverse por todos los
estados
▪ Se debe estimar los tiempos tanto de DEV como de QA
▪ Se debe tener un desarrollador asignado en caso de que sea temas de desarrollo
▪ Se debe tener comentarios tanto del desarrollador como del QA al momento de ser solucionado.
Documentación de Bugs
Nota: Si se detecta que el BUG creado en QA, no era un BUG, se debe mover el campo activity dependiendo en donde
fue detectado y dejar el comentario de porque es considerado como “no bug”.
Acorde a lo anterior si el bug es por hallazgos en el desarrollo el campo: “activity” se debe mantener como development
hasta llegar a Done.
Si por el contrario el caso es “no bug”, el equipo de Dev debe cambiar el campo: “activity” a quien corresponda (design,
deployment, requirements, testing,) y dejar el comentario y/o justificación en una nota.
Para finalizar el bug se debe tener presente una definición clara de los criterios de aceptación para considerar un bug
resuelto: Luego de que el bug se devuelve a QA para las pruebas, se debe validar los siguientes pasos:
12. Solicitar explicación a la persona que resolvió el bug, para validar si el bug encontrado hizo cambios en BD, o interfaz de
usuario.
13. Realizar un test de pruebas para validar que el bug no se siga presentando o la solución afecta algo más.
14. Mostrar el proceso obtenido, detallando en la evidencia los resultados que se obtuvieron al momento de realizar la
prueba y adjuntar las evidencias del resultado obtenido en caso de que el bug se resuelva o no.
Documentación de Bugs
15. Cada bug debe estar relacionado a un PBI.
16. Por último, cerrar el bug y continuar con las pruebas del PBI que deberá pasar de Commited, a CodeReview, a QA, a Build,
a UAT, Ready4Deployment y DONE.
Nota: Si se detecta en desarrollo o QA que en PBI requiere un cambio de alcance se debe crear un nuevo PBI y cerrar el PBI
en el que se está trabajando y no se debe crear un bug para estos temas o modificar el PBI que se está trabajando, dado que
esto afecta los tiempos estimados que deberán ser también modificados, tanto en desarrollo como en QA.
Si el BUG fue detectado en UAT, se deben revisar todas las pruebas del PBI antes de pasar el PBI al usurario para las pruebas en UAT.
Documentación de Bugs
❑ Consultando la historia de los tiempos y movimientos de cada PBI y BUG, es posible sumar el tiempo exacto de ellos
durante su permanencia en cada casilla, pudiéndose de esta manera devolver dicho PBI y Bug a la casilla de Committed
para su ajuste por parte del desarrollador.
Por ahora quedamos en que el PBI se podría devolver y no tener estados intermedios..
❑ De QA a Commited
❑ De Commited a CodeReview a QA
✓ Separar un bug de un incidente- Manejarlos como Work Item de manera separada:
INC y BUG
✓ Se acordó con el equipo de Champions que los bugs quedarían por separado (solo para temas de defectos) y se moverían
de manera lineal.
✓ El Bug si se cierra en QA, entonces debe llevarse por cada uno de los estados hasta el estado Done, esto para no impactar
las gráficas. “No se deben saltar las casillas”.
✓ Lo Incidentes se manejarán con INC, como Work Items separados para así poder visualizarlos dentro de los tableros
Documentación de Bugs
Ejemplo de BUG
Documentación de Impedimentos
Existen escenarios donde se tienen PBIs en QA pero no es posible testear por temas de ambiente, permisos o impedimentos
que NO son de desarrollo, en estos casos los PBI se deben mover al estado BUILD y se les creara el impedimento
correspondiente.
1. El nombramiento de los Impedimentos con la estructura “PBI-XXXXX Breve descripción” para determinar a qué PBI están
relacionados y poderlos relacionar de manera ágil en el tablero de indicadores
2. En los comentarios del pbi se debe de comentar que se creó un impedimento, relacionando el mismo y pasando el pbi al
estado build.
3. Cuando el impedimento se solucione, se debe de cerrar y el pbi debe de retornar al estado anterior al impedimento.
Documentación de Impedimentos
❑ Para el manejo de los Impedimentos y la creación de estos se estableció unos criterios estándar que se podrán manejar al
momento de crear el Impedimento:
1. Disponibilidad de usuario por priorización: después de pasados los 4 días en UAT o si el usuario no da espacio para
entrega.
2. 3. Disponibilidad de usuario por cierre: En caso de que el usuario reporte que está en cierre contable.
Falla ajena al desarrollo de PBI: si se presentan fallas con el ambiente o configuraciones que no dependen del
desarrollo del PBI o INC, o problemas con la Data.
4. Pendiente de asignación por prioridades y disponibilidad del equipo QA: si el team de QA supera la carga de asignación.
Se requiere que el PBI tenga justificación en VSTS de las horas ejecutadas en otros PBIs y por lo cual se ha dejado el PBI en
Build por disponibilidad.
Nota: Los PBIs podrán estar en Build máximo 5 días dentro del sprint, si el PBI va a tomar más tiempo se deberá poner en
consideración con los lideres del equipo para evaluar el manejo y el paso a seguir para no afectar los tiempos en el tablero.
El impedimento creado quedará en estado OPEN y se deberá cerrar tan pronto se solucione o se superen los 5 días que podrá
quedar en este estado.
“Tener presente que el PBI o INC se debe mantener en el estado Build mientras el impedimento se encuentre abierto”
Reporte de Tareas QA por PBI en Azure DevOps
A continuación, se detallan las actividades que se deben de crear al momento del Planning e ir ejecutando día a día del Sprint por todos los
integrantes del team QA:
-Al iniciar Sprint cada pbi que se trabajara debe contar con todas las tareas creadas, estimadas y asignadas al QA responsable de su
ejecución durante el sprint.
Tareas Descripción
QA - Recibir PBI Se tiene sesión de review, en la cual el Desarrollador realiza la entrega a QA y al usuario
QA - Análisis y Diseño Caso Prueba
Se realiza un análisis del alcance del PBI para el diseño de los test case y se realiza el diseño
del test case para la ejecución de las pruebas y se carga en el test plan
QA - Preparación de data Se realiza el diseño y la preparación de la data requerida para la prueba
QA - Ejecución Caso Prueba Ejecución de las pruebas en el ambiente de QA
QA - Re test Caso de Prueba En caso de pruebas fallidas se realiza el re-test de las pruebas (BUGS)
QA - Acompañamiento UAT-PRE
Se realiza la entrega al usuario del PBI. Acompañamiento en la ejecución de las pruebas
UAT-PRE
QA - Cargue de Evidencias UAT-PRE
Se carga las evidencias de las pruebas UAT-PRE en test Plan, se genera el PDF y se adjunta
en el PBI
QA -Documentación QA Se actualiza el Manual de acuerdo con lo solicitado en el PBI
QA - Acompañamiento pruebas UAT-POST Se realiza el acompañamiento para realizar las pruebas UAT-POST
QA - Cargue de Evidencias UAT-POST
Se carga las evidencias de las pruebas UAT-POST en test Plan, se genera el PDF y se adjunta
en el PBI
Reporte de Tareas Ceremonias Scrum en Azure DevOps
Estas tareas se crean desde el inicio de cada Sprint y se van ejecutando durante el mismo
Sprint Planning Se confirma los PBIs a trabajar en el sprint
Sprint Review
Se informa el estado en el que queda los PBIs
finalizando el sprint y lo que queda pendiente para
continuar en el siguiente sprint
Refinamiento
Funcional
Explicación de los PBIs que van a ingresar al sprint,
en el que se especifica lo que requiere el usuario
Sprint
Retrospectiva
Lo positivo del sprint ejecutado y lo que se debe
mejorar para los siguientes sprint
Daily's
Sesión diaria de 15minutos donde se informa lo
realizado el día anterior laborado, lo que se va a
realizar el día actual y si se tiene algún
impedimento para ejecutar las pruebas
Seguimiento QA
Sesión en la que se revisa el avance de cada caso
en curso y si se presenta algún impedimento
Gestión TCS Gestión TCS
Capacitación QA Capacitación QA " Contextualización
Evidencias Usuarios
Luego de hacer entrega al usuario del PBI es necesario enviar un mail formalizando la entrega con las siguientes indicaciones:
1. El mail debe ser enviado al grupo o al usuario que realizará las pruebas UAT-PRE y adicional el equipo de pruebas, si es necesario al
líder técnico
2. Asunto: como se describe a continuación:
-
“Nombre del tablero en el que se encuentre el PBI”
- Certificación y prueba UAT PRE PBI XXXXX -
“Descripción del PBI”
3. Contenido del Mail:
Con el objetivo de dar cierre al PBI xxxxx -
archivo para iniciar la ejecución de pruebas UAT-PRE.
“Descripción del PBI”, envío como adjunto
De ser satisfactorias, es necesario recibir el VoBo y evidencias UAT-PRE, en los 4 días
hábiles siguientes al envío de este mail.
Quedo pendiente de si se requiere alguna validación adicional y/o acompañamiento.
Gracias,
“Firma”
4. 5. El archivo que se envía como adjunto, debe contener la información del PBI para que el usuario o usuarios realicen sus casos de
prueba y las pruebas pertinentes para el VoBO, no es necesario enviar las pruebas que se realizaron, dado que se requiere es que el
usuario realice sus pruebas y no que apruebe las ya realizadas por el equipo de QA, de ser necesario o si el usuario lo solicita se
pueden compartir los casos de prueba.
El usuario podrá enviar las evidencias en formato Word o Excel
Lineamientos evidencias Usuarios
Ejemplo del envío de un mail:
Ejemplo de un archivo adjunto:
Automatización de
Pruebas Funcionales
Manejo de Información Azure DevOps
Test Plan Test Suite
Se debe seleccionar el Test Plan del aplicativo
correspondiente a automatización.
Dentro del Test Plan de cada proyecto, se debe
crear una suite llamada: “Automatización_QA”,
allí se debe organizar por carpetas los módulos
correspondientes a automatización
Manejo de Información Azure DevOps
PBI
Las PBIs deben de ser creadas completando todos los datos requeridos:
Titulo: Nombre del Aplicativo: Automatización de pruebas- Modulo XXX
Descripción: Descripción general del PBI
Criterios de Aceptación: Se debe de colocar todos los criterios de aceptación
definidos a nivel de negocio
Details:
Priority: Prioridad a nivel de negocio
Effort: Esfuerzo en horas estimadas para la PBI
Business Value: Valor de la PBI a nivel de negocio
Type: En caso de ser una PBI de automatización colocar
“1. Automatización “ (Para no impactar el TTM)
Application Name: Nombre de la Aplicación
Test Case
El nombramiento de los Test Case de Automatización debe ser: “PBI-
XXX Automatización # del caso: titulo”
Manejo de Información Azure DevOps
Sharepoint
✓ Se tiene un Sharepoint General para el proyecto de
Automatización.
https://avianca.sharepoint.com/sites/EvidenciasAutomatizacionesF
uncionalesQA
✓ El sharepoint esta organizado por carpetas por Gerencia y dentro
de ella, las carpetas con los aplicativos correspondientes
* Para los proyectos que inicialmente manejan la información en
Teams, deberán migrarlo al Sharepoint para tener toda la información
centralizada
Wiki
✓ Se creara en la wiki de cada dominio una sección llamada
“Automatización_QA”, allí estarán todos los enlaces donde se
encuentra la información en el Sharepoint
Lineamientos
La automatización del aplicativo debe estar enfocada las
funcionalidades más importantes a nivel de negocio y una vez
definidos los flujos deben estar asociados a los PBIs dentro de
Azure DevOps de Avianca
Herramientas
El desarrollo de la automatización debe construirse sobre
herramientas Microsoft o compatibles con Azure DevOps para
ser ejecutadas dentro de un agente de CI/CD *
.
El framework oficial de la Automatización de pruebas
funcionales es Selenium
Para automatizaciones en Java se debe utilizar JUnit como
framework de construcción
Para el manejo de Datos se debe utilizar un archivo Data
Driven Inicialmente
Lineamientos
Los pull request deben ser aprobados por un líder
Avianca
El código de la automatización de pruebas debe estar
versionado y asociado a un repositorio. El
nombramiento de los repositorios debe ser: “Nombre
del aplicativo- Test”
La automatización de las pruebas debe configurarse
dentro de un pipeline de CD* para verificar el despliegue
de la aplicación. El nombramiento de los pipelines debe
ser: “Nombre del Aplicativo-AUTOTESTF-CI”. Ej.
FlyUp-AUTOTESTF-CI
El código se debe manejar con el manejo de ramas
correspondiente Rama PBI → Rama Release → Rama
Master
Repositorios
Pipelines
Ramas
Lineamientos
El equipo deberá solicitar permisos para acceder a los Repos y Pipelines
de su dominio (Champions del dominio)
Las ejecuciones de la automatización se deben realizar sobre
el ambiente QA
Debe existir independencia del código, es decir, estructura por
modulo, feature, runner y step definition
El código debe ser desarrollado en el idioma Ingles
Al ejecutar la prueba funcional dentro del pipeline se debe
poder verificar la ejecución a través de un reporte
Se debe programar de forma concurrente la ejecución
de la automatización de las pruebas, por ejemplo, que
cada semana se ejecute un set de pruebas en la noche
o en horario no laboral
La ejecución de la automatización se realizará en un Agente
QA designado por el cliente
Toda ejecución debe dejar un registro de Logs de la ejecución
indicando éxito o errores por excepciones
¡Gracias!