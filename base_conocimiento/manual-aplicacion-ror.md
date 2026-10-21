 
 
 
 
 
 
 
 
 
 
                       
MANUAL DE APLICACIÓN 
 
ROR 
(Refund Orchestration Rules) 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Historial de Cambios y Revisiones del Documento 
 
Versión Documento 
Fecha 
Modificado por 
Secciones, páginas y texto afectado 
1.0 
13-10-2023 
Jenny Garzón 
Se crea el Manual Funcional Refund Orchestration Rules - ROR. 
1.1 
09-09-2024 
Isabel Guerra 
Se agrega funcionalidad de  API -  ROR - API Mapeos ARO 
Se agrega funcionalidad ROR - Ajuste a la tabla TM. EMD / Tabla general de parámetros (API/ListHomologation.) 
Se agrega Funcionalidad ROR - Ajuste API TM. EMD Tabla general de parámetros (API/EmdGetRfisc) 
1.2 
06-06-2025 
Jenny Garzón 
Se agrega Inactivación de Usuario, en la sección de Ingreso al Sistema 
1.3 
17-12-2025 
Jenny Garzón 
Se agrega Query Reporte usuarios Auditoria 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Aceptación del Manual de Aplicación 
 
Elaborado por:  
Revisado por: 
Aprobado por: 
 
 
 
 
 
 
​​Contents 
​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​​ 

 

 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
1. INTRODUCCIÓN 
1.1 Propósito del documento 
 
Documentar las principales funcionalidades, flujos y actividades que intervienen en Special Refund. 
1.2 Documentos de referencia: 
 
Todos los documentos relacionados con la solicitud y entregados a los usuarios se mencionan a continuación: 
Fecha Actualización 
Nombre del documento 
Ubicación 
14-07-2023 
PT-ARQ-Arquitectura de Solucion-REFUND 
Teams >Soporte Financiero>Refund>Arquitectura 
 
 
 
 
 
 
 
INSTALACIÓN 
2. PRESENTACIÓN DEL APLICATIVO 
2.1 Identificación 
ROR (Refund Orchestration Rules) es un nuevo sistema que almacenará y permitirá la actualización de reglas requeridas para el orquestamiento que realizará la capa media de Avianca durante los procesos de Reembolsos 
 
2.2 Alcance 
 
Este sistema desarrollado en AVIANCA con el fin de permitir el manejo de reglas de orquestación del proceso que sean requeridas por la capa de integraciones y que sean consideradas como reglas que puedan ser cambiadas de acuerdo al comportamiento del negocio; esto para evitar tener que hacer solicitudes y cambios de desarrollos en los componentes de orquestación. 
 
Para ser consultada la información de reglas, el sistema deberá exponer sus servicios en el APIM de Avianca para ser consumidos por los servicios de orquestamiento desde allí.  
2.5 Arquitectura  
 
2.6 Especificación detallada de los componentes: 
 
REFUND ORC RULES Front:  
Front End de la solución para el manejo de la reglas, parametrizaciones y homologaciones necesarias para el proceso de orquestamiento de reembolsos.  Será la capa de usuario final.  
 
Este componente NO estará expuesto a internet.  Entre otros deberá tener los módulos de:  
Autenticación con AAD.  
Administración de parámetros, reglas y homologaciones necesarias para el orquestamiento. 
 
 
 
 
 
 
 
REFUND ORC RULES Backend Services:  
Capa de backend de la solución de reembolsos especiales. Esta API contiene servicios con la lógica de negocio asociada a los procesos desencadenados desde el front end de la solución, así como servicios que sean necesarios para abstraer la capa de presentación. 
 
REFUND ORC RULES External Services: 
Capa de servicios externos de la solución. Esta API contiene servicios con la lógica de negocio asociada a atender las peticiones recibidas desde sistemas externos a través de la capa de middleware de Avianca. desarrollada aquí inicialmente:  
 
Los servicios necesarios para entregar la información necesaria de parámetros, reglas y homologaciones necesarias para el proceso de orquestamiento de reembolsos.  
 
DB REFUND ORC RULES:  
Base de datos principal del Sistema. El diseño de la base de datos está orientado a un sistema transaccional de baja actualización, pero alta consulta.  
 
Tiempo de Retención 1 año 
 
Key Vault REFUND ORC RULES:  
Este componente permitirá el almacenamiento de las llaves y secretos que sean necesarios para la solución de reembolsos especiales  
 
Log REFUND ORC RULES: 
La solución tiene un log que permite hacer seguimiento de diferentes procesos de la solución o sucesos de error, para ello se hará uso de un Aplication Insights de Azure, y cada componente de la solución podrá dejar información en este repositorio.  
 
Tiempo de retención 30 días. 
 
3. RECOMENDACIONES ANTES DE LA INSTALACIÓN 
 
Se recomienda que antes de la instalación se cuente con un backup a nivel de componentes en caso de requerirse posteriormente. 
4. PUESTA EN AMBIENTE PRUEBAS O PRODUCCIÓN  
 
Para el buen funcionamiento en el ambiente de producción se debe realizar despliegue según solicitud en Mauro de los artefactos que desarrollo libere en el ambiente de producción y ejecución de los scripts que correspondan.  
 
4.1 Despliegue en ambiente de pruebas  
 
Antes de iniciar el proceso de  despliegue se debe realizar backup de los artefactos que vamos a reemplazar y se dejan en ……. 
5. PROCESO DE ROLL BACK 
El proceso de Roll Back corresponde al entregado por el equipo de desarrollo quien entrega los script correspondientes a de acuerdo a la solicitud, adicional se reemplazan los archivos que se hayan modificado.  
AMBIENTE 
 
6. PROCEDIMIENTO DE CONFIGURACIÓN 
6.1 Configuración Hardware 
No aplica 
6.2 Configuración Software 
 
7. GENERACIÓN DE NUEVOS DATOS 
 
 
8. DESCRIPCIÓN DE LA FUNCIONALIDAD 
 
Es un nuevo sistema que almacenará y permitirá la actualización de reglas requeridas para el orquestamiento que realizará la capa media de Avianca durante los procesos de Reembolsos.  
9. INGRESO AL SISTEMA 
 
Para el ingreso a Special Refund ingresamos al siguiente link de QA: 
  
https://azwappsorqrulesfrontuseqa.az-asev3-use-qa.appserviceenvironment.net/auth 
 
 
 
Al dar clic en iniciar sesión se debe autenticar con Directorio Activo de Azure, debe elegir o escribir su correo que están en Microsoft. 
 
 
9.1 Inactivación de usuario 
 
Los usuarios que no hayan iniciado sesión en los últimos 90 días serán inactivados automáticamente, para mantener la seguridad y limpieza de la base de datos.  
 
Con el SP de inactivación [rfd].[ROR_DEACTIVITY_USER] 
 
USE [az-sqla-orqrules-use-qa] 
GO 
DECLARE	@return_value int 
EXEC	@return_value = [rfd].[ROR_DEACTIVITY_USER] 
SELECT	'Return Value' = @return_value 
GO 
 
 
 
Se confirma los usuarios deshabilidatos 
 
SELECT * FROM [adm].[MST_USER] order by  last_login_date asc 
 
 
De acuerdo con los parámetros configurados para la inactivación de usuario. 
 
select * from [master].[MST_PARAMETERS] where parameter_code in  
('PRE_INACTIVATION_NOTIFICATION', 
'SUBJECT_EMAIL_INACTIVATION_NOTIFICATION', 
'TEMPLANE_NAME_INACTIVATION_NOTIFICATION', 
'USER_INACTIVITY_DAYS') 
 
  
 
Se enviará una notificación a los usuarios próximos a inactivar cuando hayan cumplido 80 días sin ingreso. Ejecutando también el SP [rfd].[ROR_USERS_FOR_NOTIFICACION_OF_INACTIVITY] 
 
USE [az-sqla-orqrules-use-qa] 
GO 
DECLARE	@return_value int 
EXEC	@return_value = [rfd].[ROR_USERS_FOR_NOTIFICACION_OF_INACTIVITY] 
SELECT	'Return Value' = @return_value 
GO 
 
 
 
SELECT     [email], [FIRST_NAME] + ' ' + [LAST_NAME], [last_login_date] AS [NAME] 
FROM      [adm].[MST_USER] 
WHERE     DATEDIFF(DAY, [last_login_date], GETDATE()) = 80;		 
 
Interfaz de usuario gráfica, Aplicación, Word

El contenido generado por IA puede ser incorrecto. 
 	 
La notificación seria la siguiente:  
 
 
Se observa en el log, los usuarios inactivados 
 
SELECT * FROM [rfd].[LOGS_TRANSACTION] where created_user='ROR_DEACTIVITY_USER' order by created_DATE asc 
 
 
 
Nota: Lo anterior es de acuerdo con el PBI 982297 Refund - Inactivación Automática de Usuarios Cada 90 Días. Parte II [Final] 
 
9.2 Descripción del perfil de usuario 
 
 
A continuación, se presenta un resumen con los principales accesos.  
 
MÓDULOS   
 
Para la administración y gestión de Refund Orchestration Rules – ROR, se manejan diversos menús para cada proceso, los cuales se detallaran a continuación. 
 
PROCESOS 
 
 
ADMINISTRACIÓN 
 
 
Gestión de Menús 
 
Gestión de Roles 
 
 
Gestión de Usuarios 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
MAESTRAS 
 
10.3.1 Tabla TM. EMD / Tabla general de parámetros 
 
A través de la Maestra Configuración EMD se puede crear, modificar y consultar registros EMD 
 
Para ingresar a la Mestra de EMD, se debe ingresar al menú Maestras y elegir el sub-menú Documento misceláneo 
 
 
 
10.3.1.1  Consultar EMD 
 
Se puede utilizar la opción de paginación  para consulta de registros deseados por agrupación o pasar de pagina por grupo de registros 
 
 
 
 
 
Para consultar por un campo especifico, se selecciona el campo deseado y se inserta en el campo de búsqueda el nombre del valor deseado.  
 
Consultar por “Código”  
 
Consultar por “Nombre en español” 
 
Consultar por “Nombre en inglés” 
 
 
 
Consultar por “Nombre en portugués” 
 
 
Consultar por “Rfisc” 
 
 
Consultar por “Libro” 
 
 
 
 
Consultar por “Tipo” 
 
 
 
Consultar por “Descripción” 
 
 
Consultar por “Reembolso” 
 
10.3.1.2  Crear EMD 
 
Para crear un nuevo registro de EMD, dar clic en agregar EMD 
 
 
Dar clic en Crear e ingresar los datos deseados para Agregar el nuevo registro de EMD  
 
 
 
Se presenta mensaje confirmación de EMD creado exitosamente. 
 
10.3.1.3  Modificar EMD 
 
Para modificar un registro dar clic en icono de modifciación (Lápiz) 
 
Modificar los datos deseados y dar clic en el botón “Modificar” 
  
 
 
 
Se presenta mensaje de confirmación exitosa de Actualización del registro EMD 
 
 
 
Nota: lo anterior se agrega de acuerdo con los PBI 695447 ROR - Ajuste a la tabla TM. EMD / Tabla general de parámetros Y PBI  778915 - ROR - Ajuste API TM. EMD Tabla general de parámetros 
PROCESOS 
 
REPORTES 
 
Query Reporte usuarios Auditoria 
 
Se crea SP para generar un reporte con los datos de la maestra de usuarios. 
 
Ejecutar el SP  EXEC [rfd].[AVR_SP_USER_DATA_QUERY] 
 
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
 
1151866 Refund - Queries de Usuarios 
 
APIS 
APIS Mapeo ARO 
 
A través de esta API, se consulta los registros existentes en base de datos de la tabla master.MS_HOMOLOGATION_REFERENCE_VALUES 
 
Ingresar a la URL https://azwappsorqrulesextsuseqa.az-asev3-use-qa.appserviceenvironment.net/Swagger/index.html 
 
Buscar la API ListHomologation. Dar clic en el boton “Try it Out” para poder editar el campo  
 
 
Para consultar todos los registros existentes en Base de datos.  
 
Se deja el campo “ReferenceValueOrig” vació y Dar clic en Ejecutar 
 
 
Se presenta los registros existentes en la tabla master.MS_HOMOLOGATION_REFERENCE_VALUES en Base de datos   
 
 
 
 
 
 
 
 
 
 
Ingresar a la tabla master.MS_HOMOLOGATION_REFERENCE_VALUES desde la Base de datos para comprobar la consulta realizada por la API ListHomologation  
 
 
Para consultar un solo registro  
 
En caso de querer consultar un solo registro se edita el campo “ReferenceValueOrig” con el valor REFERENCE_VALUE_ORIG existente en la base de datos  
 
  
 
 
 
 
 
 
Se presenta el registro consultado.  
 
 
 
Ingresar a la tabla master.MS_HOMOLOGATION_REFERENCE_VALUES desde la Base de datos para comprobar la consulta realizada por la API ListHomologation 
 
Nota: lo anterior se agrega de acuerdo con los PBI 659052 ROR - API Mapeos ARO 
 
 
 
 
 
10.6.1 API EmdGetRfisc 
 
A través de esta API, se consulta los registros existentes de EMDs en base de datos de la tabla master.MST_EMD 
 
Ingresar a la URL https://azwappsorqrulesextsuseqa.az-asev3-use-qa.appserviceenvironment.net/Swagger/index.html 
 
Buscar la API EmdGetRfisc, Dar clic en la opción “Try it out”, Se habilita el campo “Emdcode” para ser editado.  
Para consultar un registro especifico, se ingresa un código existente en base de datos, dar clic en ejecutar 
 
 
Se presenta en el “response” los datos de el registro existete en la tabla Master.MST.EMD 
 
 
Nota: lo anterior se agrega de acuerdo con los PBI 696040 -ROR - Ajuste al servicio expuesto de EMDs  
 
 
11. HISTORIAL DE PRUEBAS DE PERFOMANCE Y SEGURIDAD 
N/A 
 
13. GLOSARIO DE TÉRMINOS 
 
Término 
Descripción / Definición 
Reembolso 
Devolución de una cantidad de dinero a la persona que la había desembolsado por la compra de un TKT. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 