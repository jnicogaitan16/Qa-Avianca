# 04 — UAT con usuario no técnico

**Cuándo:** **QA - Acompañamiento UAT-PRE** (y POST con el mismo criterio de evidencias).  
**Quién:** QA entrega; el **usuario** ejecuta.  
**Salida:** VoBo + Word/Excel en 4 días hábiles.

**Fuentes:** lineamientos (mail, adjunto, evidencias usuario); menús de negocio de los manuales SR/AVR/PI/ROR.  
**Omitido:** pasos SQL, swagger, “probar las cuatro apps”, tus casos QA (salvo que el usuario los pida).

---

## Mail UAT-PRE (texto del equipo)

```
Para: usuario UAT-PRE + equipo de pruebas [+ líder técnico si aplica]
Asunto: [Nombre del tablero] - Certificación y prueba UAT PRE PBI XXXXX - [Descripción del PBI]

Con el objetivo de dar cierre al PBI XXXXX - [Descripción del PBI], envío como adjunto
archivo para iniciar la ejecución de pruebas UAT-PRE.
De ser satisfactorias, es necesario recibir el VoBo y evidencias UAT-PRE,
en los 4 días hábiles siguientes al envío de este mail.
Quedo pendiente de si se requiere alguna validación adicional y/o acompañamiento.
Gracias,
[Firma]
```

El adjunto describe el PBI para que **ellos** armen sus pruebas. No envíes las de QA salvo que las pidan.

---

## Checklist del PBI (marca solo lo que este PBI toca)

```markdown
# UAT  PBI-________     App: [ ] SR  [ ] AVR  [ ] PI  [ ] ROR     Ambiente: PRE
Fecha: ________     Usuario: ________

En cada línea: OK / Falló / No aplica. Capturas con fecha y hora. Evidencia: Word o Excel.

## SR (solo ítems del PBI)
[ ] Iniciar sesión en Special Refund
[ ] Completar el formulario de solicitud del cambio
[ ] Cargar archivo de solicitudes masivas o ver el reporte de esa carga
[ ] Registrar un valor faltante (solicitud + tiquete → Validar → Guardar)
[ ] Aprobar o rechazar un faltante (Coordinador o Gerente)
[ ] El sistema no acepta un faltante mayor al total de la venta

## AVR (solo ítems del PBI)
[ ] Iniciar sesión en AV Refund
[ ] Consultar un reembolso (estación + control, o tiquete)
[ ] Revisar el correo acordado en el PBI (datos bancarios o aviso de pago)

## PI (solo ítems del PBI)
[ ] Iniciar sesión en Integrador de pagos
[ ] Consultar el pago / reembolso del caso
[ ] En gestión de pago: autorizar, generar voucher o enviar notificación
[ ] Usar la plantilla de pago del PBI (tarjeta, voucher u otra)

## ROR (solo ítems del PBI)
[ ] Iniciar sesión en Refund Orchestration Rules
[ ] Maestras → Documento misceláneo: consultar un EMD (Código, nombre, Rfisc, Libro, Tipo, Reembolso)
[ ] Crear un EMD y ver el mensaje de creado exitosamente
[ ] Modificar un EMD (lápiz) y ver la confirmación de actualización

## Cierre
VoBo: [ ] Sí  [ ] No
Evidencia: [ ] Word  [ ] Excel
```

**Nota AVR:** “Consulta tu Reembolso” en el manual es servicio hacia canales (avianca.com / Trade). En UAT interno márcalo solo si el PBI es esa consulta o la pantalla de AVR.

---

## Después del VoBo (tareas oficiales)

1. **QA - Cargue de Evidencias UAT-PRE** — Test Plan + PDF en el PBI.  
2. **QA - Documentación QA** — manual si el PBI lo pide.  
3. **UAT-POST** — acompañamiento + mismo cargue de evidencias.  
4. PBI: UAT → Ready4Deployment → DONE.
