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
# TODO

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Modules

# %% editable=true slideshow={"slide_type": ""} tags=[]
import pandas as pd
import seaborn as sns
from IPython.display import display
from proj import conf

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Settings/paths

# %% editable=true slideshow={"slide_type": ""} tags=["parameters"]
# # Input manuscript
# REPO = None

# INPUT_FILE = None
# OUTPUT_FILE = None

# # Model and its parameters
# LLM_JUDGE = None
# TEMPERATURE = None
# MAX_TOKENS = 2000
# SEED_INIT = 0

# # Evaluation parameters
# N_REPS = None

# %% editable=true slideshow={"slide_type": ""} tags=[]
INPUT_DIR = conf.common.LLM_PAIRWISE_DIR
assert INPUT_DIR.exists()
display(INPUT_DIR)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Load LLM pairwise files

# %% editable=true slideshow={"slide_type": ""} tags=[]
result_files = list(INPUT_DIR.glob("*.pkl"))
display(len(result_files))
display(result_files[:2])

# %%
pd.read_pickle(result_files[0])

# %%
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

# %%
df = pd.concat(all_results, ignore_index=True)

# %% editable=true slideshow={"slide_type": ""} tags=[]
df.shape

# %% editable=true slideshow={"slide_type": ""} tags=[]
df.head()

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Process data for plotting

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ## Reverse scores for reversed paragraphs

# %%
df.loc[df["paragraphs_reversed"], "winner_score"] = (
    -1 * df.loc[df["paragraphs_reversed"], "winner_score"]
)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ## Rename values

# %%
df["llm_judge"].unique()

# %%
models_rename = {
    "openai_gpt-4": "GPT-4",
    "openai_gpt-4-turbo-preview": "GPT-4 Turbo",
    "openai_gpt-3.5-turbo": "GPT 3.5 Turbo",
    "mistral_7b-instruct-fp16": "Mistral 7b",
}

# %%
df["manuscript_code"].unique()

# %%
df["paragraph_section"].unique()

# %%
df = df.replace(
    {
        "manuscript_code": {
            "biochatter": "BioChatter",
            "ccc": "CCC",
            "phenoplier": "PhenoPLIER",
            "epistasis": "Epistasis",
        },
        "pr_model": models_rename,
        "llm_judge": models_rename,
        "paragraph_section": {
            "abstract": "Abstract",
            "introduction": "Introduction",
            "results": "Results",
            "methods": "Methods",
            "discussion": "Discussion",
            "supplementary material": "Supplementary\nmaterial",
        },
    }
)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Plot

# %% editable=true slideshow={"slide_type": ""} tags=[]
with sns.axes_style("whitegrid"):
    g = sns.catplot(
        data=df,
        x="paragraph_section",
        y="winner_score",
        row="manuscript_code",
        col="llm_judge",
        kind="point",
        hue="paragraphs_reversed",
    )
    g.set_axis_labels("", "Revision score")
    g.set_titles("{row_name} manuscript | judge: {col_name}")
    g.tick_params(axis="x", rotation=30)

# %% editable=true slideshow={"slide_type": ""} tags=[]
with sns.axes_style("whitegrid"):
    g = sns.catplot(
        height=5,
        aspect=1.3,
        data=df,
        x="paragraph_section",
        y="winner_score",
        col="manuscript_code",
        col_order=["CCC", "PhenoPLIER", "BioChatter", "Epistasis"],
        col_wrap=2,
        kind="point",
        hue="llm_judge",
    )
    g.set_axis_labels("", "Revision score")
    g.set_titles("{col_name} manuscript")
    # g.tick_params(axis='x', rotation=30)
    # g.set_xticklabels(g.ax.get_xticklabels(), rotation=30)

# %% editable=true slideshow={"slide_type": ""} tags=[]
with sns.axes_style("whitegrid"):
    g = sns.catplot(
        height=5,
        aspect=1.3,
        data=df[df["llm_judge"] == "GPT 3.5 Turbo"],
        x="paragraph_section",
        y="winner_score",
        hue="manuscript_code",
        hue_order=["CCC", "PhenoPLIER", "BioChatter", "Epistasis"],
        # col_wrap=2,
        kind="point",
    )
    g.set_axis_labels("", "Revision score")
    g.set_titles("{col_name} manuscript")
    # g.tick_params(axis='x', rotation=30)
    # g.set_xticklabels(g.ax.get_xticklabels(), rotation=30)

# %% editable=true slideshow={"slide_type": ""} tags=[]
with sns.plotting_context("paper", font_scale=1.0), sns.axes_style("whitegrid"):
    g = sns.catplot(
        height=4,
        aspect=1.4,
        data=df[df["llm_judge"].isin(("GPT 3.5 Turbo", "GPT-4 Turbo"))],
        x="paragraph_section",
        y="winner_score",
        col="manuscript_code",
        col_order=["CCC", "PhenoPLIER", "BioChatter", "Epistasis"],
        col_wrap=2,
        kind="point",
        hue="llm_judge",
    )
    g.set_axis_labels("", "Revision score")
    g.set_titles("{col_name} manuscript")
    # g.tick_params(axis='x', rotation=30)
    # g.set_xticklabels(g.ax.get_xticklabels(), rotation=30)

# %%
