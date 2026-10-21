# Manual QA — Refund (Avianca)

Guía de ingreso. Lo que necesitás saber para operar desde el primer sprint.

> Detalle exhaustivo: manuales en `base_conocimiento/`. Plantillas: `prompts/plantillas/`.

---

## 1. Qué es Refund

Cuatro aplicaciones internas que gestionan el ciclo completo de reembolsos de tiquetes aéreos en Avianca. Tres forman una cadena; la cuarta parametriza reglas.

```
SR (Special Refund)       →  crea el caso especial (VIP, masivos, faltantes)
    ↓ Mozart / APIM
AVR (AV Refund)           →  seguimiento, timeout 30 min, correos al pasajero (NTC)
    ↓
PI  (Payment Integrator)  →  ejecuta el pago (voucher, transferencia, ACM, SAP)

ROR (Orchestration Rules) →  maestras y reglas para la capa media (no radica ni paga)
```

**Sistemas externos** que aparecen en los flujos: Mozart (Central de Reembolsos, SaaS Accelya), SAP4HANA (contabilidad), APIM de Avianca (capa media). No son fronts del equipo pero los vas a ver en logs y APIs.

---

## 2. Accesos QA

| App | Front | SQL Server |
|-----|-------|------------|
| SR  | `https://specialrefundqa.avtest.ink/` | No verificado |
| AVR | `https://azwappavrefsftuseqa.az-asev3-use-qa.appserviceenvironment.net/auth` | `az-sqla-avref-use-qa` |
| PI  | `https://azwapppiccustfrontuseqa.az-asev3-use-qa.appserviceenvironment.net/auth` | `az-sqla-piccust-use-qa` |
| ROR | `https://azwappsorqrulesfrontuseqa.az-asev3-use-qa.appserviceenvironment.net/auth` | `az-sqla-orqrules-use-qa` |

Autenticación: Azure AD (correo Microsoft). Ambientes: **DEV / QA / PRE / POST** (no usar STG ni PROD).

---

## 3. El flujo principal: Valores Faltantes (VF)

Es el único recorrido end-to-end completamente documentado entre las tres apps. Aprendélo primero.

### Qué es

Cuando un reembolso ya procesado tiene un monto pendiente (error o inconsistencia), el área de reembolsos radica un "valor faltante" para devolverlo al pasajero mediante Avianca Credits.

### Paso a paso

```
┌─────────────────────────────────────────────────────────────────────┐
│ 1. RADICAR (SR)                                                     │
│    Procesos → Formulario Captura Reembolsos Faltantes               │
│    Ingresar solicitud + tiquete → Validar → llenar formulario       │
│    → Guardar                                                        │
│    Estado en BD: "Pendiente de Autorización"                        │
│    Tablas: SR_MISSING_VALUE_REFUNDS_VF                              │
│            SR_MISSING_VALUE_REFUND_STATUS_LOG_VF                    │
├─────────────────────────────────────────────────────────────────────┤
│ 2. APROBAR (SR)                                                     │
│    Coordinador aprueba si ≤ 3500 USD                                │
│    Gerente aprueba si > 3500 USD                                    │
│    (TRM: SR_EXCHANGE_RATES + umbral: MST_APPROVAL_RANGE)            │
│    Si hay varios TKTs: se envía a PI solo cuando TODOS están        │
│    aprobados. Estado: "Autorizado" → "En progreso"                  │
├─────────────────────────────────────────────────────────────────────┤
│ 3. PAGAR (PI)                                                       │
│    PI recibe en tablas PIC_PAYMENT_REQUEST_VF / PIC_PAYMENT_DETAIL_VF│
│    Ejecuta el pago (FOP KR=voucher o NC=ACM)                       │
│    Notifica a SR: API MissingValueRefundStatus/Update               │
│    Estado en SR: "Pagado"                                           │
├─────────────────────────────────────────────────────────────────────┤
│ 4. NOTIFICAR (AVR)                                                  │
│    Envía correo al pasajero:                                        │
│    NTC23 si FOP=KR (voucher) │ NTC24 si FOP=NC (ACM)               │
│    Registro: AVR_CONTROL_NOTIFICATIONS                              │
└─────────────────────────────────────────────────────────────────────┘
```

### Datos obligatorios al radicar

| Campo | Regla |
|-------|-------|
| Número de solicitud | Alfanumérico, máx 32 chars |
| Tiquete | Numérico, 13 dígitos, placa 134/202/133/547 |
| PNR | 6 caracteres |
| IATA | 8 dígitos |
| Moneda | De PI vía API GetCurrencyList |
| Valor faltante | Decimal, máx 2 decimales, **no mayor al total de la venta** |
| Forma de pago | KR o NC (parámetro MVR_FOP_LIST) |
| Razón del faltante | De maestra MST_MISSING_REASONS |

### Estados VF

| Estado | Significado |
|--------|-------------|
| Pendiente de Autorización | Radicado, esperando aprobación |
| Autorizado | Aprobado, esperando que todos los TKTs hermanos se aprueben |
| En progreso | Enviado a PI |
| Pagado | PI procesó y notificó a SR |
| REJECTED | Rechazado por Coordinador/Gerente |

Si falla el envío a PI → vuelve a "Pendiente de Autorización".

---

## 4. Otros flujos de SR que vas a testear

### Solicitud individual (5 pantallas)

1. **Inicio** — buscar por reserva, tiquete o EMD → consume GetInfoTicket
2. **Pasajeros** — seleccionar tiquetes, fecha, titular → consume GetRefundInfo
3. **Solicitud de reembolso** — detalle de pago, excepciones, FOP. Si excepción → auditoria. Si FOP ≠ transferencia → salta a pantalla 5
4. **Datos bancarios** — país, cuenta, certificado bancario → consume GetMasterInfo (PI)
5. **Confirmación** — resumen + número de caso. Verificar en BD + Mozart

### Cargue masivo

Archivo CSV/XLSX con 20 columnas (Apply_ard, Booking, TktNumber...). Se carga en UI → la Function `az-fapp-sprefprocess-use-qa` procesa cada ~10 min. Estados: N (no procesado) → I (en proceso) → C (exitoso) / E (reintento) / F (fallido). Máximo 5 reintentos (parámetro MAX_RETRIES_MASS_SENDING).

---

## 5. Ciclo de trabajo QA en el sprint

### Tareas por PBI (crear al inicio del sprint, todas estimadas)

| Tarea | Qué hacés |
|-------|-----------|
| Recibir PBI | Dev hace review/entrega a QA y al usuario |
| Análisis y diseño | Diseñar test cases, cargarlos al Test Plan |
| Preparación de data | Armar data de prueba en el ambiente |
| Ejecución | Probar en QA. Si falla → bug **inmediatamente** |
| Re-test | Cuando Dev corrige el bug, volver a probar |
| UAT-PRE | Entregar al usuario, acompañar sus pruebas |
| Evidencias UAT-PRE | Test Plan + PDF adjunto en el PBI |
| Documentación | Actualizar manual si el PBI lo requiere |
| UAT-POST | Acompañar pruebas en POST |
| Evidencias UAT-POST | Test Plan + PDF adjunto en el PBI |

### Flujo del PBI en el tablero

```
Committed → CodeReview → QA → Build → UAT → Ready4Deployment → DONE
```

**Regla:** no se saltan casillas. Nunca. El bug sigue el mismo flujo que un PBI.

Para devolver: QA → Committed → CodeReview → QA.

---

## 6. Test Plan, Suite y Case

**Test Plan:** nombre con la app. Ejemplo: `Test Plan [SR]`.

**Test Suite:** jerárquica por sprint:

```
SR / Sprint 45
  ├── QA
  ├── UAT PRE
  └── UAT POST
      └── PBI-123456
```

Si el PBI no sale este sprint → mover la carpeta al siguiente.

**Test Case:**

| Campo | Convención |
|-------|------------|
| Nombre | `PBI-XXXXX #TC Título del escenario` |
| State | Design → Ready → Closed (al cerrar UAT) |
| Tag | Aplicación (SR, AVR, PI, ROR) |
| Related work | El PBI (obligatorio) |
| Steps | Paso a paso con datos concretos |
| Evidencias | Screenshots con **fecha y hora visible** |

---

## 7. Bugs

### Crear inmediatamente

El bug se reporta **el mismo día** que se encuentra. No se acumula.

| Campo Azure | Qué poner |
|-------------|-----------|
| Título | `PBI-XXXXX Breve descripción del defecto` |
| Activity | `Development` (dev lo inyectó) / `Deployment` (mal despliegue) / `Requirements` (PBI mal definido) / `Testing` (error de QA o hallazgo UAT) |
| Environment | DEV / QA / PRE / POST |
| Area | Tablero del bug |
| Iteration | Sprint donde se encontró |
| Application Name | SR / AVR / PI / ROR |
| Severity | 1-Critical, 2-High, 3-Medium, 4-Low |
| Related work | Vincular al PBI siempre |

### En el cuerpo del bug

- Pasos para replicar (numerados, con datos concretos)
- URL o ambiente donde se ejecutó
- Resultado esperado vs resultado actual
- Evidencias con fecha y hora
- Enviar correo al equipo de Dev para seguimiento

### Ciclo de vida

1. Crear → asignar Dev → estimar tiempos DEV y QA
2. Dev corrige → devuelve a QA
3. QA: pedir explicación (¿cambió BD? ¿UI?) → re-testear → adjuntar evidencias → comentar
4. Si pasa → mover por **todos** los estados hasta Done
5. Si no pasa → devolver a Committed con evidencia

### Casos especiales

- **No era bug:** cambiar Activity a quien corresponda + comentar por qué
- **Múltiples hallazgos:** un bug por hallazgo, o uno agrupado si todos son la misma Activity
- **Bug en UAT:** revisar todas las pruebas del PBI antes de pasarlo al usuario
- **Cambio de alcance:** NO es bug. Cerrar el PBI actual, abrir uno nuevo
- **Incidente (INC):** work item separado, no es bug

---

## 8. Impedimentos

Cuando no podés testear por algo que **no es desarrollo** (ambiente, permisos, data, usuario no disponible):

1. Mover el PBI a **Build**
2. Crear impedimento: `PBI-XXXXX Breve descripción`
3. Comentar en el PBI que se creó el impedimento
4. Máximo **5 días** en Build. Si va a más → escalar con líderes
5. Al resolverse → cerrar impedimento → devolver PBI al estado anterior

Criterios válidos: usuario no responde en 4 días, cierre contable, falla de ambiente, sobrecarga de QA (justificar horas).

---

## 9. UAT

QA entrega, el **usuario** prueba (no le mandés tus casos salvo que los pida).

**Mail de entrega:**
- Para: usuario UAT + equipo de pruebas
- Asunto: `[Tablero] - Certificación y prueba UAT PRE PBI XXXXX - [Descripción]`
- Adjunto: información del PBI para que el usuario arme sus propias pruebas
- Plazo: VoBo + evidencias (Word/Excel) en **4 días hábiles**

Después del VoBo: cargar evidencias en Test Plan, generar PDF, adjuntar en PBI.

---

## 10. Automatización (mínimo vital)

| Aspecto | Convención |
|---------|------------|
| Framework UI | **Selenium** (oficial). Java + JUnit. Data-driven |
| Repo | `[App]- Test` |
| Pipeline | `[App]-AUTOTESTF-CI` |
| Ramas | PBI → Release → Master. PR aprobado por líder Avianca |
| Ejecución | Ambiente QA, agente QA del cliente, con reporte y logs |
| Código | En **inglés** |
| En Azure | Test Plan del app → suite `Automatización_QA` → carpetas por módulo |
| PBI de automation | Type: `1. Automatización` (no impacta TTM) |
| Naming TC | `PBI-XXX Automatización # del caso: titulo` |
| Newman | Runner de API, **no reemplaza** Selenium para UI |

---

## 11. Verificación en BD

Esquemas documentados: `[rfd]`, `[master]`, `[adm]`. Siempre filtrar por solicitud/tiquete.

### Queries más usadas

```sql
-- Parámetros de cualquier app
SELECT * FROM [master].[MST_PARAMETERS]
WHERE parameter_code = '...';

-- VF: estado de la solicitud
SELECT STATUS, APPROVAL_DATE
FROM [rfd].[SR_MISSING_VALUE_REFUNDS_VF]
WHERE /* solicitud + tiquete */;

-- VF: historial de estados
SELECT * FROM [rfd].[SR_MISSING_VALUE_REFUND_STATUS_LOG_VF]
WHERE /* misma clave */;

-- VF: verificar que llegó a PI
SELECT * FROM [rfd].[PIC_PAYMENT_REQUEST_VF]
WHERE /* solicitud */;

-- NTC: notificación enviada (AVR)
SELECT TYP.NOTIF_TYPE_CODE, NOTIF.*
FROM [rfd].[AVR_CONTROL_NOTIFICATIONS] NOTIF
JOIN [az-sqla-avref-use-qa].[rfd].[AVR_TEMPLATE_CONFIGURATION] CONF
  ON NOTIF.TEMPLATE_ID = CONF.TEMPLATE_ID
JOIN [az-sqla-avref-use-qa].[rfd].[AVR_TYPE_OF_NOTIFICATIONS] TYP
  ON CONF.[NOTIF_TYPE_CODE] = TYP.[NOTIF_TYPE_CODE]
WHERE TYP.NOTIF_TYPE_CODE IN ('NTC23', 'NTC24');

-- Usuarios inactivos (cualquier app, misma estructura)
SELECT email, FIRST_NAME, LAST_NAME, last_login_date
FROM [adm].[MST_USER]
WHERE DATEDIFF(DAY, last_login_date, GETDATE()) >= 90;
```

---

## 12. Contradicciones conocidas en los manuales

No elegir una "de memoria". Confirmar en UI o BD.

| Contradicción | Qué hacer |
|--------------|-----------|
| VF: "En progreso" vs "En proceso" | Verificar el STATUS literal en BD |
| Severity Azure: 1=Critical vs F-S-V S: 4=Crítica | No mezclar. Son escalas distintas |
| SR §5 copia el texto de AVR | Verdad de SR = §2.1 Identificación |
| ROR cita SPs de AVR (`AVR_SP_USER_DATA_QUERY`) | Usar el nombre literal tal cual |

---

## 13. Tu primera semana

1. Leer este manual completo
2. Leer `lineamientos-qa.md` (es la ley del tablero)
3. Loguearte en las 4 apps en QA (ROR requiere VPN/red Avianca)
4. Seguir un VF de punta a punta en SR → PI → AVR con las queries de §11
5. Pedir accesos: tablero Azure, repos `*-Test`, pipelines, SQL QA, swaggers, SharePoint de automatización
6. Armar un PBI de práctica con las plantillas de `prompts/plantillas/`

Cuando llegue tu primer PBI real: criterios → casos en Test Plan → data → ejecución con evidencia → bug si falla → mail UAT → VoBo 4 días → PDF en el PBI → Done.
