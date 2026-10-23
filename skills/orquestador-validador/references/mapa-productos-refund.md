# Mapa de productos Refund (lectura obligatoria del orquestador)

Hay **cuatro** productos en `base_conocimiento/`. SR, AVR y PI forman la cadena transaccional. **ROR no radica ni paga**: parametriza reglas para la orquestación (APIM / capa media). No fusionar responsabilidades.

```
SR (ingresa caso especial) → Mozart / APIM → AVR (sigue / timeout / NTC) → PI (paga)
VF: SR aprueba → PI VF → PI notifica SR → AVR NTC23/24
ROR: maestras / homologaciones / EMD → APIM → orquestadores (SR, AVR, PI, Mozart)
```

| | SR | AVR | PI | ROR |
|---|---|---|---|---|
| Nombre | Special Refund | AV Refund | Payment Integrator (PIC) | Refund Orchestration Rules |
| Momento | Crear caso especial | Seguimiento, consulta, purge 30 min, mails | Pago ya aprobado | Reglas, parámetros y homologaciones para orquestar |
| Front QA | specialrefundqa.avtest.ink | azwappavrefsftuseqa…/auth | azwapppiccustfrontuseqa…/auth | azwappsorqrulesfrontuseqa…/auth |
| Front a internet | Sí (documentado) | Sí (documentado) | Sí (documentado) | **No** (manual: no expuesto a internet) |
| SQL QA | ⚠️ no verificado | az-sqla-avref-use-qa | az-sqla-piccust-use-qa | az-sqla-orqrules-use-qa |
| Swagger externo QA | azwappsprefbknduseqa…/externalservices/swagger | azwappavrefsextsuseqa…/Swagger | azwapppiccustextsuseqa…/Swagger | azwappsorqrulesextsuseqa…/Swagger |
| App Insights | 90 días | 90 días | 90 días | **30 días** |
| Retención DB | 1 año | 3 años (+ hist 2) | 24 meses | 1 año |

## Ruteo de skills

| Pregunta | Skills |
|---|---|
| Qué hace cada producto / diferencia | Este mapa + manuales |
| Casos ISTQB / Gherkin / bug F-S-V | `qa-funcional` + `prompts/plantillas/` |
| Bug en Azure, campos, estados | `qa-funcional` + `azure-devops` + `lineamientos-qa.md` |
| Selenium / Nightwatch / POM | `qa-automation` |
| Colección, Newman, endpoint | `postman` |
| SELECT, tablas, estados en BD | `db-relacional` |
| Pipeline YAML + Newman | `postman` + `azure-devops` |
| Flujo VF extremo a extremo | `qa-funcional` + `postman` + `db-relacional` + manuales SR y PI |
| Maestra EMD / ListHomologation / EmdGetRfisc | `postman` + `db-relacional` + manual ROR |
| Inactivación de usuario ROR | `db-relacional` + manual ROR (`ROR_DEACTIVITY_USER`) |
| Log de capa media, campos, arrays, saltos request/response | `validador-logs-capa-media` + el PBI en `test-cases/` si lo nombran |

## Contradicciones conocidas

- SR §5 copia el propósito de AVR. Verdad de SR = Identificación/Alcance (canal de especiales, sin lógica de negocio de reembolso).
- ROR §1.1 y §9 dicen “Special Refund”; Identificación, URL (`orqrules`) y SQL (`az-sqla-orqrules-use-qa`) son ROR. Calibración = CONTRADICCIÓN de copy-paste; no tratar ROR como SR.
- Backend y Key Vault de ROR hablan de “reembolsos especiales”. Verdad de ROR = Identificación/Alcance (reglas de orquestación).
- ROR nombra el SP de auditoría `[rfd].[AVR_SP_USER_DATA_QUERY]` (prefijo AVR). Calibración = CONTRADICCIÓN; usar el nombre literal del manual ROR y no inventar `ROR_SP_*`.
- Tabla EMD: el relato dice `master.MST_EMD`; una nota escribe `Master.MST.EMD`. Calibración = CONTRADICCIÓN; verificar el objeto real en BD.
- Severity Azure: 1 = Critical. F-S-V S: 4 = Crítica. No mezclar números.
- Título de bug: gana `PBI-XXXXX …` (`lineamientos-qa.md`).
- Ambiente: DEV/QA/PRE/POST (no STG/PROD).
- UI oficial del equipo: **Selenium**. Newman es runner de API, no reemplazo de UI.
- VF estados: el listado SR dice **En progreso**; el relato de envío a PI dice **En proceso**. Calibración = CONTRADICCIÓN; verificar literal en BD.
- VF roles documentados para aprobar: **Coordinador** (0–3500 USD) y **Gerente** (>3500). No hay rol “QA/Analista” en ese módulo.

## Fuentes

`manual-aplicacion-sr.md`, `manual-aplicacion-avr.md`, `manual-aplicacion-pi.md`, `manual-aplicacion-ror.md`, `lineamientos-qa.md`.
