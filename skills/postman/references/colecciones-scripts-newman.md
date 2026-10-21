# Colecciones, scripts y Newman

Referencia operativa para QA. Sintaxis alineada a Postman Learning Center (consultado 2026-09-22). Detalle extendido: `skills/qa-automation/references/postman-newman.md`.

---

## 1. Estructura de colección Refund

```
Refund-{APP} (SR | AVR | PI | ROR)
├── 00-Health
├── 01-{Flujo de negocio}
│   ├── {METODO} {Nombre del contrato}
│   └── Tests + pre-request
└── 99-Negative
```

Un request = un contrato. Encadenar IDs con `pm.environment.set`, no hardcodear radicados de producción.

---

## 2. Variables y environments

Precedencia (mayor a menor): local → environment → collection → global.

| Variable | Uso |
|---|---|
| `{{baseUrl}}` | Host del swagger/APIM del ambiente |
| `{{subscriptionKey}}` | Header APIM si aplica (no verificado el nombre exacto) |
| `{{authToken}}` | Bearer si el endpoint lo exige |
| `{{refundRequest}}` | Radicado / station-ctl |
| `{{ticket}}` | Tiquete 13 dígitos |
| `{{pnr}}` | Reserva 6 caracteres |

Ambientes del equipo: **DEV, QA, PRE, POST**. Un archivo `.postman_environment.json` por ambiente.

Sintaxis:

```
{{baseUrl}}/api/v1/GetRefundRTS
Authorization: Bearer {{authToken}}
```

```js
pm.environment.set('refundRequest', json.refundRequest);
const ticket = pm.environment.get('ticket');
```

---

## 3. Scripts mínimos

Ciclo: Pre-request → Request → Response → Tests.

```js
pm.test('Status 2xx', function () {
  pm.expect(pm.response.code).to.be.within(200, 299);
});

pm.test('Content-Type JSON', function () {
  pm.expect(pm.response.headers.get('Content-Type')).to.include('application/json');
});

pm.test('Campos documentados presentes', function () {
  const json = pm.response.json();
  pm.expect(json).to.have.property('/* campo del manual */');
});
```

Negativos: `400`, `401`, `404` según el contrato. No afirmar un status no documentado.

Datos dinámicos: `{{$guid}}`, `{{$timestamp}}`, `{{$randomEmail}}`.

---

## 4. Newman

```bash
npm install -g newman newman-reporter-htmlextra newman-reporter-junitfull

newman run collections/refund-avr.postman_collection.json \
  -e env/qa.postman_environment.json \
  --folder "01-ConsultaReembolso" \
  -r cli,junitfull,htmlextra \
  --reporter-junitfull-export results/newman.xml \
  --reporter-htmlextra-export results/newman.html \
  --timeout-request 15000 \
  --bail
```

Data-driven: `newman run coleccion.json -d data/tickets.csv`.

CI: el YAML de Azure DevOps vive en `azure-devops`. Este skill entrega el `newman run` y los artefactos (JUnit + HTML). Publicar resultados con `PublishTestResults@2`.

---

## 5. Checklist de calidad de un request

- [ ] URL solo con host documentado o `{{baseUrl}}`
- [ ] Body solo con campos que aparecen en el manual
- [ ] Tests de status + campos clave
- [ ] Dato de prueba (tiquete 13 dígitos, prefijos SR: 134, 202, 133, 547)
- [ ] Query SQL de verificación si persiste (skill `db-relacional`)
- [ ] Sin secretos en texto plano

---

## Fuentes

- https://learning.postman.com/docs/collections/using-collections/
- https://learning.postman.com/docs/tests-and-scripts/write-scripts/test-scripts/
- https://learning.postman.com/docs/collections/using-newman-cli/command-line-integration-with-newman/
- Consultado: 2026-09-22
