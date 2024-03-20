import subprocess
from pathlib import Path
from typing import Annotated

from proj import conf
from pytask import Product

MANUSCRIPT_REPOSITORIES = {
    "pivlab/manubot-ai-editor-code-test-biochatter-manuscript": {
        "gpt-3.5-turbo": 2,
        "gpt-4-0125-preview": 3,
    }
}

LLM_JUDGES = [
    "mistral:7b-instruct-fp16",
    "openai:gpt-4-turbo-preview",
    "openai:gpt-3.5-turbo",
]

# Model and its parameters
TEMPERATURE = 0.5
MAX_TOKENS = 2000
SEED_INIT = 0

# Evaluation parameters
N_REPS = 10


def task_run_paragraph_match_biochatter_gpt35(
    notebook_path: Path = conf.common.NBS_DIR
    / "01-paragraph_match/00-biochatter-gpt35-par_match.ipynb",
    output_file: Annotated[Path, Product] = conf.common.PARAGRAPH_MATCH_DIR
    / "biochatter-manuscript--gpt-3.5-turbo.pkl",
) -> None:
    command = f"""
    bash {conf.common.CODE_DIR}/scripts/run_nbs.sh \
        {notebook_path} \
        -p OUTPUT_FILE_PATH {str(output_file)}
    """.strip()

    return subprocess.run(
        command, shell=True, check=True, stdout=subprocess.PIPE
    ).stdout


# for repo, prs in MANUSCRIPT_REPOSITORIES.items():
#     manuscript_code = repo.split("-test-")[1]
#
#     for pr_model, pr_number in prs.items():
#         for llm_judge in LLM_JUDGES:
#             task_id = f"run_llm_pairwise-{manuscript_code}_{pr_model}-{llm_judge}"
#
#             @task(id=task_id)
#             def task_run_llm_pairwise(
#                     repository: str = repo,
#                     llm_judge: str = llm_judge,
#                     input_file: Path = (
#                             conf.common.PARAGRAPH_MATCH_DIR / manuscript_code).with_suffix(
#                         ".pkl"),
#                     output_file: Annotated[Path, Product] = (
#                             conf.common.LLM_PAIRWISE_DIR / manuscript_code).with_suffix(
#                         ".pkl"),
#             ) -> None:
#                 command
#                 f"""
#                 bash {conf.common.CODE_DIR}/scripts/run_nbs.sh
#                 """
