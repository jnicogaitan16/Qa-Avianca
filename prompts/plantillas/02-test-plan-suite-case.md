# 02 — Test Plan, Suite y Case (Azure DevOps)

**Cuándo:** tarea **QA - Análisis y Diseño Caso Prueba**.  
**Quién:** QA.  
**Salida:** work items listos en Design → Ready.

**Fuentes:** `lineamientos-qa.md` (Documentación Test Plan / Suite / Case).  
**Omitido:** campos Azure no listados ahí (Found In, Priority nativo, etc.).

---

```markdown
# Test Plan
Nombre: Test Plan [SR | AVR | PI | ROR]
Area Path: (tablero)
Iteration Path: (tablero + sprint)

# Test Suites (una por release o sprint)
[Aplicación] / [Release o Sprint]
  ├── QA
  ├── UAT PRE
  └── UAT POST
      └── carpeta PBI-XXXXX
          # Si el PBI no sale en este sprint: mover la carpeta o el caso al siguiente

# Test Case (repetir por escenario)
Nombre: PBI-XXXXX #TC Título del escenario
Asignado a:
Add tag / aplicación: SR | AVR | PI | ROR
State: Design  →  Ready (al terminar el diseño)  →  Closed (al cerrar UAT)
Area: (tablero)
Iteration: (tablero + sprint de ejecución)
Related work: PBI-XXXXX
Steps: (redactar en 03-ejecucion-qa.md y pegar aquí)
Evidencias: prints con fecha y hora de la ejecución
```

---

**Reglas**

- Un Case = un escenario de la ficha 01. No un Case “probar todo SR”.
- Related work al PBI es obligatorio (trazabilidad previa a producción).
- Tag de aplicación del listado del proyecto; no inventar el picklist.

**Siguiente ficha:** `03-ejecucion-qa.md`
