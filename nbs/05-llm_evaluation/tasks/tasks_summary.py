import subprocess
from pathlib import Path
from typing import Annotated

from proj import conf
from pytask import Product, task


#
# Summarize
#
@task(after="run_llm_pairwise")
def task_summarize(
    notebook_py_path: Path = (
        conf.common.NBS_DIR / "05-llm_evaluation/py/10-summarize.py"
    ),
    output_image: Annotated[Path, Product] = (
        conf.manuscript.FIGURES_DIR / "llm_judge.svg"
    ),
) -> None:
    notebook_path = (
        notebook_py_path.parent.parent / notebook_py_path.with_suffix(".ipynb").name
    )

    command = f"""
    bash {conf.common.CODE_DIR}/scripts/run_nbs.sh \
        {notebook_path} \
        -p OUTPUT_FIGURE_FILE {str(output_image)}
    """.strip()

    subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)


# #
# # Save scores
# #
# def task_save_scores(
#     notebook_py_path: Path = (
#         conf.common.NBS_DIR / "05-llm_evaluation/py/15-save_scores.py"
#     ),
#     output_file: Annotated[Path, Product] = (
#         conf.manuscript.SUPPLEMENTARY_MATERIAL_DIR
#         / "Supplementary_File_05-Automatic_assessment.xlsx"
#     ),
# ) -> None:
#     notebook_path = (
#         notebook_py_path.parent.parent / notebook_py_path.with_suffix(".ipynb").name
#     )
# 
#     command = f"""
#     bash {conf.common.CODE_DIR}/scripts/run_nbs.sh \
#         {notebook_path} \
#         -p OUTPUT_FILE_PATH {str(output_file)}
#     """.strip()
# 
#     subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)
