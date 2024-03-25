"""
Contains configuration regarding the manuscript.
"""

import os
import tempfile
from pathlib import Path

from proj.conf.common import ENV_PREFIX as __ENV_PREFIX

__ENV_PREFIX += f"{Path(__file__).stem.upper()}_"

DIR = os.environ.get(f"{__ENV_PREFIX}DIR", None)
if DIR is None or DIR.strip() == "":
    DIR = tempfile.TemporaryDirectory().name
DIR = Path(DIR).resolve()

FIGURES_DIR = DIR / "content" / "images"
SUPPLEMENTARY_MATERIAL_DIR = DIR / "content" / "supplementary_files"
