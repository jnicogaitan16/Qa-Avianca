# Checklist de Validación — Orquestador-Validador

Este checklist se ejecuta **obligatoriamente** sobre cada draft de respuesta antes de entregarlo al usuario. No hay excepciones.

## Tabla de contenidos

1. [Prerequisitos](#prerequisitos)
2. [Verificación A — Respaldo documental](#verificación-a--respaldo-documental)
3. [Verificación B — Contradicciones](#verificación-b--contradicciones)
4. [Verificación C — Detección de alucinación](#verificación-c--detección-de-alucinación)
5. [Verificación D — Distinción verificado/no-verificado](#verificación-d--distinción-verificadono-verificado)
6. [Verificación E — Calibración](#verificación-e--calibración)
7. [Matriz de decisión](#matriz-de-decisión)
8. [Plantilla de registro](#plantilla-de-registro)

---

## Prerequisitos

Antes de ejecutar el checklist, confirmar que se tienen los 3 elementos:

- [ ] Pregunta original del usuario
- [ ] Draft de respuesta del skill especializado
- [ ] Lista de `references/*.md` que el skill consultó

Si falta alguno, devolver al skill de origen solicitando la información completa.

---

## Verificación A — Respaldo documental

**Pregunta clave:** ¿Cada afirmación técnica del draft tiene respaldo en un `references/*.md` real?

### Procedimiento

1. Identificar cada afirmación técnica en el draft (comandos, configuraciones, comportamientos, parámetros, endpoints, valores por defecto)
2. Para cada afirmación, buscar el respaldo en el `references/*.md` citado
3. Clasificar cada afirmación:

| Clasificación | Criterio | Acción |
|---|---|---|
| ✅ Verificada | Aparece en `references/` con el mismo significado | Ninguna |
| ⚠️ Parcialmente verificada | El concepto aparece pero el detalle específico no | Marcar en la respuesta |
| ❌ Sin respaldo | No aparece en ningún `references/` | Marcar o corregir |

### Señales de alerta

- Afirmaciones sobre valores por defecto que no están en la documentación
- Nombres de parámetros o flags muy específicos sin fuente
- Secuencias de pasos que no coinciden con la documentación
- Referencias a versiones específicas de herramientas

---

## Verificación B — Contradicciones

**Pregunta clave:** ¿Hay contradicciones entre el draft y la fuente?

### Procedimiento

1. Tomar cada afirmación verificada en el paso A
2. Comparar textualmente contra la fuente:
   - ¿Los nombres de campos/parámetros coinciden exactamente?
   - ¿El comportamiento descrito es el mismo?
   - ¿Los valores posibles/rangos coinciden?
   - ¿El orden de los pasos es correcto?
3. Clasificar:

| Clasificación | Criterio | Acción |
|---|---|---|
| ✅ Consistente | Draft y fuente dicen lo mismo | Ninguna |
| ❌ Contradictorio | Draft dice algo diferente a la fuente | **Corregir el draft** usando la fuente como verdad |

### Contradicciones comunes

- Parámetros que cambiaron de nombre entre versiones
- Comportamientos deprecados que el draft presenta como vigentes
- Sintaxis que difiere levemente (guiones, mayúsculas, formato)

---

## Verificación C — Detección de alucinación

**Pregunta clave:** ¿Hay afirmaciones que suenen a relleno o invención?

### Indicadores de posible alucinación

Revisar si el draft contiene:

- [ ] **Fechas específicas** de lanzamiento/deprecación no verificadas en fuentes
- [ ] **Números de versión** (ej. "desde la versión 7.2") no confirmados
- [ ] **Nombres de parámetros/flags/endpoints** que no aparecen en `references/`
- [ ] **Valores numéricos específicos** (ej. "timeout de 30 segundos por defecto") sin fuente
- [ ] **Comportamientos "por defecto"** que no están documentados
- [ ] **URLs o paths** inventados o no verificados
- [ ] **Citas textuales** que no corresponden a ninguna fuente real
- [ ] **Afirmaciones sobre limitaciones** (ej. "máximo 100 items") sin documentación

### Procedimiento ante sospecha

1. Buscar el dato específico en `references/`
2. Si no está: buscar si otro `references/` del mismo skill lo cubre
3. Si no está en ningún `references/`: marcar como **no verificado**

---

## Verificación D — Distinción verificado/no-verificado

**Pregunta clave:** ¿La respuesta distingue claramente lo verificado de lo que no?

### Procedimiento

1. Revisar si quedan afirmaciones marcadas como ⚠️ o ❌ tras los pasos A, B y C
2. Verificar que cada una tenga una marca visible en el draft final:
   - Formato requerido: `⚠️ No verificado con certeza — se recomienda confirmar en [fuente específica]`
3. Verificar que las afirmaciones ✅ no estén marcadas innecesariamente (evitar false alarms)

---

## Verificación E — Calibración

**Pregunta clave:** ¿Cada ⚠️ y cada identificador de producto se reabrió en el manual?

Procedimiento completo: `calibracion-advertencias.md`.

1. Extraer afirmaciones atómicas (columna, rol, estado, path, mensaje, campo mandatorio)
2. Buscar el string en la fuente citada
3. CONFIRMADO / CORREGIDO / CONTRADICCIÓN / SIN RESPALDO
4. Identificador SIN RESPALDO: **borrarlo** del entregable
5. Incluir tabla Calibración en la respuesta
6. Registrar `logs/calibraciones.jsonl`

| Resultado E | Acción |
|---|---|
| ✅ Todo rebuscado y limpio | Seguir |
| ❌ Dato inventado aún en SQL/body | **RECHAZADO** → limpiar |
| ❌ Sin tabla Calibración en paquete de producto | **RETENER** |

---

## Matriz de decisión

| A | B | C | D | E | Resultado |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | **APROBADO** |
| ⚠️ | ✅ | ✅ | ✅ | ✅ | **APROBADO CON ADVERTENCIAS** |
| ❌ | — | — | — | — | **RECHAZADO** → corregir o marcar |
| — | ❌ | — | — | — | **RECHAZADO** → corregir con fuente |
| — | — | ❌ | — | — | **RECHAZADO** → eliminar o marcar |
| — | — | — | ❌ | — | **RETENER** → agregar marcas |
| — | — | — | — | ❌ | **RECHAZADO** → recalibrar y quitar inventos |

---

## Plantilla de registro

Cada ejecución del checklist genera una entrada en `logs/validaciones.jsonl`:

```json
{
  "timestamp": "ISO-8601",
  "pregunta": "resumen breve de la pregunta",
  "skill_origen": "azure-devops|qa-funcional|qa-automation|analizador-informacion",
  "verificaciones": {
    "A_respaldo_documental": {
      "resultado": "PASA|FALLA",
      "detalles": "lista de afirmaciones sin respaldo, si las hay"
    },
    "B_contradicciones": {
      "resultado": "PASA|FALLA",
      "detalles": "contradicciones encontradas, si las hay"
    },
    "C_alucinacion": {
      "resultado": "PASA|FALLA",
      "detalles": "afirmaciones sospechosas, si las hay"
    },
    "D_distincion": {
      "resultado": "PASA|FALLA",
      "detalles": "marcas faltantes, si las hay"
    },
    "E_calibracion": {
      "resultado": "PASA|FALLA",
      "detalles": "items SIN_RESPALDO aún en el entregable, si los hay"
    }
  },
  "fuentes_consultadas": ["ruta/a/references/archivo.md"],
  "resultado_final": "APROBADO|APROBADO_CON_ADVERTENCIAS|RECHAZADO_Y_CORREGIDO",
  "notas": "observaciones adicionales"
}
```

---

## Fuentes

Este checklist es un diseño interno del proyecto qa-devops-suite, no está basado en una fuente externa. Su estructura se inspira en principios de verificación de calidad de información y revisión de pares.

Fecha de creación: 2026-09-22
