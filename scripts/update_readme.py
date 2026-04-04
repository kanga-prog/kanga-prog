#!/usr/bin/env python3
import json
import os
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

USERNAME = os.getenv("PROFILE_USERNAME") or os.getenv("GITHUB_REPOSITORY_OWNER") or "kanga-prog"
README_PATH = Path("README.md")

START = "<!-- AUTO-TECH-FOCUS:START -->"
END = "<!-- AUTO-TECH-FOCUS:END -->"

PROFILE_TOKEN = (os.getenv("PROFILE_README_TOKEN") or "").strip()
GITHUB_TOKEN = (os.getenv("GITHUB_TOKEN") or "").strip()
TOKEN = PROFILE_TOKEN or GITHUB_TOKEN or None

INCLUDE_PRIVATE = os.getenv("INCLUDE_PRIVATE", "false").lower() == "true"

DOCS = {
    "React": {
        "badge": "React-20232A?logo=react",
        "url": "https://react.dev/",
    },
    "TypeScript": {
        "badge": "TypeScript-3178C6?logo=typescript&logoColor=white",
        "url": "https://www.typescriptlang.org/",
    },
    "JavaScript": {
        "badge": "JavaScript-F7DF1E?logo=javascript&logoColor=black",
        "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
    },
    "Java": {
        "badge": "Java-ED8B00?logo=openjdk&logoColor=white",
        "url": "https://dev.java/",
    },
    "Spring Boot": {
        "badge": "Spring_Boot-6DB33F?logo=springboot&logoColor=white",
        "url": "https://spring.io/projects/spring-boot",
    },
    "PostgreSQL": {
        "badge": "PostgreSQL-4169E1?logo=postgresql&logoColor=white",
        "url": "https://www.postgresql.org/docs/",
    },
    "Docker": {
        "badge": "Docker-2496ED?logo=docker&logoColor=white",
        "url": "https://docs.docker.com/",
    },
    "Linux": {
        "badge": "Linux-FCC624?logo=linux&logoColor=black",
        "url": "https://kernel.org/",
    },
    "JWT": {
        "badge": "JWT-black?logo=jsonwebtokens",
        "url": "https://jwt.io/introduction",
    },
    "Cybersecurity": {
        "badge": "Cybersecurity-8B0000",
        "url": "https://owasp.org/www-project-top-ten/",
    },
    "Python": {
        "badge": "Python-3776AB?logo=python&logoColor=white",
        "url": "https://docs.python.org/3/",
    },
}

LANGUAGE_TO_TECH = {
    "TypeScript": "TypeScript",
    "JavaScript": "JavaScript",
    "Java": "Java",
    "Python": "Python",
    "Shell": "Linux",
    "Dockerfile": "Docker",
}

SIGNAL_RULES = {
    "React": ["react", "vite", "react-router", "radix", "shadcn", "tailwind"],
    "Spring Boot": ["spring boot", "spring-security", "spring data", "maven", "java 17", "java 21"],
    "PostgreSQL": ["postgres", "postgresql", "kysely", "jdbc:postgresql"],
    "Docker": ["docker", "dockerfile", "docker-compose", "container"],
    "Linux": ["linux", "kali", "bash", "shell"],
    "JWT": ["jwt", "jose", "bearer token", "token auth"],
    "Cybersecurity": ["cyber", "security", "owasp", "idor", "command injection", "nmap", "xss", "pentest"],
}

def gh_get(url: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USERNAME}-profile-readme-bot",
        "X-GitHub-Api-Version": "2026-03-10",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    request = Request(url, headers=headers)
    with urlopen(request) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return json.loads(response.read().decode(charset))

def fetch_repos():
    repos = []
    page = 1

    while True:
        if INCLUDE_PRIVATE and PROFILE_TOKEN:
            params = urlencode({
                "per_page": 100,
                "page": page,
                "affiliation": "owner",
                "sort": "updated",
            })
            url = f"https://api.github.com/user/repos?{params}"
        else:
            params = urlencode({
                "per_page": 100,
                "page": page,
                "type": "owner",
                "sort": "updated",
            })
            url = f"https://api.github.com/users/{USERNAME}/repos?{params}"

        batch = gh_get(url)
        if not batch:
            break

        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    return repos

def repo_text(repo: dict) -> str:
    parts = [
        repo.get("name", "") or "",
        repo.get("description", "") or "",
    ]
    for topic in (repo.get("topics") or []):
        parts.append(topic)
    return " ".join(parts).lower()

def detect_techs():
    repos = fetch_repos()
    repos = [
        r for r in repos
        if not r.get("fork")
        and not r.get("archived")
        and (r.get("name", "").lower() != USERNAME.lower())
    ]

    language_bytes = Counter()
    signal_scores = Counter()

    for repo in repos:
        languages_url = repo.get("languages_url")
        if languages_url:
            try:
                lang_map = gh_get(languages_url)
                for lang, amount in lang_map.items():
                    language_bytes[lang] += int(amount)
            except Exception:
                pass

        text = repo_text(repo)
        for tech, keywords in SIGNAL_RULES.items():
            hits = sum(1 for kw in keywords if kw in text)
            if hits:
                signal_scores[tech] += hits

    chosen = []

    def add(tech_name: str):
        if tech_name in DOCS and tech_name not in chosen:
            chosen.append(tech_name)

    for tech, _score in signal_scores.most_common():
        add(tech)

    for lang, _amount in language_bytes.most_common():
        tech = LANGUAGE_TO_TECH.get(lang)
        if tech:
            add(tech)

    if not chosen:
        chosen = ["JavaScript", "TypeScript", "Java", "Python"]

    return chosen[:10], language_bytes

def build_badge(tech_name: str) -> str:
    item = DOCS[tech_name]
    return f"[![{tech_name}](https://img.shields.io/badge/{item['badge']})]({item['url']})"

def render_section(techs, language_bytes: Counter) -> str:
    dominant_langs = ", ".join(lang for lang, _ in language_bytes.most_common(5))
    if not dominant_langs:
        dominant_langs = "No dominant language detected yet"

    badges = " ".join(build_badge(t) for t in techs)

    return "\n".join([
        "## 🔧 Tech Focus",
        "",
        "> Auto-generated from repository languages and repository metadata.",
        "",
        f"Detected stack signals: **{dominant_langs}**",
        "",
        badges,
    ])

def replace_block(content: str, new_block: str) -> str:
    wrapped = f"{START}\n{new_block}\n{END}"
    pattern = re.compile(f"{re.escape(START)}.*?{re.escape(END)}", flags=re.DOTALL)

    if pattern.search(content):
        return pattern.sub(wrapped, content)

    return content.rstrip() + "\n\n" + wrapped + "\n"

def main():
    original = README_PATH.read_text(encoding="utf-8")
    techs, language_bytes = detect_techs()
    new_section = render_section(techs, language_bytes)
    updated = replace_block(original, new_section)

    if updated != original:
        README_PATH.write_text(updated, encoding="utf-8")
        print("README updated.")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    main()
