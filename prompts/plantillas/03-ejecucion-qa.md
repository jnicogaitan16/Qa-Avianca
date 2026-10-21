# 03 — Ejecución en QA

**Cuándo:** **QA - Preparación de data** y **QA - Ejecución Caso Prueba**.  
**Quién:** QA.  
**Salida:** Pass/Fail + evidencia. Fail → Bug el mismo día.

**Fuentes:** lineamientos (Steps, prints con fecha/hora); ISTQB (técnica opcional); skills `db-relacional` y `postman` (cierre).  
**Omitido:** columnas, paths o mensajes que no estén en el manual.

---

```markdown
# PBI-XXXXX #TC__ — ________________________________
Aplicación: SR / AVR / PI / ROR         Ambiente: QA
Técnica ISTQB (si aplica): [ ] Equivalencia  [ ] Límite  [ ] Decisión  [ ] Estados

## Precondiciones
1.
2. Datos: solicitud / tiquete / PNR / rol (Coordinador | Gerente | el que el PBI nombre)

## Pasos — disparador (UI, o API solo si el PBI es esa API)
1.
2.
3.

## Resultado esperado (pantalla, mensaje citado, correo)
-

## Cierre de verificación (no hace el negocio)
- [ ] No aplica
- [ ] BD: SELECT del catálogo `db-relacional` (filtro por el dato de la prueba). Esperado = literal del manual.
- [ ] API: request de `postman` solo con el endpoint escrito en `docs/proyectos/apis-por-modulo.md` para el módulo del PBI. Si la fila está vacía, no se inventa el path.
- [ ] No usé identificadores ⚠️ (columna, path, rol no citado)

## Evidencia
- [ ] Capturas con fecha y hora visibles
- Resultado: [ ] Pass    [ ] Fail
- Fail → crear Bug YA (`PBI-XXXXX breve descripción`) y seguir `../plantilla-bug-report-refund.md`

## Si no se puede probar (ambiente, permisos, no es Dev)
PBI → estado Build + Impedimento `PBI-XXXXX breve descripción`
(máx. 5 días en Build en el sprint)
```

---

**Re-test (tarea QA - Re test Caso de Prueba)**

1. Pedir al Dev qué cambió (BD o UI).  
2. Repetir pasos + cierre.  
3. Evidencia del resultado (pase o no).  
4. El Bug recorre todas las casillas hasta Done.

**Siguiente ficha:** `04-uat-cliente.md`
