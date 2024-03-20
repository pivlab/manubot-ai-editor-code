import os
import subprocess
from pathlib import Path
from typing import Annotated

from proj import conf
from proj.utils import simplify_filename
from pytask import Product, task

MANUSCRIPT_REPOSITORIES = {
    "pivlab/manubot-ai-editor-code-test-biochatter-manuscript": {
        "gpt-3.5-turbo": 2,
        # "gpt-4-0125-preview": 3,
    }
}

LLM_JUDGES = [
    "mistral:7b-instruct-fp16",
    "openai:gpt-4-turbo-preview",
]

# Model and its parameters
TEMPERATURE = 0.5
MAX_TOKENS = 2000
SEED_INIT = 0

# Evaluation parameters
N_REPS = 10

# Paths
input_notebook_dir = conf.common.NBS_DIR / "05-llm_evaluation"
input_notebook_name_template = "00-llm_pairwise-{suffix}.{ext}"

output_notebook_dir = input_notebook_dir / "output"
output_notebook_dir.mkdir(exist_ok=True, parents=True)

#
# Reverse the paragraphs (only for one of the manuscripts)
#
for llm_judge in LLM_JUDGES:
    manuscript_code = "biochatter-manuscript"
    manuscript_pr_code = f"{manuscript_code}-gpt-3.5-turbo--reversed"
    manuscript_pr_llm_judge_code = f"{manuscript_pr_code}--{llm_judge}"
    task_id = f"run_llm_pairwise-{manuscript_pr_llm_judge_code}"

    input_notebook_py_path = (
        input_notebook_dir
        / "py"
        / input_notebook_name_template.format(
            suffix="template",
            ext="py",
        )
    )

    output_notebook_path = (
        output_notebook_dir.name
        + os.sep
        + simplify_filename(
            input_notebook_name_template.format(
                suffix=manuscript_pr_llm_judge_code, ext="ipynb"
            )
        )
    )

    @task(id=task_id)
    def run_llm_pairwise(
        input_notebook_py_path: Path = input_notebook_py_path,
        output_notebook_path: str = output_notebook_path,
        repository: str = "None",
        llm_judge: str = llm_judge,
        input_file: Path = (
            conf.common.PARAGRAPH_MATCH_DIR
            / "biochatter-manuscript--gpt-3.5-turbo--reversed.pkl"
        ),
        output_file: Annotated[Path, Product] = (
            conf.common.LLM_PAIRWISE_DIR
            / simplify_filename(f"{manuscript_pr_llm_judge_code}.pkl")
        ),
    ) -> None:
        input_notebook_path = (
            input_notebook_py_path.parent.parent
            / input_notebook_py_path.with_suffix(".ipynb").name
        )

        command = f"""
        bash {conf.common.CODE_DIR}/scripts/run_nbs.sh \
            {str(input_notebook_path)} \
            {str(output_notebook_path)} \
            -p REPO {repository} \
            -p INPUT_FILE {str(input_file)} \
            -p OUTPUT_FILE {str(output_file)} \
            -p LLM_JUDGE {llm_judge} \
            -p TEMPERATURE {TEMPERATURE} \
            -p MAX_TOKENS {MAX_TOKENS} \
            -p SEED_INIT {SEED_INIT} \
            -p N_REPS {N_REPS}
        """.strip()

        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)


#
# Run the LLM pairwise comparison
#
for repo, prs in MANUSCRIPT_REPOSITORIES.items():
    for pr_model in prs.keys():
        manuscript_pr_code = f"{repo.split('-test-')[1]}--{pr_model}"
        input_file = conf.common.PARAGRAPH_MATCH_DIR / f"{manuscript_pr_code}.pkl"

        for llm_judge in LLM_JUDGES:
            manuscript_pr_llm_judge_code = f"{manuscript_pr_code}--{llm_judge}"
            task_id = f"run_llm_pairwise-{manuscript_pr_llm_judge_code}"

            input_notebook_py_path = (
                input_notebook_dir
                / "py"
                / input_notebook_name_template.format(suffix="template", ext="py")
            )

            output_notebook_path = (
                output_notebook_dir.name
                + os.sep
                + simplify_filename(
                    input_notebook_name_template.format(
                        suffix=manuscript_pr_llm_judge_code,
                        ext="ipynb",
                    )
                )
            )

            @task(id=task_id)
            def run_llm_pairwise(
                input_notebook_py_path: Path = input_notebook_py_path,
                output_notebook_path: str = output_notebook_path,
                repository: str = repo,
                input_file: Path = input_file,
                output_file: Annotated[Path, Product] = (
                    conf.common.LLM_PAIRWISE_DIR
                    / simplify_filename(f"{manuscript_pr_llm_judge_code}.pkl")
                ),
                llm_judge: str = llm_judge,
            ) -> None:
                input_notebook_path = (
                    input_notebook_py_path.parent.parent
                    / input_notebook_py_path.with_suffix(".ipynb").name
                )

                command = f"""
                bash {conf.common.CODE_DIR}/scripts/run_nbs.sh \
                    {str(input_notebook_path)} \
                    {str(output_notebook_path)} \
                    -p REPO {repository} \
                    -p INPUT_FILE {str(input_file)} \
                    -p OUTPUT_FILE {str(output_file)} \
                    -p LLM_JUDGE {llm_judge} \
                    -p TEMPERATURE {TEMPERATURE} \
                    -p MAX_TOKENS {MAX_TOKENS} \
                    -p SEED_INIT {SEED_INIT} \
                    -p N_REPS {N_REPS}
                """.strip()

                subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)
