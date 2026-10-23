"""Cliente HTTP de solo lectura hacia Azure DevOps."""

from __future__ import annotations

import base64
import json
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from agent.config import Settings


class AzureReadError(Exception):
    def __init__(self, status: int, code: str, message: str) -> None:
        self.status = status
        self.code = code
        super().__init__(message)


class _GuardedRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, allowed_hosts: frozenset[str]) -> None:
        super().__init__()
        self.allowed_hosts = allowed_hosts

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        host = urllib.parse.urlparse(newurl).hostname or ""
        if host not in self.allowed_hosts:
            raise AzureReadError(code, "redirect_bloqueado", "La redirección sale de los hosts permitidos.")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class AzureReadClient:
    def __init__(self, settings: Settings, opener: urllib.request.OpenerDirector | None = None) -> None:
        self.settings = settings
        self._opener = opener or urllib.request.build_opener(
            _GuardedRedirect(settings.allowed_hosts),
            urllib.request.HTTPSHandler(context=ssl.create_default_context()),
        )

    def get_json(self, url: str) -> dict[str, Any]:
        raw = self.get_bytes(url, accept="application/json")
        return json.loads(raw.decode("utf-8"))

    def get_bytes(self, url: str, accept: str = "*/*") -> bytes:
        self._guard_url(url)
        if not self.settings.token:
            raise AzureReadError(0, "sin_credencial", f"Falta el valor de {self.settings.pat_var} en .env.")
        basic = base64.b64encode(f":{self.settings.token}".encode()).decode()
        request = urllib.request.Request(
            url,
            headers={"Authorization": f"Basic {basic}", "Accept": accept},
            method="GET",
        )
        delay = 1.0
        last_error: AzureReadError | None = None
        for attempt in range(3):
            try:
                with self._opener.open(request, timeout=45) as response:
                    return response.read()
            except urllib.error.HTTPError as exc:
                last_error = self._http_error(exc)
                if exc.code not in {429, 500, 502, 503, 504} or attempt == 2:
                    raise last_error from None
            except AzureReadError:
                raise
            except Exception as exc:  # noqa: BLE001
                redacted = _redact(str(exc), self.settings.token)
                last_error = AzureReadError(0, "red", f"No se pudo leer Azure DevOps: {redacted}")
                if attempt == 2:
                    raise last_error from None
            time.sleep(delay)
            delay *= 2
        raise last_error or AzureReadError(0, "red", "No se pudo leer Azure DevOps.")

    def _guard_url(self, url: str) -> None:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != "https":
            raise AzureReadError(0, "url_invalida", "Solo se permiten URLs https de la organización configurada.")
        if (parsed.hostname or "") not in self.settings.allowed_hosts:
            raise AzureReadError(0, "url_invalida", "El host no está en la lista de la organización configurada.")
        if self.settings.org not in parsed.path and self.settings.org not in (parsed.hostname or ""):
            raise AzureReadError(0, "url_invalida", "La URL no pertenece a la organización configurada.")

    def _http_error(self, exc: urllib.error.HTTPError) -> AzureReadError:
        messages = {
            401: "Credencial rechazada. Revisa el PAT de la organización aviancavsts, sin pegarlo en el chat.",
            403: "El PAT no tiene permiso de lectura sobre este recurso. No es un 404.",
            404: "No se encontró el Work Item en el proyecto configurado. Revisa el ID y el proyecto.",
            429: "Azure DevOps limitó las lecturas. Reintenta más tarde.",
        }
        if exc.code in messages:
            return AzureReadError(exc.code, f"http_{exc.code}", messages[exc.code])
        if exc.code >= 500:
            return AzureReadError(exc.code, f"http_{exc.code}", "Azure DevOps respondió un error temporal.")
        return AzureReadError(exc.code, f"http_{exc.code}", f"Azure DevOps respondió HTTP {exc.code}.")


def _redact(text: str, secret: str) -> str:
    if secret and secret in text:
        return text.replace(secret, "***")
    return text
