# Nightwatch.js - Referencia

> Referencia basada en la documentacion oficial de Nightwatch.js (nightwatchjs.org).
> Fecha de consulta: 2026-09-22.

## Tabla de contenidos

1. [Que es Nightwatch.js](#que-es-nightwatchjs)
2. [Configuracion (nightwatch.conf.js)](#configuracion-nightwatchconfjs)
3. [Comandos principales](#comandos-principales)
4. [Selectores y estrategias de localizacion](#selectores-y-estrategias-de-localizacion)
5. [Assertions: assert, verify, expect](#assertions-assert-verify-expect)
6. [Hooks del ciclo de test](#hooks-del-ciclo-de-test)
7. [Page Objects](#page-objects)
8. [Ejecucion: CLI, tags y environments](#ejecucion-cli-tags-y-environments)

---

## Que es Nightwatch.js

Nightwatch.js es un framework de testing end-to-end integrado, construido sobre Node.js. Usa la API del protocolo W3C WebDriver para controlar navegadores y puede ejecutar tests de componentes (React, Vue, Angular) ademas de tests E2E. Incluye su propio test runner, assertions, y soporte nativo para Page Objects.

### Caracteristicas principales

- Test runner integrado con soporte para ejecucion en paralelo
- Sintaxis BDD (describe/it) y exports (clasica de Nightwatch)
- Assertions propias + integrado con Chai expect
- Soporte para Selenium Server, ChromeDriver directo, o GeckoDriver directo
- Page Objects nativos
- Soporte para test de componentes (React, Vue, Angular, Storybook)
- Reports integrados (HTML, JUnit XML)

---

## Configuracion (nightwatch.conf.js)

El archivo de configuracion principal es `nightwatch.conf.js` (o `nightwatch.json`) en la raiz del proyecto.

### Estructura basica

```js
// nightwatch.conf.js
module.exports = {
  // Directorio donde estan los tests
  src_folders: ['tests/e2e'],

  // Directorio de Page Objects
  page_objects_path: ['tests/page-objects'],

  // Directorio de custom commands
  custom_commands_path: ['tests/custom-commands'],

  // Directorio de custom assertions
  custom_assertions_path: ['tests/custom-assertions'],

  // Variables globales compartidas entre tests
  globals_path: 'tests/globals.js',

  // Configuracion del WebDriver
  webdriver: {
    start_process: true,
    port: 9515
  },

  // Configuracion de test settings por entorno
  test_settings: {
    default: {
      desiredCapabilities: {
        browserName: 'chrome'
      },
      globals: {
        waitForConditionTimeout: 10000,
        retryAssertionTimeout: 5000
      }
    },

    chrome: {
      desiredCapabilities: {
        browserName: 'chrome',
        'goog:chromeOptions': {
          args: ['--headless', '--no-sandbox', '--disable-gpu']
        }
      },
      webdriver: {
        start_process: true,
        server_path: '', // Nightwatch puede auto-detectar con @nightwatch/chromedriver
        port: 9515
      }
    },

    firefox: {
      desiredCapabilities: {
        browserName: 'firefox',
        'moz:firefoxOptions': {
          args: ['--headless']
        }
      },
      webdriver: {
        start_process: true,
        server_path: '', // Auto-detecta con @nightwatch/geckodriver
        port: 4444
      }
    },

    selenium: {
      selenium: {
        start_process: true,
        port: 4444,
        server_path: '', // Auto-detecta con @nightwatch/selenium-server
        cli_args: {}
      },
      desiredCapabilities: {
        browserName: 'chrome'
      }
    }
  }
};
```

### Globals file

```js
// tests/globals.js
module.exports = {
  // Variables accesibles en todos los tests via browser.globals
  baseUrl: 'https://staging.miapp.com',
  waitForConditionTimeout: 10000,
  retryAssertionTimeout: 5000,

  // Hooks globales
  before(done) {
    console.log('Ejecutando setup global...');
    done();
  },

  after(done) {
    console.log('Ejecutando teardown global...');
    done();
  },

  beforeEach(browser, done) {
    // Se ejecuta antes de cada test file
    done();
  },

  afterEach(browser, done) {
    // Se ejecuta despues de cada test file
    done();
  }
};
```

---

## Comandos principales

Nightwatch expone los comandos a traves del objeto `browser` (o `client`). Todos los comandos son encadenables y asincrono-transparentes (Nightwatch gestiona las promesas internamente).

### Navegacion

```js
module.exports = {
  'Navegacion basica': function(browser) {
    browser
      .navigateTo('https://example.com')           // Navegar a una URL
      .url('https://example.com/about')             // Alternativa a navigateTo
      .back()                                        // Navegar atras
      .forward()                                     // Navegar adelante
      .refresh()                                     // Refrescar pagina
      .urlContains('about')                          // Assert: URL contiene texto
      .title(function(result) {                      // Obtener titulo
        console.log('Titulo:', result.value);
      });
  }
};
```

### Interaccion con elementos

```js
module.exports = {
  'Interaccion con elementos': function(browser) {
    browser
      // Click en un elemento
      .click('#submit-btn')

      // Escribir texto en un input
      .setValue('input[name="username"]', 'mi_usuario')

      // Limpiar un campo
      .clearValue('input[name="username"]')

      // Obtener texto de un elemento
      .getText('#welcome-message', function(result) {
        console.log('Mensaje:', result.value);
      })

      // Obtener valor de un atributo
      .getAttribute('a.nav-link', 'href', function(result) {
        console.log('Link:', result.value);
      })

      // Obtener valor de un input
      .getValue('input[name="email"]', function(result) {
        console.log('Email:', result.value);
      })

      // Verificar visibilidad
      .isVisible('#modal', function(result) {
        console.log('Es visible:', result.value);
      })

      // Enviar teclas especiales
      .sendKeys('input[name="search"]', [browser.Keys.ENTER])

      // Submit de formulario
      .submitForm('form#login-form');
  }
};
```

### Sintaxis BDD (describe/it)

```js
describe('Login Page', function() {
  before(function(browser) {
    browser.navigateTo('https://example.com/login');
  });

  it('should display the login form', function(browser) {
    browser
      .waitForElementVisible('#login-form', 5000)
      .assert.visible('input[name="username"]')
      .assert.visible('input[name="password"]')
      .assert.visible('#submit-btn');
  });

  it('should login with valid credentials', function(browser) {
    browser
      .setValue('input[name="username"]', 'admin')
      .setValue('input[name="password"]', 'password123')
      .click('#submit-btn')
      .waitForElementVisible('#dashboard', 10000)
      .assert.urlContains('/dashboard');
  });

  after(function(browser) {
    browser.end();
  });
});
```

### Esperas (waits)

```js
module.exports = {
  'Uso de waits': function(browser) {
    browser
      // Esperar hasta que un elemento sea visible
      .waitForElementVisible('#loading-done', 10000)

      // Esperar hasta que un elemento este presente en el DOM (aunque no sea visible)
      .waitForElementPresent('#hidden-data', 5000)

      // Esperar hasta que un elemento NO sea visible
      .waitForElementNotVisible('#spinner', 15000)

      // Esperar hasta que un elemento NO este en el DOM
      .waitForElementNotPresent('#temp-modal', 5000)

      // Pause (espera explicita -- evitar en lo posible)
      .pause(1000);
  }
};
```

---

## Selectores y estrategias de localizacion

Nightwatch soporta multiples estrategias de localizacion. El tipo de selector se puede especificar explicitamente o Nightwatch lo infiere automaticamente.

### Estrategias soportadas

| Estrategia | Sintaxis | Ejemplo |
|---|---|---|
| **CSS selector** (default) | String directo | `'#my-id'`, `'.my-class'`, `'div > p'` |
| **XPath** | String que empieza con `//` o `(//` | `'//div[@data-testid="header"]'` |
| **Selector object** | `{ selector: '...', locateStrategy: '...' }` | `{ selector: '//div', locateStrategy: 'xpath' }` |
| **By.id** | Usando `by` module | `by.id('username')` |
| **By.css** | Usando `by` module | `by.css('.active')` |
| **By.xpath** | Usando `by` module | `by.xpath('//button[text()="OK"]')` |

### Ejemplos

```js
describe('Selectores', function() {
  it('usa diferentes estrategias', function(browser) {
    // CSS selector (default)
    browser.click('#submit-btn');

    // XPath (auto-detectado por //)
    browser.click('//button[@type="submit"]');

    // Selector object explicito
    browser.click({
      selector: '//button[contains(text(), "Guardar")]',
      locateStrategy: 'xpath'
    });

    // Usando el modulo `by` (estilo Selenium)
    const { by } = require('nightwatch');
    browser.click(by.id('submit-btn'));
    browser.click(by.css('.btn-primary'));
  });
});
```

---

## Assertions: assert, verify, expect

Nightwatch ofrece tres interfaces de assertions:

### assert (estricto)

Si falla, el test se detiene inmediatamente (hard assertion).

```js
module.exports = {
  'Assertions estrictas': function(browser) {
    browser
      // Verificar que un elemento es visible
      .assert.visible('#header')

      // Verificar texto de un elemento
      .assert.textContains('#welcome', 'Bienvenido')

      // Verificar texto exacto
      .assert.textEquals('#status', 'Activo')

      // Verificar que un atributo tiene un valor
      .assert.attributeEquals('input#email', 'type', 'email')

      // Verificar que un atributo contiene un valor
      .assert.attributeContains('a.link', 'href', '/dashboard')

      // Verificar que un elemento tiene una clase CSS
      .assert.hasClass('#notification', 'alert-success')

      // Verificar la URL actual
      .assert.urlContains('/dashboard')

      // Verificar el titulo de la pagina
      .assert.titleEquals('Mi Aplicacion - Dashboard')

      // Verificar el numero de elementos
      .assert.elementsCount('.list-item', 5)

      // Verificar que un elemento existe en el DOM
      .assert.elementPresent('#sidebar')

      // Verificar un valor CSS
      .assert.cssProperty('#header', 'background-color', 'rgba(0, 0, 0, 1)');
  }
};
```

### verify (flexible)

Si falla, registra el fallo pero el test continua (soft assertion).

```js
module.exports = {
  'Assertions flexibles': function(browser) {
    browser
      // Mismos metodos que assert, pero no detiene el test si falla
      .verify.visible('#optional-banner')
      .verify.textContains('#footer', '2026')
      .verify.elementPresent('#analytics-script');
  }
};
```

### expect (estilo BDD con Chai)

Interface fluida estilo Chai para assertions mas legibles:

```js
module.exports = {
  'Assertions BDD': function(browser) {
    // Verificar visibilidad
    browser.expect.element('#header').to.be.visible;

    // Verificar texto
    browser.expect.element('#message').text.to.equal('Operacion exitosa');
    browser.expect.element('#message').text.to.contain('exitosa');
    browser.expect.element('#message').text.to.match(/exitosa/i);

    // Verificar atributos
    browser.expect.element('input#email').to.have.attribute('type').equals('email');
    browser.expect.element('a.link').to.have.attribute('href').which.contains('/home');

    // Verificar clase CSS
    browser.expect.element('#btn').to.have.css('display').which.equals('block');

    // Verificar habilitado/deshabilitado
    browser.expect.element('#submit').to.be.enabled;
    browser.expect.element('#disabled-field').to.not.be.enabled;

    // Verificar seleccionado (checkbox/radio)
    browser.expect.element('#terms-checkbox').to.be.selected;

    // Verificar que un elemento esta presente
    browser.expect.element('#sidebar').to.be.present;

    // Verificar cantidad de elementos
    browser.expect.elements('.row').count.to.equal(10);

    // Verificar titulo y URL
    browser.expect.title().to.contain('Dashboard');
    browser.expect.url().to.contain('/dashboard');
  }
};
```

---

## Hooks del ciclo de test

Nightwatch soporta hooks a nivel de test file y a nivel global.

### Hooks en un test file (sintaxis exports)

```js
module.exports = {
  // Se ejecuta una vez antes de todos los tests del archivo
  before: function(browser) {
    browser
      .navigateTo('https://example.com/login')
      .setValue('#username', 'admin')
      .setValue('#password', 'pass123')
      .click('#login-btn')
      .waitForElementVisible('#dashboard', 10000);
  },

  // Se ejecuta antes de cada test individual
  beforeEach: function(browser) {
    browser.navigateTo('https://example.com/dashboard');
  },

  'Test 1: verificar header': function(browser) {
    browser.assert.visible('#header');
  },

  'Test 2: verificar sidebar': function(browser) {
    browser.assert.visible('#sidebar');
  },

  // Se ejecuta despues de cada test individual
  afterEach: function(browser) {
    // Cleanup despues de cada test
  },

  // Se ejecuta una vez despues de todos los tests del archivo
  after: function(browser) {
    browser.end();
  }
};
```

### Hooks en sintaxis BDD (describe/it)

```js
describe('Dashboard Tests', function() {
  before(function(browser) {
    // Setup: una vez antes de todos los tests
    browser.navigateTo('https://example.com/login');
  });

  beforeEach(function(browser) {
    // Antes de cada test
    browser.navigateTo('https://example.com/dashboard');
  });

  it('should show user profile', function(browser) {
    browser.assert.visible('#profile');
  });

  afterEach(function(browser) {
    // Despues de cada test
  });

  after(function(browser) {
    // Teardown: una vez despues de todos los tests
    browser.end();
  });
});
```

### Hooks globales (globals.js)

Los hooks globales se ejecutan antes/despues de toda la suite, definidos en el archivo `globals_path`:

```js
// tests/globals.js
module.exports = {
  before: function(done) {
    // Se ejecuta antes de que inicie toda la suite de tests
    // Util para: levantar servidores, seed de BD, setup de datos
    console.log('Suite global: setup');
    done();
  },

  beforeEach: function(browser, done) {
    // Se ejecuta antes de cada test file
    done();
  },

  afterEach: function(browser, done) {
    // Se ejecuta despues de cada test file
    done();
  },

  after: function(done) {
    // Se ejecuta despues de que termina toda la suite
    // Util para: cleanup de datos, cerrar conexiones
    console.log('Suite global: teardown');
    done();
  }
};
```

### Orden de ejecucion de hooks

```
globals.before
  └── globals.beforeEach
        └── testFile.before
              └── testFile.beforeEach
                    └── test individual
              └── testFile.afterEach
        └── testFile.after
  └── globals.afterEach
globals.after
```

---

## Page Objects

Nightwatch tiene soporte nativo para Page Objects. Se definen como modulos Node.js con una estructura especifica y se acceden via `browser.page.<nombre>()`.

### Estructura basica de un Page Object

```js
// tests/page-objects/loginPage.js
const loginCommands = {
  login(username, password) {
    return this
      .waitForElementVisible('@usernameInput', 5000)
      .setValue('@usernameInput', username)
      .setValue('@passwordInput', password)
      .click('@submitButton')
      .waitForElementVisible('@dashboard', 10000);
  },

  clearForm() {
    return this
      .clearValue('@usernameInput')
      .clearValue('@passwordInput');
  }
};

module.exports = {
  url: 'https://example.com/login',

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
    dashboard: {
      selector: '#dashboard'
    }
  }
};
```

### Uso del Page Object en un test

```js
describe('Login Tests', function() {
  it('should login successfully', function(browser) {
    const loginPage = browser.page.loginPage();

    loginPage
      .navigate()                        // Navega a la URL definida en el Page Object
      .login('admin', 'password123')     // Usa el custom command del Page Object
      .assert.urlContains('/dashboard');
  });

  it('should show error for invalid credentials', function(browser) {
    const loginPage = browser.page.loginPage();

    loginPage
      .navigate()
      .login('invalid_user', 'wrong_pass')
      .assert.visible('@errorMessage')
      .assert.textContains('@errorMessage', 'credenciales incorrectas');
  });
});
```

### Sections (sub-secciones de una pagina)

Las sections permiten dividir una pagina en areas logicas, cada una con sus propios elements y commands:

```js
// tests/page-objects/dashboardPage.js
module.exports = {
  url: 'https://example.com/dashboard',

  sections: {
    header: {
      selector: '#app-header',
      elements: {
        logo: { selector: '.logo' },
        userMenu: { selector: '#user-menu' },
        logoutBtn: { selector: '#logout-btn' },
        notifications: { selector: '.notification-bell' }
      },
      commands: [{
        openUserMenu() {
          return this.click('@userMenu');
        },
        logout() {
          return this
            .click('@userMenu')
            .click('@logoutBtn');
        }
      }]
    },

    sidebar: {
      selector: '#sidebar',
      elements: {
        dashboardLink: { selector: 'a[href="/dashboard"]' },
        reportsLink: { selector: 'a[href="/reports"]' },
        settingsLink: { selector: 'a[href="/settings"]' }
      },
      commands: [{
        navigateToReports() {
          return this.click('@reportsLink');
        }
      }]
    },

    content: {
      selector: '#main-content',
      elements: {
        title: { selector: 'h1' },
        statsWidget: { selector: '.stats-widget' },
        recentActivity: { selector: '.recent-activity' }
      }
    }
  }
};
```

### Uso de sections en tests

```js
describe('Dashboard', function() {
  it('should navigate to reports from sidebar', function(browser) {
    const dashboard = browser.page.dashboardPage();
    dashboard.navigate();

    // Acceder a la section sidebar
    const sidebar = dashboard.section.sidebar;
    sidebar
      .assert.visible('@dashboardLink')
      .navigateToReports();

    // Acceder a la section header
    const header = dashboard.section.header;
    header.assert.visible('@logo');
  });

  it('should logout from header menu', function(browser) {
    const dashboard = browser.page.dashboardPage();
    dashboard.navigate();

    dashboard.section.header.logout();

    // Verificar que se volvio al login
    browser.assert.urlContains('/login');
  });
});
```

### Configuracion del directorio de Page Objects

En `nightwatch.conf.js`:

```js
module.exports = {
  page_objects_path: ['tests/page-objects'],
  // Puede ser un array con multiples directorios:
  // page_objects_path: ['tests/page-objects/auth', 'tests/page-objects/dashboard'],
};
```

---

## Ejecucion: CLI, tags y environments

### Comandos CLI basicos

```bash
# Ejecutar todos los tests
npx nightwatch

# Ejecutar un archivo de test especifico
npx nightwatch tests/e2e/login.test.js

# Ejecutar un directorio de tests
npx nightwatch tests/e2e/smoke/

# Ejecutar con un environment especifico
npx nightwatch --env chrome
npx nightwatch --env firefox

# Ejecutar tests en paralelo (por defecto usa test workers)
npx nightwatch --parallel

# Especificar numero de workers
npx nightwatch --workers 4

# Ejecutar tests con un tag especifico
npx nightwatch --tag login
npx nightwatch --tag smoke

# Excluir tests con un tag
npx nightwatch --skiptags slow

# Ejecutar un test individual dentro de un archivo (BDD syntax)
npx nightwatch tests/e2e/login.test.js --testcase "should login successfully"

# Ejecutar con reporter especifico
npx nightwatch --reporter html
npx nightwatch --reporter junit

# Generar reporte HTML en directorio personalizado
npx nightwatch --output tests/reports/

# Ejecutar con headless browser
npx nightwatch --headless

# Ejecutar en modo verbose (debug)
npx nightwatch --verbose

# Ejecutar con un config file especifico
npx nightwatch --config ./config/nightwatch.staging.conf.js

# Reintentar tests fallidos
npx nightwatch --retries 2

# Timeout personalizado para tests
npx nightwatch --timeout 30000
```

### Tags

Los tags permiten categorizar y filtrar tests. Se definen como propiedad del test:

```js
// Sintaxis exports
module.exports = {
  '@tags': ['smoke', 'login', 'critical'],

  'Test de login': function(browser) {
    // ...
  }
};
```

```js
// Sintaxis BDD
describe('Login @smoke @critical', function() {
  // Nightwatch parsea los tags del nombre del describe

  it('should login', function(browser) {
    // ...
  });
});
```

### Environments

Los environments se definen en `test_settings` del archivo de configuracion y se invocan con `--env`:

```bash
# Usar el environment "staging"
npx nightwatch --env staging

# Ejecutar en multiples environments en secuencia
npx nightwatch --env chrome,firefox

# Environment + tags
npx nightwatch --env chrome --tag smoke
```

### Desactivar tests

```js
module.exports = {
  '@disabled': true, // Desactivar todo el archivo

  'Test desactivado': function(browser) {
    // No se ejecuta
  }
};
```

### Integracion con CI (ejemplo en package.json)

```json
{
  "scripts": {
    "test:e2e": "npx nightwatch",
    "test:e2e:chrome": "npx nightwatch --env chrome --headless",
    "test:e2e:smoke": "npx nightwatch --tag smoke --headless",
    "test:e2e:parallel": "npx nightwatch --parallel --workers 4 --headless",
    "test:e2e:ci": "npx nightwatch --env chrome --headless --reporter junit --output reports/"
  }
}
```

---

## Fuentes

> **Nota:** Se intento obtener documentacion en tiempo real mediante WebSearch y WebFetch, pero el acceso fue denegado. El contenido de esta referencia se baso en conocimiento previo de la documentacion oficial. Se recomienda verificar contra la fuente original.

- **Nightwatch.js Getting Started**: https://nightwatchjs.org/guide/overview/what-is-nightwatch.html -- Consultado: 2026-09-22
- **Nightwatch.js Configuration**: https://nightwatchjs.org/guide/configuration/nightwatch-configuration-file.html -- Consultado: 2026-09-22
- **Nightwatch.js Commands**: https://nightwatchjs.org/api/ -- Consultado: 2026-09-22
- **Nightwatch.js Assertions**: https://nightwatchjs.org/api/assert/ -- Consultado: 2026-09-22
- **Nightwatch.js Page Objects**: https://nightwatchjs.org/guide/using-page-objects/getting-started.html -- Consultado: 2026-09-22
- **Nightwatch.js BDD Describe**: https://nightwatchjs.org/guide/writing-tests/using-bdd-describe.html -- Consultado: 2026-09-22
- **Nightwatch.js CLI Runner**: https://nightwatchjs.org/guide/running-tests/command-line-options.html -- Consultado: 2026-09-22
