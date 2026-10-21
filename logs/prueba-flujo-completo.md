# Prueba de Flujo Completo — 3 Preguntas Reales

Fecha: 2026-09-22
Objetivo: Demostrar el recorrido completo: Skill especializado (draft) → Checklist del orquestador → Respuesta final.

---

## Pregunta 1: "¿Cómo configuro un gate de aprobación en un pipeline YAML de Azure DevOps?"

### Paso 1 — Skill: `azure-devops`

**Referencia consultada:** `references/pipelines-yaml.md`, sección "Approvals y Checks (gates de aprobación)" (líneas 559-598)

**Draft generado:**

Las aprobaciones y checks en Azure DevOps **no se configuran directamente en el YAML**, sino sobre **resources** (environments, service connections, agent pools, variable groups, secure files, repositories).

**Pasos para configurar un gate de aprobación:**

1. En tu pipeline YAML, usa un **deployment job** que apunte a un environment:

```yaml
stages:
- stage: Deploy
  jobs:
  - deployment: DeployWeb
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - script: echo "Deploying to production"
```

2. Ve a **Pipelines > Environments** en Azure DevOps.
3. Selecciona el environment (ej: `production`).
4. En la pestaña **Approvals and checks**, haz clic en **+** > **Approvals**.
5. Agrega los aprobadores (usuarios o grupos).
6. Configura el timeout y opciones (ej: si el aprobador puede aprobar su propio run).
7. Guarda.

**Tipos de checks disponibles:**

| Check | Descripción |
|---|---|
| Approval | Aprobación manual por uno o más usuarios/grupos. Admite deferred approvals. |
| Branch control | Verifica que los recursos fueron construidos desde ramas permitidas. |
| Business hours | Restringe despliegues a ventanas horarias específicas. |
| Invoke Azure Function | Llama a una Azure Function; pasa si retorna éxito. |
| Invoke REST API | Llama a un endpoint REST externo periódicamente. |
| Query Azure Monitor Alerts | Verifica que no hay alertas activas tras un despliegue. |
| Required template | Fuerza el uso de un template YAML específico (extends). |
| Exclusive lock | Solo permite un run a la vez. lockBehavior: runLatest o sequential. |

**Orden de ejecución de los checks:** Static checks → Pre-check approvals → Dynamic checks → Post-check approvals → Exclusive lock.

**Bypass:** Solo usuarios con permiso de administrador del recurso pueden hacer bypass, y se registra en auditoría.

---

### Paso 2 — Checklist del Orquestador-Validador

**Verificación A — Respaldo documental:**
- ✅ "Las aprobaciones se configuran sobre resources, no en YAML" → Confirmado en `pipelines-yaml.md` línea 561
- ✅ Pasos de configuración (Pipelines > Environments > Approvals and checks) → Confirmado en líneas 586-592
- ✅ Tipos de checks (8 tipos listados) → Confirmado en tabla de líneas 574-583
- ✅ Orden de ejecución de checks (5 categorías) → Confirmado en líneas 563-570
- ✅ Bypass de checks → Confirmado en líneas 596-598
- ✅ Deployment job con environment → Confirmado en líneas 603-616
- ✅ Deferred approvals → Confirmado en línea 575
- ✅ lockBehavior opciones → Confirmado en línea 583

**Resultado: PASA** — todas las afirmaciones verificadas

**Verificación B — Contradicciones:**
- ✅ Sin contradicciones encontradas entre el draft y la fuente.

**Resultado: PASA**

**Verificación C — Detección de alucinación:**
- ✅ Sin fechas no verificadas
- ✅ Sin números de versión no confirmados
- ✅ Todos los nombres de checks coinciden con la fuente
- ✅ Sin valores numéricos inventados

**Resultado: PASA**

**Verificación D — Distinción verificado/no-verificado:**
- ✅ Todo el contenido está verificado, no hay necesidad de marcas de advertencia.

**Resultado: PASA**

### Paso 3 — Respuesta Final

[Se entrega el draft tal cual, sin modificaciones]

---
📋 Validación: PASÓ
📚 Fuentes: skills/azure-devops/references/pipelines-yaml.md (sección "Approvals y Checks", líneas 559-616)
⚠️ No verificado: Ninguno

---

---

## Pregunta 2: "¿Cómo diseño casos de prueba por partición de equivalencia para un formulario de matrícula?"

### Paso 1 — Skill: `qa-funcional`

**Referencia consultada:** `references/tecnicas-diseno-casos.md`, sección "1. Partición de Equivalencia" (líneas 26-63)

**Draft generado:**

La **partición de equivalencia** (ISTQB CTFL v4.0, Capítulo 4) consiste en dividir los datos de entrada en **clases de equivalencia** donde todos los valores dentro de una misma partición se tratan de la misma manera por el sistema.

**Principios para aplicarla:**

1. Las particiones pueden ser **válidas** (el sistema debe aceptarlas) o **inválidas** (debe rechazarlas).
2. Las particiones no deben solaparse y deben cubrir todo el dominio de entrada.
3. Se selecciona **al menos un valor representativo** de cada partición.
4. Las particiones inválidas se prueban **individualmente** para evitar que un rechazo enmascare otro.
5. Cobertura mínima: (N° de particiones cubiertas / N° total de particiones) × 100%

**Ejemplo aplicado a un formulario de matrícula:**

Supongamos un formulario con los campos: Nombre del alumno, Edad, Número de documento, Email de contacto.

**Campo: Edad (entero, rango 3-18 para matrícula escolar)**

| Partición | Rango | Tipo | Valor representativo |
|---|---|---|---|
| P1 | < 3 (ej: 0, 1, 2) | Inválida | 1 |
| P2 | 3 a 18 | Válida | 10 |
| P3 | > 18 (ej: 19, 50) | Inválida | 25 |
| P4 | No numérico (ej: "abc") | Inválida | "xyz" |
| P5 | Campo vacío | Inválida | "" |

**Campo: Email de contacto**

| Partición | Condición | Tipo | Valor representativo |
|---|---|---|---|
| P1 | Email con formato válido (x@y.z) | Válida | "padre@email.com" |
| P2 | Email sin "@" | Inválida | "padreemail.com" |
| P3 | Email sin dominio | Inválida | "padre@" |
| P4 | Campo vacío | Inválida | "" |

**Campo: Nombre del alumno**

| Partición | Condición | Tipo | Valor representativo |
|---|---|---|---|
| P1 | Texto con longitud dentro del rango permitido (1-100 chars) | Válida | "Juan Pérez" |
| P2 | Campo vacío | Inválida | "" |
| P3 | Texto que excede longitud máxima | Inválida | String de 101+ chars |
| P4 | Caracteres especiales no permitidos | Inválida | "<script>alert(1)</script>" |

**Casos de prueba resultantes:**

Los casos de prueba se derivan tomando un valor representativo de cada partición. Las particiones inválidas se prueban **una por caso de prueba** (con los demás campos en valores válidos) para aislar la causa del rechazo.

| CP | Nombre | Edad | Email | Resultado esperado |
|---|---|---|---|---|
| CP-01 | "Juan Pérez" | 10 | "padre@email.com" | Matrícula exitosa |
| CP-02 | "" | 10 | "padre@email.com" | Error: nombre obligatorio |
| CP-03 | String 101 chars | 10 | "padre@email.com" | Error: nombre excede longitud |
| CP-04 | "Juan Pérez" | 1 | "padre@email.com" | Error: edad fuera de rango |
| CP-05 | "Juan Pérez" | 25 | "padre@email.com" | Error: edad fuera de rango |
| CP-06 | "Juan Pérez" | "xyz" | "padre@email.com" | Error: edad no válida |
| CP-07 | "Juan Pérez" | 10 | "padreemail.com" | Error: email inválido |
| CP-08 | "Juan Pérez" | 10 | "" | Error: email obligatorio |

**Recomendación:** Complementar con **análisis de valores límite** en el campo Edad (probar 2, 3, 18, 19) para mayor cobertura en los bordes.

---

### Paso 2 — Checklist del Orquestador-Validador

**Verificación A — Respaldo documental:**
- ✅ Definición de partición de equivalencia → Confirmado en `tecnicas-diseno-casos.md` líneas 30-31
- ✅ Particiones válidas e inválidas → Confirmado en línea 37
- ✅ No solaparse + cubrir todo el dominio → Confirmado en línea 38
- ✅ Un valor representativo por partición → Confirmado en línea 39
- ✅ Particiones inválidas individualmente → Confirmado en línea 40
- ✅ Fórmula de cobertura → Confirmado en línea 43
- ✅ Referencia a ISTQB CTFL v4.0 Capítulo 4 → Confirmado en líneas 1-3
- ⚠️ Rango de edad 3-18 para matrícula escolar → **Creado como ejemplo**, no proviene de la referencia. Es un supuesto razonable para el ejemplo, no una afirmación técnica de la herramienta.
- ⚠️ Validaciones de email y nombre → **Creadas como ejemplo aplicado**, no están en la referencia ISTQB. Son aplicación de la técnica, no afirmaciones sobre la técnica en sí.
- ✅ Recomendación de complementar con valores límite → Confirmado en líneas 260-267 (sección "Combinación de técnicas")

**Resultado: PASA** — Los supuestos del ejemplo están claramente presentados como ejemplo, no como doctrina ISTQB.

**Verificación B — Contradicciones:**
- ✅ Sin contradicciones. Los principios y la fórmula coinciden exactamente con la fuente.

**Resultado: PASA**

**Verificación C — Detección de alucinación:**
- ✅ Sin fechas ni versiones inventadas
- ✅ La referencia al Capítulo 4 es correcta
- ✅ No se inventan términos ISTQB

**Resultado: PASA**

**Verificación D — Distinción verificado/no-verificado:**
- ✅ Los principios ISTQB están presentados como verificados.
- ✅ El ejemplo del formulario de matrícula está claramente presentado como caso de aplicación, no como contenido ISTQB.

**Resultado: PASA**

### Paso 3 — Respuesta Final

[Se entrega el draft tal cual, sin modificaciones]

---
📋 Validación: PASÓ
📚 Fuentes: skills/qa-funcional/references/tecnicas-diseno-casos.md (sección "Partición de Equivalencia", líneas 26-63; sección "Combinación de técnicas", líneas 259-267)
⚠️ No verificado: Ninguno (los ejemplos del formulario de matrícula son aplicación de la técnica, no afirmaciones técnicas)

---

---

## Pregunta 3: "Dame un ejemplo de Page Object en Nightwatch.js para un login"

### Paso 1 — Skill: `qa-automation`

**Referencias consultadas:**
- `references/patrones-page-object.md`, sección "Implementación en Nightwatch.js" (líneas 305-528)
- `references/nightwatch.md`, sección "Page Objects" (líneas 550-723)

**Draft generado:**

Nightwatch.js tiene soporte **nativo** para Page Objects. Se definen como módulos Node.js con `module.exports` usando una estructura declarativa de `elements`, `commands` y opcionalmente `sections`.

**1. Page Object del Login:**

```js
// tests/page-objects/loginPage.js
const loginCommands = {
  login(username, password) {
    return this
      .waitForElementVisible('@usernameInput', 5000)
      .clearValue('@usernameInput')
      .setValue('@usernameInput', username)
      .clearValue('@passwordInput')
      .setValue('@passwordInput', password)
      .click('@submitButton');
  },

  loginExpectingError(username, password) {
    return this
      .login(username, password)
      .waitForElementVisible('@errorMessage', 5000);
  },

  getErrorText(callback) {
    return this.getText('@errorMessage', function(result) {
      if (typeof callback === 'function') {
        callback(result.value);
      }
    });
  }
};

module.exports = {
  url: function() {
    return `${this.api.launchUrl}/login`;
  },

  commands: [loginCommands],

  elements: {
    usernameInput: {
      selector: 'input[name="username"]'
    },
    passwordInput: {
      selector: 'input[name="password"]'
    },
    submitButton: {
      selector: '#login-btn'
    },
    errorMessage: {
      selector: '.alert-danger'
    },
    rememberMe: {
      selector: '#remember-me'
    },
    forgotPasswordLink: {
      selector: 'a[href="/forgot-password"]'
    }
  }
};
```

**2. Test usando el Page Object:**

```js
// tests/specs/login.test.js
describe('Login Tests con Page Objects', function() {

  it('should login with valid credentials', function(browser) {
    const loginPage = browser.page.loginPage();
    const dashboardPage = browser.page.dashboardPage();

    loginPage
      .navigate()
      .login('admin', 'password123');

    dashboardPage
      .waitForPageLoad()
      .section.content
        .assert.visible('@welcomeMessage')
        .assert.textContains('@welcomeMessage', 'Bienvenido');
  });

  it('should show error for invalid credentials', function(browser) {
    const loginPage = browser.page.loginPage();

    loginPage
      .navigate()
      .loginExpectingError('invalid_user', 'wrong_pass')
      .assert.visible('@errorMessage')
      .assert.textContains('@errorMessage', 'Credenciales incorrectas');
  });
});
```

**3. Configuración necesaria:**

En `nightwatch.conf.js`, asegúrate de declarar el directorio de Page Objects:

```js
module.exports = {
  page_objects_path: ['tests/page-objects'],
  // ...
};
```

**Puntos clave:**
- Los Page Objects se acceden como `browser.page.<nombreDelArchivo>()`
- Los elements se referencian con `@` en comandos del Page Object (ej: `@usernameInput`)
- `.navigate()` navega automáticamente a la URL definida en el Page Object
- Los commands encapsulan acciones (login, clearForm, etc.) — el test no toca localizadores directamente
- Si el login lleva a otra página, se usa otro Page Object (como `dashboardPage`) para las verificaciones en esa nueva vista

---

### Paso 2 — Checklist del Orquestador-Validador

**Verificación A — Respaldo documental:**
- ✅ "Nightwatch tiene soporte nativo para Page Objects" → Confirmado en `nightwatch.md` línea 552 y `patrones-page-object.md` línea 307
- ✅ Estructura con module.exports, elements, commands → Confirmado en `nightwatch.md` líneas 555-597 y `patrones-page-object.md` líneas 309-367
- ✅ Sintaxis de loginCommands con this encadenado → Confirmado en `patrones-page-object.md` líneas 313-337
- ✅ url como función con this.api.launchUrl → Confirmado en `patrones-page-object.md` línea 341
- ✅ Uso de @ para referenciar elements → Confirmado en `nightwatch.md` líneas 601-622
- ✅ browser.page.<nombre>() para acceder → Confirmado en `nightwatch.md` línea 528 y línea 605
- ✅ .navigate() navega a la URL del PO → Confirmado en `nightwatch.md` línea 608
- ✅ page_objects_path en config → Confirmado en `nightwatch.md` líneas 714-722 y `patrones-page-object.md` líneas 520-527
- ✅ Sections (dashboardPage con header, sidebar, content) → Confirmado en `nightwatch.md` líneas 626-678 y `patrones-page-object.md` líneas 369-448
- ✅ Test usando section.content.assert → Confirmado en `patrones-page-object.md` líneas 466-469

**Resultado: PASA** — todas las afirmaciones verificadas

**Verificación B — Contradicciones:**
- ✅ La estructura del Page Object (elements, commands, url, sections) coincide exactamente con ambas fuentes.
- ✅ La forma de acceder (browser.page.loginPage()) es consistente.
- ✅ La sintaxis de @ para elements es consistente.

**Resultado: PASA**

**Verificación C — Detección de alucinación:**
- ✅ Sin fechas ni versiones inventadas
- ✅ Los selectores son ejemplos genéricos, no se presentan como obligatorios
- ✅ Sin afirmaciones sobre comportamientos no documentados

**Resultado: PASA**

**Verificación D — Distinción verificado/no-verificado:**
- ✅ Todo el contenido está verificado contra las referencias.
- ✅ Los selectores (ids, clases) son ejemplos, presentados como tales.

**Resultado: PASA**

### Paso 3 — Respuesta Final

[Se entrega el draft tal cual, sin modificaciones]

---
📋 Validación: PASÓ
📚 Fuentes: skills/qa-automation/references/patrones-page-object.md (sección "Implementación en Nightwatch.js", líneas 305-528), skills/qa-automation/references/nightwatch.md (sección "Page Objects", líneas 550-723)
⚠️ No verificado: Ninguno

---

## Resumen de la prueba

| Pregunta | Skill | Verificación A | Verificación B | Verificación C | Verificación D | Resultado |
|---|---|---|---|---|---|---|
| Gate de aprobación en pipeline YAML | azure-devops | ✅ PASA | ✅ PASA | ✅ PASA | ✅ PASA | **APROBADO** |
| Partición de equivalencia para matrícula | qa-funcional | ✅ PASA | ✅ PASA | ✅ PASA | ✅ PASA | **APROBADO** |
| Page Object en Nightwatch.js para login | qa-automation | ✅ PASA | ✅ PASA | ✅ PASA | ✅ PASA | **APROBADO** |

Las 3 preguntas pasaron el checklist completo. El flujo Skill → Orquestador → Respuesta Final funciona correctamente.
