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
# This notebook reads previous results and reverses the original/modified paragraphs to assess consistency and check for "position bias".

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Modules

# %% editable=true slideshow={"slide_type": ""} tags=[]
from pathlib import Path

import pandas as pd
from IPython.display import display

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Settings/paths

# %% editable=true slideshow={"slide_type": ""} tags=["parameters"]
INPUT_FILE_PATH = None
OUTPUT_FILE_PATH = None

# %% tags=["injected-parameters"]
# Parameters
INPUT_FILE_PATH = "/home/miltondp/projects/others/manubot/manubot-ai-editor-code/base/results/paragraph_match/biochatter-manuscript--gpt-3.5-turbo.pkl"
OUTPUT_FILE_PATH = "/home/miltondp/projects/others/manubot/manubot-ai-editor-code/base/results/paragraph_match/biochatter-manuscript--gpt-3.5-turbo--reversed.pkl"


# %% editable=true slideshow={"slide_type": ""} tags=[]
OUTPUT_FILE_PATH = Path(OUTPUT_FILE_PATH).resolve()
OUTPUT_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
display(OUTPUT_FILE_PATH)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Load input data

# %% editable=true slideshow={"slide_type": ""} tags=[]
df = pd.read_pickle(INPUT_FILE_PATH)

# %% editable=true slideshow={"slide_type": ""} tags=[]
df.shape

# %% editable=true slideshow={"slide_type": ""} tags=[]
df.head()

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Reverse original/modified columns

# %% editable=true slideshow={"slide_type": ""} tags=[]
df = df.rename(columns={"original": "modified2"}).rename(
    columns={"modified": "original", "modified2": "modified"}
)

# %% editable=true slideshow={"slide_type": ""} tags=[]
df.shape

# %% editable=true slideshow={"slide_type": ""} tags=[]
df.head()

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Save

# %% tags=[]
df.to_pickle(OUTPUT_FILE_PATH)

# %% editable=true slideshow={"slide_type": ""} tags=[]
