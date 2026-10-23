# Auditoría F0 — IaAgent y Work Items

Fecha: 23 de octubre de 2026. Estado del repositorio antes de la lectura de Work Items.

## Qué existe

Este repositorio es la QA DevOps Suite: skills de Cursor, manuales en `base_conocimiento/` y casos en `test-cases/`. No hay un paquete Python de análisis de Pull Requests, ni comandos `build`, `parse`, `run`, `sanitize` o `publish`, ni cliente Gemini, ni suite pytest previa.

| Pieza | Estado |
|---|---|
| Orquestador | `skills/orquestador-validador/`. Valida contra `references/` y `base_conocimiento/`. |
| Casos | Tabla Markdown en `test-cases/PBI-*/casos-de-prueba.md`. |
| Excel | `scripts/exportar_casos.py`. Escritor OOXML de la biblioteca estándar. No se modifica su lógica. |
| Azure DevOps | Solo documentación en `skills/azure-devops/references/`. Incluye ejemplos de escritura; el código nuevo no los llama. |
| `docs/proyectos/iaagent.md` | Plan de proceso QA (la IA redacta, la persona publica). No es un cliente. |
| Dependencias | `requirements.txt`: `et_xmlfile`, `openpyxl`. El exportador no importa openpyxl. |
| Secreto | `.env` gitignored. La única clave previa es `TOKEN-AZURE`. El valor no se copia ni se imprime. |
| Git | `git` no está en el PATH de esta máquina. No se pudo correr `git ls-files`. `.gitignore` ya ignora `.env`. |

## Qué no se hereda del plan

No hay flujo de PR que preservar en código. No hay credencial `inteduc` en `.env`. No se crea un segundo agente.

## Hallazgo de conexión (solo lectura, sin imprimir el PAT)

`GET https://dev.azure.com/aviancavsts/_apis/projects?api-version=7.1` respondió 200.

El Work Item 1321233 responde 200. Su `System.TeamProject` es **Integration** (área `Integration\Reembolsos`). `UnidadesSoporteF` existe en la organización y aparece en el manual de PI para otro ítem (956304); no es el proyecto de este PBI.

Comentarios del 1321233: `7.1-preview.4`, total 3, una página.

## Decisión de diseño

1. Reutilizar `TOKEN-AZURE` mediante `AZDO_WI_PAT_VAR`. No se duplica el token.
2. Organización `aviancavsts`. Proyecto por defecto `Integration`, configurable. Si el ítem pertenece a otro proyecto de la misma organización, las llamadas siguientes usan el proyecto del ítem.
3. Solo GET. Sin POST, PATCH ni DELETE.
4. `AZDO_WI_LLM_ENABLED=false`. No hay envío a un LLM.
5. La salida nueva vive en `outputs/WI-<id>/`. Los casos y el Excel siguen el contrato actual.
6. Antes de leer el PBI, el flujo revalida los manuales de `base_conocimiento/` y deja su manifiesto en el Context Pack.
7. `QA_INSTALL_DEPS` autoriza instalar solo `requirements-workitems.txt` (`pypdf`). El resto del lector usa la biblioteca estándar.

## Lectura piloto

`python -m agent work-item fetch 1321233` respondió revisión 33, proyecto Integration, estado QA. Quedaron 5 manuales en el manifiesto, 3 comentarios y el Excel adjunto `IWB_Channel-7_3-Send_Pay_Info_Support_Files-Send_Pay_Info_Support_Files_V4.xlsx` extraído. El PAT no aparece en `outputs/WI-1321233/`. No se generó el Excel de casos.

## Riesgo de regresión

No hay suite de PR. El riesgo real es tocar `scripts/exportar_casos.py` o las columnas de `casos-de-prueba.md`. Esos archivos no entran en este cambio.
