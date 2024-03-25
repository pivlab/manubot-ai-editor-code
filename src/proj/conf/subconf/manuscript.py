"""
Contains configuration regarding the manuscript.
"""

import os
from pathlib import Path

from proj.conf.common import ENV_PREFIX as __ENV_PREFIX

__ENV_PREFIX += f"{Path(__file__).stem.upper()}_"

DIR = os.environ.get(f"{__ENV_PREFIX}DIR", None)
if DIR is not None and DIR.strip() != "":
    DIR = Path(DIR).resolve()
else:
    DIR = None
