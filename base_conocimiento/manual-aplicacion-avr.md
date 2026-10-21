Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
MANUAL DE APLICACIÓN
AVR
(AV Refund)
Historial de Cambios y Revisiones del Documento
1
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Versión
Documento Fecha Modificado
por Secciones, páginas y texto afectado
1.0 13-10-2023 Jenny Garzón Se crea el Manual Funcional AV Refund).
1.1 09-09-2024 Isabel Guerra Se agrega funcionalidad de Gestion de roles y permisos
(Crear, Modificar y Consultar)
1.2 04-10-2024 Camilo Loaiza Se añade la sección de la API para replicar adjunto en BS.
1.3 08-04-2025 Jenny Garzón Se agrega el api de Consulta tu Reembolso
1.4 06-06-2025 Jenny Garzón Se agrega Inactivación de Usuario, en la sección de Ingreso
al Sistema
1.5 31-07-2025 Dumar Ojeda Se adiciona funcionamiento de API Sendrig - Notificaciones
1.6 22-09-2025 Jenny Garzón Se agrega campo IP en el request del API Sendrig -
Notificaciones
1.7 06-10-2025 Jenny Garzón Se agrega el procedimiento: Purge Refund
1.8 10-11-2025 Jenny Garzón Se agrega la NTC 19 - Completa tus datos bancarios
1.9 17-12-2025 Jenny Garzón Se agrega el menú de Impuestos y Querys reporte usuarios
Auditoria
2.0 29-12-2025 Jenny Garzón Se agrega el menú de Parámetros del Sistema
2.1 05-06-2026 Jenny Garzón Se actualiza imágenes de todo el front por actualización de
versión de Angular de 17 a la 20
2.2 26-08-2026 Jenny Garzón Se agrega NTC23 y NTC24
Aceptación del Manual de Aplicación
Elaborado por: Revisado por: Aprobado por:
2
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
1. CONTENIDO
1. INTRODUCCIÓN ......................................................................................................... 4
2. PRESENTACIÓN DEL APLICATIVO ...................................................................... 5
2.1. Identificación ............................................................................................................. 5
2.2. Alcance ........................................................................................................................ 5
3. Arquitectura ................................................................................................................. 6
3.1. Especificación detallada de los componentes: ............................................... 6
4. PUESTA EN AMBIENTE PRUEBAS O PRODUCCIÓN ...................................... 9
4.1. Despliegue en ambiente de pruebas ................................................................. 10
5. PROCESO DE ROLL BACK ................................................................................... 10
6. DESCRIPCIÓN DE LA FUNCIONALIDAD ........................................................... 10
7. INGRESO AL SISTEMA ........................................................................................... 10
7.1. Inactivación de Usuario ........................................................................................ 11
8. Descripción del perfil de usuario......................................................................... 13
9. MÓDULOS .................................................................................................................. 13
9.1. ADMINISTRACIÓN .................................................................................................. 13
9.1.1. Gestión de Menús....................................................................... 13
9.1.2. Gestión de Roles ........................................................................ 15
9.1.3. Gestión de Usuarios .................................................................. 17
9.2. MAESTRAS ............................................................................................................... 18
9.2.1. Impuestos ..................................................................................... 18
9.2.2. Parámetros del Sistema ............................................................ 20
9.3. REPORTES ............................................................................................................... 21
9.3.1. Reporte de Usuarios Auditoría ............................................... 22
10. APIS ............................................................................................................................. 23
10.1. Api para replicar los adjuntos en el Blob storage....................................... 23
10.2. Consulta tu Reembolso ...................................................................................... 26
10.3. Sengrid - Notificaciones ..................................................................................... 31
10.4 Tipos de Notificaciones NTC ............................................................................. 36
10.4.1 NTC 19 - Completa tus datos bancarios. ..................................................... 37
10.4.2 NTC 23 - Pago exitoso en Voucher Valores Faltantes ...... 39
10.4.3 NTC 24 - Pago exitoso en ACM Valores Faltantes ............ 42
10.4.4 Notificación de reembolso pagado ........................................ 44
3
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
11. Tablas .......................................................................................................................... 48
11.1. Registro en Logs ........................................................................ 48
12. PROCESOS ................................................................................................................ 49
12.1. Purge Refund ........................................................................................................ 49
13. Procedimientos – SP ............................................................................................... 53
13.1. Querys reporte usuarios Auditoria ................................................................. 53
14. HISTORIAL DE PRUEBAS DE PERFOMANCE Y SEGURIDAD..................... 53
15. GLOSARIO DE TÉRMINOS .................................................................................... 54
2. INTRODUCCIÓN
Documentar las principales funcionalidades, flujos y actividades que intervienen
en AV Refund
4
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Documentos de referencia:
Todos los documentos relacionados con la solicitud y entregados a los usuarios
se mencionan a continuación:
Fecha
Actualización Nombre del documento Ubicación
14-07-2023 PT-ARQ-Arquitectura de
Solucion-REFUND
Teams >Soporte
Financiero>Refund>Arquitec
tura
1. PRESENTACIÓN DEL APLICATIVO
1.1. Identificación
La presente guía de la aplicación AVR (AV Refund) este sistema recibe
recurrentemente la información que se genera en Mozart de los casos de
reembolsos, para seguimiento y alimentación de otros sistemas internos de
Avianca.
1.2. Alcance
Este sistema es desarrollado en AVIANCA para la administración del proceso
de pagos de reembolsos una vez estos estén aprobados.
Teniendo en cuenta que es necesario tener la información de los casos de
reembolsos que se abren pero que por algún motivo no se continúan o cierran
correctamente por parte del cliente, el orquestador de reembolsos envia
mediante un servicio expuesto por la solución interna AV Refunds, un registro
que indique el id del caso, el estado “en validación por el cliente” y la
hora y fecha de creación.
Este registro se almacenará en la base de datos de la solución y permanecerá
allí hasta que el proceso de actualización lo elimine porque el cliente continuó,
o el proceso de purga lo use.
Y cuando el cliente cancele la solicitud de un reembolso, se acepte el reembolso
por parte del cliente, o se cierre el reembolso correctamente, el orquestador de
reembolsos mediante un servicio expuesto por AVRefunds enviará un mensaje
para que se elimine ese registro de esta solución y no sea purgado por el
proceso automático
El proceso automático de purgado de casos que se abrieron y no se cerraron,
enviará mediante un servicio que debe exponer el orquestador de reembolsos
un mensaje para que se actualice el estado de esos reembolsos y se cierren
porque el cliente no continuó. Este servicio estará expuesto en el APIM de
AVIANCA
5
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
2. Arquitectura
2.1. Especificación detallada de los componentes:
AV Refunds Front:
Front End de la solución para el manejo de la información que se recibe procesada
por el sistema de reembolsos, Será la capa de usuario final. Este componente
estará expuesto a internet.
Entre otros deberá tener los módulos de:
• Autenticación con AAD.
• Administración de parámetros y reglas de negocio requeridas para la carga
o generación de información (si aplica).
• Administración de tablas maestras que maneje esta solución.
• Seguimiento de las solicitudes de Reembolso
• Seguimiento de los procesos de carga de archivos
Deberá implementarse un proxy reverso para invocar los servicios de la capa de
backend de la solución teniendo en cuenta que esta no se publica en INTERNET.
AV Refund Backend Services:
Capa de backend de la solución Reembolsos AVIANCA. Esta API contiene
servicios con la lógica de negocio asociada a los procesos desencadenados desde
el front end de la solución, así como servicios que sean necesarios para abstraer
la capa de presentación.
AV Refund External Services:
6
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Capa de servicios externos de la solución Reembolsos AVIANCA. Esta API
contiene servicios con la lógica de negocio asociada a atender las peticiones
recibidas desde sistemas externos a través de la capa de middleware de Avianca.
Se desarrolla inicialmente:
• Un servicio que permite al orquestador de reembolsos enviar la información
de los casos de reembolsos que ha enviado a calcular, para que sean
almacenados y posteriormente si no se recibe un update de cambio de
estado ha solicitado, se envíe un cambio de estado a Mozart a través del
orquestador de reembolsos para que cierre el caso con la causa que el
cliente no continuó con el proceso.
• Un servicio que permita recibir una notificación de cambio de estado una
vez el cliente acepte continuar con el proceso (creación del reembolso) o
rechace el reembolso. Con esto el sistema podrá eliminar el registro que
tiene pendiente y de esta manera no será tenido en cuenta en el proceso de
actualización de casos no continuados (time out)
Purge Refund:
Se crea este proceso automático para tomar todos los casos de reembolso que se
tengan registrados en el sistema provenientes de los registros que el orquestador
de reembolso remite para control de Time Out, y que después de 30 minutos de
creados en la base de datos no se ha recibido una actualización correspondiente
a una acción del cliente de aceptar o rechazar el reembolso. Por cada caso
encontrado, se enviará una notificación de actualización hacia Mozart para que
cierre el caso con la causal que se defina para time out y una vez actualizado el
caso, se eliminará del registro en la solución AV Refund.
DB AV Refund:
Base de datos principal del sistema interno de almacenamiento de información de
reembolsos procesados. El diseño de la base de datos se orienta a un sistema de
consulta buscando un desempeño adecuado para generar información. Tiempo de
Retención 3 años
DB AV Refund Hist:
Base de datos histórica del sistema interno de almacenamiento de información de
reembolsos procesados. El diseño de la base de datos se orienta a un sistema de
consulta buscando un desempeño apropiado para generar información.
No es necesario que este esquema sea igual al anterior, y pueden ser
desnormalizadas u omitidas algunas de las tablas del original. Tiempo de
Retención 2 años
Load files:
7
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Se crea este proceso automático para la carga de archivos que alimenta esta
solución proveniente inicialmente de MOZART. Una vez el archivo sea cargado,
este se mueve al repositorio de archivos procesados.
Se ejecutará de manera recurrente para verificar que archivos nuevos están listos
para ser procesados
AV Refund Files:
Se tiene este repositorio para recibir los archivos provenientes de los sistemas
relacionados con el proceso de reembolsos y de los cuales requerimos tener la
información internamente.
AV Refund Files Processed:
Se tiene este repositorio para Almacenar una copia de los archivos una vez sean
cargados al sistema. Tiempo de Retención 3 años.
HistMaintenance:
Este proceso automático tiene la capacidad de hacer mantenimiento de data
Histórica de acuerdo con lo determinado en cada repositorio de datos de la solución
interna de Avianca para almacenamiento de la información de los reembolsos
procesados, y a lo calendarizado en dicha solución.
Debe ejecutarse periódicamente, dejar log de ejecución y poder recuperar el punto
en el que falló ante cualquier necesidad de relanzamiento del proceso.
De acuerdo con cada repositorio deberá:
• AV Refund Files Processed: Eliminar la data que supere el tiempo definido
para retención.
• DB AV Refund: Eliminar la data que supere el tiempo definido para la
retención y no haya sido eliminada.
• DB AV Refund Hist: Eliminar la data que supere el tiempo definido para la
retención y no haya sido eliminada.
• AV Refund Files y Processed: Eliminar los archivos que superen el tiempo
definido para almacenamiento de estos.
Key Vault AV Refund:
Este componente permitirá el almacenamiento de las llaves y secretos que sean
necesarios para la solución de reembolsos especiales.
Log AV Refund:
La solución tiene un log que permite hacer seguimiento de diferentes procesos de
la solución o sucesos de error, para ello se hará uso de un Aplication Insights de
Azure, y cada componente de la solución podrá dejar información en este
repositorio.
8
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Tiempo de retención 90 días.
DATAFACTORY:
Se desarrollan pipelines que permiten:
• Hacer el movimiento de la data de la base de datos operacional del sistema
a la base de datos histórica
• Mover información al repositorio de analítica de la compañía.
Refund Orquest Services:
Los servicios de orquestamiento de reembolsos tal cual se ha mencionado antes:
• Envian un registro de los casos de reembolsos calculados y presentados al
cliente, con la información estrictamente necesaria para posteriormente
poder hacerle seguimiento de estado para el proceso de cierre por time out
(id del caso, fecha hora de generación de la evaluación, estado (en
evaluación)).
• Una vez el caso sea aceptado o rechazado por el cliente, enviar un mensaje
de actualización a este sistema para que se elimine el registro y no sea
tenido en cuenta en el proceso de cierre por time out
Move Files Services:
Se crea un servicio de tipo worker en el ESB que hace el movimiento de
información de los archivos generados por MOZART desde el SFTP del mismo
hasta el repositorio de entrada de la solución interna de reembolsos de AVIANCA
SFTP MOZART:
Accelya dispone de un sitio SFTP donde expone los archivos con la información
de los reembolsos procesados por la solución MOZART, para que Avianca los tome
y los utilice para sus fines internos.
3. PUESTA EN AMBIENTE PRUEBAS O PRODUCCIÓN
Para el buen funcionamiento en el ambiente de producción se debe realizar
despliegue según solicitud en Yarvis de los pull request que desarrollo libere en el
ambiente de producción y ejecución de los scripts que correspondan.
3.1. Despliegue en ambiente de pruebas
Antes de iniciar el proceso de despliegue se debe realizar backup de los Pull
request que libere el equipo de desarrollo en el ambiente de QA
4. PROCESO DE ROLL BACK
El proceso de Roll Back se realiza con el equipo de desarrollo de acuerdo a los pull
request que se hayan desplegado en QA.
9
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
5. DESCRIPCIÓN DE LA FUNCIONALIDAD
Este sistema es desarrollado en AVIANCA el cual permite recibir recurrentemente
la información que se genera en Mozart de los casos de reembolsos, para
seguimiento y alimentación de otros sistemas internos de Avianca.
6. INGRESO AL SISTEMA
Para el ingreso a AV Refund ingresamos al siguiente link de QA:
https://azwappavrefsftuseqa.az-asev3-use-qa.appserviceenvironment.net/auth
Al dar clic en iniciar sesión se debe autenticar con Directorio Activo de Azure,
debe elegir o escribir su correo que están en Microsoft.
10
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
6.1. Inactivación de Usuario
Los usuarios que no hayan iniciado sesión en los últimos 90 días serán
inactivados automáticamente, para mantener la seguridad y limpieza de la
base de datos.
Con la functión de inactivación az-fapp-avrefpurge-use-qa
De acuerdo a los parámetros configurados para la inactivación de usuario.
select * from [master].[MST_PARAMETERS] where parameter_code in
('PRE_INACTIVATION_NOTIFICATION',
'SUBJECT_EMAIL_INACTIVATION_NOTIFICATION',
'TEMPLANE_NAME_INACTIVATION_NOTIFICATION',
'USER_INACTIVITY_DAYS')
11
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Se enviará una notificación a los usuarios próximos a inactivar cuando
hayan cumplido 80 días sin ingreso.
"SELECT [email], [FIRST_NAME] + ' ' + [LAST_NAME], [last_login_date] AS [NAME]
FROM [adm].[MST_USER]
WHERE DATEDIFF(DAY, [last_login_date], GETDATE()) = 80;"
La notificación seria la siguiente:
Cuando la function se ejecuta inactiva los usuarios que cumplen con el
tiempo establecido de no ingreso por 90 días
SELECT * FROM [adm].[MST_USER] order by last_login_date asc
Se observa en el log, los usuarios inactivados
12
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
SELECT * FROM [rfd].[AVR_LOGS_TRANSACTION]where created_user='AVR_DEACTIVITY_USER' order by
created_DATE asc
Nota: Lo anterior es de acuerdo al PBI
• 982297 Refund - Inactivación Automática de Usuarios Cada 90 Días. Parte II [Final]
7. Descripción del perfil de usuario
A continuación, se presenta un resumen con los principales accesos.
A continuación se relaciona los diferentes módulos de la aplicación y esta ha sido
actualizada en Angular de V17 a 20 de acuerdo al PBI 1233621 Soporte - Cambio
de version de Angular AVR
8. MÓDULOS
Para la administración y gestión de AV Refund – AVR, se manejan diversos menús
para cada proceso, los cuales se detallaran a continuación.
8.1. ADMINISTRACIÓN
8.1.1. Gestión de Menús
13
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Creación de Menus:
Editar menú
Activar o inactivar
14
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
8.1.2. Gestión de Roles
Através de esta funcionalidad se puede gestionar los Roles y permisos para los
usuarios que hagan uso de la APP. Teniendo disponible la opción de Consultar,
Modificar y Crear.
Consultar roles
Ingresar al menú Administración y seleccionar el sub menú Gestión de Roles
Se presenta la pantalla principal de la Maestra de Gestión de Roles
se debe seleccionar en filtros “todos” y escribir la palabra que se desea buscar.
Para buscar específicamente un campo en filtros, se selecciona el nombre del
filtro. Por ejemplo “nombre”: “tecnología”
Crear roles : Para crear rol selecciona la opción “crear nuevo rol”
Se presenta la pantalla para crear nuevos roles. llenar los campos requeridos y
dar clic en guardar. Al dar guardar se presenta el mensaje de confirmación
15
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Activar o inactivar rol
Editar roles: En el registro que se desea Modificar dar clic en el “lápiz”
Se abre la pantalla con los datos del registro disponibles para modificar.
Modificar el dato deseados y dar clic en el botón “Actualizar” Al dar actualizar se
presenta mensaje de confirmación si se desea mantener el estado del rol activo o
inactivo.
16
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Nota: Lo anterior se agrega de acuerdo con los PBIs:
635943 AVR- Gestión de roles y permisos (consultar y modificar)
635940 AVR - Gestión de roles y permisos (creación)
8.1.3. Gestión de Usuarios
Creación de usuarios
Editar
17
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Activar o desactivar
8.2. MAESTRAS
8.2.1. Impuestos
Se tiene una interfaz gráfica (GUI) para gestionar la tabla maestra de impuestos,
de forma que se puede crear, editar o inactivar códigos de impuestos que se
almacenan en la tabla [master].[MST_TAX_CODE].
Maestras >> Impuestos
18
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Se tiene un campo para consultar por el filtro de código o nombres de los
impuestos en los diferentes idiomas.
Crear Impuestos
Editar
19
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Activar o desactivar
Nota: Lo anterior se agrega de acuerdo al PBI:
• 1081327 AVR - Crear GUI para la Maestra de Impuestos (MST_TAX_CODE)
8.2.2. Parámetros del Sistema
En el menú de parámetros permite la consulta, creación, edición e inactivación de
registros en las tablas maestras correspondientes de AVR ingresando por
Maestras >> Parámetros del Sistema
Se tiene un campo para consultar por el filtro de código, descripción o valor de los
parámetros.
Crear
20
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Editar
Activar o desactivar
Toda la información se guarda en la base de datos en la tabla
[master].[MST_PARAMETERS]
Nota: Lo anterior se agrega de acuerdo con el PBI
• 1089252 Refund - Creación de Front para Sistemas AVR Similar al Existente en PI (Parámetros).
8.3. REPORTES
21
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
8.3.1. Reporte de Usuarios Auditoría
Este reporte genera la información de la maestra de usuarios en Excel y en csv
Excel
22
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
CSV
9. APIS
10.1. Api para replicar los adjuntos en el Blob storage
Se crea un API asíncrona que permite recibir un adjunto en base 64 que es
almacenado en un Blob Storage ; se recibe el dato del radicado del reembolso y
el documento adjunto en base 64.
Se tiene en cuenta las siguientes condiciones.
1. 2. 3. 4. Pueden recibirse varios documentos bajo la misma solicitud de reembolso
Se registra en el log con los siguientes datos:
Número de solicitud, nombre del archivo, fecha y hora
El tamaño del archivo debe ser máximo 1Mb
El formato recibido es jpg, png, pdf, msg, docx y/o xlsx:
El api es https://azwappavrefsextsuseqa.az-asev3-use-
qa.appserviceenvironment.net/SaveSupport
Se puede ingresar al swagger https://azwappavrefsextsuseqa.az-asev3-use-
qa.appserviceenvironment.net/Swagger/index.html
23
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Se ingresa los datos requeridos y se adjunta el archivo
Dar clic en Execute y se confirma el response
24
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Ingresamos al Blob Storage azstaccavrefuseqa >> soportes-excepciones
25
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Al ingresar a la carpeta observamos el archivo que se adjuntó
Al nombre del archivo cargado, le añadimos la fecha y hora en la cual fue cargado,
esto con el fin de evitar que, dentro de una misma carpeta al interior de un
contenedor, puedan existir 2 archivos con el mismo nombre, lo que generaría un
conflicto con las políticas de los blobs storage de Azure.
Nota: Lo anterior se agrega de acuerdo con el PBI:
• 723284 AVR - Crear API para replicar los adjuntos en el BS. Parte I
10.2. Consulta tu Reembolso
El sistema AV Refund expone un servicio que permite la consulta de solicitudes de
reembolso el cual es llamado por los canales Avianca.com y Avianca Trade a través
de capa media.
La capa media se encargará de orquestar en qué caso llamar el servicio teniendo
en cuenta la fecha a partir de la cual se migra la información disponible en AV
Refund y la fecha de la solicitud del reembolso.
El api permite consultar los reembolsos teniendo en cuenta los siguientes filtros de
búsqueda:
26
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
• Station. Corresponde al origen de la solicitud
• Control Number. Corresponde al consecutivo asignado a la solicitud de
reembolso.
• Document (Ticket o EMD). Corresponde al número del tique compuesto por
los 13 dígitos.
• Status. Corresponde al estado de la solicitud (autorizado ó rechazado)
El request del servicio está en capacidad de aceptar la siguiente combinación de
campos para la consulta:
• Station y Control number ó
• Station y Control number y Document ó
• Document
Restricciones en las consultas por número de tkt
Cuando en la petición del servicio de consulta tu reembolso RTS se reciba como
filtro el Documento, y el resultado de la consulta en base de datos retorne varias
solicitudes, se aplica las siguientes condiciones:
• Si el número de tique está radicado una sola vez, el servicio retorna los datos
del reembolso de este registro.
• Si el número de tique está radicado más de una vez y uno está autorizado,
el servicio debe retornar los datos del reembolso de la solicitud autorizada.
El registro se obtiene mediante el campo estado de la tabla _Det, si el valor
del campo es igual a “P”. En caso de que al menos uno este autorizado (P),
prevalecerá el último autorizado.
• Si el número de tkt está radicado más de una vez y todas las solicitudes
están rechazadas, el servicio debe retornar los datos del reembolso de la
última solicitud rechazada. (El registro se obtiene mediante el campo
Prod_Dat de la tabla _Pro debe organizar y obtener el más reciente que
corresponde a la última rechazada). En caso de que haya rechazado (R) y
no este los escenarios anteriores mostrarán el rechazado más reciente.
En AVrefund se crearon dos parámetros uno para el campo "Channel" y otro para
el campo “document-type"”
En “channel” se muestra el texto "RTS" como valor constante.
En "document-type" se muestra el texto "T" como valor constante.
"SELECT * FROM [master].[MST_PARAMETERS]
where parameter_code in ('DOCUMENT_TYPE_RTS','CHANNEL_RTS')"
27
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Las tablas consultadas en esta api son:
select * from [rfd].[AVR_DAT_REQUEST_ENC]
select * from [rfd].[AVR_DAT_REQUEST_DET]
select * from [rfd].[AVR_DAT_REQUEST_TAXES]
select * from[rfd].[AVR_DAT_PAYMENT_HISTORY]
select * from [rfd].[AVR_DAT_PROCESS_HISTORY]
select * from [rfd].[AVR_INFORMATION_ADDITIONAL_PASSENGER]
select * from [rfd].[AVR_INFORMATION_PASSENGER]
El api se encuentra en el swager:
https://azwappavrefsextsuseqa.az-asev3-use-qa.appserviceenvironment.net/Swagger/index.html
https://azwappavrefsextsuseQA.az-asev3-use-QA.appserviceenvironment.net/api/v1/GetRefundRTS
Ó el curl para pasarlo a postman es :
curl -X 'POST' \
'https://azwappavrefsextsuseqa.az-asev3-use-qa.appserviceenvironment.net/api/v1/GetRefundRTS' \
-H 'accept: text/plain' \
-H 'Content-Type: application/json' \
-d '{
"document": 0,
"station": "string",
"controlNumber": 0,
"status": "string"
}'
28
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
A continuación se relaciona los campos, definición y las tablas y campos a
consultar
29
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
AVRefund - Base de datos Destino
AVRefund - API
{ Tabla destino Campo Destino
"response-code"
"response-message"
"refund-request" Número de solicitud [rfd].[AVR_DAT_REQUEST_ENC] [STATION] [CTL_NUM]
"pnr" Número de la reserva [rfd].[AVR_INFORMATION_PASSENGER] [PNR]
"email-reservation" Email de la reserva [rfd].[AVR_DAT_REQUEST_ENC] [REF_EMA]
"channel" Canal de ingreso de la solicitud de reembolsos Por defecto el texto "RTS" N/A
"fist-name" Primer nombre del owner de la reserva/Nombre de empresa [rfd].[AVR_DAT_REQUEST_ENC] [AGE_NAM]
"middle-name" Segundo nombre del owner de la reserva [rfd].[AVR_DAT_REQUEST_ENC] [CLA_NAM]
"last-name" Primer apellido del owner de la reserva [rfd].[AVR_DAT_REQUEST_ENC] [CLA_MID]
"middle-last-name" Segundo apellido del owner de la reserva [rfd].[AVR_DAT_REQUEST_ENC] [CLA_LNA]
"lm-number" Número de lifemiles [rfd].[AVR_DAT_REQUEST_ENC] [LM_NUMBER]
"info-tickets" [{
"document" Número de tiquete (13 digitos) [rfd].[AVR_DAT_REQUEST_DET] [car_num_cod + doc_num]
"pax-first-name" Nombre Pasajero [rfd].[AVR_INFORMATION_ADDITIONAL_PASSENGER] [NAME_PAX]
"pax-last-name" Apellido Pasajero [rfd].[AVR_INFORMATION_ADDITIONAL_PASSENGER] [LAST_NAME_PAX]
"corporate-code" CC Codigo Corporativo [rfd].[AVR_INFORMATION_ADDITIONAL_PASSENGER] [TOUR_CODE]
"document-type" T como valor constante. T como valor constante.
"original-ticket" Sí el campo esta poblado se toma, de lo contrario se pobla con el tkt de la solicitud [rfd].[AVR_INFORMATION_ADDITIONAL_PASSENGER] [ORIGINAL_TICKET]
"fare-amount" Valor de la tarifa-venta [rfd].[AVR_DAT_REQUEST_DET] [FAR_AMT]
"fare-currency" Moneda de la tarifa- venta [rfd].[AVR_DAT_REQUEST_DET] [CUR_COD]
"sale-total" Valor total de la venta [rfd].[AVR_DAT_REQUEST_DET] [SALE_TOTAL]
"sale-currency" Moneda de la venta [rfd].[AVR_DAT_REQUEST_DET] [SALE_CURR_CODE]
"penalty-amount" Valor de la penalidad (Si no aplica penalidad colocar ) [rfd].[AVR_DAT_REQUEST_DET] [SER_CHA_AMT]
"commission-amount" Valor de la comisión venta [rfd].[AVR_DAT_REQUEST_DET] [AGT_COM_AMT]
"commission-currency" Moneda de la comisión venta [rfd].[AVR_DAT_REQUEST_DET] [CURR_COD_PROC]
"is-commission" si el campo "commission-amount" es igual a cero envía una "N", si no, envía una "Y". N/A N/A
"info-taxes" [{
"tax-code" Código del impuesto-venta [rfd].[AVR_DAT_REQUEST_TAXES] [TAX_COD]
"refcal-tax-amount" valor a reembolsar del tax [rfd].[AVR_DAT_REQUEST_TAXES] [TAX_AMT_ADJ]
"refcal-tax-currency" Moneda del reembolso del tax [rfd].[AVR_DAT_REQUEST_DET] [CUR_COD]
}],
"request-date" Fecha de solicitud del reembolsos desde los canales [rfd].[AVR_DAT_REQUEST_DET] [REQ_DAT]
"refcal-refund-reason" Razón del reembolso [rfd].[AVR_DAT_REQUEST_DET] [REF_REA]
"refcal-refund-reject" Razón del rechazo [AVR_DAT_PROCESS_HISTORY] [REF_REJ_REA]
"refcal-refund-amount" Monto total del reembolso de tiquete [rfd].[AVR_DAT_REQUEST_DET] [VAL_AUT]
"refund-currency" Moneda del reembolso [rfd].[AVR_DAT_REQUEST_DET] [CUR_COD]
"refund-status" Estado del reembolso [rfd].[AVR_DAT_REQUEST_DET] [REF_STA_DET]
"info-payment" [{
"fop" Forma de pago [rfd].[AVR_DAT_REQUEST_DET] [MET_PAY_FOP]
"payment-date" Fecha de pago [rfd].[AVR_DAT_PAYMENT_HISTORY] [DATE_REG]
"card-number" Tarjeta de crédito - 4 últimos dígitos [rfd].[AVR_DAT_REQUEST_DET] [CARD_NUMBER]
"exp-date" Fecha de expiración de la tarjeta [rfd].[AVR_DAT_REQUEST_DET] [CARD_EXP_DATE]
"approval-code" codigo de aprobación de la transacción [rfd].[AVR_DAT_REQUEST_DET] [CARD_APV_CODE]
"franchise" Franquicia tarjeta [rfd].[AVR_DAT_REQUEST_DET] [CARD_FRA_CODE]
"refund-amount" Valor reembolsado [rfd].[AVR_DAT_REQUEST_DET] [VAL_AUT]
"refund-currency" Moneda del reembolso [rfd].[AVR_DAT_REQUEST_DET] [VAL_AUT]
"voucher-number" Número del voucher de QC [rfd].[AVR_DAT_REQUEST_DET] [CUR_COD]
"bank-account" Ultimos 4 digitos de la cuenta bancaria a la que se transfirió [rfd].[AVR_DAT_REQUEST_DET] [VOU_NUMBER]
"bank-name" nombre del banco [rfd].[AVR_DAT_REQUEST_ENC] [BANK_ACCOUNT_NUM]
"account-type" tipo de cuenta [rfd].[AVR_DAT_REQUEST_ENC] [BANK_NAME]
}] [rfd].[AVR_DAT_REQUEST_ENC] [ACC_TYP]
}]
"summarize-payment" : [{
"tickets" Para los tiquetes con igual estado, forma de pago y fecha de pago, se concatenan todos los tiquetes separados por coma y se retornan en el elemento “tickets”
"reject-date" fecha de rechazo siempre que el estado de los tiquetes agrupados sean R”
"state" estado de los tiquetes [rfd].[AVR_DAT_REQUEST_DET] [REF_STA_DET]
"pay-date" fecha de pago, se envía únicamente si el estado de los tiquetes agrupados es pagado “P”. [rfd].[AVR_DAT_PAYMENT_HISTORY] [DATE_REG]
"fop-type" Forma de pago [rfd].[AVR_DAT_REQUEST_DET] [MET_PAY_FOP]
"credit-card-number" Tarjeta de crédito - 4 últimos dígitos [rfd].[AVR_DAT_REQUEST_DET] [CARD_NUMBER]
"currreny-code" Moneda de reembolso [rfd].[AVR_DAT_REQUEST_DET] [CUR_COD]
"authorized-value" sumar todos los montos de reembolso de los tiquetes con igual estado [rfd].[AVR_DAT_REQUEST_DET] VAL_AUT
"gross-fare" sumar todos los montos de tarifa bruta de los tiquetes [rfd].[AVR_DAT_REQUEST_DET] FAR_AMT
"penalty-amount" sumar todas las penalidades [rfd].[AVR_DAT_REQUEST_DET] SER_CHA_AMT
"taxes" sumar todos los impuestos de los tiquetes [AVR_DAT_REQUEST_TAXES] TAX_AMT_ADJ
"attached" documento de soporte de pago a base 64 BlobStorage >> azstacpiccustuseqa >> comprobantes-de-pago documento
"name-attached" nombre completo con extensión del soporte de pago
"refund-request" concatenación de los campos STATION y CTL_NUM separados por el guion [rfd].[AVR_DAT_REQUEST_ENC] [STATION] [CTL_NUM]
}
]
}
Para el campo de los adjuntos, se trae de acuerdo a lo encontrado en el
BlobStorage >> azstacpiccustuseqa >> comprobantes-de-pago
En este se busca si el nombre del comprobante de pago incluye la station y
ctl_number por ejemplo BOGWE-620472
30
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Nota: Lo anterior se agrega de acuerdo con los PBIs:
920860 AVR - Ajuste Tablas fuente para API Consulta tu Reembolso - Revisión de código
908380 AVR - Ajuste API Consulta tu Reembolso
10.3. Sengrid - Notificaciones
El Objetivo de este API es realizar el envió de una notificación a un correo
electrónico de acuerdo con los datos diligenciados en el request del API, el formato
o plantilla de la notificación enviada depende de la NTC diligenciada dentro del
request.
Se confirma las URLs en la tablea de parámetros el cual direcciona al formulario
de Datos bancarios.
SELECT * FROM [master].[MST_PARAMETERS] WHERE
PARAMETER_CODE LIKE ('%data_bank_form_url_%')
Y deben estar configuradas en las siguientes tablas
select * from [rfd].[AVR_TYPE_OF_NOTIFICATIONS]
select * from [rfd].[AVR_TEMPLATE_CONFIGURATION]
31
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
select * from [rfd].[AVR_SUBJECT_TABLE]
Se debe acceder al Swagger de AVR https://azwappavrefsextsuseqa.az-asev3-
use-qa.appserviceenvironment.net/Swagger/index.html
Ubicar el API SendgridEndpoints
Al presionar TRY OUT se observa un formato del request
Se usa el siguiente request el cual es para la NTC10, esta NTC se caracteriza por
tener detalle de pago y detalle de solicitud
Al momento de realizar este manual existe 17 NTC, las cuales pueden ser
observadas en los PBIS relacionados, las plantillas se pueden observar en el PBI
873415 AVR- Sendgrid- Configuración de plantillas HTML para Comunicaciones
(Refund) Parte 2
{
"notifaction-type": "NTC10",
32
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
"language": "ES",
"refund-request": "141944",
"refund-status": "G7",
"refund-reject-reason": "",
"pnr": "AOU2L8",
"owner-first-name": "Fernando",
"owner-middle-name": "",
"owner-last-name": "Ama",
"owner-middle-last-name": "",
"frequent-flyer-num": "04876641210",
"email-reservation": " d.ojeda@tcs.com ",
"info-tkt": [
{
"document": "2022483756366",
"document-type": "T",
"fare-amount": 0.0,
"fare-currency": "USD",
"refcal-fare-amount": 0.0,
"refcal-currency": "USD",
"penalty": 0.0,
"doc-refund-status": "C",
"info-taxes": [
{
"tax-code": "6A",
"tax-amount": 12.78,
"tax-currency": "USD",
"refcal-tax-amount": 12.78,
"refcal-tax-currency": "USD",
"refundable-tax-indicator": "Y"
},
{
"tax-code": "IF",
"tax-amount": 22.13,
"tax-currency": "USD",
"refcal-tax-amount": 22.13,
"refcal-tax-currency": "USD",
"refundable-tax-indicator": "Y"
},
{
"tax-code": "IG",
"tax-amount": 10.0,
"tax-currency": "USD",
"refcal-tax-amount": 10.0,
"refcal-tax-currency": "USD",
"refundable-tax-indicator": "Y"
},
{
"tax-code": "IM",
"tax-amount": 7.0,
"tax-currency": "USD",
"refcal-tax-amount": 7.0,
"refcal-tax-currency": "USD",
33
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
"refundable-tax-indicator": "Y"
},
{
"tax-code": "US",
"tax-amount": 22.9,
"tax-currency": "USD",
"refcal-tax-amount": 22.9,
"refcal-tax-currency": "USD",
"refundable-tax-indicator": "Y"
},
{
"tax-code": "XA",
"tax-amount": 3.71,
"tax-currency": "USD",
"refcal-tax-amount": 3.71,
"refcal-tax-currency": "USD",
"refundable-tax-indicator": "Y"
},
{
"tax-code": "XY",
"tax-amount": 7.0,
"tax-currency": "USD",
"refcal-tax-amount": 7.0,
"refcal-tax-currency": "USD",
"refundable-tax-indicator": "Y"
},
{
"tax-code": "YC",
"tax-amount": 7.2,
"tax-currency": "USD",
"refcal-tax-amount": 7.2,
"refcal-tax-currency": "USD",
"refundable-tax-indicator": "Y"
}
],
"payment-detail": {
"payment-date": "2025-05-30",
"fop": "KR",
"card-num": "1212121",
"bank-acount": "98978",
"voucher-num": "1500012140350665",
"voucher-issue-date": "2025-06-06",
"voucher-exp-date": "2026-06-10",
"voucher-cpg": "string",
"doc-ref-original": "7789564656",
"ip":null
}
}
],
"total-refund-amount": 92.72,
"total-refund-currency": "USD"
}
34
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Cuando se ejecuta se muestra la información de respuesta del API, es exitosa,
esta NTC10 requiere que se tenga un comprobante de pago, asi que como se
observa se recuepra codificado en binario
Se revisa el correo y se observa que la notificación NTC10 fue enviada
correctamente, teniendo en cuenta todos los valores enviados en el request
Se observa el comprobante de pago adjunto
35
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
10.4 Tipos de Notificaciones NTC
• NTC1 Reembolso Denegado
• NTC2 Redeposito Millas Rechazado
• NTC3 Redeposito Exitoso Millas
• NTC4 Pago Exitoso Tarjeta
• NTC5 Pago Exitoso Millas
• NTC6 Pago Exitoso Avianca Credits
• NTC7 Pago Avianca Credits Cambio Forma De Pago
• NTC8 Actualización De Tu Reembolso
• NTC9 Emisión Avianca Credits Pago No Exitoso Tarjeta De Crédito
• NTC10 Emisión Avianca Credits Pago No Exitoso
• NTC11 Confirmación Pago De Reembolso Avianca Credits
• NTC12 Confirmación Pago De Reembolso Transferencia Tarjeta De
Crédito
• NTC13 Confirmación Pago De Reembolso Transferencia Cuenta Bancaria
• NTC14 Confirmación Rechazo De Reembolso Varios Motivos
• NTC15 Confirmación Rechazo De Reembolso Único Motivo
• NTC16 Recibimos Tu Solicitud De Reembolso
• NTC17 Confirmación pago de reembolso transferencia con múltiples
tarjetas de crédito
• NTC19 Completa tus datos bancarios
• NTC20 Confirmación pago de reembolso ACM
• NTC21 Radicación de reembolso proactivo Equipaje - Ley DOT
• NTC22 Radicación de reembolso proactivo PNR - Ley DOT
• NTC23 Pago exitoso en Voucher Valores Faltantes
• NTC24 Pago exitoso en ACM Valores Faltantes
36
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
10.4.1 NTC 19 - Completa tus datos bancarios.
Esta notificación se dispara en los casos que llega un caso de cash, pero sin datos
bancarios, por ende, le llega notificación al usuario final para que actualice la
información.
Adicional para los que llegan a la pantalla de gestión de pago y la central de
reembolsos solicita enviar notificación.
Para utilizar el siguiente swagger la solicitud debe de existir en AVR
{
"notifaction-type":"NTC19",
"refund-request":"173192",
"pnr":"CFN9AC",
"owner-first-name":"Nikita",
"owner-last-name":"Ward",
"email-reservation":"PRUEBASSMTP10@GMAIL.COM",
"info-tkt":[
]
}
URL del parámetro data_bank_form_url_fr de la NTC19
37
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Se confirma la notificación en AVR y en el correo
38
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Nota: Lo anterior es de acuerdo con los siguientes PBIs:
• 1118621 AVR - Ajustar link NTC19
10.4.2 NTC 23 - Pago exitoso en Voucher Valores Faltantes
Esta notificación es cuando se realiza Pago en voucher de Valores Faltantes.
Cuando en las siguientes tablas el estado Final es Pagado “P” en FOP voucher
“KR” [rfd].[PIC_PAYMENT_REQUEST_VF] y [rfd].[PIC_PAYMENT_DETAIL_VF]
rfd.AVR_TYPE_OF_NOTIFICATIONS (Tabla de Tipo de notificación)
• NOTIF_TYPE_CODE: NTC23
• NOTIF_TYPE_NAME: Pago exitoso en Voucher Valores Faltantes
rfd.AVR_SUBJECT_TABLE (Tabla de asuntos de notificación)
• [Importante] Tu solicitud de reembolso fue pagado en un avianca credits.
• [Important] Your refund request has been paid in avianca credits.
• [Importante] Pagamento bem-sucedido Avianca Credits.
El request en el api es:
{
"notifaction-type": "NTC23",
"language": "PT", >> este idioma cambia de acuerdo a la solicitud
"refund-request": "191208",
"refund-status": "G7",
"refund-reject-reason": "",
"pnr": "AAL85H",
39
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
"owner-first-name": "Diego",
"owner-middle-name": "",
"owner-last-name": "test",
"owner-middle-last-name": "",
"frequent-flyer-num": "",
"email-reservation": "DIEGO.GARCIATORRES@AVIANCA.COM",
"subchannel": "",
"info-tkt": [
{
"document": "1342153984574",
"document-type": "T",
"fare-amount": 850000.00,
"fare-currency": "COP",
"refcal-fare-amount": 234000.00,
"refcal-currency": "COP",
"penalty": 0,
"doc-refund-status": "",
"doc-refund-reject-reason": "",
"info-taxes": [
{
"tax-code":"",
"tax-amount":0,
"tax-currency":"",
"refcal-tax-amount":0,
"refcal-tax-currency":"",
"refundable-tax-indicator":""
}
],
"payment-detail": {
"payment-date": "2026-07-01",
"fop": "KR",
"card-num": "",
"bank-acount": "",
"voucher-num": "1500014149489715",
"voucher-issue-date": "2026-07-01",
"voucher-exp-date": "",
"voucher-cpg": "AV Refund/DOT Law PF",
"acm-num": "",
"miles": "0",
"doc-ref-original": "",
"ip": ""
}
}
"total-refund-amount": 384000.00,
"total-refund-currency": "COP"
}
Template Español:
40
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Template Inglés:
Template Portugués:
Nota: Lo anterior se agrega de acuerdo al PBI
• 1302121 AVR- Sendgrid- Ajuste Configuración de plantilla HTML – Pago en KR_Valores Faltantes (NTC23)
41
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
10.4.3 NTC 24 - Pago exitoso en ACM Valores Faltantes
Esta notificación es cuando se realiza Pago en Nota Crédito - ACM de Valores
Faltantes.
Cuando en las siguientes tablas el estado Final es Pagado “P” en FOP voucher
“NC” [rfd].[PIC_PAYMENT_REQUEST_VF] y [rfd].[PIC_PAYMENT_DETAIL_VF]
rfd.AVR_TYPE_OF_NOTIFICATIONS (Tabla de Tipo de notificación)
• NOTIF_TYPE_CODE: NTC24
• NOTIF_TYPE_NAME: Pago exitoso en ACM Valores Faltantes
rfd.AVR_SUBJECT_TABLE (Tabla de asuntos de notificación)
• [Importante] Tu solicitud de reembolso fue pagado en una nota de crédito - ACM
• [Important] Your refund request was paid in a credit note - ACM.
• [Importante] Sua solicitação de reembolso foi paga em nota de crédito - ACM.
El request en el api es:
{
"notifaction-type": "NTC24",
"language": "PT", >> este idioma cambia de acuerdo a la solicitud
"refund-request": "191208",
"refund-status": "G7",
"refund-reject-reason": "195088",
"pnr": "AMDY4G",
"owner-first-name": "Jenny",
"owner-middle-name": "",
"owner-last-name": "Quintero",
"owner-middle-last-name": "",
"frequent-flyer-num": "",
"email-reservation": "PRUEBASE2EPROYECTODE@OUTLOOK.COM",
"subchannel": "",
"info-tkt": [
{
"document": "1342441242124",
"document-type": "T",
"fare-amount": 2097560.00,
"fare-currency": "COP",
"refcal-fare-amount": 88000.00,
"refcal-currency": "COP",
"penalty": 0,
"doc-refund-status": "C",
"doc-refund-reject-reason": "",
"info-taxes": [
{
"tax-code":"",
"tax-amount":0,
"tax-currency":"",
"refcal-tax-amount":0,
"refcal-tax-currency":"",
"refundable-tax-indicator":""
}
],
"payment-detail": {
42
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
"payment-date": "2026-04-01",
"fop": "NC",
"card-num": "",
"bank-acount": "",
"voucher-num": "",
"voucher-issue-date": "2026-04-01",
"voucher-exp-date": "",
"voucher-cpg": "",
"acm-num": "100001",
"miles": "0",
"doc-ref-original": "",
"ip": ""
}
}
],
"total-refund-amount": 88000.00,
"total-refund-currency": "COP"
}
Template Español:
Template Inglés:
Template Portugués:
43
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Nota: Lo anterior se agrega de acuerdo al PBI
• 1302540 AVR- Sendgrid- Ajuste Configuración de plantilla HTML – Pago en ACM_Valores Faltantes (NTC24)
10.4.4 Notificación de reembolso pagado
Los valores del reembolso son correctos según el request enviado
El detalle es correcto siguiendo los lineamientos solicitados en la documentación y basado en los
datos del request enviado.
44
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Para cambiar de idioma, se envia en el campo "language" el valor EN para ingles o PT para
protugues, usando el mismo request se puede observar como la notificación cambia de idioma
Ingles
Se visualiza correctamente
45
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Portugues
46
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
47
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
10. Tablas
10.1. Registro en Logs
Se observa que el LOG de la notificación enviada se guarda correctamente
SELECT TYP.NOTIF_TYPE_CODE, TYP.NOTIF_TYPE_NAME, CONF.LANG_CODE, NOTIF.*
FROM [rfd].[AVR_CONTROL_NOTIFICATIONS] NOTIF
JOIN [az-sqla-avref-use-qa].[rfd].[AVR_TEMPLATE_CONFIGURATION] CONF ON NOTIF.TEMPLATE_ID =
CONF.TEMPLATE_ID
JOIN [az-sqla-avref-use-qa].[rfd].[AVR_TYPE_OF_NOTIFICATIONS] TYP ON CONF.[NOTIF_TYPE_CODE] =
TYP.[NOTIF_TYPE_CODE]
--where CONF.NOTIF_TYPE_CODE = 'NTC17'
where NOTIF.REFUND_REQUEST in ('141944')
ORDER BY SEND_DATE DESC
Nota: Lo anterior es de acuerdo con los siguientes PBIs:
• 937075 AVR - SendGrid - Integración API / Plantillas de Notificaciones. Parte II [Final]
• 982298 AVR - Ajuste al API de Notificaciones
• 1016268 AVR - Ajuste al API de Notificaciones (2) – Tipo de documento
• 1003679 AVR- Sendgrid- Ajuste Configuración de plantilla HTML – Confirmación pago de reembolso
transferencia tarjeta de crédito
• 1033960 AVR – AJUSTE - API envío de notificaciones -SendGrid (Nuevo campo – Notificación NTC15 texto
razón de rechazo)
• 1037675 AVR - API envío de notificaciones -SendGrid – Cálculo de reembolso notificaciones Lifemiles
• 1038836 AVR - API envío de notificaciones - Ajuste Mandatoriedad campo "owner-last-name"
• 1042793 AVR - API envío de notificaciones -SendGrid – Nuevos campos
• 1059574 AVR - API envío de notificaciones -SendGrid – AJUSTE Cálculo de reembolso notificaciones Lifemiles
(servicios adicionales – montos en millas)
48
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
• 1044587 AVR - Sengrid - Ajuste asuntos Notificaciones
• 1097892 AVR - API envío de notificaciones -SendGrid - Nuevo Campo (Request)
11. PROCESOS
12.1. Purge Refund
Proceso Automático para controlar el tiempo máximo de 30 minutos que puede
esperar el sistema para que un cliente logre completar y aceptar una solicitud de
reembolso desde un canal, por ejemplo, Avianca Trade; antes de que sea
considerado como desistido y ejecutarse la purga de la solicitud por tiempo de
espera superado.
la Function az-fapp-avrefpurge-use-qa, se encarga de tomar los registros con
estado "UNDER VALIDATION" y de ellos filtrará aquellos donde el Register Date
comparado con la fecha actual, tenga una diferencia mayor a 30 minutos, tiempo
que es configurado en la tabla MST_PARAMETERS.
select * from [master].[MST_PARAMETERS] where parameter_code ='purge_time'
select * from [master].[MST_PARAMETERS] where parameter_code='purge_scope_days'
Se inicia el proceso de solicitud de reembolso desde SR AV
Se pasa a 2da pantalla
49
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Pasamos a pantalla 3 de la cotización y no continúo, se desiste de la solicitud
cambiando de menú en SR.
Se confirma la inserción de la información en AV Refund
select * from [rfd].[AVR_INFORMATION_PASSENGER] r where REFUND_REQUEST = '172435'
select * from [rfd].[AVR_INFORMATION_ADDITIONAL_PASSENGER] i where REFUND_REQUEST = '172435'
50
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Se observa que la purga lo toma para la ejecución de los 30 min
SELECT DATEADD(MINUTE, -30, CAST(SYSDATETIMEOFFSET() AT TIME ZONE 'UTC' AT TIME ZONE 'SA Pacific
Standard Time' AS datetime)) AS FechaLimite30Minutos, i.CREATED_DATE,
* FROM [rfd].[AVR_INFORMATION_PASSENGER] r
JOIN [rfd].[AVR_INFORMATION_ADDITIONAL_PASSENGER] i ON r.REFUND_REQUEST = i.REFUND_REQUEST
WHERE i.Status = 'U'
AND r.CREATED_DATE >= DATEADD(DAY, -3, CAST(SYSDATETIMEOFFSET() AT TIME ZONE 'UTC' AT TIME ZONE
'SA Pacific Standard Time' AS datetime))
AND i.CREATED_DATE <= DATEADD(MINUTE, -30, CAST(SYSDATETIMEOFFSET() AT TIME ZONE 'UTC' AT TIME
ZONE 'SA Pacific Standard Time' AS datetime))
AND i.REFUND_REQUEST = '172435'
Se confirma que a los 30min pasó la purge cambiando el status de U a F
Se valida en Mozart cambio de estado
51
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Nota: Lo anterior es de acuerdo a los PBIs:
• 649565 AVR - Purge Refund - Proceso Automático para cierre de reembolsos abiertos sin aceptación Parte 2
• 1116709 AVR - Agregar la setting: access_token_mozart
52
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
12. Procedimientos – SP
13.1. Querys reporte usuarios Auditoria
Se crea SP para generar un reporte con los datos de la maestra de usuarios.
Ejecutar el SP EXEC [rfd].[AVR_SP_USER_DATA_QUERY].
La consulta retorna para cada usuario, los siguientes campos:
Nombre de usuario (username),
Nombre del responsable de la cuenta,
Número de identificación,
Estado del usuario (activo, bloqueado, inactivo u otro)
Roles o privilegios asignados,
Fecha de creación del usuario,
Fecha de última modificación,
Fecha de último acceso,
Tipo de usuario (directo o tercero)
Al final del informe, se incluye los siguientes metadatos:
a. Query Usada
b. Número de registros generados
c. Fecha y hora de generación del informe"
Nota: Lo anterior se agrega de acuerdo con el PBI
• 1151866 Refund - Queries de Usuarios
13. HISTORIAL DE PRUEBAS DE PERFOMANCE Y SEGURIDAD
N/A
14. GLOSARIO DE TÉRMINOS
53
Manual de Aplicación AVR
Versión 1.0
_________________________________________________________
______
Término Descripción / Definición
Reembolso Devolución de una cantidad de dinero a la persona que
la había desembolsado por la compra de un TKT.
54