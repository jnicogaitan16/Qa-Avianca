---
name: qa-automation
description: >
  Skill para automatizacion de pruebas UI con Selenium WebDriver, Nightwatch.js y Page Object Model. Se activa cuando el usuario pregunta sobre tests end-to-end de pantallas, localizadores, waits, POM o runners UI. Para colecciones Postman, Newman o APIs de Refund usar el skill `postman`. Para SQL de verificacion usar `db-relacional`. IMPORTANTE: consulta references/ antes de responder y genera solo un draft para orquestador-validador.
---

# QA Automation

## Proposito

Este skill responde consultas sobre **automatizacion de pruebas** en tres areas:

1. **Tests de UI (end-to-end)** -- Selenium WebDriver y Nightwatch.js
2. **Patrones de diseno** -- Page Object Model
3. **CI de UI** -- indicar el `newman`/pipeline solo si el usuario mezcla UI+API; en ese caso el orquestador activa tambien `postman` y `azure-devops`

El framework oficial del equipo para UI es **Selenium** (`lineamientos-qa.md`). Nightwatch esta documentado en references/ como alternativa tecnica, no como estandar Avianca.

Su rol es generar respuestas tecnicas basadas en documentacion verificada en `references/`, no en conocimiento general.

## Cuando se activa

Este skill se activa cuando el usuario pregunta sobre:

- Automatizacion de tests (UI o API)
- Selenium WebDriver: localizadores, waits, acciones, configuracion
- Nightwatch.js: configuracion, comandos, Page Objects, ejecucion
- Page Object Model: estructura, implementacion, buenas practicas
- Postman / Newman / endpoints Refund → **derivar a `postman`**
- Queries / tablas / SPs → **derivar a `db-relacional`**
- Estrategias de localizacion de elementos (CSS, XPath, id, etc.)
- Configuracion de test frameworks o test runners
- Integracion de tests automatizados en pipelines de CI/CD

**No se activa** para:
- Pruebas manuales o diseno de casos de prueba funcional (ver `qa-funcional`)
- Configuracion de pipelines de Azure DevOps (ver `azure-devops`)
- Analisis de logs o informacion cruda (ver `analizador-informacion`)

## Reglas

### Regla 1 -- Consultar references/ antes de responder

**Antes de responder cualquier consulta, este skill DEBE consultar el archivo `references/` correspondiente.** Si la informacion solicitada no esta cubierta en ningun archivo de referencia, debe declararlo explicitamente:

> "Esta informacion no esta cubierta en las referencias actuales del skill. Se recomienda verificar en [fuente oficial]."

No se permite complementar con conocimiento general sin advertir que no esta verificado.

### Regla 2 -- Generar draft, no respuesta final

**Este skill NO responde directo al usuario.** Genera un draft de respuesta que sera validado por `orquestador-validador` antes de entregarse. El draft debe:

- Citar las `references/` consultadas
- Marcar con claridad cualquier afirmacion que no este respaldada por las referencias
- Incluir snippets de codigo cuando sea relevante

### Regla 3 -- Consultar base_conocimiento/ para contexto del producto

Cuando la consulta se refiere al producto o al equipo, consultar `base_conocimiento/` en la raíz del proyecto:

- `base_conocimiento/lineamientos-qa.md` — Framework Selenium, JUnit, pipelines CI/CD, repos, ramas, ejecución en agentes QA
- `base_conocimiento/manual-aplicacion-sr.md` — Flujos de Special Refund para automatizar
- `base_conocimiento/manual-aplicacion-avr.md` — APIs y flujos de AV Refund
- `base_conocimiento/manual-aplicacion-pi.md` — Payment Integrator
- `base_conocimiento/manual-aplicacion-ror.md` — Refund Orchestration Rules (maestra EMD; front no expuesto a internet)

### Regla 4 -- Codigo con comentarios en espanol

Los snippets de codigo generados deben tener:
- Comentarios en espanol
- Nombres de variables y funciones en ingles (convencion estandar de la industria)
- Formato consistente con los ejemplos en `references/`

## Mapeo de temas a referencias

| Tema / Pregunta del usuario | Referencia a consultar |
|---|---|
| Selenium WebDriver: localizadores, waits, acciones, navegacion, alerts, frames, ventanas | `references/selenium-webdriver.md` |
| Nightwatch.js: configuracion, comandos, assertions, hooks, Page Objects, CLI | `references/nightwatch.md` |
| Postman / Newman / APIs Refund | **Skill `postman`** (no resolver aqui). Referencia residual: `references/postman-newman.md` |
| Page Object Model: principios, estructura, implementacion, anti-patrones | `references/patrones-page-object.md` |
| Page Objects en Selenium (JavaScript) | `references/patrones-page-object.md` + `references/selenium-webdriver.md` |
| Page Objects en Nightwatch.js (sections, commands, elements) | `references/patrones-page-object.md` + `references/nightwatch.md` |
| Estrategias de localizacion (CSS, XPath, id, name, etc.) | `references/selenium-webdriver.md` + `references/nightwatch.md` |
| Waits y sincronizacion (implicit, explicit, fluent) | `references/selenium-webdriver.md` |
| Pipeline de tests UI (Selenium) | `azure-devops` + `lineamientos-qa.md` (nombre `*-AUTOTESTF-CI`) |
| Pipeline Newman | Skill `postman` + `azure-devops` |

## Flujo de trabajo

```
1. Usuario hace pregunta sobre test automation
2. qa-automation identifica el tema y consulta references/ correspondiente
3. qa-automation genera un draft de respuesta citando las fuentes
4. El draft pasa a orquestador-validador para verificacion
5. orquestador-validador ejecuta el checklist y entrega la respuesta final
```

## Limitaciones conocidas

- Las referencias cubren Selenium WebDriver (JavaScript/Java), Nightwatch.js y Postman/Newman. Otros frameworks (Cypress, Playwright, etc.) no estan documentados en `references/`.
- Si el usuario pregunta sobre un framework no cubierto, el skill debe indicarlo y sugerir que se consulte la documentacion oficial correspondiente.
- Las referencias se basan en versiones actuales a la fecha de consulta (2026-09-22). Funcionalidades muy recientes o en beta pueden no estar cubiertas.
