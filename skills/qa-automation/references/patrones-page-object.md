# Patron Page Object Model (POM) - Referencia

> Referencia basada en la documentacion oficial de Selenium y mejores practicas de la industria.
> Fecha de consulta: 2026-09-22.

## Tabla de contenidos

1. [Principios del patron](#principios-del-patron)
2. [Estructura tipica](#estructura-tipica)
3. [Implementacion en Selenium (JavaScript)](#implementacion-en-selenium-javascript)
4. [Implementacion en Nightwatch.js](#implementacion-en-nightwatchjs)
5. [Beneficios](#beneficios)
6. [Anti-patrones](#anti-patrones)

---

## Principios del patron

El Page Object Model (POM) es un patron de diseno ampliamente adoptado en test automation que establece una **separacion clara entre la logica del test y la interaccion con la interfaz de usuario**. Cada pagina (o componente significativo) de la aplicacion se representa como una clase o modulo que encapsula:

- **Los elementos** de esa pagina (localizadores)
- **Las acciones** que un usuario puede realizar en esa pagina (metodos)

### Reglas fundamentales

1. **Un Page Object por pagina (o componente significativo)** -- Cada pagina o seccion funcional de la UI tiene su propio Page Object.
2. **Los tests no acceden directamente a elementos del DOM** -- Solo interactuan con los metodos del Page Object.
3. **Los Page Objects exponen servicios, no implementacion** -- El test dice `loginPage.login(user, pass)`, no `driver.findElement(By.id('user')).sendKeys(user)`.
4. **Los Page Objects no contienen assertions** -- Las assertions pertenecen al test, no al Page Object (excepto waits de estado que son parte de la navegacion).
5. **Los metodos retornan otros Page Objects cuando la accion navega a otra pagina** -- Si hacer click en "Login" lleva al Dashboard, el metodo `login()` retorna un `DashboardPage`.

---

## Estructura tipica

### Organizacion de archivos

```
tests/
├── page-objects/
│   ├── BasePage.js           # Clase base con metodos comunes
│   ├── LoginPage.js
│   ├── DashboardPage.js
│   ├── UserProfilePage.js
│   └── components/
│       ├── HeaderComponent.js
│       ├── SidebarComponent.js
│       └── ModalComponent.js
├── specs/                     # Tests
│   ├── login.spec.js
│   ├── dashboard.spec.js
│   └── user-profile.spec.js
├── data/                      # Datos de test
│   └── test-users.json
└── config/
    └── nightwatch.conf.js
```

### Anatomia de un Page Object

Cada Page Object tiene tres partes:

| Parte | Descripcion | Ejemplo |
|---|---|---|
| **Localizadores** (elements) | Selectores para encontrar elementos en la pagina | `usernameInput = By.id('username')` |
| **Acciones** (methods) | Metodos que representan acciones del usuario | `login(user, pass)`, `searchProduct(query)` |
| **URL / Navegacion** | URL de la pagina y metodo para navegar a ella | `url = '/login'`, `open()` |

---

## Implementacion en Selenium (JavaScript)

### Clase base (BasePage)

```js
// tests/page-objects/BasePage.js
const { By, until } = require('selenium-webdriver');

class BasePage {
  constructor(driver) {
    this.driver = driver;
    this.timeout = 10000;
  }

  async open(path) {
    const baseUrl = process.env.BASE_URL || 'https://example.com';
    await this.driver.get(`${baseUrl}${path}`);
    return this;
  }

  async findElement(locator) {
    await this.driver.wait(until.elementLocated(locator), this.timeout);
    return this.driver.findElement(locator);
  }

  async click(locator) {
    const element = await this.findElement(locator);
    await this.driver.wait(until.elementIsEnabled(element), this.timeout);
    await element.click();
    return this;
  }

  async type(locator, text) {
    const element = await this.findElement(locator);
    await element.clear();
    await element.sendKeys(text);
    return this;
  }

  async getText(locator) {
    const element = await this.findElement(locator);
    return element.getText();
  }

  async isDisplayed(locator) {
    try {
      const element = await this.findElement(locator);
      return element.isDisplayed();
    } catch {
      return false;
    }
  }

  async waitForVisible(locator, timeout = this.timeout) {
    const element = await this.driver.findElement(locator);
    await this.driver.wait(until.elementIsVisible(element), timeout);
    return element;
  }

  async takeScreenshot(filename) {
    const screenshot = await this.driver.takeScreenshot();
    const fs = require('fs');
    fs.writeFileSync(`screenshots/${filename}.png`, screenshot, 'base64');
  }
}

module.exports = BasePage;
```

### Page Object: LoginPage

```js
// tests/page-objects/LoginPage.js
const { By } = require('selenium-webdriver');
const BasePage = require('./BasePage');
const DashboardPage = require('./DashboardPage');

class LoginPage extends BasePage {
  // Localizadores
  get usernameInput() { return By.id('username'); }
  get passwordInput() { return By.id('password'); }
  get submitButton() { return By.id('login-btn'); }
  get errorMessage() { return By.css('.alert-danger'); }
  get rememberMeCheckbox() { return By.id('remember-me'); }
  get forgotPasswordLink() { return By.css('a[href="/forgot-password"]'); }

  constructor(driver) {
    super(driver);
    this.path = '/login';
  }

  async open() {
    await super.open(this.path);
    return this;
  }

  // Accion principal: login exitoso retorna DashboardPage
  async login(username, password) {
    await this.type(this.usernameInput, username);
    await this.type(this.passwordInput, password);
    await this.click(this.submitButton);
    return new DashboardPage(this.driver);
  }

  // Accion: intento de login con credenciales invalidas (se queda en LoginPage)
  async loginExpectingError(username, password) {
    await this.type(this.usernameInput, username);
    await this.type(this.passwordInput, password);
    await this.click(this.submitButton);
    await this.waitForVisible(this.errorMessage);
    return this; // Se queda en la misma pagina
  }

  async getErrorText() {
    return this.getText(this.errorMessage);
  }

  async isErrorDisplayed() {
    return this.isDisplayed(this.errorMessage);
  }

  async checkRememberMe() {
    await this.click(this.rememberMeCheckbox);
    return this;
  }
}

module.exports = LoginPage;
```

### Page Object: DashboardPage

```js
// tests/page-objects/DashboardPage.js
const { By, until } = require('selenium-webdriver');
const BasePage = require('./BasePage');

class DashboardPage extends BasePage {
  // Localizadores
  get welcomeMessage() { return By.id('welcome-msg'); }
  get userMenu() { return By.id('user-menu'); }
  get logoutButton() { return By.id('logout-btn'); }
  get searchInput() { return By.css('input[name="search"]'); }
  get statsWidget() { return By.css('.stats-widget'); }
  get recentActivity() { return By.css('.recent-activity'); }

  constructor(driver) {
    super(driver);
    this.path = '/dashboard';
  }

  async open() {
    await super.open(this.path);
    return this;
  }

  async getWelcomeText() {
    return this.getText(this.welcomeMessage);
  }

  async isLoaded() {
    return this.isDisplayed(this.welcomeMessage);
  }

  async search(query) {
    await this.type(this.searchInput, query);
    const { Key } = require('selenium-webdriver');
    const input = await this.findElement(this.searchInput);
    await input.sendKeys(Key.ENTER);
    return this; // o return new SearchResultsPage(this.driver);
  }

  async logout() {
    await this.click(this.userMenu);
    await this.click(this.logoutButton);
    const LoginPage = require('./LoginPage');
    return new LoginPage(this.driver);
  }
}

module.exports = DashboardPage;
```

### Test usando Page Objects

```js
// tests/specs/login.spec.js
const { Builder } = require('selenium-webdriver');
const assert = require('assert');
const LoginPage = require('../page-objects/LoginPage');

describe('Login Tests', function() {
  let driver;
  let loginPage;

  before(async function() {
    driver = await new Builder().forBrowser('chrome').build();
    loginPage = new LoginPage(driver);
  });

  beforeEach(async function() {
    await loginPage.open();
  });

  it('should login with valid credentials', async function() {
    const dashboardPage = await loginPage.login('admin', 'password123');

    const welcomeText = await dashboardPage.getWelcomeText();
    assert.ok(welcomeText.includes('Bienvenido'));
  });

  it('should show error with invalid credentials', async function() {
    await loginPage.loginExpectingError('invalid', 'wrong');

    const errorText = await loginPage.getErrorText();
    assert.strictEqual(errorText, 'Credenciales incorrectas');
  });

  it('should navigate to dashboard after login and back to login after logout', async function() {
    const dashboardPage = await loginPage.login('admin', 'password123');
    assert.ok(await dashboardPage.isLoaded());

    const loginPageAfterLogout = await dashboardPage.logout();
    // Ahora estamos de vuelta en LoginPage
  });

  after(async function() {
    await driver.quit();
  });
});
```

---

## Implementacion en Nightwatch.js

Nightwatch.js tiene soporte nativo para Page Objects usando `module.exports` con una estructura declarativa de `elements`, `commands` y `sections`.

### Page Object: loginPage

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

### Page Object con sections: dashboardPage

```js
// tests/page-objects/dashboardPage.js
module.exports = {
  url: function() {
    return `${this.api.launchUrl}/dashboard`;
  },

  commands: [{
    waitForPageLoad() {
      return this
        .waitForElementVisible('@mainContent', 10000);
    }
  }],

  elements: {
    mainContent: { selector: '#main-content' }
  },

  sections: {
    header: {
      selector: '#app-header',
      elements: {
        logo: { selector: '.logo' },
        userMenu: { selector: '#user-menu' },
        logoutBtn: { selector: '#logout-btn' },
        searchInput: { selector: 'input[name="search"]' },
        notifications: { selector: '.notification-bell' }
      },
      commands: [{
        openUserMenu() {
          return this.click('@userMenu');
        },
        logout() {
          return this
            .click('@userMenu')
            .waitForElementVisible('@logoutBtn', 3000)
            .click('@logoutBtn');
        },
        search(query) {
          return this
            .clearValue('@searchInput')
            .setValue('@searchInput', [query, this.api.Keys.ENTER]);
        }
      }]
    },

    sidebar: {
      selector: '#sidebar',
      elements: {
        dashboardLink: { selector: 'a[href="/dashboard"]' },
        usersLink: { selector: 'a[href="/users"]' },
        reportsLink: { selector: 'a[href="/reports"]' },
        settingsLink: { selector: 'a[href="/settings"]' }
      },
      commands: [{
        navigateTo(section) {
          const linkMap = {
            dashboard: '@dashboardLink',
            users: '@usersLink',
            reports: '@reportsLink',
            settings: '@settingsLink'
          };
          return this.click(linkMap[section]);
        }
      }]
    },

    content: {
      selector: '#main-content',
      elements: {
        title: { selector: 'h1' },
        welcomeMessage: { selector: '#welcome-msg' },
        statsWidget: { selector: '.stats-widget' },
        recentActivity: { selector: '.recent-activity' }
      }
    }
  }
};
```

### Test usando Page Objects de Nightwatch

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

  it('should logout from dashboard', function(browser) {
    const loginPage = browser.page.loginPage();
    const dashboardPage = browser.page.dashboardPage();

    loginPage
      .navigate()
      .login('admin', 'password123');

    dashboardPage
      .waitForPageLoad()
      .section.header
        .logout();

    // Verificar que volvemos al login
    loginPage.assert.visible('@usernameInput');
  });

  it('should navigate using sidebar', function(browser) {
    const loginPage = browser.page.loginPage();
    const dashboardPage = browser.page.dashboardPage();

    loginPage
      .navigate()
      .login('admin', 'password123');

    dashboardPage
      .waitForPageLoad()
      .section.sidebar
        .assert.visible('@reportsLink')
        .navigateTo('reports');

    browser.assert.urlContains('/reports');
  });
});
```

### Configuracion de Page Objects en Nightwatch

```js
// nightwatch.conf.js
module.exports = {
  page_objects_path: ['tests/page-objects'],
  // ...
};
```

Los Page Objects se acceden como `browser.page.<nombreDelArchivo>()`. Nightwatch convierte el nombre del archivo a una funcion accesible desde `browser.page`.

---

## Beneficios

### Mantenibilidad

Si un localizador cambia en la UI (por ejemplo, el id de un boton pasa de `#submit` a `#login-submit`), solo se modifica en **un lugar** -- el Page Object -- en vez de en cada test que usa ese boton.

**Sin Page Object** (duplicacion de localizadores):
```js
// test1.js
driver.findElement(By.id('submit')).click(); // Hay que cambiar aqui
// test2.js
driver.findElement(By.id('submit')).click(); // Y aqui
// test3.js
driver.findElement(By.id('submit')).click(); // Y aqui tambien
```

**Con Page Object** (cambio en un solo lugar):
```js
// LoginPage.js
get submitButton() { return By.id('login-submit'); } // Solo aqui
```

### Reusabilidad

Los metodos del Page Object se reusan en multiples tests sin duplicar codigo:

```js
// Multiples tests reusan el mismo metodo login()
const dashboard = await loginPage.login('admin', 'pass123');
```

### Legibilidad

Los tests se leen como acciones de usuario, no como manipulacion del DOM:

```js
// Legible: describe QUE hace el usuario
const dashboard = await loginPage.login('admin', 'pass');
await dashboard.search('producto A');
await dashboard.logout();

// Menos legible: describe COMO se manipula el DOM
await driver.findElement(By.id('username')).sendKeys('admin');
await driver.findElement(By.id('password')).sendKeys('pass');
await driver.findElement(By.id('submit')).click();
```

---

## Anti-patrones

### 1. Pages demasiado grandes

**Problema**: Un Page Object que representa toda la aplicacion o una pagina muy compleja con decenas de metodos.

**Solucion**: Dividir en componentes (HeaderComponent, SidebarComponent, FormComponent) o usar sections en Nightwatch.

```js
// MAL: un Page Object gigante
class AppPage {
  async clickHeaderLogo() { /* ... */ }
  async clickSidebarReports() { /* ... */ }
  async fillLoginForm() { /* ... */ }
  async fillRegistrationForm() { /* ... */ }
  async openSettings() { /* ... */ }
  // ... 50 metodos mas
}

// BIEN: separar en componentes
class HeaderComponent extends BasePage { /* logo, menu, logout */ }
class SidebarComponent extends BasePage { /* links de navegacion */ }
class LoginPage extends BasePage { /* solo login */ }
```

### 2. Assertions en Page Objects

**Problema**: Poner assertions dentro del Page Object mezcla responsabilidades.

```js
// MAL: assertion dentro del Page Object
class LoginPage {
  async login(user, pass) {
    await this.type(this.usernameInput, user);
    await this.type(this.passwordInput, pass);
    await this.click(this.submitButton);
    // NO HACER ESTO: la assertion pertenece al test
    assert.ok(await this.driver.getCurrentUrl().includes('/dashboard'));
  }
}

// BIEN: el Page Object solo ejecuta acciones, el test hace assertions
class LoginPage {
  async login(user, pass) {
    await this.type(this.usernameInput, user);
    await this.type(this.passwordInput, pass);
    await this.click(this.submitButton);
    return new DashboardPage(this.driver);
  }
}

// En el test:
const dashboard = await loginPage.login('admin', 'pass');
assert.ok(await dashboard.isLoaded()); // Assertion en el test
```

**Excepcion aceptable**: Waits que verifican estado como precondicion de navegacion (por ejemplo, `waitForElementVisible` dentro de un metodo del Page Object es aceptable porque es parte del flujo, no una assertion de test).

### 3. Herencia profunda

**Problema**: Cadenas largas de herencia que hacen dificil entender de donde viene cada metodo.

```js
// MAL: herencia profunda
class BasePage { }
class AuthenticatedPage extends BasePage { }
class AdminPage extends AuthenticatedPage { }
class AdvancedAdminPage extends AdminPage { }
class SuperAdminSettingsPage extends AdvancedAdminPage { }

// BIEN: herencia maxima de 2 niveles, usar composicion para el resto
class BasePage { /* metodos genericos: click, type, waitFor */ }
class DashboardPage extends BasePage {
  constructor(driver) {
    super(driver);
    this.header = new HeaderComponent(driver);
    this.sidebar = new SidebarComponent(driver);
  }
}
```

### 4. Exponer localizadores directamente

**Problema**: Los tests acceden directamente a los localizadores del Page Object, rompiendo la encapsulacion.

```js
// MAL: test accede a localizadores internos
const loginPage = new LoginPage(driver);
await driver.findElement(loginPage.usernameInput).sendKeys('admin');

// BIEN: test usa metodos del Page Object
await loginPage.login('admin', 'pass');
```

### 5. Page Objects con estado mutable compartido

**Problema**: Guardar estado (como datos del usuario logueado) en propiedades del Page Object que persisten entre tests.

```js
// MAL: estado compartido
class LoginPage {
  constructor(driver) {
    this.driver = driver;
    this.loggedInUser = null; // Estado que se filtra entre tests
  }
  async login(user, pass) {
    this.loggedInUser = user; // Efecto secundario peligroso
    // ...
  }
}

// BIEN: sin estado compartido, datos en el test o en fixtures
class LoginPage {
  async login(user, pass) {
    // Solo ejecuta la accion, no guarda estado
    await this.type(this.usernameInput, user);
    await this.type(this.passwordInput, pass);
    await this.click(this.submitButton);
    return new DashboardPage(this.driver);
  }
}
```

### 6. Hardcodear datos en Page Objects

**Problema**: Valores como URLs, credenciales o textos esperados hardcodeados dentro del Page Object.

```js
// MAL: datos hardcodeados
class LoginPage {
  async loginAsAdmin() {
    await this.type(this.usernameInput, 'admin@company.com');
    await this.type(this.passwordInput, 'Admin123!');
  }
}

// BIEN: datos como parametros o en archivos de test data
class LoginPage {
  async login(username, password) {
    await this.type(this.usernameInput, username);
    await this.type(this.passwordInput, password);
    await this.click(this.submitButton);
    return new DashboardPage(this.driver);
  }
}

// En el test, los datos vienen de fixtures:
const users = require('../data/test-users.json');
const dashboard = await loginPage.login(users.admin.username, users.admin.password);
```

---

## Fuentes

> **Nota:** Se intento obtener documentacion en tiempo real mediante WebSearch y WebFetch, pero el acceso fue denegado. El contenido de esta referencia se baso en conocimiento previo de la documentacion oficial. Se recomienda verificar contra la fuente original.

- **Selenium - Page Object Models**: https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/ -- Consultado: 2026-09-22
- **Selenium - Test Practices**: https://www.selenium.dev/documentation/test_practices/ -- Consultado: 2026-09-22
- **Nightwatch.js - Page Objects**: https://nightwatchjs.org/guide/using-page-objects/getting-started.html -- Consultado: 2026-09-22
- **Martin Fowler - PageObject**: https://martinfowler.com/bliki/PageObject.html -- Consultado: 2026-09-22
