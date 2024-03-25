# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all,-execution,-papermill,-trusted
#     notebook_metadata_filter: -jupytext.text_representation.jupytext_version
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Description

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# Analyzes some specific paragraphs.

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Modules

# %% editable=true slideshow={"slide_type": ""} tags=[]
from pathlib import Path

import pandas as pd
from IPython.display import display
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from proj import conf

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Settings/paths

# %% editable=true slideshow={"slide_type": ""} tags=["parameters"]
OUTPUT_FILE = None

# %% tags=["injected-parameters"]
# Parameters
OUTPUT_FILE = "/home/miltondp/projects/others/manubot/manubot-gpt-manuscript/content/supplementary_files/Supplementary_File_05-Automatic_assessment.xlsx"


# %% editable=true slideshow={"slide_type": ""} tags=[]
INPUT_DIR = conf.common.LLM_PAIRWISE_DIR
assert INPUT_DIR.exists()
display(INPUT_DIR)

# %% editable=true slideshow={"slide_type": ""} tags=[]
assert (
    OUTPUT_FILE is not None and OUTPUT_FILE.strip() != ""
), "Output file not specified"
OUTPUT_FILE = Path(OUTPUT_FILE).resolve()

assert OUTPUT_FILE.suffix == ".xlsx", "Output file should have the .xslx extension"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Load LLM pairwise files

# %% editable=true slideshow={"slide_type": ""} tags=[]
result_files = list(INPUT_DIR.glob("*.pkl"))
display(len(result_files))
display(result_files[:2])

# %% tags=[]
pd.read_pickle(result_files[0])

# %% tags=[]
result_files[0].name.split("--")

# %% editable=true slideshow={"slide_type": ""} tags=[]
all_results = []

for f in result_files:
    print(f.name, flush=True)
    df = pd.read_pickle(f)

    f_name_parts = f.name.split("--")
    idx = 0
    manuscript_code = f_name_parts[idx]
    manuscript_code = manuscript_code.split("-manuscript")[0]
    idx += 1

    manuscript_pr_model = f_name_parts[idx]
    idx += 1

    reversed_paragraphs = False
    if len(f_name_parts) > 3:
        reversed_paragraphs = f_name_parts[idx] == "reversed"
        idx += 1

    llm_judge = f_name_parts[idx].split(".pkl")[0]

    df.insert(0, "llm_judge", llm_judge)
    df.insert(0, "paragraphs_reversed", reversed_paragraphs)
    df.insert(0, "pr_model", manuscript_pr_model)
    df.insert(0, "manuscript_code", manuscript_code)

    all_results.append(df)

# %% tags=[]
df = pd.concat(all_results, ignore_index=True)

# %% editable=true slideshow={"slide_type": ""} tags=[]
df.shape

# %% editable=true slideshow={"slide_type": ""} tags=[]
df.head()

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Process data for plotting

# %% tags=[]
df["llm_judge"].unique()

# %% tags=[]
df["manuscript_code"].unique()

# %% tags=[]
df["paragraph_section"].unique()

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Clean illegal characters for openpyxl

# %% tags=[]
df = df.replace(ILLEGAL_CHARACTERS_RE, "", regex=True)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Save

# %% editable=true slideshow={"slide_type": ""} tags=[]
df.to_excel(OUTPUT_FILE)

# %% tags=[]
