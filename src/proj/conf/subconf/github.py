"""
Contains configuration to use GitHub API.
"""
import os
from pathlib import Path

from proj.conf.common import ENV_PREFIX as __ENV_PREFIX

__ENV_PREFIX += f"{Path(__file__).stem.upper()}_"

API_TOKEN = os.environ.get(f"{__ENV_PREFIX}AUTH_TOKEN")
