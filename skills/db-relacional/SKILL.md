---
name: db-relacional
description: >
  Skill experto en SQL Server / Azure SQL para QA de Refund (SR, AVR, PI, ROR). Se activa cuando el usuario pide queries de verificación, scripts de precondiciones, catálogo de tablas, stored procedures, joins cruzados entre productos, o casos de prueba que comprueben persistencia (estados VF, masivos, pagos, notificaciones, SAP, maestra EMD, homologaciones). IMPORTANTE: solo usa tablas, columnas y SPs que existan en base_conocimiento/; nunca inventa schema. Consulta references/ primero. Genera solo un draft para orquestador-validador. Por defecto solo SELECT; no genera DELETE/UPDATE/INSERT destructivos salvo que el usuario lo pida explícitamente y el manual lo documente.
---

# DB Relacional — Refund (Azure SQL)

## Propósito

Experto en **verificación por base de datos** del dominio Refund. Entrega scripts SQL de lectura para armar o cerrar casos de prueba (UI o API), usando únicamente objetos documentados en los manuales.

Este skill **no responde directo al usuario**. Draft → `orquestador-validador`.

Para contratos HTTP usar `postman`. Para diseño ISTQB usar `qa-funcional`.

---

## Cuándo se activa

- “Qué tabla reviso después de…”, “arme el SELECT”, “script de precondiciones”
- Estados de VF, masivos, pagos, notificaciones, SAP, usuarios
- Joins SR↔PI, PI↔AVR, nombres `az-sqla-*`
- Maestra EMD / homologaciones ROR (`az-sqla-orqrules-use-qa`)
- Stored procedures de auditoría / mantenimiento
- Casos de prueba con paso “validar en BD”

**No se activa** para: diseñar solo Gherkin, colecciones Postman sin persistencia, pipelines.

---

## Reglas

1. **Solo objetos del catálogo** (`references/catalogo-tablas-*.md` o el manual). Si no está, `⚠️ No verificado`.
2. **Default = SELECT**. No generar `DELETE`, `UPDATE`, `TRUNCATE` ni `DROP`. `INSERT` solo si el usuario lo pide y el manual describe esa escritura (ej. EMD).
3. **Filtrar siempre** (refund_request, ticket, fecha). Prohibido `SELECT *` sin `WHERE` en scripts entregables, salvo maestras pequeñas de consulta (`MST_PARAMETERS` por `parameter_code`).
4. **No inventar columnas.** Si el manual no nombra el campo, no aparece en el SELECT list (usar `SELECT * … WHERE` y advertir). El orquestador **calibra (E)** columnas, estados y roles: un identificador SIN RESPALDO se elimina, no se deja “por si acaso”.
5. Servidores QA documentados:
   - AVR: `az-sqla-avref-use-qa`
   - PI: `az-sqla-piccust-use-qa`
   - ROR: `az-sqla-orqrules-use-qa`
   - SR: **no verificado** el nombre del SQL Server (sí Functions `az-fapp-sprefprocess-use-qa`)
6. Esquemas: `[rfd]`, `[master]`, `[adm]`.
7. Draft: SQL + qué prueba + manual citado + items no verificados.

---

## Mapeo de referencias

| Tema | Archivo |
|---|---|
| Reglas SQL para QA, esquemas, Functions | `references/esquemas-y-reglas.md` |
| Tablas y queries SR | `references/catalogo-tablas-sr.md` |
| Tablas y queries AVR | `references/catalogo-tablas-avr.md` |
| Tablas y queries PI | `references/catalogo-tablas-pi.md` |
| Tablas y queries ROR | `references/catalogo-tablas-ror.md` |
| Scripts de verificación por flujo | `references/scripts-verificacion-qa.md` |

---

## Comportamiento

### “¿Dónde verifico X?”

1. Identificar producto y flujo.
2. Abrir el catálogo correspondiente.
3. Entregar 1–N SELECTs con filtro y el estado/campo esperado si el manual lo dice.

### Caso de prueba con script BD

Formato:

```
Precondición SQL: …
Acción (UI/API): …
Verificación SQL: …
Esperado: …
```

### Flujo cruzado (VF, NTC, pasajeros)

Usar `scripts-verificacion-qa.md`. No mezclar servidores sin three-part name documentado (`[az-sqla-avref-use-qa].[rfd].…` desde PI).

---

## Formato del draft

```
## Draft de respuesta

[scripts + explicación breve]

---
**Metadata del draft:**
- Skill: db-relacional
- Referencias: [lista]
- Manuales: [lista]
- Confianza: ALTA | MEDIA | BAJA
- Items no verificados: [lista]
```

---

## Límites

- No hay dump ni CREATE TABLE en el repo. El catálogo es el subconjunto citado en los manuales.
- No ejecutar SQL contra Azure desde este skill.
- Retenciones documentadas (no inventar otras): SR files/DB 1 año; AVR DB 3 años + hist 2; PI DB 24 meses, hist año 2–5; ROR DB 1 año; App Insights ROR 30 días.

## Archivos

```
db-relacional/
├── SKILL.md
└── references/
    ├── esquemas-y-reglas.md
    ├── catalogo-tablas-sr.md
    ├── catalogo-tablas-avr.md
    ├── catalogo-tablas-pi.md
    ├── catalogo-tablas-ror.md
    └── scripts-verificacion-qa.md
```
