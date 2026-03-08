from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from module_registry import (  # noqa: E402
    GROUP_ORDER,
    PAGE_REGISTRY,
    count_pages_by_group,
    get_grouped_pages,
    get_teaching_modules,
)


def main() -> int:
    errors: list[str] = []

    for page in PAGE_REGISTRY:
        if not page.group:
            errors.append(f"分组为空: {page.slug}")
        if not page.title:
            errors.append(f"标题为空: {page.slug}")
        if not page.icon:
            errors.append(f"图标为空: {page.slug}")
        if not page.core_concepts:
            errors.append(f"核心考点为空: {page.slug}")
        if not (ROOT / page.page_path).exists():
            errors.append(f"页面不存在: {page.page_path}")

    grouped = get_grouped_pages()
    if list(grouped.keys()) != GROUP_ORDER:
        errors.append("导航分组顺序与 GROUP_ORDER 不一致")

    if len(get_teaching_modules()) != 12:
        errors.append("教学模块数量不是 12")

    counts = count_pages_by_group()
    if sum(counts.values()) != len(PAGE_REGISTRY):
        errors.append("分组统计总数与注册表总数不一致")

    if errors:
        print("Registry validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Registry validation passed.")
    print(f"Total pages: {len(PAGE_REGISTRY)}")
    print(f"Teaching modules: {len(get_teaching_modules())}")
    for group, count in counts.items():
        print(f"- {group}: {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
