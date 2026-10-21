# Postman y Newman - Referencia

> **El experto de producto es el skill `postman`.** Este archivo queda como referencia oficial de sintaxis (colecciones, `pm.*`, Newman, CI). Para APIs SR/AVR/PI, environments Refund y plantillas de coleccion, usar `skills/postman/`.

> Referencia basada en la documentacion oficial de Postman (learning.postman.com).
> Fecha de consulta: 2026-09-22.

## Tabla de contenidos

1. [Colecciones: estructura y organizacion](#colecciones-estructura-y-organizacion)
2. [Environments y variables](#environments-y-variables)
3. [Scripts: pre-request y test scripts](#scripts-pre-request-y-test-scripts)
4. [Assertions comunes](#assertions-comunes)
5. [Newman CLI](#newman-cli)
6. [Integracion con CI/CD](#integracion-con-cicd)

---

## Colecciones: estructura y organizacion

Una **coleccion** en Postman es un grupo organizado de requests de API. Funciona como contenedor principal para organizar, documentar y ejecutar tests de API.

### Estructura jerarquica

```
Collection (Mi API Tests)
├── Folder: Auth
│   ├── POST Login
│   ├── POST Register
│   └── POST Refresh Token
├── Folder: Users
│   ├── GET List Users
│   ├── GET Get User by ID
│   ├── POST Create User
│   ├── PUT Update User
│   └── DELETE Delete User
├── Folder: Products
│   ├── GET List Products
│   └── ...
└── Folder: Health
    └── GET Health Check
```

### Componentes de un request

| Componente | Descripcion |
|---|---|
| **Method** | GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD |
| **URL** | Endpoint completo, puede usar variables: `{{baseUrl}}/api/users` |
| **Headers** | Key-value pairs (Content-Type, Authorization, etc.) |
| **Body** | Cuerpo del request: raw (JSON, XML, text), form-data, x-www-form-urlencoded, binary, GraphQL |
| **Params** | Query parameters y path variables |
| **Auth** | Configuracion de autenticacion (Bearer Token, Basic Auth, OAuth 2.0, API Key, etc.) |
| **Pre-request Script** | JavaScript que se ejecuta ANTES de enviar el request |
| **Tests** | JavaScript que se ejecuta DESPUES de recibir la respuesta |

### Exportar coleccion (formato JSON)

Las colecciones se exportan como archivos JSON (Collection Format v2.1) para compartir o usar con Newman:

```bash
# Exportar desde Postman: Collection > Export > Collection v2.1
# El archivo resultante es un JSON con toda la estructura
```

Estructura simplificada del JSON exportado:

```json
{
  "info": {
    "name": "Mi API Tests",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "POST Login",
          "request": {
            "method": "POST",
            "header": [],
            "body": {
              "mode": "raw",
              "raw": "{\"username\": \"{{username}}\", \"password\": \"{{password}}\"}"
            },
            "url": {
              "raw": "{{baseUrl}}/api/auth/login"
            }
          },
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": ["pm.test('Status 200', function() { pm.response.to.have.status(200); });"]
              }
            }
          ]
        }
      ]
    }
  ]
}
```

---

## Environments y variables

Las variables permiten parametrizar requests para reutilizarlos en diferentes contextos (dev, staging, production).

### Tipos de variables (orden de precedencia, de mayor a menor)

| Tipo | Scope | Persistencia | Uso tipico |
|---|---|---|---|
| **Local (data)** | Request unico | Solo durante la ejecucion del script actual | Variables temporales dentro de scripts |
| **Environment** | Environment activo | Se guardan en el environment file | URLs base, credenciales por entorno |
| **Collection** | Coleccion | Se guardan en la coleccion | Valores compartidos dentro de una coleccion |
| **Global** | Workspace completo | Disponible en todas las colecciones | Valores universales (API keys de servicios externos) |

### Sintaxis de uso

En URLs, headers y body:
```
{{variableName}}
```

Ejemplos:
```
URL:    {{baseUrl}}/api/users/{{userId}}
Header: Authorization: Bearer {{authToken}}
Body:   { "email": "{{userEmail}}" }
```

### Manejo de variables en scripts

```js
// ========= OBTENER VARIABLES =========

// Obtener una variable (resuelve segun orden de precedencia)
const baseUrl = pm.variables.get('baseUrl');

// Obtener de un scope especifico
const envUrl = pm.environment.get('baseUrl');
const colVar = pm.collectionVariables.get('apiVersion');
const globalVar = pm.globals.get('apiKey');

// ========= ESTABLECER VARIABLES =========

// Variables de environment
pm.environment.set('authToken', 'eyJhbGciOiJIUzI1NiIs...');
pm.environment.set('userId', '12345');

// Variables de coleccion
pm.collectionVariables.set('lastCreatedId', responseData.id);

// Variables globales
pm.globals.set('sharedApiKey', 'key_abc123');

// Variables locales (solo disponibles en el request actual)
pm.variables.set('tempValue', 'solo para este request');

// ========= ELIMINAR VARIABLES =========

pm.environment.unset('authToken');
pm.collectionVariables.unset('lastCreatedId');
pm.globals.unset('sharedApiKey');
```

### Ejemplo de environment file

```json
{
  "name": "Staging",
  "values": [
    {
      "key": "baseUrl",
      "value": "https://staging-api.example.com",
      "enabled": true
    },
    {
      "key": "username",
      "value": "test_user",
      "enabled": true
    },
    {
      "key": "password",
      "value": "test_pass_123",
      "enabled": true
    }
  ]
}
```

---

## Scripts: pre-request y test scripts

Postman ejecuta scripts en dos momentos del ciclo de un request:

```
Pre-request Script --> Envio del Request --> Recepcion de Response --> Test Script
```

### Pre-request scripts

Se ejecutan **antes** de enviar el request. Utiles para generar datos dinamicos, tokens, o configurar variables.

```js
// Generar un timestamp
pm.environment.set('timestamp', new Date().toISOString());

// Generar un ID unico
pm.environment.set('uniqueId', pm.variables.replaceIn('{{$guid}}'));

// Generar un numero aleatorio
pm.environment.set('randomNumber', Math.floor(Math.random() * 1000));

// Generar datos dinamicos con variables built-in de Postman
// {{$randomFirstName}}, {{$randomLastName}}, {{$randomEmail}}, {{$guid}}, {{$timestamp}}

// Obtener un token antes del request (encadenar requests)
const loginRequest = {
  url: pm.environment.get('baseUrl') + '/api/auth/login',
  method: 'POST',
  header: { 'Content-Type': 'application/json' },
  body: {
    mode: 'raw',
    raw: JSON.stringify({
      username: pm.environment.get('username'),
      password: pm.environment.get('password')
    })
  }
};

pm.sendRequest(loginRequest, function(err, response) {
  if (!err) {
    const token = response.json().token;
    pm.environment.set('authToken', token);
  }
});
```

### Test scripts

Se ejecutan **despues** de recibir la respuesta. Se usan para validar la respuesta y extraer datos.

```js
// ========= ESTRUCTURA BASICA DE UN TEST =========

pm.test('Nombre descriptivo del test', function() {
  // Assertions aqui
});

// ========= VALIDAR STATUS CODE =========

pm.test('Respuesta exitosa (200)', function() {
  pm.response.to.have.status(200);
});

pm.test('Recurso creado (201)', function() {
  pm.response.to.have.status(201);
});

pm.test('Status code es 2xx', function() {
  pm.expect(pm.response.code).to.be.within(200, 299);
});

// ========= VALIDAR RESPONSE TIME =========

pm.test('Tiempo de respuesta menor a 500ms', function() {
  pm.expect(pm.response.responseTime).to.be.below(500);
});

// ========= VALIDAR HEADERS =========

pm.test('Content-Type es JSON', function() {
  pm.response.to.have.header('Content-Type');
  pm.expect(pm.response.headers.get('Content-Type')).to.include('application/json');
});

// ========= VALIDAR JSON BODY =========

pm.test('Body contiene los campos esperados', function() {
  const jsonData = pm.response.json();

  pm.expect(jsonData).to.have.property('id');
  pm.expect(jsonData).to.have.property('name');
  pm.expect(jsonData).to.have.property('email');
  pm.expect(jsonData.name).to.be.a('string');
  pm.expect(jsonData.id).to.be.a('number');
});

pm.test('Lista tiene elementos', function() {
  const jsonData = pm.response.json();
  pm.expect(jsonData.data).to.be.an('array').that.is.not.empty;
  pm.expect(jsonData.data.length).to.be.greaterThan(0);
});

// ========= VALIDAR SCHEMA (JSON Schema validation) =========

pm.test('Response cumple con el schema', function() {
  const schema = {
    type: 'object',
    required: ['id', 'name', 'email'],
    properties: {
      id: { type: 'number' },
      name: { type: 'string' },
      email: { type: 'string', format: 'email' }
    }
  };

  pm.response.to.have.jsonSchema(schema);
});

// ========= EXTRAER DATOS PARA SIGUIENTES REQUESTS =========

pm.test('Guardar token para proximos requests', function() {
  const jsonData = pm.response.json();
  pm.environment.set('authToken', jsonData.token);
  pm.environment.set('userId', jsonData.user.id);
});
```

### Objeto pm - Referencia rapida

| Propiedad/Metodo | Descripcion |
|---|---|
| `pm.response.json()` | Parsea el body como JSON |
| `pm.response.text()` | Body como string |
| `pm.response.code` | Status code numerico (200, 404, etc.) |
| `pm.response.status` | Status text ("OK", "Not Found", etc.) |
| `pm.response.responseTime` | Tiempo de respuesta en ms |
| `pm.response.headers` | Headers de la respuesta |
| `pm.response.to.have.status(code)` | Assertion de status code |
| `pm.response.to.have.header(name)` | Assertion de header presente |
| `pm.response.to.have.jsonSchema(schema)` | Validacion de JSON Schema |
| `pm.expect(value)` | Wrapper de Chai expect |
| `pm.test(name, fn)` | Define un test |
| `pm.sendRequest(options, callback)` | Envia un request adicional |
| `pm.environment.get(key)` | Obtiene variable de environment |
| `pm.environment.set(key, value)` | Establece variable de environment |
| `pm.variables.get(key)` | Obtiene variable (con precedencia) |
| `pm.info.requestName` | Nombre del request actual |
| `pm.info.iteration` | Numero de iteracion actual (en collection runs) |

---

## Assertions comunes

Resumen de las assertions mas usadas organizadas por categoria:

### Status code

```js
pm.response.to.have.status(200);
pm.response.to.have.status(201);
pm.response.to.have.status(204);
pm.response.to.have.status(400);
pm.response.to.have.status(401);
pm.response.to.have.status(404);
pm.response.to.have.status(500);

// Por rango
pm.expect(pm.response.code).to.be.oneOf([200, 201]);
pm.expect(pm.response.code).to.be.within(200, 299);
```

### Response time

```js
pm.expect(pm.response.responseTime).to.be.below(500);
pm.expect(pm.response.responseTime).to.be.below(2000);
```

### Headers

```js
pm.response.to.have.header('Content-Type');
pm.response.to.have.header('X-Request-Id');
pm.expect(pm.response.headers.get('Content-Type')).to.include('application/json');
pm.expect(pm.response.headers.get('Cache-Control')).to.equal('no-cache');
```

### JSON body

```js
const json = pm.response.json();

// Existencia de propiedades
pm.expect(json).to.have.property('data');
pm.expect(json).to.have.nested.property('data.user.name');

// Valores exactos
pm.expect(json.status).to.equal('success');
pm.expect(json.count).to.equal(10);

// Tipos
pm.expect(json.id).to.be.a('number');
pm.expect(json.name).to.be.a('string');
pm.expect(json.items).to.be.an('array');
pm.expect(json.metadata).to.be.an('object');
pm.expect(json.active).to.be.a('boolean');

// Arrays
pm.expect(json.items).to.have.lengthOf(5);
pm.expect(json.items).to.include('item1');
pm.expect(json.tags).to.be.an('array').that.is.not.empty;
pm.expect(json.results).to.have.lengthOf.at.least(1);

// Strings
pm.expect(json.email).to.include('@');
pm.expect(json.name).to.match(/^[A-Z]/);
pm.expect(json.description).to.not.be.empty;

// Null / undefined
pm.expect(json.deletedAt).to.be.null;
pm.expect(json.optionalField).to.not.be.undefined;

// Deep equality
pm.expect(json.address).to.deep.equal({
  street: '123 Main St',
  city: 'Springfield'
});
```

---

## Newman CLI

Newman es la herramienta de linea de comandos para ejecutar colecciones de Postman. Permite integrar tests de API en pipelines de CI/CD.

### Instalacion

```bash
# Instalacion global
npm install -g newman

# Instalacion como devDependency del proyecto
npm install --save-dev newman

# Instalar reporters adicionales
npm install -g newman-reporter-htmlextra
npm install -g newman-reporter-junitfull
```

### Ejecucion basica

```bash
# Ejecutar una coleccion exportada
newman run mi-coleccion.postman_collection.json

# Ejecutar con un environment
newman run mi-coleccion.postman_collection.json \
  -e staging.postman_environment.json

# Ejecutar con variables globales
newman run mi-coleccion.postman_collection.json \
  -e staging.postman_environment.json \
  -g globals.postman_globals.json

# Ejecutar solo un folder de la coleccion
newman run mi-coleccion.postman_collection.json \
  --folder "Auth"

# Ejecutar con multiples iteraciones
newman run mi-coleccion.postman_collection.json \
  -n 5

# Ejecutar con datos de un archivo CSV o JSON (data-driven testing)
newman run mi-coleccion.postman_collection.json \
  -d test-data.csv

# Sobreescribir variables via CLI
newman run mi-coleccion.postman_collection.json \
  --env-var "baseUrl=https://production-api.example.com" \
  --env-var "apiKey=key_prod_123"
```

### Reporters

```bash
# Reporter CLI (default -- muestra resultados en consola)
newman run coleccion.json -r cli

# Reporter JUnit (genera XML para CI)
newman run coleccion.json -r junit \
  --reporter-junit-export results/junit-report.xml

# Reporter HTML (usando newman-reporter-htmlextra)
newman run coleccion.json -r htmlextra \
  --reporter-htmlextra-export results/report.html

# Multiples reporters simultaneamente
newman run coleccion.json \
  -r cli,junit,htmlextra \
  --reporter-junit-export results/junit-report.xml \
  --reporter-htmlextra-export results/report.html

# Reporter JSON
newman run coleccion.json -r json \
  --reporter-json-export results/report.json
```

### Opciones avanzadas

```bash
# Timeout global (ms)
newman run coleccion.json --timeout 60000

# Timeout por request (ms)
newman run coleccion.json --timeout-request 10000

# Timeout de scripts (ms)
newman run coleccion.json --timeout-script 5000

# Ignorar certificados SSL invalidos
newman run coleccion.json --insecure

# Parar al primer error
newman run coleccion.json --bail

# Deshabilitar redirects automaticos
newman run coleccion.json --no-follow-redirects

# Color en output
newman run coleccion.json --color on

# Silencioso (sin output CLI)
newman run coleccion.json --silent

# Verbose (mas detalle)
newman run coleccion.json --verbose

# Delay entre requests (ms)
newman run coleccion.json --delay-request 500
```

### Uso programatico (Node.js)

```js
const newman = require('newman');

newman.run({
  collection: require('./coleccion.postman_collection.json'),
  environment: require('./staging.postman_environment.json'),
  reporters: ['cli', 'junit'],
  reporter: {
    junit: {
      export: './results/junit-report.xml'
    }
  },
  iterationCount: 1,
  bail: true,
  timeoutRequest: 10000
}, function(err, summary) {
  if (err) {
    console.error('Error ejecutando coleccion:', err);
    process.exit(1);
  }

  console.log('Ejecucion completada');
  console.log(`Total requests: ${summary.run.stats.requests.total}`);
  console.log(`Tests exitosos: ${summary.run.stats.assertions.total - summary.run.stats.assertions.failed}`);
  console.log(`Tests fallidos: ${summary.run.stats.assertions.failed}`);

  if (summary.run.stats.assertions.failed > 0) {
    process.exit(1);
  }
});
```

---

## Integracion con CI/CD

### Ejemplo en Azure DevOps Pipeline

```yaml
steps:
- task: NodeTool@0
  inputs:
    versionSpec: '18.x'
  displayName: 'Instalar Node.js'

- script: npm install -g newman newman-reporter-junitfull newman-reporter-htmlextra
  displayName: 'Instalar Newman y reporters'

- script: |
    newman run tests/api/coleccion.postman_collection.json \
      -e tests/api/$(environment).postman_environment.json \
      -r cli,junitfull,htmlextra \
      --reporter-junitfull-export $(Build.ArtifactStagingDirectory)/newman-results.xml \
      --reporter-htmlextra-export $(Build.ArtifactStagingDirectory)/newman-report.html \
      --bail
  displayName: 'Ejecutar tests de API con Newman'

- task: PublishTestResults@2
  inputs:
    testResultsFormat: 'JUnit'
    testResultsFiles: '$(Build.ArtifactStagingDirectory)/newman-results.xml'
  condition: always()
  displayName: 'Publicar resultados de tests'

- publish: $(Build.ArtifactStagingDirectory)/newman-report.html
  artifact: 'newman-report'
  condition: always()
  displayName: 'Publicar reporte HTML'
```

### Ejemplo en GitHub Actions

```yaml
- name: Install Newman
  run: npm install -g newman newman-reporter-htmlextra

- name: Run API Tests
  run: |
    newman run tests/api/coleccion.postman_collection.json \
      -e tests/api/staging.postman_environment.json \
      -r cli,htmlextra \
      --reporter-htmlextra-export results/report.html \
      --bail
```

### Ejemplo en package.json

```json
{
  "scripts": {
    "test:api": "newman run tests/api/coleccion.json -e tests/api/staging.env.json",
    "test:api:dev": "newman run tests/api/coleccion.json -e tests/api/dev.env.json",
    "test:api:ci": "newman run tests/api/coleccion.json -e tests/api/staging.env.json -r cli,junit --reporter-junit-export results/api-results.xml --bail"
  }
}
```

---

## Fuentes

> **Nota:** Se intento obtener documentacion en tiempo real mediante WebSearch y WebFetch, pero el acceso fue denegado. El contenido de esta referencia se baso en conocimiento previo de la documentacion oficial. Se recomienda verificar contra la fuente original.

- **Postman Learning Center**: https://learning.postman.com/docs/getting-started/overview/ -- Consultado: 2026-09-22
- **Postman Collections**: https://learning.postman.com/docs/collections/using-collections/ -- Consultado: 2026-09-22
- **Postman Variables**: https://learning.postman.com/docs/sending-requests/variables/variables/ -- Consultado: 2026-09-22
- **Postman Scripting Reference**: https://learning.postman.com/docs/tests-and-scripts/write-scripts/test-scripts/ -- Consultado: 2026-09-22
- **Postman pm API Reference**: https://learning.postman.com/docs/tests-and-scripts/write-scripts/postman-sandbox-api-reference/ -- Consultado: 2026-09-22
- **Newman Documentation**: https://learning.postman.com/docs/collections/using-newman-cli/command-line-integration-with-newman/ -- Consultado: 2026-09-22
- **Newman GitHub Repository**: https://github.com/postmanlabs/newman -- Consultado: 2026-09-22
