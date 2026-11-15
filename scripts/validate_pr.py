# -*- coding: utf-8 -*-
import sys, json, zipfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

def main():
    errors = []
    reg_path = ROOT / "registry.json"
    if not reg_path.exists():
        print("❌ 缺少根目录 registry.json")
        return 1
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    pkgs = reg.get("packages", [])
    if not isinstance(pkgs, list) or not pkgs:
        errors.append("registry.json 的 packages 必须是非空数组")

    for zpath in sorted((ROOT / "packages").glob("*.zip")):
        with zipfile.ZipFile(zpath, "r") as zf:
            names = zf.namelist()
            if any(n.endswith("data.json") for n in names):
                errors.append(f"[{zpath.name}] 包含废弃的 data.json（强制纯 Markdown 单轨制）")
            if not any(n.endswith(".md") for n in names):
                errors.append(f"[{zpath.name}] 缺少 .md 章节文件")

    if errors:
        for e in errors:
            print("  -", e)
        return 1
    print(f"✅ [1410-share-hub CI 门禁通过] 共校验 {len(pkgs)} 个知识库条目！")
    return 0

if __name__ == "__main__":
    sys.exit(main())
