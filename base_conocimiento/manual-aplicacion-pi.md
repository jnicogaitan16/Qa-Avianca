MANUAL DE APLICACIÓN
PI
(Payment Integrator)
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Historial de Cambios y Revisiones del Documento
Versión
Documento Fecha Modificado
por Secciones, páginas y texto afectado
1.0 13-10-
2023
Jenny
Garzón Se crea el Manual Funcional Payment Integrator Customer.
1.1 26-10-
2023
Andres
Diaz Se agrega informacion de la tabla SAP
1.2 01-11-
2023
Monica
Perez Se agrega el módulo Formas de pago
1.3 01-12-
2024
Isabel
Guerra Se agrega Ingreso al Sistema, Roles, Usuarios
1.4 27-11-
2023
María
Barrios Se agrega la opción Bancos del módulo Maestras.
1.5 19-12-
2023
María
Barrios Se agrega la opción Tipo de Identificación del módulo Maestras.
1.6 21-12-
2023
María
Barrios Se agrega la opción Tipo de Cuenta del módulo Maestras
1.7 08-05-
2024
Camilo
Loaiza
Se agregan las opciones Generar reporte y Administrar reporte del
módulo Reportes.
1.8 09-05-
2024
Camilo
Loaiza
Se agrega:
• opción Cargue de casos rechazos posterior la fecha de pago del
módulo de Procesos.
• opción Configuración de datos bancarios del módulo de
Maestras.
• sección de APIS, y se añade la API Payment Refund Request.
• la API Get Master Data SAP: Get currency list, en la sección de
APIS.
1.9 09-10-
2024
Isabel
Guerra
Se agrega:
• Funcionalidad API - Cambio para PBIs 605150 y 611686 IBAN
(API/ BankDataInformation)
• funcionalidad - Creación de API para cargar en una tabla de
control las solicitudes de reembolso para ser agrupadas en una
solicitud (Api/PicTempControl/create)
• funcionalidad de Creación de API para rechazar las solicitudes
de reembolso en la tabla temporal (Api/
ControlReuqest/Reject)
• funcionalidad de Function de SEND-CASH y Notificaciones
2 09-11-
2024
Isabel
Guerra
Se agrega funcionalidad - Consulta de reembolso con usuario con
mismo Canal al reembolso consultado. Y Reporte de Usuarios
2.1 09-12-
2024
Isabel
Guerra Se agrega funcionalidad – Reporte de Roles y Tabla de parámetros
2.2 09-13-
2024
Isabel
Guerra
Se agrega funcionalidad de API de chargebacck Y Reporte
Template to Output CCD to PIC
2
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
2.3 09-16-
2024
Isabel
Guerra
• Se agrega funcionalidad de Reporte Template to create Voucher
PIC
• funcionalidad API API Insert Refund Statu
• funcionalidad Procedimiento PIC_RETURN_SAP_INTERFACE
(proceso automático de la interfaz de retorno para pago con
cash a SAP)
2.4 09-18-
2024
Isabel
Guerra
• Se agrega funcionalidad del procedimiento de segunda forma de
pago EXEC rfd.SECOND_METHOD_OF_PAYMENT
• funcionalidad de Function que ejecuta el procedimiento
PIC_RETURN_SAP_UPDATE_PAYMENT_REQUEST_STATUS
• funcionalidad de Log de Auditoria
2.5 11-27-
2024
Isabel
Guerra
• Se agrega la funcionalidad de segunda forma de pago con los
ajustes realizados EXEC
rfd.SECOND_METHOD_OF_PAYMENT - Casos 15 y 16 T
• funcionalidad de segunda forma de pago con los ajustes
realizados EXEC rfd.SECOND_METHOD_OF_PAYMENT -
Ajuste Procedimiento Segunda Forma de Pago - Casos CR
• funcionalidad de la API que genera Diseño para comprobante de
pago TR y CR
2.6 12-09-
2024
Maria
Barrios
• Creación Tabla MST_FRANCHISE.
• Creación de campos en tabla
MST_PAYMENT_PROCESS_WAY.
• Creación de tabla MST_MANUAL_TEMPLATES_PAY_PROCC
• Actualización nombre campo SALE_CHANNEL_COD POR
CHANNEL_CODE en tabla MST_PAYMENT_PROCESS_WAY
2.7 27-12-
2024
Jenny
Garzón Se agrega menú Reapertura bancaria
2.8 28-01-
2025
Maria
Barrios Gestión de pagos PBI 629879.
2.9 11-03-
2025
Jenny
Garzón
Se agrega tabla maestra de Datos Bancarios y api Get Master Info. Y
Margen de tolerancia en el cargue de las plantillas de Pago para TC
3.0 14-04-
2025
Jenny
Garzón Se agrega API Bank_Data_Information
3.1 05-05-
2025
Jenny
Garzón
Para Salida temprana se agrega modificación de la llave para el
cargue de la Plantilla de Pago para Tarjeta de Crédito (Pago por
Primera Vez).
Y se agrega en Cargue de Resultados solo para "Otros Pagos
Manuales"
3.2 06-06-
2025
Jenny
Garzón
Se agrega Inactivación de Usuario, en la sección de Ingreso al
Sistema
3.3 07-30-
2025
Jenny
Garzón Se agrega Function de Rezagos
3.3 08/08/2025 Jenny
Garzón Se actualiza Reporte de Usuarios y Roles
3
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
3.4 10/14/2025 Jenny
Garzón Se agrega API Check Payment Status, APIM GetCurrencyList
3.5 10/28/2025 Jenny
Garzón Se Actualiza PaymentRequestEndPoint – PaymentOutput
3.6 11/04/2025 Jenny
Garzón
Se actualiza el response del api check Payment status adicionando
el campo IP
3.7 11/25/2025 Jenny
Garzón
Se actualiza las tablas agregando campo FOP Payment Request y
se agrega parámetros para Estados de pago. y para estado y
rechazo de capture Y se adiciona Servicio de procesamiento para
evaluar el estado capture
3.8 12/15/2025 Jenny
Garzón
Se agrega información en cargue de resultados. Querys reporte
Usuarios Auditoria y Consumo API refund
3.9 12/29/2025 Jenny
Garzón
Se actualiza los campos ed la plantilla manual, se adiciona en Otros
Pagos Manual
4.0 01/05/2026 Jenny
Garzón Se adiciona el campo “miles” en el api del Check Payment Status
4.1 02/05/2026 Jenny
Garzón Se adiciona “Cuando la segunda fop es CASH-CR - Notificación”
4.2 02/24/2026 Jenny
Garzón Se agrega el menú y procedimiento de Cargue de Resultados IP
4.3 02/25/2026 Jenny
Garzón
Se agrega Días máx para actualizar información de Datods
Bancarios o se Finaliza o Rechaza la solicitud
4.4 03/18/2026 Jenny
Garzón Se actualiza Plantillas de pago
4.5 04/27/2026 Jenny
Garzón Se agrega Maestra Iatas ACM y Gestión de Pago ACM
4.6 05/12/2026 Jenny
Garzón
Se agrega información del chek Payment Status y Vouchers no
Generados
4.7 05/19/2026 Jenny
Garzón
Se agrega información de para Descargar Plantillas de Pago
(Plantillas de Pago) y Ajuste Plantilla “Otros Pagos Manual”
4.8 05/25/2026 Jenny
Garzón
Se deshabilita el proceso de IP >> 1233639 PI - Moneda Formularios
datos bancarios - limpieza en API del desarrollo de IP
4.9 05/29/2026 Jenny
Garzón
Se agrega ACCOUNT_CURRENCY_CODE en el proceso de envío
a SAP CASH. Y se actualiza check Payment status
5.0 07/21/2026 Jenny
Garzón Se agrega Tabla de reglas de segunda forma de pago – Ley DOT
5.1 07/29/2026 Jenny
Garzón
Se agrega Envío de información a SAP ACM – NC para Valores
Faltantes Ley DOT
5.2 08/10/2026 Jenny
Garzón
Se actualiza plantillas manuales. Y se adiciona Reporte Casos
Autorizados Valores Faltantes
5.3 08/13/2026 Jenny
Garzón
Se agrega API MissingModules - Valores Faltantes de SR a PI. Se
agrega parámetro de reintentos para actualización de datos bancarios.
Se actualiza proceso de envío de información a SAP CASH – CR con
reembolsos con decimales y números de identificación en el campo
vendor
4
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
5.4 08/25/2026 Jenny
Garzón Se actualiza pantalla Gestión de pago, Botón enviar notificación
5.5 09/08/2026 Jenny
Garzón Se adiciona información de comprobantes de Pago en Francés
Aceptación del Manual de Aplicación
Elaborado por: Revisado por: Aprobado por:
5
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
1 Contenido
1 Contenido ......................................................................................... 6
1. INTRODUCCIÓN............................................................................ 10
1.1. 1.2. 2. Propósito del documento .......................................................... 10
Documentos de referencia: ....................................................... 10
PRESENTACIÓN DEL APLICATIVO ........................................ 10
2.1. Identificación ................................................................................. 10
2.2. Alcance ........................................................................................... 10
2.3. Arquitectura ................................................................................... 11
2.4. 3. 4. 4.1. 5. 6. Especificación detallada de los componentes: ................... 11
RECOMENDACIONES ANTES DE LA INSTALACIÓN ......... 15
PUESTA EN AMBIENTE PRUEBAS O PRODUCCIÓN ........ 15
Despliegue en ambiente de pruebas ...................................... 15
PROCESO DE ROLL BACK ....................................................... 15
PROCEDIMIENTO DE CONFIGURACIÓN ............................... 15
6.1. Configuración Hardware ............................................................ 15
6.2. Configuración Software.............................................................. 15
7. 8. 9. GENERACIÓN DE NUEVOS DATOS ........................................ 15
DESCRIPCIÓN DE LA FUNCIONALIDAD ............................... 16
RELACIÓN CON OTROS SISTEMAS ....................................... 16
10. INGRESO AL SISTEMA ............................................................... 18
10.1. Inactivación de Usuario .............................................................. 20
10.2. Descripción del perfil de usuario ............................................. 22
11. MÓDULOS ...................................................................................... 22
11.1. PROCESOS .................................................................................... 22
11.1.1. Pagos RTS...................................................................................... 22
11.1.1.1. Plantilla de Pago para Tarjeta de Crédito (Pago por
Primera Vez) .......................................................................................................... 22
11.1.1.2. Plantilla de Pago para Voucher (Pago por primera vez)) .. 23
11.1.1.3. Plantilla de Pago para Voucher (Pago por Primera Vez) ... 28
11.1.1.4. Plantilla para Actualización de Datos (Voucher)) ................ 29
11.1.2. Plantillas de pago ......................................................................... 29
6
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
11.1.2.1. BAC Regional ................................................................................ 34
11.1.2.2. Sin Captura .................................................................................... 38
11.1.2.3. Cardinal ........................................................................................... 39
11.1.2.4. Credibanco ..................................................................................... 42
11.1.2.5. Cielo ................................................................................................. 45
11.1.2.6. Redeban .......................................................................................... 47
11.1.2.7. Santander ....................................................................................... 51
11.1.2.8. 11.1.3. 11.1.4. 11.1.6. Otros Pagos Manual .................................................................... 53
Cargue de Resultados ................................................................ 58
Cargue de Rechazados ............................................................... 71
11.1.5. Reapertura Bancaria ................................................................... 76
Consulta de Reembolso ............................................................. 85
11.1.7. Gestión de Pago ........................................................................... 86
11.1.7.1. Botón Autorizar: ........................................................................... 92
11.1.7.2. Botón Voucher .............................................................................. 93
11.1.7.3. Botón Enviar notificación .......................................................... 94
11.1.7.4. Datos Dummy ................................................................................ 97
11.1.7.5. 11.1.8. Validación en Output de Pago para DM ................................. 99
Vouchers no Generados .......................................................... 100
11.1.9. 11.1.10. Cargue de Resultados IP >> Menú deshabilitado ............. 102
Gestión de Pago ACM ............................................................... 107
11.2. ADMINISTRACIÓN...................................................................... 111
11.2.1. Gestión de Usuarios .................................................................. 111
11.2.2. Gestión de Roles ........................................................................ 114
11.3. TABLERO ..................................................................................... 125
11.4. MAESTRAS .................................................................................. 125
11.4.1. IATAs ACM ................................................................................... 125
11.4.2. Parámetros del Sistema ........................................................... 127
11.4.3. Datos Bancarios ......................................................................... 133
11.4.4. Países ............................................................................................ 141
11.4.5. Ciudades ....................................................................................... 143
7
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
11.4.6. Tipos de Identificación ............................................................. 146
11.4.7. Formas de Pago.......................................................................... 148
11.4.8. Moneda por País ......................................................................... 158
11.4.9 Tipo de Cuenta ............................................................................ 158
11.4.10 Bancos .......................................................................................... 166
11.5 REPORTES ................................................................................... 171
11.5.1 Administrar Reporte .................................................................. 171
11.5.2 Generar Reporte ......................................................................... 173
11.5.2.1 Reporte de Usuarios.................................................................. 175
11.5.2.2 Reporte de Roles ........................................................................ 183
11.5.2.3 Reporte Casos Autorizados Valores Faltantes .................. 189
11.5.2.4 Querys reporte Usuarios Auditoria ....................................... 196
12. Reporte de RTS para TC y Voucher ...................................... 197
12.1 Reporte Template to Output CCD to PIC Report ............... 197
12.2 Reporte Template to create Voucher PIC ............................ 200
13. Procesos Adicionales ............................................................... 202
13.1. SAP ................................................................................................ 202
13.1.1. Envío de información a SAP CASH - CR.............................. 202
13.1.2. Procedimiento de Retorno ....................................................... 210
13.1.3. Retorno de información de SAP CASH - CR ....................... 212
13.1.4. Envío de información a SAP ACM - NC ................................ 215
13.1.5. Envío de información a SAP ACM – NC para Valores
Faltantes Ley DOT ............................................................................................. 216
13.2. Días máx para actualizar información de Datos Bancarios
o se Finaliza o Rechaza la solicitud .............................................................. 218
13.3. Function de Rezagos ................................................................ 224
13.4. Proceso de Contracargo – Chargeback ............................... 228
13.5. Proceso Estados de Pago – TR .............................................. 228
13.6. Proceso Creación de Voucher - KR ...................................... 230
13.7. Workaround Ley Dot (Canal 15 y 16) .................................... 232
13.7.1. Tabla de reglas de segunda forma de pago – Ley DOT... 232
14. APIs ................................................................................................ 235
8
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
14.1. 14.1.1. PaymentRequestEndPoint – PaymentOutput .................... 235
Tratamiento especial para canales BSP en flujo de pagos
237
14.1.2. 14.1.3. 14.1.4. 14.2. Control de registros de TKT duplicados para pago ......... 239
PaymentRequestEndPoint – PaymentOutput para LM .... 241
PaymentRequestEndPoint – PaymentOutput para TC .... 246
Servicio de procesamiento para evaluar el estado capture
247
14.3. Segunda forma de Pago – Payment Output Mozart ......... 250
14.3.1. Cuando la segunda fop es CASH-CR - Notificación ......... 250
14.3.2. Modificación campos rechazo con segunda forma de
pago. 256
14.4. Payment Refund Request ........................................................ 257
14.5. Get Master Data SAP: Get currency list ............................... 260
14.6. API PicTempControl/create ..................................................... 264
14.7. API ControlRequest Reject ...................................................... 266
14.8. API GetChargeback ................................................................... 268
14.9. External API Insert Refund Status ......................................... 274
14.10. API Comprobante de Pago ...................................................... 275
14.11. API Bank_Data_Information .................................................... 280
14.12. API Check Payment Status ...................................................... 286
14.13. Número de reintento.................................................................. 296
14.14. APIM GetCurrencyList .............................................................. 297
14.15. Consumo API refund ................................................................. 300
14.16. API MissingModules - Valores Faltantes de SR a PI ........ 302
15. TABLAS ........................................................................................ 304
15.1. [rfd].[PIC_FOP_PAYMENT_REQUEST] ................................ 304
15.2. MST_PAYMENT_PROCESS_WAY ......................................... 304
15.3. [master].[MST_PARAMETERS] .............................................. 307
15.4. MST_CHANNEL_FOP_ADDITIONAL ..................................... 309
15.5. MST_FRANCHISE ....................................................................... 309
15.6. MST_MANUAL_TEMPLATES_PAY_PROCC ....................... 310
9
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
16. 18. Mantenimiento y Limpieza de data histórica ...................... 311
17. ERRORES CONOCIDOS ........................................................... 320
GLOSARIO DE TÉRMINOS ...................................................... 320
1. INTRODUCCIÓN
1.1. Propósito del documento
Documentar las principales funcionalidades, flujos y actividades que intervienen
en el Integrador de Pagos (PIC).
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
La presente guía de la aplicación PIC (Payment Integrator Customer) este
sistema administra la información requerida para ejecutar los pagos de
reembolsos. Así mismo es el punto de configuración y control para el
lanzamiento de las interfaces de pagos a los diferentes sistemas pagadores
de AVIANCA.
2.2. Alcance
Este sistema es desarrollado en AVIANCA para la administración del proceso
de pagos de reembolsos una vez estos estén aprobados.
Además, almacena la información del reembolso que es solicitada al cliente
y que está relacionada únicamente con el pago y que no es almacenada ni
requerida en ninguno de los otros sistemas participantes en el proceso de
reembolso.
10
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
En este sistema se encuentra también la parametrización de tipos de pago y
documentos o datos adicionales necesarios para realizar el pago de un
reembolso de acuerdo con su tipo.
2.3. Arquitectura
2.4. Especificación detallada de los componentes:
Payment Integrator Customer Front:
Front End de la Solución PIC, Es la capa de usuario final. Este componente
está expuesto a internet.
Entre otros tiene los módulos de:
• Autenticación con AAD.
• Administración de parámetros y reglas de negocio requeridas para la
generación de los pagos de reembolsos.
• Administración de tablas maestras que maneja esta solución (ej. Tipos
de Pago de reembolsos)
• Seguimiento de los procesos de pago de los reembolsos
• Consulta de información adicional ingresada para el pago de reembolsos
Se implementó un proxy reverso para invocar los servicios de la capa de
backend de la solución teniendo en cuenta que esta no se publica en
INTERNET.
11
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Type: Web Responsive
Protocol: HTTPS
Language: Angular
Payment Integ Backend Services:
Capa de backend de la solución de Revenue. API que contiene servicios con
lógica de negocio asociada a los procesos desencadenados desde el front
end de la solución de revenue, así como servicios que son necesarios para
abstraer la capa de presentación.
Type: RESTful API
Protocol: HTTPS
Language: .NET Core / Java
Contenerizable
Payment Integrator External Services:
API de servicios de la solución para exponer los servicios a ser consumidos
por las aplicaciones externas y desarrollar la lógica de negocio asociada a
los mismos. Los servicios son expuestos a través del APIM de AVIANCA
Language: .NET Core / Java
Contenerizable
Validate Payment Status:
Este proceso automático se encarga de hacer validaciones de pagos que
hayan sido generados y de los que no hubiese obtenido respuesta, para
recuperar su último estado y actualizarlo en la base de datos.
Language: .NET Core
Desarrollado para desplegar en una function (método principal de
despliegue) con capacidad de ser contenerizado.
SAP PROCESS:
El proceso de envío de información a SAP se ajustó para que las interfaces
se generen mediante este proceso automático y que lleguen a la capa de
servicios actual para entregarlas a SAP por la integración actual.
Language: .NET Core
Debe ser desarrollado para desplegar en una function (método principal de
despliegue) con capacidad de ser contenerizado
12
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Update Payment Status:
Este proceso se ejecuta periódicamente para enviar actualización de estado
del reembolso cuando se celebre el pago.
Language: .NET Core
Desarrollado para desplegar en una function (método principal de
despliegue) con capacidad de ser contenerizado
Hist. Payment Integ:
Para procesos de consultas históricas o información de pagos de
reembolsos, se hace uso de este esquema de base de datos. Esta base de
datos almacenará información únicamente desde el año 2 hasta el año 5.
Importante: Esta base de datos histórica se empezará a poblar a partir del
mes 25.
Motor: SQL Azure Database.
DB Payment Integ:
Éste es un esquema de base de datos y es el repositorio principal de la
solución Payment Integrator Customer.
Su diseño de base de datos es completamente eficiente enfocado a ser un
sistema transaccional con alta recurrencia.
Esta base de datos almacena información únicamente de dos años y
después se mueve a la base de datos histórica.
Motor: SQL Azure Database.
Retención de información: 24 meses
HistMaintenance:
Este proceso tiene la capacidad de hacer mantenimiento de data Histórica
de acuerdo con lo determinado en cada repositorio de datos de la solución
PIC, y a lo calendarizado en dicha solución. Se ejecuta periódicamente, deja
log de ejecución y puede recuperar el punto en el que falló ante cualquier
necesidad de relanzamiento del proceso.
De acuerdo con cada repositorio realiza:
Hist. Payment Integ: Elimina la data que supere los 5 años.
DB Payment Integ: Elimina la data que supere los 2 años.
Payment Integ Files y Processed: elimina los archivos que superen el tiempo
definido para almacenamiento de estos.
13
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Generate files:
Este proceso automático se encarga de generar los archivos de informes de
pagos necesarios requeridos de acuerdo con las especificaciones de los
requerimientos de negocio.
Desarrollado para desplegar en una function (método principal de
despliegue), en web app o incluso contenerizado.
Payment Integ Files:
Este repositorio es para almacenar los archivos generados por la solución de
reembolsos y requeridos por la central de reembolsos de AVIANCA
Los archivos son accedidos por medio del storage explorer de acuerdo a los
permisos otorgados al usuario de la central de reembolsos.
Payment Integ Files Processed:
Este repositorio es para almacenar los archivos adjuntos relacionados al
pago para una solicitud de reembolsos. Se crea una carpeta por cada caso
de reembolso recibido para poder acceder a la información cuando esta
requiera ser consultada desde el sistema.
Los archivos son accedidos por el storage explorer de acuerdo a los permisos
otorgados al usuario de la central de reembolsos.
Key Vault Payment Integ:
Este componente permite almacenar las llaves y secretos necesarios para la
solución PIC.
Log Payment Integrator:
La solución tiene un log que permite hacer seguimiento de diferentes
procesos de la solución o sucesos de error, para ello se hace uso de un
Aplication Insights de Azure, y cada componente de la solución Payment
Integrator Customer puede dejar información en este repositorio.
Tiempo de retención 90 días.
DATAFACTORY:
Tiene pipelines para realizar el movimiento de información de la base de
datos transaccional a la histórica.
Internal Channel / External Channel:
En este modelo solo se hace referencia a estos canales que son los de
interacción del cliente.
ZENDESK:
Se actualiza el estado del caso de reembolso en Zendesk una vez se cierre
el ciclo de pago de este.
14
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
MOZART:
Este sistema envía la solicitud de pago de reembolso al PIC una vez la misma
esté debidamente aprobada. Además, recibe la debida notificación para
cambio de estado del reembolso una vez se aplica.
SAP4HANA:
Se usan las mismas integraciones con SAP que han estado funcionando para
el sistema de reembolsos RTS.
Por otra parte, se crea una nueva interfaz que desde SAP envía la
información de bancos por país para que el PIC pueda tenerlos disponibles
para las consultas que requiere el orquestador de reembolsos.
3. RECOMENDACIONES ANTES DE LA INSTALACIÓN
• Se recomienda que antes de la instalación se cuente con un backup a nivel
de componentes en caso de requerirse posteriormente.
4. PUESTA EN AMBIENTE PRUEBAS O PRODUCCIÓN
Para el buen funcionamiento en el ambiente de producción se debe realizar
despliegue según solicitud en Mauro de los artefactos que desarrollo libere
en el ambiente de producción y ejecución de los scripts que correspondan.
4.1. Despliegue en ambiente de pruebas
Antes de iniciar el proceso de despliegue se debe realizar backup de los
artefactos que vamos a reemplazar y se dejan en …….
5. PROCESO DE ROLL BACK
El proceso de Roll Back corresponde al entregado por el equipo de desarrollo
quien entrega los script correspondientes a de acuerdo a la solicitud,
adicional se reemplazan los archivos que se hayan modificado.
6. PROCEDIMIENTO DE CONFIGURACIÓN
6.1. Configuración Hardware
No aplica
15
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
6.2. Configuración Software
7. GENERACIÓN DE NUEVOS DATOS
8. DESCRIPCIÓN DE LA FUNCIONALIDAD
Este sistema es desarrollado en AVIANCA para la administración del proceso
de pagos de reembolsos una vez estos estén aprobados.
Además, almacena información adicional del reembolso que es solicitada al
cliente y que está relacionada únicamente con el pago y que no es
almacenada ni requerida en ninguno de los otros sistemas participantes en
el proceso de reembolso.
En este sistema está también la parametrización de tipos de pago y
documentos o datos adicionales necesarios para realizar el pago de un
reembolso de acuerdo con su tipo.
Los servicios que requiere consumir de otros sistemas, así como la
exposición y consumo de sus servicios es a través del APIM de Avianca.
9. RELACIÓN CON OTROS SISTEMAS
El aplicativo tiene relación con los siguientes sistemas:
• AVIANCA.com: Canal Web principal de Avianca por el que podrán
hacerse solicitudes y consulta de Reembolsos. al momento es el canal
desarrollado por NewShore.
• MyAvianca: Aplicación móvil de Avianca por la que podrán hacerse
solicitudes y consulta de Reembolsos.
• LIFEMILES: Sitio Web de LIFEMILES, por donde los clientes que tienen
un programa de lealtad podrán hacerse solicitudes y consulta de
Reembolsos.
• AVIAJAR: Los colaboradores de Avianca y las personas que tienen
paquetes de beneficios de vuelos, podrán hacer solicitudes y seguimiento
de sus casos por el sitio web de AVIAJAR.
• AVC: Mediante la solución de administración de viajes en servicio podrán
solicitarse los reembolsos y hacer tracking de los mismos.
16
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• Avianca Trade: Portal de centralización de solicitudes de servicio de
agencias NDC B2T y ARC.
• MyIdTravel Utility: La utilidad de MyIdTravel generará la información
requerida para ingresar las solicitudes de reembolsos de colaboradores
de otras aerolíneas que viajan con Avianca bajo los convenios de tiquetes
ZED.
• Special Refunds: Nueva solución interna de Avianca para ingreso de
casos especiales de reembolsos como clientes VIP o procesamiento de
lotes de reembolsos mediante archivos.
• BSP Link: Canal de gestión de ventas de agencias diferentes a NDC B2T
y ARC.
• RAPID20: Sistema SaaS de manejo de Revenue Accounting, donde se
harán actualizaciones de estado de tiquetes reembolsados por AVIANCA.
• MOZART: Sistema SaaS que manejará toda la información del reembolso
como tal, recibiendo los casos solicitados, administrándolos de acuerdo
con las definiciones funcionales, y permitiendo entre otras el seguimiento
de los casos y el manejo de operaciones especiales sobre los reembolsos
ejecutadas por el equipo de la Central de Reembolsos de Avianca.
• AVRefund: Este nuevo sistema permite recibir recurrentemente la
información que se genera en Mozart de los casos de reembolsos, para
seguimiento y alimentación de otros sistemas internos de Avianca.
• Refund Orq Rules: este nuevo sistema almacena y permite la
actualización de reglas requeridas para el orquestamiento que realizará
la capa media de Avianca durante los procesos de Reembolsos.
• Avianca Middelware: La capa media de AVIANCA (APIM e ESB) permite
el desarrollo de los orquestamiento y exposición de servicios de
integración requeridos para el proceso de reembolsos y la comunicación
entre los diferentes sistemas participantes en el proceso.
• SAP4HANA: Sistema ERP de Avianca, encargado de llevar la
contabilidad y ejecución del pago de reembolsos en cash a cuentas
bancarias.
17
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• AMADEUS: AMADEUS PSS se realiza consultas de información de
tiquetes y reservas requeridas para el proceso de reembolsos, y para
actualizar su información una vez reembolsados.
• CHARGEBACK: El Sistema de contracargos de Avianca es consultado
en diferentes partes del proceso para validar que no existan solicitudes
del cliente mediante esta solución y se termine generando doble pago.
• SBR: Sistema interno de Avianca que maneja la información de las ventas
realizadas, a partir de la información que recibe recurrentemente de
AMADEUS. Durante el proceso será requerido en algunos momentos
acceder a esta información para complementar datos requeridos del
reembolso.
• REVAP: Sistema interno de AVIANCA que maneja toda la informacion
generada por los procesos de revenue accounting desde RAPID20. Será
consultado en algunas ocasiones para complementar la información
requerida para los reembolsos.
• LIFEMILES PAYMENT: Sistema de pagos de LIFEMILES al que se
enviará la información de pagos de casos de reembolsos que deban ser
pagados en millas.
• DEAL ENGINE: Este es otro de los sistemas importantes de esta
solución. Encargado de entregar la información de los cálculos detallados
de los valores que aplican para el pago de un reembolso.
• ZENDESK: El sistema de AVIANCA para administración de casos de
requerimientos de Clientes, será parte fundamental para el proceso de
reembolsos, teniendo en cuenta que aquí se llevará el control de
seguimiento de los casos de reembolsos solicitados por los clientes y será
el canal principal de consulta para la mesa de ayuda de AVIANCA.
• CRM Dynamics: En este sistema se encuentra la información de relación
IATA-CANAL DE ATENCIÓN, requerida por para el cálculo de los valores
detallados del reembolso.
• FHELIA: Sistema de facturación electrónica de Avianca, donde se
crearán las facturas asociadas al pago de comisiones adicionales
requeridas en algunos casos para el pago de los reembolsos.
18
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
10. INGRESO AL SISTEMA
Para el ingreso al Integrador de Pagos ingresamos al siguiente link de QA:
https://azwapppiccustfrontuseqa.az-asev3-use-
qa.appserviceenvironment.net/auth
Al dar clic en iniciar sesión se debe autenticar con Directorio Activo de Azure,
debe elegir o escribir su correo que están en Microsoft.
19
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: Lo anterior se agrega de acuerdo con el PBI 612328 Crear home de la
aplicación Integrador de Pagos.
10.1. Inactivación de Usuario
Los usuarios que no hayan iniciado sesión en los últimos 90 días serán
inactivados automáticamente, para mantener la seguridad y limpieza de la
base de datos.
Con la function de inactivación az-fapp-picpaystatus-use-qa
De acuerdo a los parámetros configurados para la inactivación de usuario.
select * from [master].[MST_PARAMETERS] where parameter_code in
('PRE_INACTIVATION_NOTIFICATION',
'SUBJECT_EMAIL_INACTIVATION_NOTIFICATION',
'TEMPLANE_NAME_INACTIVATION_NOTIFICATION',
'USER_INACTIVITY_DAYS')
20
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se enviará una notificación a los usuarios próximos a inactivar cuando
hayan cumplido 80 días sin ingreso.
SELECT [email], [FIRST_NAME] + ' ' + [LAST_NAME], [last_login_date] AS [NAME]
FROM [adm].[MST_USER]
WHERE DATEDIFF(DAY, [last_login_date], GETDATE()) = 80;
La notificación seria la siguiente:
Cuando la function se ejecuta inactiva los usuarios que cumplen con el
tiempo establecido de no ingreso por 90 días
SELECT * FROM [adm].[MST_USER] order by last_login_date asc
Se observa en el log, los usuarios inactivados
21
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
SELECT * FROM [rfd].[PIC_LOGS_TRANSACTION]where
created_user='PIC_DEACTIVITY_USER' order by created_DATE asc
Nota: Lo anterior es de acuerdo al PBI 982297 Refund - Inactivación Automática de Usuarios Cada 90 Días. Parte
II [Final]
10.2. Descripción del perfil de usuario
A continuación, se presenta un resumen con los principales accesos.
11. MÓDULOS
Para la administración y gestión del Integrador de Pagos – PIC, se manejan diversos
menús para cada proceso, los cuales se detallarán a continuación.
11.1. PROCESOS
11.1.1. Pagos RTS
Las plantillas a cargar en este menú son las que se descargan desde RTS.
Mencionado en el Manual de RTS “Plantillas de Cargue para PIC” MANUAL DE
APLICACIÓN RTS.docx
11.1.1.1. Plantilla de Pago para Tarjeta de Crédito (Pago por Primera Vez)
22
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
11.1.1.2. Plantilla de Pago para Voucher (Pago por primera vez))
Para esta plantilla se ha creado un parámetro llamado
TOLERANCE_MARGIN_FOR_TEMPLATES configurable para el Margen de
tolerancia.
En el que el valor 1.005 es igual a 0.005 ya que 0.005 es el % de tolerancia que se
solicitó.
SELECT * FROM [master].[MST_PARAMETERS] where parameter_code =
'TOLERANCE_MARGIN_FOR_TEMPLATES'
23
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se carga la plantilla de Pago en PIC
Se inserta en la tabla inicial
24
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se da clic en procesar
25
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se procesa la información llenando las tablas temporales y pasando a las otras
tablas, FOP, request
26
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se observa el correo con la confirmación de lo cargado y procesado
Para los registros que superaron el margen de tolerancia de 0.005 se realizó el
rollback
27
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se confirma y se cumple lo solicitado para los escenarios
Se aplica un control que modifica la llave primaria agregando el tiquete como parte
de la llave adicional al Transaction Unique ID.
La agrupación de pagos se mantendrá únicamente por Transaction Unique ID para
aquellos registros que superen esta validación.
Para el siguiente escenario:
En la primera carga, se incluye uno o más registros que tienen el mismo número
de solicitud, pero con tiquetes diferentes. Todos comparten la misma tarjeta y el
mismo approvalCode. Estos registros fueron enviados a pagos manuales. En la
notificación salen los casos cargados en este archivo de 1era carga.
28
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
En una segunda carga, se vuelve a cargar la misma solicitud, pero con un tiquete
diferente. También se utiliza la misma tarjeta y el mismo approvalCode. Esta vez,
la solicitud fue procesada como pago automático. El sistema deja en estado "P"
únicamente el tiquete cargado en ese momento, incluso si comparte el
mismo transactionUniqueId con otros registros en otras cargas. Al notificar solo
muestra los casos cargados en ese momento
Nota: Lo anterior se agrega de acuerdo a los PBIs
914437 PIC - [Salida Temprana] Control de Reembolso en PIC Basado en Porcentaje de Incertidumbre
Configurado.
1014441 PIC - Modificación de la llave para Validaciones en el PIC sin afectar el Pago
11.1.1.3. Plantilla de Pago para Voucher (Pago por Primera Vez)
11.1.1.4. Plantilla para Actualización de Datos (Voucher))
29
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
11.1.2. Plantillas de pago
Este módulo permite descargar las plantillas de pago manuales, después del cargue
y notificación de Pagos RTS. En este módulo se descarga por plantilla
correspondiente a lo cargado (Santander, Otros pagos Manuales, Cielo, BAC
Regional, Credibanco y Redeban).
Se tiene el parámetro 'GET_INFO_SALE_CAPTURE_IN_TRANSACTION' para
almacenar una lista de estados de transacción. Este parámetro permitie definir los
estados que se considerarán como exitosos para el proceso de captura de la
transacción
Se valida con el api Get Info Sale en el nodo "info-capture" en el campo “capture-
status"
Para las notificaciones se tienen los parámetros:
select * from [master].[MST_PARAMETERS] where parameter_code in
(‘EMAIL_NOTIFICATION_DOWNLOAD_TEMPLATE_FAILED’,
‘EMAIL_NOTIFICATION_DOWNLOAD_TEMPLATE_RESULT’)
30
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Procesos >> Plantillas de Pago.
Este menú realiza el descargue en un proceso que se ejecuta en background y de
esta manera se permite que el usuario continúe en PIC sin ver afectadas sus tareas,
el proceso debe enviar la plantilla generada a los correos que se encuentren
parametrizados en el campo EMAIL_NOTIFICATION_DOWNLOAD_TEMPLATE_RESULT de
la tabla [master].[MST_PARAMETERS].
Al no tener valores en el campo parametrizado para los correos, sólo debe enviarse
el correo con la plantilla a la persona que ejecutó la solicitud.
En la tabla MST_PAYMENT_PROCESS_WAY] se tiene la configuración de
procesamiento de pago de reembolsos. En esta tabla se configura si se toma el
proceso Automático o Manual, y si es manual en que plantilla se descarga.
31
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se tiene un procedimiento almacenado que valida la forma de proceso de pago
aplicada una “A” o una “M” o una “O” teniendo en cuenta que:
• El valor que debe retornar el procedimiento en el campo forma de proceso de
pago “A” que indica que es automático.
• “M” que indica que es manual.
• “O” que indica que es manual por datos incompletos para el pago o que no se
encontró en la tabla de forma de proceso de pago. (Plantilla Otros).
select * from [master].[MST_PAYMENT_PROCESS_WAY]
Y para la descarga de las plantillas se debe de cumplir las reglas configuradas en
la siguiente tabla SELECT * FROM [rfd].[PIC_TEMPLATE_CONFIG_DOWNLOAD]
32
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al descargar una plantilla queda alojada en la tabla Select * from
[rfd].[PIC_LOG_RECORDS_CONTAINET_FILE] si se requiere volver a descargar un registro de
la plantilla solo Se elimina el registro de la tabla y se puede volver a descargar.
Las iniciales del campo File_id significan lo siguiente:
• TD Descarga
• TU Carga de resultados
• TUP Carga posterior al pago
Adicional se tiene un Blob Storage azstacpiccustuseqa >> descarga-plantillas-
manuales en el que se guardan las plantillas descargadas.
Se debe validar que las plantillas se encuentren correctamente configurada en las
siguientes tablas
select * from [master].[MST_PAYMENT_PROCESSOR]
select * from [master].[MST_PAYMENT_PROVIDER]
select * from [rfd].[PIC_TEMPLATE_CONFIG_DOWNLOAD]
select * from [master].[MST_PAYMENT_PROCESS_WAY]
select * from [rfd].[PIC_CONTROL_DOWNLOAD_TEMPLATE_MANUAL_PAYMENT]
select * from [rfd].[PIC_LOG_EVENT_FILE] order by 1 desc
select * from [rfd].[PIC_LOG_RECORDS_CONTAINET_FILE]
33
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
En la tabla [rfd].[PIC_TEMPLATE_CONFIG_DOWNLOAD] el parámetro
“Procesador” es para confgurar los procesadores que NO aplican.
Nota: Lo anterior se agrega de acuerdo con los PBIs:
• 660695 PIC - Ajuste 6, TM. y Procedimiento para aplicar reglas de proceso automático o manual de pago de
reembolsos. Parte I
• 968945- PIC - [E2E] - Auste al servicio de procesamiento TC - Captured. Parte II [Final])
• 968937 PIC - Proceso en Background para Descarga de Plantillas de Pago
• 1150188 [PIC] Dejar reporte en blobstorage
A continuación, se relaciona el menú por plantilla de pago.
Para descargar las plantillas manuales para todas (excepto Otras), en la
SALE_REPOSITORY debido a que solo se almacena un Approval code se actualiza
la llave de búsqueda a PNR + REFUND REQUEST + (STATUS = V), para
garantizar que se descarguen todos los registros. Los registros con un status
diferente a "V" no se incluyen en la plantilla.
Nota: Lo anterior se agrega de acuerdo con los siguientes PBIs:
34
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• 1215537 PIC - Ajuste Descarga Plantillas de Pago - Llave
11.1.2.1. BAC Regional
Para descargar datos de BAC Regional debe cumplir con los parámetros mencionados en el item
Plantillas de pago y adicional siempre debe de existir el registro en las siguientes tablas:
select * from [rfd].[pic_fop_payment_request]
select * from [rfd].[pic_payment_request]
select * from [rfd].[pic_sale_repository]
Al dar clic en Descargar, Se mostrará el pop-pup de confirmación de generación
de plantilla
.
Y se recibirá un correo con la plantilla para descargar.
35
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se descarga plantilla y se observa que se relacionan todos los registros, incluso
en escenarios donde hay 2 TC asociadas a la misma reserva.
Se mostrará en el log la información de la plantilla descargada.
Si la plantilla no generó información, se muestra un pop-up informando que no se
tienen registros para dicha plantilla.
Si el pago debe realizarse en moneda USD y si el procesador de pagos no
corresponde a CPD o Worldpay o Yuno debe ir por el flujo de pago por BAC
Regional.
• El estado debe ser igual a Validado
• La forma de proceso es Automático
• La moneda del reembolso es en USD
• el procesador de pagos debe ser "BAC"
36
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Campos de la plantilla:
Campo Descripción
Identificador único
de transacción
Tipo Indentificador de transacción generado por el PIC
Campo utilizado para el cargue de resultados.
valor constante “Devolucion”
Terminal Para determinar el valor a enviar de este campo ir al
Requerimiento 6
Tarjeta Fecha de
vencimiento
Valor actual recibido desde la solicitud de reembolso.
Ejemplo: 998877XXXXX4433
formato MMYY. Si viene vacía entonces se envía de forma
predeterminada el valor "1226" Tabla
[rfd].[PIC_FOP_PAYMENT_REQUEST]
Monto Suma total correspondiente a valor de reembolso por cada
tkt perteneciente a la misma transacción (transaction unique
id). El carácter separador decimal es punto. La longitud es
(12,2) de tipo decimal.
Referencia Boleto Correlativo Aerolínea Corresponde al número de tkt. Extraer los últimos 10
caracteres. Es de tipo Number de longitud 10.
Corresponde al número de transacción único del PIC
(Transaction Unique ID)
Es de tipo Number y de longitud 3. (airline-code)
Requerimiento 6: Lógica para obtener la Terminal de la tabla Relación
Afiliados
Para enviar el valor correspondiente al campo terminal, el servicio debe consultar
en la tabla de “Relación Afiliados” enviando los siguientes parámetros:
• Franquicia. Corresponde al código de la franquicia de longitud 2 de tipo string.
• Aerolínea. Corresponde al código de la aerolínea de longitud 3 de tipo numérico
La consulta debe retornar el valor correspondiente a la columna Terminal como se
muestra en la siguiente a continuación:
Franquicia Terminal Afiliado Aerolínea
CA TACAPN01 92691608 202 o 547
VI TACAPN01 92691594 202 o 547
AX TACACR01 77436421 202 o 547
DS TACACR01 77436421 202 o 547
DC TACACR01 77436421 202 o 547
37
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
AX LACSAREE 70304384 133
VI LACSAREE 70304384 133
CA LACSAREE 70304384 133
VI AVIAPN01 94273307 134
CA AVIAPN01 94273323 134
AX AVIACR01 73655498 134
DS AVIACR01 73655498 134
DC AVIACR01 73655498 134
El nombre del archivo debe tener la siguiente estructura prestablecida:
BAC_REGIONAL_ YYYYMMDD_HHmm.xlsx
La fecha y hora corresponde al actual en el momento de crear el archivo.
Nota : Lo anterior se agrega de acuerdo al PBI:
• 715271 PIC - Recepción BAC Regional
• 755792 PIC - Construcción de Layout BAC a partir de la generación de Plantillas Manuales
• 1215537 PIC - Ajuste Descarga Plantillas de Pago – Llave
11.1.2.2. Sin Captura
La plantilla Manual sin captura está basada en una lista de Transaction Unique ID
para facilitar el seguimiento y la gestión de dichas transacciones y que esta pueda
ser cargada en RTS para actualizar los registros.
Para cada Transaction Unique ID proporcionado, el procedimiento para los casos
de RTS verifica que los registros de la transacción estén marcados como "F"
Para los casos de la E2E (numéricos)
(comparando con el parámetro ya configurado). Se aplica los siguientes ajustes si
el estado es diferente al configurado en el parámetro
“GET_INFO_SALE_CAPTURE_IN_TRANSACTION” debe venir en la get info sale
en el campo “capture-status”
.
El estado debe mantenerse como "V".
El registro deberá actualizarse a "M".
Se debe poblar el campo de la Plantilla manual (campo: "Template" de la Payment
request) con una plantilla configurada como "CAP" (esta plantilla debe ser
configurada en la Tabla Maestra). - Nombre: (Registros sin Captura) - Con los
mismos datos que en salida temprana y para registros numéricos debe excluir el
38
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
registro de la plantilla del procesador que si correspondía, por ejemplo, ingresa un
registro ABC, catalogado como CBD (Credibanco), y su estado es diferente a
capturado, este registro no deberá mostrarse en la plantilla CBD pero si en la CAP
independiente del procesador (NO deberá validar el procesador en el Sale
Repository)
Con los registros que superen la validación anterior se genera una plantilla
que tiene la siguiente estructura para cada transacción rechazada:
Campo Descripción
Ctl num Número generado a partir del 6to carácter del campo refund request.
Station Los primeros 5 caracteres del campo refund request.
Ticket Los 10 últimos dígitos del campo ticket de la transacción.
Car num Los primeros 3 dígitos del campo ticket de la transacción.
Comentario
Valor almacenado en el campo REJECTION_REASON de la tabla
PIC_PAYMENT_DETAIL
Codigo solucion Default "12"
El documento se debe llamar “Transacciones sin captura_YYYYMMDD"
inicialmente estaba en csv pero ahora es en xlsx. “pendiente de pbi donde se cambió
la extensión”
Nota: Lo anterior se agrega de acuerdo con los PBIs
• 872852 PIC - [Salida Temprana] Ajuste al Get Info Sale y al botón Procesar
• 872860 PIC - TC - [Salida Temprana] Crear Plantilla Transacciones sin captura para cargar en RTS (CSV)
• 884456 PIC - [Salida Temprana] - Manejo del Nodo Lifemiles & Plantillas de Rechazo Salida Temprana
• 968945 PIC- [E2E] - Ajuste al servicio de procesamiento TC - Captured. Parte II [Final]
• 991635 PIC - INC7327808 - Correccion en notificacion para los rechazados por ciclo de venta incompleto
11.1.2.3. Cardinal
Para descargar datos de Cardinal debe cumplir con los parámetros mencionados en el item Plantillas
de pago y adicional siempre debe de existir el registro en las siguientes tablas:
select * from [rfd].[pic_fop_payment_request]
select * from [rfd].[pic_payment_request]
select * from [rfd].[pic_sale_repository]
39
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al dar clic en Descargar, Se mostrará el pop-pup de confirmación de generación
de plantilla
.
Y se recibirá un correo con la plantilla para descargar.
Se descarga plantilla y se observa que cuando se tiene más de un tkt con el
mismo transaction y aproval este se agrupa
40
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Si la plantilla no generó información, se muestra un pop pup informando que no se
tienen registros para dicha plantilla.
Si el procesador seleccionado es Cardinal, el sistema debe ejecutar una consulta
en la base de datos del PIC con las siguientes condiciones para obtener las
transacciones para pago que deben ser insertadas en el archivo:
• La forma de pago es “TR” tarjeta de crédito
• El proceso de pago es manual “M”
• La moneda de pago del reembolso es “USD”
• La franquicia es American express “AX” o VISA “VI”
• El estado debe ser “Validado” el cual indica que está listo para enviar a pago.
El sistema genera un archivo Excel (*.xlsx) insertando el resultado de la consulta
anterior sin encabezado con el siguiente orden de columnas:
Campo Descripción
Identificador único
de transacción Indentificador de transacción generado por el PIC
refund se envía el valor constante "refund"
Monto del
reembolso
Asociado a la transacción (Agrupado por transaction Unique
ID)
La separación de decimal sería por (,) siempre dos decimales,
sin embargo, para entero no se relacionarían decimales
Longitud (18,2)
El monto para reembolsar debe ser igual a la suma montos
liquidados por tique o emd agrupando por el transaction unique
ID.
El valor del reembolso no debe ser mayor al valor de la venta.
Si es mayor, debe conservar la forma de pago manual y en un
estado que permita gestionarse desde el tablero de control de
Medios de Pago para autorizar el pago de acuerdo con el
PBI #690868
Transaction ID Identificador de la transacción de la compra obtenido del
repositorio de ventas
41
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Deben generarse 2 archivos en formato Excel (*.xlsx) diferenciados por franquicia.
Uno para American Expres y otro con VISA. No deben mezclar los registros de
ambas franquicias en un archivo.
El nombre del archivo generado debe tener la siguiente estructura prestablecida si
el conjunto de registros pertenece a la franquicia American Express PLANTILLA
CARDINAL AX_YYYYMMDD_HHmm, ejemplo: PLANTILLA CARDINAL
AX_20240603_1301.xlsx
El nombre del archivo generado debe tener la siguiente estructura prestablecida si
el conjunto de registros pertenece a la franquicia VISA PLANTILLA CARDINAL
VI_YYYYMMDD_HHmm,
Nota : Lo anterior se agrega de acuerdo al PBI:
• 697814 PIC - Plantilla para pagos Manuales por tarjeta de crédito. Back – Cardinal
• 1215537 PIC - Ajuste Descarga Plantillas de Pago – Llave
11.1.2.4. Credibanco
Para descargar datos de Credibanco debe cumplir con los parámetros mencionados
en el item Plantillas de pago y adicional siempre debe de existir el registro en las
siguientes tablas:
select * from [rfd].[pic_fop_payment_request]
select * from [rfd].[pic_payment_request]
select * from [rfd].[pic_sale_repository]
Si el procesador seleccionado es Credibanco, el sistema debe ejecutar una consulta
en la base de datos del PIC con las siguientes condiciones para obtener las
transacciones para pago:
1. 2. 3. 4. 5. La forma de pago es “TR” tarjeta de crédito
El proceso de pago es manual “M”
La moneda de pago del reembolso es “COP”
franquicia es American express “AX” o VISA “VI”
El estado debe ser “Validado” el cual indica que está listo para enviar a pago
42
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al dar clic en Descargar, Se mostrará el pop-pup de confirmación de generación
de plantilla
Y se recibirá un correo con la plantilla para descargar.
Se descarga plantilla y se observa que cuando se tiene más de un tkt con el
mismo transaction y aproval este se agrupa
En caso de que aplique se recibe dos archivos uno de Reembolsos Totales y otro
de ajustes parciales.
43
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Debe generarse dos archivos CSV (*.csv) independientes.
Uno que contendrá los registros de transacciones para pagos parciales y otro para
pagos totales.
Si el Saletotalamount (Del payment database en caso de que el valor exista aquí) =
Valor del Reembolso, debe caer en la plantilla “Ajustes Totales Y Parciales
DDMMYYYY_HHmm.csv,” pero si el Valor del Reembolso es menor al
Saletotalamount debe caer en la plantilla "Reembolsos Totales
DDMMYYYY_HHmm.csv"
El sistema debe generar cada archivo insertando el resultado de la consulta anterior
sin encabezado usando el caracter punto y coma ";" como separador de columnas
El nombre del archivo generado para reembolsos parciales debe tener la siguiente
estructura prestablecida Ajustes Totales Y Parciales DDMMYYYY_HHmm.csv.
Los campos de los archivos son:
Ajustes Totales Y Parciales
Campo Descripción
transaction_unique_id Campo utilizado para el cargue de resultados
Número de Autorización Corresponde al número de aprobación - approval_code
Fecha de venta issue_date viene de mozart - YYYYMMDD
Número de tarjeta Cuatro últimos dígitos de la tarjeta - cardNumber
Para el monto para reembolsar debe agrupar por transaction unique ID. El
monto debe ser menor a la transacción de la venta (obtenido del repositorio
de ventas) refund_amount_pnr
Monto a reembolsar
Sin decimales. Si se encuentra con decimal debe aproximarse (de 0.5 inclusive
para arriba se aproxima al siguiente número mayor y si es menor de 0.5 para
abajo se aproxima al entero más bajo)
No aplica Valor prestablecido y constante "NO"
No aplica Valor prestablecido y constante 0 (Cero)
No aplica Valor prestablecido y constante 0 (Cero)
44
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
No aplica Valor prestablecido y constante 0 (Cero)
No aplica Valor prestablecido y constante 0 (Cero)
No aplica Valor prestablecido y constante 0 (Cero)
No aplica Valor prestablecido y constante 0 (Cero)
No aplica Valor prestablecido y constante 0 (Cero)
No aplica Vacío
Usuario pagador
autorizado de Avianca Correo del usuario pagador, del parámetro TEMPLATE_CREDIBANCO_EMAIL
No aplica Vacío
No aplica Valor prestablecido y constante "SI"
Reembolsos Totales
Campo Descripción
transaction_unique_id Campo utilizado para el cargue de resultados
Número de Autorización Corresponde al número de aprobación - approval_code
Fecha de venta issue_date viene de mozart - YYYYMMDD
Número de tarjeta Cuatro últimos dígitos de la tarjeta - cardNumber
Monto a reembolsar agrupado por transaction unique ID. El monto debe ser
igual a la transacción de la venta (obtenido del repositorio de ventas)
Monto para reembolsar
Sin decimales. Si se encuentra con decimal debe aproximarse (de 0.5 inclusive
para arriba se aproxima al siguiente número mayor y si es menor de 0.5 para
abajo se aproxima al entero más bajo)
Monto total de la
transacción de venta Monto total obtenido del repositorio de venta
No aplica Valor prestablecido y constante 0 (Cero)
No aplica Valor prestablecido y constante 0 (Cero)
No aplica Valor prestablecido y constante 0 (Cero)
No aplica Valor prestablecido y constante 0 (Cero)
No aplica Vacío
Nota : Lo anterior se agrega de acuerdo al PBI:
• 697832 PIC - Plantilla para pagos Manuales por tarjeta de crédito. Credibanco Parte I.
• 866058 PIC - Ajuste [Salida Temprana] Pantallas de Descargue de plantillas
• 911024 PIC - Ajuste Plantilla para pagos Manuales por tarjeta de crédito. Credibanco
• 1215537 PIC - Ajuste Descarga Plantillas de Pago – Llave
11.1.2.5. Cielo
Para descargar datos de Cielo debe cumplir con los parámetros mencionados en el item Plantillas
de pago y adicional siempre debe de existir el registro en las siguientes tablas:
select * from [rfd].[pic_fop_payment_request]
select * from [rfd].[pic_payment_request]
select * from [rfd].[pic_sale_repository]
45
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Si el procesador seleccionado es Cielo, el sistema debe ejecutar una consulta en la base de datos
del PIC con las siguientes condiciones para obtener las transacciones para pago que deben ser
insertadas en el archivo:
1. 2. 3. 4. La forma de pago es “TR” tarjeta de crédito
El proceso de pago es manual “M”
La moneda de pago del reembolso es “BRL”
El estado debe ser "Validado" el cual indica que está listo para enviar a pago
Si el procesador seleccionado es Cielo, el sistema debe generar un archivo Excel (*.xlsx) insertando
el resultado de la consulta anterior con el siguiente encabezado y orden de columnas:
Al dar clic en Descargar, Se mostrará el pop-pup de confirmación de generación
de plantilla
Y se recibirá un correo con la plantilla para descargar.
Se descarga plantilla y se observa que cuando se tiene más de un tkt con el
mismo transaction y aproval este se agrupa
46
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Los encabezado del archivo son:
Encabezado en
portugués Característica del campo
ESTABELECIMENTO Código único que identifica a Avianca ante el procesador Cielo. Valor constante
1064518866
LOTE Campo vacío
DT DEPÓSITO issue_date Fecha de venta
La tarjeta es truncada y depende de cómo se encuentre en el repositorio de venta.
Hay casos en los que el truncado corresponde a los 6 primeros dígitos + XXXXXX + 4
CARTÃO / XID
últimos dígitos
Cuando es american express amex vienen 5 'X'
Se obtiene del repositorio de venta.
DT VENDA issue_date Fecha de venta
Valor total de la transacción de la venta. Depende de cómo se encuentre en el repositorio
de venta.
VL VENDA
Conservar el punto "." como separador de miles y con coma "," para el separador de
decimales. Longitud: (10, 2)
Valor del reembolso.
El monto para reembolsar debe ser igual a la suma montos liquidados por tkt o emd
agrupando por el transaction unique ID.
El valor del reembolso no debe ser mayor al valor de la venta.
Para los casos que sea mayor, corresponde a un reembolso total siempre que la diferencia
VL CANCELAR
debe ser menor a 1BRL y debe ser calculado por el PIC ajustando el valor a reembolsar
igual al valor de la venta.
Si es mayor a 1BRL, debe conservar la forma de pago manual y en un estado que permita
gestionarse desde el tablero de control de Medios de Pago para autorizar el pago de
acuerdo con el PBI #690868
AUT. Corresponde al código o número de aprobación. Se obtiene del campo approval_code
MOTIVO Se envía el identificador único del PIC, transaction unique id
El nombre del archivo generado tiene la siguiente estructura PLANILHA DE
CANCELAMENTO CIELO_YYYYMMDD_HHmm.xlsx
Nota : Lo anterior se agrega de acuerdo con el PBI:
697818 PIC - Plantilla para pagos Manuales por tarjeta de crédito. Cielo
• 1215537 PIC - Ajuste Descarga Plantillas de Pago – Llave
11.1.2.6. Redeban
47
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para descargar datos de Redeban debe cumplir con los parámetros mencionados
en el item Plantillas de pago y adicional siempre debe de existir el registro en las
siguientes tablas:
select * from [rfd].[pic_fop_payment_request]
select * from [rfd].[pic_payment_request]
select * from [rfd].[pic_sale_repository]
Las condiciones que deben cumplir los registros para que sean descargados en la
plantilla “Redeban” son las siguientes
1. 2. 3. 4. 5. La forma de pago es “TR” tarjeta de crédito
El proceso de pago es manual “M”
La moneda de pago del reembolso es “COP”
La franquicia es MasterCard "CA"
El estado debe ser “Validado” el cual indica que está listo para enviar a
pago
Al dar clic en Descargar, Se mostrará el pop-pup de confirmación de generación
de plantilla
Al dar clic en Descargar, se recibirá un correo con la plantilla para descargar.
48
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se descarga plantilla y se observa que cuando se tiene más de un tkt con el
mismo transaction y aproval este se agrupa
En caso de que aplique se recibe dos archivos uno de Ajustes Totales y otro de
ajustes parciales.
El archivo se descarga en formato *.csv, donde cada columna está separado por
punto y coma (;) y sin encabezado.
El final de cada línea no tiene carácter punto y coma (;) y ningún otro exceptuando
el salto de línea.
El máximo de registros insertados por archivo no debe ser superior a 500. Si la
consulta genera un resultado con una cantidad mayor a 500 registros, el sistema
genera tantos archivos como sean requeridos para incluir la cantidad total de
registros obtenidos de la consulta.
Se genera dos archivos independientes. Uno con los registros de transacciones
para pagos parciales y otro para pagos totales.
Para saber en cual archivo asignar la transacción para pago se verifica si el monto
a reembolsar agrupado por el identificador de transacción es menor al monto de la
transacción de venta (Obtenido del repositorio de venta), corresponde a un monto
parcial y se almacena en el archivo correspondiente a montos parciales.
49
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
totales.
Si el monto es igual, el registro se almacena en el archivo correspondiente a montos
La estructura de nombre del archivo para reembolsos parciales es
"Formato_ajustes_parciales DDMMYYYY_HHmm_#.csv", donde el caracter #
corresponde a un consecutivo asignado al archivo para indicar el número de
archivos generados cuando la cantidad de registros de la consulta es mayor a 500,
ejemplo: Formato_ajustes_parciales 21122023_2400_1.csv
REDEBAN - AJUSTES PARCIALES
Campo Descripción
Identificador único de
transacción Indentificador de transacción generado por el PIC
Merchant Código único que identifica a Avianca ante el procesador Redeban. Se
obtiene del repositorio de venta
Fecha de venta Corresponde a la fecha de venta (issue date, enviado por mozart).
Formato: YYYY-MM-DD
Tarjeta de crédito Corresponde a los 4 últimos dígitos de la tarjeta (enviado por mozart)
Para el monto para reembolsar debe agrupar por transaction unique ID.
El monto debe ser menor a la transacción de la venta (obtenido del
Monto total de venta
repositorio de ventas)
Monto total de la venta sin decimales y sin caracteres de separación de
miles
Código/Número de aprobación Valor obtenido de Mozart. Viene en el campo approval_code
Debe ser la resta del valor total de la venta menos el del monto a
reembolsar.
Debe usarse el siguiente cálculo: Saletotalamount (Si se encuentra en la
tabla [PIC_SALE_REPOSITORY] deberá tomarse el campo value, de lo
Monto Parcial para Reembolsar
contrario deberá tomarse de la tabla [PIC_PAYMENT_REQUEST] del
campo SALE_TOTAL_AAMOUNT) - la sumatoria del Refundamount de
todos los registros del mismo transaction Unique ID. (Tabla Payment
Requets)
Valor prestablecido y constante 0 (Cero)
REDEBAN - AJUSTES TOTALES
Campo Descripción
Identificador único de
transacción Identificador de transacción generado por el PIC
Merchant Código único que identifica a Avianca ante el procesador Redeban. Se
obtiene del repositorio de venta
Fecha de venta Corresponde a la fecha de venta (issue date, enviado por mozart)
formato: YYYY-MM-DD
Tarjeta de crédito Corresponde a los 4 últimos dígitos de la tarjeta (enviado por mozart)
50
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para el monto para reembolsar debe agrupar por transaction unique ID.
El monto debe ser menor a la transacción de la venta (obtenido del
Monto
repositorio de ventas)
Monto total de la venta sin decimales y sin caracteres de separación de
miles
Código/Número de aprobación Valor obtenido de Mozart. Viene en el campo approval_code
Nota: Lo anterior se agrega de acuerdo con los PBIs:
• 697836 PIC - Plantilla para pagos Manuales por tarjeta de crédito. Redeban
• 866058 PIC - Ajuste [Salida Temprana] Pantallas de Descargue de plantillas
• 909760 PIC - [Salida Temprana] Ajuste Plantilla para pagos Manuales por tarjeta de crédito. Redeban
• 1215537 PIC - Ajuste Descarga Plantillas de Pago – Llave
11.1.2.7. Santander
Para descargar datos de Santander debe cumplir con los parámetros mencionados
en el item Plantillas de pago y adicional siempre debe de existir el registro en las
siguientes tablas:
select * from [rfd].[pic_fop_payment_request]
select * from [rfd].[pic_payment_request]
select * from [rfd].[pic_sale_repository]
1. 2. 3. 4. 5. La forma de pago es “TR” tarjeta de crédito
El proceso de pago es manual “M”
La moneda de pago del reembolso es “MXN”
La franquicia es American Express “AX” o Visa “VI” o MasterCard "CA"
El estado debe ser “Validado” el cual indica que está listo para enviar a pago
51
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
de plantilla
Al dar clic en Descargar, Se mostrará el pop-pup de confirmación de generación
Se descarga plantilla y se observa que se relacionan todos los registros, cuando se
tiene más de un tkt con el mismo transaction y aproval este se agrupa.
52
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
de columnas:
El sistema genera un archivo Excel (*.xlsx) con encabezado y el siguiente orden
Campo Descripción
Identificador único de
transacción Indentificador de transacción generado por el PIC
Fecha de venta Corresponde a la fecha de venta MM/DD/YYYY
Número de Afiliación valor constante: 9413394 parametrizable TEMPLATE_SANTANDER
Terminación de la tarjeta cuatro últimos dígitos de la tarjeta
Número de Autorización Debe obtenerse del repositorio de ventas
Número de operación vacío
Valor de la transaccion debe traerse del respositorio,
Importe de Venta
simbolo $ al inicio del valor
separador de mil con punto ".", separador de decimal con coma ","
Lo relacionado en el output de pago, simbolo $ al inicio del valor
separador de mil con punto "." separador de decimal con coma ","
Importe a devolver
El monto para reembolsar debe agrupar por transaction unique ID.
El monto debe ser menor a la transacción de la venta (obtenido del
repositorio de ventas)
Si la franquicia es American Express "AX" se debe generar un archivo individual
únicamente con registros de transacciones pertenecientes a la franquicia de AX. El
nombre del archivo generado tiene la siguiente estructura para la franquicia
American Express Layout Santander AX DDMMYYYY_HHmm.xlsx
Si la franquicia es Visa “VI” o MasterCard "CA" se debe generar un segundo archivo
únicamente con registros de transacciones pertenecientes a Visa “VI” o MasterCard
"CA". El nombre del archivo generado tiene la siguiente estructura para la franquicia
Visa “VI” o MasterCard "CA" Layout Santander VI-CA DDMMYYYY_HHmm.xlsx
Nota: Se agrega de acuerdo a los PBIs:
692544 PIC - Plantilla para pagos Manuales por tarjeta de crédito. Santander
866058 PIC - Ajuste [Salida Temprana] Pantallas de Descargue de plantillas
1215537 PIC - Ajuste Descarga Plantillas de Pago – Llave
11.1.2.8. Otros Pagos Manual
Las condiciones que deben cumplir los registros para que sean descargados en la
plantilla “Otros Pagos Manual” son las siguientes:
Las tablas relacionadas para estos registros son PIC_FOP_PAYMENT_REQUEST,
PIC_PAYMENT_REQUEST y PIC_SALE_REPOSITORY, adicionalmente los
tickets de los registros no deben contar con ChargeBack
53
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• Las solicitudes de reembolso con forma de pago tarjeta de crédito “TR” en
estado igual a Validado “V”
o La forma de proceso es manual “M”
o La moneda de pago del reembolso es diferente de COP, USD, BRL,
EUR, GBP, CAD, ARS, MXN, CLP
o El procesador de pago es diferente de Payflow “PYF”, “CPD”, Yuno
“YUN”, Credibanco “CBD”, Ingenico “ING”, Cielo “CIE”, BAC Regional
“BAC”, Redeban “RBM”, Transbank “TBK”, Worldpay “WPY”,
Santander “SNR”, Cardinal “CAR”,
• Las solicitudes de reembolso con forma de pago tarjeta de crédito “TR” en
estado igual a Validado “V”
o La forma de proceso es manual “O”
• Las solicitudes de reembolso con forma de pago tarjeta de crédito “TR” en
estado igual a Validado “V”
o El procesador de pago es Davivienda (de acuerdo con el PBI #732663)
o La moneda es COP
o La franquicia es DINERS Club "DC"
Proceso en PIC
Se accede al descargue de plantillas
Seleccionar Otros pagos manuales
54
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se Verifica el archivo descargado
55
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al abrir se observan los registros, se aclara que los registros provenientes del
procesador de pago DAVIVIENDA tienen una forma diferente de ser mostrados en
el archivo.
Para la plantilla “Otros Pagos Manuales” se adiciona los siguientes campos
• PNR: Sí el canal es 3 (BSPLink) se debe tomar del campo [PNR] de la tabla
[PIC_PAYMENT_REQUEST]. Sí el canal es diferente a 3 se debe tomar del
campo [PNR] de la tabla [PIC_SALE_REPOSITORY].
• CHANNEL:Campo CHANNEL de la tabla [rfd].[PIC_SALE_REPOSITORY] si
existe
• PSP: Campo PSP de la tabla [rfd].[PIC_SALE_REPOSITORY] si existe
• TRANSACTION_ID: Campo TRANSACTION_ID de la
tabla [rfd].[PIC_SALE_REPOSITORY] si existe
• COMENTARIO
• CAPTURED_STATUS: Campo CAPTURED_STATUS de la
tabla [rfd].[PIC_SALE_REPOSITORY] si existe.
• SOURCE: nombre asociado al código de acuerdo con las maestras Campo
[SOURCE] de la tabla [rfd].[PIC_PAYMENT_REQUEST].
• SUB_CHANNEL: nombre asociado al código de acuerdo con las maestras
Campo [SUB_CHANNEL] de la tabla [rfd].[PIC_PAYMENT_REQUEST].
56
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: Lo anterior se relaciona de acuerdo a los siguientes PBIs:
• 697838 PIC - Ajuste [Salida Temprana] Pantallas de Descargue deplantillas
• 732663 PIC - Cambiar flujo de plantilla de Davivienda para que se vaya como Manual (Otros)
• 866058 PIC - Ajuste [Salida Temprana] Pantallas de Descargue de plantillas
• 864096 PIC - [Salida Temprana] Ajuste Plantilla para pagos Manuales por tarjeta de crédito. (Manual) Otros - Ajuste
Control de Descarga
• 1148876 PI - [E2E] - Estados de pago - Modificación Plantilla Otros Pagos Manuales
• 1241083 PI – Países no integrados – Ajuste Plantilla “Otros Pagos Manual”
Ingresar a la Base de datos y consulta las tablas:
PIC_LOG_RECORDS_CONTAINET_FILE (Contiene los datos de la solicitud)
PIC_LOG_EVENT_FILE (contiene el registro con el evento del archivo en este caso
Download)
57
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con el PBI
778678 - PIC - Cambio Logs Auditoria #2
11.1.3. Cargue de Resultados
Este proceso se encarga de actualizar los estados de pago de las plantillas
manuales descargadas; para que el proceso se lleve a cabo a cada plantilla se le
adicionarán 3 columnas al inicio para establecer el estatus de la devolución y el
motivo de rechazo si fuera el caso, y el sistema debe reconocer las respuestas
proporcionadas para realizar el cierre de los casos, cada campo adicional será
manejado con las siguientes validaciones:
• Transaction ID: ID único de la transacción generado (Usado como llave)
• Status: Debe validarse que el status aquí ingresado sea únicamente (Paid
(P), reject (R)), en caso de que tenga un código diferente, el registro no
será procesado y arrojará el mensaje de error
• Reject Reason: Razon de rechazo
Esto aplica para todas las plantillas:
• Manual
• Redeban
• Santader
• Credibanco (Parcial)
• Credibanco (Total)
• Cielo
• Cardinal
Ejemplo del proceso:
58
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se usará una plantilla de Redeban parcial
El contenido de la Plantilla al ser descargada se observa de esta manera:
Como se informa al inicio para que sea leído se ingresan las 3 primeras columnas,
en este caso como la plantilla no lleva encabezados, se ingresa sin encabezados
e intencionalmente se ingresan campos erróneos.
Se ingresa al respectivo MENU
59
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para este caso se selecciona Redeban y al ser parcial se marca el respectivo
CheckButton de PARCIAL
60
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Cuando finaliza el proceso se recibe un correo con el archivo enviado, este correo
debe ser configurado en la tabla de parámetros [master].[MST_PARAMETERS] en
el parámetro llamado EMAIL_LOAD_FILE_MANUAL_REQUEST_OK
El correo que se recibe es el siguiente:
61
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al abrir el archivo que se encuentra adjunto en el correo se pueden observar las
columnas que indican si fue exitoso o los problemas que se presentar en el cargue
de un registro:
Se verifica que los registros que tuvieron una actualización exitosa se actualizaron
correctamente en las tablas
PIC_PAYMENT_REQUEST
62
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
PIC_PAYMENT_DETAIL
63
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
64
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se presenta mensaje de carga exitosa si la plantilla cumple las condiciones para la
carga.
El archivo cargado tiene la siguiente estructura.
En la carga se toman los 3 primeros campos
Ingresar a la Base de datos y consulta las tablas:
PIC_LOG_RECORDS_CONTAINET_FILE (Contiene los datos de la solicitud) en
este caso Upload)
65
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
PIC_LOG_EVENT_FILE (contiene el registro con el evento del archivo)
Solo para la plantilla "Otros Pagos Manuales" en Salida temprana, se agrega el
campo TKT (placa + documento) como parte de la llave para actualizar el estado
del pago; así asegurar que solo se actualicen registros que coincidan con el
Transaction Unique ID y el TKT correcto
66
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se recibe notificación con el resultado de la carga y se observa que actualizó correctamente el
estado de las solicitudes por tkt y no por refund request
67
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para los archivos que son con muchos registros se generará un mensaje
Se procede a cargar 900 registros
68
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se deja la observación que el botón de carga queda habilitado para recibir más
archivos.
Se carga un archivo de 200 registros
Se recibe correo de la 2da carga que era un archivo de 200 registros los cuales
todos se procesaron
69
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se recibe correo de la 1era carga exitosamente
Nota: Lo anterior se agrega de acuerdo a los PBIs:
• 613158 PIC - Cargue de resultados de pagos manuales TC Parte I (Rechazos / Pago Exitoso).
• 700820 PIC - Cambio Cargue de resultados de pagos manuales TC Parte 2 (Rechazos / Pago Exitoso) Cardinal y Cielo.
• 706301 PIC - Cambio Cargue de resultados de pagos manuales TC Parte 3 FINAL (Rechazos / Pago Exitoso) Cardinal
y Cielo.
• 1018396 PIC - REQ1696509 - Adición del campo TKT como parte de la llave de actualización en "Otros Pagos
Manuales".
• 1132036 INC7426312 - PI - Pantalla de Cargue de resultado.
70
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
11.1.4. Cargue de Rechazados
Este módulo permite el cargue de un archivo con los formatos relacionados a
EXCEL, para cargar transacciones de reembolsos (TR) rechazadas tras la fecha de
pago en el integrador de pagos para actualizar su estado y posteriormente el PIC
ejecute la actualización del estado de pago en Mozart.
Para realizar este cargue se ingresa al PIC, al menú de “Procesos” y la opción
“Cargue de rechazados después del pago”.
El aplicativo permite seleccionar un archivo en el explorador.
71
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Después de seleccionar el archivo, se da clic en el botón “Cargar archivo”, donde el
sistema pasa a validar que el archivo sea de los formatos relacionados a EXCEL,
que pueda leerse, y que contenga los encabezados escritos de manera correcta y
en el orden adecuado (Número de seguimiento, Estado, Motivo de rechazo, Fecha
de rechazo del Banco, Descripción).
Si la validación es exitosa, el sistema genera un archivo, para descargar, con el
resultado del cargue.
72
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Los registros que cumplan con las características indicadas tendrán actualización
en base de datos pasando a estado “Rechazado”.
Para el archivo resultado, los casos exitosos se marcan con “Actualización exitosa”.
En los casos contrarios, se indica cómo “Actualización fallida”, el motivo o razón de
la característica que no fue cumplida, tal como se muestra en el siguiente archivo
resultado:
Si la validación del formato del archivo, su ejecución o la validación de los
encabezados tiene un resultado negativo, el sistema mostrará un mensaje
indicando el error correspondiente. Por ejemplo, el siguiente mensaje se presenta
cuando se intenta cargar un archivo con formato PDF.
73
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
El archivo tiene la siguiente estructura:
74
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Ingresar a la Base de datos y consulta las tablas:
SELECT * FROM [rfd].[PIC_LOG_RECORDS_CONTAINET_FILE] order by
created_date desc
SELECT * FROM [rfd].[PIC_LOG_EVENT_FILE] order by created_date desc
75
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: Lo anterior se agrega de acuerdo con los siguientes PBIS: 613179 PIC - Cargue de
casos rechazados por TC posterior al proceso cierre. Front y 697799 PIC - Cargue de
casos rechazados por TC posterior al proceso cierre. Back.
11.1.5. Reapertura Bancaria
Tesorería tiene este módulo que permite cambiar las solicitudes de reembolsos
pagadas con transferencia bancaria (CR) para cambiar su estado de pagado a
rechazado debido a excepciones de bancos por rechazos tardíos u otros motivos.
El proceso es en el menú de "Procesos" >> Reapertura bancaria.
Antes de iniciar el proceso se debe configurar los correos a los que les debe llegar
el resultado de lo procesado.
En Base de Datos la tabla de correos internos es MST_INTERNAL_EMAILS y el
proceso es 'CR Reapertura de pagos'
Select * from [master].[MST_INTERNAL_EMAILS] where process='CR Reapertura
de pagos'
Desde el PIC vamos al menú a Maestras >> Correos Internos y se filtra por el
proceso : “CR Reapertura de pagos”
Se da clic en editar (lapiz) y se agregan los correos deseados separados por punto
y coma “;”
76
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Después de configurar el correo para cargar el archivo se ingresa al menú de
"Procesos" >> Reapertura bancaria
El archivo de Excel o csv debe ser con los siguientes encabezados
77
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
El encabezado del archivo contiene el siguiente orden y nombres de columnas:
Motivo de rechazo, “son los códigos de la tabla [rfd].[CODES_REJECTION_REASON]
Número de Zendesk
Fecha de rechazo del Banco: El formato de fecha es DD.MM.YYYY
Los códigos de rechazo son de acuerdo a la tabla:
SELECT*FROM [az-sqla-piccust-use-qa].[rfd].[CODES_REJECTION_REASON]
Dar clic en "Cargar archivo", y se selecciona el archivo que se desea cargar
Dar clic en Procesar
78
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Validar el correo enviado de acuerdo a los correos configurados en correos internos
Proceso = 'CR Reapertura de pagos'
Se observa archivo adjunto el cual tiene dos columnas adicionales a continuación
del campo Fecha de Rechazo del Banco llamadas “Resultado” y “Motivo” que tendrá
los siguientes usos:
“Resultado” será usado para poner frente a cada registro de solicitud el resultado
de las validaciones por cada campo y registro a registro del archivo con los valores
“Exitoso” y “Fallido”
“Motivo” será usado para poner frente a cada registro de solicitud con resultado
fallido el motivo de su fallo que impidió la actualización del estado a pagado.
79
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se observa en pantalla de consulta reembolso en PIC
Se inserta correctamente en base de datos en la tabla Detail
Select * from [rfd].[PIC_PAYMENT_DETAIL]
80
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se actualiza el estado en la Request
81
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• Validar la tabla temporal SELECT * FROM [rfd].[PIC_TEMP_TREASURY]
Extrae todos los registros del archivo y los almacena en la tabla [rfd].[PIC_TEMP_TREASURY]
update_status: validada "V" significa que la solicitud ya fue verificada y como resultado ya se cuenta
con un resultado exitoso o fallido error "E" significa que ocurrió un error al enviar el estado de la
solicitud a capa media y por lo tanto el registro debe ser enviado nuevamente.
Nota: La marca de fallo del registro se hará sobre la primera condición que falle. Las demás
verificaciones serán saltadas y continuará con la siguiente solicitud del archivo.
Si una solicitud no cumple las condiciones el procesamiento del archivo no finaliza. El procesamiento
debe continuar con todos los registros incluidos dentro del archivo cargado.
Se realiza las siguientes validaciones:
✓ Verificar si existen dos o más registros con igual número de solicitud en el archivo
✓ Verificar que el valor del campo Fecha de Rechazo del Banco tiene el formato DD.MM.YYYY
✓ Verificar si el Numero Zendesk existe en base de datos.
✓ Verificar que si el Numero Zendesk tiene forma de pago transferencia bancaria “CR”
✓ Verifica que la solicitud se encuentra en estado “Pagado”
✓ Verificar que la fecha del campo Fecha de Rechazo del Banco debe ser igual o mayor a la
fecha de pago.
✓ Verificar que la fecha del campo Fecha de Rechazo del Banco debe ser igual o menor a la
fecha de cargue del archivo, es decir, fecha actual del sistema.
Conteo de registros y control de proceso
SELECT * from [rfd].[PIC_LOG_EVENT_FILE] order by 1 desc
82
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Revisar los campos que se inserten correctamente:
FILE_NAME: Nombre del archivo cargado y procesado debe incluir la extensión
TOTAL_RECORDS: Total solicitudes del archivo
TOTAL_RECORDS_PROCESSED: Total solicitudes exitosas del archivo
TOTAL_RECORDS_UNPROCESSED: Total solicitudes Fallidas del archivo.
Tipo Evento. Almacena el tipo de evento ejecutado. Para este caso almacena el valor “Upload” para
indicar la operación de carga de un archivo.
Fecha y hora del archivo cargado.
Usuario quien carga el archivo, el cual corresponde a la cuenta de correo del usuario autenticado.
Validar archivo en Blob Storage
Ingresar al portal azure / azstacpiccustuseqa y al contenedor CR_Reapertura.
83
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se observa la carpeta nombrada con el año y mes para almacenar lo archivos procesados. Donde
YYYY corresponde al año actual en número y MM corresponde al mes actual en número. Si no existe
una carpeta nombrada con el año y mes actual el sistema debe crearla automáticamente.
Se observa que si se carga n veces el archivo con el mismo nombre deja almacenado el ultimo
cargado.
Desde el backend se puede cargar archivo en el siguiente link
https://azwapppiccustbknduseqa.az-asev3-use-qa.appserviceenvironment.net/swagger/index.html
Opción "ReopenApplicationCR"
84
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: Se agrega el menú de acuerdo a los PBIs 893737 PIC - Reapertura de solicitudes con transferencia bancaria –
Validación de data cargada en plantilla - Back End. PBI 893818 PIC - Reapertura de solicitudes con transferencia bancaria
- Procesamiento de transacciones - Back End - Parte 1. PBI 898729 PIC - Reapertura de solicitudes con transferencia
bancaria - Pantalla de carga - Front End Parte 2.
11.1.6. Consulta de Reembolso
Para consultar un reembolso el usuario quien consulta debe tener asignado el
mismo canal del reembolso consultado
Consultar los canales asociados al usuario que consultará reembolso
Ingresar al menú de Procesos, elegir la opción en Sub-menú de “Consulta de
rembolso”
Ingresa en el campo de búsqueda un reembolso relacionado con el mismo canal
de usuario quien consulta (Validado previamente en la pantalla de Usuarios)
85
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con los PBI
• 805524 - PIC - Segregar el sistema por canales configurados - Pantalla de Consulta TC
11.1.7. Gestión de Pago
Este módulo permite consultar el detalle de una solicitud de pago rechazada,
visualizar los archivos de datos adjuntos de la solicitud y modificar los datos
bancarios para repetir la ejecución automática o manualmente el pago en SAP.
86
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para ingresar a la opción Gestión de pago se debe ingresar al menú Procesos
opción Gestión de Pagos. Por defecto se va a mostrar todos aquellos reembolsos
con forma de pago Cash en estado no procesado “U” y que pertenecen a los mismos
canales que tiene relacionado el usuario que se autenticó en el PIC.
En inglés
El módulo muestra un campo de búsqueda por solicitud de reembolso, una malla
con la solicitud del reembolso, la fecha en que se ingresó la solicitud, el país al que
pertenece la solicitud, el canal del cual se hizo, el tiempo de antigüedad en número
de días desde la solicitud a la fecha actual y el check para enviar la notificación para
que el usuario final actualice los datos bancarios a nivel masivo; adicional se
87
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
sistema.
muestran los registros en orden ascendente del menor número de días en el
Los registros que se muestran en la pantalla deben ser forma de pago cash, en
estado rechazado y tener la información en las tablas
PIC_FOP_PAYMENT_REQUEST,
PIC_PAYMENT_REQUEST,
PIC_PAYMENT_DETAIL,
PIC_BANK_DATA_INFORMATION y
PIC_SUPPORT_FILE.
PIC_PAYMENT_REQUEST: PAYMENT_STATUS= U.
PIC_FOP_PAYMENT_REQUEST: FOP=CR.
PIC_PAYMENT_DETAIL: STATUS_CODE= U, FOP_CODE=CR.
PIC_BANK_DATA_INFORMATION: UPDATED_STATUS=Y
PIC_SUPPORT_FILE: Debe tener un registro en la tabla con referencia en el
campo ID_BANK_DATA_INFORMATION con el mismo valor del registro del
mismo campo de la tabla PIC_BANK_DATA_INFORMATION.
Nota: Para registros pertenecientes a los canales MyIdTravel y Aviajar en estado
rechazado en las tablas PIC_PAYMENT_REQUEST y PIC_PAYMENT_DETAIL,
se debe tener el campo FILES_ARE_VALID=NULL de la tabla
PIC_BANK_DATA_INFORMATION.
ejemplo
88
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al seleccionar uno de los registros por pantalla se debe desplegar la pantalla de
proceso de pago
89
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
90
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se debe poder visualizar los botones Autorizar, Ejecución de interfaz, Voucher y
enviar notificación de acuerdo con los criterios de cada solicitud y este ultimo de
enviar notificación se va amostrar siempre para todos los casos sin importar si
tienen o no datos bancarios Dummy o no.
91
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
11.1.7.1. Botón Autorizar:
El botón Autorizar se va a habilitar si se selecciona el radio button Archivos válidos
en la opción “SI”.
Al confirmar se guarda la información y queda en estado V pendiente del paso de
la function para irse a sap
92
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
11.1.7.2. Botón Voucher
En caso de seleccionar el radio button “NO” en archivos válidos, se debe activar el
botón Voucher (para todos los canales).
93
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
y Agrega el botón Actualizar para almacenar el documento como no válido, el
sistema conserva el registro como rechazado
Para este módulo, se realizó un ajuste sobre la columna “Fecha de rechazo del
banco”, donde esta no puede ser vacía, con formato diferente a “YYYY/MM/DD”, o
que sea menor a la fecha de pago. Para ello se definieron tres razones de
“Actualización fallida”, para cada escenario. Tal como se muestra a continuación,
para la ejecución de ellos.
11.1.7.3. Botón Enviar notificación
El bóton “enviar notificación” se habilitó para todas las solicitudes sin restricción.
Tener en cuenta que para enviar la notificación debe de existir la información de
los pasajeros en AVR en las tablas [rfd].[AVR_INFORMATION_ADDITIONAL_PASSENGER] y
[rfd].[AVR_INFORMATION_PASSENGER]
Se puede realizar el envío de las notificaciones de forma masiva; seleccionando el
check a cada solicitud y después dando clic en enviar notificación
94
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
O de forma individual ingresando a la solicitud y dando clic en el botón de enviar
notificación
95
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Y se envía la notificación al usuario final para actualizar los datos bancarios desde
el formulario de av.com
En AVR se observa aquí, consultar Manual funcional de AVR.
Nota: Lo anterior se crea de acuerdo con los PBIs:
• 629879 PIC - Botón Ingresar para Pantalla de consulta por número de solicitud de reembolso (Central Reembolsos
Transferencia Bancaria) Front End parte 3 - Control y gestión de pago - proceso de pago
96
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• 629879 PIC - Botón Ingresar para Pantalla de consulta por numero de solicitud de reembolso (Central Reembolsos
Transferencia Bancaria) Front End parte 3 - Control y gestión de pago - proceso de pago
• 741397 PIC - Ajuste 2.3 pantalla de Control y Gestión de Pago
• 800932 PIC - Ajuste query de consulta y actualización de datos bancarios en pantalla de Proceso de pago - API Bank
Data Information - Módulo Control y gestión de pago
• 1005046 PIC - Actualizar Datos Bancarios - Generar Notificaciones. Parte I
• 1316984 PI - Eliminar restricción de filtrado para envío de notificaciones en Gestión de Pagos
11.1.7.4. Datos Dummy
El área de reembolsos requiere que se le permita completar manualmente los datos
bancarios de solicitudes masivas con forma de pago Cash cargadas desde el canal
Special Refund.
El flujo que llama la API Bank Data Information envia los datos Dummy y no se
requiere modificar el servicio para que valide el canal y envíe los datos.
Al momento de almacenar los datos bancarios se obtiene el numero de la solicitud
Zendesk, verifica si tiene transacciones con forma de pago transferencia bancaria
“CR” con estado “U” y el canal de la solicitud es Special Refund (AV, 8), (LM, 9),
(EMDs, 14) Si cumple la condición, se ejecuta las siguientes acciones:
Los campos que se utilizarán son los mimos campos que se utilizan el servicio
Bank Data Information. Cuando inserte los datos bancarios debe almacenar los
siguientes datos:
Nombre del dato bancario Valor almacenar Observación
account_Currency_code Moneda del Reembolso
accountCodeSap 1
address Dummy
agencyNumber
bankAccountNo 9999999999
Utilizar un código de la tabla de bancos y enviar
bankCode
siempre el primero
cityCode
companyName Dummy
customerZipCode Address
destinationCountryCode aa
firstName Dummy
iban Iban
Utilizar un código de la tabla de identificación de
identificationCode
Colombia y enviar siempre el primero
identificationNumber 9999999999
lastName Dummy
97
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
middleName Dummy
noticeFormCountry
payingCountryCode CO
Corresponde al número Zendesk recibido en la
refundRequest
solicitud del servicio. Este valor se conserva
rou_Bco Vacío
secondLastName Dummy
stateCode
typePersonCode Y
fileName Vacío
contentType Vacío
fileExten Vacío
size Vacío
content Vacío
Para este escenario, aunque se crearon datos dummy de Colombia, el usuario debe
poder seleccionar únicamente los países correspondientes a la moneda en la
pantalla (No se podrá cambiar la Moneda)
Debe almacenar el registro en la tabla principal PIC_BANK_DATA_INFORMATION
con los datos dummy ingresados cuando se realice una actualización.
Teniendo en cuenta el número de solicitud Zendesk actual recibido, si ya existe un
registro de datos bancarios debe actualizar el campo update_status con el valor "N"
para indicar que no es el último registro actualizado. El registro nuevo debe
almacenarse con el valor "Y" para indicar que es el último registro actualizado.
En esta pantalla de Gestión de pago se ven las solicitudes de reembolso en:
• Estado “V” validado
• sin soporte de pago (no tiene archivo adjunto) y
• con dato Dummy en el campo bankAccountNo igual a 9999999999
PIC - Actualizar Datos Bancarios - Generar Notificaciones.
Si la FOP de pago es CR y se identifica que es una línea dummy debe realizar la
notificación nueva, solicitando estos datos
Nota: Lo anterior se crea de acuerdo con los PBIs:
• 747906 SR - Ajuste 7: Uso del API Bank Data Information para enviar al integrador de pagos datos genéricos para
que manualmente un agente de reembolsos complete los datos
• 758751 PIC - Ajuste al formulario de datos Bancarios del PIC (Ajuste del Dinamismo) Pantalla Control y gestión de
pago - proceso de pago - API Bank Data Information.
98
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• 787064 PIC - Ajuste comportamiento de Tipo de Persona para pantalla Control y gestión de pago - proceso de pago
• 1005046 PIC - Actualizar Datos Bancarios - Generar Notificaciones. Parte I
• 1062004 PIC - Inclusión de FOP CR sin datos bancarios en la Pantalla de Control y Gestión de Pago
• 1081349 PIC - Pantalla de Gestión de Pagos para registros con DM
11.1.7.5. Validación en Output de Pago para DM
Cuando la FOP es CR. Se tiene la siguiente lógica:
1. Verificación de datos bancarios:
o Consultar la tabla PIC_Bank_Data_Informationpara verificar si existen
datos bancarios registrados para este registro.
o Si no existen datos bancarios, continúe con el paso 2.
o Si existen datos bancarios, evalúe si se trata de datos dummy (FirstName:
Dummy, LastName: Dummy, crear parámetros de estos datos).
▪ Si los datos son ficticios, continúe con el paso 2.
▪ Si los datos son reales, continua con el proceso normal de salida de
pago.
2. Evaluación del canal de reembolso:
o Validar el canal del reembolso.
Si el canal es igual a 8 (valor definido por parámetros separados por
coma o '|' - Pueden existir varios canales “
CHANNEL_SR_PAYMENT_REQUEST“),
el reembolso debe ser cambiado a estado 'U'. (Actualizar en la Payment
Request, y crear nuevo registro en la Detail) - - Solo deben ser
considerados los tiquetes que no se encuentren en estado "Pagado" ni
"Enviado a Pago"
CHANNEL_SR_PAYMENT_REQUEST
o Si el canal es diferente al valor configurado en el parámetro, se debe:
o Enviar la notificación desarrollada en el PBI#1079427, utilizando el
servicio correspondiente en AVR (ver código de notificación en dicho
PBI).
o El reembolso deberá cambiar a estado a 'R'. (Actualizar en la
Payment Request, y crear nuevo registro en la Detail) - - Solo deben
99
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
ser considerados los tiquetes que no se encuentren en estado
"Pagado" ni "Enviado a Pago"
Nota: Lo anterior es de acuerdo al PBI
• 1081336 PIC - Validación en Output de Pago para DM
11.1.8. Vouchers no Generados
Se ingresa por el menú de Procesos >> Vouchers no Generados
Se observa el campo “Buscar” el cual filtra por número de reembolso.
Se tiene la acción de “Generar voucher” el cual reprocesa los casos hace el llamado
para la generación del voucher.
Y en el “Detalle” icono de ojo podemos observar la información de la solicitud, sin
poder editar ningún campo
100
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al Dar clic en “Generar voucher” se abre un pop up informando "Se está procesando
los voucher rechazados en segundo plano. La pantalla será habilitada al finalizar el
procesamiento."
Al dar clic en aceptar, se devuelve al home del Integrador de pagos (PI).
101
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Si ingresamos de nuevo en procesos >> Voucher no Generados y aún se están
procesando las solicitudes; entonces se observa el mensaje "En este momento se
están reprocesando los voucher rechazados. Intente más tarde"
En la tabla de logs transaction se observa toda la trazabilidad de cada solicitud
registrada en la pantalla
select id_log, log_source, log_table, log_msn, created_date, created_user from [az-sqla-piccust-
use-qa].[rfd].[pic_logs_transaction]
Nota: Lo anterior es de acuerdo al PBI
• 1233617 PI – Restringir edición de campo en menú Voucher no Generado – solo visualización para todos los roles
11.1.9. Cargue de Resultados IP >> Menú deshabilitado
102
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Esta pantalla es para cargar el Pago, Rechazo o Finalización de las solicitudes de
los colaboradores que llegan por el canal 5 y 6. Se ingresa por el menú de
Procesos >> Cargue de resultado IP
Antes de cargar el pago se tiene el siguiente proceso:
Cuando el colaborador actualiza los datos bancarios y el sistema va a decidir si
dejar el pago en IP o automático de SAP se tomar en cuenta lo siguiente:
• Moneda del reembolso: [rfd].[PIC_PAYMENT_REQUEST] -- >
refund_currency
• Moneda de la cuenta bancaria: rfd.PIC_BANK_DATA_INFORMATION ---->
account_currency_code
Si la moneda del reembolso es la misma de la cuenta bancaria seleccionada por el
pasajero (empleado) se envía a SAP si es diferente envia el archivo IP.
Por ejemplo
Moneda del reembolso es diferente de la cuenta bancaria
103
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Usuario actualiza datos bancarios y se observa que las monedas son diferentes,
por lo que llega correctamente el correo configurado en el parámetro
TEMPLATE_BANK_INFORMATION_TO
Se confirma adjunto del correo
104
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Moneda del reembolso es igual de la cuenta bancaria
Se confirma que se tiene el caso 189018 en estado Rechazado y en canal 6
(aviajar), Usuario actualiza datos bancarios y se observa que las monedas son
iguales, por lo que no se envía correo de IP y si se envía a SAP cash
Al recibir el correo de IP se valida los datos y se procede a cargar el archivo para
realizar el (P,R ó F) de esa solicitud.
El archivo para cargar debe tener las siguientes columnas:
Columna Refund
Request Obligatorio Descripción / Restricciones
Sí Identificador único del reembolso.
Ticket Sí Número de ticket asociado al reembolso.
Status Sí Estado del registro. Solo se permiten los
valores: P, F o R.
Reject Reason
Condicional Campo opcional, pero obligatorio cuando el Status sea
“R” (Rechazado) o "F" (Finalizado)
El sistema permite la carga de la plantilla en formato Excel.
105
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Antes de cargar el archivo se debe tener presente:
El estado de las solicitudes debe ser en proceso “I”.
Los campos Número de Zendesk, ticket y estado están completamente
diligenciados.
El formato admitido es Excel (*.xlsx).
El tamaño máximo del archivo para procesar será hasta 1MB.
Validaciones al momento de la carga
campos obligatorios
o El sistema deberá verificar que las columnas Refund
Request, Ticket y Status estén diligenciadas.
o Si el campo Status es “R” o "F", el campo Reason Reject deberá
ser obligatorio.
llave compuesta
o El sistema deberá utilizar la llave Refund Request + Ticket para
identificar los registros que serán actualizados.
estado actual
o Solo podrán ser actualizados los registros que actualmente se
encuentren en estado “I” y que tengan el campo IP en la
tabla [rfd].[PIC_FOP_PAYMENT_REQUEST] poblado con Y
o Si el registro se encuentra en un estado diferente o no se encuentra
con el campo IP en la tabla [rfd].[PIC_FOP_PAYMENT_REQUEST]
poblado con Y, deberá ser omitido y reportado en un log de errores.
Resultado del proceso de carga
o Los registros válidos deberán ser actualizados conforme a la
información suministrada en la plantilla.
o Los registros inválidos o con errores deberán incluirse en un correo
como se hace en actualmente en el proceso de plantilla de resultados
o
Proceso:
1. Filtrado por REFUND_REQUEST:
106
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
o Deberá evaluarse el REFUND_REQUEST (Los procesos
mencionados solo deben ejecutarse para registros donde el
campo REFUND_REQUEST contenga un valor numérico.)
▪ Deberá realizar las actualizaciones que actualmente son
ejecutadas para los estados P, F y R
▪ Para el estado R, deberá ejecutarse los mismos pasos que se
ejecutan cuando se recibe una respuesta Código 1110 o 2002
del PBI #928243 (Activar Segunda Forma de pago solo para los
registros numéricos)
▪ Deberá evaluar los registros de la solicitud. En caso de que
todos los registros de la solicitud se encuentren en un estado
Final (F, C o P), deberá realizar el siguiente flujo:
▪ Deberá generar los comprobantes de pago
correspondientes y dejarlos almacenados de acuerdo a
lo ya desarrollado
▪ Deberá llamar el API - Update Payment
Nota: En caso de que uno de los registros de la misma solicitud, no
contenga un estado final el proceso se detendrá (No ejecutará este
paso)
Si el campo no es numérico o está vacío, el registro debe ser omitido en el
procesamiento.
Nota: Lo anterior se agrega de acuerdo a los siguientes PBIs:
• 1123978 PIC – Pago rechazados canal MyIDtravel y aviajar - Fronted para Plantilla de Resultados
• 1123055 PIC – Pago rechazados canal MyIDtravel y aviajar - Plantilla de Resultados para IP Cash
• 1122847 PIC – Pago rechazados canal MyIDtravel y aviajar - Envío automático de correo al equipo de Reembolsos
• 1122862 PIC – Pago rechazados canal MyIDtravel y aviajar - Validación al recibir información en el API “Payment Output”
• 1106581 PIC – Pago rechazados canal MyIDtravel y aviajar - Detección de rechazo bancario en proceso de pago TC
backend - Parte II
• 1194835 PI - Ajuste en el proceso de actualizacion de datos bancarios para enviar a SAP
• 1233639 PI - Moneda Formularios datos bancarios - limpieza en API del desarrollo de IP
11.1.10. Gestión de Pago ACM
Este módulo permite la actualización de los iatas-acm de las solicitudes que no se
lograron procesar; por motivos del iata errado.
Se ingresa por Procesos >> Gestión de pago ACM
107
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Aquí observamos todos los casos con fop NC, status = “U”
Sí el IATA recibido llega vacío, con valor 0 ó con valor 00000000 ó si en el Retorno
de SAP ACM el mensaje de error es “Error en el campo: customerNumber must
not be blank”.
El registro debe quedar en estado U y la razón de rechazo “IATA no existe”. Los
cuales se verán en esta pantalla de gestión de pago ACM.
En la pantalla se debe agrupar por solicitud.
Frente a cada solicitud tenemos la opción de editar el iata (ícono de lápiz)
Al dar clic en editar nos muestra un Pop-up con los documentos (tkt o emd)
asociados a la solicitud y cada documento debe tener asociado un Iata, de lo
contrario no se permita guardar.
Validar con maestra de IATAS (MST_IATA_ACM) que el IATA exista y este activo,
de lo contrario presentar un mensaje de advertencia "IATA no configurado en la
maestra" y no permita guardar.
108
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• el botón “Finalizar”: Se cancelan las acciones realizadas.
• el botón "Guardar". Al Guardar, se debe ejecutar lo siguiente:
o Actualiza el IATA en la PIC_PAYMENT_REQUEST.
o Actualiza estado a "V"
o Actualiza mensaje (REJECTION_REASON) a "Modificación en la IATA" en
la PIC_PAYMENT_DETAIL. Nota: Esto se agrega para identificar que se
actualizó el estado a "V" por actualización en IATA.
109
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
La function pasa az-fapp-picsap-use-qa y toma todos los casos en V y T y se los
lleva a sapa cm dejandolos en la tabla Select * from
[rfd].[PIC_SAP_ACM_INTERFACE_OUT] Y se actualiza el estado a En proceso “I”
Y cuando SAP ACM genera el acm capa media nos actualiza la tabla
[rfd].[PIC_SAP_ACM_INTERFACE_OUT] con el ACM (TRX_NUMBER) y lo deja en
estado Completado y la function cuando pasa actualiza el PI dejándolo en estado
Pagado “P” y con la referencia del acm y en la tabla de salida lo deja en estado
“actualizado”.
Nota: Lo anterior se agrega de acuerdo a los siguientes PBIs:
• 1156705 PIC - Pantalla de Control y Gestión de Pago ACM - Parte II
• 1177418 PI - Ajustes y Controles – ACM
• 1215091 PIC - Ajuste - Pantalla de Control y Gestión de Pago ACM
• 1215330 PI - Ajuste proceso Envío a SAP ACM – Control por IATA inválido
110
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
11.2. ADMINISTRACIÓN
11.2.1. Gestión de Usuarios
Este módulo permite la consulta, creación y modificación de cuentas de usuario que
puedes usarse para ingresar a la web app PIC. Este módulo se puede acceder
seleccionando la opción Gestión de Usuarios, del menú Administración.
Una vez seleccionada la opción, se mostrará por pantalla el listado con los usuarios
creados en base de datos hasta el momento. Se mostrará el nombre del usuario,
su identificación, su correo electrónico y su estado. La columna detalle está
destinada para las acciones de modificación y cambio de estado de un registro en
particular.
111
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
En la pantalla se podrá observar el campo disponible para ingresar el criterio de
búsqueda para el campo Nombre de usuario. Al ingresar el dato a buscar se
mostrará inmediatamente en pantalla los registros que obedecen el criterio.
En caso de no encontrarse el registro, el sistema mostrará un mensaje de validación
informando que el usuario no se encuentra en la base de datos.
Junto al campo de consulta por nombre, se encuentra el icono con el signo +, con
la etiqueta Agregar usuario.
En esta opción, al hacer click sobre el ícono, se desplegará una nueva ventana en
donde se podrá agregar un nuevo usuario en el sistema.
112
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
En la ventana se debe diligenciar el nombre del nuevo usuario, el tipo de
identificación, el número de identificación, email, gerencia a la que pertenece, cargo
al que pertenece y tipo de contratación. A excepción de los campos segundo
nombre y apellido, todos los campos son obligatorios para la creación de un nuevo
usuario. En la parte inferior de la nueva ventana hay dos pestañas correspondientes
a los roles y canales que puede tener el usuario creando, siendo obligatoria solo la
selección del rol.
Se debe tener presente que el nuevo usuario no puede tener el mismo email o tipo
y número de identificación de un usuario ya existente en base de datos.
Imagen XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
En la columna se encuentra el switch que permite el cambio de estado, así como
el icono en forma de lápiz, con el que se podrán hacer modificaciones. Estas
acciones se realizan para un registro en particular, el que se relaciona en frente de
cada icono.
Imagen con el recuadro en el icono de modificar y del switch.XXXXXXXXXXXXX
Al hacer el cambio de estado mediante el switch de Detalle, el usuario
seleccionado quedará deshabilitado.
Imagen XXXXXXXXXXXXXXXXX
Se debe presionar el icono del lápiz para modificar algún usuario existente, con lo
que se desplegará una nueva ventana donde se podrá modificar cualquiera de los
campos. Al modificar los campos email, tipo de identificación o número de
identificación, se debe tener en cuenta que el valor ingresado no puede ser igual a
un valor existente en base de datos.
Imagen XXXXXXXXXXXXXXXXXXXXXXXXX
113
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
En caso de ingresar valores existentes, se mostrará un popup informando que el
registro ya existe en base de datos.
Imagen con el pop up de usuario existente XXXXXXXXXXXXXXXXXXX.
11.2.2. Gestión de Roles
El módulo de gestión de roles permite consultar, crear y modificar Roles.
Para ingresar a Gestion de roles se ingresa por la opción de menú “Administración”
y submenú “Gestión de Roles”
En la pantalla de la Maestra de gestión de roles se encuentra la opción para
consultar, crear nuevo rol y modificar rol
114
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
10.2.2.1 Consultar ROL
Para consultar se puede seleccionar los filtros por los cuales se desea buscar
información.
Se ingresa los datos a consultar en la caja de texto de búsqueda.
115
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
10.2.2.2 Creación de Rol
Para crear un Rol se da clic en la opción “Crear nuevo rol”
Se presenta la pantalla para agregar la información del nuevo Rol
116
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se ingresa los datos requeridos, Nombre Español, Nombre Inglés, Nombre
Portugués, Critico y Menús. El campo descripción es opcional.
Se debe seleccionar alménenos un menú para el nuevo Rol, Se puede elegir al
seleccionar el menú, los permisos, solo lectura o escritura
Al crear el Rol se muestra mensaje de creación exitosa.
117
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Después de la creación del rol se presenta el registro disponible para consultar
10.2.2.3 Modificación de Rol
Para Modificar un rol se ingresa por la opción que se presenta en forma de “lápiz”
Al ingresar se presenta la pantalla de modificación con los campos disponibles para
ser editados.
118
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se actualiza la información deseada en el Rol
Al dar clic en botón actualizar se presenta mensaje de validación de estado Activo
119
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al dar clic en el botón de “si, deseo Activarlo” Se presenta mensaje de actualización
exitosa
10.2.2.4 Activar y Desactivar Rol
El rol se puede desactivares activar desde la pantalla de Modificación de Rol y
desde la pantalla principal
Al desactivar un rol los usuarios que estén relacionados con dicho rol ya no podrán
ingresar con el perfil del rol desactivado y el rol ya no estará visible en las opciones
de gestión de usuarios para ser relacionado a un usuario.
Desactivando y Activando Roles desde la pantalla de Modificación
120
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al cambiar el rol de un estado Activo a Inactivo se presenta mensaje de Advertencia
Al desactivar el rol se presenta mensaje de actualización exitosa.
Al Activar el rol desde pantalla de modificación se presenta mensaje de advertencia
de activación
121
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al acepar la activación se presenta mensaje de actualización exitosa
122
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Cuando se Activa o desactiva desde pantalla principal se presentan las mismas
validaciones encontradas al modificar el rol desde la pantalla de modificación.
Al desactivar el rol por pantalla principal se presenta mensaje de advertencia
Al Aceptar desactivar el rol se presenta mensaje de actualización exitosa
Al Activar el rol por pantalla principal se presenta mensaje de advertencia de
Activación
123
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al aceptar la activación se presenta mensaje de actualización exitosa.
Nota: Lo anterior se agrega de acuerdo con los PBIs: 649828 PIC - Gestion de roles y
permisos - Front End FINAL, 601196 PIC - Gestión de roles y permisos Parte 1 Crear –
Back, 605894, PIC - Gestion de roles y permisos Parte 2 Consultar y Modificar – Back.
Gestión de Menús
124
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
11.3. TABLERO
11.4. MAESTRAS
11.4.1. IATAs ACM
En la Maestra de IATAS-ACM permite Consultar, Crear un nuevo IATA y modificar.
Para ingresar a la maestra de IATAS ACM se debe ingresar por la opción de menú
“Maestras” y submenú “Iatas Acm”
Esta información se guarda en la base de datos en la tabla master.MST_IATA_ACM.
Select * from [master].[MST_IATA_ACM]
Se puede consultar a través de la paginación disponible agrupando registros.
125
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Si se desea buscar un registro específico se puede consultar por los campos “IATA”,
“Código de país” y “Código de ciudad”
Consultar por IATA
Consultar por Código de país
Consultar por Código de ciudad
126
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Validación campos obligatorios
Cuando se crea un iata correctamente este confirma
Nota: Lo anterior es de acuerdo con los siguientes PBIs:
• 1215089 PIC – Crear GUI para Maestra de IATAS_ACM (MST_IATA_ACM)
11.4.2. Parámetros del Sistema
A través de la Maestra parámetros del sistema se puede crear un parámetro
específico para diferentes funcionalidades como: configuración de correos,
tiempos de respuestas. Entre otros.
Para ingresar seleccionar el menú Maestras, seleccionar el submenú
“Parámetros del sistema” Al ingresar se presenta la pantalla principal donde se
puede crear, modificar y consultar un Parámetro y se presenta la pantalla principal
donde se puede crear, modificar y consultar un Parámetro.
127
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
10.4.10.1 Consultar
Se puede consultar a través de la paginación disponible agrupando registros.
Si se desea buscas un registro especifico se puede consultar por los campos
“Código”, “Descripción” y “Valor”
128
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Consultar por código
Consultar por Descripción
129
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Consultar por Valor
10.4.10.2 Crear Parámetro
Para crear un nuevo parámetro dar clic en “Agrega nuevo parámetro”
Se presenta la pantalla para agregar la información del nuevo parámetro
130
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
realizada
Al dar clic en el botón “Crear” se presenta mensaje de confirmación de la creación
10.4.10.3 Modificar parámetro
Para modificar un parámetro dar clic en la opción de Modificar (lápiz)
Se presenta la pantalla con los campos del parámetro seleccionado para ser
editados
Al dar clic en el botón Actualizar se presenta mensaje de confirmación del
parámetro modificado.
131
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
La tabla en base de datos donde se encuentra los registros de creación y
actualización es: master.MST.PARAMETERS
Las acciones realizadas en la Maestra de parámetros quedan registradas en la
tabla PIC_LOGS_TRANASCTION
Nota: lo anterior se agrega de acuerdo con el PBI 611676 PIC - TM. Parámetros del
sistema
132
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
11.4.3. Datos Bancarios
Este módulo permite la configuración de los datos bancarios que deben ser usados
por los canales para determinar los campos del formulario que debe ser habilitado
al titular del reembolso.
Se ingresa en la aplicación, en el menú “Maestras” y la opción “Datos Bancarios”
Al ingresar a esta opción el sistema despliega en pantalla una lista desplegable
donde se puede seleccionar el país al cual se le configurarán los datos bancarios.
Cuando se selecciona uno de los países se muestra una tabla con las columnas:
Orden, Dato Bancario, Mandatorio, Estado, Detalle.
La tabla presenta los datos bancarios que se tienen creados, su estado
(activo/inactivo), la obligatoriedad y una opción para modificar los datos. En la parte
final del módulo, se presentan textos de ayuda en español, inglés y portugués,
asociados a los datos bancarios del país seleccionado.
133
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Cada uno de los datos bancarios puede ser modificado en cuanto su obligatoriedad,
lo cual se realiza activando o inactivando el interruptor deslizante que se presenta
para la columna “Mandatorio”, con lo cual el sistema presenta un mensaje de
actualización del dato bancario.
Del mismo modo, se puede realizar la activación o inactivación del estado de un
dato bancario para el país en cuestión. Sin embargo, para poder realizar la
inactivación del dato bancario, es necesario validar que este no sea un campo
mandatorio. Si lo es, se genera un mensaje al usuario indicándole que no se puede
inactivar el campo, porque es un campo mandatorio.
134
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Cuando se selecciona el ícono de lápiz en la columna “Detalle”, el sistema muestra
una ventana donde se tienen los campos Longitud mínima, Longitud máxima, Tipo
de dato, Mandatorio, Estado y Textos de ayuda en español, inglés y portugués, para
el dato bancario.
Cuando se modifican correctamente estos campos, el sistema habilita el botón
“Guardar” y, posteriormente, muestra un mensaje de la actualización exitosa.
135
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
El módulo permite que se pueda modificar el orden de los datos bancarios para el
país, para ello se da clic sobre el ícono de llave de configuración en la columna
orden.
El sistema despliega una ventana donde se permite mover los datos bancarios,
seleccionando con clic sostenido el dato bancario desde la posición inicial hasta la
posición donde se quiera ubicar.
136
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Cuando los datos bancarios han cambiado de posición, se habilita el botón
“Guardar” y dando clic en él, se muestra una ventana de éxito en la modificación.
137
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Por último, se puede visualizar en la tabla los datos bancarios del país seleccionado
en el orden modificado.
Los Datos Bancarios en la Base de datos se encuentra en la tabla
[master].[MST_SCREEN_FIELD_BANK],
Y se expone a los canales a través del api Get Master Info en el nodo field-country
https://azwapppiccustextsuseqa.az-asev3-use-qa.appserviceenvironment.net/MasterBank
138
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
En el swager es: https://azwapppiccustextsuseqa.az-asev3-use-qa.appserviceenvironment.net/Swagger/index.html
en MasterBankEndpoint
Este api tiene varias reglas para mostrar la información de acuerdo con el canal,
los cuales son los siguientes:
139
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Lifemiles.com - 11
Avianca Trade - 4
Aviajar - 6
Canal (Ver por código) Regla - PBI 886648
Si todas las FOP son CR, debe retornar CR + KR
Si todas las FOP son TR, debe retornar TR + KR
Avianca.com - 10
Si existen formas de pago TR + CR dentro de la misma solicitud, debe retornar CR + KR
Si hay documentos con formas de pago diferentes a TR, CR o KR pero tiene al menos una forma de pago CR, debe retornar CR + KR
Si hay documentos con formas de pago diferentes a TR, CR o KR pero tiene al menos una forma de pago TR y ninguna CR, debe retornar TR + KR
Si todas las FOP son CR, debe retornar CR + KR + LM
Si todas las FOP son TR, debe retornar TR + KR + LM
Si existen formas de pago TR + CR dentro de la misma solicitud, debe retornar CR + KR + LM
Si hay documentos con formas de pago diferentes a TR, CR o KR pero tiene al menos una forma de pago CR, debe retornar CR + KR + LM
Si hay documentos con formas de pago diferentes a TR, CR o KR pero tiene al menos una forma de pago TR y ninguna CR, debe retornar TR + KR + LM
Si todas las FOP son CR, debe retornar CR (Natural + Juridico)
Si todas las FOP son TR, debe retornar TR
Si existen formas de pago TR + CR dentro de la misma solicitud, debe retornar CR (Natural + Juridico)
Si hay documentos con formas de pago diferentes a TR, CR o KR pero tiene al menos una forma de pago CR, debe retornar CR (Natural + Juridico)
Si hay documentos con formas de pago diferentes a TR, CR o KR pero tiene al menos una forma de pago TR y ninguna CR, debe retornar TR
Si todas las FOP son CR, debe retornar CR (Natural + Juridico)
Si todas las FOP son TR, debe retornar TR
Si existen formas de pago TR + CR dentro de la misma solicitud, debe retornar CR (Natural + Juridico)
Si hay documentos con formas de pago diferentes a TR, CR o KR pero tiene al menos una forma de pago CR, debe retornar CR (Natural + Juridico)
Si hay documentos con formas de pago diferentes a TR, CR o KR pero tiene al menos una forma de pago TR y ninguna CR, debe retornar TR
Si el parametro "Load Masive" no se encuentra marcado o contine una N debe retornar las formas de Pago (CR, TR, KR, NC, LM, CS, CV)
Si el parametro "Load Masive" se encuentra marcado y todas las FOP son CR, debe retornar CR
Si el parametro "Load Masive" se encuentra marcado y todas las FOP son TR, debe retornar TR
Si el parametro "Load Masive" se encuentra marcado y tiene formas de pago Mixtas, debe retornarCR
Si el parametro "Load Masive" no se encuentra marcado debe retornar las formas de Pago (CR, TR, KR, NC, LM, CS, CV)
Si el parametro "Load Masive" se encuentra marcado y todas las FOP son CR, debe retornar CR
Special Refund LM - 9
Si el parametro "Load Masive" se encuentra marcado y todas las FOP son TR, debe retornar TR
Si el parametro "Load Masive" se encuentra marcado y tiene formas de pago Mixtas, debe retornarCR
Si el parametro "Load Masive" no se encuentra marcado debe retornar las formas de Pago (CR, TR, KR, NC, LM, CS, CV)
Special Refund
Chargeback - 12
Si el parametro "Load Masive" se encuentra marcado y todas las FOP son TR, debe retornar TR
Si el parametro "Load Masive" se encuentra marcado y tiene formas de pago Mixtas, debe retornarCR
Si el parametro "Load Masive" no se encuentra marcado debe retornar las formas de Pago (CR, TR, KR, NC, LM, CS, CV)
Si el parametro "Load Masive" no se encuentra marcado debe retornar las formas de Pago (CR, TR, KR, NC, LM, CS, CV)
Special Refund Call
Center - 13
Si el parametro "Load Masive" se encuentra marcado y todas las FOP son TR, debe retornar TR
Si el parametro "Load Masive" se encuentra marcado y tiene formas de pago Mixtas, debe retornarCR
Si el parametro "Load Masive" no se encuentra marcado debe retornar las formas de Pago (CR, TR, KR, NC, LM, CS, CV)
Special Refund EMD - 14 Se respetará la forma de pago enviada, se radica por documento
MyIdTravel - 5 Se respetará la forma de pago enviada, se radica por documento
BSP - 3 Se respetará la forma de pago enviada, se radica por documento
Special Refund AV - 8
• El nodo payments-method:
De acuerdo al campo "Is Massive"
Si es Y = Debe retornar solo el nodo de "payment-methods" únicamente
SI es N / Vacío =
o Si en el campo ""payment-method-code" se retorna al menos una vez la
forma de pago CR (Parámetro) debe retornar la totalidad de los campos.
o Si en el campo "payment-method-code" no retorna la forma de pago CR
(Parámetro) debe retornar solo el nodo de "payment-methods"
Si el campo "corporate-code" está poblado en el request, la respuesta no debe
incluir el parámetro "KR" en el nodo "payments-method".
Si el campo "corporate-code" está vacío o no está presente, la respuesta puede
incluir la forma de pago "KR" si corresponde a la lógica de negocio.
• El nodo person-type debe evaluarse en el siguiente orden.
140
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Esto debe ser un parámetro configurable
SELECT * FROM [master].[MST_PARAMETERS]
WHERE PARAMETER_CODE IN ('API_EXT_CHANNEL','API_EXT_FOP')
1. Si el canal (Parámetro) es = 4, retornará todos los tipos de personas
2. Si el canal es diferente al configurado en el Parámetro deberá evaluar si el
campo "Corporate-code" se encuentra poblado:
2.1 Si se encuentra poblado, deberá retornar lo asociado a persona Jurídica (si
type_person_code = N)
2.2 Si no se encuentra poblado, deberá retornar lo asociado a persona Natural
(SI type_person_code = Y)
Nota: Lo anterior se agrega de acuerdo con los PBIs:
729462 PIC - Crud para TM que une campos bancarios por país. Parte I.
886648 PIC - Ajuste API Get Master Info (Nodo payments-method)
914507 PIC - Ajuste al servicio Get Master Info. PBI para Finalizar
968952 PIC - Ajuste Payment Methods en la Get Master Info para Código Corporativo
11.4.4. Países
La Maestra de países permite consultar, crear país y modificar país.
Se Ingresa a la pantalla de Países por la opción de menú “Maestras” y submenú
“países”
141
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para consultar un País se puede filtrar por NOMBRE ES, NOMBRE EN, NOMBRE
PT y CÓDIGO PAÍS
Filtrando por “NOMBRE ES”
Filtrando por “Código País”
Nota: Lo anterior se agrega de acuerdo con los PBI:
• 611681 - PIC - TM. Países
• 649833 - PIC - TM. Países FINAL
142
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
11.4.5. Ciudades
En la Maestra de ciudades permite Consultar, Crear una ciudad nueva y modificar
una ciudad.
Para ingresar a la maestra de ciudades se debe ingresar por la opción de menú
“Maestras” y submenú “Ciudades”
Se puede consultar una ciudad a través de la caja de texto de búsqueda
143
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
10.4.2 Crear Ciudad
Para crear una ciudad se da clic en la opción “Agregar ciudad”
Se presentan la pantalla para crear la ciudad con todos los campos editables.
Ingresar todos los campos para la creación exitosa de la ciudad, Seleccionar el
País el cual habilitará la lista de estados.
144
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al dar clic en el Botón crear se presenta el mensaje de Creación exitosa
10.4.3 Modificar ciudad
Para modificar una ciudad se debe seleccionar la opción en forma de “lápiz”
Se presenta la pantalla de modificación de la ciudad
145
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se puede modificar cualquier campo del formulario
Al dar clic en Actualizar se presenta mensaje de actualización exitosa
Nota: Lo anterior se agrega de acuerdo con los PBI
625663 - PBI PIC - TM. Ciudades (Creación)
630334 - PIC - TM. Ciudades (Modificación)
11.4.6. Tipos de Identificación
Este módulo permite consultar los documentos de identificación cargados
previamente en base de datos. El listado de tipos de identificación que se muestra
en esta opción se encuentra agrupado y ordenado alfabéticamente por país. A
este módulo se puede acceder seleccionando la opción Tipo de Identificación, del
menú Maestras.
146
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Una vez seleccionada la opción, se mostrará por pantalla el listado mencionado
inicialmente, con sus respectivas traducciones al idioma inglés y portugués.
Se dispone de igual manera con un campo de filtro que permite realizar la consulta
por el país o el tipo de identificación en cualquiera de los tres idiomas que maneja
la opción (español, inglés y portugués).
Una vez se ingrese un criterio de búsqueda en el campo ubicado al lado del filtro,
el sistema desplegara los registros que coinciden.
147
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
11.4.7. Formas de Pago
El módulo permite gestionar la creación y modificación de las formas de pago. Luego
de estar en la pantalla principal, dar clic en las opciones Maestras/Formas de pago
Agregar Formas de Pago
Seleccionar el botón +Agregar formas de pago:
Ingresar la información de la forma de pago y al finalizar dar clic en “Crear”:
148
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se observa mensaje “CREACIÓN Forma de Pago Creada exitosamente”
Se observa el registro anteriormente creado
Modificación de forma de pago
Sobre la Forma de pago a editar damos clic en el ícono de lápiz para actualizar.
149
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se actualiza el campo requerido y se da clic en el botón actualizar.
Se observa mensaje “ACTUALIZACIÓN Forma de Pago Actualizada correctamente”
Activar/Desactivar forma de pago
Sobre la forma de pago dar clic en el visto bueno del botón a la derecha
desplazándose hacia la derecha para activar o a la izquierda para desactivar.
150
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se observa mensaje “ACTUALIZACION Forma de Pago Actualizada
correctamente”.
Nota: Lo anterior se agrega de acuerdo con los PBIs 612330 PIC - TM. Formas de pago
(Creación) y 630679 PIC - TM. Formas de pago (Modificación)
10.4.2.4 - Procedimiento segunda Forma de Pago
A través del procedimiento de segunda forma de pago, EXEC
rfd.SECOND_METHOD_OF_PAYMENT, se actualiza la forma de pago de una
solicitud según la lógica que cumple esta, teniendo en cuenta los siguientes campos:
número de reintetos, estado, canal, subcanal, forma de proceso, moneda, código
corporativo, procesador de pago o fecha de expiración de tarjeta de crédito si aplica,
los cuales varian según la lógica al momento de realizar la ejecucuón del
procedimiento.
Ingresar a la base de datos de PIC y ejecutar el procedimiento EXEC
rfd.SECOND_METHOD_OF_PAYMENT
151
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Considerando las solicitudes en base de datos y si cumplen las condiciones
incluidas en la lógica del procedimiento, actualiza la forma de pago a TR, KR, NC O
CR y actualiza los estados de las solicitudes a R o V.
Las tablas implicadas son:
PIC_FOP_PAYMENT_REQUEST (Se actualiza la forma de pago),
PIC_PAYMENT_REQUEST (se actualiza el estado) y PIC_PAYMENT_DETAIL (Se
inserta el nuevo registro con la nueva forma de pago y el estado en caso de aplicar
)
152
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con los PBI 737193 - PIC - Ajuste 2.1: Evaluar la
segunda forma de pago, 839955 - PIC - Ajuste Procedimiento que Evalúa la segunda forma
de pago - Casos 1 al 6, 15 y 16. Parte 2, 839723 - PIC - Ajuste Procedimiento que Evalúa
la segunda forma de pago - Caso 9: Cambiar de fop con TC a Voucher cuando la fecha de
expiración caducó Parte 2
10.4.2.5 - Procedimiento segunda Forma de Pago - Ajuste Procedimiento
Segunda Forma de Pago - Casos 15 y 16 TR
A continuación, se realiza la demostración con canal es MyIdTravel (5), ya que
aplica las mismas condiciones para el canal es Aviajar (6)
Se consulta la solicitud que cumple con las siguientes características:
1. Si la forma de pago actual es “TR” y 2. Si el número de intentos actual es igual o
mayor al parámetro definido para forma de pago con “TR” y 3. El estado actual es
rechazado “R” y 4. Si el valor recibido en el parámetro forced_retry es igual a Nulo
y 5. Si el canal es MyIdTravel (5) o el canal es Aviajar (6)
153
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se consulta el número de intentos parametrizados para la forma de pago, en este
caso está en 3 es decir que la solicitud cumple los 3 intentos máximos
parametrizados,
154
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se ejecuta el procedimiento EXEC rfd.SECOND_METHOD_OF_PAYMENT
El procedimiento imprime los datos que son requeridos para el caso 15
Nota: lo anterior se agrega de acuerdo con los PBI 902049 - PIC - Ajuste
Procedimiento Segunda Forma de Pago - Casos 15 y 16 TR
155
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
10.4.2.6 - Procedimiento segunda Forma de Pago - Reapertura de solicitudes
con transferencia bancaria - Ajuste Procedimiento Segunda Forma de Pago -
Casos CR
A continuación, se realiza la demostración con un caso (Los demás casos tienen el
mismo proceso, solo se debe adecuar la data a las condiciones especificadas en el
PBI)
Se consulta que una solicitud cumpla las siguientes condiciones
1. Si la forma de pago actual es “CR” y
2. El estado actual es rechazado “R” y
3. No tiene código corporativo y
4. Si el canal origen de la solicitud es Avianca.com (10) o Avianca Trade (4)
o Special Refund AV (8)
Para este ejemplo se utiliza el canal Avianca.com (10)
Se ejecuta el procedimiento
156
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se consulta nuevamente en la base de datos para validar la actualización de la
solicitud
Nota: lo anterior se agrega de acuerdo con los PBI 902041 - PIC - Reapertura de
solicitudes con transferencia bancaria - Ajuste Procedimiento Segunda Forma
de Pago - Casos CR
157
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
11.4.8. Moneda por País
11.4.9 Tipo de Cuenta
Este módulo permite la consulta por nombre, adición y modificación de tipos de
cuentas que se pueden manejar en PIC. A este módulo se puede acceder
seleccionando la opción Tipo de Cuenta, del menú Maestras.
Una vez seleccionada la opción, se mostrará por pantalla el listado con los
diferentes tipos de cuenta creados en base de datos hasta el momento. Se
mostrará el nombre de la cuenta, su código, una breve descripción y su estado. La
columna detalle está destinada para las acciones de modificación y cambio de
estado de un registro en particular.
En la pantalla se podrá observar el campo disponible para ingresar el criterio de
búsqueda para el campo Nombre de cuenta. Al ingresar el dato a buscar se
mostrará inmediatamente en pantalla los registros que obedecen el criterio.
ImagenXXXXXXXXXXXXXXX
Si no se encuentra el registro, el sistema mostrará un mensaje de validación
informando que el nombre de cuenta no está en la base de datos.
158
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Junto al campo de consulta por nombre, se encuentra el icono con el signo +, con
la etiqueta Agregar tipo de cuenta, en la cual al hacer click sobre el icono, se
deplegará una nueva ventana en donde se podrá agregar una nueva cuenta en el
sistema. En la ventana se debe diligenciar el nombre de la nueva cuenta en
español, inglés y portugués (Los nombres no podrán superar los 15 caracteres)
código de cuenta y descripción. A excepción del campo descripción, todos los
campos son obligatorios para la creación de una nueva cuenta. Se debe tener
presente que la nueva cuenta no puede tener el mismo código o nombre en
español de una cuenta ya existente en base de datos.
Imagen XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
En la columna se encuentra el switch que permite el cambio de estado, así como
el icono en forma de lápiz, con el que se podrán hacer modificaciones. Estas
acciones se realizan para un registro en particular, el que se relaciona en frente de
cada icono.
Imagen con el recuadro en el icono de modificar y del switch.XXXXXXXXXXXXX
Al cambiar de estado por el switch de Detalla, la cuenta seleccionada quedará
deshabilitada.
Imagen XXXXXXXXXXXXXXXXX
Para modificar alguna cuenta existente se debe presionar el icono del lápiz, con lo
que se desplegará una nueva ventana donde se podrá modificar cualquiera de los
campos. Los campos nombre de cuenta y código de cuenta no podrán ser
modificados si el valor ingresado es igual a un valor existente en base de datos.
Imagen XXXXXXXXXXXXXXXXXXXXXXXXX
En caso de ingresar valores existentes, se mostrará un popup informando que el
registro ya existe en base de datos.
Imagen con el pop up de cuenta existente XXXXXXXXXXXXXXXXXXX.
Adición del campo PAIS para Tipo de Cuenta
PBI relacionado
728884 PIC - Cambio Front End en TM. Tipo de Cuenta
159
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para el módulo Tipo de cuenta se adiciona la opción de adicionar un PAIS, aunque
no es obligatorio, esto aplica tanto para nuevos tipos de cuenta o editar un registro
actual
Primero se muestra el proceso para editar una cuenta ya existente y
posteriormente adicionarle un País
Se debe seleccionar el pais
160
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se despliega el listado de países disponibles
Para guardar se presiona en MODIFICAR
161
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Proceso en cuenta nueva
162
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
La cuenta nueva se visualizará con el PAIS seleccionado
10.4.8 Estados/Departamentos
En la maestra de estado/departamentos se permite Buscar, Crear o Modificar
Estados/Departamentos para un país.
163
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
10.4.8.1 Buscar Estado/Departamento por Nombre
Se ingresa el nombre del estado/departamento que se quiere buscar
10.4.8.2 Crear un Estado/Departamento
Al ingresar a la opción “Agregar estado” Se presenta los campos habilitados para
crear el estado
Se ingresa los datos de creación del estado/departamento
164
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se presenta mensaje de creación exitosa del Estado/Departamento
10.4.8.3 Modificar Estado/Departamento
Se ingresa por la opción en forma de para actualizar un estado/departamento
“lápiz”
Se presenta la pantalla para modificar un estado/departamento con todos los
campos habilitados
165
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se realiza la modificación
Se presenta mensaje de actualización exitosa del Estado/Departamento
Nota: Lo anterior se agrega de acuerdo con los PBI 630442 - PIC - TM. Estado/Depto. (Modificación), 625660 PIC - TM.
Estados / Departamentos (Creación), 649838 - PIC - TM. Estados / Departamentos Front End FINAL
11.4.10 Bancos
Este módulo permite visualizar los bancos guardados en base de datos en la tabla
maestra de PIC [master].[MST_BANK]. Para ingresar desde el fornt se da clic en
Maestras >> Bancos
166
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
En esta opción se podrá encontrar los diferentes Bancos con el país al que
pertenece, su código SAP y su respectivo SWIFT.
Se puede filtrar por el Nombre del banco y País
En caso de realizar una búsqueda por cualquiera de los filtros y no encontrar
resultados, se visualiza un mensaje informando que el criterio de búsqueda no
arroja resultados.
167
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Si el usuario lo desea, puede cambiar el idioma y las etiquetas cambiaran sin
modificar la funcionalidad.
El check del campo acciones permite activar o desactivar un banco. De igual
manera se agrega la opción de Agregar o crear un Banco en el botón +
Al presionar se despliega el siguiente pop up
168
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
El botón guardar no se activará hasta que los campos sean diligenciados de forma
correcta, de la siguiente manera:
Nombre de banco: Texto de longitud de 60 caracteres, es un campo obligatorio y
se puede repetir. Debe permitir letras minúsculas, mayúsculas, los números del 0
al 9, el punto, la coma, paréntesis de abre "(" y cierre ")", punto y coma ";", el y
"&", el espacio " " y el guion "-".
Clave de banco: Texto de longitud de 15 caracteres, es un campo obligatorio,
identificador único y permitirá almacenar la llave del banco que lo identifica en
SAP. Debe permitir únicamente letras minúsculas, mayúsculas y los números del 0
al 9.
Código de país: corresponde a la lista de nombres de países en estado activo
obtenido de la tabla maestra que permitirán relacionar el código ISO del país del
banco. Este campo es de selección única, obligatorio y deberá tener un filtro de
búsqueda de tipo texto que permita buscar el valor ingresado por coincidencia
sobre los resultados previamente consultados a la tabla maestra de países y debe
permitir restablecer los resultados (registros precargados) en la tabla de resultados
al quitar el valor del filtro de estado.
Swift: Texto de longitud de 11 caracteres y es un campo obligatorio. Debe permitir
únicamente letras mayúsculas y los números del 0 al 9.
Una vez diligenciados los datos de forma correcta, se realizará la creación del
nuevo banco.
También se tiene la opción modificación de Bancos, esta se da por medio del
botón en forma de lápiz.
169
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se despliega el siguiente popup, los campos que se muestran deben cumplir las
mismas características de la creación, no se va a activar el botón guardar hasta
que los campos cumplan las condiciones de expuestas en la creación.
Se aclara que los campos ID y Clave de banco no son editables en pantalla.
Se puede crear y actualizar un banco de tal manera que pueda tener la misma
clave de banco, siempre y cuando no se tenga el mismo País de otro banco que
esté creado previamente.
Una vez realizada una creación o actualización de banco, esta debe quedar
registrada en la tabla [PIC_LOGS_TRANSACTION]
170
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con el PBI:
• 684184 PIC - Cambio TM. Bancos
• 915995 PIC - Cambio TM. Bancos - Adición de funcionalidades para creación y actualización
11.5 REPORTES
11.5.1 Administrar Reporte
Este módulo permite crear y administrar los reportes que se podrán generar en el
aplicativo teniendo en cuenta los roles de los usuarios del sistema. Se aclara que
solo un rol técnico puede parametrizar o configurar los reportes.
Se ingresa por medio del menú “Reportes”, en la opción “Administrar reporte”.
El módulo presenta un buscador, el cual utiliza la cadena ingresada, para realizar la
búsqueda en cada uno de los campos de la grilla mostrada. La grilla presenta los
reportes creados en el aplicativo.
Para agregar un reporte, se da clic en la opción “Agregar reporte” donde el sistema
despliega una ventana que solicita los campos del reporte, que una vez solicitados
permite que se pueda agregar parámetros al reporte.
171
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Cuando se selecciona el botón “Agregar parámetro”, se muestra una nueva ventana
que permite seleccionar desde el campo “nombre”, el listado de parámetros creados
en el sistema, para poder asociarlos al reporte que se está creando.
Una vez asociado el parámetro, este se muestra en la sección de parámetros del
reporte.
Por último, para agregar el parámetro, se selecciona el botón “Guardar reporte”,
donde el sistema muestra un mensaje indicando la creación exitosa.
El módulo también nos permite visualizar la información de cada reporte creado.
Esto se puede realizar seleccionando el botón “Detalles”, que contiene también el
ícono de “ojo” sobre el reporte requerido.
Esto mostrará al usuario la información detallada del reporte creado, como su
nombre, el script de data generada, el script de generación formato, el tipo de
ejecución, los roles que pueden generar el reporte y los formatos en los cuales se
pueden generar.
172
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Otra funcionalidad que presenta el módulo es la de configurar los parámetros que
son usados por los reportes, para esto, se da clic en la opción “Configurar
parámetros”, donde se muestra los parámetros creados en el aplicativo.
Se presenta un buscador, el cual utiliza la cadena ingresada, para realizar la
búsqueda en cada uno de los campos de la grilla mostrada. La grilla presenta los
parámetros creados en el aplicativo.
Para crear un nuevo parámetro, se da clic en la opción “Crear parámetro” donde el
sistema despliega una ventana que solicita los campos del parámetro, que una vez
solicitados permite que se pueda agregar el parámetro en el aplicativo.
Las tablas relacionadas son:
Select * from [reports].[PIC_REP_REQUEST_GENERATION_REPORT_PARAMS]
Select * from [reports].[PIC_REP_REQUEST_GENERATION_REPORTS]
Select * from [reports].[PIC_REP_REGISTER_REPORTS]
Select * from [reports].[PIC_REP_REGISTER_REPORTS_PARAMS]
Nota: Lo anterior se agrega de acuerdo con los PBIs siguientes
697798 Reportes - Modulo de configuración de reportes.
697795 Reportes - Crear reporteador,
11.5.2 Generar Reporte
Este módulo permite la generación de los reportes que se encuentran creados en el
aplicativo y que, además, están disponibles para el rol del usuario que ha ingresado.
Se ingresa por medio del menú “Reportes”, en la opción “Generar reporte”.
173
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
En el módulo, se presenta un buscador de reportes, en el cual se pueda ingresar el
texto a buscar. La búsqueda se realiza de acuerdo con el nombre del reporte.
Para generar un reporte es necesario seleccionarlo, con lo cual el sistema
desplegará una ventana donde solicita ingresar los parámetros asociados al reporte.
Seguido a esto, y después de haber ingresado los parámetros solicitados para el
reporte, se da clic en el botón “Generar reporte”, donde se obtiene respuesta del
sistema.
174
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
El módulo también nos permite visualizar la información de cada reporte generado.
Esto se puede realizar seleccionando el botón “Detalles”, que contiene también el
ícono de “ojo” sobre el reporte requerido.
Esto mostrará al usuario la información detallada del reporte generado, como su
nombre, fecha de creación, usuario de creación, estado y parámetros asociados.
Finalmente, el módulo permite descargar el reporte, esto se hace seleccionando el
botón “Descargar” que se presenta para cada reporte generado.
Nota: Lo anterior se agrega de acuerdo a los siguientes PBIs
• 697797 Reportes - Modulo de generación de reportes.
• 697795 Reportes - Crear reporteador
11.5.2.1 Reporte de Usuarios
A través de la funcionalidad de reporte de usuario se genera la información de los
usuarios creados en el PIC
175
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Antes de generar el reporte se explica a continuación como configurar el reporte de
Usuarios para que se pueda generar siempre que sea requerido.
Para configurar y generar el reporte se realiza lo siguiente:
Creación de los parámetros del reporte:
Correo electrónico
Usamos la expresión regular: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
Roles activos
Usamos la siguiente consulta:
select ID_ROL, ROL_NAME_ES from [adm].[MST_ROL] where [STATUS] = 1
Estado
Usamos la siguiente consulta:
select '0' as cod, 'Inactivo' as det union select '1' as cod, 'Activo' as det
176
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Canales Activos
Usamos la siguiente consulta:
select CHANNEL_CODE, CHANNEL from [master].[MST_CHANNEL] where
[STATUS] = 1
Fecha Creación
Fecha inactivación.
Fecha Último accesso
177
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Configuración del reporte
Script de generacion:
execute [reports].[SP_REPORT_USERS] :p1,:p2,:p3,:p4,:p5,:p6,:p7
Asignación de parámetros al reporte:
Se da clic en agregar parámetro y se agrega los parámetros anteriormente
configurados
Email, Rol, Estado, Canal, Fecha Creación, Fecha Inactivación y Fecha ultimo
acceso
178
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Ahora ya finalizada la configuración del reporte lo vamos a generar en el menú de
Reportes >> Generar reporte
Buscamos el reporte de roles y lo seleccionamos
Se nos habilita las opciones de filtro deseadas que se configuraron en los
parámetros.
Seleccionar el formato en el que se desea descargar el reporte Xlsx o Csv
179
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Ingresar los datos del usuario especifico o campos para generar un reporte de
todos los usuarios a través de los filtros disponibles.
Para generar reporte de un usuario especifico ingresar los datos del usuario y dar
clic en “Generar Reporte”
Para descargar información con varios usuarios No ingresar el Email e ingresar los
filtros deseados para obtener en el reporte
180
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al generarse el reporte se presenta mensaje confirmando la generación del
reporte
Buscar el reporte en la lista de reportes y se presentan dos opciones “Resumen” Y
“Descargar”
Para ver el detalle del reporte dar clic en “Resumen”
181
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para bajar el Reporte Dar clic en “Descargar”
Según el formato seleccionado se descarga el reporte y queda disponible para Abrir
y consultar.
182
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con lo el PBI 799219 PIC - Reporte de Usuarios
11.5.2.2 Reporte de Roles
A través de la funcionalidad de reporte de Roles y Permisos se genera la
información de los Roles creados en el PIC.
Antes de generar el reporte se explica a continuación como configurar el reporte de
roles para que se pueda generar siempre que sea requerido.
Para configurar y generar el reporte se realiza lo siguiente:
Creación de los parámetros del reporte:
Rol
Creamos el parámetro para los roles con el siguiente valor:
select '-1' as id_rol, 'Todos' as Rol_name_es union all select
convert(varchar,ID_ROL,20), ROL_NAME_ES from [adm].[MST_ROL]
order by Rol_name_es asc
183
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Estado
Creamos el parámetro con el siguiente valor:
select '1' as id_status, 'Activo' as [status] union all
select '0' as id_status, 'Inactivo' as [status] union all
select '-1' as id_status, 'Todos' as [status]
Funcionalidad
utilizamos el siguiente valor:
select '-1' as id_rol, 'Todos' as MENU_NAME union all
select convert(varchar,ID_MENU,20), MENU_NAME from [adm].[MST_MENU]
order by MENU_NAME
184
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Crítico
utilizamos el siguiente valor:
select '-1' as id_critico, 'Ambos' as critic union all
select '1' as id_critico, 'Si' as critic union all
select '0' as id_critico, 'No' as critic order by critico
Configuración del reporte
Script de generacion:
execute [reports].[SP_REPORT_ROLES] :p1, :p2,:p3,:p4
Asignación de parámetros al reporte:
Se da clic en agregar parámetro y se agrega los parámetros anteriormente
configurados
185
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Ahora ya finalizada la configuración del reporte lo vamos a generar en el menú de
Reportes >> Generar reporte
Buscamos el reporte de roles y lo seleccionamos
Se nos habilita las opciones de filtro deseadas que se configuraron en los
parámetros.
Seleccionar el formato en el que se desea descargar el reporte Xlsx o Csv
186
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para generar reporte de un Rol, ingresar los datos específicos de éste y dar clic en
el botón “Generar reporte”
Para generar reporte de varios Roles, No ingresar el nombre de un Rol e ingresar
los filtros deseados.
187
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al generarse el reporte se presenta mensaje confirmando la generación del reporte
Buscar el reporte en la lista de reportes y se presentan dos opciones “Resumen” Y
“Descargar”
Para ver el detalle del reporte dar clic en “Resumen”
188
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para bajar el Reporte dar clic en “Descargar”, inmediatamente comienza la descarga
Según el formato seleccionado se descarga el reporte y queda disponible para Abrir
y consultar.
Nota: lo anterior se agrega de acuerdo con el PBI 829214 - PIC - Ajuste a Reporte
de Roles y permisos Parte 2
11.5.2.3 Reporte Casos Autorizados Valores Faltantes
189
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Este reporte, es un consolidado de los casos autorizados en SR desde el Módulo
de Valores Faltantes para disponer de la información necesaria para el seguimiento,
control y gestión operativa de los reembolsos asociados al proceso Ley DOT, con
el fin de consolidar y disponer de la información necesaria para el seguimiento,
control y gestión operativa de los reembolsos asociados al proceso Ley DOT,
permitiendo su descarga desde el PI mediante información obtenida de las tablas:
PIC_PAYMENT_REQUEST_VF
PIC_PAYMENT_DETAIL_VF
El PI permite la generación de un reporte que consolida todos los casos autorizados
desde el Módulo de Valores Faltantes:
Antes de generar el reporte se explica a continuación como configurar el reporte de
roles para que se pueda generar siempre que sea requerido.
Para configurar y generar el reporte se realiza lo siguiente:
Creación de los parámetros del reporte:
Número de solicitud
Creamos el parámetro para Número de solicitud:
Estado Solicitud
Creamos el parámetro con el siguiente valor:
190
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Tiquete
Creamos el parámetro con el siguiente valor:
Configuración del reporte
Script de generacion:
execute [reports].[SP_REPORT_MISSING_VALUES_VF] :p1,:p2,:p3
191
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Asignación de parámetros al reporte:
Se da clic en agregar parámetro y se agrega los parámetros anteriormente
configurados
Ahora ya finalizada la configuración del reporte lo vamos a generar en el menú de
Reportes >> Generar reporte
Buscamos el reporte Casos Autorizados Valores Faltantes y lo seleccionamos
192
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se nos habilita las opciones de filtro deseadas que se configuraron en los
parámetros.
Seleccionar el formato en el que se desea descargar el reporte Xlsx o Csv
193
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Ingresar los datos específicos que se requieran y dar clic en el botón “Generar
reporte” Al generarse el reporte se presenta mensaje confirmando la generación
del reporte
Buscar el reporte en la lista de reportes y se presentan dos opciones “Resumen” Y
“Descargar”
Para ver el detalle del reporte dar clic en “Resumen”
Para bajar el Reporte dar clic en “Descargar”, inmediatamente comienza la descarga
194
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Según el formato seleccionado se descarga el reporte y queda disponible para Abrir
y consultar.
Los campos del reporte son:
Campo
ID_PIC_PAYMENT_REQUEST
REFUND_REQUEST
TICKET
PNR
PAYMENT_STATUS_DESCRIPCION
REFUND_CURRENCY
REFUND_AMOUNT
REFUND_ACCOUNT_OWNER_NAME
195
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
REFUND_ACCOUNT_OWNER_LASTNAME
SOURCE
IATA
REFUND_EMAIL
REFUND_REQUEST_DATE
RECEIVED_DATE_BY_PI
ISSUE_DATE
SALE_AMOUNT
SALE_CURRENCY
FOP
PAYMENT_DATE
VOUCHER_NUMBER
CPG
La información refleja el estado más reciente registrado en PI.
• El campo PAYMENT_STATUS_DESCRIPCION: muestra la descripción
funcional del estado del pago.
• El campo PAYMENT_DATE: corresponde a la fecha de pago registrada en PI.
• El campo VOUCHER_NUMBER se muestra si el caso tiene voucher asociado.
• El campo CPG: Se muestra si existe programa de voucher asociado.
Nota: lo anterior se agrega de acuerdo con el PBI 1274263- PI - Workaround Ley
Dot - Reporte casos autorizados desde el Módulo de Valores Faltantes
11.5.2.4 Querys reporte Usuarios Auditoria
Se crea SP para generar un reporte con los datos de la maestra de usuarios.
Ejecutar el SP EXEC [rfd].[PIC_SP_USER_DATA_QUERY]
La consulta retorna para cada usuario, los siguientes campos:
Nombre de usuario (username),
Nombre del responsable de la cuenta,
Número de identificación,
Estado del usuario (activo, bloqueado, inactivo u otro)
Roles o privilegios asignados,
Fecha de creación del usuario,
196
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Fecha de última modificación,
Fecha de último acceso,
Tipo de usuario (directo o tercero)
Al final del informe, se incluye los siguientes metadatos:
a. Query Usada
b. Número de registros generados
c. Fecha y hora de generación del informe"
Nota: Lo anterior se agrega de acuerdo con el PBI
• 1151866 Refund - Queries de Usuarios
12. Reporte de RTS para TC y Voucher
12.1 Reporte Template to Output CCD to PIC Report
A través del reporte Template to Output CCD to PIC Report, se obtiene la
información las solicitudes que tiene forma de pago tarjeta de crédito, autorizadas
(F) y sin fecha de pago
Ingresar a: https://webappsdev.taca.com/websites/b1/rts/Login.aspx
Seleccionar el menú “Refund Queries” y buscar el sub-menú “Template to Output
to CCD to PIC”
197
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para descargar el reporte se da clic en la opción de descarga (Icono de disquete) y
se selecciona el formato deseado para el archivo descargado.
198
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al descargar el archivo correctamente queda disponible para abrir
199
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con los PBI 843869 RTS - TC – AJUSTE – [Salida
Temprana] Creación de Plantilla Req Input MP (Output de Pago - Pending CCD) - Reporting
Services.
12.2 Reporte Template to create Voucher PIC
A través del reporte Template to create Voucher PIC, se obtiene la información de
los reembolsos que se hallen en el estado "Autorizado (F)" y que todavía no tengan
asignada una fecha de pago, efectuados con el método de pago "ACC - VOUCHER"
sin voucher asignado.
Ingresar a: https://webappsdev.taca.com/websites/b1/rts/Login.aspx
Seleccionar el menú “Refund Queries” y buscar el sub-menú “Template to create
Voucher PIC”
200
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para descargar el reporte se da clic en la opción de descarga (Icono de disquete) y
se selecciona el formato deseado para el archivo descargado
201
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con los PBI 843870 - RTS – AJUSTE - [Salida
Temprana] Crear Query para Plantilla desde RTS para solicitud de voucher.
13. Procesos Adicionales
13.1. SAP
13.1.1. Envío de información a SAP CASH - CR
La tabla [rfd].[PIC_SAP_INTERFACE_OUT] almacena la información bancaria que
es enviada para iniciar el proceso de pagos en SAP de las solicitudes con FOP
Cash.
202
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
El procedimiento almacenado para enviar la información bancaria a SAP de los
casos por CASH es PIC_SEND_SAP_INTERFACE la lógica de enviar a la tabla de
salida de SAP los registros que tengan el campo UPDATE_STATUS = ‘Y’ en la tabla
rfd.PIC_BANK_DATA_INFORMATION y conservando la condición del estado de la
solicitud en la tabla PIC_FOP_PAYMENT_REQUEST con el campo
PAYMENT_STATUS = ‘V’.
En caso de encontrarse el campo UPDATE_STATUS = ‘N’, No se toman las
solicitudes como disponibles para ser enviadas al archivo de salida.
203
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se ejecuta el procedimiento:
Al cumplirse las condiciones de la solicitud, esta queda en la tabla de salida
PIC_SAP_INTERFACE_OUT, lista para ser enviar a SAP
204
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se configura el correo en la tabla de parámetros
Tabla: [master].[MST_PARAMETERS]
Campo identificador: PARAMETER_CODE
Campo valor: PARAMETER_VALUE
205
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
A través de la Function SEND_SAP se consume el procedimiento EXECUTE
@RC = [rfd].[PIC_SEND_SAP_INTERFACE]
Ingresar a la URL: https://portal.azure.com/#settings/directory
Ingresar a la Function az-fapp-picsap-use-qa, dar clic en Iniciar
206
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Si existen registros disponibles para enviar a SAP se almacenan en la tabla de
salida de SAP o en caso de presentarse un error en los datos disponibles para SAP,
como errores en la data o respuestas de estados INCOMPLETO por parte de SAP
se almacenan en la tabla PIC_SAP_INTERFACE_OUT_ERROR
Al existir datos FALLIDOS o en estado INCOMPLETO se envía Notificación con
archivo adjunto.
Cuando no se encuentra registros pendientes por procesar se envía una
notificación sin archivo adjunto y se presenta el siguiente mensaje.
207
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Cuando hay registros pendientes por procesar, pero no hay registros para enviar
en el archivo de FALLIDOS o INCOMPLETOS se presenta el siguiente mensaje.
En el envío de Datos se tiene en cuenta que para el envío de la información del
valor del reembolso si la moneda no está configurada en la maestra de Monedas
por Pais, se debe enviar siempre el valor recibido del reembolso con los dos
decimales. Pero si está configurada en la maestra se debe de respetar los decimales
configurados.
Ejemplo: Recibir solicitud con datos bancarios con otra moneda a la original
208
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
No se tiene moneda de GBP en el salvador
Se confirma envío de decimales
Se confirma en SAP
209
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Adicional se confirma el envío de información de los números de documentos a los
vendor correspondientes de acuerdo a lo configurado en el SP
PIC_SEND_SAP_INTERFACE
Nota: lo anterior se agrega de acuerdo con los PBI:
• 624259 PIC - Crear tabla SAP
• 754007 PIC - Ajuste en la function SEND_CASH y procedimiento de envío de pago Cash (Back End) - Update
Payment Status (to RO)
• 754015 PIC - Ajuste en la function SEND_CASH y procedimiento de envío de pago Cash (BD) - Update Payment
Status (to RO)
• 760732 PIC - Ajuste al procedimiento almacenado para que siempre tome los últimos datos Bancarios
• 791045 PIC - Ajuste en la function SEND_CASH de envío de pago Cash (Back End) - Update Payment Status (to RO)
• 1295949 [PI] Moneda Formularios datos bancarios – Ajuste proceso de envío a SAP
• 1308401 [PI] Configuración de Sudáfrica y China para procesamiento al Vendor 5
13.1.2. Procedimiento de Retorno
PIC_RETURN_SAP_UPDATE_PAYMENT_REQUEST_STATUS
A través del procedimiento
PIC_RETURN_SAP_UPDATE_PAYMENT_REQUEST_STATUS, se garantiza la
actualización de los datos bancarios de acuerdo con el número de intentos y
número de días parametrizado en la base de datos, aplica para las solicitudes que
vienen de los canales Aviajar (6) y MyIdTravel (5)
210
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
La lógica se cumple si el canal es Aviajar (6) y MyIdTravel (5), la forma de pago es
cash (CR) y se cumple la siguiente condición:
Si el número de veces (que se ha actualizado los datos debido a un rechazo
bancario) es mayor o igual comparado con el valor parametrizado, entonces debe
actualizar el estado finalizado “F” en la tabla PIC_PAYMENT_REQUEST en el
campo PAYMENT_STATUS (debido a que no tiene más oportunidades para
actualizar datos)
Si es menor se establece la siguiente lógica: Si el número de días trascurridos
teniendo en cuenta la última actualización de datos es mayor al valor parametrizado
en los días recibidos en el campo created_date y con valor "Y" en la tabla
PIC_BANK_DATA_INFORMATION entonces debe actualizar la transacción a
finalizada “F”.
De lo contrario no se realiza actualización de estado en el campo
PAYMENT_STATUS.
Ingresar a: https://portal.azure.com/#settings/directory
Se ejecuta la Function az-fapp-picvalidpaystat-use-qa que contiene el
procedimiento de la validación del número de intentos de actualización de datos
bancarios PIC_RETURN_SAP_UPDATE_PAYMENT_REQUEST_STATUS
Al realizarse una ejecucón exitosa, en la tabla PIC_PAYMENT_REQUEST se
actualiza el campo PAYMENT_STATUS del valor rechazado(R) a Finalizado (F).
211
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con el PBI 767313 - PIC - Update Payment Status
(to RO). Parte III (Function)
13.1.3. Retorno de información de SAP CASH - CR
A través del SP EXECUTE @RC = [rfd].[PIC_RETURN_SAP_INTERFACE], se
toman los datos retornados por SAP teniendo en cuenta el estado y el último estado
de la solicitud, para realizar las acciones de actualizar e insertar el estado de las
solicitudes para Rechazado o No procesado.
Inicialmente debe existir datos que cumplen con las condiciones para ser
procesados.
Se ejecuta el SP EXECUTE @RC = [rfd].[PIC_RETURN_SAP_INTERFACE]
212
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se obtiene estado igual a R o U, Según las condiciones del registro.
Cuando es pago fallido: [STATUS] = 'E' AND LAST_STATUS_SAP IN (NULL,
vacío, 'P', 'R', 'E')
• Insertar en la tabla PIC_PAYMENT_DETAILS con STATUS = R
• Actualizar el registro en la tabla PIC_PAYMENT_REQUEST con STATUS =
R
Cuando la creación es fallida: [STATUS] = 'R' AND LAST_STATUS_SAP IN
(NULL, vacío, 'R', 'E').
• Insertar en la tabla PIC_PAYMENT_DETAILS con STATUS = U
• Actualizar el registro en la tabla PIC_PAYMENT_REQUEST con STATUS = U
Estados de retorno SAP a PI
STATUS='P' THEN 0 -creación correcta
STATUS='R' THEN 1 -creación fallida
STATUS='Y' THEN 2 -pago correcto
STATUS='E' THEN 3 -pago fallido
213
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
El Integrador de Pagos verifica que al cumplirse el máximo permitido de intentos de
pago para actualizar los datos bancarios, al cumplirse ese valor el caso se Finaliza.
Parámetros para el número de reintentos y los días transcurridos para actualización:
SELECT * FROM [master].[MST_PARAMETERS] WHERE PARAMETER_CODE =
'RETRIES_UPDATE_BANK_DATA_INFO';
SELECT * FROM [master].[MST_PARAMETERS] WHERE PARAMETER_CODE =
'DAYS_FOR_UPDATE_BANK_DATA_INFO';
Se puede usar el siguiente query para tener registros que cumplen con las
condiciones iniciales, luego de esto sería revisar por cada Refund Request los
registros en la tabla Bank Data Information.
SELECT DISTINCT PAYMENT_REQ.REFUND_REQUEST, PAYMENT_REQ.PAYMENT_STATUS
FROM rfd.PIC_PAYMENT_REQUEST AS PAYMENT_REQ
INNER JOIN RFD.PIC_FOP_PAYMENT_REQUEST AS PAYMENT_FOP
ON PAYMENT_REQ.REFUND_REQUEST = PAYMENT_FOP.REFUND_REQUEST
WHERE
PAYMENT_REQ.PAYMENT_STATUS = 'R'
AND PAYMENT_FOP.FOP = 'CR'
AND PAYMENT_REQ.SOURCE IN (5, 6)
Nota: lo anterior se agrega de acuerdo con los PBI
767313 PIC - Update Payment Status (to RO). Parte III (Function) - Cash SAP Retorno
780183 - PIC - Update Payment Status (to RO). Parte II Final (BD) Modificar el proceso automático de la interfaz de retorno
para pago con cash a SAP
214
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
13.1.4. Envío de información a SAP ACM - NC
Desde el área de Reembolsos requieren que el integrador de pagos PIC almacene
los datos requeridos para el pago de notas débito ACM proveniente del flujo de
agencias de viaje a través del canal Avianca Trade y sean los cuales deben ser
utilizados para ejecutar el pago en SAP.
La tabla en la base de datos con los datos requeridos para las solicitudes de
reembolsos pertenecientes a notas débito ACM dirigidas a SAP es
[rfd].[PIC_SAP_ACM_INTERFACE_OUT] y este se llena al ejecutarse el SP
[PIC_SEND_ACM_INTERFACE]
Nuevo nombre y orden Tipo de dato Longitud Condición Observaciones Descripción Campo
[TRX_DATE] [varchar] 20 NULL Formato de tabla: DD/MM/YY, el bus deberá hacer la
transformacion para enviar a SAP A YYYYMMDD Fecha de la Transaccion
[GL_DATE] [varchar] 20 NULL Formato de tabla: DD/MM/YY, el bus deberá hacer la
transformacion para enviar a SAP A YYYYMMDD Fecha de Contabilizacion
[CUST_TRX_TYPE_NAME] [varchar] 20 NOT NUL Tipo de documento
[ORG_ID] [varchar] 4 NOT NUL Unidad Operacional
[CURRENCY_CODE] [varchar] 15 NOT NUL Moneda de la transaccion
[BATCH_SOURCE_NAME] [varchar] 50 NOT NUL Sistema generador de la informacion
[INTERFACE_LINE_ATTRIBUTE1] [varchar] 150 NOT NUL Numero de referencia de la transaccion de POF
[POSTING_KEY] [varchar] 2 NULL Llave de posteo
[ACCOUNT] [varchar] 240 NULL Cuenta contable de la transacción
[AMOUNT] [numeric] 20, 2 NOT NUL Monto de la transaccion
[TAX_CODE] [varchar] 50 NOT NUL Codigo del Impuesto
[TAXABLE_FLAG] [varchar] 1 NOT NUL
[DESCRIPTION] [varchar] 240 NOT NUL Descripcion de la transaccion
[TRX_NUMBER] [varchar] 20 NULL
[PRIMARY_SALES_REP_NUMBER] [varchar] 30 NULL Codigo ciudad de la venta
[CUSTOMER_NUMBER] [varchar] 240 NULL Codigo del cliente
[HEADER_ATTRIBUTE1] [varchar] 1 NOT NUL Indica si la factura se envia por email
[HEADER_ATTRIBUTE2] [varchar] 1 NOT NUL Indica Factura requiere soporte
[TRANSLATED_DESCRIPTION] [varchar] 1000 NULL Numero de Guia
[TRX_NUMBER_LEGAL] [varchar] 20 NULL Número de ACM
[STATUS] [varchar] 50 NULL El bus tomará unicamente los registros que esten en NEW Estado de la Transacción
[ERROR_MESSAGES] [varchar] max NULL Mensaje de Error
[COUNTRY] [varchar] 2 NULL Reporte Pais
[PAYMENT_INSTR] [varchar] 300 NULL Campo que se envia en blanco Instrucciones de Pago
[INVOICE_REMARK] [varchar] 300 NULL Campo que se envia en blanco Remark Factura
[INVOICE_CONCEPT] [varchar] 300 NULL Campo que se envia en blanco Concepto Factura
[BUSINESS_AREA] [varchar] 30 NULL Campo que se envia en blanco Municipio de la transacción
[TAX_BASE] [numeric] 20, 2 NOT NUL Monto base de impuesto
[TAX_AMOUNT] [numeric] 20, 2 NOT NUL Monto impuesto
[INVOICE_REASON] [varchar] 240 NULL Razon de Factura
[TAX_INDICATOR] [int] NULL
[CROSS_COMPANY] [varchar] 4 NULL
Cuando la function pasa se lleva la información a la tabla
[rfd].[PIC_SAP_ACM_INTERFACE_OUT] siempre y cuando la información esté
correcta se va a dejar la solicitud en estado “Processed”, ya Capa media lo toma y
lo envía a sapa cm dejándolo en estado “Completed”; Ya cuando sap le responde
con el número de ACM; capa media nos lo registra en los campos TRX_number y
215
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
TRX_number_legal y al pasar la function de sap acm este lo deja en estado
“Actualizado” y se actualiza en la tabla Detail y request.
Nota: Lo anterior es de acuerdo con los siguientes PBIs
• 968936 PIC - [E2E] - Function de procesamiento ACM - NC (Envío). Parte II [Final]
• 1039554 PIC - [E2E] - Ajuste Function de procesamiento ACM - NC (Envío).
13.1.5. Envío de información a SAP ACM – NC para Valores Faltantes
Ley DOT
Con el fin de dar cumplimiento a la Ley DOT, se implementó un workaround que
contempla ajustes funcionales y de parametrización en los sistemas involucrados
en el proceso de reembolsos.
Se evalua los registros almacenados en la tabla PIC_PAYMENT_REQUEST_VF.
Para estos registros, se aplica exactamente las mismas reglas, validaciones y
condiciones que actualmente se utilizan para el procesamiento y envío de los
reembolsos provenientes de PIC_PAYMENT_REQUEST, considerando los
siguientes ajustes:
Generación del registro de salida ACM
Cuando el ACM sea generado a partir de un registro de la tabla
PIC_PAYMENT_REQUEST_VF, en la tabla de salida
[rfd].[PIC_SAP_ACM_INTERFACE_OUT] el campo
INTERFACE_LINE_ATTRIBUTE1 se pobla con la siguiente estructura:
REFUNDACM + VF + REFUND_REQUEST
Donde REFUND_REQUEST corresponde al valor almacenado en la tabla
PIC_PAYMENT_REQUEST_VF.
216
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Retorno
Se incorpora una nueva regla en la Function encargada de procesar el retorno de
los ACM generados a través de la tabla [rfd].[PIC_SAP_ACM_INTERFACE_OUT].
La lógica se ejecuta de la siguiente manera:
Si el campo INTERFACE_LINE_ATTRIBUTE1 no contiene la cadena "VF", el
proceso continua con el comportamiento actual, poblando las tablas:
PIC_PAYMENT_REQUEST y PIC_PAYMENT_DETAIL
Si el campo INTERFACE_LINE_ATTRIBUTE1 contiene la cadena "VF", el proceso
pobla exclusivamente las siguientes tablas:
PIC_PAYMENT_REQUEST_VF y PIC_PAYMENT_DETAIL_VF
Al pasar la function este toma el num de acm y actualiza el estado a Pagado y en
la tabla de sap acm lo deja en estado completado.
217
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: Lo anterior es de acuerdo con los siguientes PBIs
• 1274263 PI – Workaround Ley Dot – Módulo de valores faltantes – Ajuste Function de procesamiento ACM (Envío &
Retorno)
13.2. Días máx para actualizar información de Datos Bancarios o se
Finaliza o Rechaza la solicitud
Parámetro de configuración de días de rechazo por no actualizar datos bancarios
Se valida los parámetros de configuración de los días para las notificaciones y
Finalización o Rechazo y activación de la 2da FOP.
Para temas de pruebas en ambiente qa se deja
DAYS_FOR_NTC19_BANK_DATA_INFO = 1 día y que el múltiplo al ser 2día se
notifique, en prd se dejaría en 7 dias para enviar la notificación a los 7 y 14 días
Y el parámetro DAYS_FOR_UPDATE_BANK_DATA_INFO=3 para que finalice o
Rechace la solicitud
Select * from [master].[MST_PARAMETERS] where parameter_code in
('DAYS_FOR_UPDATE_BANK_DATA_INFO','DAYS_FOR_NTC19_BANK_DATA_INFO')
Canal 6 - Se Finaliza solicitud
Se utiliza la reserva 124142 en la que se observa que se solicitó los datos bancarios
el día 2026-02-20 y se recordó la actualización de datos los días 2026-02-21 y 2026-
02-22 y al no recibir actualización de datos bancarios se procedió a finalizar la
solicitud.
218
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se confirma en AVR el envío de las notificaciones de recordación
SELECT TYP.NOTIF_TYPE_CODE, TYP.NOTIF_TYPE_NAME, CONF.LANG_CODE, NOTIF.*
FROM [rfd].[AVR_CONTROL_NOTIFICATIONS] NOTIF
JOIN [rfd].[AVR_TEMPLATE_CONFIGURATION] CONF ON NOTIF.TEMPLATE_ID = CONF.TEMPLATE_ID
JOIN [rfd].[AVR_TYPE_OF_NOTIFICATIONS] TYP ON CONF.[NOTIF_TYPE_CODE] =
TYP.[NOTIF_TYPE_CODE]
where NOTIF.REFUND_REQUEST = '124142'
ORDER BY SEND_DATE DESC
Y en Mozart se observa el rechazo
219
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Canal 5 - Se activa 2da fop
Para la activación de la 2da FOP esta depende de la configuración en la tabla
[rfd].[TEMP_SECOND_FORM_OF_PAYMENT_RULES]
Se utiliza la reserva 123646 en la que se observa que se solicitó los datos bancarios
el día 2026-02-20 y se recordó la actualización de datos los días 2026-02-21 y 2026-
02-22 y al no recibir actualización de datos bancarios se procedió a rechazar y se
activó la 2da fop.
Se confirma en AVR el envío de las notificaciones de recordación
SELECT TYP.NOTIF_TYPE_CODE, TYP.NOTIF_TYPE_NAME, CONF.LANG_CODE, NOTIF.*
FROM [rfd].[AVR_CONTROL_NOTIFICATIONS] NOTIF
JOIN [rfd].[AVR_TEMPLATE_CONFIGURATION] CONF ON NOTIF.TEMPLATE_ID = CONF.TEMPLATE_ID
JOIN [rfd].[AVR_TYPE_OF_NOTIFICATIONS] TYP ON CONF.[NOTIF_TYPE_CODE] =
TYP.[NOTIF_TYPE_CODE]
where NOTIF.REFUND_REQUEST = 123646
ORDER BY SEND_DATE DESC
220
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para este caso por temas de la data se presentó un error al enviar la notificación de pago por data
Se confirma que se actualiza en Mozart
Otros canales diferente a 5 y 6
Finalizado
Se utiliza el caso 124016 el cual el canal es 10 y corporativo por lo que se Finaliza
al no recibir la actualización de los datos bancarios.
Se observa que se solicitó los datos bancarios el día 2026-02-20 y se recordó la
actualización de datos los días 2026-02-21 y 2026-02-22 y al no recibir actualización
de datos bancarios se procedió a Finalizar la solicitud.
221
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se confirma en AVR el envío de las notificaciones de recordación
SELECT TYP.NOTIF_TYPE_CODE, TYP.NOTIF_TYPE_NAME, CONF.LANG_CODE, NOTIF.*
FROM [rfd].[AVR_CONTROL_NOTIFICATIONS] NOTIF
JOIN [rfd].[AVR_TEMPLATE_CONFIGURATION] CONF ON NOTIF.TEMPLATE_ID = CONF.TEMPLATE_ID
JOIN [rfd].[AVR_TYPE_OF_NOTIFICATIONS] TYP ON CONF.[NOTIF_TYPE_CODE] =
TYP.[NOTIF_TYPE_CODE]
where NOTIF.REFUND_REQUEST = 124016
ORDER BY SEND_DATE DESC
Se confirma que se actualiza en Mozart
222
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
2da FOP
Se utiliza el caso 123745 el cual el canal es 10 no corporativo por lo que se Rechaza
y se activa la 2da fop..
Se observa que se solicitó los datos bancarios el día 2026-02-20 y se recordó la
actualización de datos los días 2026-02-21 y 2026-02-22 y al no recibir actualización
de datos bancarios se procedió a Rechazar la solicitud y se activó la 2da fop
realizando el pago.
Se confirma en AVR el envío de las notificaciones de recordación
SELECT TYP.NOTIF_TYPE_CODE, TYP.NOTIF_TYPE_NAME, CONF.LANG_CODE, NOTIF.*
FROM [rfd].[AVR_CONTROL_NOTIFICATIONS] NOTIF
JOIN [rfd].[AVR_TEMPLATE_CONFIGURATION] CONF ON NOTIF.TEMPLATE_ID = CONF.TEMPLATE_ID
JOIN [rfd].[AVR_TYPE_OF_NOTIFICATIONS] TYP ON CONF.[NOTIF_TYPE_CODE] =
TYP.[NOTIF_TYPE_CODE]
where NOTIF.REFUND_REQUEST = 123745
ORDER BY SEND_DATE DESC
223
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se confirma que se actualiza en Mozart
Nota: Lo anterior se agrega de acuerdo con los siguientes PBIs
• 1181421 - PI - Modificación validación rechazo posterior a 21 días - Parte II
• 1165124 - PI - Ajustes
13.3. Function de Rezagos
Esta function verifica ciertas condiciones en los reembolsos que no tienen estados
finales y los envía al API de procesamiento, para que continúen el flujo de pago.
La function es az-rg-refundspic-use-qa >> az-fapp-picretrypayment-use-qa
224
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se verifica lo siguiente:
• Reembolsos con FOP TR:
Si el tipo de método de pago (FOP) es TR en la FOP payment Request
El estado del reembolso en la Payment Request es V y T
El tiempo de actualización en la payment request del reembolso es mayor a una
hora,
Entonces, el reembolso debe ser enviado al API de procesamiento. (Paso 3
#928243)
Vemos un ejemplo
En la tabla de logs [rfd].[PIC_LOGS_TRANSACTION] Se observa la ejecución
de la function de rezagos en log_source= 'Function_retry_payment'
225
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• Reembolsos con FOP LM:
Si el tipo de método de pago (FOP) es LM en la FOP payment Request
El estado del reembolso en la Payment Request es V y T
El tiempo de actualización en la payment request del reembolso es mayor a una
hora,
Entonces, el reembolso debe ser enviado al API de procesamiento. (API
desarrollada en el PBI #933867)
En la tabla de logs [rfd].[PIC_LOGS_TRANSACTION] Se observa la ejecución
de la function de rezagos en log_source= 'Function_retry_payment'
Se observa que se genera correctamente el transaction id y se queda a la espera de la respuesta de LM
para el pago
226
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• Reembolsos con FOP KR:
Si el tipo de método de pago (FOP) es KR en la FOP payment Request
El estado del reembolso es diferente a P, F o C
El tiempo de creación del reembolso es mayor a una hora,
Entonces, el reembolso debe ser enviado al API de procesamiento. (Paso 3 del
PBI #948164)
En la tabla de logs [rfd].[PIC_LOGS_TRANSACTION] Se observa la ejecución
de la function de rezagos en log_source= 'Function_retry_payment'
227
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
En todos los casos se realiza el llamado de Update Payment en caso de que todos
los registros de la misma solicitud tiene un estado Final y el campo
UPDATED_MOZART de al menos uno de los registros se encuentra "null" o con "0"
debe ser llamada la External API creada en el PBI #1010208 (Teniendo en cuenta
el envío de adjuntos)
Nota: lo anterior se agrega de acuerdo con el PBI:
• 1020325 PIC - E2E - Creación de Function de Rezagos. Parte III [Final]
13.4. Proceso de Contracargo – Chargeback
13.5. Proceso Estados de Pago – TR
Se crea los parámetros:
select * from [master].[MST_PARAMETERS] where parameter_code in
('FIRST_RETRY_AGE','SUBSEQUENT_RETRIES_AGE','STATUS_PROCESSORS','O
MITTED_CHANNELS_STATUS','STATUS_TO_REVIEW',
'PAYMENT_ROUTE_TO_REVIEW_STATUS','3DS','ATTEMPTS_STATUS')
228
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
select * from [master].[MST_PARAMETERS] where parameter_code in
('PARAM_SIN_CAPTURED_REASON_REJECTED','GET_INFO_SALE_CAPTUR
E_IN_TRANSACTION')
Se agrega campos en la tabla [rfd].[PIC_SALE_REPOSITORY]
Campo Origen (nodo) Ejemplo / Descripción
TXN_DATE
nodo:info-transaction, campo: txn-date
"2025-02-05 06:21:00" (mismo formato
que el original) - Formato en Fecha YYYY-MM-
DD HH:MM:SS
3DS
nodo: info-pay, campo: 3ds-check
"Authentication Success" - Formato
Varchar 50 caracteres máximo
PAYMENT_ROUTE
nodo: info-pay. campo: payment-route
Valor según response del servicio -
Formato Varchar 50 caracteres máximo
PSP_CAPTURE nodo: info_capture, campo: orchestrator
Nombre del orquestador del pago
(PSP)
y se crea [rfd].[PIC_SALE_REPOSITORY_HISTORY]
Al recibirse un caso de Mozart de TR, este se revisa en la GetInfoSale, al
confirmar datos de venta
229
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se inserta en la tabla [rfd].[PIC_SALE_REPOSITORY]. Y posterior se replica en la
tabla [rfd].[PIC_SALE_REPOSITORY_HISTORY]. Esta tabla no tiene validaciones
adicionales y funciona como una réplica en la que se almacenarán todos los
registros desde la primera invocación de la tabla [rfd].[PIC_SALE_REPOSITORY].
Nota: lo anterior se agrega de acuerdo con los PBIs
• 1130836 PI - [E2E] - Estados de pago - Creación de contador, parámetros
• 1130689 PI - [E2E] - Estados de pago - Almacenamiento / Creación de nuevos campos en Get Info Sale y tabla
histórica de la Get Info Sale
13.6. Proceso Creación de Voucher - KR
El Integrador de Pagos PI permite la integración con Qwikcilver (QC) para el
llamado de los servicios requeridos para la generación del Voucher, ya sea en
1era FOP o 2da fop de pago.
Cada vez que llega una solicitud de pago al integrador y la fop es Voucher - KR:
230
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se almacena el registro de la solicitud con estado "Validado" y con proceso de
pago "A" de automático; Se peticiona a capa media el API de creación de voucher
a través de los siguientes endpoints:
DEV: https://api-payments-dev.avtest.ink/api_qwikcilver_in/createVoucher
QA: https://api-payments-qa.avtest.ink/api_qwikcilver_in/createVoucher
PRD: https://api-payments.avianca.com/api_qwikcilver_in/createVoucher
Se tiene el siguiente request para el envio de creación de voucher
{
"create-voucher":{
"channel":"PIC",
"number-of-cards":"1",
"reference-number":"33068171",
"group-name":"AV Refund/ Payment feedback",
"amount":"94162000",
"currency":"COP",
"carrier":"AV",
"office-id":"1",
"first-name":"Edwin Stiven",
"last-name":"Mosquera Palacios",
"email":"DIDIER.BOHORQUEZ@DENARIO.COM.CO",
"mobile":""
}
}
Campo Mandatorio Tipo Descripción
Channel SI String Default: PIC
reference-number SI String Solicitud de reembolso asociada
number-of-cards SI String Cantidad de tarjetas, default: 1
group-name SI String Nombre del CPG, la lógica para poblar este campo
trabajado en el el PBI #649724
Valor de reembolso en voucher, no debe tener separador
amount SI String
de miles ni decimales, ejem el valor es 120.30, se envía
12030 Siempre se tomará los dos últimos dígitos como
decimales
currency SI String Moneda de la transacción
carrier SI String Aerolinea (AV / LR / TA)
agent NO String null
Office-id SI String default: 1
first-name SI String Concatenar primer y segundo nombre de la solicitud de
reembolso
last-name SI String concatenar primer y segundo apellido de la solicitud de
reembolso
Email SI String relacionar el correo relacionado en la solicitud de
reembolso
mobile NO String Vacío
231
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Ejemplo de la BD de PI
Se confirma en el log que se envía el request correspondiente
API Voucher Request: {"create-voucher":{"channel":"PIC","number-of-cards":"1","reference-
number":"2166","group-name":"LR Refund/ Voucher as
FOP","amount":"15400","currency":"USD","carrier":"AV","office-id":"1","first-name":"JACQUELINE","last-
name":"HAGMANN","email":"pruebas@qa.com","mobile":""}}
Nota: Lo anterior se agrega de acuerdo con los siguientes PBIs:
• 679889 PIC - API Creación de Voucher de QwickCilver. Escenario 1 Parte 2
• 729354 PIC - [Salida Temprana] Creación de Pantalla para reprocesar rechazos de voucher Parte I
• 1252225 PI – Ajuste – Creación de voucher (Create Voucher – campo “mobile”
13.7. Workaround Ley Dot (Canal 15 y 16)
Debido a la necesidad de dar cumplimiento a la Ley DOT mientras se completa el
desarrollo automatizado definitivo, se implementa un workaround que contempla
ajustes funcionales y de parametrización en los sistemas involucrados en el
proceso de reembolsos.
13.7.1. Tabla de reglas de segunda forma de pago – Ley DOT
Se agregar 3 nuevos campos a la tabla [rfd].[TEMP_SECOND_FORM_OF_PAYMENT_RULES]
para identificar por palabra clave y vigencia para la generación de voucher por
segunda forma de pago. (Debe verse reflejado en la Detail el programo tomado)
Nuevos campos:
• PROGRAM_AV: Programa de AV, el nombre completo (Solo informativo)
Tipo: Varchar (100)
• CPG_KEY: Este campo determina la palabra clave que se usa en el like
para la búsqueda del CPG a asignar en el voucher (ej: payment feedback o
232
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
ley dot)
Tipo: Varchar (50)
VIGENCIA: Este campo determina la vigencia (en años) que se debe tener
en cuenta para la asignación del CPG del voucher.
Tipo: Integer
SELECT * FROM [rfd].[TEMP_SECOND_FORM_OF_PAYMENT_RULES] WHERE SALE_CHANNEL IN
('15','16')
Se realiza el proceso de 2da fop de TR y CR para los canales 15 y 16 y se obtiene
el pago correcto y programa de acuerdo con las reglas realizadas.
Nota: al adicionar nuevos canales en la tabla previamente desarrollo debió agregar
la lógica por código que se va a recibir X canal.
A continuación, observamos del canal 15 tanto de TR a KR como de CR a KR
233
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
A continuación, observamos del canal 16 tanto de TR a KR como de CR a KR
234
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con los PBIs
• 1241198 PI - Workaround Ley Dot – Nuevos campos para reglas de segunda forma de pago
14. APIs
14.1. PaymentRequestEndPoint – PaymentOutput
El servicio del output de pago es consumido por capa media de forma automática,
se realizará un llamado con todos los registros que pertenezcan a la misma solicitud
Se ingresa en el enlace del swagger https://azwapppiccustextsuseqa.az-asev3-
use-qa.appserviceenvironment.net/Swagger/index.html
235
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se selecciona la tercera opción, el api llamado PaymentOutput, que relaciona los
cambios provenientes de Mozart. El request solicitado para esta api es el
siguiente:
[
{
"status":"A",
"refundRequest":"100066",
"refundAmountPnr":0,
"saleChannel":3,
"iata":80990475,
"pnr":"B558BK",
"saleTotalAmount":238,
"refundAccountOwnerName":"James",
"refundAccountOwnerLastname":"Trimarco",
"purchaseEmail":"",
"refundEmail":"pruebas@qa.com",
"frequentFlyerNumber":"",
"refundRequestDate":"20251020 14:21:17",
"recievedDateByPI":"2025-10-24T12:03:32.799626",
"paymentType":2,
"tickets":[
{
"ticket":2022477277968,
"originalTicketNumber":2022477277968,
"isTicket":"Y",
"issueDate":"20251021",
"refundCurrency":"USD",
"refundAmount":48,
"miles":0,
"saleCurrency":"USD",
"subChannel":"3",
"fopPayment":[
{
"fop":"TR",
"fopRefundCurrency":"USD",
"fopRefundAmount":48,
"bankCardHolder":"James Trimarco ",
"purchasePhone":"",
"addressCard":"",
"countryCard":"SV",
"cityCard":"",
"franchise":"CA",
"expiryDate":"1128",
"cardNumber":"518941XXXXXX6973",
"approvalCode":"111351"
}
]
}
]
}
]
Se debe tener en cuenta lo siguiente:
236
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• El campo forma de pago solo recibe los valores CR, TR, KR, NC, LM.
• El campo status recibe el valor A, este debe almacenarse como V.
• Si la solicitud de reembolso ya existe, se informa con un mensaje "La solicitud
de reembolso ya existe en nuestra base de datos"
• Se debe agrupar por RefundRequest, si uno de los tiquetes genera error o no
cumple con las validaciones, se rechaza toda la solicitud de reembolso.
• Los campos source, refundAccountOwnerName, refundAccountOwnerLastname y
refundEmail deben ser los mismos para cada tiquete perteneciente a una misma
solicitud de reembolso.
• El campo Refund Email debe ser obligatorio.
• El campo refundRequestDate debe tener el formato YYYYMMDD HH:mm:ss y el
campo issueDate debe tener formato YYYYMMDD.
• El campo moneda no puede ser null, puesto que es un campo obligatorio en la
inserción de la tabla pic_payment_request.
• Si el campo canal es igual a 8, debe tomar el valor que se tenga en el campo
subchannel. Este valor se define en primera instancia pero esta guardado en base de
datos en el parámetro CHANNEL_SR_PAYMENT_REQUEST.
• Si el campo subchannel tiene los valores "NDC, BT2 o AGY", el campo Canal debe
guardar el valor 4. Estos valores se definen en primera instancia pare están
guardados en base de datos en el parámetro
SUBCHANNEL_SR_PAYMENT_REQUEST.
• El campo Name_File_source de la tabla PIC_PAYMENT_REQUEST debe guardar la
palabra Mozart.
Las validaciones de tamaño y obligatoriedad se encuentran en la tabla Output Api adjunto
en el pbi 928188.
14.1.1. Tratamiento especial para canales BSP en flujo de pagos
Cuando el canal sea 3 o el canal sea 8 con subcanal 3, para que se manejen
correctamente las particularidades del tipo de pago y la actualización hacia Mozart cuando
estos sean BSP
• Integración de entrada (Output de Pago):
Cuando el canal sea 3 o el canal sea 8 y subcanal 3, si se recibe el tipo de pago CC
(en vez de TR), deberá:
➢ Almacenarse como si fuera TR.
➢ Tratarse como TR en todo el flujo de pago dentro del PIC.
• Actualización hacia Mozart (update):
237
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
En los casos donde el source sea 3 o el subchannel sea 3:
Cuando la FOP en el PIC sea "TR" Deberá enviar la siguiente información:
• "payment-fop":"CC",
• "Payment_FOP_Details": "444433XXXXXX1110" (Tarjeta Enmascarada
almacenada en [rfd].[PIC_FOP_PAYMENT_REQUEST]
• "ACM_Number": null
Los otros campos deben mantenerse como ya se envía
Se inserta con canal 3 con FOP TR
Y se observa en el log que se envia los datos correctamente a Mozart
Se envia solicitud a mozart: {"channel":3,"update-request-paid":
[{"request-number":"100066","process":"1","fop-dif":"","documents":[{"document-
num":"2022477277968","payment-fops":[{"payment-status":"P","payment-fop":"CC","payment-fop-
details":"518941XXXXXX6973","credit-card-entity":"CA","expiration-date":"20281101","approval-
code":"111351","acm-number":0,"payment-amount":48,"payment-currency":"USD","accounting-
date":"","payment-date":"20251028","payment-reference-number":"","rejection-reason":""}]}],"support-
attachments":[]}]}
Cuando la FOP en el PIC sea "NC" Deberá enviar la siguiente información:
• "payment-fop":"CC",
• "Payment_FOP_Details": "444433XXXXXX1110" (Tarjeta Enmascarada
almacenada en [rfd].[PIC_FOP_PAYMENT_REQUEST] - Ajuste
• "ACM_Number": Número de la ACM
Los otros campos deben mantenerse como ya se envía.
238
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se inserta con canal 3 con FOP NC
Se confirma que se envia los datos correctamente a Mozart
Se envia solicitud a mozart: {"channel":3,"update-request-paid":
[{"request-number":"100060","process":"1","fop-dif":"","documents":[{"document-
num":"1342148971700","payment-fops":[{"payment-status":"P","payment-fop":"CC","payment-fop-
details":"528209XXXXXX8136","credit-card-entity":null,"expiration-date":"","approval-code":"","acm-
number":8813400054,"payment-amount":150630,"payment-currency":"COP","accounting-
date":"","payment-date":"20251028","payment-reference-number":"","rejection-reason":""}]}],"support-
attachments":[]}]}
Nota: Lo anterior se agrega de acuerdo al PBI:
• 928188 PIC - E2E Output de Pago, solicitud de pago desde Mozart.
• 1051951 PIC - Tratamiento especial para canales BSP en flujo de pagos
• 1089550 PI - Ajuste para el tratamiento especial para canales BSP en flujo de pagos
14.1.2. Control de registros de TKT duplicados para pago
Teniendo en cuenta que están ingresando al PI desde la fuente algunas solicitudes
de pago sobre un mismo TKT se establece un control que restringe que puedan
ingresar.
Se tiene en cuenta la siguiente regla y aplica solo para registros de fuente: Mozart
• Llave: TKT+Fecha de venta (la fecha de venta se debe comparar sin horas
minutos segundos)
• Estados diferente a F no se permite ingresar al PI. Es decir, si se encuentra un
registro con la llave pero el estado es F, este si se permite registrar en el PI.
239
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• Las solicitudes que no ingresen al PI: Se rechaza el caso en Mozart; campo
payment status reject razon: There is refund request
• Se debe rechazar por TKT repetido, los demás si proceden a registrarse en el
PI.
Ejem
Vamos a insertar un tkt con fecha de venta que ya existe en PI
Obtenemos un rechazo del Pi informando que ya existe en el sistema
240
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: Lo anterior es de acuerdo al PBI:
1146007 PI - Control de registros de TKT duplicados para pago
14.1.3. PaymentRequestEndPoint – PaymentOutput para LM
Para la ejecución del api del output de pago para registros LM se debe tener en
cuenta que se puede recibir de los canales 9 y 11, con formas de pago LM y TR, y
guardan diferente estructura en el request.
Para canales 9 y 11 con FOP LM la estructura del request es:
[
{
"status": "A",
"refundRequest": "9338671101",
"refundAmountPnr": 2000,
"saleChannel": 11,
"iata": 7550271,
"pnr": "37XVD9",
"saleTotalAmount": 2000,
"refundAccountOwnerName": "Maria",
"refundAccountOwnerLastname": "Barrios",
"purchaseEmail": "maria.barrios@avianca.com",
"refundEmail": "maria.barrios@avianca.com",
"frequentFlyerNumber": "58745124512",
"refundRequestDate": "20241210 11:55:30",
"recievedDateByPI": "2024-12-10T01:22:25.445Z",
"paymentType": 2,
"tickets": [
{
"ticket": 2029338675501,
"originalTicketNumber": 2029338675501,
"isTicket": "Y",
241
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
"issueDate": "20250205",
"refundCurrency": "USD",
"refundAmount": 100,
"miles": 0,
"saleCurrency": "USD",
"subChannel": "LM",
"fopPayment": [
{
"fop": "LM",
"fopRefundCurrency": "USD",
"fopRefundAmount": 100,
"bankCardHolder": "MARIA BARRIOS",
"purchasePhone": "4568795451",
"addressCard": "Cr 16 # 32 - 65",
"countryCard": "CO",
"cityCard": "BOG",
"franchise": "",
"expiryDate": "",
"cardNumber": "",
"approvalCode": ""
}
]
}
]
}
]
Para canales 9 y 11 con FOP TR la estructura del request es:
[
{
"status": "A",
"refundRequest": "928243031001",
"refundAmountPnr": 18.0,
"saleChannel":11,
"iata": 7550271,
"pnr": "382VLY",
"saleTotalAmount": 18.0,
"refundAccountOwnerName": "maria",
"refundAccountOwnerLastname": "barrios",
"purchaseEmail": "mb@avianca.com",
"refundEmail": "mb@avianca.com",
"frequentFlyerNumber": "58745121001",
242
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
"refundRequestDate": "20240610 11:55:30",
"recievedDateByPI": "2024-12-10T01:22:25.445Z",
"paymentType": 2,
"tickets": [
{
"ticket":1339282431001,
"originalTicketNumber":1339282431001,
"isTicket": "Y",
"issueDate": "20250205",
"refundCurrency": "USD",
"refundAmount": 5,
"miles": 0,
"saleCurrency": "USD",
"subChannel": "LM",
"fopPayment": [
{
"fop": "TR",
"fopRefundCurrency": "USD",
"fopRefundAmount": 5,
"bankCardHolder": "maria barrios",
"purchasePhone": "4568795451",
"addressCard": "Cr 16 # 32 - 65",
"countryCard": "CO",
"cityCard": "BOG",
"franchise": "VI",
"expiryDate": "1230",
"cardNumber": "411111******1111",
"approvalCode": "332467"
}
]
}
]
}
]
Además, para las solicitudes de reembolso con forma de pago LM el transaction
unique id se construirá con la misma Base (Número de la solicitud del reembolso +
correlativo (05) + Unidad de Negocio (AV o LM)), es decir el transactionID para LM
estará basado únicamente a la Forma de Pago y asociará todos los registros que
la relacionan a esa forma de Pago (Es decir, todo lo que sea pago LM tendrá
correlativo 05)
243
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Solicitud Ticket FOP TransactionUniqueID
ABC123 111 LM ABC12305LM
ABC123 222 LM ABC12305LM
ABC123 333 TR ABC12301LM
La ejecución exitosa del proceso genera un registro por cada solicitud de
reembolso en estado I.
244
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
245
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
14.1.4. PaymentRequestEndPoint – PaymentOutput para TC
Para la ejecución del api del output de pago para registros de tarjeta de crédito se
debe tener en cuenta que se puede recibir desde cualquier canal (Recordando que
los canales 9 y 11 son para Lifemiles), con formas de pago TR, y guardan
diferente estructura en el request.
[
{
"status": "A",
"refundRequest": "928243031001",
"refundAmountPnr": 18.0,
"saleChannel":10,
"iata": 7550271,
"pnr": "382VLY",
"saleTotalAmount": 18.0,
"refundAccountOwnerName": "maria",
"refundAccountOwnerLastname": "barrios",
"purchaseEmail": "mb@avianca.com",
"refundEmail": "mb@avianca.com",
"frequentFlyerNumber": "58745121001",
"refundRequestDate": "20240610 11:55:30",
"recievedDateByPI": "2024-12-10T01:22:25.445Z",
"paymentType": 2,
"tickets": [
{
"ticket":1339282431001,
"originalTicketNumber":1339282431001,
"isTicket": "Y",
"issueDate": "20250205",
"refundCurrency": "USD",
"refundAmount": 5,
"miles": 0,
"saleCurrency": "USD",
"subChannel": "10",
"fopPayment": [
{
"fop": "TR",
"fopRefundCurrency": "USD",
"fopRefundAmount": 5,
"bankCardHolder": "maria barrios",
"purchasePhone": "4568795451",
"addressCard": "Cr 16 # 32 - 65",
246
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
"countryCard": "CO",
"cityCard": "BOG",
"franchise": "VI",
"expiryDate": "1230",
"cardNumber": "411111******1111",
"approvalCode": "332467"
}
]
}
]
}
]
Al ingresar una solicitud de reembolso exitosa, esta debe guardarse en base de
datos de la siguiente manera:
14.2. Servicio de procesamiento para evaluar el estado capture
Cuando se evalúa el "capture-status" en el api de la getinfosale de los registros que
ingresan a través del output de Pago (Mozart) se tiene lo siguiente:
Para las transacciones que NO se encuentran en la API de la Get Info Sale continua
el flujo ya establecido.
247
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para las transacciones que NO presenten estado de venta "capture-status" de
acuerdo con el parámetro 'GET_INFO_SALE_CAPTURE_IN_TRANSACTION' y si
se encuentran en la API de la Get Info Sale, se implementa lo siguiente:
• El registro cambia a estado "I" en la tabla [rfd].[PIC_PAYMENT_REQUEST]
• Se adiciona un registro en la tabla [rfd].[PIC_PAYMENT_DETAIL] con la razón
"01 - Pendiente Captured" (Parámetro:
'PARAM_SIN_CAPTURED_REASON_REJECTED') & concatenar el Intento
ejem "01 - Pendiente Captured, Intento 1"(campo REJECTION_REASON).
• Se registra la operación en la tabla [rfd].[PIC_LOGS_TRANSACTION]
incluyendo: PNR, solicitud asociada y número de reintento
Para las transacciones que presenten estado de venta "Captured" de acuerdo con
el parámetro definido, se continua con el flujo normal del proceso de pago.
248
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se encuentra en la get info sale
El estado de la get info sale se observa configurado en el parámetro de capture
Se ejecuta el Pyment Output y se inserta y se procesa correctamente en el PI
Nota: Lo anterior se agrega de acuerdo al PBI:
• 1124050 PI - [E2E] - Captured - Ajuste al servicio de procesamiento para que evaluar el capture. Parte III
249
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
14.3. Segunda forma de Pago – Payment Output Mozart
El Api Payment Output para Mozart está en la capacidad de enviar a una segunda
forma de pago aquellas solicitudes de reembolsos que cumplan con las condiciones
especificadas en la tabla [rfd].[TEMP_SECOND_FORM_OF_PAYMENT_RULES].
De esta forma el output de pago para Mozart se comportará y enviará a una segunda
forma de pago obedeciendo a la forma de pago con la que se inicia el proceso, se
tiene en cuenta el número de reintentos definido en la tabla
[master].[MST_PAYMENT_RETRIES] (Los números de reintentos no hacen parte
del desarrollo del pbi mencionado inicialmente.)
FOP_
IN
STATUS_C
ODE
TOUR_CO
DE
SALE_CHAN
NEL
SUB_CHAN
NEL
FORCED_RE
TRY
BANK_SUPP
ORT
PAYMENT_PRO
CESS
REFUND_CURRE
NCY
PS
P
EXPIRY_D
ATE
FOP_O
UT
STATUS_CODE_OU
T
NU
TR R 0 10 N
LL KR V
Nota: Lo anterior se agrega de acuerdo al PBI
• 1000067 - PIC - Segunda forma de Pago
• 1016946 se adiciona el campo Status_code_out)
•
14.3.1. Cuando la segunda fop es CASH-CR - Notificación
250
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para la actualización de datos Bancarios se debe de tener en cuenta el parámetro
RETRIES_UPDATE_BANK_DATA_INFO el cual valida los intentos de actualización
de Datos bancarios de acuerdo con lo recibido en la tabla
[rfd].[PIC_BANK_DATA_INFORMATION], si se supera el numero parametrizado
estos casos de Finalizan.
Aplica a los tres tipos de medios de pago: Cash, Tarjeta de Crédito (TR) y Millas
(LM).
Cuando se tiene un rechazo y se activa la segunda fop de acuerdo con lo
parametrizado en la tabla [rfd].[TEMP_SECOND_FORM_OF_PAYMENT_RULES]
se envía una notificación al cliente, siempre y cuando exista la información de los
pasajeros en AVR.
Validar que exista el registro aqui en AVR
SELECT * FROM [rfd].[AVR_INFORMATION_ADDITIONAL_PASSENGER] where refund_request in ('')
SELECT * FROM [rfd].[AVR_INFORMATION_PASSENGER] where refund_request in ('')
Y posterior confirmar aqui las notificaciones
SELECT TYP.NOTIF_TYPE_CODE, TYP.NOTIF_TYPE_NAME, CONF.LANG_CODE, NOTIF.*
FROM [rfd].[AVR_CONTROL_NOTIFICATIONS] NOTIF
JOIN [az-sqla-avref-use-qa].[rfd].[AVR_TEMPLATE_CONFIGURATION] CONF ON NOTIF.TEMPLATE_ID =
CONF.TEMPLATE_ID
JOIN [az-sqla-avref-use-qa].[rfd].[AVR_TYPE_OF_NOTIFICATIONS] TYP ON CONF.[NOTIF_TYPE_CODE]
= TYP.[NOTIF_TYPE_CODE]
--where CONF.NOTIF_TYPE_CODE = 'NTC9'
--and NOTIF.CONTROL_EMAIL_ID = '4328'
where NOTIF.REFUND_REQUEST = '122398'
ORDER BY SEND_DATE DESC
Cash (Interfaz de retorno / y de envío SAP)
Si se evalúa la segunda forma de pago y el resultado de la segunda forma de
pago. es CR, y el canal pertenece a: 5, 6, 15, 16 (Parámetro) o cualquier canal con
código corporativo
Entonces:
Enviar notificación NTC8.
Cambiar el estado a (R) en la Payment Request
Crear un campo en la Payment Request que reciba un 1 o 0 como resultado
exitoso o fallido del envío de la notificación (NOTIFICATION_SENT)
251
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Ejem
Se confirma notificación en AVR
Se confirma la notificación por correo
Tarjeta de Crédito (TR): (Proceso automático y manual - Resultado API
Refund, Plantillas Manual y send Refund - Payflow)
Si el estado es de rechazo.
Evaluar la segunda forma de pago Inmediatamente (Ya se hace)
252
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Si el resultado es CR.
Y el canal es 5, 6, 15, 16 (Parámetro) o cualquier canal con código corporativo.
Entonces:
Enviar notificación NTC8.
Cambiar el estado a (R) en la Payment Request
Crear un campo en la Payment Request que reciba un 1 o 0 como resultado
exitoso o fallido del envío de la notificación (NOTIFICATION_SENT)
Ejemplo
Se confirma notificación en AVR
Se confirma la notificación por correo
253
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Tarjeta de Crédito (LM): (Proceso automático- Resultado API Refund, y send
Refund - Payflow)
Si el estado es de rechazo.
Evaluar la segunda forma de pago Inmediatamente (Ya se hace
Si el resultado es CR.
Y el canal es 5, 6, 15, 16 (Parámetro) cualquier canal con código corporativo.
Entonces:
Enviar notificación NTC8.
Cambiar el estado a (R) en la Payment Request
Crear un campo en la Payment Request que reciba un 1 o 0 como resultado
exitoso o fallido del envío de la notificación (NOTIFICATION_SENT)
Ejem
al tratar de hacer la prueba con el canal 5 con fop LM no lo permite
254
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al tratar de hacer el rechazo por el APISendInfoResult este no reconoce solicitud
como LM si el source de la request es diferente a 9 ó 11Image
Pero si lo cambio a 11 o 9 ahi si lo reconoce
255
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: Lo anterior se agrega de acuerdo con el PBI
• 1010207 PIC - Actualizar Datos Bancarios - Generar Notificaciones. Parte II
14.3.2. Modificación campos rechazo con segunda forma de pago.
Atendiendo el pbi 1051548, se actualiza la revisión de segunda forma de pago
para que cuando en la tabla de segunda forma de pago finalice en un estado R en
su segunda forma de pago, los campos REJECTION_REASON y
REJECTED_DATE en la tabla de pic_payment_detail deben ser poblados con la
información del rechazo inmediatamente anterior, que dio origen a la evaluación
de dicha segunda forma de pago.
256
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
14.4. Payment Refund Request
Como usuario de Medios de pago se requiere que el sistema almacene para toda
solicitud de pago un identificador único de transacción relacionado a cada tiquete o
EMD asociado al mismo número de solicitud de reembolso.
Se realiza un ajuste al proceso de creación de “Transaction Unique ID” para evaluar
también el subcanal dentro de la API.
Al crear el “Transaction Unique ID” de acuerdo con el PBI #616023, se debe ajustar
la condición de asignación de unidad de negocio por verificar el si el subcanal es
"11"modifique la condición de la siguiente manera:
Si al menos uno de los campos (Pueden ser los dos campos), subcanal o canal está
relacionado el canal 11 (LifeMiles) se cataloga el registro como "LM", de lo contrario
catalogarlo como "AV".
Se ingresa al swagger https://azwapppiccustextsuseqa.az-asev3-use-
qa.appserviceenvironment.net/Swagger/index.html, y se ubica el api
“PaymentOutput/v2” dentro de la sección “PaymentRequestsEndPoints”
.
Se modifica y envía la API con subcanal igual a 11.
257
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se valida en la base de datos que efectivamente se cataloga el registro como “LM”.
Se modifica y envía la API con canal igual a 11.
258
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se valida en la base de datos que efectivamente se cataloga el registro como “LM”.
Se modifica y envía la API con canal y subcanal diferentes a 11.
259
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se valida en la base de datos que efectivamente se cataloga el registro como “AV”.
Nota: Lo anterior se agrega de acuerdo con el siguiente PBI: 728882 PIC - Ajuste al
Transaction Unique ID.
14.5. Get Master Data SAP: Get currency list
Como usuario de Tesorería se requiere que el Integrador de Pagos PIC exponga
una API con un método que permita actualizar o insertar los registros de la tabla
maestra de monedas para que el sistema SAP pueda llamar cada servicio.
Se ingresa a https://azwapppiccustextsuseqa.az-asev3-use-
qa.appserviceenvironment.net/Swagger/index.html, y se ubica el api
“CreateUpdate” dentro de la sección “CurrencyEndPoints”.
260
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para insertar un registro el servicio debe leer como entrada un objeto JSON,
recibiendo en el elemento “recordType” el valor “02” y en el elemento “operation” el
valor “C”.
Se valida en la tabla “master.MST_CURRENCY” la creación exitosa del registro
enviado en la API.
261
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para modificar un registro el servicio debe leer como entrada un objeto JSON,
recibiendo en el elemento “recordType” el valor “02” y en el elemento “operation” el
valor “M”.
Se valida en la tabla “master.MST_CURRENCY” la modificación exitosa del registro
enviado en la API.
262
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
La API está en la capacidad de controlar casos donde no se puede ejecutar, es
decir, donde se presente error de acuerdo con lo solicitado. En este caso, se
presenta en valor diferente de “02” en el campo “recordType”.
En este caso, el servicio responde que el campo “recordType” tiene un valor no
determinado.
263
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: Lo anterior se agrega de acuerdo con el siguiente PBI: 708014 PIC - API Get
Master Data SAP: Get currency list.
14.6. API PicTempControl/create
A través de la API PicTempControl/create, se puede cargar en la tabla
rfd.PIC_CONTROL_REFUND_REQUEST de la base de datos de PIC las
solicitudes de reembolso para ser agrupadas en una solicitud.
Ingresar a la URL: https://azwapppiccustextsuseqa.az-asev3-use-
qa.appserviceenvironment.net/Swagger/index.html
Buscar la API PicTempControl/create, Dar clic en “Try it out”, ingresar los datos
de las solicitudes que se desean cargar y dar clic en ejecutar
264
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
La API genera un “Response” con mensaje informativo de ejecución correcta
Se inserta correctamente el registro en la tabla
rfd.PIC_CONTROL_REFUND_REQUEST
265
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con los PBI 697808 PIC - Creación de API para
cargar en una tabla de control las solicitudes de reembolso para ser agrupadas en una
solicitud. Parte III (Final)
14.7. API ControlRequest Reject
A través de API controlReuqest/Reject, se puede rechazar una solicitud cuando
es el último registro y estado diferente a rechazado
Ingresar a la URL: https://azwapppiccustextsuseqa.az-asev3-use-
qa.appserviceenvironment.net/Swagger/index.html
Tener una solicitud con último registro si estado asignado.
Ingresar a la API controlReuqest/Reject , Dar clic en la opción “Try It Out” y dar
clic en Ejecutar
266
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Si es correcta la información ingresada se obtiene en el “Response” de la API con
mensaje informativo indicando la correcta ejecución de la API
Se inserta en la tabla control el estado “Reject” de la solicitud ingresada
267
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con los PBI 688370 PIC - Creación de API para
rechazar las solicitudes de reembolso en la tabla temporal. Parte II
14.8. API GetChargeback
A través de la API GetChargeback se consume el procedimiento
SP_VALIDATE_EXIST_CVS que se encuentra en la base de datos de CVS y
contiene la lógica para responder si un ticket tiene chargeback o no tiene
chargeback (contracargo)
Ingresar a https://azwapppiccustextsuseqa.az-asev3-use-
qa.appserviceenvironment.net/Swagger/index.html
Buscar la API GetChargeback, dar clic en la opción “Try it out”, se habilitan los
campos para consultar.
Como precondición para consultar un ticket, debe existir en la base de datos de
CVS y de PIC, se debe poblar para cada ticket los siguientes campos igual como
se encuentra en la base de datos de CVS:
1. Cuando es tarjeta de crédito:
1 -
“document" = “Ticket + número de Aerolínea” en la tabla PIC_PAYMENT_REQUEST,
PIC_FOP_PAYMENT_REQUEST, PIC_SALE_REPOSITORY y PIC_PAYMENT_DETAIL
2 -
"date-sale"= ISSUE_DATE en la tabla PIC_PAYMENT_REQUEST
3 -
"card-number" = “CARD_NUMBER” en la tabla PIC_FOP_PAYMENT_REQUEST
4-
"ammount"= SALE_TOTAL_AMOUNT en la tabla PIC_PAYMENT_REQUEST o
VALUE en la tabla PIC_SALE_REPOSITORY (El valor se busca en la
PAYMENT_REQUEST cuando en la SALE_REPOSITORY no existe valor)
268
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
5 -
"approval-code" = APPROVAL_CODE en la tabla PIC_FOP_PAYMENT_REQUEST y
PIC_SALE_REPOSITORY
2. Cuando es diferente a tarjeta de crédito:
1 -
“document" = “Ticket + número de Aerolínea” en la tabla PIC_PAYMENT_REQUEST,
PIC_FOP_PAYMENT_REQUEST y PIC_SALE_REPOSITORY
2 -
"date-sale"= ISSUE_DATE en la tabla PIC_PAYMENT_REQUEST
3 -
"ammount"= SALE_TOTAL_AMOUNT en la tabla PIC_PAYMENT_REQUEST
Para consultar si un Ticket tiene chargeback, cuando su forma de pago es TR
(Tarjeta de crédito) enviar en el request de la API el
TRANSACTION_UNIQUED_ID.
Al ticket tener chargeback se presenta mensaje indicando que tiene contracargo y
finalizado exitosamente en el “response”.
Se Actualiza en la tabla PIC_PAYMENT_REQUEST el estado a “C” (cerrado) e
insertando en la tabla PIC_PAYMENT_DETAIL el registro con estado C, rezón y
código de rechazo.
269
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Para consultar si un Ticket que tiene chargeback cuando su forma de pago es
Diferente a Tarjeta de crédito) enviar en el “request” de la API el “refund_Request”
y el ticket o lista de tickets asociados.
Al ticket tener chargeback se presenta mensaje indicando que tiene contracargo,
finalizado exitosamente. Actualizando en la tabla PIC_PAYMENT_REQUEST el
estado a “C” (cerrado) e insertando en la tabla PIC_PAYMENT_DETAIL el registro
con estado C, rezón y código de rechazo.
270
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
En caso de existir un Time_Out se envía una notificación al correo que se
encuentre parametrizado.
La tabla y campos que contiene los parámetros del Time_Out se consulta de la
siguiente forma en SQL:
SELECT * FROM [az-sqla-piccust-use-qa].[master].[MST_PARAMETERS] where
PARAMETER_CODE = 'SERVER_ERROR_HANDLING_RETRIES' (el número
de intentos)
271
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
SELECT * FROM [az-sqla-piccust-use-qa].[master].[MST_PARAMETERS] where
PARAMETER_CODE = 'SERVER_ERROR_HANDLING_TIMEOUT' (contiene los
segundos que espera la API)
SELECT * FROM [az-sqla-piccust-use-qa].[master].[MST_PARAMETERS] where
PARAMETER_CODE = 'NOTIFICATION_EMAIL_API_LOADED_TEMPLATE'
(Contiene el correo Electronico donde llegará la notificación)
En caso de Existir un fallo en la comunicación o respuesta de la API
Se actualiza el campo PAYMENT_PROCESS a “O”
272
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se registra en la tabla PIC_LOGS_TRANSACTION
Nota: lo anterior se agrega de acuerdo con los PBI 839401 - PIC - [Salida Temprana] API Chargeback y validaciones
necesarias de Chargeback Parte 3
273
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
14.9. External API Insert Refund Status
A través de la API Insert Refund Status se consume la respuesta de la API
InsertRefundStatus
Ingresar a: https://azwapppiccustextsuseqa.az-asev3-use-
qa.appserviceenvironment.net/Swagger/index.html
Buscar la API InsertRefundStatusEndpoints, Dar clic en “Try it Out”, ingresar
los datos requeridos en cada campo y dar clic en ejecutar
Se obtiene la res puesta de la API correctamente al ingresar los campos
requeridos.
274
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: lo anterior se agrega de acuerdo con los PBI
852886 - PIC - [Salida Temprana] External API Insert Refund Status - API para actualizar estado de reembolso en la
Payment Database
14.10. API Comprobante de Pago
Con el API UploadPaymentCheckerFileEndpoints se genera los comprobantes de
pago según su lenguaje (ES, EN, PT, FR) para la forma de pago TR o CR
Ingresar al swagger:
https://azwapppiccustextsuseqa.az-asev3-use-qa.appserviceenvironment.net/Swagger/index.html
Se digita el Refund request para el comprobante de pago y este se genera en los
4 idiomas de la fop correspondiente
275
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
El comprobante queda en el blob storage az-rg-refundspic-use-qa >>
Comprobantes de pago
Descargar el comprobante de pago
En la base de datos del integrador de pago se comprueba los valores que se
presentan en el comprobante En la tabla: PIC_PAYMENT_REQUEST
276
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se realiza el proceso para Tarjeta de crédito – TR
Se confirma en PI que se encuentre Pagado en TR
Se valida en AVR que se haya enviado la notificación NTC12
SELECT TYP.NOTIF_TYPE_CODE, TYP.NOTIF_TYPE_NAME, CONF.LANG_CODE, NOTIF.*
FROM [rfd].[AVR_CONTROL_NOTIFICATIONS] NOTIF
JOIN [az-sqla-avref-use-qa].[rfd].[AVR_TEMPLATE_CONFIGURATION] CONF ON NOTIF.TEMPLATE_ID = CONF.TEMPLATE_ID
JOIN [az-sqla-avref-use-qa].[rfd].[AVR_TYPE_OF_NOTIFICATIONS] TYP ON CONF.[NOTIF_TYPE_CODE] = TYP.[NOTIF_TYPE_CODE]
--where CONF.NOTIF_TYPE_CODE = 'NTC12'
where NOTIF.REFUND_REQUEST in ('192899')
ORDER BY SEND_DATE DESC
Se ingresa correctamente al Blob Storage az-rg-refundspic-use-qa >>
Comprobantes de pago
277
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se confirma comprobante correcto en FR de TR
Adicional en el flujo E2E se envia la notificación al correo con el comprobante adjunto
278
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se realiza el proceso para Cash o Transferencia Bancaria – CR
Se confirma en PI que se encuentre Pagado en CR
Se valida en AVR que se haya enviado la notificación NTC13
SELECT TYP.NOTIF_TYPE_CODE, TYP.NOTIF_TYPE_NAME, CONF.LANG_CODE, NOTIF.*
FROM [rfd].[AVR_CONTROL_NOTIFICATIONS] NOTIF
JOIN [az-sqla-avref-use-qa].[rfd].[AVR_TEMPLATE_CONFIGURATION] CONF ON NOTIF.TEMPLATE_ID = CONF.TEMPLATE_ID
JOIN [az-sqla-avref-use-qa].[rfd].[AVR_TYPE_OF_NOTIFICATIONS] TYP ON CONF.[NOTIF_TYPE_CODE] = TYP.[NOTIF_TYPE_CODE]
--where CONF.NOTIF_TYPE_CODE = 'NTC13'
where NOTIF.REFUND_REQUEST in ('192899')
ORDER BY SEND_DATE DESC
Se ingresa correctamente al Blob Storage az-rg-refundspic-use-qa >>
Comprobantes de pago
Se confirma comprobante correcto en FR de CR
279
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Adicional en el flujo E2E se envia la notificación al correo con el comprobante adjunto
Nota: Lo anterior se agrega de acuerdo con el PBI
• 1269349 PI – Experiencia Francés - Ajuste Creación comprobante de pago
14.11. API Bank
Data
Information
_
_
Se requiere almacenar la información que será enviada por canales a través de la Capa
media cada vez que llegue una solicitud de reembolsos con forma de pago (FOP) cash
280
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se crea el api en la external del swager del PIC https://azwapppiccustextsuseqa.az-asev3-
use-qa.appserviceenvironment.net/Swagger/index.html
O en el Postman con el curl
curl -X 'POST' \
'https://azwapppiccustextsuseqa.az-asev3-use-
qa.appserviceenvironment.net/BankDataInformation' \
-H 'accept: text/plain' \
-H 'Content-Type: application/json' \
-d ' {
"identificationCode": "string",
"typePersonCode": "string",
"accountCodeSap": 0,
"payingCountryCode": "string",
"destinationCountryCode": "string",
"destinationCurrencyCode": "string",
"stateCode": "string",
"cityCode": "string",
"bankCode": "string",
"agencyNumber": "string",
"bankAccountNo": "string",
"rou_Bco": "string",
"account_Currency_code": "string",
"firstName": "string",
"middleName": "string",
"lastName": "string",
"secondLastName": "string",
"identificationNumber": "string",
"customerZipCode": "string",
"address": "string",
"noticeFormCountry": "string",
"iban": "string",
"createdUser": "string",
"refundRequest": "string",
"companyName": "string",
281
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
"chd": "string",
"fileAttachments": [
{
"fileName": "string",
"contentType": "string",
"fileExten": "string",
"size": 0,
"content": "string"
}
]
} '
A continuación se relaciona la descripción de cada campo del request y esa información
que se registre se guarda en la tabla [rfd].[PIC_BANK_DATA_INFORMATION]
Descripción Tabla Campo
"idIdentificationType": 0, Tipo de identificación Select * FROM
[master].[MST_IDENTIFICATION_TYPE] IDENTIFICATION_CODE
"string", "typePersonCode":
Tipo de persona select * FROM
[master].[MST_TYPE_PERSON] TYPE_PERSON_CODE
"accountCodeSap": 0, Tipo de Cuenta Select * FROM
[master].[MST_ACCOUNT_TYPE] ID_ACCOUNT_TYPE
"payingCountryCode":
"string", Pais pagador Select * FROM [master].[MST_COUNTRY] COUNTRY_CODE
"destinationCountryCode":
"string", Pais destino Select * FROM [master].[MST_COUNTRY] COUNTRY_CODE
"stateCode": "string", Estado o Departamento Select * FROM [master].[MST_STATE] STATE_CODE
"cityCode": "string", Ciudad Select * FROM [master].[MST_CITY] CITY_CODE
"bankCode": 0, Banco Select * FROM [master].[MST_BANK] BANK_KEY
"agencyNumber": "string", Número de Agencia - Para
BR
"bankAccountNo": "string", Número de cuenta bancaria
"destinationCurrencyCode" almacena la moneda
seleccionada por el usuario
282
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
al realizar la solicitud de
reembolso
"rou_Bco": "string", Numero ABA ó swift
"account_Currency_code":
"string", Moneda de la cuenta select * [master].[MST_CURRENCY] CURRENCY_CODE
"firstName": "string", Primer Nombre
"middleName": "string", Segundo Nombre
"lastName": "string", Primer Apellido
"secondLastName":
"string", Segundo Apellido
"identificationNumber":
"string", Número de identificación
"customerZipCode":
"string",
Código postal dependiendo
del pais
"address": "string", Dirección
"noticeFormCountry":
"string", Mensaje
"iban": "string", Código IBAN dependiendo el
país
"createdUser": "string", Usuario quien inserta
registro
"refundRequest": 0, Número de solicitud zendesk select *
[rfd].[PIC_BANK_DATA_INFORMATION]
Se guarda en el campo
REFUND_REQUEST
"companyName": "", Nombre de la razón social en caso de ser persona juridica
"fileAttachments": [
{ [rfd].[PIC_SUPPORT_FILE]
"fileName": "string", Nombre del adjunto Pruebas qa"
"contentType": "string", Tipo de archivo "application/pdf"
"fileExten": "string", tipo de doc ejem: PDF "pdf"
"size": 0, Tamaño del arhivo en bytes 150
"content": "string" Códificación base 64 “ERi0xLjcNCiW1tb”
Para las transacciones con forma de pago “TR” con estado rechazado “R” y el
canal de la solicitud es MyIdTravel o AViajar
Actualizar la forma de pago a transferencia bancaria “CR” de las transacciones con
estado validado “V” en la tabla principal y en la tabla de forma de pago (FOP
Payment Request)
Cuando se inserte o actualice los datos bancarios debe tenerse en cuenta los
campos de auditoría estándar para su posterior uso.
Teniendo en cuenta el número de solicitud Zendesk actual recibido, si ya existe un
registro de datos bancarios debe actualizar el campo update_status con el valor "N"
para indicar que no es el último registro actualizado. El registro nuevo debe
almacenarse con el valor "Y" para indicar que es el último registro actualizado.
283
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Cuando se inserta un adjunto solo formatos permitidos (*.jpg, *.png, *.pdf, *.msg,
*.docx, *.xlsx, jpeg) este queda en el Blob Storage aztacpiccustuseqa >>
bank_data_folder
Y en la Base de datos se observa en la tabla [rfd].[PIC_SUPPORT_FILE] el cual
la llave es el id de la tabla pic_bank_data_information
Se deja un ejemplo del request pero sin el cod base 64 completo por tema de
espacio
{
"identificationCode": "R2",
"typePersonCode": "Y",
"accountCodeSap": 1,
"payingCountryCode": "BR",
"destinationCountryCode": "BR",
284
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
"stateCode": "SP",
"cityCode": "SOR",
"bankCode": "4790001",
"agencyNumber": "6468",
"bankAccountNo": "4564560004564654646",
"destinationCurrencyCode": "BRL",
"rou_Bco": "",
"account_Currency_code": "",
"firstName": "Ariadna",
"middleName": "",
"lastName": "Paredes",
"secondLastName": "",
"identificationNumber": "45564470000",
"customerZipCode": "18105596",
"address": "cll 87",
"iban": "",
"refundRequest": "194530",
"companyName": "",
"fileAttachments": [
{
"fileName": "pruebas jpg.jpg",
"contentType": "image/jpeg",
"fileExten": "jpeg",
"size": 25500,
"content": "/9j/4AAQSkZJRgABAQEAkACQAAD/…..
}
]
}
Al servicio expuesto por Capa Media encargado del envío de información de pago a la interfaz de
SAP se le agregó un nuevo campo:
Campo: account-currency-code
Tipo: string
Longitud: 3
Mandatorio: No
durante el proceso de la function, al momento de realizar la petición se pobla el nuevo campo
“account-currency-code” con el valor del campo [ACCOUNT_CURRENCY_CODE] de la tabla
[PIC_SAP_INTERFACE_OUT] . el campo es de carácter opcional, en caso de no estar poblado, se
debe enviar vacío o no enviar el campo en la petición.
Y en el log se observa la información enviada
select id_log, log_source, log_table, log_msn, created_date, created_user
from [az-sqla-piccust-use-qa].[rfd].[pic_logs_transaction] where log_msn like ('%194530%')
285
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
{"send-sap-info":
[{"company-cod":"AB01","invoice-received-date":"20260529","gl-date":"20260529","name-org1":"","name-org2":"","name-
org3":"Ariadna ","name-org4":"Paredes ","address-line1":"cll 87","city":"SOROCABA","country":"BR","email-
address":"ARIADNA.PAREDES@TEST.AVIANCA.COM","zip":"18105596","bank-key":"4796468","country-code":"BR","bank-
account-num":"456456000456465464","rou-bco":"","acc-typ":"02","iban":"","vendor-num":"","doc-typ":"R2","per-
typ":"Y","invoice-amount":92.40,"description":"REEMBOLSO CASO 194530 TICKET 2022489396477","bnk-inf":"T","account-
currency-code":"BRL","invoice-num":"194530-2022489396477","tkt-numb":"2022489396477","invoice-currency-
code":"USD","profit-segment":"1","profit-category":"ATO","profit-city":"GRU","region":"SP","cross-company":"TA01","vendor-
num2":"","vendor-num3":"","vendor-num4":"45564470000","vendor-num5":""},{"company-cod":"AB01","invoice-received-
date":"20260529","gl-date":"20260529","name-org1":"","name-org2":"","name-org3":"Ariadna ","name-org4":"Paredes
","address-line1":"cll 87","city":"SOROCABA","country":"BR","email-
address":"ARIADNA.PAREDES@TEST.AVIANCA.COM","zip":"18105596","bank-key":"4796468","country-code":"BR","bank-
account-num":"456456000456465464","rou-bco":"","acc-typ":"02","iban":"","vendor-num":"","doc-typ":"R2","per-
typ":"Y","invoice-amount":92.40,"description":"REEMBOLSO CASO 194530 TICKET 2022489396478","bnk-inf":"T","account-
currency-code":"BRL","invoice-num":"194530-2022489396478","tkt-numb":"2022489396478","invoice-currency-
code":"USD","profit-segment":"1","profit-category":"ATO","profit-city":"GRU","region":"SP","cross-company":"TA01","vendor-
num2":"","vendor-num3":"","vendor-num4":"45564470000","vendor-num5":""}]}
Nota: Lo anterior se agrega de acuerdo con los siguientes PBIs:
• 609668 PIC - Crear API para obtener datos bancarios para pago de reembolso - API Bank Data Information
• 629882 PIC - Crear API para obtener datos bancarios para pago de reembolso Parte II (tablas)
• 629883 PIC - Crear API para obtener datos bancarios para pago de reembolso Parte II (adjuntos) - API Bank Data
Information
• 658840 PIC - Cambio para PBI 605150 y 611686 IBAN
• 1123422 PI - Ajuste para admitir formatos JPEG
• 1232694 PI - Moneda Formularios datos bancarios - Modificar la function para la petición de API de SAP con nuevo
campo
• 1224253 PI – Moneda Formularios datos bancarios – Ajuste proceso de envío a SAP_Nuevo campo
14.12. API Check Payment Status
Los canales consumen el api el cual permite consultar el detalle de pago del reembolso. Se puede
consultar en swagger en la external del PI https://azwapppiccustextsuseqa.az-asev3-use-
qa.appserviceenvironment.net/Swagger/index.html
https://azwapppiccustextsuseqa.az-asev3-use-
qa.appserviceenvironment.net/Api/QueryPaymentDetails/List
286
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Request
Request Description Mandatory DataType
tkt-zendesk
Número de caso de seguimiento de Zendesk
(Obligatorio en caso de que el (PNR + apellido) o (tkt
information + apellido) no venga poblado)
N Alfanumerico
channel Canal registrado en el caso N Numérico
level 1. Nivel Básico o 2. Nivel Detallado Y Numérico
last-name Apellido (Obligatorio en caso de que el PNR o tkt
information venga poblado N Alfanumerico
PNR PNR (Obligatorio en caso de que el tkt-zendesk o (tkt
information + Apellido) no venga poblado) N Alfanumerico
tkt-information
[ N
Número de tiquete ((Obligatorio en caso de que el tkt-
zendesk o (PNR + Apellido) no venga poblado) tkt N Numérico
]
Si el nivel del request es 1 por favor retornar únicamente la información en rojo
Si el nivel se encuentra poblado con 2 debe retornar la totalidad de la información
del request
Response
tkt-zendesk Número de caso de seguimiento de Zendesk
status
Indicador de confirmación del pago 0 = pagado, 1= Sin pago, 2 = pago
parcial
error-code Valor que retorna de Éxito o Error
error-msg Detalle del error
info payment: [{
Nodo: No deben repetirse los tiquetes, debe traer la información del
último registro
document
Número del documento (13 digitos) TICKET de la tabla
[rfd].[PIC_PAYMENT_REQUEST]
287
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Forma de pago FOP de la tabla [rfd].[PIC_FOP_PAYMENT_REQUEST] de
acuerdo con la llave REFUND_REQUEST devuelto en el campo "tkt-
zendesk" y el campo TICKET devuelto en el "document"
fop
payment-date
Fecha de pago - PAYMENT_DATE de la tabla
[rfd].[PIC_PAYMENT_DETAIL] de acuerdo con la llave REFUND_REQUEST
devuelto en el campo "tkt-zendesk" y el campo TICKET devuelto en el
"document" solo si la PAYMENT_STATUS de la tabla
[rfd].[PIC_FOP_PAYMENT_REQUEST]
card-number Tarjeta de crédito - 4 últimos dígitos
card-type Tipo de tarjeta Débito - Crédito
exp-date Fecha de expiración de la tarjeta
approval-code
codigo de aprobación de la transacción - APPROVAL_CODE de la tabla
[rfd].[PIC_FOP_PAYMENT_REQUEST] solo si la "fop" = "TR"
franchise
Franquicia tarjeta FRANCHISE de la tabla
[rfd].[PIC_FOP_PAYMENT_REQUEST] de acuerdo con la llave
REFUND_REQUEST devuelto en el campo "tkt-zendesk" y el campo
TICKET devuelto en el "document" solo si la "fop" = "TR"
refund-amount
Valor reembolsado - REFUND_AMOUNT de la tabla
[rfd].[PIC_PAYMENT_REQUEST] el servicio regresa la información sin
tener en cuenta el último intento de pago. se valida el estado de los
tiquetes de la PAYMENT_REQUEST contra el estado en la
PAYMENT_DETAIL, sí el estado es P (sin importar el número de
reintento).
refund-currency
Moneda del reembolso - REFUND_CURRENCY de la tabla
[rfd].[PIC_PAYMENT_REQUEST]
attempt-number
Numero de intento de pago - Último intento registrado en el campo
NUMBER_RETRIES de la tabla [rfd].[PIC_PAYMENT_DETAIL]
payment-status
(Exitoso, Rechazado) - PAYMENT_STATUS de la tabla
[rfd].[PIC_PAYMENT_REQUEST]
payment-attempts-result
Resultado intento de pago - STATUS_CODE de la tabla
[rfd].[PIC_PAYMENT_DETAIL] de acuerdo con la llave "attempt-number"
payment-attempts-date
Si el STATUS_CODE es P o I , se debe tomar el campo PAYMENT_DATE
de la tabla [rfd].[PIC_PAYMENT_DETAIL]
Si el STATUS_CODE es C, F o R, se debe tomar el campo REJECTED_DATE
de la tabla [rfd].[PIC_PAYMENT_DETAIL]
Si el STATUS_CODE es V, U o T se debe tomar el campo CREATED_DATE
de la tabla [rfd].[PIC_PAYMENT_DETAIL]
voucher-number Número del voucher de QC
voucher-encryp
cpg
Programa del voucher - para reembolsos. CPG de la tabla
[rfd].[PIC_PAYMENT_DETAIL] de acuerdo con la llave REFUND_REQUEST
288
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
devuelto en el campo "tkt-zendesk" y el campo TICKET devuelto en el
"document" solo si la "fop" = "KR"
FechaVencimiento EXPIRE_DATE de la tabla [rfd].[PIC_VOUCHER] en formato DD/MM/AAAA
FechaEmision
ACTIVATION_DATE de la tabla [rfd].[PIC_VOUCHER] en formato
DD/MM/AAAA
issue-date
Fecha de emision del voucher / ACM - ISSUE_DATE de la tabla
[rfd].[PIC_PAYMENT_REQUEST]
bank-account
Ultimos 4 digitos de la cuenta bancaria a la que se transfirió -
BANK_ACCOUNT_NO de la tabla [rfd].[PIC_BANK_DATA_INFORMATION]
solo si la solo si la "fop" = "CR"
bank-name
nombre del banco - El nombre en español del Banco de acuerdo con el
campo BANK_CODE de la tabla [rfd].[PIC_BANK_DATA_INFORMATION]
solo si la solo si la "fop" = "CR" (Ej. Banco BBVA)
account-type
tipo de cuenta - El nombre en español del Tipos de Banco de acuerdo la
tabla [rfd].[PIC_BANK_DATA_INFORMATION] solo si la solo si la "fop" =
"CR" (Ej. Cuenta de Ahorros)
date-update
fecha de actualización de datos bancarios - Campo UPDATED_DATE de la
tabla [rfd].[PIC_BANK_DATA_INFORMATION] solo si la solo si la "fop" =
"CR"
acm-number
Numerro de la ACM - Campo ACM_NUBER de la tabla
[rfd].[PIC_PAYMENT_DETAIL solo si la solo si la "fop" = "NC"
miles Valor de reembolso equivalente en millas
ip
de la tabla Fop_paid_request, No es obligatorio Los posibles valores para
este campo son:"Y" , "N" o Vacío
}]
total-payment: [{ Informacion sumarizada del pago
"total-refund-amount"
la sumatoria de refund-amount de todos los documentos entregados -
sumatoria del campo REFUND_AMOUNT de todos los registros de la
tabla [rfd].[PIC_PAYMENT_REQUEST]
"refund-currency"
la moneda de la sumatoria realizada anteriormente -
REFUND_CURRENCY de la tabla [rfd].[PIC_PAYMENT_REQUEST] del
primer registro
"summarize-payment":
[{ Este nodo refleja el último intento resumido.
"document"
todos los tkt de la misma solicitud que cumpla con la misma fop, doc-ref,
status payment y date
"refund-amount-tkt"
sumatoria del campo REFUND_AMOUNT de la tabla
[rfd].[PIC_PAYMENT_REQUEST] de los documentos regresados
anteriormente. el servicio regresa la información sin tener en cuenta el
último intento de pago. se valida el estado de los tiquetes de la
PAYMENT_REQUEST contra el estado en la PAYMENT_DETAIL, sí el
estado es P (sin importar el número de reintento).
289
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
"refund-currency-tkt"
REFUND_CURRENCY de la tabla [rfd].[PIC_PAYMENT_REQUEST] del
primer registro retornado en el campo "document"
"info-fop": [{
"fop"
forma de pago del reembolso (CR, TR, KR..).. Etc fop de los tiquetes
retornados en el campo "document"
"amount-fop"
Valor de pago de esa forma de pago - sumatoria del campo
REFUND_AMOUNT de la tabla [rfd].[PIC_FOP_PAYMENT_REQUEST] de
los tkt regresados anteriormente que cumplan con la misma fop
miles
sumatoria del valor en millas (campo MILES de la tabla
[rfd].[PIC_PAYMENT_REQUEST]) de los tiquetes agrupados en el campo
“document” del response.
"doc-ref"
Si la Fop es CR: debe retornar el número de cuenta bancaria truncada, si
es TR debe retornar la TC truncada, si es KR, debe retornar el número del
voucher en claro, si la forma de pago es LM retornará el número de
viajero frecuente, si es NL retornará el número de la ACM en claro
"status-payment"
estado de la transacción - Estado de los tkt retornados en el campo
"document"
transaction-date debe mapearse del campo created_date sin incluir la fecha y la hora
"date" Fecha de acuerdo con el estado
ip
de la tabla Fop_paid_request, No es obligatorio Los posibles valores para
este campo son:"Y" , "N" o Vacío
}]
}]
"transaction-group": [{
Información de todos los intentos (De forma ordenada - (Primero en
forma de pago y posterior el reintento) Este nodo hace referencia al
historial completo de los registros de la solicitud.
"tiquete"
todos los tkt de la misma solicitud que cumpla con la misma fop, doc-ref,
status payment
"attempt-number"
Número de intento - NUMBER_RETRIES de la tabla
[rfd].[PIC_PAYMENT_DETAIL]
"fop" forma de pago - FOP de la tabla [rfd].[PIC_PAYMENT_DETAIL]
"doc-ref"
Si la Fop es CR: debe retornar el número de cuenta bancaria truncada, si
es TR debe retornar la TC truncada, si es KR, debe retornar el número del
voucher en claro, si la forma de pago es LM retornará el número de
viajero frecuente, si es NL retornará el número de la ACM en claro
"amount-doc"
Valor enviado en reintento - sumatoria del campo REFUND_AMOUNT de
la tabla [rfd].[PIC_FOP_PAYMENT_REQUEST] de los documentos
regresados anteriormente que cumplan con la misma fop
refund-currency
REFUND_CURRENCY de la tabla [rfd].[PIC_PAYMENT_REQUEST] del
primer registro retornado en el campo "tiquetes"
"status-payment"
Estado del pago - Estado de los tiquetes retornados en el campo
"tiquetes"
290
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
transaction-date debe mapearse del campo created_date sin incluir la fecha y la hora
date
}]
}]
}]
{
"tkt-zendesk": "167197",
"level": 1,
"pnr": "",
"lastName": "",
"tktInformation": [
""
]
}
{
Response Nivel 1
"tkt-zendesk": "167197",
"status": "Pago Parcial",
"error-code": "",
"error-msg": "",
"info-payment": [
{
"document": "2022483837432",
"fop": "LM",
"payment-date": "2025-10-23T11:46:40",
"card-number": "",
"card-type": "",
"exp-date": "",
"approval-code": "",
"franchise": "",
"refund-amount": 21.47,
"refund-currency": "USD",
"attempt-number": 2,
"payment-status": "P",
"payment-attempts-result": "Pagado",
"payment-attempts-date": "2025-10-23T11:46:40",
"voucher-number": "",
"voucher-encryp": null,
"FechaVencimiento": "",
"FechaEmision": "",
"cpg": "",
"issue-date": "2025-08-26T00:00:00",
"bank-account": "",
"bank-name": "",
"account-type": "",
"date-update": null,
"acm-number": "",
"miles": 1652,
291
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
"ip": ""
}
]
}
{
Response Nivel 2 >> Detallado
"tkt-zendesk": "167197",
"status": "Pago Parcial",
"error-code": "",
"error-msg": "",
"info-payment": [
{
"document": "2022483837432",
"fop": "LM",
"payment-date": "2025-10-23T11:46:40",
"card-number": "",
"card-type": "",
"exp-date": "",
"approval-code": "",
"franchise": "",
"refund-amount": 21.47,
"refund-currency": "USD",
"attempt-number": 2,
"payment-status": "P",
"payment-attempts-result": "Pagado",
"payment-attempts-date": "2025-10-23T11:46:40",
"voucher-number": "",
"voucher-encryp": null,
"FechaVencimiento": "",
"FechaEmision": "",
"cpg": "",
"issue-date": "2025-08-26T00:00:00",
"bank-account": "",
"bank-name": "",
"account-type": "",
"date-update": null,
"acm-number": "",
"miles": 1652,
"ip": ""
}
],
"total-payment": [
{
"total-refund-amount": 21.47,
"refund-currency": "USD",
"summarize-payment": [
{
"document": "2022483837432",
"refund-amount-tkt": 21.47,
"refund-currency-tkt": "USD",
292
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
"info-fop": [
{
"fop": "LM",
"amount-fop": 21.47,
"miles": 1652,
"doc-ref": "1210",
"status-payment": "C",
"transaction-date": "2025-10-23T11:46:40",
"date": "2025-10-23T11:46:40",
"ip": ""
}
]
],
}
{
"transaction-group": [
"tiquete": "2022483837432",
"attempt-number": 0,
"fop": "LM",
"doc-ref": "1210",
"amount-doc": 21.47,
"refund-currency": "USD",
"status-payment": "A",
"transaction-date": "2025-09-01T06:09:28",
"date": "2025-09-01T06:09:28"
},
{
"tiquete": "2022483837432",
"attempt-number": 1,
"fop": "LM",
"doc-ref": "1210",
"amount-doc": 21.47,
"refund-currency": "USD",
"status-payment": "A",
"transaction-date": "2025-09-01T06:09:32",
"date": "2025-09-01T06:09:32"
},
{
"tiquete": "2022483837432",
"attempt-number": 2,
"fop": "LM",
"doc-ref": "1210",
"amount-doc": 21.47,
"refund-currency": "USD",
"status-payment": "C",
"transaction-date": "2025-10-23T11:46:40",
"date": "2025-10-23T11:46:40"
}
]
}
]
293
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
El campo status retorna la siguiente información: 0 = pagado, 1= Sin pago y 2 = pago
}
parcial.
Retorna el estado en texto y no en número utilizando la siguiente lógica:
Pagado:
Para retornar este estado debe cumplir con los siguientes criterios (Todos)
• Si el refund request es numérico, deberá tomar todos los tiques o EMDs que
coincidan con un estado (C, P, F) y al menos un registro debe tener un estado
pagado “P”.
• Si el refund request es alfanumérico, deberá tomar todos los tiques o EMDs que
coincidan con un estado final (C, P) y al menos un registro debe tener un estado
pagado “P”.
Sin pago:
Para retornar este estado debe cumplir con la siguiente lógica
• No existe un solo registro en estado P
Pago Parcial:
Para retornar este estado debe cumplir con la siguiente lógica
• Si el refund request es numérico, deberá al menos un tique/EMD tener un estado
pagado “P” y al menos un tique/EMD de la solicitud debe tener un estado diferente
a un estado finalizado o cerrado (F, C).
• Si el refund request es alfanumérico, deberá al menos un tique/EMD tener un
estado pagado “P” y al menos un tique/EMD de la solicitud debe tener un estado
diferente a un estado cerrado (C)
Lógica para el campo payment-status
El estado que ser retornado es en letra y texto de acuerdo a la información que se
encuentre en la tabla payment request, ejemplo:
• Si se encuentra un estado (V, I, U, O) debe retornar una A
• Si se encuentra un estado (R, T) debe retornar F
• Si se encuentra un estado (P) debe retornar C
294
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• Si se encuentra un estado (C) ó (F) debe retornar una R
Si el estado que se esta regresando en el campo payment-attempts-result es
"Exitoso" o se encuentra vacío debe retornar el estado que se encuentra en la Payment
Request (Con la lógica mencionada anteriormente)
SI el estado que se esta regresando en el campo payment-attempts-result es
"Rechazado" debe retornar el estado que se encuentra en la Payment detail en el campo
status code (Con la lógica mencionada anteriormente)
para el campo payment-attempts-result resultado del reintento relacionado (Exitoso /
Rechazado)
Lógica para nivel 1 o 2
• Para nivel 1:
En caso de que exista información en la tabla detail:
Debe enviarse únicamente el último intento de pago
En caso de que no existe información en el tabla detail (Pero existe en en el PIC
- Validando en la payment request)
Debe enviarse en el campo payment status = A, y en el campo payment-attempts-
result = Vacío
Para Nivel 2:
En caso de que exista información en la tabla detail:
Debe enviarse todos los intentos de pago
En caso de que no existe información en el tabla detail (Pero existe en en el PIC
- Validando en la payment request)
Debe enviarse en el campo payment status = A, y en el campo payment-attempts-
result = Vacío
Nota: Lo anterior se agrega de acuerdo a los PBIs:
• 689341 PIC - API de consulta de Detalle de Pago.
• 699520 PIC - Check payment status
• 737201 PIC - Ajuste Check payment status
• 747885 PIC - Ajuste Check payment status cuando encuentre F retorna R
• 832768 PIC - Ajuste al servicio Check Payment Status - Modificación consulta de tiques o EMDs en estado Final
• 914515 PIC - Ajuste Check Payment Status (Millas) Parte 2
• 1010235 PIC - Ajuste en API externa del Check Payment status [Final]
• 1044333 PIC - Mejoras al Check Payment Status. Parte II [Final]
• 1063775 PIC - Ajuste Check Payment Status (Nodos Sumarizado - Transaction Group)
• 1097886 PIC – Pago rechazados canal MyIDtravel y aviajar - Agregar campo ip en la estructura de check payment
status
• 1137590 PIC- Check Payment Status – Nuevo campo en response “miles” (“summarize-payment”)
• 1256790 [Refund] – PI - Ajuste Check Payment Status – Info Payment y Sumarize Payment
295
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
14.13. Número de reintento
Se envía el número real de reintentos efectuados para cada transacción, y no un
número secuencial asignado por el sistema. (Campo "attempt-number" del nodo
"info-payment"). Esto NO afecta el nodo de “transaction-group"
De acuerdo con la siguiente configuración por cada FOP vs Estatus se tomará en
cuenta los reintentos.
Consultar la tabla Select * from [rfd].[PIC_PARAM_STATUS_RETRIES]
De acuerdo al caso 150886 para TR aplica el reintento en el estado P y T,
entonces serian 2 reintentos reales de pago.
296
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: Lo anterior se agrega de acuerdo con el PBI
• 1073359 PIC - Ajuste Check Payment Status - "Número de reintento"
14.14. APIM GetCurrencyList
Se desarrolla un servicio en la External que expone todas las monedas creadas y
registradas en el sistema PI (Servicio Get, sin request Y/o Payload)
Requisitos:
El servicio esta desplegado y disponible en APIM (API Management).
Proporciona la lista completa de monedas con su información relevante (código).
El servicio sigue las normas de seguridad y autenticación definidas para APIM.
La respuesta es en formato JSON para facilitar su consumo por otros sistemas.
Fuente: [master].[MST_CURRENCY]
APIM
https://api-avianca-qa.avtest.ink/API_Refund_PIC/api/GetCurrencyList
CURL
curl --location --request GET 'https://api-avianca-qa.avtest.ink/API_Refund_PIC/api/GetCurrencyList' \
--header 'Ocp-Apim-Subscription-Key: 9b5545d5d3c540e3a28c1043fe99cd01' \
--header 'Content-Type: application/json' \
--
header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkhTMjNiN0RvN1RjYVUxUm
9MSHdwSXEyNFZZZyJ9.eyJhdWQiOiI3MmI1MjQwZC0wZjYzLTQ3YmMtOTFjOC05MTZmOGIwYzA0ODEiL
CJpc3MiOiJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vMzk3ZWQwMzEtMzkzNS00MGIwLTljNjk
tMTRmZDExNjRkYjhmL3YyLjAiLCJpYXQiOjE3NjA2NDMzMTIsIm5iZiI6MTc2MDY0MzMxMiwiZXhwIjoxNzYw
297
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
NjQ3MjEyLCJhaW8iOiJrMkpnWURBUjkxNzFxUE43Lzl6bGZtMzlYcHMrR2t6VXZ1V2JZK3V2WWloV1BQR0px
ZzRBIiwiYXpwIjoiNzJiNTI0MGQtMGY2My00N2JjLTkxYzgtOTE2ZjhiMGMwNDgxIiwiYXpwYWNyIjoiMSIsIm9p
ZCI6ImI1MWFiNjZjLTg1YWEtNGY3NC05ODhjLTFlNGZlN2UxMzgzNCIsInJoIjoiMS5BU2tBTWRCLU9UVTVz
RUNjYVJUOUVXVGJqdzBrdFhKakQ3eEhrY2lSYjRzTUJJSE9BUUFwQUEuIiwic3ViIjoiYjUxYWI2NmMtODVh
YS00Zjc0LTk4OGMtMWU0ZmU3ZTEzODM0IiwidGlkIjoiMzk3ZWQwMzEtMzkzNS00MGIwLTljNjktMTRmZDEx
NjRkYjhmIiwidXRpIjoiT0ZJc01SOW9IazY0SWE5VmJucGhBQSIsInZlciI6IjIuMCIsInhtc19mdGQiOiJwUXY5czJ
aTXVnbElKZVh5d250SG8wSjhjT1RaNTRhbDFkOFZXVzBKREg0QmRYTnpiM1YwYUMxa2MyMXoifQ.bbeQb
7X7JE0GrIhUyNKqii7ROFSmmqkRFbHi_zXS0IT0bhIMMcLwHJo7w4YI96sEuYjSzNsgc8SwyUs82b68PUaz76
MPsv_Ky_VBDLhSxOWgYZSp28lH0WsFKHZGIerGHM6gwVye1fMWpZM1w3Ka69dPv2H50ucvynx1D0I446H
fyNtWSmNdE9QDVxvNn578uHeX5C4iRa6FYstRz0z-OoJWEs0j8Rh7mrwnFb-tESNWpi61h8odi-
5TWyGzW50CYDeAHfy1afEpH-3HIeI0UgDIZsrLr6QiyfmxRytinK-
ccak4FHWOpF4QiqU9grWuKNceQNNqfaXsWl2_spe1DA' \
--
header 'Cookie: ak_bmsc=8B45F6DDDC0D07A95FD8E993AEE4AD2C~00000000000000000000000000000
0~YAAQcmQwFxdZst+ZAQAAa2yJ7h1/kjOyUaP29EobzdgPE3AUf+C8Bv8flQc+XtMx15LZAjayfq0dChLOdNa
60DQkaxfNb0U9nAm67KRoF47U/0c74PDudZxf0u31pEbz8rbWYvGBT3w0nE2TXOyATFPCbxFEKQUsXmllIe
Lhn08WgG8Loe9C69C2n8W9xWmRyWxd8xYYFalNZXHTR0fqQkYcJF81u2yQcVxYK3Mlu6CQ/2NQSTXvuiJ
OM1dpoF5LUtQuLAQA3wsR9nx8vixrjUkJRQ0Y9MfFowOhjyL0GGwz46eOsRTGTq1iNRbTNbbitWNk0G0JTfs
WLuo/L/tS38kWuRzUNVyg1bAd+DQ=; bm_sv=5B2A349F20A395F6553BD96339B4342A~YAAQcmQwF5pos
t+ZAQAAu7yJ7h0/MDDaAgVgNd6jPi7osZdax+GaL+42lwlgiwJs8g4g14H2HMN1bUvQKqPmEieYwycWlmXvw
6FJ7IVJP3xLepJoWK5pwCeTfUms2XYpIoJ/Xia0EZBMPQNnN1uyeEn+zzwtJ81XGVd1yiH+1SwnMKf+GMEIc
3o9T1nA9E1qzsUlE2ZB2vm57ZtmGo2Pr3k/CKJWCgTeTmvaBjn37hPQIQ5rGFKHNRdJPwIs5FnQ~1' \
--data '{}'
Para ejecutar el APIM se obtiene primero el token
Se copia y se pega en Token de Bearer Token en la opción de Autentication, después de
envía y se obtiene la información de las monedas registradas en el PI
298
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
En el swager de la external encontramos Lista de Monedas del PI
https://azwapppiccustextsuseqa.az-asev3-use-qa.appserviceenvironment.net/Swagger/index.html
https://azwapppiccustextsuseqa.az-asev3-use-qa.appserviceenvironment.net/api/GetCurrencyList
299
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota Lo anterior es de acuerdo al PBI
• 1097890 PI - Pago rechazados canal MyIDtravel y aviajar - Servicio para exponer las monedas creadas en el PIC
14.15. Consumo API refund
Para los casos de FOP TR al consumir el API de refund para los montos menores
a 1 USD se envía en formato entero representando centavos
El campo amount.value no incluye puntos decimales ni separadores de miles. Los
valores se envian en centavos.
Si el monto es menor a 1 USD, se agrega los ceros necesarios a la izquierda.
Ejemplos:
$0.30 → 030
$0.05 → 005
$0.99 → 099
Si el monto es mayor o igual a 1 USD, se convierte a centavos directamente
multiplicándolo por 100
$1.00 → 100
$12.30 → 1230
$120.30 → 12030
Se envió caso en TR y se pago por el process Automático
300
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se confirma que se envia los dos ceros adicionales
Se inserta otra solictud en COP, aunque se obtiene un rechazo y pasó a 2da fop
Se confirma en el log y se envia correctamente los ceros adicionales a la derecha
en el api de las pasarelas de pago
301
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota: Lo anterior es de acuerdi al PBI 1128520 PIC - Ajuste consumo API refund para valores menores a un USD
14.16. API MissingModules - Valores Faltantes de SR a PI
Se tiene un Módulo de Valores Faltantesen Special Refund el cual permite gestionar
el reembolso de montos pendientes, en aquellos casos donde existan errores o
inconsistencias en el proceso de reembolso original. En este módulo se permite la
radicación, validación y autorización de estos casos, bajo un flujo de aprobación
controlado.
Con este servicio “MissingModules” en el PI: se recibe la información de los
reembolsos gestionados a través del Módulo de valores Faltantes de SR (el servicio
es consumido por SR). Se puede recibir más de un tkt por solicitud. Y se inserta la
información recibida de Special Refund al Integardor de pagos en las tablas
[rfd].[PIC_PAYMENT_REQUEST_VF] y [rfd].[PIC_PAYMENT_DETAIL_VF].
Request ejemplo de una solicitud con 2tkt:
[
{
"refund-request": "1000",
"ticket": "1335451010012",
"pnr": "BZSXZJ",
"iata": "76997561",
"channel": 10,
"missing-value": 15.00,
"currency": "USD",
"total-sale": 54.41,
"sale-date": "2026-08-10",
"owner-firstname": "jenn",
"owner-lastname": "QA",
"email": "pruebas@qa.com",
"fop": "NC",
"cpg": "",
"reason": "Error de Liquidación Manual",
"document-type": "T"
302
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
},
{
"refund-request": "1000",
"ticket": "1335451010013",
"pnr": "BZSXZJ",
"iata": "76997561",
"channel": 10,
"missing-value": 15.00,
"currency": "USD",
"total-sale": 54.41,
"sale-date": "2026-08-10",
"owner-firstname": "jenn",
"owner-lastname": "QA",
"email": "pruebas@qa.com",
"fop": "NC",
"cpg": "",
"reason": "Error de Liquidación Manual",
"document-type": "T"
},
{
"refund-request": "1000",
"ticket": "1335451010014",
"pnr": "BZSXZJ",
"iata": "76997561",
"channel": 10,
"missing-value": 15.00,
"currency": "USD",
"total-sale": 54.41,
"sale-date": "2026-08-10",
"owner-firstname": "jenn",
"owner-lastname": "QA",
"email": "pruebas@qa.com",
"fop": "NC",
"cpg": "",
"reason": "Error de Liquidación Manual",
"document-type": "T"
}
]
Al ejecutarlo se inserta en el PI
Nota: Lo anterior se agrega de acuerdo con el PBI
• 1298387 PI - Modulo Faltantes - Ajuste API Valores Faltantes para Soportar Múltiples Tiquetes
303
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
15. TABLAS
15.1. [rfd].[PIC_FOP_PAYMENT_REQUEST]
• CONTADOR_ESTADOS: diferente al de capture, que indica cuántas veces
se ha ejecutado el proceso TR de la function
Nota Lo anterior es de acuerdo al PBI
1130836 PI - [E2E] - Estados de pago - Creación de contador, parámetros
15.2. MST_PAYMENT_PROCESS_WAY
Por solicitud de PBI 908828 - PIC - Modulo de Configuración de Proceso de Pago -
Base de datos, se modifica la tabla MST_PAYMENT_PROCESS_WAY para que permita
relacionar las columnas con su respectivo campo en la tabla maestra:
• Para el campo de “Código de forma de pago” se crea la llave que referencie al
código de forma de pago de la tabla maestra de formas de pago.
304
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
• Para el campo “código ISO de la moneda” se crea la llave que referencie al código
de la moneda de la tabla maestra de monedas.
• Para el campo “Código del procesador de pago” se crea la llave que referencie al
código del procesador de la tabla maestra de procesadores de pago
305
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
306
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
15.3. [master].[MST_PARAMETERS]
• Parámetros para Estados de pago
"SELECT * FROM [MASTER].[MST_PARAMETERS] WHERE PARAMETER_CODE IN
('FIRST_RETRY_AGE','SUBSEQUENT_RETRIES_AGE','STATUS_PROCESSORS','OMITTED_CHANNELS_
STATUS','STATUS_TO_REVIEW',
'PAYMENT_ROUTE_TO_REVIEW_STATUS','3DS','ATTEMPTS_STATUS')"
307
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Nota Lo anterior es de acuerdo al PBI
1130836 PI - [E2E] - Estados de pago - Creación de contador, parámetros
• Parámetros TC - Razón de rechazo de solicitudes de mozart que no estén
capturadas y estados del api getinfosale "capture-status"
select * from [master].[MST_PARAMETERS] where parameter_code in
('PARAM_SIN_CAPTURED_REASON_REJECTED', 'GET_INFO_SALE_CAPTURE_IN_TRANSACTION')
Nota Lo anterior es de acuerdo al PBI
1124050 PI - [E2E] - Captured - Ajuste al servicio de procesamiento para que evaluar el capture. Parte III
• Cantidad máxima de días para actualizar los datos bancarios y motivo de
rechazo
Cantidad máxima de días para actualizar los datos bancarios
Para temas de pruebas en ambiente qa se deja
DAYS_FOR_NTC19_BANK_DATA_INFO = 1 día y que el múltiplo al ser 2día se
notifique, en prd se dejaría en 7 dias para enviar la notificación a los 7 y 14 días
308
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Y el parámetro DAYS_FOR_UPDATE_BANK_DATA_INFO=3 para que finalice o
Rechace la solicitud
Razón de rechazo a Mozart para los casos Rechazados o Finalizados en cash -
CR
Bank Details”
REASON_REJECT_API_PAYMENT_REQUEST_MOZART_CR = “Incomplete
15.4. MST_CHANNEL_FOP_ADDITIONAL
En la tabla master.MST_CHANNEL_FOP_ADDITIONAL se encuentra la relación
entre el canal y la forma de pago a través de los códigos de cada campo.
Para consultar la tabla desde la base de datos, se debe ingresar a la Base de
datos de PIC y realalizar la consulta SQL: SELECT * FROM
master.MST_CHANNEL_FOP_ADDITIONAL
15.5. MST_FRANCHISE
Por solicitud de PBI 908828 - PIC - Modulo de Configuración de Proceso de Pago -
Base de datos, se crea la tabla MST_FRANCHISE para guardar las franquicias que se
manejen en el PIC. Hasta Diciembre 10 de 2024 no se tiene pantalla en PIC para la
parametrización de este campo.
309
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
15.6. MST_MANUAL_TEMPLATES_PAY_PROCC
Por solicitud de PBI 908828 - PIC - Modulo de Configuración de Proceso de Pago -
Base de datos, se crea la tabla MST_MANUAL_TEMPLATES_PAY_PROCC para
almacenar la lista de plantillas manuales disponibles para el proceso de pago manual que
se manejan en el PIC. Hasta Diciembre 10 de 2024 no se tiene pantalla en PIC para la
parametrización de este campo.
310
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
16. Mantenimiento y Limpieza de data histórica
PBI relacionado:
832748 PIC - Ajuste procedimiento de eliminación en BD - Function Para limpieza
y mantenimiento de data histórica
Este proceso consiste en ejecutar una función para eliminar los registros Refund
Request que en un tiempo configurado cumplen las siguientes condiciones:
• Si el refund request es numérico, deberá tomar todos los tiques o EMDs
relacionados al refund request que coincidan con un estado final cerrado
“C”, pagado “P” o final “F” (C, P, F).
o Si todos los tiques/EMDs pertenecientes a la misma solicitud se
encuentran en un estado final debe ser parte de la consulta de
eliminación
o Si al menos un tique/EMD se encuentra en un estado diferente al
estado final no debe ser tenido en cuenta en la eliminación.
• Si el refund request es un caso alfanumérico, deberá tomar todos los tiques
o EMDs relacionados al refund request que coincidan con un estado final
cerrado “C” o pagado “P” (C, P).
o Si todos los tiques/EMDs pertenecientes a la misma solicitud se
encuentran en un estado final debe ser parte de la consulta de
eliminación
311
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
o Si al menos un tique/EMD se encuentra en un estado diferente al
estado final no debe ser tenido en cuenta en la eliminación.
El tiempo en años que deben tener los registros de antigüedad se configura en el
parámetro llamado PIC_AZFHISTMAINT_YEARS_FOR_REMOVE_REFUNDS
Para el alcance se realizaron las verificaciones en el SP
[rfd].[PIC_AZFHISTMAINT_DATA_DELETE] el cual será posteriormente llamado
en la respectiva función que se encargará de ejecutarse para el eliminado de esta
data histórica.
Cada tipo de pago cuenta con tablas relacionadas en la base de datos, cuando se
ejecuta el SP, los registros serán eliminados de todas las respectivas tablas
Cuando la forma de pago es Tarjeta de crédito
PIC_CONTROL_REFUND_REQUEST
PIC_PAYMENT_REQUEST
PIC_PAYMENT_DETAIL
PIC_FOP_PAYMENT_REQUEST
PIC_SALE_REPOSITORY
Cuando la forma de pago es Voucher
PIC_CONTROL_REFUND_REQUEST
PIC_PAYMENT_REQUEST
PIC_FOP_PAYMENT_REQUEST
PIC_VOUCHER
PIC_PAYMENT_DETAIL
Cuando la forma de pago es Cash
312
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
PIC_CONTROL_REFUND_REQUEST
PIC_PAYMENT_REQUEST
PIC_FOP_PAYMENT_REQUEST
PIC_PAYMENT_DETAIL
PIC_BANK_DATA_INFORMATION
PIC_HIS_BANK_DATA_INFORMATION
PIC_SUPPORT_FILE
PIC_SAP_INTERFACE_OUT
PIC_SAP_INTERFACE_RETURN
Cuando la forma de pago es ACM
PIC_CONTROL_REFUND_REQUEST
PIC_PAYMENT_REQUEST
PIC_FOP_PAYMENT_REQUEST
PIC_PAYMENT_DETAIL
PIC_SAP_ACM_INTERFACE_OUT
PIC_SAP_ACM_INTERFACE_RETURN
A continuación, se muestra un ejemplo de cómo fue ejecutado el SP para eliminar
un registro compuesto por un tipo de pago Tarjeta de Crédito (TR)
Se tiene el siguiente Refund Request en estado P que aplica para la prueba y
adicionalmente cuenta con registros en todas las tablas relacionadas.
Se confirma que el SALE DATE es mayor a un año anterior a la fecha de hoy,
actualmente el parámetro está configurado a 1 año
313
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Se consulta el SP RFD.PIC_AZFHISTMAINT_GET_REFUNDS el cual tiene como
función validar cuales registros cumplen la condición de ser eliminados, y en el
respectivo listado arrojado se observa el Refund request objeto de prueba.
Se ejecuta el SP [rfd].[PIC_AZFHISTMAINT_DATA_DELETE], como motivo de
pruebas, se ejecuta de tal manera que se envía el refund rquest individualmente,
en un escenario real, el SP se ejecutaría en forma general, se confirma que la
respuesta es exitosa
314
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al consultar nuevamente las tablas relacionadas con el tipo de pago Tarjeta de
Crédito se verifica que los registros se eliminaron completamente.
10.10 APIS
315
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
API Eliminar Comprobante de Pago
PBI relacionado
809521 PIC - API Eliminar Comprobante de Pago
Esta API llamada DeletePaymentVoucher tiene como función eliminar los
comprobantes de pago que se encuentran guardados en el Azure Storage, para su
funcionamiento se debe enviar el o los refund request que se requieren eliminar.
Se accede desde SwaagerBack
https://azwapppiccustbknduseqa.az-asev3-use-
qa.appserviceenvironment.net/Swagger/index.html
Proceso
Se tienen identificados previamente registros que se encuentran en la carpeta de
comprobantes de pago en el portal Azure
https://portal.azure.com/#@avtestonline.onmicrosoft.com/resource/subscriptions/1
b3f8b8d-3a05-4d91-a270-46907a9d0259/resourceGroups/az-rg-refundspic-use-
qa/providers/Microsoft.Storage/storageAccounts/azstacpiccustuseqa/containersList
azstacpiccustuseqa
>> Blob Storage >> comprobantes-de-pago
316
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
El número de refund Request es 204101 el cual tiene diversos comprobantes de
pagos asociados
Teniendo identificado el respectivo Refundrequest se diligencia en el API
317
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
Al ejecutar se observa en el resultado que es exitosa la eliminación, para cada
registro trae la información del nombre, tamaño y la ubicación.
Al acceder nuevamente a la carpeta de comprobante de pagos se confirma que el
registro es eliminado
318
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
319
Manual de
Aplicación
Versión 1.0
_________________________________________________________
______
17. ERRORES CONOCIDOS
• Error en carga de casos PI : Ha ocurrido un error en el flujo | Mensaje: The
method or operation is not implemented.
El client secret de un API, se actualizó y no se actualizó en los settings de PIC.
https://aviancavsts.visualstudio.com/UnidadesSoporteF/_workitems/edit/956304
18. GLOSARIO DE TÉRMINOS
Término Descripción / Definición
Reembolso Devolución de una cantidad de dinero a la persona que
la había desembolsado por la compra de un TKT.
320