from pathlib import Path
import unittest


from module_registry import (
    GROUP_ORDER,
    PAGE_REGISTRY,
    get_teaching_modules,
)


ROOT = Path(__file__).resolve().parents[1]


class ModuleRegistryTests(unittest.TestCase):
    def test_group_order_matches_product_structure(self) -> None:
        self.assertEqual(
            GROUP_ORDER,
            ["项目总览", "基础理论", "变换域分析", "系统与通信"],
        )

    def test_teaching_module_count_is_twelve(self) -> None:
        self.assertEqual(len(get_teaching_modules()), 12)

    def test_registry_entries_have_unique_slugs(self) -> None:
        slugs = [page.slug for page in PAGE_REGISTRY]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_registry_page_paths_exist(self) -> None:
        for page in PAGE_REGISTRY:
            self.assertTrue((ROOT / page.page_path).exists(), page.page_path)


if __name__ == "__main__":
    unittest.main()
