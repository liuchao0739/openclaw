#!/usr/bin/env python3
"""Generate phase-2 migration tasks from OpenClaw TS source tree."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

SOURCE = Path("/Users/liuchao/openclaw")
TARGET = Path("/Users/liuchao/openclaw-py")
OUT = SOURCE / "migration" / "progress-phase2.json"

SKIP_PARTS = {"test-helpers", "test-utils", "__pycache__"}


def count_ts_files(path: Path) -> int:
    return len([p for p in path.rglob("*.ts") if not p.name.endswith(".test.ts")])


def py_target_for(rel: str) -> str:
    rel = rel.replace("src/", "openclaw/").replace("packages/", "openclaw_packages/")
    return rel.replace("-", "_")


def add_task(tasks: list[dict], task_id: int, title: str, source: str, target: str, files: int) -> int:
    tasks.append(
        {
            "id": f"P2-{task_id:04d}",
            "phase": "phase-2-full",
            "title": title,
            "source_paths": [source],
            "target_paths": [target],
            "file_count": files,
            "status": "pending",
            "acceptance": f"pytest passes for {target}",
        }
    )
    return task_id + 1


def walk_module(tasks: list[dict], task_id: int, module_root: Path, prefix: str) -> int:
    if not module_root.is_dir():
        return task_id

    direct_files = count_ts_files(module_root) - sum(
        count_ts_files(p) for p in module_root.iterdir() if p.is_dir() and p.name not in SKIP_PARTS
    )
    subdirs = sorted(
        [p for p in module_root.iterdir() if p.is_dir() and p.name not in SKIP_PARTS],
        key=lambda p: p.name,
    )

    for sub in subdirs:
        files = count_ts_files(sub)
        if files == 0:
            continue
        rel = f"{prefix}/{sub.name}"
        target = py_target_for(rel)
        if files >= 15:
            task_id = walk_module(tasks, task_id, sub, rel)
        else:
            task_id = add_task(tasks, task_id, f"移植 {rel}", rel, target, files)

    loose = len([p for p in module_root.glob("*.ts") if not p.name.endswith(".test.ts")])
    if loose >= 5:
        task_id = add_task(
            tasks,
            task_id,
            f"移植 {prefix} 根文件",
            prefix,
            py_target_for(prefix),
            loose,
        )
    return task_id


def main() -> None:
    tasks: list[dict] = []
    task_id = 1

    src = SOURCE / "src"
    for module in sorted(p for p in src.iterdir() if p.is_dir()):
        if module.name in SKIP_PARTS:
            continue
        files = count_ts_files(module)
        if files == 0:
            continue
        prefix = f"src/{module.name}"
        if files >= 40:
            task_id = walk_module(tasks, task_id, module, prefix)
        else:
            task_id = add_task(
                tasks,
                task_id,
                f"移植 {prefix}",
                prefix,
                py_target_for(prefix),
                files,
            )

    packages = SOURCE / "packages"
    for pkg in sorted(p for p in packages.iterdir() if p.is_dir()):
        pkg_src = pkg / "src"
        if not pkg_src.is_dir():
            continue
        files = count_ts_files(pkg_src)
        if files == 0:
            continue
        prefix = f"packages/{pkg.name}"
        task_id = add_task(
            tasks,
            task_id,
            f"移植 {prefix}",
            prefix,
            py_target_for(prefix),
            files,
        )

    extensions = SOURCE / "extensions"
    ext_count = 0
    for ext in sorted(p for p in extensions.iterdir() if p.is_dir()):
        manifest = ext / "openclaw.plugin.json"
        if not manifest.exists():
            continue
        files = count_ts_files(ext)
        if files == 0:
            continue
        ext_count += 1
        if ext_count <= 50:
            task_id = add_task(
                tasks,
                task_id,
                f"移植 extension {ext.name}",
                f"extensions/{ext.name}",
                f"openclaw_extensions/{ext.name}",
                files,
            )

    payload = {
        "version": "2.0.0",
        "source_repo": str(SOURCE),
        "target_repo": str(TARGET),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stats": {
            "total": len(tasks),
            "done": 0,
            "pending": len(tasks),
            "failed": 0,
        },
        "current_phase": "phase-2-full",
        "current_task": tasks[0]["id"] if tasks else None,
        "tasks": tasks,
        "notes": "Phase-2 auto-generated from src/, packages/, and first 50 extensions.",
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Generated {len(tasks)} tasks -> {OUT}")


if __name__ == "__main__":
    main()
