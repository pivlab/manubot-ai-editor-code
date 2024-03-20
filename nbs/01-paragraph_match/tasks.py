import subprocess
from pathlib import Path
from typing import Annotated

from proj import conf
from pytask import Product


def task_run_paragraph_match_biochatter_gpt35(
    notebook_path: Path = (
        conf.common.NBS_DIR / "01-paragraph_match/00-biochatter-gpt35-par_match.ipynb"
    ),
    output_file: Annotated[Path, Product] = (
        conf.common.PARAGRAPH_MATCH_DIR / "biochatter-manuscript--gpt-3.5-turbo.pkl"
    ),
) -> None:
    command = f"""
    bash {conf.common.CODE_DIR}/scripts/run_nbs.sh \
        {notebook_path} \
        -p OUTPUT_FILE_PATH {str(output_file)}
    """.strip()

    subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)


def task_reverse_paragraph_match_biochatter_gpt35(
    notebook_path: Path = (
        conf.common.NBS_DIR
        / "01-paragraph_match/01-biochatter-gpt35-par_match-reversed.ipynb"
    ),
    input_file: Path = (
        conf.common.PARAGRAPH_MATCH_DIR / "biochatter-manuscript--gpt-3.5-turbo.pkl"
    ),
    output_file: Annotated[Path, Product] = (
        conf.common.PARAGRAPH_MATCH_DIR
        / "biochatter-manuscript--gpt-3.5-turbo--reversed.pkl"
    ),
) -> None:
    command = f"""
    bash {conf.common.CODE_DIR}/scripts/run_nbs.sh \
        {notebook_path} \
        -p INPUT_FILE_PATH {str(input_file)} \
        -p OUTPUT_FILE_PATH {str(output_file)}
    """.strip()

    subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)
