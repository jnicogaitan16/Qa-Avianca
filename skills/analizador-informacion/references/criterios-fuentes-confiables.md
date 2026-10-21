# Criterios de Confiabilidad de Fuentes

Este documento define la escala de confiabilidad usada por el skill `analizador-informacion` para puntuar fuentes externas citadas en respuestas.

## Escala de confiabilidad (0-5)

### Score 5 — Documentación oficial del proveedor

**Criterio:** Documentación publicada y mantenida por el creador/propietario de la tecnología.

**Ejemplos:**
- `learn.microsoft.com` para Azure DevOps
- `selenium.dev/documentation` para Selenium
- `nightwatchjs.org/guide` para Nightwatch.js
- `learning.postman.com/docs` para Postman
- `docs.python.org` para Python
- `developer.mozilla.org` (MDN) para estándares web

**Por qué score 5:** El proveedor tiene acceso directo al código fuente y al roadmap. La información es de primera mano y se actualiza con cada release.

**Riesgo residual:** Puede estar desactualizada si el proveedor no mantiene bien su documentación. Verificar la fecha de "last updated" si está disponible.

---

### Score 4 — Estándares reconocidos de la industria

**Criterio:** Documentos publicados por organismos de estandarización o cuerpos profesionales reconocidos internacionalmente.

**Ejemplos:**
- ISTQB Foundation Level Syllabus
- RFCs (IETF)
- IEEE 829 (documentación de testing)
- W3C specifications
- OWASP guidelines

**Por qué score 4:** Pasan por procesos de revisión rigurosos y representan consenso de la industria. Son estables pero pueden quedar atrás de la práctica actual.

**Riesgo residual:** Pueden ser más teóricos que prácticos. Versiones antiguas pueden no reflejar prácticas modernas.

---

### Score 3 — Documentación de terceros reconocidos

**Criterio:** Contenido técnico publicado por organizaciones o individuos con reputación establecida en el campo, aunque no sean los creadores de la tecnología.

**Ejemplos:**
- Tutoriales de DigitalOcean
- Artículos de Martin Fowler (martinfowler.com)
- Thoughtworks Technology Radar
- Blogs oficiales de empresas reconocidas (Google Developers, AWS blogs)
- Libros de O'Reilly, Addison-Wesley

**Por qué score 3:** Reputación a cuidar + revisión editorial. La información suele ser precisa pero es de segunda mano.

**Riesgo residual:** Puede simplificar, omitir edge cases, o quedar desactualizada respecto a la fuente oficial.

---

### Score 2 — Comunidad curada

**Criterio:** Contenido generado por la comunidad pero con mecanismos de curación (votación, moderación, revisión de pares).

**Ejemplos:**
- Stack Overflow (respuestas aceptadas o con alta votación)
- GitHub Issues/Discussions en repos oficiales
- Reddit (posts con alta votación en subreddits especializados)
- Dev.to (artículos con engagement significativo)

**Por qué score 2:** La curación comunitaria filtra errores obvios, pero no garantiza precisión técnica.

**Riesgo residual:** Respuestas populares no siempre son correctas. El contexto del preguntador puede diferir del nuestro. Las respuestas envejecen.

**Regla especial:** Una respuesta de Stack Overflow que cita documentación oficial hereda el score de la fuente citada (no el score 2 de SO), siempre que el enlace sea verificable.

---

### Score 1 — Contenido sin curación

**Criterio:** Contenido publicado sin revisión de pares ni mecanismos de calidad.

**Ejemplos:**
- Blogs personales sin reputación establecida
- Posts de Medium sin verificación
- Tutoriales en YouTube sin respaldo documental
- Foros sin moderación
- Wikis abiertas sin revisión

**Por qué score 1:** Sin filtro de calidad. Puede ser correcto pero no hay forma de saberlo sin verificación independiente.

**Uso permitido:** Solo como pista para investigar más — nunca como fuente única para una afirmación técnica.

---

### Score 0 — Sin fuente identificable

**Criterio:** La afirmación no tiene ninguna fuente rastreable. Incluye "conocimiento general", "es sabido que...", o información generada puramente desde la memoria del modelo.

**Ejemplos:**
- "Azure DevOps por defecto usa..." (sin cita)
- "Es una buena práctica..." (sin referencia)
- "Generalmente se recomienda..." (sin fuente)

**Por qué score 0:** Sin fuente = sin verificabilidad = riesgo de alucinación.

**Acción requerida:** Toda afirmación con score 0 debe marcarse como "⚠️ No verificado" o encontrarse una fuente que la respalde antes de incluirla en la respuesta final.

---

## Reglas de aplicación

1. **El score mínimo aceptable para una afirmación técnica en la respuesta final es 3.** Afirmaciones respaldadas solo por fuentes score 0-2 deben marcarse con advertencia.

2. **El score se asigna a la fuente, no a la afirmación.** Una afirmación correcta sin fuente sigue siendo score 0.

3. **Múltiples fuentes suman confianza:** Si una afirmación tiene respaldo en una fuente score 2 Y una score 3, se toma el score más alto (3), no se suman.

4. **La fecha importa:** Una fuente score 5 de hace 3+ años para una tecnología que se actualiza frecuentemente baja a score 3. Usar el criterio de `last_updated` cuando esté disponible.

5. **El contexto importa:** Una respuesta de Stack Overflow sobre un error específico con código reproducible puede ser más útil que documentación oficial genérica. En ese caso, usar score 2 pero marcar como "verificado empíricamente".

---

## Fuentes

Este documento es un diseño interno del proyecto qa-devops-suite. La escala está inspirada en principios de evaluación de fuentes de información (librería académica, fact-checking periodístico) adaptados al contexto de documentación técnica.

Fecha de creación: 2026-09-22
