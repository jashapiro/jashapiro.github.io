"""Publish the CV PDF at its old address.

Run by Quarto as a project post-render script (see `_quarto.yml`), so it uses
only the standard library: CI runs it with the system python3, not pixi.
Copies the PDF rendered from `cv.qmd` (`_site/cv.pdf`) to
`_site/docs/JAShapiro_CV.pdf`, where the hand-made CV used to be, so old links
get the current CV.
"""

import os
import shutil
from pathlib import Path

OUTPUT = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
SOURCE = OUTPUT / "cv.pdf"
TARGET = OUTPUT / "docs" / "JAShapiro_CV.pdf"


def main() -> None:
    # not there if the render didn't include the CV's PDF
    if not SOURCE.exists():
        return
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)


if __name__ == "__main__":
    main()
