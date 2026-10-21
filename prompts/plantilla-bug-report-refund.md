# Prompt: ¿Cuál es la mejor manera de reportar un bug en Refund?

Fichas hermanas (criterios, Test Plan, ejecución, UAT): `prompts/plantillas/README.md`.

> Usa este prompt en una sesión de Claude Code apuntando a `/QA/`. Las skills y la base de conocimiento harán el trabajo.

---

## Prompt

```
Necesito que me indiques cuál es la mejor manera de reportar un bug en el proyecto Refund (SR, AVR, PI o ROR), considerando tanto las buenas prácticas de la industria como los lineamientos internos del equipo.

Tu respuesta debe:

1. CONSULTAR las siguientes fuentes antes de responder:
   - skills/qa-funcional/references/plantillas-bug-report.md (template estándar + modelo F-S-V)
   - base_conocimiento/lineamientos-qa.md (lineamientos del equipo en Azure DevOps: naming, campos obligatorios, flujo del bug, Activity, Severity, evidencias)
   - skills/azure-devops/references/boards-y-work-items.md (campos de work items en Azure DevOps)

2. COMBINAR ambas fuentes en una plantilla unificada que incluya:
   a) Los campos obligatorios del equipo en Azure DevOps:
      - Título con formato "PBI-XXXXX Breve descripción"
      - Activity (Development / Deployment / Requirements / Testing)
      - Environment (DEV, QA, PRE, POST)
      - Area (tablero)
      - Iteration (sprint)
      - Application Name (SR, AVR, PI, ROR)
      - Severity (1-Critical, 2-High, 3-Medium, 4-Low)
      - Relacionar al PBI correspondiente
   b) Los campos de calidad del template F-S-V:
      - Prioridad F-S-V calculada (Frecuencia + Severidad + Visibilidad)
      - Resumen / Dónde sucede / Resultado esperado / Resultado actual / Antecedentes
      - Evidencia con checklist (screenshots con fecha/hora, logs, network trace)
   c) Las reglas del equipo:
      - El bug se crea INMEDIATAMENTE se encuentre el defecto
      - Debe moverse por TODOS los estados linealmente (no saltar casillas)
      - Enviar correo al equipo de desarrollo con los bugs encontrados
      - Solicitar explicación al dev que lo resolvió antes de cerrar
      - Si no es bug: cambiar Activity a quien corresponda + comentario justificando
      - Separar BUGs de INC (incidentes como work items separados)

3. ENTREGAR:
   - Una plantilla consolidada lista para copiar/pegar en Azure DevOps
   - Un ejemplo completo aplicado al proyecto Refund (usando una aplicación real: SR, AVR, PI o ROR)
   - El cálculo F-S-V del ejemplo

4. VALIDAR contra el orquestador:
   - Cada campo debe tener respaldo en lineamientos-qa.md O en plantillas-bug-report.md
   - Si hay contradicción entre ambas fuentes, priorizar lineamientos-qa.md (es la convención real del equipo)
   - Marcar como "⚠️ No verificado" cualquier campo que no esté en ninguna fuente
```

---

## Flujo esperado

```
qa-funcional → draft (template F-S-V + buenas prácticas ISTQB/IEEE)
azure-devops → draft (campos de work items en Azure DevOps)
base_conocimiento/lineamientos-qa.md → contexto del equipo (naming, Activity, flujo de estados)
    ↓
orquestador-validador → agrega, valida cruzado, entrega respuesta unificada
```
