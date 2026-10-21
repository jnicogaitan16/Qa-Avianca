# Plantilla de colección y caso de prueba API — Refund

Usar esta plantilla al generar entregables. Completar solo con datos verificados en `apis-refund.md` o en el manual.

---

## 1. Caso de prueba API (para copiar al Test Case / colección)

```markdown
### ID: API-{APP}-{NNN}
### Título: PBI-XXXXX #{n} {contrato} — {escenario}

| Campo | Valor |
|---|---|
| Aplicación | SR / AVR / PI / ROR |
| Ambiente | QA |
| Método + path | {solo si está en el manual o swagger} |
| Precondiciones | Solicitud existente / tiquete válido / rol |
| Datos | ticket, pnr, refund-request |

**Pasos**
1. Set environment QA (`baseUrl` del swagger del producto)
2. Ejecutar request {nombre}
3. Validar tests Postman
4. Verificar persistencia (query en skill db-relacional)

**Esperado:** status {n} + campos {lista del manual}
**Actual:** (ejecución)
```

---

## 2. Request Postman (esqueleto)

```json
{
  "name": "GET GetRefundRTS — consulta por document",
  "request": {
    "method": "GET",
    "header": [
      { "key": "Content-Type", "value": "application/json" },
      { "key": "Authorization", "value": "Bearer {{authToken}}" }
    ],
    "url": "{{baseUrlAvr}}/api/v1/GetRefundRTS"
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Status 2xx', function () {",
          "  pm.expect(pm.response.code).to.be.within(200, 299);",
          "});",
          "pm.test('Respuesta parseable', function () {",
          "  pm.response.json();",
          "});"
        ]
      }
    }
  ]
}
```

Ajustar method/body según swagger. GetRefundRTS acepta combinaciones Station+Control, Station+Control+Document, o Document.

---

## 3. Tests recomendados por tipo

| Tipo de API | Assertions |
|---|---|
| Consulta (GetRefundRTS, GetCurrencyList, Check Payment Status) | 2xx, array/objeto no vacío si hay data, campos de negocio del manual |
| Comando (SaveSupport, NTC, Emd, Update VF) | 2xx + query SQL de inserción/update |
| Negativo | tiquete inválido, request inexistente, archivo > 1 MB (SaveSupport) |

SaveSupport: fallar si se envía archivo > 1 MB o extensión no listada.

GetCurrencyList: cada ítem debe exponer `currency-code` (así lo consume SR VF).

---

## 4. Environment QA (mínimo)

```json
{
  "name": "Refund-QA",
  "values": [
    { "key": "baseUrlSr", "value": "https://azwappsprefbknduseqa.az-asev3-use-qa.appserviceenvironment.net", "enabled": true },
    { "key": "baseUrlAvr", "value": "https://azwappavrefsextsuseqa.az-asev3-use-qa.appserviceenvironment.net", "enabled": true },
    { "key": "baseUrlPi", "value": "https://azwapppiccustextsuseqa.az-asev3-use-qa.appserviceenvironment.net", "enabled": true },
    { "key": "baseUrlApim", "value": "https://api-avianca-qa.avtest.ink", "enabled": true },
    { "key": "authToken", "value": "", "enabled": true },
    { "key": "ticket", "value": "1341234567890", "enabled": true },
    { "key": "pnr", "value": "ABC123", "enabled": true },
    { "key": "refundRequest", "value": "", "enabled": true }
  ]
}
```

Hosts tomados de los manuales (QA). No inventar PRE/POST.

---

## 5. Newman del folder

```bash
newman run collections/refund-avr.postman_collection.json \
  -e env/refund-qa.postman_environment.json \
  --folder "01-ConsultaReembolso" \
  -r cli,htmlextra \
  --reporter-htmlextra-export results/avr-consulta.html
```

---

## 6. Cruce API + BD (obligatorio si persiste)

| Request | Query de verificación (origen: manuales) |
|---|---|
| EmdEndpoints | `SELECT * FROM Master.EMD_NUMBER` (SR) |
| SaveSupport | Blob `soportes-excepciones` + log de archivo |
| LoadMassive | `[rfd].[SP_REF_LOAD_MASSIVE_REQUEST]` |
| NTC SendGrid | `[rfd].[AVR_CONTROL_NOTIFICATIONS]` + templates |
| VF update PI→SR | `[rfd].[SR_MISSING_VALUE_REFUNDS_VF]` |
| Bank_Data_Information | `[rfd].[PIC_BANK_DATA_INFORMATION]` |

El SQL lo redacta `db-relacional`. Este skill solo nombra la tabla.
