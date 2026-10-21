# Calibración de advertencias

Paso **E** del orquestador. No entrega un ⚠️ ni un dato “de producto” (columna, rol, estado, path, mensaje) sin **rebuscarlo** en la fuente.

Sirve para el fallo típico: el draft marca 8 huecos de swagger y **deja pasar** `LANG_CODE` o rol “QA” como si fueran verdad.

---

## Cuándo corre

Después de A–D, **antes** de la respuesta final. También si el usuario pega un paquete ya generado y pide calibrar.

---

## Qué se calibra (barrido, no solo lo ya marcado)

Recorrer el draft y extraer **afirmaciones atómicas** de estos tipos, aunque el draft las presente como hechas:

| Tipo | Ejemplo |
|---|---|
| Columna SQL | `LANG_CODE`, `SEND_DATE`, `APPROVAL_DATE = NULL` |
| Literal de estado | `En progreso`, `En proceso`, `Pagado`, `REJECTED` |
| Rol / permiso | `QA`, `Analista`, `Coordinador` |
| Path / host / método | `/api/GetCurrencyList`, SendgridEndpoints |
| Mensaje de UI | “se aprobó correctamente” |
| Campo de formulario mandatorio | Fecha de Venta, Valor faltante ≤ Total |
| Body JSON (nombre de campo) | `notifaction-type`, `acm-num` |

Un dato que no sea de esta lista (estilo Gherkin, estructura de folders) no entra al barrido.

---

## Procedimiento por afirmación

1. Escribir la afirmación en una línea: *“La tabla X tiene la columna Y”*.
2. Abrir **solo** el archivo que debería respaldarla (`base_conocimiento/…` o `references/…`).
3. Buscar el string exacto (o el sinónimo que el manual use).
4. Clasificar:

| Resultado | Criterio | Acción en la respuesta |
|---|---|---|
| **CONFIRMADO** | El string está y significa lo mismo | Quitar ⚠️; citar archivo + ancla (§ o frase) |
| **CORREGIDO** | Está, pero con otro valor | Reemplazar el dato; no dejar el inventado |
| **CONTRADICCIÓN** | Dos literales oficiales distintos | Mostrar ambos; el tester confirma en BD/UI; no elegir uno |
| **SIN RESPALDO** | No aparece tras la búsqueda | ⚠️ + archivo buscado + qué se buscó. **Eliminar** el dato del SQL/body/pasos si era un identificador (columna, path, rol) |

5. **Prohibido** confirmar de memoria. Si no se abrió el archivo en este paso, el resultado no vale.

---

## Reglas de corte

- Columna / path / rol **SIN RESPALDO** → no se usa en scripts ni requests. Se lista solo en el bloque de calibración.
- Inferencia útil (`APPROVAL_DATE` vacío al radicar) → puede quedar como hipótesis con ⚠️, no como `= NULL` en el esperado oficial.
- Contradicción documental (En progreso / En proceso) → el caso dice: *verificar el literal persistido*; no forzar uno.

---

## Salida obligatoria en la respuesta

```
## Calibración
| Afirmación | Fuente buscada | Resultado | Acción |
|---|---|---|---|
| … | manual-….md §… | CONFIRMADO \| CORREGIDO \| CONTRADICCIÓN \| SIN RESPALDO | … |
```

Sin esta tabla no se entrega un paquete de prueba de producto.

---

## Registro

Una línea en `logs/calibraciones.jsonl` por corrida:

```json
{
  "timestamp": "ISO-8601",
  "pregunta": "resumen",
  "items": [
    {
      "afirmacion": "AVR_CONTROL_NOTIFICATIONS.SEND_DATE existe",
      "fuente": "base_conocimiento/manual-aplicacion-avr.md",
      "busqueda": "SEND_DATE",
      "resultado": "SIN_RESPALDO",
      "accion": "eliminado del SELECT"
    }
  ]
}
```

---

## Caso ancla (VF)

Calibración que ya se aplicó al paquete `paquetes/vf-valores-faltantes/`:

| Afirmación | Resultado |
|---|---|
| Roles QA / Analista para radicar | SIN RESPALDO — no usar |
| Coordinador ≤ 3500 USD / Gerente > 3500 | CONFIRMADO — SR §7.2.4.2 |
| Fecha de Venta mandatoria | CONFIRMADO — faltaba en el primer draft |
| `LANG_CODE`, `SEND_DATE`, `NOTIF.REFUND_REQUEST` | SIN RESPALDO — fuera del SQL |
| En progreso vs En proceso | CONTRADICCIÓN — §7.2.4.4 vs §7.2.4.2.1 |
| Bodies NTC23/24 completos | CONFIRMADO — AVR §10.4.2–10.4.3 |
| Paths SendGrid / MissingValue / MissingModules | SIN RESPALDO — no inventar request |
| `APPROVAL_DATE = NULL` al radicar | SIN RESPALDO (inferencia) — no es esperado oficial |

## Caso ancla (ROR)

El manual ROR tiene copy-paste de SR/AVR. Calibrar siempre:

| Afirmación | Resultado |
|---|---|
| §1.1 / §9 hablan de Special Refund | CONTRADICCIÓN — Identificación + URL `orqrules` = ROR |
| Backend / Key Vault = “reembolsos especiales” | CONTRADICCIÓN — Alcance = reglas de orquestación |
| SP auditoría `[rfd].[AVR_SP_USER_DATA_QUERY]` en ROR | CONTRADICCIÓN de nombre — usar el literal; no inventar `ROR_SP_*` |
| `master.MST_EMD` vs `Master.MST.EMD` | CONTRADICCIÓN — verificar objeto en BD |
| Paths REST ListHomologation / EmdGetRfisc | SIN RESPALDO — solo swagger + nombre de API |
| Front ROR expuesto a internet | SIN RESPALDO — el manual dice que **no** |
