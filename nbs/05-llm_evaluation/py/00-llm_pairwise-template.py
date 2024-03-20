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
# This notebook TODO

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Modules

# %% editable=true slideshow={"slide_type": ""} tags=[]
from IPython.display import display
import pandas as pd
from langchain.globals import set_llm_cache
from langchain.cache import SQLiteCache

from proj import conf
from proj.utils import llm_pairwise

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Settings/paths

# %% editable=true slideshow={"slide_type": ""} tags=["parameters"]
REPO = "pivlab/manubot-ai-editor-code-test-biochatter-manuscript"
# LLM_JUDGE = "openai:gpt-4-turbo-preview"
# LLM_JUDGE = "openai:gpt-4"
# LLM_JUDGE = "openai:gpt-3.5-turbo"
LLM_JUDGE = "mistral:7b-instruct-fp16"
N_REPS = 10

# Model parameters
TEMPERATURE = 0.5
MAX_TOKENS = 2000
SEED_INIT = 0

# %% editable=true slideshow={"slide_type": ""} tags=[]
MANUSCRIPT_CODE = REPO.split("-test-")[1]
display(MANUSCRIPT_CODE)

# %% editable=true slideshow={"slide_type": ""} tags=[]
INPUT_FILE = (
    conf.common.RESULTS_DIR / "paragraph_match" / MANUSCRIPT_CODE
).with_suffix(".pkl")
assert INPUT_FILE.exists()
display(INPUT_FILE)

# %% editable=true slideshow={"slide_type": ""} tags=[]
OUTPUT_FILE = (conf.common.RESULTS_DIR / "llm_pairwise" / MANUSCRIPT_CODE).with_suffix(
    ".pkl"
)
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
display(OUTPUT_FILE)

# %% editable=true slideshow={"slide_type": ""} tags=[]
BASE_LANGCHAIN_CACHE_DIR = conf.common.RESULTS_DIR / "llm_cache"
BASE_LANGCHAIN_CACHE_DIR.mkdir(parents=True, exist_ok=True)
display(BASE_LANGCHAIN_CACHE_DIR)

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
    output_cache_file = BASE_LANGCHAIN_CACHE_DIR / f"rep{rep_idx}.db"
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

# %% editable=true slideshow={"slide_type": ""} tags=[]
df_results = pd.DataFrame(results)
df_results["winner_score"] = df_results["winner"].replace(winner_matchings).apply(float)

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
