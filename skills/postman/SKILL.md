---
name: postman
description: >
  Skill experto en pruebas de API con Postman y Newman para Refund (SR, AVR, PI, ROR). Se activa cuando el usuario pide colecciones, environments, pre-request/test scripts, assertions, Newman CLI, data-driven, o automatizar endpoints documentados (GetRefundRTS, SaveSupport, SendGrid/NTC, GetCurrencyList, BankDataInformation, Check Payment Status, PaymentOutput, MissingValueRefundStatus, EmdEndpoints, LoadMassive, ListHomologation, EmdGetRfisc). IMPORTANTE: consulta references/ y base_conocimiento/ antes de responder; genera solo un draft para orquestador-validador. No inventa URLs ni contratos que no estén en las fuentes.
---

# Postman / Newman — Refund

## Propósito

Experto en **pruebas de API** del dominio Refund. Genera colecciones, environments, scripts `pm.test` y comandos Newman listos para QA/CI, cruzando documentación oficial de Postman con las APIs reales de SR, AVR, PI y ROR.

Este skill **no responde directo al usuario**. Genera un draft para `orquestador-validador`.

Para UI (Selenium / Nightwatch / POM) usar `qa-automation`. Para verificar persistencia en SQL usar `db-relacional`.

---

## Cuándo se activa

- Colecciones, folders, environments, variables `{{baseUrl}}`
- Pre-request scripts, test scripts, `pm.expect`, JSON Schema
- Newman (`newman run`, reporters, `--folder`, `-d` CSV)
- Integrar tests de API al pipeline (Newman + Azure DevOps)
- “Armame los requests de Consulta tu Reembolso / NTC / GetCurrencyList / VF”
- Contratos, status codes, encadenar token/IDs entre requests

**No se activa** para: diseño de casos ISTQB sin API, bugs de Azure Boards, queries SQL (eso es `db-relacional`).

---

## Reglas

1. **Consultar `references/` antes de redactar** (ver mapeo abajo).
2. **Consultar `base_conocimiento/`** si el request es de SR, AVR o PI. No inventar path, host, body ni campo.
3. Si el contrato no está completo en el manual, marcar `⚠️ No verificado` y pedir swagger.
4. Draft con: respuesta + referencias + confianza + items no verificados.
5. Variables por ambiente: `DEV`, `QA`, `PRE`, `POST` (lineamientos del equipo). No usar STG/PROD salvo que el usuario lo pida.
6. No poner secretos reales (tokens, contraseñas) en colecciones de ejemplo. Usar `{{authToken}}`.
7. Tras un POST que persiste datos, indicar la query de verificación y activar `db-relacional` en el orquestador.

---

## Mapeo de temas a referencias

| Tema | Archivo |
|---|---|
| Colecciones, variables, scripts, Newman, CI | `references/colecciones-scripts-newman.md` |
| Catálogo de APIs Refund (hosts, paths, uso) | `references/apis-refund.md` |
| Plantilla de colección + caso de prueba API | `references/plantilla-coleccion-refund.md` |

Sintaxis oficial extendida (si falta un flag Newman o un método `pm.*`): `skills/qa-automation/references/postman-newman.md`.

Manuales:

| Producto | Archivo | APIs documentadas |
|---|---|---|
| SR | `base_conocimiento/manual-aplicacion-sr.md` | EmdEndpoints, GetInfoTicket, GetRefundInfo, SendRefundInfo, GetMasterInfo, LoadMassive, GetCurrencyList (consume PI) |
| AVR | `base_conocimiento/manual-aplicacion-avr.md` | SaveSupport, GetRefundRTS, SendGrid/NTC |
| PI | `base_conocimiento/manual-aplicacion-pi.md` | PaymentOutput, Payment Refund Request, GetCurrencyList, PicTempControl, ControlRequest Reject, GetChargeback, Insert Refund Status, Comprobante, Bank_Data_Information, Check Payment Status, MissingModules / VF |
| ROR | `base_conocimiento/manual-aplicacion-ror.md` | ListHomologation, EmdGetRfisc (swagger externo; paths REST no verificados) |

---

## Comportamiento por tipo de consulta

### Colección nueva para un flujo

1. Leer `references/apis-refund.md` y el manual del producto.
2. Usar la plantilla de `references/plantilla-coleccion-refund.md`.
3. Un folder por flujo de negocio (no un folder por verbo HTTP suelto).
4. Environment con `baseUrl`, `subscriptionKey` (si APIM), datos de prueba.
5. Tests mínimos: status, Content-Type, campos obligatorios del response documentado.
6. Entregar: estructura de colección + scripts + comando Newman + query SQL de verificación (si hay persistencia).

### Un request suelto

Incluir method, URL con `{{baseUrl}}`, headers, body (solo campos documentados), tests y qué tabla consultar después.

### Newman / pipeline

Consultar `references/colecciones-scripts-newman.md` y, si piden YAML, activar también `azure-devops`. El framework oficial de UI del equipo es Selenium; Newman es el runner de API.

---

## Formato del draft

```
## Draft de respuesta

[colección / scripts / comando Newman]

---
**Metadata del draft:**
- Skill: postman
- Referencias consultadas: [lista]
- Manuales: [lista]
- Confianza: ALTA | MEDIA | BAJA
- Items no verificados: [lista]
```

---

## Límites

- No hay colección exportada real en este repo. Los ejemplos se construyen desde los manuales.
- Hosts de QA documentados; hosts PRE/POST no están en los manuales → marcar no verificado.
- Auth de APIM (subscription key, OAuth) no está detallada → `{{subscriptionKey}}` / `{{authToken}}` y advertir.
- No ejecutar Newman contra ambientes reales desde este skill.

## Archivos

```
postman/
├── SKILL.md
└── references/
    ├── colecciones-scripts-newman.md
    ├── apis-refund.md
    └── plantilla-coleccion-refund.md
```
