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
# This notebook is a template notebook that is intended to be run across different parameters.
#
# TODO

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Modules

# %% editable=true slideshow={"slide_type": ""} tags=[]
import pandas as pd
from IPython.display import display
from langchain.cache import SQLiteCache
from langchain.globals import set_llm_cache
from proj import conf
from proj.utils import llm_pairwise

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Settings/paths

# %% editable=true slideshow={"slide_type": ""} tags=["parameters"]
# Input manuscript
REPO = None

INPUT_FILE = None
OUTPUT_FILE = None

# Model and its parameters
LLM_JUDGE = None
TEMPERATURE = None
MAX_TOKENS = 2000
SEED_INIT = 0

# Evaluation parameters
N_REPS = None
THROW_IF_FAILED = False

# %% editable=true slideshow={"slide_type": ""} tags=[]
conf.common.LLM_CACHE_DIR.mkdir(parents=True, exist_ok=True)
display(conf.common.LLM_CACHE_DIR)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Set default LangChain cache file

# %%
default_cache_file = conf.common.LLM_CACHE_DIR / "default.db"
display(default_cache_file)
set_llm_cache(SQLiteCache(database_path=str(default_cache_file)))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Load paragraphs

# %% editable=true slideshow={"slide_type": ""} tags=[]
df = pd.read_pickle(INPUT_FILE)

# %% editable=true slideshow={"slide_type": ""} tags=[]
df.shape

# %% editable=true slideshow={"slide_type": ""} tags=[]
df.head()

# %% editable=true slideshow={"slide_type": ""} tags=[]
df.iloc[0]["original"]

# %% editable=true slideshow={"slide_type": ""} tags=[]
df.iloc[0]["modified"]

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Test run

# %% editable=true slideshow={"slide_type": ""} tags=[]
t_json = llm_pairwise(
    df.iloc[0]["original"],
    df.iloc[0]["modified"],
    df.iloc[0]["section"],
    model_name=LLM_JUDGE,
    model_params={
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "model_kwargs": {
            "seed": SEED_INIT,
        },
    },
    verbose=True,
)

# %% editable=true slideshow={"slide_type": ""} tags=[]
t_json

# %% editable=true slideshow={"slide_type": ""} tags=[]
type(t_json)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Run

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# Since models are stochastic, we run the pairwise comparison many times.
#
# Here I use a cache to avoid hitting an external API multiple times.

# %% editable=true slideshow={"slide_type": ""} tags=[]
results = []

# %% editable=true slideshow={"slide_type": ""} tags=[]
for rep_idx in range(N_REPS):
    # we cache prompt/results by repetition
    output_cache_file = conf.common.LLM_CACHE_DIR / f"rep{rep_idx}.db"
    set_llm_cache(SQLiteCache(database_path=str(output_cache_file)))

    print(f"{str(rep_idx).zfill(2)} ({output_cache_file.name}): ", end="", flush=True)

    for par_idx, par in df.iterrows():
        print(".", end="", flush=True)

        res = llm_pairwise(
            par["original"],
            par["modified"],
            par["section"],
            model_name=LLM_JUDGE,
            model_params={
                "temperature": TEMPERATURE,
                "max_tokens": MAX_TOKENS,
                "model_kwargs": {
                    "seed": SEED_INIT + rep_idx,
                },
            },
            throw_if_failed=THROW_IF_FAILED,
            verbose=False,
        )

        results.append(
            {
                "rep_index": rep_idx,
                "paragraph_index": par_idx,
                "paragraph_section": par["section"],
                "winner": res["best"],
                "rationale": res["rationale"],
            }
        )

    print(flush=True)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Process results

# %% editable=true slideshow={"slide_type": ""} tags=[]
winner_matchings = {
    "Paragraph A": "-1",  # Original
    "Paragraph 1": "1",  # Modified
    "tie": "0",
}

# %%
df_results = pd.DataFrame(results)

# %%
df_results.shape

# %%
df_results.head()

# %%
df_results["winner"].value_counts()

# %%
df_results = df_results[df_results["winner"].isin(winner_matchings.keys())]

# %%
df_results.shape

# %% editable=true slideshow={"slide_type": ""} tags=[]
df_results = df_results.assign(
    winner_score=df_results["winner"].replace(winner_matchings).apply(float)
)

# %% editable=true slideshow={"slide_type": ""} tags=[]
df_results.shape

# %% editable=true slideshow={"slide_type": ""} tags=[]
df_results.head()

# %% editable=true slideshow={"slide_type": ""} tags=[]
df_results.dtypes

# %% editable=true slideshow={"slide_type": ""} tags=[]
df_results.groupby("paragraph_section")["winner_score"].mean()

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Save

# %% editable=true slideshow={"slide_type": ""} tags=[]
df_results.to_pickle(OUTPUT_FILE)

# %% editable=true slideshow={"slide_type": ""} tags=[]
