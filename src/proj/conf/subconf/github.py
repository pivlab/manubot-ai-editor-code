"""
Contains configuration to use GitHub API.
"""
import os

from proj.conf import common

API_TOKEN = os.environ.get(f"{common.ENV_PREFIX}GITHUB_AUTH_TOKEN")
