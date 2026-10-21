# Criterios de Aceptación en Formato Given-When-Then

Referencia sobre la escritura de criterios de aceptación utilizando la sintaxis **Gherkin** y el patrón **Given-When-Then** (GWT), basada en la documentación oficial de Cucumber y buenas prácticas de la industria BDD (Behavior-Driven Development).

---

## Qué son los criterios de aceptación

Los criterios de aceptación definen las **condiciones que deben cumplirse** para que una funcionalidad (user story, feature) sea considerada completa y correcta. Son el contrato entre el equipo de desarrollo, QA y el Product Owner.

### Características de buenos criterios de aceptación

| Característica | Descripción |
|---|---|
| **Verificables** | Se puede determinar objetivamente si se cumplen o no |
| **Específicos** | Sin ambigüedad; cada persona los interpreta igual |
| **Independientes** | Cada criterio es evaluable por separado |
| **Orientados al comportamiento** | Describen QUE hace el sistema, no COMO lo implementa |
| **Completos** | Cubren el happy path y los escenarios alternativos/negativos |

---

## Gherkin: el lenguaje

**Gherkin** es un lenguaje de dominio específico (DSL) diseñado para describir el comportamiento del software en un formato legible por humanos y ejecutable por herramientas de automatización (Cucumber, SpecFlow, Behave, etc.).

### Estructura de un archivo .feature

```gherkin
# language: es
@etiqueta_feature
Feature: Nombre de la funcionalidad
  Como [rol de usuario]
  Quiero [acción o funcionalidad]
  Para [beneficio o valor de negocio]

  Background:
    Given una precondición común a todos los escenarios

  @etiqueta_escenario
  Scenario: Nombre descriptivo del escenario
    Given [contexto inicial / precondición]
    And [otra precondición si es necesario]
    When [acción del usuario o evento]
    And [otra acción si es necesario]
    Then [resultado esperado observable]
    And [otro resultado esperado]
    But [algo que NO debería ocurrir]

  Scenario Outline: Nombre con parámetros
    Given [contexto con <variable>]
    When [acción con <variable>]
    Then [resultado con <variable>]

    Examples:
      | variable | otra_variable |
      | valor1   | resultado1    |
      | valor2   | resultado2    |
```

---

## Keywords de Gherkin

### Keywords principales

| Keyword | Español | Propósito |
|---|---|---|
| `Feature` | `Característica` | Agrupa escenarios relacionados. Describe la funcionalidad bajo prueba |
| `Scenario` | `Escenario` | Un caso de prueba concreto, un ejemplo del comportamiento |
| `Given` | `Dado` / `Dada` / `Dados` / `Dadas` | Establece el contexto inicial (precondiciones) |
| `When` | `Cuando` | Describe la acción o evento que desencadena el comportamiento |
| `Then` | `Entonces` | Define el resultado esperado (observable y verificable) |
| `And` | `Y` | Continúa el paso anterior (Given, When o Then) |
| `But` | `Pero` | Igual que And, pero para condiciones negativas o excepciones |
| `Background` | `Antecedentes` | Pasos comunes que se ejecutan antes de cada Scenario del Feature |
| `Scenario Outline` | `Esquema del escenario` | Template de escenario con variables, combinado con Examples |
| `Examples` | `Ejemplos` | Tabla de datos que alimenta un Scenario Outline |

### Keywords secundarios

| Keyword | Propósito |
|---|---|
| `@tag` | Etiqueta para filtrar, organizar o configurar ejecuciones |
| `#` | Comentario (se ignora en la ejecución) |
| `"""` (docstring) | Bloque de texto largo como parámetro de un paso |
| `\|` (data table) | Tabla de datos inline para un paso |
| `Rule` | Agrupa escenarios bajo una regla de negocio (Gherkin 6+) |

---

## Given-When-Then en detalle

### Given (Dado que...)

Establece el **estado inicial** del sistema antes de la acción. Describe precondiciones que ya ocurrieron (tiempo pasado o estado presente).

**Ejemplos**:
```gherkin
Given el usuario "juan@email.com" está registrado en el sistema
Given el carrito de compras contiene 3 productos
Given la fecha actual es posterior al 2026-01-01
```

**Reglas**:
- No describe acciones del usuario (eso es When).
- Puede incluir datos de configuración, estados de base de datos, etc.
- Si hay múltiples precondiciones, usar `And`.

### When (Cuando...)

Describe la **acción o evento** que desencadena el comportamiento bajo prueba. Es el punto de inflexión del escenario.

**Ejemplos**:
```gherkin
When el usuario hace clic en "Iniciar sesión"
When el sistema recibe una solicitud POST en /api/orders
When transcurren 30 minutos sin actividad
```

**Reglas**:
- Idealmente **un solo When** por escenario (una acción principal).
- Si hay múltiples acciones, considerar si debería ser escenarios separados.
- Describe la interacción, no el resultado.

### Then (Entonces...)

Define el **resultado esperado** observable y verificable. Es lo que se valida.

**Ejemplos**:
```gherkin
Then el sistema muestra el mensaje "Bienvenido, Juan"
Then el pedido queda registrado con estado "Pendiente"
Then se envía un email de confirmación a "juan@email.com"
Then el código de respuesta HTTP es 201
```

**Reglas**:
- Debe ser **verificable** (no "el sistema funciona bien").
- Puede incluir múltiples validaciones con `And`.
- Usar `But` para lo que NO debe ocurrir: `But no se muestra el campo de contraseña`.

---

## Scenario Outline con Examples

Un **Scenario Outline** es un template que se ejecuta múltiples veces con distintos datos. Es ideal para probar la misma lógica con diferentes combinaciones de entrada/salida.

### Ejemplo completo

```gherkin
Feature: Validación de edad para registro
  Como sistema de registro
  Quiero validar la edad del usuario
  Para cumplir con requisitos legales de edad mínima

  Scenario Outline: Validar rango de edad permitido
    Given el usuario está en el formulario de registro
    When ingresa la edad <edad>
    Then el sistema muestra <resultado>

    Examples:
      | edad | resultado                          |
      | 17   | "Debe ser mayor de 18 años"        |
      | 18   | "Edad válida"                      |
      | 25   | "Edad válida"                      |
      | 65   | "Edad válida"                      |
      | 66   | "La edad máxima permitida es 65"   |
      | -1   | "La edad debe ser un número válido"|
```

### Cuándo usar Scenario Outline vs. Scenarios separados

| Usar Scenario Outline | Usar Scenarios separados |
|---|---|
| La lógica es la misma, solo cambian los datos | Cada escenario tiene pasos diferentes |
| Se quiere probar múltiples valores límite | Los escenarios representan flujos distintos |
| La tabla de Examples documenta bien las variaciones | Cada escenario necesita su propio contexto narrativo |

---

## Background

El **Background** define pasos comunes que se ejecutan antes de **cada** Scenario dentro del mismo Feature. Evita repetición de precondiciones.

### Ejemplo

```gherkin
Feature: Gestión de carrito de compras

  Background:
    Given el usuario "maria@email.com" está autenticado
    And existe el producto "Laptop Pro" con precio $999
    And existe el producto "Mouse Wireless" con precio $29

  Scenario: Agregar producto al carrito
    When el usuario agrega "Laptop Pro" al carrito
    Then el carrito muestra 1 producto
    And el total es $999

  Scenario: Agregar múltiples productos
    When el usuario agrega "Laptop Pro" al carrito
    And el usuario agrega "Mouse Wireless" al carrito
    Then el carrito muestra 2 productos
    And el total es $1028
```

**Regla**: el Background no debe ser excesivamente largo. Si supera 4-5 líneas, considerar si algunos pasos pertenecen solo a ciertos escenarios.

---

## Data Tables

Las **data tables** permiten pasar datos estructurados a un paso individual.

```gherkin
Scenario: Registro de nuevo usuario con todos los campos
  Given el usuario está en la página de registro
  When completa el formulario con los siguientes datos:
    | campo      | valor              |
    | nombre     | Juan Pérez         |
    | email      | juan@email.com     |
    | contraseña | SecurePass123!     |
    | país       | Argentina          |
  And hace clic en "Registrarse"
  Then el sistema muestra "Cuenta creada exitosamente"
```

---

## Tags (Etiquetas)

Los tags permiten organizar, filtrar y configurar la ejecución de escenarios.

```gherkin
@smoke @login
Feature: Autenticación de usuarios

  @happy-path
  Scenario: Login exitoso con credenciales válidas
    ...

  @negative @security
  Scenario: Login fallido con contraseña incorrecta
    ...

  @wip
  Scenario: Login con autenticación de dos factores
    ...
```

### Tags comunes

| Tag | Propósito |
|---|---|
| `@smoke` | Pruebas de humo (suite rápida) |
| `@regression` | Pruebas de regresión |
| `@wip` | Work in progress (excluir de ejecución CI) |
| `@happy-path` | Flujo principal exitoso |
| `@negative` | Escenarios de error o rechazo |
| `@manual` | Requiere ejecución manual |
| `@bug-XXXX` | Relacionado con un defecto específico |
| `@sprint-XX` | Asociado a un sprint |

---

## Rule (Gherkin 6+)

El keyword `Rule` agrupa escenarios que ilustran una misma regla de negocio dentro de un Feature.

```gherkin
Feature: Política de descuentos

  Rule: Clientes premium reciben 10% de descuento
    Scenario: Cliente premium compra producto regular
      Given el cliente "Ana" tiene membresía premium
      When agrega un producto de $100 al carrito
      Then el precio con descuento es $90

    Scenario: Cliente premium compra producto en oferta
      Given el cliente "Ana" tiene membresía premium
      And el producto "Auriculares" tiene 20% de oferta
      When agrega "Auriculares" de $100 al carrito
      Then se aplica el mayor descuento (20%)
      And el precio final es $80

  Rule: Clientes regulares no reciben descuento automático
    Scenario: Cliente regular compra producto
      Given el cliente "Pedro" tiene membresía regular
      When agrega un producto de $100 al carrito
      Then el precio es $100
```

---

## Buenas prácticas

### 1. Escribir en lenguaje de negocio, no técnico

```gherkin
# MAL - demasiado técnico
When el usuario envía un POST a /api/v2/users con body JSON {"name": "Juan"}
Then el response code es 201

# BIEN - lenguaje de negocio
When el usuario crea una nueva cuenta con nombre "Juan"
Then la cuenta se crea exitosamente
```

**Excepción**: si los criterios son para pruebas de API específicamente, el lenguaje técnico es apropiado.

### 2. Un escenario = un comportamiento

```gherkin
# MAL - múltiples comportamientos en un escenario
Scenario: Gestión completa de usuario
  When el usuario se registra
  Then la cuenta se crea
  When el usuario inicia sesión
  Then accede al dashboard
  When el usuario cambia su contraseña
  Then recibe confirmación

# BIEN - un comportamiento por escenario
Scenario: Registro exitoso
  Given el usuario está en la página de registro
  When completa el formulario con datos válidos
  Then la cuenta se crea exitosamente

Scenario: Login exitoso
  Given el usuario tiene una cuenta activa
  When ingresa sus credenciales correctas
  Then accede al dashboard
```

### 3. Given establece contexto, no cuenta una historia

```gherkin
# MAL - narrativa paso a paso en Given
Given el usuario abre el navegador
And el usuario navega a la página principal
And el usuario hace clic en "Registro"
And el usuario completa el formulario
And la cuenta fue creada exitosamente
When el usuario intenta iniciar sesión
Then ...

# BIEN - estado declarativo
Given el usuario tiene una cuenta registrada
When intenta iniciar sesión con sus credenciales
Then ...
```

### 4. Evitar detalles de implementación UI

```gherkin
# MAL - acoplado a la UI
When el usuario hace clic en el botón con id="btn-submit" en el div.form-container
Then el elemento span.success-message muestra "OK"

# BIEN - comportamiento observable
When el usuario envía el formulario
Then se muestra un mensaje de éxito
```

### 5. Usar Scenario Outline para variaciones de datos

```gherkin
# MAL - escenarios duplicados
Scenario: Login con email vacío
  Given el usuario está en la página de login
  When deja el email vacío y hace clic en "Entrar"
  Then ve el mensaje "El email es obligatorio"

Scenario: Login con contraseña vacía
  Given el usuario está en la página de login
  When completa el email pero deja la contraseña vacía
  Then ve el mensaje "La contraseña es obligatoria"

# BIEN - Scenario Outline
Scenario Outline: Validación de campos obligatorios en login
  Given el usuario está en la página de login
  When deja el campo <campo> vacío y hace clic en "Entrar"
  Then ve el mensaje <mensaje_error>

  Examples:
    | campo      | mensaje_error                    |
    | email      | "El email es obligatorio"        |
    | contraseña | "La contraseña es obligatoria"   |
```

### 6. Then debe ser verificable y observable

```gherkin
# MAL - no verificable
Then el sistema funciona correctamente
Then los datos se guardan en la base de datos

# BIEN - verificable
Then se muestra el mensaje "Pedido confirmado con número #12345"
Then el estado del pedido en la lista es "Procesando"
```

### 7. Mantener los escenarios cortos

- **Given**: 1-5 líneas (contexto necesario)
- **When**: 1-2 líneas (idealmente una sola acción)
- **Then**: 1-5 líneas (resultados verificables)
- **Total por escenario**: no más de 10-12 pasos

### 8. No reutilizar el Feature file como manual de usuario

El feature file documenta **comportamiento esperado**, no es un manual paso a paso. Si necesita demasiado detalle, probablemente falta una abstracción.

---

## Anti-patrones comunes

| Anti-patrón | Problema | Solución |
|---|---|---|
| **Escenario enciclopédico** | 30+ pasos, imposible de mantener | Dividir en escenarios atómicos |
| **Given interminable** | Background con 15 precondiciones | Usar helpers, simplificar estado inicial |
| **Lenguaje de programador** | "Ejecutar query SQL...", "Hacer click en #btn-123" | Escribir en lenguaje de negocio |
| **Escenario sin Then** | Describe acciones pero no verifica nada | Siempre incluir al menos un Then verificable |
| **Datos hardcodeados sin sentido** | "El usuario abc123 con password xyz789" | Usar datos que transmitan intención |
| **Incidental details** | Pasos irrelevantes para el comportamiento bajo prueba | Incluir solo lo necesario para el comportamiento |
| **Scenario Outline con 1 Example** | No tiene sentido parametrizar para un solo caso | Usar Scenario simple |

---

## Gherkin en español

Gherkin soporta múltiples idiomas. Para escribir en español, agregar el header `# language: es` al inicio del archivo .feature.

### Keywords en español

| Inglés | Español |
|---|---|
| Feature | Característica |
| Scenario | Escenario |
| Scenario Outline | Esquema del escenario |
| Examples | Ejemplos |
| Background | Antecedentes |
| Given | Dado / Dada / Dados / Dadas |
| When | Cuando |
| Then | Entonces |
| And | Y |
| But | Pero |
| Rule | Regla |

### Ejemplo completo en español

```gherkin
# language: es
@login
Característica: Inicio de sesión
  Como usuario registrado
  Quiero iniciar sesión en la aplicación
  Para acceder a mis datos personales

  Antecedentes:
    Dado que existe el usuario "maria@email.com" con contraseña "Pass123!"

  @happy-path
  Escenario: Login exitoso con credenciales válidas
    Dado que el usuario está en la página de inicio de sesión
    Cuando ingresa el email "maria@email.com"
    Y ingresa la contraseña "Pass123!"
    Y hace clic en "Iniciar sesión"
    Entonces accede al dashboard principal
    Y ve el mensaje "Bienvenida, Maria"

  @negative
  Escenario: Login fallido con contraseña incorrecta
    Dado que el usuario está en la página de inicio de sesión
    Cuando ingresa el email "maria@email.com"
    Y ingresa la contraseña "incorrecta"
    Y hace clic en "Iniciar sesión"
    Entonces ve el mensaje de error "Credenciales inválidas"
    Pero no accede al dashboard

  Esquema del escenario: Validación de campos obligatorios
    Dado que el usuario está en la página de inicio de sesión
    Cuando deja el campo <campo> vacío
    Y hace clic en "Iniciar sesión"
    Entonces ve el mensaje <mensaje>

    Ejemplos:
      | campo      | mensaje                        |
      | email      | "El email es obligatorio"      |
      | contraseña | "La contraseña es obligatoria" |
```

---

## Fuentes

- **Cucumber — Gherkin Reference**. Documentación oficial de la sintaxis Gherkin. Disponible en: https://cucumber.io/docs/gherkin/reference/ — Consultado: 2026-09-22
- **Cucumber — BDD Overview / Better Gherkin**. Buenas prácticas para escritura de escenarios. Disponible en: https://cucumber.io/docs/bdd/ — Consultado: 2026-09-22
- **Cucumber — Gherkin Localisation (i18n)**. Keywords en español y otros idiomas. Disponible en: https://cucumber.io/docs/gherkin/languages/ — Consultado: 2026-09-22
- **Dan North — "Introducing BDD"** (2006). Artículo fundacional de Behavior-Driven Development. Disponible en: https://dannorth.net/introducing-bdd/ — Consultado: 2026-09-22
- **ISTQB CTFL Syllabus v4.0** (2023). Sección sobre Acceptance Testing y criterios de aceptación. Disponible en: https://www.istqb.org/certifications/certified-tester-foundation-level — Consultado: 2026-09-22
