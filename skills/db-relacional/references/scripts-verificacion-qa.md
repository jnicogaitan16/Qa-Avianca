# Scripts de verificación por flujo

Cada bloque es un **paso de Test Case**. Sustituir variables. No ejecutar `UPDATE`/`DELETE`.

---

## 1. VF — radicación en SR

**Acción:** Guardar formulario Procesos >> Formulario Captura Reembolsos Faltantes.

```sql
SELECT *
FROM [rfd].[SR_MISSING_VALUE_REFUNDS_VF]
-- filtrar por número de solicitud / tiquete de la prueba
;

SELECT *
FROM [rfd].[SR_MISSING_VALUE_REFUND_STATUS_LOG_VF]
-- misma clave; debe existir traza de alta
;
```

**Esperado:** `STATUS` = Pendiente de autorización.

---

## 2. VF — aprobación / rechazo

**Aprobar** (rol Coordinador ≤ 3500 USD o Gerente > 3500; TRM en `SR_EXCHANGE_RATES` + `MST_APPROVAL_RANGE`):

```sql
SELECT STATUS, APPROVAL_DATE
FROM [rfd].[SR_MISSING_VALUE_REFUNDS_VF]
WHERE /* solicitud */;
```

**Esperado:** `STATUS` = Autorizado; `APPROVAL_DATE` poblado. Si hay TKT hermanos pendientes, **no** debe existir aún fila nueva de pago en PI.

**Cuando no quedan TKT pendientes:**

```sql
SELECT *
FROM [rfd].[PIC_PAYMENT_REQUEST_VF]
WHERE /* solicitud */;

SELECT *
FROM [rfd].[PIC_PAYMENT_DETAIL_VF]
WHERE /* solicitud */;
```

**Esperado:** SR en **En progreso**; filas en PI VF.

**Rechazar:**

```sql
SELECT STATUS, APPROVAL_DATE
FROM [rfd].[SR_MISSING_VALUE_REFUNDS_VF]
WHERE /* solicitud */;
```

**Esperado:** `STATUS` = `REJECTED`.

---

## 3. VF — PI pagó y avisó a SR + NTC

```sql
-- PI
SELECT *
FROM [rfd].[PIC_PAYMENT_REQUEST_VF]
WHERE /* solicitud */;  -- estado P

-- SR
SELECT STATUS
FROM [rfd].[SR_MISSING_VALUE_REFUNDS_VF]
WHERE /* solicitud */;  -- Pagado

-- AVR notificación (NTC23 KR / NTC24 NC)
-- Solo columnas/joins citados en el manual. No filtrar por REFUND_REQUEST,
-- LANG_CODE ni SEND_DATE: esos nombres no están documentados.
SELECT TYP.NOTIF_TYPE_CODE, TYP.NOTIF_TYPE_NAME, NOTIF.*
FROM [rfd].[AVR_CONTROL_NOTIFICATIONS] NOTIF
JOIN [az-sqla-avref-use-qa].[rfd].[AVR_TEMPLATE_CONFIGURATION] CONF
  ON NOTIF.TEMPLATE_ID = CONF.TEMPLATE_ID
JOIN [az-sqla-avref-use-qa].[rfd].[AVR_TYPE_OF_NOTIFICATIONS] TYP
  ON CONF.[NOTIF_TYPE_CODE] = TYP.[NOTIF_TYPE_CODE]
WHERE TYP.NOTIF_TYPE_CODE IN ('NTC23', 'NTC24');
```

Fallo de envío SR→PI: SR vuelve a **Pendiente de Autorización**.

---

## 4. Cargue masivo SR

```sql
SELECT PROCESSED, ERROR_REASON, LOADED_BY, CREATED_DATE, send_attempt
FROM [rfd].[SP_REF_LOAD_MASSIVE_REQUEST]
WHERE LOADED_BY = @qa
ORDER BY CREATED_DATE DESC;

SELECT *
FROM [rfd].[SP_REF_LOGS_TRANSACTION]
WHERE created_DATE >= @inicio_prueba
ORDER BY created_DATE DESC;
```

Function: `az-fapp-sprefprocess-use-qa` (~10 min). No llamar LoadMassive si la validación previa falla (tiquetes duplicados / estado E).

---

## 5. Consulta tu Reembolso (AVR)

```sql
SELECT STATION, CTL_NUM, REF_EMA
FROM [rfd].[AVR_DAT_REQUEST_ENC]
WHERE STATION = @station AND CTL_NUM = @ctl;

SELECT REF_STA_DET, MET_PAY_FOP, VAL_AUT, FAR_AMT
FROM [rfd].[AVR_DAT_REQUEST_DET]
WHERE /* document / request */;
```

Si el tiquete tiene varias solicitudes, la API debe devolver la **autorizada**. Contrastar `REF_STA_DET`.

---

## 6. Plantilla / gestión de pago PI

```sql
SELECT *
FROM [rfd].[PIC_FOP_PAYMENT_REQUEST]
WHERE /* refund o tkt */;

SELECT *
FROM [rfd].[PIC_PAYMENT_REQUEST]
WHERE /* misma clave */;

SELECT *
FROM [rfd].[PIC_PAYMENT_DETAIL]
WHERE REFUND_REQUEST = @req;

-- Si FOP = KR
SELECT EXPIRE_DATE, ACTIVATION_DATE
FROM [rfd].[PIC_VOUCHER]
WHERE /* misma clave */;

-- Si FOP = CR
SELECT BANK_ACCOUNT_NO, BANK_CODE
FROM [rfd].[PIC_BANK_DATA_INFORMATION]
WHERE /* misma clave */;
```

---

## 7. Usuarios inactivos (cualquier app)

```sql
SELECT email, FIRST_NAME, LAST_NAME, last_login_date
FROM [adm].[MST_USER]
WHERE DATEDIFF(DAY, last_login_date, GETDATE()) >= 90;
```

Log: `SP_REF_LOGS_TRANSACTION` / `AVR_LOGS_TRANSACTION` / `PIC_LOGS_TRANSACTION` / `LOGS_TRANSACTION` (ROR, `created_user = 'ROR_DEACTIVITY_USER'`) según producto.

---

## 8. ROR — maestra EMD y homologación

**Acción UI:** Maestras → Documento misceláneo → consultar / crear / modificar EMD.

```sql
SELECT *
FROM [master].[MST_EMD]
-- filtrar por el Código / Emdcode de la prueba
;
```

**Esperado:** el registro creado o modificado aparece. Mensajes de UI documentados: “EMD creado exitosamente” / confirmación de actualización.

**Acción API:** ListHomologation (campo `ReferenceValueOrig` vacío = todos).

```sql
SELECT *
FROM [master].[MS_HOMOLOGATION_REFERENCE_VALUES]
-- si se filtró: WHERE REFERENCE_VALUE_ORIG = @valor
;
```

**Acción API:** EmdGetRfisc (`Emdcode` existente).

Cierre: misma fila en `[master].[MST_EMD]`. ⚠️ El manual también escribe `Master.MST.EMD`.

---

## Cómo adjuntar el script al Test Case

En Azure DevOps (lineamientos): nombre `PBI-XXXXX #TC …`, Area, Iteration, Related work al PBI, evidencias con fecha/hora. El SQL va en un paso:

> **Paso n — Verificar en BD:** ejecutar `{script}`. Esperado: `{estado/campo}`. Adjuntar result set.
