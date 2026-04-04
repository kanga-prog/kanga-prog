#!/usr/bin/env python3
import base64
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

INCLUDE_PRIVATE = os.getenv("INCLUDE_PRIVATE", "true").lower() == "true"
CLICKABLE_BADGES = False

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

TECH_PRIORITY = [
    "React",
    "TypeScript",
    "JavaScript",
    "Java",
    "Spring Boot",
    "PostgreSQL",
    "Docker",
    "JWT",
    "Python",
    "Linux",
    "Cybersecurity",
]

LANGUAGE_TO_TECH = {
    "TypeScript": "TypeScript",
    "JavaScript": "JavaScript",
    "Java": "Java",
    "Python": "Python",
    "Shell": "Linux",
    "Dockerfile": "Docker",
}

PREFERRED_REPOS = {
    "watyouface-backend",
    "watyouface-frontend",
    "bagage-voyage",
    "rebois-connect",
    "projet_personnel",
    "kanga-prog",
}

IGNORE_PREFIXES = (
    "holbertonschool-",
)

IGNORE_EXACT = {
    "binary_trees",
    "simple_shell",
    "printf",
    "mermaid",
    "scripts",
    "tests_projet",
    "hbnb_v2",
    "hbnb_v2_backend",
    "hbnb_v2_frontend",
}

PACKAGE_JSON_PATHS = [
    "package.json",
    "frontend/package.json",
    "client/package.json",
    "web/package.json",
    "app/package.json",
]

POM_PATHS = [
    "pom.xml",
    "backend/pom.xml",
]

PYTHON_PATHS = [
    "requirements.txt",
    "pyproject.toml",
]

README_PATHS = [
    "README.md",
    "readme.md",
]

DOCKER_PATHS = [
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
]

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

def repo_name(repo):
    return (repo.get("name") or "").strip()

def is_ignored_repo(name: str) -> bool:
    lower = name.lower()
    if lower in IGNORE_EXACT:
        return True
    return any(lower.startswith(prefix) for prefix in IGNORE_PREFIXES)

def repo_weight(name: str) -> int:
    lower = name.lower()
    if lower in PREFERRED_REPOS:
        return 6
    if is_ignored_repo(lower):
        return 0
    return 1

def repo_text(repo: dict) -> str:
    parts = [
        repo.get("name", "") or "",
        repo.get("description", "") or "",
    ]
    for topic in (repo.get("topics") or []):
        parts.append(topic)
    return " ".join(parts).lower()

def bump(scores: Counter, tech: str, weight: int = 1):
    if tech in DOCS:
        scores[tech] += weight

def detect_meta_signals(text: str, scores: Counter, weight: int):
    if any(k in text for k in ["react", "vite", "react-router", "radix", "shadcn", "tailwind"]):
        bump(scores, "React", weight)
    if any(k in text for k in ["typescript", "ts", "tsx"]):
        bump(scores, "TypeScript", weight)
    if any(k in text for k in ["javascript", "node", "vite", "hono"]):
        bump(scores, "JavaScript", weight)
    if any(k in text for k in ["java", "maven"]):
        bump(scores, "Java", weight)
    if any(k in text for k in ["spring", "spring boot", "spring-security", "spring data"]):
        bump(scores, "Spring Boot", weight)
    if any(k in text for k in ["postgres", "postgresql", "kysely", "jdbc:postgresql"]):
        bump(scores, "PostgreSQL", weight)
    if any(k in text for k in ["docker", "dockerfile", "docker-compose"]):
        bump(scores, "Docker", weight)
    if any(k in text for k in ["jwt", "jose", "jsonwebtoken", "auth"]):
        bump(scores, "JWT", weight)
    if any(k in text for k in ["python", "werkzeug", "flask", "fastapi", "django"]):
        bump(scores, "Python", weight)
    if any(k in text for k in ["linux", "bash", "shell", "kali"]):
        bump(scores, "Linux", weight)
    if any(k in text for k in ["cyber", "security", "owasp", "idor", "nmap", "xss", "injection", "pentest"]):
        bump(scores, "Cybersecurity", weight)

def get_file_text(owner: str, repo: str, path: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    try:
        data = gh_get(url)
    except Exception:
        return None

    if isinstance(data, list):
        return None

    content = data.get("content")
    encoding = data.get("encoding")

    if not content:
        return None

    if encoding == "base64":
        try:
            return base64.b64decode(content).decode("utf-8", errors="ignore")
        except Exception:
            return None

    return content

def analyze_package_json(text: str, scores: Counter, weight: int):
    try:
        pkg = json.loads(text)
    except Exception:
        return

    deps = {}
    for section in ["dependencies", "devDependencies", "peerDependencies"]:
        deps.update(pkg.get(section, {}) or {})

    keys = set(k.lower() for k in deps.keys())

    if "react" in keys:
        bump(scores, "React", weight * 3)
    if "typescript" in keys:
        bump(scores, "TypeScript", weight * 2)
    if "react-router-dom" in keys or "@tanstack/react-query" in keys or "@radix-ui/react-slot" in keys:
        bump(scores, "React", weight * 2)
    if "tailwindcss" in keys:
        bump(scores, "React", weight)
    if "vite" in keys:
        bump(scores, "JavaScript", weight)
    if "hono" in keys:
        bump(scores, "JavaScript", weight * 2)
    if "jose" in keys or "jsonwebtoken" in keys:
        bump(scores, "JWT", weight * 2)
    if "pg" in keys or "postgres" in keys or "postgresql" in keys or "kysely" in keys:
        bump(scores, "PostgreSQL", weight * 2)

def analyze_pom(text: str, scores: Counter, weight: int):
    lower = text.lower()
    if "spring-boot" in lower or "org.springframework.boot" in lower:
        bump(scores, "Spring Boot", weight * 3)
        bump(scores, "Java", weight * 2)
    if "postgresql" in lower:
        bump(scores, "PostgreSQL", weight * 2)
    if "jwt" in lower or "jjwt" in lower:
        bump(scores, "JWT", weight * 2)

def analyze_python(text: str, scores: Counter, weight: int):
    lower = text.lower()
    bump(scores, "Python", weight * 2)
    if "werkzeug" in lower or "flask" in lower or "fastapi" in lower or "django" in lower:
        bump(scores, "Python", weight * 2)

def analyze_readme(text: str, scores: Counter, weight: int):
    detect_meta_signals(text.lower(), scores, weight)

def analyze_docker(text: str, scores: Counter, weight: int):
    lower = text.lower()
    bump(scores, "Docker", weight * 2)
    if "postgres" in lower:
        bump(scores, "PostgreSQL", weight)

def analyze_repo(repo: dict, tech_scores: Counter, language_bytes: Counter, analyzed_repos: list):
    name = repo_name(repo)
    owner = repo.get("owner", {}).get("login", USERNAME)
    weight = repo_weight(name)

    if weight == 0:
        return
    if repo.get("fork") or repo.get("archived"):
        return

    analyzed_repos.append(name)

    text = repo_text(repo)
    detect_meta_signals(text, tech_scores, weight)

    languages_url = repo.get("languages_url")
    if languages_url:
        try:
            lang_map = gh_get(languages_url)
            for lang, amount in lang_map.items():
                language_bytes[lang] += int(amount) * weight
        except Exception:
            pass

    for path in PACKAGE_JSON_PATHS:
        content = get_file_text(owner, name, path)
        if content:
            analyze_package_json(content, tech_scores, weight)

    for path in POM_PATHS:
        content = get_file_text(owner, name, path)
        if content:
            analyze_pom(content, tech_scores, weight)

    for path in PYTHON_PATHS:
        content = get_file_text(owner, name, path)
        if content:
            analyze_python(content, tech_scores, weight)

    for path in README_PATHS:
        content = get_file_text(owner, name, path)
        if content:
            analyze_readme(content, tech_scores, weight)

    for path in DOCKER_PATHS:
        content = get_file_text(owner, name, path)
        if content:
            analyze_docker(content, tech_scores, weight)

def detect_techs():
    repos = fetch_repos()

    tech_scores = Counter()
    language_bytes = Counter()
    analyzed_repos = []

    for repo in repos:
        analyze_repo(repo, tech_scores, language_bytes, analyzed_repos)

    for lang, amount in language_bytes.items():
        tech = LANGUAGE_TO_TECH.get(lang)
        if tech:
            tech_scores[tech] += max(1, amount // 50000)

    chosen = []
    for tech in TECH_PRIORITY:
        if tech_scores[tech] > 0:
            chosen.append(tech)

    if not chosen:
        chosen = ["React", "TypeScript", "Java", "Spring Boot", "PostgreSQL", "Docker"]

    return chosen[:10], language_bytes, analyzed_repos[:8]

def build_badge(tech_name: str) -> str:
    item = DOCS[tech_name]
    img = f"![{tech_name}](https://img.shields.io/badge/{item['badge']})"
    if CLICKABLE_BADGES:
        return f"[{img}]({item['url']})"
    return img

def render_section(techs, language_bytes: Counter, analyzed_repos: list) -> str:
    dominant_langs = ", ".join(lang for lang, _ in language_bytes.most_common(5))
    if not dominant_langs:
        dominant_langs = "No dominant language detected yet"

    repo_line = ", ".join(analyzed_repos) if analyzed_repos else "No repositories analyzed"
    badges = " ".join(build_badge(t) for t in techs)
    stack_line = ", ".join(techs)

    return "\n".join([
        "## 🔧 Tech Focus",
        "",
        "> Auto-generated from repository metadata and selected file contents.",
        "",
        f"Analyzed repositories: **{repo_line}**",
        "",
        f"Detected stack signals: **{stack_line}**",
        "",
        f"Weighted language baseline: **{dominant_langs}**",
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
    techs, language_bytes, analyzed_repos = detect_techs()
    new_section = render_section(techs, language_bytes, analyzed_repos)
    updated = replace_block(original, new_section)

    if updated != original:
        README_PATH.write_text(updated, encoding="utf-8")
        print("README updated.")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    main()
