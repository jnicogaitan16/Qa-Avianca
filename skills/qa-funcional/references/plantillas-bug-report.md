# Plantillas de Bug Report

Referencia de formatos y mejores prácticas para la redacción de reportes de defectos en QA funcional. Incluye la convención de equipo **Prioridad F-S-V** (Frecuencia-Severidad-Visibilidad) y un template completo alineado con estándares de la industria.

---

## Estándar de referencia: IEEE 829

El estándar **IEEE 829** (Standard for Software and System Test Documentation) define la estructura documental para pruebas de software, incluyendo el "Test Incident Report" (reporte de incidentes). Si bien fue reemplazado por ISO/IEC/IEEE 29119, los campos esenciales siguen siendo la base de cualquier bug report profesional:

- Identificador único
- Resumen del incidente
- Descripción detallada
- Impacto
- Pasos para reproducir
- Entorno de prueba
- Evidencia

---

## Campos estándar de un Bug Report

| Campo | Descripción | Obligatorio |
|---|---|---|
| **ID** | Identificador único del defecto (generado por la herramienta) | Si |
| **Título** | Resumen conciso en una línea: [QUE falló] + [DONDE] + [CUANDO] | Si |
| **Proyecto / Módulo** | Área funcional o componente afectado | Si |
| **Entorno** | SO, navegador/versión, dispositivo, ambiente (DEV/QA/STG/PROD) | Si |
| **Versión / Build** | Versión de la aplicación donde se encontró el defecto | Si |
| **Precondiciones** | Estado necesario antes de ejecutar los pasos (usuario logueado, datos cargados, etc.) | Si |
| **Pasos para reproducir** | Secuencia numerada, clara y específica | Si |
| **Resultado esperado** | Qué debería ocurrir según el requisito o criterio de aceptación | Si |
| **Resultado actual** | Qué ocurre realmente (el defecto) | Si |
| **Evidencia** | Screenshots, videos, logs, request/response HTTP | Si |
| **Severidad** | Impacto técnico del defecto (ver sección F-S-V) | Si |
| **Prioridad F-S-V** | Evaluación integral: Frecuencia + Severidad + Visibilidad | Si |
| **Estado** | Nuevo, Abierto, En progreso, Resuelto, Cerrado, Reabierto | Si |
| **Asignado a** | Responsable de la corrección | No |
| **Sprint / Iteración** | Sprint en el que se reporta | No |
| **Etiquetas / Tags** | Clasificación adicional (regresión, bloqueo, UX, etc.) | No |
| **Notas adicionales** | Workarounds, contexto de negocio, frecuencia observada | No |

---

## Modelo de Prioridad F-S-V (Convención de equipo)

### Definición

El modelo **F-S-V** es una convención interna del equipo para determinar la **prioridad de resolución** de un defecto evaluando tres dimensiones independientes:

| Dimensión | Pregunta clave | Evalúa |
|---|---|---|
| **F — Frecuencia** | ¿Con qué frecuencia ocurre? | Reproducibilidad y alcance de usuarios afectados |
| **S — Severidad** | ¿Qué tan grave es el impacto técnico/funcional? | Daño al sistema, datos o funcionalidad |
| **V — Visibilidad** | ¿Quién lo ve? ¿Es evidente? | Exposición ante usuarios, clientes o stakeholders |

### Escala de Frecuencia (F)

| Nivel | Valor | Criterio |
|---|---|---|
| **Alta** | 3 | Ocurre siempre (100% reproducible) o afecta a la mayoría de usuarios |
| **Media** | 2 | Ocurre intermitentemente o bajo condiciones específicas |
| **Baja** | 1 | Ocurre raramente, difícil de reproducir, o afecta a un subconjunto muy pequeño |

### Escala de Severidad (S)

| Nivel | Valor | Criterio |
|---|---|---|
| **Crítica** | 4 | Sistema caído, pérdida de datos, vulnerabilidad de seguridad, sin workaround |
| **Alta** | 3 | Funcionalidad principal rota, pero existe workaround parcial |
| **Media** | 2 | Funcionalidad secundaria afectada, no bloquea flujo principal |
| **Baja** | 1 | Defecto cosmético, typo, mejora menor de UX |

### Escala de Visibilidad (V)

| Nivel | Valor | Criterio |
|---|---|---|
| **Alta** | 3 | Visible para todos los usuarios finales o clientes externos |
| **Media** | 2 | Visible para usuarios internos o en flujos frecuentes pero no principales |
| **Baja** | 1 | Solo visible en flujos edge-case, admin, o entornos de desarrollo |

### Cálculo de prioridad

**Puntaje total = F + S + V** (rango: 3 a 10)

| Rango | Prioridad resultante | Acción |
|---|---|---|
| **8-10** | P1 — Crítica | Resolver de inmediato. Bloquea release. |
| **5-7** | P2 — Alta | Resolver en el sprint actual. |
| **3-4** | P3 — Baja | Planificar para sprint futuro o backlog. |

### Ejemplo de evaluación F-S-V

**Bug**: "El botón 'Guardar' en el formulario de perfil no responde al hacer clic."

| Dimensión | Evaluación | Valor |
|---|---|---|
| Frecuencia | Ocurre siempre al hacer clic | F = 3 |
| Severidad | Funcionalidad principal rota (no se puede guardar), sin workaround | S = 3 |
| Visibilidad | Visible para todos los usuarios que editan su perfil | V = 3 |
| **Total** | | **9 --> P1 Crítica** |

**Bug**: "El ícono de notificaciones se ve pixelado en resolución 4K."

| Dimensión | Evaluación | Valor |
|---|---|---|
| Frecuencia | Solo en pantallas 4K (minoría de usuarios) | F = 1 |
| Severidad | Cosmético, no afecta funcionalidad | S = 1 |
| Visibilidad | Visible solo para usuarios con pantalla 4K | V = 1 |
| **Total** | | **3 --> P3 Baja** |

---

## Template completo de Bug Report

```markdown
# [BUG] [Módulo/Funcionalidad] - Breve descripción del defecto

## Información general

| Campo | Valor |
|---|---|
| **ID** | BUG-XXXX |
| **Fecha** | YYYY-MM-DD |
| **Reportado por** | [nombre] |
| **Proyecto** | [nombre del proyecto] |
| **Módulo** | [módulo o funcionalidad] |
| **Entorno** | [OS, Navegador/versión, Dispositivo, Ambiente] |
| **Versión / Build** | [versión de la app] |
| **Estado** | Nuevo |
| **Asignado a** | [pendiente / nombre] |

## Prioridad F-S-V

| Dimensión | Nivel | Valor |
|---|---|---|
| Frecuencia | [Alta/Media/Baja] | [3/2/1] |
| Severidad | [Crítica/Alta/Media/Baja] | [4/3/2/1] |
| Visibilidad | [Alta/Media/Baja] | [3/2/1] |
| **Total** | | **[suma] --> P[1/2/3]** |

## Descripción

### Resumen
[1-2 oraciones describiendo el defecto de forma clara y directa.]

### Dónde sucede
[Pantalla, URL, sección, flujo específico donde se manifiesta el defecto.]

### Precondiciones
1. [Estado previo necesario para reproducir]
2. [Datos de prueba requeridos]

### Pasos para reproducir
1. [Paso 1 — acción concreta]
2. [Paso 2 — acción concreta]
3. [Paso 3 — acción concreta]
4. ...

### Resultado esperado
[Descripción clara de lo que DEBERÍA ocurrir según el requisito o criterio de aceptación.]

### Resultado actual
[Descripción clara de lo que REALMENTE ocurre. Incluir mensajes de error exactos si aplica.]

### Antecedentes
[Contexto adicional relevante:]
- ¿Funcionaba antes? ¿Desde cuándo falla?
- ¿Hay workaround conocido?
- ¿Está relacionado con otro bug?
- ¿Se intentó en otros navegadores/dispositivos?

## Evidencia

- [ ] Screenshot(s) adjuntos
- [ ] Video de reproducción
- [ ] Logs del navegador (Console)
- [ ] Network trace (HAR o request/response relevante)
- [ ] Logs del servidor (si aplica)

## Notas adicionales
[Cualquier información extra que ayude al desarrollador a entender o reproducir el defecto.]
```

---

## Buenas prácticas para redactar Bug Reports

### Título efectivo

**Fórmula**: `[QUE falla] + [DONDE] + [CUANDO/condición]`

| Mal titulo | Buen titulo |
|---|---|
| "No funciona" | "El botón Guardar no responde en el formulario de perfil al hacer clic" |
| "Error en pagos" | "Se muestra error 500 al procesar pago con tarjeta VISA en checkout" |
| "Bug de login" | "Login permite acceso con contraseña vacía en pantalla de inicio de sesión" |

### Pasos para reproducir

- Escribir en **imperativo**: "Hacer clic en...", "Ingresar el valor...", "Navegar a..."
- Ser **específico**: incluir datos exactos usados (usuario, valores, URLs)
- Ser **mínimo**: incluir solo los pasos necesarios para reproducir, sin ruido
- **Numerar** cada paso
- Indicar si requiere un **estado previo** particular (precondiciones)

### Resultado esperado vs. actual

- El resultado esperado debe referirse a un **requisito documentado** o criterio de aceptación cuando sea posible.
- El resultado actual debe ser **observable y verificable**: incluir mensajes de error textuales, códigos HTTP, comportamiento visual exacto.
- Evitar interpretaciones subjetivas como "se ve mal" -- describir qué se ve exactamente.

### Evidencia

- **Screenshots**: marcar con flechas o recuadros el área del defecto.
- **Videos**: útiles para defectos de interacción, animaciones, timing.
- **Logs**: copiar el texto del error, no solo captura de pantalla del log.
- **Network**: incluir el request/response HTTP relevante para errores de API.

---

## Ciclo de vida de un Bug

```
Nuevo --> Abierto --> En progreso --> Resuelto --> Verificado --> Cerrado
                          |               |
                          v               v
                       Rechazado      Reabierto
                       (no es bug /   (verificación
                        duplicado)     falló)
```

| Estado | Responsable | Descripción |
|---|---|---|
| **Nuevo** | QA | Bug recién reportado, pendiente de revisión |
| **Abierto** | Lead/PM | Confirmado y aceptado para corrección |
| **En progreso** | Dev | Desarrollador trabajando en la corrección |
| **Resuelto** | Dev | Corrección implementada, lista para verificar |
| **Verificado** | QA | QA confirmó que la corrección funciona |
| **Cerrado** | QA/Lead | Defecto resuelto definitivamente |
| **Reabierto** | QA | La verificación falló, el defecto persiste |
| **Rechazado** | Lead/Dev | No es un defecto, es duplicado, o no se corregirá |

---

## Fuentes

- **IEEE 829-2008**: IEEE Standard for Software and System Test Documentation. Institute of Electrical and Electronics Engineers. Disponible en: https://standards.ieee.org/standard/829-2008.html — Consultado: 2026-09-22
- **ISO/IEC/IEEE 29119-3:2021**: Software and systems engineering — Software testing — Part 3: Test documentation. Referencia para estructura de reportes de incidentes. — Consultado: 2026-09-22
- **ISTQB CTFL Syllabus v4.0** (2023). Sección 5.3: Defect Management. Disponible en: https://www.istqb.org/certifications/certified-tester-foundation-level — Consultado: 2026-09-22
- **Modelo F-S-V**: Convención interna del equipo. No corresponde a un estándar externo; es una adaptación propia para priorización de defectos combinando tres dimensiones: Frecuencia, Severidad y Visibilidad. — Documentado: 2026-09-22
