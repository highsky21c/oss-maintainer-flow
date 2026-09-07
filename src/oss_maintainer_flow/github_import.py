from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class GitHubRepository:
    owner: str
    name: str


def parse_repository(value: str) -> GitHubRepository:
    parts = value.strip().removeprefix("https://github.com/").strip("/").split("/")
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise ValueError("Repository must be in owner/name form or a GitHub repository URL.")
    return GitHubRepository(parts[0], parts[1])


def label_names(labels: list[Any]) -> list[str]:
    names: list[str] = []
    for label in labels:
        if isinstance(label, dict) and label.get("name"):
            names.append(str(label["name"]))
        elif isinstance(label, str):
            names.append(label)
    return names


def normalize_issue(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "number": int(item.get("number", 0)),
        "title": str(item.get("title", "")),
        "body": item.get("body") or "",
        "labels": label_names(item.get("labels", [])),
    }


def normalize_pull_request(item: dict[str, Any]) -> dict[str, Any]:
    user = item.get("user") or {}
    return {
        "number": int(item.get("number", 0)),
        "title": str(item.get("title", "")),
        "author": str(user.get("login", "")),
        "labels": label_names(item.get("labels", [])),
        "merged_at": item.get("merged_at"),
    }


def github_api_request(path: str, token: str | None = None) -> list[dict[str, Any]]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "oss-maintainer-flow",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(f"https://api.github.com{path}", headers=headers)
    try:
        with urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        message = error.read().decode("utf-8")
        raise SystemExit(f"GitHub API request failed with {error.code}: {message}") from error

    if not isinstance(data, list):
        raise SystemExit("GitHub API response was not a list.")
    return data


def fetch_github_export(repository: str, kind: str, state: str = "open", token: str | None = None) -> list[dict[str, Any]]:
    repo = parse_repository(repository)
    query = urlencode({"state": state, "per_page": "100"})

    if kind == "issues":
        items = github_api_request(f"/repos/{repo.owner}/{repo.name}/issues?{query}", token or os.getenv("GITHUB_TOKEN"))
        return [normalize_issue(item) for item in items if "pull_request" not in item]
    if kind == "pulls":
        items = github_api_request(f"/repos/{repo.owner}/{repo.name}/pulls?{query}", token or os.getenv("GITHUB_TOKEN"))
        return [normalize_pull_request(item) for item in items]

    raise ValueError("kind must be either 'issues' or 'pulls'.")
