"""Run local quality gates for Git hooks and CI."""

from __future__ import annotations

import argparse
import compileall
import importlib.util
import os
import re
import subprocess  # nosec B404
import sys
from collections.abc import Sequence
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LANGUAGE_DATA = {
    "English": REPO_ROOT / "data" / "affirmations_en.txt",
    "Hindi": REPO_ROOT / "data" / "affirmations_hi.txt",
    "Telugu": REPO_ROOT / "data" / "affirmations_te.txt",
}
SECRET_PATTERNS = [
    re.compile(
        r"(?i)(api[_-]?key|secret|token|password)\s*=\s*['\"][^'\"\s]{12,}['\"]"
    ),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)ghp_[A-Za-z0-9_]{20,}"),
]
TEXT_SUFFIXES = {
    ".cfg",
    ".css",
    ".env",
    ".example",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}


def run(command: Sequence[str], label: str) -> bool:
    print(f"\n==> {label}")
    print(" ".join(command))
    completed = subprocess.run(command, cwd=REPO_ROOT, check=False)  # nosec B603

    if completed.returncode == 0:
        print(f"OK: {label}")
        return True

    print(f"FAIL: {label}")
    return False


def run_python_module_if_available(
    module_name: str,
    module_args: Sequence[str],
    label: str,
    *,
    required: bool,
) -> bool:
    if importlib.util.find_spec(module_name):
        return run([sys.executable, "-m", module_name, *module_args], label)

    message = (
        f"Missing tool: {module_name}. Install development checks with "
        "`python -m pip install -r requirements-dev.txt`."
    )

    if required:
        print(f"\nFAIL: {message}")
        return False

    print(f"\nSKIP: {message}")
    return True


def check_compile() -> bool:
    print("\n==> Compile Python")
    paths = [
        str(REPO_ROOT / "app.py"),
        str(REPO_ROOT / "scripts"),
        str(REPO_ROOT / "tests"),
    ]
    ok = bool(compileall.compile_file(paths[0], quiet=1))

    for path in paths[1:]:
        if Path(path).exists():
            ok = bool(compileall.compile_dir(path, quiet=1)) and ok

    print("OK: Compile Python" if ok else "FAIL: Compile Python")
    return ok


def tracked_files() -> list[Path]:
    completed = subprocess.run(  # nosec B603 B607
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [REPO_ROOT / line for line in completed.stdout.splitlines() if line]


def is_text_file(path: Path) -> bool:
    if path.suffix in TEXT_SUFFIXES:
        return True

    return path.name in {".env.example", ".gitignore", ".pre-commit-config.yaml"}


def check_secrets() -> bool:
    print("\n==> Secret scan")
    failures: list[str] = []

    for path in tracked_files():
        if not path.is_file() or not is_text_file(path):
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                failures.append(str(path.relative_to(REPO_ROOT)))
                break

    if failures:
        print("FAIL: Potential secrets found in tracked files:")
        for failure in failures:
            print(f"- {failure}")
        return False

    print("OK: Secret scan")
    return True


def check_affirmation_data() -> bool:
    print("\n==> Affirmation data compliance")
    ok = True

    for language, path in LANGUAGE_DATA.items():
        if not path.exists():
            print(f"FAIL: Missing {language} data file: {path.relative_to(REPO_ROOT)}")
            ok = False
            continue

        lines = [
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

        if not lines:
            print(f"FAIL: {language} affirmation file is empty.")
            ok = False
            continue

        if len(lines) != len(set(lines)):
            print(f"FAIL: {language} affirmation file contains duplicates.")
            ok = False

    print(
        "OK: Affirmation data compliance" if ok else "FAIL: Affirmation data compliance"
    )
    return ok


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["pre-commit", "pre-push"], required=True)
    args = parser.parse_args()

    required_optional_tools = os.environ.get("LOCAL_CHECKS_STRICT", "0") == "1"
    checks = [
        run_python_module_if_available(
            "ruff",
            ["format", "--check", "."],
            "Format check",
            required=True,
        ),
        run_python_module_if_available(
            "ruff",
            ["check", "."],
            "Lint check",
            required=True,
        ),
        check_compile(),
        run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests"], "Unit tests"
        ),
        check_secrets(),
        check_affirmation_data(),
    ]

    if args.stage == "pre-push":
        checks.extend(
            [
                run_python_module_if_available(
                    "mypy",
                    ["app.py", "scripts", "tests"],
                    "Type check",
                    required=required_optional_tools,
                ),
                run_python_module_if_available(
                    "vulture",
                    ["app.py", "scripts", "tests", "--min-confidence", "80"],
                    "Dead code check",
                    required=required_optional_tools,
                ),
                run_python_module_if_available(
                    "bandit",
                    ["-q", "-r", "app.py", "scripts"],
                    "Security check",
                    required=required_optional_tools,
                ),
                run_python_module_if_available(
                    "pip_audit",
                    ["--local"],
                    "Package audit",
                    required=required_optional_tools,
                ),
            ]
        )

    if all(checks):
        print("\nAll local checks passed.")
        return 0

    print("\nOne or more local checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
