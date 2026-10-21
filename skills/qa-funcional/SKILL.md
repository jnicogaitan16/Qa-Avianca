---
name: qa-funcional
description: >
  Skill para QA funcional: técnicas de diseño de casos de prueba basadas en ISTQB (partición de equivalencia, valores límite, tablas de decisión, transición de estados), plantillas de bug report con prioridad F-S-V, y criterios de aceptación en formato Given-When-Then. Se activa cuando el usuario pregunta sobre diseño de casos de prueba, reportes de bugs, o definición de criterios de aceptación. IMPORTANTE: consulta references/ antes de responder y genera solo un draft para validación por orquestador-validador.
---

# QA Funcional

## Propósito

Este skill cubre las prácticas de **QA funcional manual**: diseño de casos de prueba, reporte de defectos y definición de criterios de aceptación. Toda la información se basa en fuentes documentadas en `references/` y se alinea con el ISTQB CTFL Syllabus v4.0 (2023), convenciones de equipo (modelo F-S-V) y la especificación Gherkin de Cucumber.

Este skill **no responde directamente al usuario**. Genera un draft que pasa por `orquestador-validador` antes de convertirse en respuesta final.

---

## Cuándo se activa

Este skill se activa cuando el usuario pregunta sobre cualquiera de los siguientes temas:

### Diseño de casos de prueba
- Cómo diseñar casos de prueba para una funcionalidad
- Técnicas ISTQB: partición de equivalencia, valores límite, tablas de decisión, transición de estados
- Cuántas pruebas necesito para cubrir un requisito
- Combinación de técnicas de prueba
- Cobertura de pruebas funcionales

### Reportes de bugs
- Cómo escribir un bug report
- Plantilla o template de reporte de defectos
- Prioridad de bugs, severidad, modelo F-S-V
- Campos de un buen reporte de bugs
- Ciclo de vida de un defecto

### Criterios de aceptación
- Cómo escribir criterios de aceptación
- Formato Given-When-Then
- Sintaxis Gherkin (Feature, Scenario, Scenario Outline, Background, Examples)
- Buenas prácticas para archivos .feature
- BDD (Behavior-Driven Development) aplicado a QA

### Frases que activan este skill
- "Diseñame casos de prueba para..."
- "Necesito un bug report de..."
- "Escribime los criterios de aceptación para..."
- "Qué técnica de testing uso para...?"
- "Cómo reporto este bug?"
- "Escribime los scenarios para esta user story"
- "Qué prioridad tiene este bug?"

---

## Regla fundamental: consultar references/ primero

**SIEMPRE** antes de generar cualquier respuesta, este skill debe:

1. Identificar qué tema(s) aborda la pregunta del usuario
2. Consultar el archivo de referencia correspondiente (ver mapeo abajo)
3. Basar la respuesta en lo documentado en `references/`
4. Si la información no está en `references/`, indicarlo explícitamente en el draft

**Nunca inventar técnicas, campos o formatos que no estén documentados en las referencias.**

---

## Regla de salida: draft para orquestador-validador

Este skill **NO entrega respuestas directas al usuario**. El flujo es:

```
Usuario pregunta --> qa-funcional consulta references/ --> genera DRAFT --> orquestador-validador valida --> respuesta final
```

El draft generado debe incluir:

1. **La respuesta al usuario** — basada en las referencias consultadas
2. **Referencias utilizadas** — qué archivos `references/*.md` se consultaron
3. **Nivel de confianza** — qué parte de la respuesta está respaldada por las referencias y qué parte no se pudo verificar

### Formato del draft

```
## Draft de respuesta

[Contenido de la respuesta]

---
**Metadata del draft:**
- Skill: qa-funcional
- Referencias consultadas: [lista de archivos]
- Confianza: [ALTA si todo está en references/ | MEDIA si hay partes inferidas | BAJA si hay contenido no verificable]
- Items no verificados: [lista, si aplica]
```

---

## Mapeo de temas a referencias

| Tema del usuario | Archivo de referencia | Secciones clave |
|---|---|---|
| Técnicas de diseño de casos | `references/tecnicas-diseno-casos.md` | Partición de equivalencia, Valores límite, Tablas de decisión, Transición de estados |
| Partición de equivalencia | `references/tecnicas-diseno-casos.md` | Sección 1 |
| Valores límite / boundary | `references/tecnicas-diseno-casos.md` | Sección 2 |
| Tablas de decisión | `references/tecnicas-diseno-casos.md` | Sección 3 |
| Transición de estados | `references/tecnicas-diseno-casos.md` | Sección 4 |
| Qué técnica usar | `references/tecnicas-diseno-casos.md` | Cuándo usar cada técnica |
| Bug report / reporte de defecto | `references/plantillas-bug-report.md` | Template completo, Campos estándar |
| Prioridad de bugs / F-S-V | `references/plantillas-bug-report.md` | Modelo de Prioridad F-S-V |
| Severidad vs. prioridad | `references/plantillas-bug-report.md` | Escalas F, S, V |
| Ciclo de vida de bugs | `references/plantillas-bug-report.md` | Ciclo de vida de un Bug |
| Cómo escribir un buen bug | `references/plantillas-bug-report.md` | Buenas prácticas |
| Plantillas de trabajo (CA, Plan, ejecución, UAT) | `prompts/plantillas/` | Un archivo por momento |
| Criterios de aceptación | `references/criterios-aceptacion.md` | Given-When-Then en detalle |
| Given-When-Then / GWT | `references/criterios-aceptacion.md` | Given-When-Then en detalle |
| Gherkin / Feature files | `references/criterios-aceptacion.md` | Estructura de archivo .feature, Keywords |
| Scenario Outline | `references/criterios-aceptacion.md` | Scenario Outline con Examples |
| Background | `references/criterios-aceptacion.md` | Background |
| Buenas prácticas Gherkin | `references/criterios-aceptacion.md` | Buenas prácticas, Anti-patrones |
| Gherkin en español | `references/criterios-aceptacion.md` | Gherkin en español |

---

## Comportamiento esperado por tipo de consulta

### Cuando piden diseñar casos de prueba

1. Consultar `references/tecnicas-diseno-casos.md`
2. Identificar qué técnica(s) aplican según la naturaleza del requisito
3. Aplicar la técnica siguiendo los pasos documentados (particiones, límites, reglas, estados)
4. Generar los casos de prueba con el formato:
   - ID del caso
   - Precondiciones
   - Datos de entrada
   - Pasos
   - Resultado esperado
5. Indicar la cobertura alcanzada

### Cuando piden un bug report

1. Consultar `references/plantillas-bug-report.md`
2. Usar el template completo documentado
3. Aplicar el modelo F-S-V para calcular la prioridad
4. Incluir todos los campos obligatorios
5. Si el usuario da información parcial, completar lo que se pueda e indicar qué falta

### Cuando piden criterios de aceptación

1. Consultar `references/criterios-aceptacion.md`
2. Escribir en formato Gherkin (Given-When-Then)
3. Incluir escenarios positivos y negativos
4. Usar Scenario Outline cuando haya variaciones de datos
5. Seguir las buenas prácticas documentadas (lenguaje de negocio, un comportamiento por escenario, etc.)

---

## Consultar base_conocimiento/ para contexto del equipo

Cuando la pregunta se refiere a procesos del equipo o al producto, consultar:
- `base_conocimiento/lineamientos-qa.md` — Cómo se documentan Test Plans, Test Suites, Bugs, impedimentos y evidencias en Azure DevOps
- `base_conocimiento/manual-aplicacion-sr.md`, `manual-aplicacion-avr.md`, `manual-aplicacion-pi.md`, `manual-aplicacion-ror.md` — Flujos del producto
- Mapa corto: `skills/orquestador-validador/references/mapa-productos-refund.md`

Si el caso de prueba debe **verificar persistencia**, el draft debe decir que el orquestador active `db-relacional` (no inventar SQL aqui). Si debe **pegarle a un endpoint**, activar `postman`. Un caso Refund completo suele ser: Gherkin (`qa-funcional`) + request (`postman`) + SELECT (`db-relacional`) + work item (`azure-devops`).

Plantillas listadas para copiar (solo campos documentados): `prompts/plantillas/README.md`.

---

## Limitaciones

- Este skill cubre **QA funcional manual**. Para automatización (Selenium, Nightwatch, Postman), usar el skill `qa-automation`.
- Las técnicas documentadas son las cuatro de caja negra del nivel ISTQB Foundation. Técnicas avanzadas (pairwise, classification trees) no están cubiertas en las referencias actuales.
- El modelo F-S-V es una **convención de equipo**, no un estándar de la industria. No presentarlo como estándar universal.
- Las referencias se basan en el ISTQB CTFL Syllabus v4.0 (2023), la documentación de Cucumber y estándares IEEE. Si se necesita información más reciente, se debe actualizar `references/`.

---

## Archivos de referencia

```
qa-funcional/
├── SKILL.md                                    # Este archivo
└── references/
    ├── tecnicas-diseno-casos.md                # ISTQB: EP, BVA, DT, ST
    ├── plantillas-bug-report.md                # Bug report template + F-S-V
    └── criterios-aceptacion.md                 # Gherkin, GWT, buenas prácticas
```
