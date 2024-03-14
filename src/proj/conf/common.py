import os
from pathlib import Path

from proj.conf import main, ENV_PREFIX

# CODE_DIR points to the base directory where the code is
CODE_DIR = Path(main.__file__).parent.parent.parent.parent.resolve()

# ROOT_DIR points to the base directory where all the data and results are
ROOT_DIR = os.environ.get(f"{ENV_PREFIX}ROOT_DIR")
if ROOT_DIR is None:
    ROOT_DIR = str(CODE_DIR / "base")

# DATA_DIR stores input data
DATA_DIR = Path(ROOT_DIR, "data").resolve()

# RESULTS_DIR stores newly generated data
RESULTS_DIR = Path(ROOT_DIR, "results").resolve()

# N_JOBS
options = [
    m if (m := os.environ.get(f"{ENV_PREFIX}N_JOBS")) is not None and m.strip() != "" else None,
    1,
]
N_JOBS = next(int(opt) for opt in options if opt is not None)
