# 01 — Criterios de aceptación (review con producto)

**Cuándo:** refinamiento o tarea **QA - Recibir PBI**.  
**Quién:** QA + producto (+ Dev).  
**Salida:** acuerdo de qué se da por bueno. No es el Test Case de Azure.

**Fuentes:** `criterios-aceptacion.md` (verificables, específicos, comportamiento).  
**Omitido:** cómo se implementa, nombres de tablas, paths de API.

---

```markdown
# Criterios de aceptación — PBI-________

Fecha: ________    Tablero / Area: ________    Sprint: ________
Aplicación: [ ] SR    [ ] AVR    [ ] PI    [ ] ROR
Ambiente de la primera prueba: [ ] QA    [ ] PRE    [ ] POST

## Una frase de alcance
El usuario de negocio puede ________________________________.

## Fuera de alcance
Este PBI no incluye:
Productos que no se tocan: [ ] SR    [ ] AVR    [ ] PI    [ ] ROR

## Comportamiento (Given / When / Then)

Como [rol del manual: Coordinador / Gerente / Central / tesorería]
Quiero [acción]
Para [beneficio]

### Escenario 1 — camino feliz
Dado
Cuando
Entonces (se ve en pantalla o llega un correo)

### Escenario 2 — negativo o alternativo
Dado
Cuando
Entonces

## Listo para diseñar casos
- [ ] Cada Entonces es sí/no (no “rápido”, “claro”, “amigable”)
- [ ] Hay al menos un escenario que debe fallar o rechazarse
- [ ] Hay datos posibles en el ambiente marcado
- [ ] Si el alcance cambió: se cierra este PBI y se abre otro (no se crea Bug)
```

---

**Siguiente ficha:** `02-test-plan-suite-case.md`
