import subprocess
from pathlib import Path
from typing import Annotated

from proj import conf
from pytask import Product


def task_run_paragraph_match_biochatter_gpt35(
    notebook_py_path: Path = (
        conf.common.NBS_DIR / "01-paragraph_match/py/00-biochatter-gpt35-par_match.py"
    ),
    output_file: Annotated[Path, Product] = (
        conf.common.PARAGRAPH_MATCH_DIR / "biochatter-manuscript--gpt-3.5-turbo.pkl"
    ),
) -> None:
    notebook_path = (
        notebook_py_path.parent.parent / notebook_py_path.with_suffix(".ipynb").name
    )

    command = f"""
    bash {conf.common.CODE_DIR}/scripts/run_nbs.sh \
        {notebook_path} \
        -p OUTPUT_FILE_PATH {str(output_file)}
    """.strip()

    subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)


def task_reverse_paragraph_match_biochatter_gpt35(
    notebook_py_path: Path = (
        conf.common.NBS_DIR
        / "01-paragraph_match/py/01-biochatter-gpt35-par_match-reversed.py"
    ),
    input_file: Path = (
        conf.common.PARAGRAPH_MATCH_DIR / "biochatter-manuscript--gpt-3.5-turbo.pkl"
    ),
    output_file: Annotated[Path, Product] = (
        conf.common.PARAGRAPH_MATCH_DIR
        / "biochatter-manuscript--gpt-3.5-turbo--reversed.pkl"
    ),
) -> None:
    notebook_path = (
        notebook_py_path.parent.parent / notebook_py_path.with_suffix(".ipynb").name
    )

    command = f"""
    bash {conf.common.CODE_DIR}/scripts/run_nbs.sh \
        {notebook_path} \
        -p INPUT_FILE_PATH {str(input_file)} \
        -p OUTPUT_FILE_PATH {str(output_file)}
    """.strip()

    subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)


def task_run_paragraph_match_ccc_gpt35(
    notebook_py_path: Path = (
        conf.common.NBS_DIR / "01-paragraph_match/py/05-ccc-gpt35-par_match.py"
    ),
    output_file: Annotated[Path, Product] = (
        conf.common.PARAGRAPH_MATCH_DIR / "ccc-manuscript--gpt-3.5-turbo.pkl"
    ),
) -> None:
    notebook_path = (
        notebook_py_path.parent.parent / notebook_py_path.with_suffix(".ipynb").name
    )

    command = f"""
    bash {conf.common.CODE_DIR}/scripts/run_nbs.sh \
        {notebook_path} \
        -p OUTPUT_FILE_PATH {str(output_file)}
    """.strip()

    subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)
