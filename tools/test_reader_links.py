import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class ReaderLinkTests(unittest.TestCase):
    def test_readme_points_to_this_fork_pages_and_compressed_pdf(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("https://vink567.github.io/codex-orange-book/", readme)
        self.assertIn(
            "https://raw.githubusercontent.com/Vink567/codex-orange-book/main/Codex%E6%A9%99%E7%9A%AE%E4%B9%A6.pdf",
            readme,
        )
        self.assertIn("https://github.com/Vink567/codex-orange-book/blob/main/README.md", readme)

    def test_reader_page_markdown_link_points_to_this_fork(self) -> None:
        index_html = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn("https://github.com/Vink567/codex-orange-book/blob/main/README.md", index_html)
        self.assertNotIn("github.com/bozhouDev/codex-orange-book/blob/main/README.md", index_html)


if __name__ == "__main__":
    unittest.main()
