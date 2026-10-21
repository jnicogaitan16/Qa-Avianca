# language: es
# Naming Azure DevOps: PBI-XXXXX #TC <titulo> | Application Name: SR
# Disparador: UI. Cierre: sql/verificacion-vf.sql
# Fuente: manual-aplicacion-sr.md §7.2.4–7.2.4.4; manual-aplicacion-avr.md §10.4.2–10.4.3

Feature: Valores Faltantes SR a PI y notificación AVR

  # El manual no nombra el rol de quien radica (campo "Usuario que radica", precargado).
  # No usar roles "QA" ni "Analista": no están en este módulo.

  Scenario: PBI-XXXXX #TC01 Radicar VF con FOP KR
    Given el usuario autenticado abre Procesos >> Formulario Captura Reembolsos Faltantes
    When ingresa número de solicitud alfanumérico de máximo 32 caracteres
    And ingresa tiquete de 13 dígitos que inicia por 134, 202, 133 o 547
    And da clic en Validar
    Then el sistema consulta Consut_refund y precarga nombre, apellido y correo si existen
    When completa los mandatorios:
      | Campo              | Regla                                      |
      | PNR                | 6 caracteres                               |
      | IATA               | 8 dígitos                                  |
      | Canal de Solicitud | [master].[MST_CHANNEL]                     |
      | Moneda             | currency-code de PI /api/GetCurrencyList   |
      | Valor faltante     | decimal, punto, 2 decimales, <= Total venta|
      | Total de la venta  | decimal, punto, 2 decimales                |
      | Fecha de Venta     | mandatoria, formato fecha corta YYYY-MM-DD |
      | Forma de Pago      | KR (MVR_FOP_LIST)                          |
      | Programa Avianca   | mandatorio si KR (MVR_CPG_FILTER_LIST)     |
      | Razón del faltante | [master].[MST_MISSING_REASONS]             |
    And da clic en Guardar
    Then existen filas en [rfd].[SR_MISSING_VALUE_REFUNDS_VF] y [rfd].[SR_MISSING_VALUE_REFUND_STATUS_LOG_VF]
    And STATUS es Pendiente de Autorización
    # ⚠️ El texto exacto del toast de Guardar no está en el manual

  Scenario: PBI-XXXXX #TC02 Rechazar valor faltante mayor al Total de la venta
    Given el formulario VF está listo para Guardar
    When Valor faltante es mayor que Total de la venta
    Then el sistema no debe persistir el caso
    # Regla: "este campo no debe ser mayor al Total de la venta"

  Scenario: PBI-XXXXX #TC03 Coordinador aprueba todos los TKT (<= 3500 USD) y envía a PI
    Given una solicitud VF con 2 tiquetes en Pendiente de Autorización
    And el valor faltante convertido a USD es de 0 a 3500 según [rfd].[SR_EXCHANGE_RATES] y [master].[MST_APPROVAL_RANGE]
    And el usuario tiene rol Coordinador
    When consulta por número + tiquete o con Buscar todas
    And da clic en Validar y luego en Aprobar en el primer tiquete
    And confirma "¿Está seguro de aprobar este reembolso faltante?"
    Then ve "El reembolso faltante se aprobó correctamente"
    And STATUS del primer TKT es Autorizado y APPROVAL_DATE está poblado
    And no hay filas nuevas de esa solicitud en [rfd].[PIC_PAYMENT_REQUEST_VF]
    When aprueba el segundo tiquete
    Then se envía a PI
    And STATUS en SR es el literal persistido (ver calibración En progreso vs En proceso)
    And existen filas en [rfd].[PIC_PAYMENT_REQUEST_VF] y [rfd].[PIC_PAYMENT_DETAIL_VF]

  Scenario: PBI-XXXXX #TC04 Coordinador no aprueba monto mayor a 3500 USD
    Given valor faltante convertido a USD es mayor de 3500
    And el usuario tiene rol Coordinador
    When intenta aprobar
    Then no debe completar la aprobación de Gerente
    # Umbral documentado; el mensaje de UI no está citado

  Scenario: PBI-XXXXX #TC05 Rechazar VF
    Given una solicitud VF en Pendiente de Autorización
    And el usuario tiene rol Coordinador o Gerente
    When usa Buscar todas, localiza el caso y da clic en Rechazar
    Then STATUS es REJECTED y APPROVAL_DATE está poblado
    And hay traza en [rfd].[SR_MISSING_VALUE_REFUND_STATUS_LOG_VF]

  Scenario Outline: PBI-XXXXX #TC06 Pago PI y NTC AVR
    Given la solicitud VF ya fue enviada a PI
    When PI deja estado final P y FOP <fop> en [rfd].[PIC_PAYMENT_REQUEST_VF] y [rfd].[PIC_PAYMENT_DETAIL_VF]
    Then PI notifica a SR por MissingValueRefundStatus/Update
    And STATUS en [rfd].[SR_MISSING_VALUE_REFUNDS_VF] es Pagado
    And AVR emite <ntc> con asunto <asunto_es>
    And [rfd].[AVR_CONTROL_NOTIFICATIONS] se puede cruzar a NTC vía TEMPLATE_ID y NOTIF_TYPE_CODE
    # Disparador: pago en PI (UI/proceso). NTC por API solo si {{sendgridPath}} está definido.

    Examples:
      | fop | ntc   | asunto_es                                                              |
      | KR  | NTC23 | [Importante] Tu solicitud de reembolso fue pagado en un avianca credits. |
      | NC  | NTC24 | [Importante] Tu solicitud de reembolso fue pagado en una nota de crédito - ACM |

  Scenario: PBI-XXXXX #TC07 Fallo de envío a PI
    Given todos los TKT de la solicitud están Autorizado
    When el envío automático a PI falla
    Then STATUS vuelve a Pendiente de Autorización
