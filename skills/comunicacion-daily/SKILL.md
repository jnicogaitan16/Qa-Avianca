---
name: comunicacion-daily
description: >
  Skill comunicativa para la daily de QA. Se activa cuando el usuario pide un speech, pitch o resumen hablado de lo trabajado ayer, con bloqueos y prioridades de hoy. Lee el resumen que pega el usuario y los casos en test-cases/, y redacta un speech en primera persona. No responde directo: el texto hablado pasa por orquestador-validador y es lo único que se entrega.
---

# Comunicación daily

## Propósito

Convertir el trabajo del día anterior en un speech para decirlo en la daily. El speech sale de dos insumos y de nada más:

1. El resumen que escribe el usuario (qué hizo, bloqueos, a quién hay que avisar).
2. Los casos de `test-cases/PBI-*/casos-de-prueba.md` que correspondan a ese trabajo.

## Cuándo se activa

- "Ármame el speech de la daily"
- "Comenta lo de ayer"
- Un resumen de PBI, casos, bloqueos o pendientes para decirlo en la reunión

## Cómo se lee

1. Tomar el resumen del usuario tal cual. No completar huecos con suposiciones.
2. Abrir solo los markdown de `test-cases/` de los PBI que el resumen nombra. Si el resumen no nombra un PBI, no se menciona.
3. Si adjunta una captura de log, usar únicamente el hallazgo que se ve: qué campo llega, a qué componente, y si el campo sigue o se pierde en el paso siguiente. No copiar nombres, documentos, cuentas ni otros datos de persona que aparezcan en el log.
4. Separar en tres bloques internos, sin mostrarlos como títulos en la respuesta:
   - Hecho: casos diseñados y lo que sí se pudo validar.
   - Bloqueos: accesos, dominios, dependencias de otra persona.
   - Hoy: el aviso pendiente y el siguiente paso para destrabar.

## Cómo se habla

- Primera persona, en voz alta, como si ya estuviera en la daily.
- Un solo bloque de prosa. Sin viñetas, sin negrillas, sin tablas y sin marcas `**`.
- Frases cortas y encadenadas. Cabe en menos de un minuto.
- Nombrar el PBI, el campo y el pod solo cuando salen del resumen, del caso o de la captura.
- Lo que sigue pendiente se dice como pendiente. No se presenta como prueba cerrada.
- No se inventa código HTTP, texto de error ni dueño del defecto si el insumo no lo trae.

## Salida

El orquestador entrega solo el speech. No agrega la tabla de calibración ni una lista de fuentes al texto que la persona va a leer en voz alta. Si un dato no está en el resumen, en el caso o en la captura, no entra al speech.
