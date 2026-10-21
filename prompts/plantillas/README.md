# Plantillas QA — Refund

Fichas para copiar. **Un momento = un archivo.** No sustituyen los manuales ni las skills.

## Cuándo usar cuál

| Momento | Archivo | Quién |
|---|---|---|
| Review con producto / Recibir PBI | `01-criterios-aceptacion.md` | QA + producto + Dev |
| Armar Test Plan / Suite / Case en Azure | `02-test-plan-suite-case.md` | QA |
| Ejecutar en QA (UI + evidencia + cierre BD/API) | `03-ejecucion-qa.md` | QA |
| Endpoint a probar o validar, por módulo | `../../docs/proyectos/apis-por-modulo.md` | QA lo llena |
| Entregar UAT a un usuario no técnico | `04-uat-cliente.md` | QA + usuario |
| Hallazgo de defecto | `../plantilla-bug-report-refund.md` | QA |

## Reglas de ingeniería

1. Solo campos que están en `lineamientos-qa.md`, Gherkin (`criterios-aceptacion.md`) o los manuales SR/AVR/PI/ROR.
2. Se prueba el **PBI**, no las cuatro aplicaciones.
3. UI (o la API si el PBI *es* esa API) dispara el caso. SQL y Newman **cierran**.
4. Si un dato no está en la fuente: se omite. No se rellena “por si acaso”.
5. Un ⚠️ en la ficha = calibración E: reabrir el manual o no usar el dato.

## Ruteo de skills

```
01 criterios     → qa-funcional
02 Azure         → qa-funcional + azure-devops
03 ejecución     → qa-funcional + db-relacional + postman (si hay contrato)
04 UAT           → qa-funcional + lineamientos-qa.md
bug              → qa-funcional + azure-devops
                 → orquestador-validador (siempre)
```

## Fuentes

- `base_conocimiento/lineamientos-qa.md` — Plan, Suite, Case, Bug, Impedimento, mail UAT, tareas QA
- `skills/qa-funcional/references/criterios-aceptacion.md` — Given-When-Then
- `skills/qa-funcional/references/tecnicas-diseno-casos.md` — ISTQB (opcional en el caso)
- Manuales SR / AVR / PI / ROR — ítems de negocio del checklist UAT
