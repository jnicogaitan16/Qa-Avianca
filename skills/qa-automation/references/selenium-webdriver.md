# Selenium WebDriver - Referencia

> Referencia basada en la documentacion oficial de Selenium (selenium.dev).
> Fecha de consulta: 2026-09-22.

## Tabla de contenidos

1. [Arquitectura y componentes](#arquitectura-y-componentes)
2. [Protocolo W3C WebDriver](#protocolo-w3c-webdriver)
3. [Localizadores](#localizadores)
4. [Waits (esperas)](#waits-esperas)
5. [Acciones principales](#acciones-principales)
6. [Manejo de alerts](#manejo-de-alerts)
7. [Manejo de frames e iframes](#manejo-de-frames-e-iframes)
8. [Manejo de ventanas y pestanas](#manejo-de-ventanas-y-pestanas)
9. [Configuracion del navegador](#configuracion-del-navegador)

---

## Arquitectura y componentes

Selenium WebDriver es una herramienta de automatizacion de navegadores que sigue una arquitectura cliente-servidor:

```
Test Script (cliente) --> WebDriver API --> Driver binario (chromedriver, geckodriver, etc.) --> Navegador
```

### Componentes principales

| Componente | Descripcion |
|---|---|
| **Selenium Client Library** | Bindings del lenguaje (JavaScript, Java, Python, C#, Ruby) que exponen la API de WebDriver |
| **WebDriver Protocol (W3C)** | Protocolo estandar basado en HTTP/JSON para comunicacion entre cliente y driver |
| **Browser Driver** | Ejecutable especifico del navegador que traduce comandos WebDriver a acciones nativas (chromedriver, geckodriver, msedgedriver) |
| **Selenium Manager** | Herramienta integrada desde Selenium 4.6 que descarga y configura automaticamente los drivers necesarios |
| **Selenium Grid** | Permite ejecutar tests en paralelo distribuyendo sesiones entre multiples nodos (maquinas/contenedores) |

### Diagrama de comunicacion

```
┌─────────────┐      HTTP/JSON       ┌──────────────┐      Comandos       ┌──────────┐
│ Test Script  │ ──────────────────> │ Browser       │ ──────────────────> │ Navegador │
│ (JS/Java/Py) │ <────────────────── │ Driver        │ <────────────────── │ (Chrome,  │
└─────────────┘    W3C WebDriver     └──────────────┘    nativos          │  Firefox) │
                    Protocol                                               └──────────┘
```

---

## Protocolo W3C WebDriver

Desde Selenium 4, WebDriver usa exclusivamente el **protocolo W3C WebDriver** (reemplazando el antiguo JSON Wire Protocol de Selenium 3). El protocolo esta definido como una recomendacion W3C y garantiza interoperabilidad entre navegadores.

### Caracteristicas del protocolo W3C

- **Basado en REST**: Los comandos se envian como requests HTTP (POST, GET, DELETE) a endpoints del driver.
- **Formato JSON**: Los cuerpos de request y response usan JSON.
- **Sesiones**: Cada interaccion comienza creando una sesion (`POST /session`) con `capabilities` que describen el navegador y opciones deseadas.
- **Capabilities estandarizadas**: `browserName`, `browserVersion`, `platformName`, `acceptInsecureCerts`, `pageLoadStrategy`, `proxy`, `timeouts`, `unhandledPromptBehavior`.

### Ejemplo de creacion de sesion (JavaScript)

```js
const { Builder } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');

const options = new chrome.Options();
options.addArguments('--headless');
options.addArguments('--no-sandbox');
options.addArguments('--disable-dev-shm-usage');

const driver = await new Builder()
  .forBrowser('chrome')
  .setChromeOptions(options)
  .build();
```

### Ejemplo en Java

```java
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

ChromeOptions options = new ChromeOptions();
options.addArguments("--headless");
WebDriver driver = new ChromeDriver(options);
```

---

## Localizadores

Los localizadores son estrategias para encontrar elementos en el DOM. Selenium ofrece las siguientes estrategias via la clase `By`:

### Estrategias disponibles

| Localizador | Descripcion | Ejemplo (JS) |
|---|---|---|
| `By.id('valor')` | Busca por atributo `id`. El mas rapido y confiable si el id es unico y estable | `driver.findElement(By.id('login-btn'))` |
| `By.css('selector')` | Busca por selector CSS. Flexible y recomendado como estrategia principal | `driver.findElement(By.css('.btn-primary'))` |
| `By.xpath('expresion')` | Busca por expresion XPath. Potente para navegacion compleja del DOM | `driver.findElement(By.xpath('//div[@data-testid="header"]'))` |
| `By.name('valor')` | Busca por atributo `name`. Util para formularios | `driver.findElement(By.name('username'))` |
| `By.className('valor')` | Busca por atributo `class` (una sola clase, no compuestas) | `driver.findElement(By.className('active'))` |
| `By.linkText('texto')` | Busca un `<a>` por su texto exacto visible | `driver.findElement(By.linkText('Sign In'))` |
| `By.partialLinkText('texto')` | Busca un `<a>` por coincidencia parcial del texto | `driver.findElement(By.partialLinkText('Sign'))` |
| `By.tagName('tag')` | Busca por nombre de etiqueta HTML | `driver.findElement(By.tagName('h1'))` |

### Prioridad recomendada de localizadores

1. **`By.id`** -- Si el elemento tiene un `id` unico y estable
2. **`By.css`** -- Para la mayoria de los casos; rapido y legible
3. **`By.xpath`** -- Cuando se necesita navegar relaciones padre/hijo o texto parcial
4. **`By.name`** -- Util en formularios
5. **`By.linkText` / `By.partialLinkText`** -- Solo para enlaces
6. **`By.className` / `By.tagName`** -- Poco especificos, usar con precaucion

### findElement vs findElements

```js
// Retorna el primer elemento encontrado. Lanza NoSuchElementError si no existe.
const element = await driver.findElement(By.css('.my-class'));

// Retorna un array de todos los elementos que coinciden. Array vacio si no hay coincidencias (no lanza error).
const elements = await driver.findElements(By.css('.list-item'));
console.log(`Se encontraron ${elements.length} elementos`);
```

### Relative locators (Selenium 4+)

Selenium 4 agrego localizadores relativos que permiten encontrar elementos en relacion espacial a otros:

```js
const { locateWith } = require('selenium-webdriver');

// Encontrar el input que esta debajo del label "Username"
const usernameLabel = await driver.findElement(By.css('label[for="username"]'));
const usernameInput = await driver.findElement(locateWith(By.tagName('input')).below(usernameLabel));

// Otros: above(), toLeftOf(), toRightOf(), near()
```

---

## Waits (esperas)

Las esperas son esenciales para manejar la naturaleza asincrona de las aplicaciones web. Selenium ofrece tres tipos de esperas.

### Implicit Wait

Configura un tiempo global de espera para `findElement`. Si el elemento no esta disponible inmediatamente, el driver reintentara durante el tiempo configurado antes de lanzar un error.

```js
// Configurar implicit wait de 10 segundos (aplica a todos los findElement)
await driver.manage().setTimeouts({ implicit: 10000 });

// A partir de aqui, todos los findElement esperaran hasta 10 segundos
const element = await driver.findElement(By.id('dynamic-element'));
```

**Advertencia**: No mezclar implicit waits con explicit waits -- puede causar tiempos de espera impredecibles.

### Explicit Wait (WebDriverWait + ExpectedConditions)

Espera hasta que una condicion especifica se cumpla o se agote el timeout. Es la estrategia **recomendada** porque es precisa y explicita.

```js
const { until } = require('selenium-webdriver');

const driver = await new Builder().forBrowser('chrome').build();

// Esperar hasta que un elemento sea visible (maximo 10 segundos)
const element = await driver.wait(
  until.elementLocated(By.id('results')),
  10000,
  'El elemento #results no aparecio en 10 segundos'
);

// Esperar hasta que el elemento sea visible en pantalla
await driver.wait(until.elementIsVisible(element), 5000);

// Esperar hasta que el titulo de la pagina contenga un texto
await driver.wait(until.titleContains('Dashboard'), 5000);

// Esperar hasta que una URL contenga un patron
await driver.wait(until.urlContains('/dashboard'), 5000);

// Esperar hasta que un elemento sea clickeable
await driver.wait(until.elementIsEnabled(element), 5000);
```

### ExpectedConditions comunes (modulo `until` en JS)

| Condicion | Descripcion |
|---|---|
| `until.elementLocated(locator)` | El elemento existe en el DOM |
| `until.elementIsVisible(element)` | El elemento es visible (displayed) |
| `until.elementIsNotVisible(element)` | El elemento deja de ser visible |
| `until.elementIsEnabled(element)` | El elemento esta habilitado (no disabled) |
| `until.elementIsDisabled(element)` | El elemento esta deshabilitado |
| `until.titleIs(title)` | El titulo de la pagina es exactamente `title` |
| `until.titleContains(text)` | El titulo contiene `text` |
| `until.urlIs(url)` | La URL es exactamente `url` |
| `until.urlContains(text)` | La URL contiene `text` |
| `until.alertIsPresent()` | Hay un alert/confirm/prompt visible |
| `until.stalenessOf(element)` | El elemento ya no esta attached al DOM |
| `until.elementsLocated(locator)` | Al menos un elemento coincide con el locator |

### Explicit Wait en Java

```java
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import java.time.Duration;

WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

// Esperar hasta que el elemento sea clickeable
WebElement element = wait.until(
    ExpectedConditions.elementToBeClickable(By.id("submit-btn"))
);
element.click();
```

### Fluent Wait

Es una variante de explicit wait que permite configurar el intervalo de polling y las excepciones a ignorar durante la espera.

```java
import org.openqa.selenium.support.ui.FluentWait;

Wait<WebDriver> fluentWait = new FluentWait<>(driver)
    .withTimeout(Duration.ofSeconds(30))
    .pollingEvery(Duration.ofMillis(500))
    .ignoring(NoSuchElementException.class)
    .ignoring(StaleElementReferenceException.class);

WebElement element = fluentWait.until(d -> d.findElement(By.id("dynamic-content")));
```

En JavaScript, el `driver.wait()` ya actua como un fluent wait con configuracion de polling:

```js
// Condicion personalizada con polling implicito
const element = await driver.wait(async function() {
  const el = await driver.findElement(By.id('status'));
  const text = await el.getText();
  return text === 'Complete' ? el : false;
}, 15000, 'El estado no cambio a Complete');
```

### Comparacion de waits

| Tipo | Scope | Granularidad | Recomendado |
|---|---|---|---|
| **Implicit** | Global (toda la sesion) | Baja -- aplica a todos los findElement | No como estrategia principal |
| **Explicit** | Por operacion | Alta -- condicion especifica | Si -- estrategia principal |
| **Fluent** | Por operacion | Alta -- con control de polling e ignorar excepciones | Si -- para escenarios avanzados |

---

## Acciones principales

### Interaccion con elementos

```js
// Click en un elemento
const button = await driver.findElement(By.id('submit'));
await button.click();

// Escribir texto en un campo
const input = await driver.findElement(By.name('username'));
await input.sendKeys('mi_usuario');

// Limpiar un campo antes de escribir
await input.clear();
await input.sendKeys('nuevo_valor');

// Obtener el texto visible de un elemento
const heading = await driver.findElement(By.tagName('h1'));
const text = await heading.getText();
console.log(text); // "Bienvenido"

// Obtener el valor de un atributo
const link = await driver.findElement(By.css('a.nav-link'));
const href = await link.getAttribute('href');
console.log(href); // "https://example.com/dashboard"

// Obtener una propiedad CSS
const color = await link.getCssValue('color');

// Verificar si un elemento esta visible
const isDisplayed = await button.isDisplayed();

// Verificar si un elemento esta habilitado
const isEnabled = await button.isEnabled();

// Verificar si un checkbox/radio esta seleccionado
const checkbox = await driver.findElement(By.id('terms'));
const isSelected = await checkbox.isSelected();

// Submit de un formulario
const form = await driver.findElement(By.id('login-form'));
await form.submit();
```

### Navegacion

```js
// Navegar a una URL
await driver.get('https://example.com');

// Equivalente usando navigate()
await driver.navigate().to('https://example.com');

// Navegar hacia atras
await driver.navigate().back();

// Navegar hacia adelante
await driver.navigate().forward();

// Refrescar la pagina
await driver.navigate().refresh();

// Obtener la URL actual
const currentUrl = await driver.getCurrentUrl();

// Obtener el titulo de la pagina
const title = await driver.getTitle();

// Obtener el page source
const source = await driver.getPageSource();
```

### Actions API (interacciones avanzadas)

Para interacciones complejas como drag & drop, hover, o combinaciones de teclas, se usa la Actions API:

```js
const { Key } = require('selenium-webdriver');

const actions = driver.actions({ async: true });

// Hover sobre un elemento
const menu = await driver.findElement(By.id('dropdown-menu'));
await actions.move({ origin: menu }).perform();

// Double click
await actions.doubleClick(element).perform();

// Right click (context click)
await actions.contextClick(element).perform();

// Drag and drop
const source = await driver.findElement(By.id('draggable'));
const target = await driver.findElement(By.id('droppable'));
await actions.dragAndDrop(source, target).perform();

// Combinacion de teclas (Ctrl+A, Ctrl+C)
await actions
  .keyDown(Key.CONTROL)
  .sendKeys('a')
  .keyUp(Key.CONTROL)
  .perform();

// Scroll a un elemento
await actions.scroll(0, 0, 0, 500, { origin: element }).perform();
```

---

## Manejo de alerts

Los alerts de JavaScript (`alert()`, `confirm()`, `prompt()`) se manejan con `switchTo().alert()`:

```js
// Esperar a que aparezca el alert
await driver.wait(until.alertIsPresent(), 5000);

// Cambiar el contexto al alert
const alert = await driver.switchTo().alert();

// Obtener el texto del alert
const alertText = await alert.getText();
console.log(alertText);

// Aceptar el alert (boton OK / Aceptar)
await alert.accept();

// Rechazar el alert (boton Cancelar -- para confirm/prompt)
await alert.dismiss();

// Escribir texto en un prompt
await alert.sendKeys('Mi respuesta');
await alert.accept();
```

### Ejemplo completo de manejo de confirm

```js
// Click que dispara un confirm()
await driver.findElement(By.id('delete-btn')).click();

// Manejar el confirm
const confirm = await driver.switchTo().alert();
const message = await confirm.getText();
console.log(`Confirm dice: ${message}`);

// Aceptar o rechazar segun la logica del test
await confirm.accept(); // o confirm.dismiss()
```

---

## Manejo de frames e iframes

Para interactuar con elementos dentro de un `<frame>` o `<iframe>`, se debe cambiar el contexto del driver:

```js
// Cambiar a un frame por indice (0-based)
await driver.switchTo().frame(0);

// Cambiar a un frame por nombre o id
await driver.switchTo().frame('frame-name');

// Cambiar a un frame usando un WebElement
const iframeElement = await driver.findElement(By.css('iframe#my-iframe'));
await driver.switchTo().frame(iframeElement);

// Interactuar con elementos dentro del frame
const innerButton = await driver.findElement(By.id('inner-button'));
await innerButton.click();

// Volver al frame padre (un nivel arriba)
await driver.switchTo().parentFrame();

// Volver al contexto principal (top-level)
await driver.switchTo().defaultContent();
```

### Patron recomendado para frames

```js
// Siempre volver al contexto principal antes de cambiar a otro frame
await driver.switchTo().defaultContent();
await driver.switchTo().frame('otro-frame');

// Interactuar...

// Al terminar, volver al contexto principal
await driver.switchTo().defaultContent();
```

---

## Manejo de ventanas y pestanas

```js
// Obtener el handle de la ventana actual
const originalWindow = await driver.getWindowHandle();

// Obtener todos los handles abiertos
const allWindows = await driver.getAllWindowHandles();

// Abrir una nueva pestana
await driver.switchTo().newWindow('tab');

// Abrir una nueva ventana
await driver.switchTo().newWindow('window');

// Cambiar a otra ventana/pestana por handle
for (const handle of allWindows) {
  if (handle !== originalWindow) {
    await driver.switchTo().window(handle);
    break;
  }
}

// Cerrar la pestana/ventana actual
await driver.close();

// Volver a la ventana original
await driver.switchTo().window(originalWindow);

// Maximizar ventana
await driver.manage().window().maximize();

// Establecer tamano de ventana
await driver.manage().window().setRect({ width: 1280, height: 720 });

// Obtener tamano de ventana
const rect = await driver.manage().window().getRect();
console.log(`${rect.width}x${rect.height}`);
```

### Ejemplo: manejar popup que abre nueva ventana

```js
const originalWindow = await driver.getWindowHandle();
const windowsBefore = await driver.getAllWindowHandles();

// Click que abre nueva ventana
await driver.findElement(By.id('open-popup')).click();

// Esperar a que aparezca la nueva ventana
await driver.wait(async () => {
  const handles = await driver.getAllWindowHandles();
  return handles.length > windowsBefore.length;
}, 10000);

// Cambiar a la nueva ventana
const allHandles = await driver.getAllWindowHandles();
const newWindow = allHandles.find(h => !windowsBefore.includes(h));
await driver.switchTo().window(newWindow);

// Interactuar con la nueva ventana...
const popupTitle = await driver.getTitle();
console.log(`Popup title: ${popupTitle}`);

// Cerrar popup y volver a la original
await driver.close();
await driver.switchTo().window(originalWindow);
```

---

## Configuracion del navegador

### Screenshots

```js
// Captura de pantalla completa
const screenshot = await driver.takeScreenshot();
const fs = require('fs');
fs.writeFileSync('screenshot.png', screenshot, 'base64');

// Captura de un elemento especifico
const element = await driver.findElement(By.id('chart'));
const elementScreenshot = await element.takeScreenshot();
fs.writeFileSync('element.png', elementScreenshot, 'base64');
```

### Manejo de cookies

```js
// Agregar una cookie
await driver.manage().addCookie({ name: 'session', value: 'abc123' });

// Obtener una cookie
const cookie = await driver.manage().getCookie('session');

// Obtener todas las cookies
const allCookies = await driver.manage().getCookies();

// Eliminar una cookie
await driver.manage().deleteCookie('session');

// Eliminar todas las cookies
await driver.manage().deleteAllCookies();
```

### Ejecutar JavaScript

```js
// Ejecutar script sincrono
const result = await driver.executeScript('return document.title;');

// Ejecutar script con argumentos (los elementos WebElement se pasan correctamente)
const element = await driver.findElement(By.id('my-element'));
await driver.executeScript('arguments[0].scrollIntoView(true);', element);

// Ejecutar script asincrono
await driver.executeAsyncScript(`
  const callback = arguments[arguments.length - 1];
  setTimeout(() => callback('done'), 2000);
`);
```

### Cerrar el driver

```js
// Cerrar la ventana actual
await driver.close();

// Cerrar el navegador y terminar la sesion (siempre llamar al final)
await driver.quit();
```

---

## Fuentes

> **Nota:** Se intento obtener documentacion en tiempo real mediante WebSearch y WebFetch, pero el acceso fue denegado. El contenido de esta referencia se baso en conocimiento previo de la documentacion oficial. Se recomienda verificar contra la fuente original.

- **Selenium WebDriver Documentation**: https://www.selenium.dev/documentation/webdriver/ -- Consultado: 2026-09-22
- **W3C WebDriver Specification**: https://www.w3.org/TR/webdriver2/ -- Consultado: 2026-09-22
- **Selenium WebDriver - Locating Elements**: https://www.selenium.dev/documentation/webdriver/elements/locators/ -- Consultado: 2026-09-22
- **Selenium WebDriver - Waits**: https://www.selenium.dev/documentation/webdriver/waits/ -- Consultado: 2026-09-22
- **Selenium WebDriver - Interactions**: https://www.selenium.dev/documentation/webdriver/interactions/ -- Consultado: 2026-09-22
- **Selenium WebDriver - Actions API**: https://www.selenium.dev/documentation/webdriver/actions_api/ -- Consultado: 2026-09-22
- **Selenium WebDriver - Alerts**: https://www.selenium.dev/documentation/webdriver/interactions/alerts/ -- Consultado: 2026-09-22
- **Selenium WebDriver - Frames**: https://www.selenium.dev/documentation/webdriver/interactions/frames/ -- Consultado: 2026-09-22
- **Selenium WebDriver - Windows**: https://www.selenium.dev/documentation/webdriver/interactions/windows/ -- Consultado: 2026-09-22
