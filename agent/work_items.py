"""Lectura de solo lectura de un Work Item y su contexto."""

from __future__ import annotations

import hashlib
import re
import tempfile
import urllib.parse
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from agent.attachments import ExtractedDocument, extract_bytes, safe_name
from agent.code_changes import collect_code_changes
from agent.azure_client import AzureReadClient, AzureReadError
from agent.config import Settings
from agent.html_text import html_to_text


@dataclass
class WorkItemContext:
    source: dict[str, Any]
    metadata: dict[str, Any]
    requirements: dict[str, Any]
    discussions: list[dict[str, Any]] = field(default_factory=list)
    relations: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    attachments: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    provenance: list[dict[str, Any]] = field(default_factory=list)
    warnings: dict[str, list[str]] = field(default_factory=dict)
    manuals: list[dict[str, Any]] = field(default_factory=list)
    code_changes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def revalidate_manuals(root: Path) -> list[dict[str, Any]]:
    folder = root / "base_conocimiento"
    found: list[dict[str, Any]] = []
    if not folder.is_dir():
        return [{"path": "base_conocimiento/", "status": "no_encontrado"}]
    for path in sorted(folder.glob("*.md")):
        payload = path.read_bytes()
        found.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "status": "presente",
            }
        )
    return found


def parse_work_item_ref(raw: str, settings: Settings) -> tuple[str, int]:
    text = raw.strip()
    if text.isdigit():
        return settings.project, int(text)
    parsed = urllib.parse.urlparse(text)
    host = parsed.hostname or ""
    if host not in settings.allowed_hosts:
        raise AzureReadError(0, "url_invalida", "La URL no es de la organización configurada.")
    if settings.org not in host and f"/{settings.org}/" not in parsed.path:
        raise AzureReadError(0, "url_invalida", "La URL pertenece a otra organización. No se cruza el PAT.")
    match = re.search(r"/_workitems/edit/(\d+)|/workitems/(\d+)", parsed.path, re.I)
    query = urllib.parse.parse_qs(parsed.query)
    query_id = ""
    for key in ("workitem", "workItemId", "id"):
        values = query.get(key) or []
        if values and values[0].isdigit():
            query_id = values[0]
            break
    if match:
        work_id = int(next(group for group in match.groups() if group))
    elif query_id:
        work_id = int(query_id)
    else:
        raise AzureReadError(0, "url_invalida", "La URL no contiene un Work Item ID.")
    parts = [part for part in parsed.path.split("/") if part]
    project = settings.project
    if parts and parts[0] not in {settings.org, "_workitems", "workitems"}:
        project = urllib.parse.unquote(parts[0])
    return project, work_id


class WorkItemReader:
    def __init__(self, settings: Settings, client: AzureReadClient) -> None:
        self.settings = settings
        self.client = client

    def locate(self, work_id: int) -> str:
        """Empieza por Integration y, si no está, recorre el resto de proyectos. Solo GET."""
        first = self.settings.project
        try:
            item = self._get_item(first, work_id)
            fields = item.get("fields") or {}
            return str(fields.get("System.TeamProject") or first)
        except AzureReadError as exc:
            if exc.status != 404:
                raise
        catalog = self.client.get_json(
            f"https://dev.azure.com/{self.settings.org}/_apis/projects?api-version=7.1"
        )
        for project in catalog.get("value") or []:
            name = str(project.get("name") or "")
            if not name or name == first:
                continue
            try:
                item = self._get_item(name, work_id)
            except AzureReadError as exc:
                if exc.status == 404:
                    continue
                raise
            fields = item.get("fields") or {}
            return str(fields.get("System.TeamProject") or name)
        raise AzureReadError(
            404,
            "http_404",
            "No se encontró el Work Item en Integration ni en los demás proyectos de la organización.",
        )

    def fetch(self, ref: str, root: Path, project: str | None = None) -> WorkItemContext:
        if not self.settings.enabled:
            raise AzureReadError(0, "deshabilitado", "AZDO_WI_ENABLED está en false.")
        manuals = revalidate_manuals(root)
        parsed_project, work_id = parse_work_item_ref(ref, self.settings)
        project = project or parsed_project
        item = self._get_item(project, work_id)
        fields = item.get("fields") or {}
        real_project = str(fields.get("System.TeamProject") or project)
        if real_project != project:
            project = real_project
            item = self._get_item(project, work_id)
            fields = item.get("fields") or {}
        description = html_to_text(fields.get("System.Description"))
        acceptance = self._acceptance(fields)
        comments = self._comments(project, work_id)
        relations = self._relations(item, project, {work_id})
        extracted, skipped = self._attachments(item)
        warnings = self._warnings(description, acceptance, relations, skipped)
        evidence = f"AZDO-WI-{work_id}"
        provenance = [
            {"id": f"{evidence}:DESC", "kind": "description", "status": "recuperado" if description else "vacio"},
            {"id": f"{evidence}:AC", "kind": "acceptance_criteria", "status": "recuperado" if acceptance else "vacio"},
        ]
        for index, comment in enumerate(comments, start=1):
            provenance.append({"id": f"{evidence}:COMMENT-{index}", "kind": "comment", "status": "recuperado"})
        for index, doc in enumerate(extracted, start=1):
            provenance.append({"id": f"{evidence}:ATT-{index}", "kind": "attachment", "status": doc["status"], "filename": doc["filename"]})
        for manual in manuals:
            provenance.append({"id": f"MANUAL:{manual.get('path')}", "kind": "manual", "status": manual.get("status"), "sha256": manual.get("sha256")})
        return WorkItemContext(
            source={
                "organization": self.settings.org,
                "project": project,
                "work_item_id": item.get("id") or work_id,
                "url": item.get("url"),
                "revision": item.get("rev"),
            },
            metadata={
                "title": fields.get("System.Title"),
                "type": fields.get("System.WorkItemType"),
                "status": fields.get("System.State"),
                "area": fields.get("System.AreaPath"),
                "iteration": fields.get("System.IterationPath"),
                "tags": fields.get("System.Tags"),
            },
            requirements={
                "description": description,
                "acceptance_criteria": acceptance,
                "acceptance_field": self._acceptance_field(fields),
                "custom_fields": self._custom_fields(fields),
                "evidence_ids": {"description": f"{evidence}:DESC", "acceptance_criteria": f"{evidence}:AC"},
            },
            discussions=comments,
            relations=relations,
            attachments={"extracted_documents": extracted, "skipped_documents": skipped},
            code_changes=collect_code_changes(self.client, self.settings.org, relations.get("prs") or []),
            provenance=provenance,
            warnings=warnings,
            manuals=manuals,
        )

    def _get_item(self, project: str, work_id: int) -> dict[str, Any]:
        url = (
            f"https://dev.azure.com/{self.settings.org}/{urllib.parse.quote(project)}"
            f"/_apis/wit/workitems/{work_id}?$expand=relations&api-version=7.1"
        )
        return self.client.get_json(url)

    def _acceptance_field(self, fields: dict[str, Any]) -> str | None:
        if "Microsoft.VSTS.Common.AcceptanceCriteria" in fields:
            return "Microsoft.VSTS.Common.AcceptanceCriteria"
        for key in fields:
            if "acceptance" in key.lower() and key.startswith("Custom."):
                return key
        return None

    def _acceptance(self, fields: dict[str, Any]) -> str:
        key = self._acceptance_field(fields)
        if not key:
            return ""
        return html_to_text(str(fields.get(key) or ""))

    def _custom_fields(self, fields: dict[str, Any]) -> dict[str, str]:
        custom: dict[str, str] = {}
        for key, value in fields.items():
            if not key.startswith(("Custom.", "ScrumProject.", "ScrumSupport.")):
                continue
            text = html_to_text(str(value)) if isinstance(value, str) else str(value)
            if text and len(text) <= 2000:
                custom[key] = text
        return custom

    def _comments(self, project: str, work_id: int) -> list[dict[str, Any]]:
        collected: list[dict[str, Any]] = []
        token = ""
        while len(collected) < self.settings.max_comments:
            query = f"api-version=7.1-preview.4&$top=100"
            if token:
                query += "&continuationToken=" + urllib.parse.quote(token)
            url = (
                f"https://dev.azure.com/{self.settings.org}/{urllib.parse.quote(project)}"
                f"/_apis/wit/workItems/{work_id}/comments?{query}"
            )
            page = self.client.get_json(url)
            for comment in page.get("comments") or []:
                if len(collected) >= self.settings.max_comments:
                    break
                collected.append(
                    {
                        "id": comment.get("id"),
                        "text": html_to_text(comment.get("text")),
                        "created_date": (comment.get("createdDate") or ""),
                        "source": "comment",
                        "note": "Un comentario no es un criterio de aceptación.",
                    }
                )
            token = str(page.get("continuationToken") or "")
            if not token:
                break
        return collected

    def _relations(self, item: dict[str, Any], project: str, seen: set[int]) -> dict[str, list[dict[str, Any]]]:
        grouped = {"parents": [], "children": [], "related": [], "prs": [], "external": []}
        for relation in item.get("relations") or []:
            rel = str(relation.get("rel") or "")
            url = str(relation.get("url") or "")
            attributes = relation.get("attributes") or {}
            name = attributes.get("name") or ""
            record = {"rel": rel, "name": name, "url": url if self._same_org(url) or not url else url}
            if "ArtifactLink" in rel or "/pullrequest/" in url.lower() or "PullRequest" in rel:
                record["status"] = "metadata"
                record["note"] = "Enlace de código. Se intenta leer el último commit."
                grouped["prs"].append(record)
                continue
            if rel == "AttachedFile":
                continue
            if not self._same_org(url):
                grouped["external"].append({"url": url, "status": "no_recuperado", "name": name})
                continue
            linked_id = _id_from_url(url)
            bucket = "related"
            if "Hierarchy-Reverse" in rel:
                bucket = "parents"
            elif "Hierarchy-Forward" in rel:
                bucket = "children"
            if linked_id is None or linked_id in seen:
                if linked_id is not None:
                    record["id"] = linked_id
                if linked_id in seen:
                    record["status"] = "duplicado_o_ciclo"
                grouped[bucket].append(record)
                continue
            record["id"] = linked_id
            record["status"] = "metadata"
            if self.settings.max_related_depth >= 1:
                try:
                    linked = self._get_item(self._project_from_url(url, project), linked_id)
                    linked_fields = linked.get("fields") or {}
                    record["title"] = linked_fields.get("System.Title")
                    record["type"] = linked_fields.get("System.WorkItemType")
                    record["state"] = linked_fields.get("System.State")
                    record["status"] = "recuperado"
                    seen.add(linked_id)
                except AzureReadError as exc:
                    record["status"] = "no_recuperado"
                    record["warning"] = str(exc)
            grouped[bucket].append(record)
        return grouped

    def _attachments(self, item: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        extracted: list[dict[str, Any]] = []
        skipped: list[dict[str, Any]] = []
        if not self.settings.include_attachments:
            skipped.append({"status": "omitido", "warnings": ["AZDO_WI_INCLUDE_ATTACHMENTS=false"]})
            return extracted, skipped
        total = 0
        with tempfile.TemporaryDirectory(prefix="wi-att-") as temp_name:
            temp = Path(temp_name)
            for relation in item.get("relations") or []:
                if relation.get("rel") != "AttachedFile":
                    continue
                url = str(relation.get("url") or "")
                filename = safe_name(str((relation.get("attributes") or {}).get("name") or "adjunto"))
                if not self._same_org(url):
                    skipped.append({"filename": filename, "status": "omitido", "warnings": ["URL de adjunto fuera de la organización."]})
                    continue
                try:
                    payload = self.client.get_bytes(url)
                except AzureReadError as exc:
                    skipped.append({"filename": filename, "status": "omitido", "warnings": [str(exc)]})
                    continue
                if len(payload) > self.settings.max_attachment_bytes or total + len(payload) > self.settings.max_total_attachment_bytes:
                    skipped.append({"filename": filename, "status": "omitido", "warnings": ["Supera el límite de tamaño configurado."]})
                    continue
                total += len(payload)
                raw_path = temp / filename
                raw_path.write_bytes(payload)
                document = extract_bytes(filename, payload, self.settings.max_extract_chars, source_url=url)
                target = extracted if document.status == "extraido" else skipped
                target.append(_document_dict(document))
                if not self.settings.keep_raw and raw_path.exists():
                    raw_path.unlink()
        return extracted, skipped

    def _warnings(self, description: str, acceptance: str, relations: dict[str, list], skipped: list[dict]) -> dict[str, list[str]]:
        missing: list[str] = []
        inaccessible: list[str] = []
        if not description:
            missing.append("System.Description vacío. No se inventan requisitos.")
        if not acceptance:
            missing.append("No hay criterios de aceptación en el campo estándar ni en un campo custom con 'acceptance'.")
        for bucket in ("parents", "children", "related", "external"):
            for row in relations.get(bucket) or []:
                if row.get("status") == "no_recuperado":
                    inaccessible.append(f"{bucket}: {row.get('id') or row.get('status')}")
        for row in skipped:
            inaccessible.append(f"adjunto {row.get('filename')}: {'; '.join(row.get('warnings') or [])}")
        return {"missing_requirements": missing, "inaccessible_resources": inaccessible}

    def _project_from_url(self, url: str, fallback: str) -> str:
        parts = [part for part in urllib.parse.urlparse(url).path.split("/") if part]
        if len(parts) >= 2 and parts[0] == self.settings.org:
            return urllib.parse.unquote(parts[1])
        return fallback

    def _same_org(self, url: str) -> bool:
        if not url:
            return False
        parsed = urllib.parse.urlparse(url)
        host = parsed.hostname or ""
        return parsed.scheme == "https" and host in self.settings.allowed_hosts and (
            self.settings.org in host or f"/{self.settings.org}/" in parsed.path
        )


def _id_from_url(url: str) -> int | None:
    match = re.search(r"/workItems/(\d+)", url, re.I)
    return int(match.group(1)) if match else None


def _document_dict(document: ExtractedDocument) -> dict[str, Any]:
    return {
        "filename": document.filename,
        "extension": document.extension,
        "status": document.status,
        "text": document.text,
        "sheets_or_pages": document.sheets_or_pages,
        "sha256": document.sha256,
        "warnings": document.warnings,
    }
