# QA DevOps Suite

Sistema de Skills para Claude especializado en QA e infraestructura Azure DevOps, con validación obligatoria contra documentación oficial y base de conocimiento del producto.

## Estructura

```
/QA/
├── CLAUDE.md                              # Instrucciones maestras del proyecto
├── base_conocimiento/                     # Conocimiento del producto y equipo (manual)
│   ├── lineamientos-qa.md                 # Lineamientos QA del equipo
│   ├── manual-aplicacion-sr.md            # Manual Special Refund
│   ├── manual-aplicacion-avr.md           # Manual AV Refund
│   ├── manual-aplicacion-pi.md            # Manual Payment Integrator
│   └── manual-aplicacion-ror.md           # Manual Refund Orchestration Rules
├── skills/                                # Skills especializados
│   ├── azure-devops/                      # Boards, Pipelines, Repos, REST API
│   ├── qa-funcional/                      # ISTQB, bug reports, Gherkin
│   ├── qa-automation/                     # Selenium, Nightwatch, POM (UI)
│   ├── postman/                           # Colecciones, Newman, APIs Refund
│   ├── db-relacional/                     # SQL de verificación SR/AVR/PI/ROR
│   ├── analizador-informacion/            # Estructurar info + scoring fuentes
│   └── orquestador-validador/             # Gate A–D + calibración E
├── docs/
│   └── manual-general.md                  # Digest de ingreso QA (proceso + 4 apps)
├── prompts/                               # Plantillas de trabajo QA
│   ├── plantilla-bug-report-refund.md
│   └── plantillas/                        # CA, Test Plan, ejecución, UAT
├── paquetes/                              # Entregables de prueba calibrados
│   └── vf-valores-faltantes/              # Gherkin + SQL + Postman VF
└── logs/                                  # validaciones.jsonl + calibraciones.jsonl
```

## Flujo

```
Usuario → Skills (drafts) → Orquestador (A–D + calibración E) → Respuesta
                    ↑                         ↑
             references/              base_conocimiento/
```
