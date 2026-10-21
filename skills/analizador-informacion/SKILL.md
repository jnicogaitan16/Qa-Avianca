---
name: analizador-informacion
description: >
  Skill para recibir información cruda (logs, respuestas de API, texto de tickets, capturas de Sentry, outputs de consola) y estructurarla en un formato analizable. También puntúa la confiabilidad de fuentes externas usadas en respuestas. Se activa cuando el usuario pega información desestructurada pidiendo análisis, cuando hay que evaluar la calidad de una fuente citada, o cuando otro skill necesita pre-procesar datos antes de responder. Este skill es insumo del orquestador — NO responde directo al usuario.
---

# Analizador de Información

## Propósito

Este skill cumple dos funciones:

1. **Estructurar información cruda** — Recibe datos desestructurados y los organiza en un formato analizable
2. **Puntuar confiabilidad de fuentes** — Evalúa qué tan confiable es cada fuente utilizada en una respuesta

Es un skill de **soporte interno**: sus resultados alimentan al orquestador-validador y a otros skills. **No responde directamente al usuario.**

## Cuándo se activa

- Cuando el usuario pega **logs, stack traces, respuestas de API o texto de tickets** pidiendo análisis
- Cuando otro skill necesita **evaluar la confiabilidad** de una fuente externa antes de citarla
- Cuando hay **información ambigua o contradictoria** que requiere estructuración antes de poder responder
- Cuando el usuario comparte **capturas de Sentry, outputs de consola, o datos de monitoring**

## Función 1 — Estructuración de información cruda

### Tipos de entrada soportados

| Tipo de entrada | Qué extraer |
|---|---|
| Stack trace / logs | Timestamp, nivel de error, mensaje, archivo:línea, causa raíz probable |
| Respuesta de API (JSON/XML) | Status code, headers relevantes, cuerpo estructurado, errores |
| Texto de ticket / issue | Resumen, pasos para reproducir, resultado esperado vs actual, prioridad |
| Output de Sentry | Evento, fingerprint, breadcrumbs, tags, frecuencia |
| Output de consola (Newman, npm, build) | Comando ejecutado, resultado (pass/fail), errores específicos, warnings |

### Formato de salida estructurada

```yaml
tipo_entrada: "stack_trace|api_response|ticket|sentry|console_output"
resumen: "descripción en una línea"
datos_clave:
  - campo: valor
  - campo: valor
errores_identificados:
  - descripcion: "qué falló"
    severidad: "critico|alto|medio|bajo"
    ubicacion: "archivo:línea o endpoint"
contexto_faltante:
  - "qué información adicional se necesitaría para un diagnóstico completo"
analisis_preliminar: "hipótesis sobre la causa, marcada explícitamente como preliminar"
```

### Reglas de estructuración

1. **No interpretar más allá de los datos** — Si la información es insuficiente para un diagnóstico, decirlo
2. **Separar hechos de hipótesis** — Los datos del log son hechos; la causa probable es hipótesis
3. **Identificar contexto faltante** — Siempre listar qué información adicional ayudaría
4. **Preservar datos originales clave** — No resumir tanto que se pierdan los datos necesarios para debug

## Función 2 — Puntuación de confiabilidad de fuentes

### Escala de confiabilidad

Basada en los criterios definidos en `references/criterios-fuentes-confiables.md`:

| Nivel | Score | Tipo de fuente | Ejemplo |
|---|---|---|---|
| 🟢 Oficial | 5 | Documentación oficial del proveedor | learn.microsoft.com, selenium.dev |
| 🟢 Estándar | 4 | Estándares reconocidos de la industria | ISTQB syllabus, RFCs, IEEE |
| 🟡 Tercero reconocido | 3 | Docs de terceros con reputación | MDN, DigitalOcean tutorials, Martin Fowler |
| 🟡 Comunidad curada | 2 | Foros con votación/moderación | Stack Overflow (respuesta aceptada), GitHub issues oficiales |
| 🔴 Sin curación | 1 | Blogs personales, foros sin moderación | Posts de Medium sin verificar, foros random |
| 🔴 Sin fuente | 0 | Afirmación sin ninguna fuente identificable | Memoria del modelo, "es sabido que..." |

### Uso del script de scoring

El script `scripts/extract_and_score.py` automatiza la puntuación:

```bash
python scripts/extract_and_score.py --sources '["https://learn.microsoft.com/...", "https://stackoverflow.com/..."]'
```

Ver `scripts/extract_and_score.py` para detalles de implementación.

## Integración con el orquestador

Este skill **no entrega resultados al usuario**. Sus outputs van al orquestador-validador, que los usa para:

1. Verificar que las fuentes citadas en un draft tengan score >= 3 (o estén marcadas si son menores)
2. Estructurar información cruda antes de que un skill especializado la procese
3. Alimentar el checklist de validación con datos sobre la confiabilidad de las fuentes

## Reglas

1. **No responder directo al usuario** — Siempre pasar resultados al orquestador
2. **No inventar scores** — Usar la escala definida en `references/criterios-fuentes-confiables.md`
3. **No interpretar más allá de los datos** — Si la información es insuficiente, decirlo
4. **Preservar la trazabilidad** — Cada análisis debe indicar qué datos de entrada usó
