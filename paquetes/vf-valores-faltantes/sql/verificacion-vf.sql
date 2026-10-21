-- Verificación VF — solo columnas/tablas citadas en los manuales.
-- Cierre de paso UI. Sustituir @solicitud / @tiquete / @moneda.
-- NO usar LANG_CODE, SEND_DATE, AVR_CONTROL_NOTIFICATIONS.REFUND_REQUEST.

/* ========== Post-radicación (después de Guardar en UI) ========== */
SELECT STATUS, APPROVAL_DATE
FROM [rfd].[SR_MISSING_VALUE_REFUNDS_VF]
WHERE /* número de solicitud + tiquete de la prueba */;
-- Esperado: STATUS = 'Pendiente de Autorización' (listado §7.2.4.4; en relato también 'Pendiente de autorización')
-- APPROVAL_DATE: el manual no dice el valor al radicar. No afirmar NULL.

SELECT *
FROM [rfd].[SR_MISSING_VALUE_REFUND_STATUS_LOG_VF]
WHERE /* misma clave */;
-- Esperado: al menos un registro de alta. Columnas del log no listadas.

SELECT parameter_code, *
FROM [master].[MST_PARAMETERS]
WHERE parameter_code IN (
  'MVR_FOP_LIST',
  'MVR_CPG_FILTER_LIST',
  'MVR_FINAL_STATUSES',
  'MVR_SEND_FAILED_STATUS',
  'MVR_PIC_SEND_SUCCESS_STATUS'
);

/* ========== Precondición umbral (antes de aprobar) ========== */
SELECT *
FROM [master].[MST_APPROVAL_RANGE];
-- Coordinador 0-3500 USD; Gerente > 3500 USD

SELECT *
FROM [rfd].[SR_EXCHANGE_RATES]
WHERE /* moneda del caso */;

/* ========== Post-aprobación primer TKT (aún hay hermanos) ========== */
SELECT STATUS, APPROVAL_DATE
FROM [rfd].[SR_MISSING_VALUE_REFUNDS_VF]
WHERE /* solicitud + tiquete 1 */;
-- Esperado: STATUS = 'Autorizado', APPROVAL_DATE poblado
-- Esperado: SIN fila nueva de esta solicitud en PIC_PAYMENT_REQUEST_VF

SELECT *
FROM [rfd].[PIC_PAYMENT_REQUEST_VF]
WHERE /* solicitud */;

/* ========== Post-aprobación último TKT (envío a PI) ========== */
SELECT STATUS, APPROVAL_DATE
FROM [rfd].[SR_MISSING_VALUE_REFUNDS_VF]
WHERE /* solicitud */;
-- CONTRADICCIÓN documental: listado §7.2.4.4 = 'En progreso'; relato §7.2.4.2.1 = 'En proceso'.
-- Anotar el literal real de BD.

SELECT *
FROM [rfd].[PIC_PAYMENT_REQUEST_VF]
WHERE /* solicitud */;

SELECT *
FROM [rfd].[PIC_PAYMENT_DETAIL_VF]
WHERE /* solicitud */;
-- Esperado: existen filas en ambas.

/* ========== Post-rechazo ========== */
SELECT STATUS, APPROVAL_DATE
FROM [rfd].[SR_MISSING_VALUE_REFUNDS_VF]
WHERE /* solicitud */;
-- Esperado: STATUS = 'REJECTED', APPROVAL_DATE poblado

SELECT *
FROM [rfd].[SR_MISSING_VALUE_REFUND_STATUS_LOG_VF]
WHERE /* misma clave */;

/* ========== Post-pago PI + NTC ========== */
SELECT *
FROM [rfd].[PIC_PAYMENT_REQUEST_VF]
WHERE /* solicitud */;
-- Esperado: estado final P (Pagado) y FOP KR o NC

SELECT *
FROM [rfd].[PIC_PAYMENT_DETAIL_VF]
WHERE /* solicitud */;

SELECT STATUS
FROM [rfd].[SR_MISSING_VALUE_REFUNDS_VF]
WHERE /* solicitud */;
-- Esperado: Pagado

-- Join documentado. Filtrar solo por tipo NTC. Revisar el result set a mano.
SELECT TYP.NOTIF_TYPE_CODE, TYP.NOTIF_TYPE_NAME, NOTIF.*
FROM [rfd].[AVR_CONTROL_NOTIFICATIONS] NOTIF
JOIN [az-sqla-avref-use-qa].[rfd].[AVR_TEMPLATE_CONFIGURATION] CONF
  ON NOTIF.TEMPLATE_ID = CONF.TEMPLATE_ID
JOIN [az-sqla-avref-use-qa].[rfd].[AVR_TYPE_OF_NOTIFICATIONS] TYP
  ON CONF.[NOTIF_TYPE_CODE] = TYP.[NOTIF_TYPE_CODE]
WHERE TYP.NOTIF_TYPE_CODE IN ('NTC23', 'NTC24');
-- Esperado: aparece NTC23 si FOP=KR, NTC24 si FOP=NC (asuntos en AVR_SUBJECT_TABLE).

/* ========== Fallo envío SR → PI ========== */
SELECT STATUS
FROM [rfd].[SR_MISSING_VALUE_REFUNDS_VF]
WHERE /* solicitud */;
-- Esperado: Pendiente de Autorización
