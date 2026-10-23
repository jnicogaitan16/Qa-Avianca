"""Lee commits enlazados al Work Item. El último pesa más. Si no hay enlace, no bloquea."""

from __future__ import annotations

import re
import urllib.parse
from typing import Any

from agent.azure_client import AzureReadClient, AzureReadError


_HTTPS_COMMIT = re.compile(
    r"https://dev\.azure\.com/[^/]+/([^/]+)/_git/([^/]+)/commit/([0-9a-fA-F]{7,40})"
)
_HTTPS_PR = re.compile(
    r"https://dev\.azure\.com/[^/]+/([^/]+)/_git/([^/]+)/pullrequest/(\d+)"
)
_HTTPS_WIKI = re.compile(
    r"https://dev\.azure\.com/[^/]+/([^/]+)/_wiki/wikis/([^/?#]+)(?:/(\d+))?"
)
_WIKI_PATH = re.compile(r"[?&]pagePath=([^&#]+)")
_EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
_MAX_PATHS = 40
_MAX_COMMENT = 400


def parse_git_link(url: str) -> dict[str, str] | None:
    text = urllib.parse.unquote((url or "").strip())
    https_commit = _HTTPS_COMMIT.search(text)
    if https_commit:
        return {
            "kind": "commit",
            "project": https_commit.group(1),
            "repo": https_commit.group(2),
            "commit": https_commit.group(3),
        }
    https_pr = _HTTPS_PR.search(text)
    if https_pr:
        return {
            "kind": "pr",
            "project": https_pr.group(1),
            "repo": https_pr.group(2),
            "pr": https_pr.group(3),
        }
    if not text.lower().startswith("vstfs:///git/"):
        return None
    parts = [part for part in text.split("/") if part and part != "vstfs:"]
    if len(parts) < 5 or parts[0].lower() != "git":
        return None
    kind = parts[1].lower()
    project, repo, ident = parts[2], parts[3], parts[4]
    if kind == "commit":
        return {"kind": "commit", "project": project, "repo": repo, "commit": ident}
    if kind == "pullrequestid":
        return {"kind": "pr", "project": project, "repo": repo, "pr": ident}
    return None


def parse_wiki_link(url: str) -> dict[str, str] | None:
    text = urllib.parse.unquote((url or "").strip())
    https = _HTTPS_WIKI.search(text)
    page_path = ""
    path_match = _WIKI_PATH.search(text)
    if path_match:
        page_path = urllib.parse.unquote(path_match.group(1))
    if https and (https.group(3) or page_path):
        return {
            "project": https.group(1),
            "wiki": https.group(2),
            "page": https.group(3) or "",
            "path": page_path,
        }
    if not text.lower().startswith("vstfs:///wiki/wikipage/"):
        return None
    parts = [part for part in text.split("/") if part and part != "vstfs:"]
    if len(parts) < 5 or parts[0].lower() != "wiki":
        return None
    return {"project": parts[2], "wiki": parts[3], "page": parts[4], "path": ""}


def collect_code_changes(client: AzureReadClient, org: str, links: list[dict[str, Any]]) -> dict[str, Any]:
    parsed = []
    wiki_links = []
    for link in links:
        url = str(link.get("url") or "")
        found = parse_git_link(url)
        if found:
            parsed.append(found)
        wiki = parse_wiki_link(url)
        if wiki:
            wiki_links.append(wiki)
    wiki_pages = _read_wiki_pages(client, org, wiki_links)
    if not parsed and not wiki_pages:
        empty = _empty("sin_enlaces", "No se encontraron enlaces de código. Se continúa.")
        empty["wiki_read"] = 0
        return empty
    commits: list[dict[str, Any]] = []
    for item in parsed:
        try:
            if item["kind"] == "commit":
                commits.append(_read_commit(client, org, item["project"], item["repo"], item["commit"]))
            else:
                commits.extend(_read_pr(client, org, item["project"], item["repo"], item["pr"]))
        except (AzureReadError, ValueError):
            continue
    commits = _dedupe(commits)
    if not commits and not wiki_pages:
        return _empty("no_recuperado", "El enlace de código no devolvió cambios. Se continúa.")
    ordered = sorted(commits, key=lambda item: item.get("date") or "")
    last = ordered[-1] if ordered else None
    previous = []
    if last:
        last["peso"] = "ultimo"
        previous = [{"commit_id": item["commit_id"], "date": item.get("date") or "", "peso": "anterior"} for item in reversed(ordered[:-1])]
    notice = "No se encontraron enlaces de código. Se continúa."
    if ordered:
        notice = f"Se leyeron {len(ordered)} commits. El de más peso es el último, {last.get('date') or 'sin fecha'}."
    elif wiki_pages:
        notice = f"Se leyeron {len(wiki_pages)} páginas wiki. Se continúa."
    return {
        "status": "leido" if ordered or wiki_pages else "sin_enlaces",
        "notice": notice,
        "last": last,
        "previous": previous[:3],
        "commits_read": len(ordered),
        "wiki_read": len(wiki_pages),
        "wiki": wiki_pages,
    }


def _empty(status: str, notice: str) -> dict[str, Any]:
    return {
        "status": status,
        "notice": notice,
        "last": None,
        "previous": [],
        "commits_read": 0,
        "wiki_read": 0,
        "wiki": [],
    }


def _read_wiki_pages(client: AzureReadClient, org: str, links: list[dict[str, str]]) -> list[dict[str, str]]:
    pages = []
    for link in links:
        try:
            if link.get("page"):
                url = (
                    f"https://dev.azure.com/{_segment(org)}/{_segment(link['project'])}/_apis/wiki/wikis/"
                    f"{_segment(link['wiki'])}/pages/{_segment(link['page'])}?includeContent=true&api-version=7.1"
                )
            elif link.get("path"):
                url = (
                    f"https://dev.azure.com/{_segment(org)}/{_segment(link['project'])}/_apis/wiki/wikis/"
                    f"{_segment(link['wiki'])}/pages?path={urllib.parse.quote(link['path'])}&includeContent=true&api-version=7.1"
                )
            else:
                continue
            payload = client.get_json(url)
        except (AzureReadError, ValueError):
            continue
        content = _EMAIL.sub("el correo", str(payload.get("content") or ""))[:_MAX_COMMENT]
        if not content and not payload.get("path"):
            continue
        pages.append({"path": str(payload.get("path") or link.get("path") or ""), "content": content})
    return pages


def _read_pr(client: AzureReadClient, org: str, project: str, repo: str, pr_id: str) -> list[dict[str, Any]]:
    url = (
        f"https://dev.azure.com/{_segment(org)}/{_segment(project)}/_apis/git/repositories/{_segment(repo)}"
        f"/pullRequests/{_segment(pr_id)}/commits?api-version=7.1"
    )
    payload = client.get_json(url)
    found = []
    for commit in payload.get("value") or []:
        sha = str(commit.get("commitId") or "")
        if sha:
            found.append(_read_commit(client, org, project, repo, sha, summary=commit))
    return found


def _read_commit(
    client: AzureReadClient,
    org: str,
    project: str,
    repo: str,
    sha: str,
    summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if summary is None:
        url = (
            f"https://dev.azure.com/{_segment(org)}/{_segment(project)}/_apis/git/repositories/{_segment(repo)}"
            f"/commits/{_segment(sha)}?api-version=7.1"
        )
        summary = client.get_json(url)
    changes_url = (
        f"https://dev.azure.com/{_segment(org)}/{_segment(project)}/_apis/git/repositories/{_segment(repo)}"
        f"/commits/{_segment(sha)}/changes?api-version=7.1"
    )
    paths: list[str] = []
    try:
        changes = client.get_json(changes_url)
        for change in changes.get("changes") or []:
            path = str((change.get("item") or {}).get("path") or "")
            if path and path not in paths:
                paths.append(path)
            if len(paths) == _MAX_PATHS:
                break
    except AzureReadError:
        paths = []
    author = (summary or {}).get("author") or {}
    comment = _EMAIL.sub("el correo", str((summary or {}).get("comment") or ""))[:_MAX_COMMENT]
    return {
        "commit_id": sha,
        "date": str(author.get("date") or ""),
        "comment": comment,
        "paths": paths,
    }


def _dedupe(commits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for commit in commits:
        sha = str(commit.get("commit_id") or "")
        if not sha:
            continue
        current = by_id.get(sha)
        if current is None or len(commit.get("paths") or []) > len(current.get("paths") or []):
            by_id[sha] = commit
    return list(by_id.values())


def _segment(value: str) -> str:
    text = str(value or "").strip()
    if not text or ".." in text or "/" in text or "\\" in text or "://" in text:
        raise ValueError("segmento")
    return urllib.parse.quote(text, safe="")
