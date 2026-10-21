MANUAL DE APLICACIÓN
SR
(Special Refund)
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Historial de Cambios y Revisiones del Documento
Versión
Documento Fecha Modificado
por Secciones, páginas y texto afectado
1.0 13-10-2023 Jenny
Garzón Se crea el Manual Funcional Special Refund).
1.1 5-09-2024 Isabel
Guerra
1- Se agrega funcionalidad de Gestion de Roles y permisos
2- Se agrega funcionalidad de Gestión de menú
3- Se agrega funcionalidad API EMD - SR - Ajuste al servicio
para recibir EMDs de aeropuertos (Lista de Objetos)
4- Se agrega funcionalidad - Pantalla para radicación de
solicitudes masivas desde la aplicación web
1.2 27-11-2024 Isabel
Guerra
1- Se agrega funcionalidad de Radicaciones masivas - Ajuste
Radicación de solicitudes masivas desde la aplicación web
(Back End) - Modificación de campos Parte 3
2- Se agrega funcionalidad de Radicaciones masivas - Ajuste
Function Load File para procesamiento masivo de
solicitudes - Modificación al PASO 1 - VERIFICACIÓN Y
CARGUE DE REGISTROS Parte 3
3- Se agrega funcionalidad de Radicaciones masivas - SR -
Cargue masivo para radicación de solicitudes - Paso 4
Mantenimiento de datos históricos Parte 3 Final
1.3 06-06-2025 Jenny
Garzón
Se agrega Inactivación de Usuario, en la sección de Ingreso al
Sistema
1.4 31-07-2025 Dumar
Ojeda
Se agrega proceso de carga masiva, desde cargue hasta
reporte
1.5 31-10-2025 Jenny
Garzón
Se actualiza imágenes y se complementa información del
proceso tanto solicitud individual como cargue masivo
1.6 10-11-2025 Jenny
Garzón
Se agrega el request de send refund info cuando tiene
excepción y un adjunto de certificación bancaria en pantalla 4
1.7 21-11-2025 Jenny
Garzón
1.8 17-12-2025 Jenny
Garzón
1. Se adiiciona nuevo estado F -Fallido al tener solicitudes con
estado E-Error en Solicitudes masivas de Reembolso.
2. Se agrega Reintentos de envío de las solicitudes masivas
Se actualiza la opción de Creación de reporte para carga
masiva y Query Reporte usuarios Auditoria
1.9 21-05-2026 Jenny
Garzón Se actualiza Cuarta Pantalla: Datos Bancarios
2.0 03-07-2026 Rafael
Avila
Se actualiza Solicitudes masivas de Reembolso.
1. Se agregan nuevos campos y validaciones en la plantilla de
“Solicitudes Masivas de Reembolso.”
2. Se actualiza la Function Load File con validación de tiquetes
duplicados y reprocesamiento de registros en estado E
2.1 27-07-2026 Jenny
Garzón
Se agrega Formulario Captura Reembolsos Faltantes,
radicación y aprobación
2
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
2.2 31/07/2026 Cindy
Arenas Se agrega modulo de maestras y nueva razon faltante
2.3 05/08/2026 Cindy
Arenas
Se agrega nuevo formulario de captura de reembolsos
individuales
2.4 09-09-2026 Jenny
Garzón
Se actualiza radicación, aprobación y se agrega rechazo del
Formulario Captura Reembolsos Faltantes
Aceptación del Manual de Aplicación
Elaborado por: Revisado por: Aprobado por:
3
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Contents
Contents ................................................................................................................... 4
1. INTRODUCCIÓN.............................................................................. 6
1.1. 1.2. 2. Propósito del documento ............................................................ 6
Documentos de referencia: ......................................................... 6
PRESENTACIÓN DEL APLICATIVO .......................................... 7
2.1. Identificación ................................................................................... 7
2.3. Arquitectura ..................................................................................... 8
2.4. 3. Especificación detallada de los componentes: ..................... 8
PUESTA EN AMBIENTE PRUEBAS O PRODUCCIÓN ........ 10
3.1. 4. 5. Despliegue en ambiente de pruebas ...................................... 11
PROCESO DE ROLL BACK ....................................................... 11
DESCRIPCIÓN DE LA FUNCIONALIDAD ............................... 11
6. INGRESO AL SISTEMA ............................................................... 11
6.1. Inactivación de Usuario .............................................................. 12
7. MÓDULOS ...................................................................................... 14
7.1. ADMINISTRACIÓN........................................................................ 14
7.1.1. Gestión de Menús ........................................................................ 14
7.1.2. Gestión de Roles .......................................................................... 17
7.1.3. Gestión de Usuarios .................................................................... 21
7.2. PROCESOS .................................................................................... 21
7.2.1. Formulario de Solicitud Central ............................................... 21
7.2.1.1. Primera Pantalla: Formas de iniciar una solicitud .............. 22
7.2.1.2. 7.2.1.3. Segunda Pantalla: Ajuste de pasajeros ................................. 23
Tercera Pantalla: Solicitud de Reembolso ............................ 26
7.2.1.3.1. Rechazo de solicitud ................................................................... 31
7.2.1.3.2. 7.2.1.4. Proceso cuando se eligen excepciones ................................ 35
Cuarta Pantalla: Datos Bancarios ........................................... 37
7.2.1.5. Quinta Pantalla: Confirmación ................................................. 41
4
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
7.2.1.5.1. 7.2.1.5.2. 7.2.2. 7.2.3. 7.2.3.1. 7.2.3.2. 7.2.3.3. solicitudes 60
Verificar Registro de solicitud en Base de datos ................ 42
Registro en Mozart ....................................................................... 42
Formulario Captura de reembolsos Individuales ................ 43
Solicitudes masivas de Reembolso ........................................ 46
Estados de las solicitudes cargadas masivamente: .......... 58
Reintentos de envío de las solicitudes masivas: ................ 59
Function Load File para procesamiento masivo de
7.2.3.4. 7.2.4. 7.2.4.1. 7.2.4.2. 7.2.4.2.1. 7.2.4.2.2. 7.2.4.3. 7.2.4.4. 7.3.1. Mantenimiento de datos históricos de Cargue masivo ..... 64
Formulario Captura Reembolsos Faltantes .......................... 69
Creación solicitud VF .................................................................. 70
Aprobación o Rechazo Del Coordinador o Gerente: .......... 73
Aprobar solicitud de Valores Faltantes ................................. 76
Rechazo de solicitud de Valores Faltantes ........................... 79
Respuesta de PI a SR .................................................................. 82
Estados de valores faltantes: ................................................... 82
7.3. MAESTRAS .................................................................................... 83
Gestión de Razones Faltante .................................................... 83
7.4. REPORTES ..................................................................................... 90
7.4.1. 8. Reporte de carga Masiva ........................................................... 90
Query Reporte usuarios Auditoria .......................................... 93
9. APIS ................................................................................................. 93
9.1. API Emd .......................................................................................... 93
10. HISTORIAL DE PRUEBAS DE PERFOMANCE Y
SEGURIDAD .......................................................................................................... 96
11. GLOSARIO DE TÉRMINOS ........................................................ 96
5
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
1. INTRODUCCIÓN
1.1. Propósito del documento
Documentar las principales funcionalidades, flujos y actividades que intervienen
en Special Refund.
1.2. Documentos de referencia:
Todos los documentos relacionados con la solicitud y entregados a los usuarios
se mencionan a continuación:
PT-ARQ-Arquitectura de
Solucion-REFUND
Fecha
Actualización Nombre del documento Ubicación
14-07-2023 Teams >Soporte
Financiero>Refund>Arquitec
tura
2. PRESENTACIÓN DEL APLICATIVO
2.1. Identificación
La presente guía de la aplicación SR (Special Refund) este sistema es nueva
solución interna de Avianca para ingreso de casos especiales de reembolsos
como clientes VIP o procesamiento de lotes de reembolsos mediante
archivos.
2.2. Alcance
Este sistema es desarrollado en AVIANCA con el ánimo de tener un canal
que permita el ingreso de casos especiales de reembolsos como los que se
definen como VIP.
Se desarrolla las pantallas necesarias para permitir la solicitud y seguimiento
de los casos de reembolsos, así como los procesos automáticos necesarios
para la creación de reembolsos a partir de archivos.
No deberá desarrollarse en este canal ninguna lógica de negocio propia de
reembolsos.
Consulta mediante el APIM de Avianca los servicios necesarios para traer la
información que deba presentársele al cliente en pantalla, asociados a
6
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
reembolsos. Así mismo hace el consumo a través del mismo componente de
los servicios de solicitud de cálculo de reembolso y creación del caso.
2.3. Arquitectura
2.4. Especificación detallada de los componentes:
SpecialRefund Front:
Front End de la solución para el canal de reembolsos especiales, es la capa
de usuario final. Este componente está expuesto a internet.
Entre otros tiene los módulos de:
• Autenticación con AAD.
• Administración de parámetros y reglas de negocio requeridas para el
ingreso de casos de reembolsos especiales (si aplica).
• Administración de tablas maestras que maneje esta solución y que no
corresponda a las que se devuelven desde los servicios de
reembolsos
• Calculo y Solicitud de reembolsos
• Seguimiento de las solicitudes de Reembolso
• Seguimiento de los procesos de solicitud de carga de archivos para
reembolsos masivos.
7
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se implementa un proxy reverso para invocar los servicios de la capa de
backend de la solución teniendo en cuenta que esta no se publica en
INTERNET.
Special Refund Backend Services:
Capa de backend de la solución de reembolsos especiales. Esta API contiene
servicios con la lógica de negocio asociada a los procesos desencadenados
desde el front end de la solución, así como servicios que sean necesarios
para abstraer la capa de presentación.
Los procedimientos aquí desarrollados se comunican con los servicios de
orquestación del proceso de reembolso a través de APIM de Avianca
Process Refund:
Se crea este proceso automático para tomar los casos especiales de
reembolsos solicitados con archivos y solicitarlos según el proceso estándar
definido para todos los canales. Este proceso invocará los servicios a través
del APIM de AVIANCA.
DB Special Refund:
Base de datos principal del sistema de creación de casos especiales de
reembolsos. El diseño de la base de datos está orientado a un sistema
transaccional de alto desempeño.
Load files:
Se crea este proceso automático para la carga de archivos de solicitudes
especiales de reembolsos.
Una vez el archivo es cargado, este se mueve al repositorio de archivos
procesados.
Se ejecuta de manera recurrente para verificar que archivos nuevos están
listos para ser procesados.
Generate files:
Se crea este proceso automático para la generación de archivos de respuesta
a solicitudes especiales de reembolsos.
Special Refund Files:
Se tiene este repositorio para:
• El usuario de la central de reembolsos dejará en este repositorio los
archivos de solicitudes especiales de reembolsos que provengan de
procesos manuales.
8
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• Recibir los archivos provenientes de sistemas que generen archivos
de reembolsos para procesamiento en batch.
• Dejar la respuesta para los sistemas que hagan solicitudes de
reembolsos mediante archivos.
Los archivos serán accedidos por medio del storage explorer de acuerdo con
los permisos otorgados al usuario de la central de reembolsos
Special Refund Files Processed:
Se deberá tener este repositorio para: Almacenar una copia de los archivos
una vez sean cargados al sistema.
Tiempo de Retención 1 año
HistMaintenance:
Este proceso automático tiene la capacidad de hacer mantenimiento de data
Histórica de acuerdo con lo determinado en cada repositorio de datos de la
solución de pagos especiales de reembolsos, y a lo calendarizado en dicha
solución.
Debe ejecutarse periódicamente, dejar log de ejecución y poder recuperar el
punto en el que falló ante cualquier necesidad de relanzamiento del proceso.
De acuerdo con cada repositorio deberá:
• Special Refund Files Processed: Eliminar la data que supere el año.
• DB Special Refund: Eliminar la data que supere el año.
• Payment Integ Files y Processed: Eliminar los archivos que superen el
tiempo definido para almacenamiento de estos.
Key Vault Special Refund:
Este componente permitirá el almacenamiento de las llaves y secretos que
sean necesarios para la solución de reembolsos especiales
Log Special Refund:
La solución tiene un log que permite hacer seguimiento de diferentes
procesos de la solución o sucesos de error, para ello se hará uso de un
Aplication Insights de Azure, y cada componente de la solución podrá dejar
información en este repositorio.
Tiempo de retención 90 días.
9
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
3. PUESTA EN AMBIENTE PRUEBAS O PRODUCCIÓN
Para el buen funcionamiento en el ambiente de producción se debe realizar
despliegue según solicitud en Mauro de los artefactos que desarrollo libere
en el ambiente de producción y ejecución de los scripts que correspondan.
3.1. Despliegue en ambiente de pruebas
Antes de iniciar el proceso de despliegue se debe realizar backup de los
artefactos que vamos a reemplazar y se dejan en …….
4. PROCESO DE ROLL BACK
El proceso de Roll Back corresponde al entregado por el equipo de desarrollo
quien entrega los script correspondientes a de acuerdo a la solicitud,
adicional se reemplazan los archivos que se hayan modificado.
5. DESCRIPCIÓN DE LA FUNCIONALIDAD
Este sistema es desarrollado en AVIANCA el cual permite recibir
recurrentemente la información que se genera en Mozart de los casos de
reembolsos, para seguimiento y alimentación de otros sistemas internos de
Avianca.
6. INGRESO AL SISTEMA
Para el ingreso a Special Refund ingresamos al siguiente link de QA:
https://specialrefundqa.avtest.ink/
10
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al dar clic en iniciar sesión se debe autenticar con Directorio Activo de Azure,
debe elegir o escribir su correo que están en Microsoft.
6.1. Inactivación de Usuario
Los usuarios que no hayan iniciado sesión en los últimos 90 días serán
inactivados automáticamente, para mantener la seguridad y limpieza de la
base de datos.
Con la function de inactivación az-fapp-sprefprocess-use-qa
De acuerdo con los parámetros configurados para la inactivación de
usuario.
select * from [master].[MST_PARAMETERS] where parameter_code in
('PRE_INACTIVATION_NOTIFICATION',
'SUBJECT_EMAIL_INACTIVATION_NOTIFICATION',
11
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
'TEMPLANE_NAME_INACTIVATION_NOTIFICATION',
'USER_INACTIVITY_DAYS')
Se enviará una notificación a los usuarios próximos a inactivar cuando
hayan cumplido 80 días sin ingreso.
SELECT [email], [FIRST_NAME] + ' ' + [LAST_NAME], [last_login_date] AS [NAME]
FROM [adm].[MST_USER]
WHERE DATEDIFF(DAY, [last_login_date], GETDATE()) = 80;
La notificación seria la siguiente:
Cuando la function se ejecuta inactiva los usuarios que cumplen con el
tiempo establecido de no ingreso por 90 días
SELECT * FROM [adm].[MST_USER] order by last_login_date asc
12
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se observa en el log, los usuarios inactivados
SELECT * FROM [rfd].[SP_REF_LOGS_TRANSACTION]where
created_user='SP_DEACTIVITY_USER' order by created_DATE asc
Nota: Lo anterior es de acuerdo con el PBI 982297 Refund - Inactivación Automática de Usuarios Cada 90 Días.
Parte II [Final]
7. MÓDULOS
Para la administración y gestión de Special Refund se manejan diversos menús
para cada proceso, los cuales se detallaran a continuación.
7.1. ADMINISTRACIÓN
7.1.1. Gestión de Menús
Ingresar al menú Administración y en el Sub-Menú seleccionar la opción Gestión
de Menús
13
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se debe seleccionar en filtros “todos” y escribir la palabra que se desea busca.
Para buscar específicamente un campo en filtros, se selecciona el nombre del filtro
especifico. por ejemplo “nombre”: “Maestras”
Crear Menú: Para crear menú selecciona la opción “crear nuevo menú”
Se presenta la pantalla para crear nuevos roles. llenar los campos requeridos y
dar clic en guardar
14
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al dar guardar se presenta el mensaje de confirmación
Modificar Menú: Dar clic en la opción de “Lápiz”
Se abre un Pop-Up con los datos del registro disponibles para editar.
Se actualiza la información correspondiente, al finalizar se debe dar clic en el
botón “actualizar”.
15
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al dar actualizar se presenta mensaje de confirmación si se desea mantener el
estado del rol activo o inactivo
Al dar aceptar en la confirmación del estado se presenta mensaje de confirmación
de actualización del registro
Nota: lo anterior se agrega de acuerdo con el PBI
• 638913- SR - Opciones de menú (Modificación)
• 638912- SR - Opciones de menú (Creación)
7.1.2. Gestión de Roles
Ingresar al menú Administración y en el Sub-Menú seleccionar la opción Gestión
de Roles
16
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se debe seleccionar en filtros “todos” y escribir la palabra que se desea buscar. si
se desea buscar específicamente un campo en filtros.
Por ejemplo se selecciona Nombre en filtro y en el campo de buscar se escribe
“Admin”
Crear Rol: Para crear rol selecciona la opción “crear nuevo rol”
17
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se presenta la pantalla para crear nuevos roles. Llenar los campos requeridos y
dar clic en guardar
Al dar guardar se presenta el mensaje de confirmación
Modificar Rol: En el registro dar clic en el “lápiz”
Se actualiza la información correspondiente, al finalizar se debe dar clic en el
botón “actualizar”.
18
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al dar actualizar se presenta mensaje de confirmación si se desea mantener el
estado del rol activo o inactivo.
Dar clic en Aceptar y se presenta mensaje de confirmación de actualización del
registro
Nota: lo anterior se agrega de acuerdo con el PBI
• 638756 SR - Gestión de roles y permisos (Consultar y Modificar)
• 638489-SR - Gestión de roles y permisos (Creación)
7.1.3. Gestión de Usuarios
7.2. PROCESOS
7.2.1. Formulario de Solicitud Central
El objetivo de este módulo es permitir solicitar el reembolso de una reserva.
Ingresar al menú Procesos y en el Sub-Menú seleccionar la opción Formulario de
Solicitud.
19
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al ingresar al submenú en la parte superior observamos las diferentes pantallas o
momentos en la que nos encontramos. En este primer momento estamos en la
pantalla No 1 “Formas de Iniciar una Solicitud”.
Y en la parte inferior podemos seleccionar la opción en la que podemos crear la
solicitud; ya sea por Código de reserva, Número de tiquete ó Número de servicio
adicional (EMD).
A continuación crearemos la solicitud y se explicará por pantallas
7.2.1.1. Primera Pantalla: Formas de iniciar una solicitud
En esta pantalla se puede realizar el diligenciado para iniciar el proceso de
reembolso, existen las opciones de Consultar por Reserva, Consulta por ticket y
consulta por EMD
20
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se diligencian todos los datos correspondientes
Al diligenciar todos los campos y dar clic en continuar este inicia el proceso de
consumo a un API llamado GetInfoticket para consultar los datos básicos del
reembolso.
Nota: lo anterior se agrega de acuerdo con los PBIs:
• 878776 SR - Integrar API Get Info Tkt. Parte 2
• 977701 SR - Ajuste a los Labels de Búsqueda de Special Refund
7.2.1.2. Segunda Pantalla: Ajuste de pasajeros
En esta pantalla se puede seleccionar la fecha de la solicitud, no puede ser mayor
al día actual que se realiza la solicitud, se muestra los tickets o EMDs relacionados
21
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
reembolso.
a la reserva, se puede seleccionar cual ticket o EMDs quiere ser solicitado para
La sección mostrada anteriormente puede cambiar si el canal seleccionado en
pantalla 1 es Special Refund LM ya que solicita un numero de viajero frecuente
Ejemplo:
Para reservas que no son personas naturales, viene con código corporativo, para
este caso, en esta sección también se muestra en un nuevo campo con el código
corporativo recuperado para la reserva.
22
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Continuando podemos observar la información del titular de la reserva.
Adiciona si se requiere se puede cambiar el titular.
Al presionar en continuar se realiza el consumo del API GetRefundInfo para
recuperar todos los datos del pago que fue efectuado en esta reserva
23
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con los PBIs:
• 687305 SR - Verificación de la estructura de Email del Titular
• 897306 SR - Integrar API Send Refund Info - Pantalla 2 - Número de viajero frecuente
• 943246 SR - Radicación Solicitudes Individual - Pantalla 2 - Integrar API Get Master Info Parte 4 [Final)
• 947918 SR - Ajuste Pantalla 2 Código Corporativo. Parte II [Final]
24
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
7.2.1.3. Tercera Pantalla: Solicitud de Reembolso
En esta pantalla se puede observar lo relacionado con toda la información de pago
que tuvo la reserva en el momento de ser generada y también se formalizan los
datos que de pago para el reembolso.
Observamos el número de caso generado para la solicitud, el “Detalle por pasajero”
todo los tickets o EMD recuperados en el API GetRefundInfo junto con su estado
actual y la razón, todo esto es recuperado del respectivo API
En caso de que el tickete tenga un estado que lo haría no reembolsable, se puede
observar su estado en esta sección, por ejemplo:
25
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
En la sección “Detalle de Reembolso” se puede observar los valores relacionados
con el reembolso, toda esta información es retornada por el API GetRefundInfo.
Si queremos el detalle de los valores, damos clic en la flecha al final de cada valor
para desglosar la información
26
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
En la sección de Resumen de reembolso se observa el resumen de los valores, el
cargo “pro-servicio” se resta, para este caso no cuenta con cargos
En la siguiente sección de la pantalla se puede elegir si el reembolso es debido a
una excepción, en dado caso que así sea se debe seleccionar una de acuerdo con
el listado que se despliega.
27
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Si la Excepción elegida requiere un adjunto, estos archivos deben ser adjuntados y
no deben tener el mismo nombre
En esta sección “¿Titular de la reserva es mayor de edad?”, en dado caso de marcar
“NO” se tomará como una excepción. Y se debe adjuntar un documento solicitado.
Cuando se selecciona una excepción como fue mostrado en estos dos pasos
anteriores, NO se despliegan las formas de pago ya que por defecto se tomará el
pago del reembolso como una transferencia bancaria.
Para objeto de este manual NO se enviará ninguna excepción.
28
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Ahora podemos ver que se despliegan las formas de pago, y por defecto se
selecciona la forma de pago que registra en la compra del reembolso, esto es
recuperado en el API GetRefundInfo.
En la imagen anterior se puede observar que el pago por defecto seleccionado es
Tarjeta de Crédito, si se continua el proceso y no hay inconvenientes se llegara a
Quinta pantalla: Confirmación, ya que la única forma de moverse a Cuarta Pantalla:
Datos Bancarios es al elegir forma de pago del reembolso “Transferencia Bancaria”,
para efectos del manual se realizara el proceso eligiendo “Transferencia Bancaria”
y poder observar la pantalla de Datos Bancarios
29
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con los PBIs:
• 914504 SR - Radicación Solicitudes Individual - Pantalla 3 - Integrar llamado a API Get Refund Info (Req 15 al Req 16)
Soporte para finalizar
• 906968 SR - Radicación Solicitudes Individual - Pantalla 3 - Integrar llamado a API Get Refund Info (Req 12) Parte 3
• 898668 SR - Radicación Solicitudes Individual - Pantalla 3 - Integrar llamado a API Get Refund Info (Req 1 al Req 4)
Parte 2
• 914501 SR - Radicación Solicitudes Individual - Pantalla 3 - Integrar llamado a API Get Refund Info (Req 5) Parte 3
Soporte para finalizar pruebas
• 914510 SR - Radicación Solicitudes Individual - Pantalla 3 - Integrar llamado a API Get Refund Info (Req 13 al Req 14)
Parte 4 PBI Soporte para finalizar
• 947904 SR - Radicación Solicitudes Individual - Pantalla 3 - Integrar llamado a API Get Refund Info (Req 17 al Req 18)
Parte 4 [Final]
• 898807 SR - Integrar API Send Refund Info - Pantalla 3 - Caso: forma de pago diferente a Transferencia Bancaria “CR”
Parte 2
• 947620 SR - Radicación Solicitudes Individual - Pantalla 3 - Integrar llamado a API Get Refund Info (Req 6 al Req 11).
Parte 7 [Final]
• 898570 SR - Radicación Solicitudes Individual - Pantalla 3 - Integrar llamado a API Get Refund Info (Req 19) Parte 3
• 968916 SR - Ajuste en el manejo de solicitudes en proceso y reconfiguración del servicio de "Send Refund Info". Parte
III [Final]
• 977223 SR - Ajuste a la Pantalla 3 / 4 para finalizar cuando hay un error
• 995354 SR - Rechazo de tiquetes con actualización en Mozart y AVR
• 1004993 SR - Ajuste Special Refund FOP
• 1015345 SR - Validación de nombres duplicados en archivos adjuntos
7.2.1.3.1. Rechazo de solicitud
Este es un proceso que se puede realizar en la Tercera pantalla, consiste en
rechazar la solicitud presionando una opción que se puede apreciar en la sección
inferior de la pantalla, la cual es la siguiente
30
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se desplegará un POP UP solicitando elegir la razón de rechazo
31
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Opciones de rechazo, Se selecciona una y se da clic en “Confirmar”
Dentro de la Base de Datos de AVrefund la cual es az-sqla-avref-use-qa usando el
número de solicitud creado en el proceso, se pueden consultar las tablas
[rfd].[AVR_INFORMATION_PASSENGER]
[rfd].[AVR_INFORMATION_ADDITIONAL_PASSENGER]
para ver la información de la solicitud creada, para el ejemplo se observa que
correctamente se guardó como Rechazada.
32
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se verifica Mozart y fue registrado el refund request en estado rechazado
Se confirma que se encuentra rechazado en Mozart
Nota: lo anterior se agrega de acuerdo con los PBIs:
• 995354 SR - Rechazo de tiquetes con actualización en Mozart y AVR
33
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
7.2.1.3.2. Proceso cuando se eligen excepciones
Desde la Tercera pantalla “Ajuste de pasajeros” se pueden elegir excepciones, esto
ocasiona un comportamiento diferente en el proceso, ya que la solicitud pasa a una
auditoria, se documenta el proceso:
Para este caso
Al seleccionar “Defunción” y que es “Mayor de edad” se confirma que no solicita
elegir una forma de pago.
34
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se pasa a pantalla 4 y solicita los datos bancarios
Al dar clic en “Continuar” muestra un mensaje indicando que la solicitud será
cancelada y pasará a un proceso de revisión
Nota: lo anterior se agrega de acuerdo con los PBIs:
• 968916 SR - Ajuste en el manejo de solicitudes en proceso y reconfiguración del servicio de "Send Refund Info". Parte
III [Final]
35
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
7.2.1.4. Cuarta Pantalla: Datos Bancarios
En esta sección “Datos bancarios” se observa los datos del titular de la cuenta e
información de contacto, lo cual no es editable.
Adicional tenemos la Moneda en la que se hizo la compra de los tiquetes y que si
se puede modificar.
El campo “País de la cuenta bancaria” se lista los países que tengan configurada
esa moneda en el PI en la tabla [rfd].[CUR_CURRENCY_COUNTRY] o en la
pantalla del PI en Maestras >> Monedas por país; estos datos bancarios y países
son recuperados al consumirse el API GetMasterInfo en este proceso.
36
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Los campos bancarios se solicitan de acuerdo al país seleccionado y que tengan
configurado en el PI en la tabla [master].[MST_SCREEN_FIELD_BANK] o en la
pantalla del PI en Maestras >> Datos Bancarios.
En la última sección se puede adjuntar un certificado bancario, se da clic en
“Continuar”
37
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al dar clic en continuar y pasar de la pantalla 4 a 5 se envía la información en la
send
refund
_
_
info agregando los nodos de los adjuntos cuando se tiene una
excepción y una certificación bancaria.
38
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con los PBIs:
• 892394 SR - Radicación Solicitudes Individual - Pantalla 4 - Datos bancarios - Front End
• 924817 SR - Radicación Solicitudes Individual - Pantalla 4 - Datos del titular de la cuenta y Adjuntar certificado bancario
- Front End
• 947930 SR - Radicación Solicitudes Individual - Pantalla 4 - Integrar API Get Master Info al formulario - Back End. Parte
II [Final]
• 898789 SR - Integrar API Send Refund Info - Pantalla 4 - Caso forma de pago "CR" Transferencia Bancaria Parte 2
• 977223 SR - Ajuste a la Pantalla 3 / 4 para finalizar cuando hay un error
• 1118535 SR - Ajustar el request de send refund info cuando tiene excepción y un adjunto de certificación bancaria
• 1233618 SR - Moneda Formularios datos bancarios - Solicitar moneda para FOP cash en formulario datos bancarios.
• 1241664 SR - Moneda Formularios datos bancarios - Procesar moneda de la cuenta bancaria
39
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
7.2.1.5. Quinta Pantalla: Confirmación
En esta pantalla se muestra el resultado final de la solicitud con un breve resumen
de la reserva, datos del titular y valores.
En esta primera sección se observa la forma de pago elegida, los datos de la reserva
y numero de caso.
En “detalle de reembolso” se puede desplegar las pestañas para observar los
detalles de los tickets o EMD.
Al final se observa un resumen del total
40
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Con esto se da por finalizado el proceso de solicitud de reembolso
7.2.1.5.1. Verificar Registro de solicitud en Base de datos
Dentro de la Base de Datos de AVrefund la cual es az-sqla-avref-use-qa usando las
el número de solicitud creado en el proceso, para ver la información de la solicitud
creada se pueden consultar las tablas:
[rfd].[AVR_INFORMATION_PASSENGER]
y[rfd].[AVR_INFORMATION_ADDITIONAL_PASSENGER]
7.2.1.5.2. Registro en Mozart
Al crearse una solicitud también se registra en Mozart, se verifica el registro en
Mozart https://mozart.av.accelya.com/mozart_uat/RefundSearch/Index#
Se consulta el número de solicitud
41
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con los PBIs:
• 947622 SR - Radicación Solicitudes Individual - Pantalla 5 - Confirmación - Front & Backend. Parte II [Final]
7.2.2. Formulario Captura de reembolsos Individuales
Cuando el cliente ingresa la información en el formulario, el sistema realiza la
llamada a la API Get Info TKT. Si la API responde con código 1110 (información no
encontrada), el sistema despliega una modal con el mensaje:
42
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
a continuación
“No se encontraron registros con el PNR y apellidos ingresados.” como se muestra
Cuando no se encuentra la información automáticamente al dar clic en “Ingresar
TKT o EMD” y se abre formulario el cual permite a negocio continuar con la creación
de una solicitud de reembolso cuando no es posible obtener la información del
documento (PNR, TKT o EMD).
Ingreso manual de datos bancarios (Pantalla 2)
Esta pantalla se divide en dos módulos, información general e información de
tiquetes.
43
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Información General:
• PNR: Código localizador de la reserva correspondiente al pasajero.
• Email: Correo electrónico del pasajero o del contacto asociado a la solicitud.
• Nombres: Nombre del pasajero tal como aparecen en el documento de viaje.
• Apellidos: Apellido del pasajero.
• Frequent Flyer Number: Número de Lifemilles (11 digitos)
• Canal: Canal por el cual se recibió la solicitud de reembolso.
• Fecha de Solicitud fecha en la que se está registrando la solicitud.
• Idioma: Idioma en el que se atenderá la solicitud.
Información de Tiquetes:
• TKT Number: Número del tiquete.
• Tipo de Documento: tipo de documento que desea registrar:
o TKT: tiquete aéreo.
o EMD: documento electrónico asociado a servicios adicionales.
• Corporate Code: código corporativo asociado al tiquete.
• Nombre del pasajero: nombre del pasajero asociado al documento.
• Apellido del pasajero: apellido del pasajero asociado al documento.
• Código Tipo de Pasajero: tipo de pasajero (Adulto, Niño o Infante).
• Código EMD: cuando el Tipo de Documento seleccionado es EMD. Ingrese el
código EMD correspondiente.
Si la solicitud incluye más de un documento, dar clic en el botón “Agregar Tiquete”
.
Se insertará una nueva línea para diligenciar la información del siguiente
documento.
Eliminar un tiquete: Cuando existan dos o más registros, el sistema mostrará el
ícono de papelera para Eliminar la línea del Tiquete correspondiente, el cual permite
retirar el registro seleccionado sin afectar la información de los demás documentos.
Una vez diligenciados todos los campos obligatorios y verificando que la
información sea correcta, dar clic en el botón Continuar.
44
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
El sistema validará la información registrada y, si no encuentra inconsistencias,
enviará los datos al servicio correspondiente para continuar con el proceso en la
Tercera Pantalla: Solicitud de reembolso.
Nota: lo anterior se agrega de acuerdo con el PBI:
• 1243385 SR – Workaround Ley Dot – Módulo de valores faltantes – Creación de tabla
• 1281947 SR – AV/LM para ingreso de tiquetes - Creación de nuevo formulario de captura de reembolsos Individuales-
Parte II
7.2.3. Solicitudes masivas de Reembolso
Para cargar una solicitud de reembolso, ingresar al menú Procesos y seleccionar
el sub-menú Solicitudes Masivas de reembolso
45
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se presenta la pantalla donde se carga la solicitud.
Antes de cargar el archivo se debe Parametrizar el correo electrónico para recibir
la notificación del resultado de la carga en la tabla de parámetros de la base de
datos: SELECT * FROM [master].[MST_PARAMETERS] where PARAMETER_CODE =
'EMAIL_NOTIFY_MASSIVE_LOAD_TESTERS'
Dar clic “Seleccionar un archivo”. Escoger un archivo con el formato y columnas
correctas
Pero antes del proceso de debe tener un archivo listo, debe cumplir con
características como, cantidad de columnas y sus nombres correctos, cada campo
debe cumplir una estructura
Este archivo puede estar en formato XLSX o CSV separado por comas
46
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• Apply_ard = "N= tkt_number es mandatorio . Y= consulta api para mirar los tkt
de las otras bases amadeus,Cryptico, BSR."
• Booking = PNR
• TktNumber = Numero de tiket o EMD
• Channel = Canal de solicitud
• RequestDate = Fecha de solicitud del reembolso. dd/mm/aaaa
• Exception = Excepciones
• FrequentFlyerNumber = Número de viajero frecuente
• Email = email del titular
• Name = Nombre del pasajero
• LastName = Apellido del pasajero
• Fop = Forma de pago (CR-TR)
• AgentRemarks = Remark
• Lang = Lenguaje ES, PT, EN
• DocumentType = Condicional, Tipo de documento asociado al registro. Valores
permitidos: T (Ticket) o E (EMD). Obligatorio cuando Apply_Ard = "N".
• CorporateCode: opcional; Código corporativo asociado al registro. Puede
enviarse vacío.
• IdPax= Condicional Identificador del pasajero. Debe iniciar con "PT".
Obligatorio cuando Apply_Ard = "N".
• PassengerTypeCode= Condicional, Tipo de pasajero.ADT, CHD e INF. Debe
venir en mayúscula. Mandatorio, cuando Apply_Ard = "N".
• PaxFirstName= Nombre del pasajero. Mandatorio cuando Apply_Ard = "N".
• PaxLastName= Apellido del pasajero. Mandatorio cuando Apply_Ard = "N".
• EmdCode= Código EMD asociado al registro. Mandatorio cuando Apply_Ard =
"N" y DocumentType = "E".
Validaciones para Apply_Ard = "N": el sistema deberá validar obligatoriamente
la siguiente información:
• Channel
• Lang
• Booking
• RequestDate
• Email: cuando no exista CorporateCode
• Name: cuando no exista CorporateCode
• LastName
• TktNumber
• DocumentType
• IdPax
• PassengerTypeCode
47
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• PaxFirstName
• PaxLastName
• EmdCode: cuando DocumentType = "E"
Validación de DocumentType: El valor deberá encontrarse parametrizado Y se
debe almacenar en mayúscula.
•
•
“T” = Ticket.
“E” = EMD.
Validación de PassengerTypeCode: El valor deberá encontrarse parametrizado
Y se debe almacenar en mayúscula.
“ADT”
,
“CHD”
,
“INF”
Validación de IdPax: Debe iniciar con el prefijo: “PT”, ejemplos válidos: PT1, PT2,
PT3, PT…
Validación de TktNumber: Debe iniciar con una placa válida. Las placas
permitidas deberán encontrarse configuradas mediante parámetro. El sistema
valida que la placa corresponda a alguno de los valores configurados.
Ejemplo: “134”
”202”
”133”
”547”
,
,
,
Resultado de la carga:
Cuando alguna de las validaciones anteriormente descritas no se cumpla:
• El registro se procesa como Fallido.
• El sistema informa el motivo correspondiente.
• El registro no se almacena como exitoso en la tabla de carga masiva.
Ejemplos:
• DocumentType no válido.
• PassengerTypeCode no configurado.
• IdPax debe iniciar con PT.
• Placa de TktNumber no permitida.
• EmdCode obligatorio para documentos tipo E.
Las demás características y validaciones del proceso de carga masiva continúan
funcionando de acuerdo con la solución actual.
El Excel o csv nuevo debe contener las columnas:
48
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Apply_ard, Booking, TktNumber, Channel, RequestDate, Exception,
FrequentFlyerNumber, Email, Name, LastName, Fop, AgentRemarks, Lang,
DocumentType, CorporateCode, IdPax, PassengerTypeCode, PaxFirstName,
PaxLastName, EmdCode.
Si existen campos que no cumplan la estructura o el archivo no es válido, se
avisara con un mensaje en pantalla
Cuando es exitoso
Al cargar el archivo, Dar clic en el botón “Procesar Archivo”
Al finalizar el procesamiento del archivo se presenta mensaje de “Carga
completada exitosamente”
49
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se recibe un correo con la información del cargue, acá se puede observar cuales
registros fueron cargados exitosamente, y cuales contaban con un dato que impedía
su cargue en las tablas.
Revisar el correo electrónico parametrizado previamente al proceso
Descargar el archivo adjunto y descomprimirlo, en este se encontrará el archivo de
resultados de la carga realizada.
50
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Ahora, podemos observar que estos registros fueron cargados a la tabla
SP_REF_LOAD_MASSIVE_REQUEST con el estado de PROCESSED en N, es
decir aún no han sido procesados
SELECT * FROM [rfd].[SP_REF_LOAD_MASSIVE_REQUEST]
La function az-fapp-sprefprocess-use-qa se encarga de cada 10 minutos (tiempo
parametrizado en QA) tomar todos los registros de esta tabla y enviarlos en el API
Load Massive, si el proceso es correcto le asigna un refund request y cambia su
estado a C y si falla, cambia su estado a E con su razón de rechazo.
Para este caso, todos fallaron
Para los registros en estado E, verificar si existe otro registro con estado Processed
(C) dentro de la misma agrupación, considerando los siguientes criterios:
51
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• Mismo REFUND_REQUEST y PNR, o
• Solo el mismo PNR (en caso de que el registro no tenga
REFUND_REQUEST).
Si se encuentra al menos un registro con esas condiciones:
• Todos los registros en estado E de esa misma agrupación deben cambiar
su estado a F.
• En el campo razón de rechazo, se debe colocar el siguiente mensaje
reducido: "No se puede enviar, otro registro ya procesado."
Se carga archivo con datos que ya están en la Base de datos en estado C
Se confirma la inserción en la tabla de SR
SELECT REQUEST_DATE, REFUND_REQUEST, APPLY_ARD, PNR, EXCEPTION, NAME, LAST_NAME, E_MAIL, CHANNEL, TKT_NUMBER, LANGUAGE,
PROCESSED, ERROR_REASON,LOADED_BY, CREATED_DATE FROM [rfd].[SP_REF_LOAD_MASSIVE_REQUEST]
52
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Cambia de estado N a E
Cambia de estado E a F con el mensaje "No se puede enviar, otro registro ya
procesado"
Solo los registros que no cumplan con la condición anterior podrán continuar con
el consumo de la API load massive.
Se documenta un ejemplo cuando es exitoso, como se observa el estado cambio a
C y le asigno su refund request
Cuando los registros están siendo procesados por la function su estado cambia a I
en la columna PROCESSED
Cuando los registros ya tienen su refund request se pueden consultar en la tabla
en AVR
53
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Los siguientes refund request son exitosos realizados en otro proceso:
Tablas AVR
Se verifica inserción en tablas AVR
Se verifica que fueron registrados en Mozart
Se puede verificar que en los LOGS registra como la function construyo la solicitud
en el API LoadMassive
54
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
7.2.3.1. Estados de las solicitudes cargadas masivamente:
N o vacío = No procesado
I = En proceso de radicación
E = Reintento
F = Finalizado
C = Radicado - Exitoso
Nota: lo anterior se agrega de acuerdo con los PBI
• 765345 - SR - Pantalla para radicación de solicitudes masivas desde la aplicación web
• 889855 - SR - Ajuste Radicación de solicitudes masivas desde la aplicación web (Back End) - Modificación de campos
Parte 3
• 889855 SR - Ajuste Radicación de solicitudes masivas desde la aplicación web (Back End) - Modificación de campos
Parte 3
• 687244 SR - Layout cargue masivo para radicación de solicitudes Parte 1 Paso 1 y Paso 2
• 776339 SR - Pantalla para radicación de solicitudes masivas desde la aplicación web (Back End)
• 814422 SR - Soporte para Cargue masivo para radicación de solicitudes - Paso 3 Procesar la creación de reembolsos
• 982283 SR - Modificación de función para integración con Load Massive Refund Request. Parte III [Final]
• 1047102 SR - Ajuste para agregar canal 14 (aeropuertos) y parametrización de canales en Load Massive - Carga
Masiva
• 1039233 SR - Ajuste Plantilla Reembolsos Masivos
• 1131714 SR - Load Massive - Ajuste - Validación previa antes del consumo de la API load massive
• 1252259 - SR AV/LM para ingreso de tiquetes - Ajuste plantilla y tabla Load Massive - Nuevos campos.
7.2.3.2. Reintentos de envío de las solicitudes masivas:
Se tiene un contador de reintentos de envío en el proceso de envío masivo, dentro
de la función encargada de ejecutar los envíos, se implementó un mecanismo para
contar el número de intentos realizados por cada registro.
Si un registro supera el número máximo de intentos permitidos (por defecto: 5), su
estado debe actualizarse automáticamente a "F" (Fallido) y dejar de procesarse.
• Cada intento de envío incrementa un contador de intentos asociado al registro.
en el campo send_attempt de la tabla [rfd].[SP_REF_LOAD_MASSIVE_REQUEST].
55
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• El límite de intentos es configurable a través del parámetro
'MAX_RETRIES_MASS_SENDING' (valor por defecto: 5).
• Si el número de intentos supera el límite configurado, el estado del registro se
cambia a "F" (Finalizado). Y Una vez en estado "F", el registro no debe ser
considerado para futuros reintentos.
• Se debe registrar en el log [rfd].[SP_REF_LOGS_TRANSACTION] el motivo del cambio
de estado.
Si sacamos el log_msn tenemos:
56
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con el PBI:
• 1063404 SR - Control de Reintentos en Envío Masivo – Cambio de Estado a “F”
7.2.3.3. Function Load File para procesamiento masivo de
solicitudes
Ingresar a Portal azure en avtest a la function azstaccsprefuseqa:
https://portal.azure.com/#@avtestonline.onmicrosoft.com/resource/subscriptions/1b3f8b8d-3a05-4d91-a270-
46907a9d0259/resourceGroups/az-rg-refundsSP-use-
qa/providers/Microsoft.Storage/storageAccounts/azstaccsprefuseqa/storagebrowser
Ingresa a la carpeta SR_Bulk_Upload y cargar el archivo de solicitudes de carga
masiva
57
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
La Function Load File se encargará de procesar los registros contenidos en el
archivo enviando a las carpetas de procesados y No procesados los registros que
apliquen para cada carpeta
Ajuste Function Load File – Validación de Tiquetes Duplicados y
Reprocesamiento de Registros:
58
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Antes de realizar el consumo de la API Load Massive, la Function deberá validar
que dentro de una misma agrupación no existan números de tiquete duplicados.
La agrupación deberá considerar los mismos criterios actualmente existentes y
adicionalmente el campo Created_Date, tomando únicamente la fecha (AAAA-
MM-DD) sin tener en cuenta la hora.
Si dentro de una agrupación se identifica un número de tiquete repetido:
• Ningún registro de la agrupación deberá ser enviado a la API Load Massive.
• Todos los registros de la agrupación deberán actualizarse con estado:
PROCESSED = F
• Se deberá registrar la siguiente razón de rechazo: Tiquete duplicado
• Adicionalmente, la Function deberá considerar para el proceso de envío
aquellos registros que cumplan las siguientes condiciones: PROCESSED =
E y ERROR_REASON IS NULL o ERROR_REASON = '' (cadena vacia)
Los registros que cumplan estas condiciones deberán ser incluidos nuevamente
en el proceso de agrupación y validación previo al consumo de la API Load
Massive.
Con esta validación se evita el envío de información desactualizada perteneciente
a registros antiguos y se garantiza el reprocesamiento correcta de registros que
quedaron en estado de error sin una razón de rechazo registrada.
Nota: Lo anterior se agrega de acuerdo con el INC 1255907 - Issue [Refund] -
[SR Masivos] - Carga el tiquete con fecha de solicitud diferente al formato de
carga masiva.
Se ingresa a la carpeta de procesados
59
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Descargar el archivo y se encuentra el resultado, para este caso como es un
registro procesado queda resultado = Exitoso
Se ingresa a la carpeta de No procesados
Se descarga el archivo y se encuentra el resultado, para este caso como es un
registro procesado queda resultado = Fallido, con el detalle del Motivo del Fallo.
Nota: lo anterior se agrega de acuerdo con los PBI
• 889638 - SR - Ajuste Function Load File para procesamiento masivo de solicitudes - Modificación al PASO 1 -
VERIFICACIÓN Y CARGUE DE REGISTROS Parte 3
60
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
7.2.3.4. Mantenimiento de datos históricos de Cargue masivo
Con la siguiente funcionalidad se tiene como objetivo eliminar los archivos que
lleven 1 año en el repositorio en las carpetas de No procesados y procesados y en
la tabla SP_REF_LOAD_MASSIVE_REQUEST
En la base de datos se encuentra el siguiente parámetro el cual se parametrizará
por años es decir solo se debe ingresar número de años, ejemplo: 0, 1, 2
SELECT * FROM [master].[MST_PARAMETERS] WHERE PARAMETER_CODE =
'SP_AZFHISTMAINT_YEARS_FOR_REMOVE_REQUEST'
La lógica consultará el parámetro existente en base de datos y procederá a eliminar
los registros que coincidan con el número de años que se haya ingresado,
adicionalmente para esto cada registro tendrá PROCESSED = 1 (Indica que es un
registro que ya fue procesado y enviado) y en el campo DATE_SEND = (contiene
la fecha de envío la cual debe coincidir con 1 año o el número de años
parametrizados al momento de la Function MaintHistorySpRef buscar registros para
eliminar)
Ingresar a AVTEST donde se encuentra la Function az-fapp-sprefhistmaint-use-qa
- MaintHistorySpRef:
https://portal.azure.com/#@avtestonline.onmicrosoft.com/resource/subscriptions/1
61
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
b3f8b8d-3a05-4d91-a270-46907a9d0259/resourceGroups/az-rg-refundsSP-use-
qa/providers/Microsoft.Storage/storageAccounts/azstaccsprefuseqa/overview
Ejecutar la Function: az-fapp-sprefhistmaint-use-qa - MaintHistorySpRef
Ingresar al correo electrónico parametrizado donde se encuentra la notificación
con el LOG del resultado de la ejecución adjunto
Consultar el LOG Transaccional donde se encuentra la trazabilidad de la ejecución
62
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
De igual manera es el mismo proceso para eliminar las carpetas del repositorio,
para el ambiente QA se prueba con parámetro = 0, debido a que para el momento
no hay archivos de 1 año atrás.
Se consulta si existen registros en el repositorio
63
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se ejecuta la function az-fapp-sprefhistmaint-use-qa - MaintHistorySpRef
Ingresar al correo electrónico parametrizado donde se encuentra la notificación
con el LOG del resultado de la ejecución adjunto
64
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Consultar el LOG Transaccional donde se encuentra la trazabilidad de la ejecución
Nota: lo anterior se agrega de acuerdo con los PBI
• 801291 - SR - Cargue masivo para radicación de solicitudes - Paso 4 Mantenimiento de datos históricos Parte 3 Final
7.2.4. Formulario Captura Reembolsos Faltantes
El área de reembolsos solicitó un Módulo de Valores Faltantes el cual permite
gestionar el reembolso de montos pendientes mediante Avianca Credits, en
65
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
original.
aquellos casos donde existan errores o inconsistencias en el proceso de reembolso
En este módulo se permite la radicación, validación y autorización de estos casos,
bajo un flujo de aprobación controlado.
Los parámetros relacionados que tenemos son:
select * from [master].[MST_PARAMETERS] where parameter_code in
('MVR_FINAL_STATUSES','MVR_SEND_FAILED_STATUS','MVR_PIC_SEND_SUCCESS_STATUS')
Para ingresar es por el módulo de Procesos >> Formulario Captura Reembolsos
Faltantes.
Número de solicitud: Alfanumérico - Max 32 caracteres) mandatorio
Tiquete: Numérico. Mandatorio, longitud 13, debe iniciar por 134, 202, 133 o 547.
66
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
7.2.4.1. Creación solicitud VF
Al ingresar los datos de solicitud y tkt se da clic en “validar”; se consulta en
Consut_refund, pasa al formulario y si encuentra datos precarga la información de
nombre, apellido y correo, caso contrario deja los campos en blanco.
Formulario
Los campos del formulario son los siguientes
Linea Campo Tipo Mandatorio Editable Detalle
Caso del reembolso Alfanumérico si no precargado número de solicitud digitado por el usuario
en la Pantalla 1
Información
del caso
Tiquete Numérico si no precargado número de tiquete digitado por el usuario
en la Pantalla 1
PNR Alfanumérico si si 6 caracteres
IATA Numérico si si 8 caracteres
Canal de Solicitud Lista si si De acuerdo con la maestra de canales
[master].[MST_CHANNEL]
Información
financiera
Moneda Lista si s
si - Se debe realizar el consumo del API de monedas
del PI (/api/GetCurrencyList). Se debe mostrar el
código de la moneda ("currency-code").
67
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Valor faltante Decimal si si Separado por punto y máx. 2 decimales, este campo
no debe ser mayor al Total de la venta.
Total de la venta Decimal si si Separado por punto y máx. 2 decimales
Fecha de Venta Fecha si si (calendario – fecha corta) Formato: YYYY-Fecha MM-
DD
Nombre del Titular Varchar si no
precargado, en caso de no traer información es
editable - Se pobla con el valor del campo “first-name"
de la consulta del servicio.
Datos del
cliente
Apellido del Titular Varchar si no
precargado, en caso de no traer información es
editable - Se pobla con el valor del campo “last-name"
de la consulta del servicio.
Correo Varchar si no
precargado, en caso de no traer información es
editable - Se pobla con el valor del campo “email-
reservation" de la consulta del servicio.
Forma de Pago Lista si si (KR, NC) [master].[MST_PARAMETERS]
parameter_code ='MVR_FOP_LIST'
Reembolso
credits Programa Avianca
Lista si para KR si Para KR consulta [master].[MST_PARAMETERS]
parameter_code ='MVR_CPG_FILTER_LIST'
Razón del faltante Lista si si de la Maestra [master].[MST_MISSING_REASONS]
Usuario que radica Deshabilitado si no Precargado
Control y
trazabilidad
Fecha de radicación Deshabilitado si no Precargado
Estado Deshabilitado si no Precargado
Al terminar de diligenciar el formulario se habilitará el botón de “Guardar” el cual
almacena los datos en la tabla [rfd].[SR_MISSING_VALUE_REFUNDS_VF] y
[rfd].[SR_MISSING_VALUE_REFUND_STATUS_LOG_VF]
68
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se consulta en la tabla [rfd].[SR_MISSING_VALUE_REFUNDS_VF]
El botón “Cancelar” Permite salir del registro sin guardar información.
7.2.4.2. Aprobación o Rechazo Del Coordinador o Gerente:
Para realizar la aprobación de las solicitudes de Valores Faltantes se debe de contar
con el Rol Coordinador si el valor faltante es de 0 a 3500 USD y el Rol Gerente
aprueba si el valor faltante es mayor de 3500 USD. El cual se configura los valores
en la tabla [master].[MST_APPROVAL_RANGE]
La cual en la conversión de las diferentes monedas que se reciben; se realiza de
acuerdo con el TRM con la tabla [rfd].[SR_EXCHANGE_RATES]
69
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para iniciar consultamos un caso en la base de datos de SR en las tablas
[rfd].[SR_MISSING_VALUE_REFUNDS_VF] y
[rfd].[SR_MISSING_VALUE_REFUND_STATUS_LOG_VF] al encontrar la solicitud
y el estado es “Pendiente de autorización”.
Se realiza la consulta por numero de solicitud y ticket ó si se desea se da clic en el
botón “Buscar todas” para que se les muestre todas las solicitudes pendientes de
aprobar o de rechazar.
Antes de dar cualquier acción se muestra el siguiente mensaje informativo “Para
buscar una solicitud puntual, ingrese Número de solicitud y Tiquete. También
puedes consultar todas las solicitudes pendientes usando “Buscar todas” sin aplicar
filtros.”
Al consultar individualmente se tiene
70
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al dar clic en Validar se despliega una tabla con la información del valor faltante
Al consultar todos los casos se da clic en el botón “Buscar todas”
71
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se listan todos los casos pendientes a aprobar o rechazar dependiendo del rol ya
sea coordinador o Gerente
Y al final se observa los botones de aprobar o rechazar la solicitud
72
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
7.2.4.2.1. Aprobar solicitud de Valores Faltantes
Al confirmar que la información es correcta se da clic en “Aprobar” y se observa
mensaje “¿Está seguro de aprobar este reembolso faltante?”
Al dar clic en Aceptar se muestra el mensaje “El reembolso faltante se aprobó
correctamente”
Se observa el estado de la solicitud en “Autorizado” pendiente de ser enviado al PI
pero hace falta que se apruebe otro tkt relacionado a la solicitud Ya que si existe
más de un tkt relacionado a la misma solicitud no se envía hasta que todos los tkt
estén autorizados
73
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al dar clic en "Aprobar" ultimo campo del registro Se actualiza el estado del
proceso a “Autorizado” en el campo [STATUS] y se inserta la fecha de aprobación
en el campo APPROVAL_DATE en la tabla
[rfd].[SR_MISSING_VALUE_REFUNDS_VF] e inserta una linea con el nuevo
estado en la tabla [rfd].[SR_MISSING_VALUE_REFUND_STATUS_LOG_VF]
Se procede a aprobar el otro tkt relacionado
Se da clic en aprobar
74
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al no tener más tkt relacionados pendientes de aprobación; automáticamente se
envía al Integrador de pagos – PI dejando los casos en estado “En proceso”
Se confirma en Base de datos
75
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Y al pasar al Integrador de pagos pasan a las tablas
[rfd].[PIC_PAYMENT_REQUEST_VF] y [rfd].[PIC_PAYMENT_DETAIL_VF] e inicia
el proceso de pago.
En este caso se pago el voucher correctamente.
7.2.4.2.2. Rechazo de solicitud de Valores Faltantes
Con rol Coordinador o Gerente se tiene el botón de validar todas las solicitudes
pendientes de autorizar o rechazar; botón "Buscar todas" sin necesidad de
diligenciar los campos de solicitud y tiquete
Se busca la solicitud y se desplaza al final del lado derecho de la pantalla, allí vemos
el botón de Aceptar y Rechazar.
76
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al dar clic en "Rechazar" se ejecuta el proceso de rechazo
77
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se Actualiza en la BD el campo STATUS de la tabla:
[rfd].[SR_MISSING_VALUE_REFUNDS_VF] con el valor REJECTED. El campo
APPROVAL_DATE se inserta la fecha y hora en que se ejecuta la acción. Y se
Genera el registro de trazabilidad correspondiente en la tabla:
[rfd].[SR_MISSING_VALUE_REFUND_STATUS_LOG_VF]
78
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
7.2.4.3. Respuesta de PI a SR
Cuando en el PI se realiza el Pago de la solicitud del valor faltante este envia el
estado a SR a través del api MissingValueRefundStatus/Update
Si en el PI se realiza el pago
Este se actualiza en SR en la tabla [rfd].[SR_MISSING_VALUE_REFUNDS_VF]
Para validar la notificación y envío de reset pin en caso de voucher se confirma en
el PI y el template en AVR.
7.2.4.4. Estados de valores faltantes:
• Pendiente de Autorización: Registrado correctamente y pendiente de
aprobación
• Autorizado: Aprobado pero pendiente de tkts relacionados para aprobación
• En progreso: Enviado al integrador de pagos – PI
79
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• Pagado: Enviado del PI a SR
Si falla el envío al Pi la solicitud se devuelve a estado Pendiente de Autorización.
Nota: Lo anterior se agrega de acuerdo con los siguientes PBIs:
• 1252288 SR – Workaround Ley Dot – Módulo de valores faltantes – Formulario de captura de reembolsos faltantes-
Parte II
• 1274259 SR – Workaround Ley Dot – Ajuste Módulo de valores faltantes - Mapeo campos "Consult Refund" y Campo
FOP (ACM)
• 1262795 SR - Workaround Ley Dot - Modulo Faltantes - Workflow aprobación ley dot
• 1298428 SR - Modulo Faltantes - Ajuste al Envío de Solicitudes de Valores Faltantes hacia PI
• 1299002 [SR] Valores Faltantes: consulta masiva e individual, validación de monto y botón Rechazar
• 1300163 [SR] Modulo Faltantes- Crear API para actualización de estado de tiquetes desde PI
7.3. MAESTRAS
7.3.1. Gestión de Razones Faltante
Este módulo permite administrar las razones faltantes de reembolso; utilizadas
durante el proceso de gestión de razones faltantes para identificar el motivo
asociado a cada caso.
Para ingresar damos clic en Maestras y seleccionamos la opción “Gestión de
Razones Faltantes”
Desde este módulo se puede consultar, crear, modificar y activar o inactivar los
registros, de acuerdo con los permisos asignados.
80
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Función Consultar: El sistema mostrará la pantalla principal con el listado de las
razones de faltante registradas.
• La información se visualizará en una tabla con las columnas ID, Razón de
Faltante, Estado y Acciones.
Buscar una razón de faltante
• Ubique el campo de búsqueda ubicado en la parte superior de la tabla.
• Ingrese el texto correspondiente a la razón que desea consultar.
• El sistema filtrará automáticamente los registros que coincidan con el
criterio ingresado.
81
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• Si la búsqueda no encuentra coincidencias, el sistema mostrará un mensaje
indicando que no existen registros para el criterio de búsqueda ingresado.
• Para visualizar nuevamente todos los registros, elimine el texto del campo
de búsqueda.
Navegar entre los registros
• En la parte inferior de la tabla encontrará el control de paginación.
• Utilice los controles de navegación para desplazarse entre las diferentes
páginas de resultados.
• Si la funcionalidad está habilitada, podrá seleccionar la cantidad de registros
que desea visualizar por página.
Crear una nueva Razón de Faltante
En la pantalla principal, haga clic en el botón Agregar Razón de Faltante.
82
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
El sistema abrirá una ventana emergente (Pop-Up) para el registro de la nueva
razón.
• Diligencie los siguientes campos:
o Razón de Faltante.
o Estado.
• Haga clic en el botón Crear.
• Si alguno de los campos obligatorios no ha sido diligenciado, el sistema
mostrará el mensaje correspondiente indicando que la información es
obligatoria.
Si la longitud de la Razón de Faltante supera el máximo permitido, el sistema no
permitirá ingresar más caracteres.
83
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Si la Razón de Faltante ya existe en la maestra, el sistema informará que el registro
ya se encuentra creado y no permitirá almacenarlo nuevamente.
Cuando la información sea válida, el sistema almacenará el registro y mostrará un
mensaje de creación exitosa.
Si desea salir sin crear el registro, haga clic en el botón Cerrar (X).
Se crea correctamente, aparece mensaje exitoso, se almacena en BD, en la tabla
[master].[MST_MISSING_REASONS]
Modificar una Razón de Faltante:
Ubique el registro que desea modificar
En la columna Acciones, haga clic en el ícono Editar.
84
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
El sistema abrirá una ventana emergente con la información del registro
seleccionado.
• Modifique la información requerida.
• Haga clic en el botón Modificar.
• Si la información ingresada corresponde a una Razón de Faltante ya
existente, el sistema informará la duplicidad y no realizará la actualización.
• Cuando la modificación se realice correctamente, el sistema mostrará un
mensaje de actualización exitosa.
• Si desea salir sin guardar los cambios, haga clic en el botón Cerrar (X).
• Actualiza correctamente el registro, en la tabla
[master].[MST_MISSING_REASONS] en el campo UPDATED_DATE y
UPDATED_USER y muestra mensaje de actualización exitosa.
85
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Activar o Inactivar una Razón de Faltante
• Localice el registro que desea actualizar.
• En la columna Acciones, cambie el estado del registro utilizando el control
de activación o inactivación.
• El sistema actualizará el estado del registro.
• Una vez realizado el cambio, el sistema reflejará el nuevo estado en la tabla y
conservará la actualización realizada.
• El sistema actualiza el estado y STATUS cambia a 0 (Inactivo) o a 1 (Activo)
86
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con el PBI:
• 1292341: SR – Workaround Ley Dot - Creación del Front de la maestra de Razones de faltantes - parte 2
7.4. REPORTES
7.4.1. Reporte de carga Masiva
Reporte para consultar los resultados de las cargas masivas.
select * from [rfd].[SP_REF_LOAD_MASSIVE_REQUEST]
Ingresamos al menú Reportes y en el Sub-Menú Resultado Procesos Masivos.
Se realiza consulta por fecha
87
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
No puede ser mayor a un mes
Se confirma filtro Estado del Proceso:
Si es C = Exitoso
Si es I = En proceso
Si es E = Reintento
Si es F = Finalizado
N o vacío = No procesado
88
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Funcionamiento del filtro Refund Request
Funcionamiento del filtro Tiquete
Todos los resultados se pueden exportar tanto Excel como en CSV
Nota: lo anterior es de acuerdo con el PBI
89
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• 1046355 SR - Creación de reporte para carga masiva
8. Query Reporte usuarios Auditoria
Se crea SP para generar un reporte con los datos de la maestra de usuarios.
Ejecutar el SP EXEC [rfd].[SR_SP_USER_DATA_QUERY]
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
9. APIS
9.1. API Emd
A través de la API EmdEndpoints se ingresa registros a la tabla
Master.EMD_NUMBER
90
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Ingrear a la URL: https://azwappsprefbknduseqa.az-asev3-use-
qa.appserviceenvironment.net/externalservices/swagger/index.html
Buscar la APIEmdEndepoint, dar clice en el Boton “Try it out” para poder ingresar
datos en cada campo
Ingresar los datos del registro, dar clic en Ejecutar y se presenta mensaje de
inserción exitosa en el Response.
Se consulta en la base de datos el registro insertado en la tabla
Master.EMD_NUMBER
91
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Consultar en el LOG
92
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con el PBI
737197 - SR - Ajuste al servicio para recibir EMDs de aeropuertos (Lista de Objetos)
10. HISTORIAL DE PRUEBAS DE PERFOMANCE Y SEGURIDAD
N/A
11. GLOSARIO DE TÉRMINOS
Término Descripción / Definición
Reembolso Devolución de una cantidad de dinero a la persona que
la había desembolsado por la compra de un TKT.
93