# QA DevOps Suite — Instrucciones del Proyecto

## Arquitectura de respuesta

```
Usuario
  ↓
  ├── Skill especializado 1 (genera draft + cita references/)
  ├── Skill especializado 2 (genera draft + cita references/)  ← si la pregunta toca varios dominios
  ├── ...
  ↓
Orquestador-Validador
  ├── Cruza drafts contra references/ (documentación técnica oficial)
  ├── Cruza contra base_conocimiento/ (contexto del producto y equipo)
  ├── Ejecuta checklist A–D
  ├── Calibración E: reconfirma cada ⚠️ y cada columna/rol/estado/path contra el manual
  ↓
Respuesta final al usuario (con fuentes, marcas de confianza y tabla Calibración)
```

**Regla #1:** Ningún skill responde directo al usuario. Todo pasa por `orquestador-validador`.
**Regla #2:** Si algo no se puede verificar contra las fuentes, se marca como "no verificado" — nunca se inventa.
**Regla #3:** Cada skill trabaja de forma independiente consultando sus propios `references/`.

## Fuentes de conocimiento (2 capas)

### Capa 1 — `references/` (dentro de cada skill)
Documentación técnica oficial verificable:
- Microsoft Learn para Azure DevOps
- ISTQB CTFL Syllabus v4.0 para técnicas de QA
- Documentación oficial de Selenium, Nightwatch.js, Postman/Newman
- Cucumber/Gherkin para criterios de aceptación
- Catálogos de APIs y tablas Refund (skills `postman` y `db-relacional`)

### Capa 2 — `base_conocimiento/` (raíz del proyecto)
Información específica del producto y equipo, mantenida manualmente:
- `manual-aplicacion-sr.md` — Special Refund (SR)
- `manual-aplicacion-avr.md` — AV Refund (AVR)
- `manual-aplicacion-pi.md` — Payment Integrator (PI)
- `manual-aplicacion-ror.md` — Refund Orchestration Rules (ROR)
- `lineamientos-qa.md` — Lineamientos de QA del equipo (Avianca)

Los skills deben consultar `base_conocimiento/` cuando la pregunta del usuario se refiere al producto, sus flujos, APIs, tablas de BD, o procesos del equipo.

## Skills disponibles

| Skill | Dominio | Independiente |
|---|---|---|
| `azure-devops` | Boards, Pipelines YAML, Repos, REST API | Sí |
| `qa-funcional` | Técnicas ISTQB, bug reports F-S-V, Gherkin | Sí |
| `qa-automation` | Selenium, Nightwatch.js, POM (UI) | Sí |
| `postman` | Colecciones, scripts `pm.test`, Newman, APIs SR/AVR/PI/ROR | Sí |
| `db-relacional` | SQL de verificación, catálogo de tablas, SPs Refund | Sí |
| `analizador-informacion` | Estructurar info cruda + scoring de fuentes | Sí (soporte) |
| `comunicacion-daily` | Speech de daily a partir del resumen y de `test-cases/` | Sí |
| `orquestador-validador` | Gate de calidad — valida y entrega respuesta final | Sí (obligatorio) |

## Flujo para preguntas multi-dominio

Si una pregunta toca varios dominios, el orquestador activa **todos** los skills del dominio y consulta el mapa `skills/orquestador-validador/references/mapa-productos-refund.md`.

Ejemplos:

- "Automatizo el masivo SR con Selenium y lo subo al pipeline" → `qa-automation` + `azure-devops` + `db-relacional` (tabla `SP_REF_LOAD_MASSIVE_REQUEST`) + manual SR.
- "Colección Postman del VF y queries de verificación" → `postman` + `db-relacional` + manuales SR y PI.
- "Casos de prueba del pago PI" → `qa-funcional` + `db-relacional` + `postman` (si hay API) + manual PI.
- "Maestra EMD de ROR y ListHomologation" → `qa-funcional` + `postman` + `db-relacional` + manual ROR.
- "Speech de la daily con lo de ayer" → `comunicacion-daily`, leyendo el resumen del usuario y `test-cases/`. El entregable es solo el speech.

Ningún skill inventa tablas, paths o estados que no estén en `references/` o `base_conocimiento/`.

## Idioma

Español para todo el contenido, excepto términos técnicos sin traducción estándar (endpoint, pipeline, pull request, Page Object, etc.).
