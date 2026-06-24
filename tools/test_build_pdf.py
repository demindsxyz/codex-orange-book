import tempfile
import os
import sys
import types
import unittest
from pathlib import Path

from PIL import Image

sys.modules.setdefault("markdown", types.SimpleNamespace(Markdown=object))

import build_pdf


class BuildPdfAssetTests(unittest.TestCase):
    def test_build_outputs_preview_pdf_without_overwriting_original_download(self) -> None:
        self.assertEqual(build_pdf.OUTPUT_PDF.name, "Codex橙皮书.preview.pdf")

    def test_resolve_chrome_prefers_env_path(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            fake_chrome = Path(raw_tmp) / "chrome"
            fake_chrome.write_text("", encoding="utf-8")
            old_value = os.environ.get("CHROME_PATH")
            os.environ["CHROME_PATH"] = str(fake_chrome)
            try:
                self.assertEqual(build_pdf.resolve_chrome(), fake_chrome)
            finally:
                if old_value is None:
                    os.environ.pop("CHROME_PATH", None)
                else:
                    os.environ["CHROME_PATH"] = old_value

    def test_prepare_pdf_assets_rewrites_local_png_to_optimized_jpeg(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            tmp_path = Path(raw_tmp)
            source = tmp_path / "assets" / "images" / "sample.png"
            source.parent.mkdir(parents=True)
            Image.new("RGB", (2000, 1000), "#f2660a").save(source)

            html = '<p><img src="assets/images/sample.png" alt="sample" width="860"></p>'

            optimized = build_pdf.prepare_pdf_assets(html, tmp_path)

            expected = tmp_path / ".cache" / "pdf-assets" / "assets" / "images" / "sample.jpg"
            self.assertTrue(expected.exists())
            self.assertIn('src=".cache/pdf-assets/assets/images/sample.jpg"', optimized)

            with Image.open(expected) as image:
                self.assertEqual(image.format, "JPEG")
                self.assertLessEqual(image.width, build_pdf.PDF_IMAGE_MAX_WIDTH)
                self.assertLess(image.height, 1000)


if __name__ == "__main__":
    unittest.main()
