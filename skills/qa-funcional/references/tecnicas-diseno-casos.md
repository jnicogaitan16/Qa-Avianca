# Técnicas de Diseño de Casos de Prueba (ISTQB CTFL v4.0)

Referencia basada en el **ISTQB Certified Tester Foundation Level (CTFL) Syllabus v4.0**, publicado en 2023 por el International Software Testing Qualifications Board. Las técnicas aquí descritas corresponden al Capítulo 4 del syllabus: "Test Analysis and Design".

---

## Clasificación de técnicas

El ISTQB clasifica las técnicas de prueba en tres categorías:

| Categoría | Descripción |
|---|---|
| **Black-box** (caja negra) | Se basan en la especificación del componente/sistema, sin conocer la estructura interna |
| **White-box** (caja blanca) | Se basan en la estructura interna del código |
| **Basadas en experiencia** | Se apoyan en el conocimiento del tester |

Este documento cubre las **cuatro técnicas de caja negra** del nivel Foundation:

1. Partición de equivalencia
2. Análisis de valores límite
3. Tablas de decisión
4. Transición de estados

---

## 1. Partición de Equivalencia (Equivalence Partitioning)

### Definición

La partición de equivalencia divide los datos de entrada (y en algunos casos los datos de salida) en **particiones** o **clases de equivalencia**. El principio fundamental es que todos los valores dentro de una misma partición deben ser tratados de la misma manera por el sistema bajo prueba. Por lo tanto, si un caso de prueba con un valor de la partición detecta un defecto, se asume que cualquier otro valor de esa partición también lo detectaría.

### Principios clave

- Las particiones pueden ser **válidas** (el sistema debe aceptarlas) o **inválidas** (el sistema debe rechazarlas).
- Las particiones no deben solaparse y deben cubrir todo el dominio de entrada (ser exhaustivas en conjunto).
- Se selecciona **al menos un valor representativo** de cada partición.
- Las particiones inválidas deben probarse **individualmente** (una por caso de prueba), para evitar que un rechazo enmascare otro.

### Cobertura

- **Cobertura mínima**: al menos un valor de cada partición identificada.
- **Fórmula**: (N.o de particiones cubiertas / N.o total de particiones) x 100%

### Ejemplo práctico

**Requisito**: Un campo "Edad" acepta valores enteros entre 18 y 65 inclusive.

| Partición | Rango | Tipo | Valor representativo |
|---|---|---|---|
| P1 | < 18 (ej: -1, 0, 17) | Inválida | 10 |
| P2 | 18 a 65 | Válida | 30 |
| P3 | > 65 (ej: 66, 100) | Inválida | 70 |
| P4 | Entrada no numérica (ej: "abc") | Inválida | "xyz" |
| P5 | Campo vacío | Inválida | "" |

**Casos de prueba mínimos**: 5 (uno por partición)

- CP-01: Ingresar edad = 10 --> Resultado esperado: error de validación
- CP-02: Ingresar edad = 30 --> Resultado esperado: aceptado
- CP-03: Ingresar edad = 70 --> Resultado esperado: error de validación
- CP-04: Ingresar edad = "xyz" --> Resultado esperado: error de formato
- CP-05: Dejar campo vacío --> Resultado esperado: campo obligatorio

---

## 2. Análisis de Valores Límite (Boundary Value Analysis)

### Definición

Es una extensión de la partición de equivalencia que se enfoca en los **valores en los límites** (boundaries) de las particiones. Los defectos tienden a concentrarse en los bordes donde el comportamiento del sistema cambia. Esta técnica verifica que los límites estén implementados correctamente.

### Principios clave

- Se prueban los valores **exactamente en el límite** y los **inmediatamente adyacentes** a este.
- El ISTQB v4.0 distingue dos niveles de cobertura:
  - **Two-value BVA (2 valores)**: se prueban el valor límite y un valor adyacente fuera de la partición. Es el nivel mínimo.
  - **Three-value BVA (3 valores)**: se prueban el valor límite, el valor inmediatamente por debajo y el inmediatamente por encima. Proporciona mayor rigor.
- Aplica a datos **ordenados** (números, fechas, caracteres alfabéticos, etc.).

### Cobertura

- **Fórmula 2-value**: (N.o de valores límite cubiertos / N.o total de valores límite identificados) x 100%
- **Fórmula 3-value**: similar, pero con tres valores por límite.

### Ejemplo práctico

**Requisito**: El mismo campo "Edad" (18-65 inclusive).

**Límites identificados**: 18 (inferior) y 65 (superior).

#### Con Two-value BVA:

| Valor | Partición | Expectativa |
|---|---|---|
| 17 | Inválida (justo debajo del límite inferior) | Rechazado |
| 18 | Válida (límite inferior) | Aceptado |
| 65 | Válida (límite superior) | Aceptado |
| 66 | Inválida (justo encima del límite superior) | Rechazado |

**Casos de prueba**: 4

#### Con Three-value BVA:

| Valor | Partición | Expectativa |
|---|---|---|
| 17 | Inválida | Rechazado |
| 18 | Válida (límite inferior) | Aceptado |
| 19 | Válida (adyacente al límite inferior) | Aceptado |
| 64 | Válida (adyacente al límite superior) | Aceptado |
| 65 | Válida (límite superior) | Aceptado |
| 66 | Inválida | Rechazado |

**Casos de prueba**: 6

---

## 3. Tablas de Decisión (Decision Table Testing)

### Definición

Las tablas de decisión son una técnica para modelar **reglas de negocio complejas** donde múltiples condiciones (entradas) afectan el resultado (acciones/salidas). Son especialmente útiles cuando hay combinaciones de condiciones que producen comportamientos distintos.

### Estructura de una tabla de decisión

| Elemento | Descripción |
|---|---|
| **Condiciones** (filas superiores) | Variables de entrada que pueden ser verdaderas (V) o falsas (F) |
| **Acciones** (filas inferiores) | Resultados o comportamientos que se activan según la combinación de condiciones |
| **Reglas** (columnas) | Cada combinación única de condiciones con sus acciones asociadas |

### Principios clave

- Una tabla completa con N condiciones booleanas tiene **2^N reglas** posibles.
- Se pueden **simplificar** las tablas colapsando reglas donde una condición es irrelevante (se marca con "-" o "N/A").
- El ISTQB recomienda cubrir **al menos una vez cada regla** que no sea redundante o imposible.
- Cada columna (regla) corresponde a al menos un caso de prueba.

### Cobertura

- **Fórmula**: (N.o de reglas cubiertas por casos de prueba / N.o total de reglas factibles) x 100%

### Ejemplo práctico

**Requisito**: Un sistema de descuentos en e-commerce.
- Condición 1: Cliente es premium (V/F)
- Condición 2: Compra supera $100 (V/F)
- Condición 3: Tiene cupón vigente (V/F)
- Acciones posibles: descuento 20%, descuento 10%, descuento 5%, sin descuento, envío gratis

| | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|
| **C1: Premium** | V | V | V | V | F | F | F | F |
| **C2: Compra > $100** | V | V | F | F | V | V | F | F |
| **C3: Cupón vigente** | V | F | V | F | V | F | V | F |
| **A1: Descuento 20%** | X | | | | | | | |
| **A2: Descuento 10%** | | X | X | | | | | |
| **A3: Descuento 5%** | | | | X | X | | | |
| **A4: Sin descuento** | | | | | | | | X |
| **A5: Envío gratis** | X | X | | | X | | | |

**Simplificación posible**: Si R2 y R3 producen la misma acción (descuento 10%), se pueden colapsar indicando que C2/C3 es irrelevante cuando la otra está activa.

**Casos de prueba mínimos**: 8 (uno por regla), o menos si se simplifica.

---

## 4. Transición de Estados (State Transition Testing)

### Definición

Esta técnica modela el comportamiento de un sistema como una **máquina de estados finitos**. El sistema puede estar en un número finito de estados, y las transiciones entre estados se producen por eventos (entradas) bajo ciertas condiciones (guardas). Cada transición puede generar acciones (salidas).

### Componentes del modelo

| Componente | Descripción |
|---|---|
| **Estado** | Condición en la que el sistema permanece hasta recibir un evento |
| **Transición** | Cambio de un estado a otro, provocado por un evento |
| **Evento** | Estímulo que puede provocar una transición |
| **Guarda** (guard condition) | Condición booleana que debe cumplirse para que la transición ocurra |
| **Acción** | Comportamiento producido durante la transición (salida) |

### Representación

Se puede representar como:
- **Diagrama de transición de estados**: grafo con nodos (estados) y flechas (transiciones etiquetadas con evento[guarda]/acción).
- **Tabla de transición de estados**: matriz con estados en filas y eventos en columnas, indicando el estado destino.

### Niveles de cobertura

| Nivel | Descripción |
|---|---|
| **Cobertura de todos los estados** | Cada estado es visitado al menos una vez |
| **Cobertura de todas las transiciones válidas** (0-switch) | Cada transición válida se ejecuta al menos una vez. Este es el nivel mínimo recomendado por ISTQB |
| **Cobertura de pares de transiciones** (1-switch) | Cada secuencia de dos transiciones consecutivas se ejecuta al menos una vez |
| **Transiciones inválidas** | Verificar que eventos no esperados en un estado dado son rechazados correctamente |

### Ejemplo práctico

**Requisito**: Sistema de bloqueo de cuenta por intentos de login fallidos.

**Estados**:
- S1: Bloqueada
- S2: Primer intento disponible (estado inicial)
- S3: Un intento fallido
- S4: Dos intentos fallidos

**Diagrama conceptual**:

```
                 login correcto
          ┌──────────────────────────────────┐
          │                                  v
[S2: Inicio] --login incorrecto--> [S3: 1 fallo] --login incorrecto--> [S4: 2 fallos] --login incorrecto--> [S1: Bloqueada]
     ^                                  │                                    │
     │            login correcto        │          login correcto            │
     └──────────────────────────────────┘                                    │
     ^                                                                       │
     └───────────────────────────────────────────────────────────────────────┘
                                     (via reset de admin)
```

**Tabla de transición**:

| Estado actual | Login correcto | Login incorrecto | Reset de admin |
|---|---|---|---|
| S1: Bloqueada | - (inválida) | - (inválida) | S2: Inicio |
| S2: Inicio | Acceso OK (permanece) | S3: 1 fallo | - |
| S3: 1 fallo | Acceso OK --> S2 | S4: 2 fallos | - |
| S4: 2 fallos | Acceso OK --> S2 | S1: Bloqueada | - |

**Casos de prueba para cobertura de todas las transiciones**:

| CP | Estado inicial | Evento | Estado esperado | Acción esperada |
|---|---|---|---|---|
| CP-01 | S2 | Login correcto | S2 | Acceso concedido |
| CP-02 | S2 | Login incorrecto | S3 | Mensaje "credenciales incorrectas" |
| CP-03 | S3 | Login correcto | S2 | Acceso concedido, contador reset |
| CP-04 | S3 | Login incorrecto | S4 | Mensaje "último intento" |
| CP-05 | S4 | Login correcto | S2 | Acceso concedido, contador reset |
| CP-06 | S4 | Login incorrecto | S1 | Cuenta bloqueada |
| CP-07 | S1 | Reset de admin | S2 | Cuenta desbloqueada |
| CP-08 | S1 | Login correcto | S1 | Transición inválida: error "cuenta bloqueada" |
| CP-09 | S1 | Login incorrecto | S1 | Transición inválida: error "cuenta bloqueada" |

---

## Cuándo usar cada técnica

| Técnica | Mejor aplicación | Señal para usarla |
|---|---|---|
| **Partición de equivalencia** | Campos de entrada con rangos o conjuntos definidos | Hay especificaciones con rangos, listas de valores, tipos de datos |
| **Valores límite** | Complemento de partición de equivalencia para datos ordenados | Los requisitos definen rangos numéricos, fechas mínimas/máximas, longitudes |
| **Tablas de decisión** | Reglas de negocio con múltiples condiciones combinadas | "Si X y Y entonces Z", requisitos con lógica condicional compleja |
| **Transición de estados** | Sistemas con flujos, workflows, procesos con pasos | Hay estados definidos, ciclos de vida, flujos de aprobación |

---

## Combinación de técnicas

El ISTQB recomienda **no depender de una sola técnica**. En la práctica profesional:

1. Usar **partición de equivalencia** como base para identificar los dominios de datos.
2. Refinar con **valores límite** para los bordes de esos dominios.
3. Aplicar **tablas de decisión** cuando hay interacción entre condiciones de negocio.
4. Modelar con **transición de estados** los flujos donde el comportamiento depende del historial.
5. Complementar con técnicas basadas en experiencia (error guessing, exploratory testing).

---

## Fuentes

- **ISTQB Certified Tester Foundation Level (CTFL) Syllabus v4.0** (2023). International Software Testing Qualifications Board. Capítulo 4: "Test Analysis and Design". Disponible en: https://www.istqb.org/certifications/certified-tester-foundation-level — Consultado: 2026-09-22
- **ISTQB Glossary of Testing Terms**. Disponible en: https://glossary.istqb.org/ — Consultado: 2026-09-22
- **ASTQB** (American Software Testing Qualifications Board). Recursos y materiales de estudio CTFL. Disponible en: https://www.astqb.org/ — Consultado: 2026-09-22
