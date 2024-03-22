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
# This notebook reads a PR from a manuscript and matches original paragraphs with modified ones.

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Modules

# %% editable=true slideshow={"slide_type": ""} tags=[]
from pathlib import Path

import pandas as pd
from github import Auth, Github
from IPython.display import display
from proj import conf
from proj.utils import process_paragraph

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Settings/paths

# %% editable=true slideshow={"slide_type": ""} tags=["parameters"]
REPO = "pivlab/manubot-ai-editor-code-test-phenoplier-manuscript"
PR = (4, "gpt-3.5-turbo")

OUTPUT_FILE_PATH = None
REVERSED_OUTPUT_FILE_PATH = None

# %% tags=["injected-parameters"]
# Parameters
OUTPUT_FILE_PATH = "/home/miltondp/projects/others/manubot/manubot-ai-editor-code/base/results/paragraph_match/phenoplier-manuscript--gpt-3.5-turbo.pkl"
REVERSED_OUTPUT_FILE_PATH = "/home/miltondp/projects/others/manubot/manubot-ai-editor-code/base/results/paragraph_match/phenoplier-manuscript--gpt-3.5-turbo--reversed.pkl"


# %% editable=true slideshow={"slide_type": ""} tags=[]
OUTPUT_FILE_PATH = Path(OUTPUT_FILE_PATH).resolve()
OUTPUT_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
display(OUTPUT_FILE_PATH)

# %% editable=true slideshow={"slide_type": ""} tags=[]
REVERSED_OUTPUT_FILE_PATH = Path(REVERSED_OUTPUT_FILE_PATH).resolve()
REVERSED_OUTPUT_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
display(REVERSED_OUTPUT_FILE_PATH)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Get Repo

# %% editable=true slideshow={"slide_type": ""} tags=[]
auth = Auth.Token(conf.github.API_TOKEN)

# %% editable=true slideshow={"slide_type": ""} tags=[]
g = Github(auth=auth)

# %% editable=true slideshow={"slide_type": ""} tags=[]
repo = g.get_repo(REPO)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Get Pull Request

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr = repo.get_pull(PR[0])

# %% editable=true slideshow={"slide_type": ""} tags=[]
list(pr.get_files())

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_commits = list(pr.get_commits())

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_commits[0].parents

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_prev = pr_commits[0].parents[0].sha
print(pr_prev)

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_curr = pr_commits[0].sha
print(pr_curr)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Get file list

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_files = [f for f in pr.get_files() if f.filename.endswith(".md")]
display(pr_files)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Sections

# %% tags=[]
paragraph_matches = []

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ## Abstract

# %% tags=[]
section_name = "abstract"

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_filename = pr_files[0].filename
assert section_name in pr_filename
print(pr_filename)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Original

# %% tags=[]
# get content
orig_section_content = repo.get_contents(pr_filename, pr_prev).decoded_content.decode(
    "utf-8"
)
print(orig_section_content[:50])

# %% tags=[]
# split by paragraph
orig_section_paragraphs = orig_section_content.split("\n\n")
display(len(orig_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Modified

# %% tags=[]
# get content
mod_section_content = repo.get_contents(pr_filename, pr_curr).decoded_content.decode(
    "utf-8"
)
print(mod_section_content[:50])

# %% tags=[]
# split by paragraph
mod_section_paragraphs = mod_section_content.split("\n\n")
display(len(mod_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Match

# %% tags=[]
orig_section_paragraphs[0]

# %% tags=[]
mod_section_paragraphs[0]

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 00

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[1])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[1])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ## Introduction

# %% tags=[]
section_name = "introduction"

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_filename = pr_files[1].filename
assert section_name in pr_filename
print(pr_filename)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Original

# %% tags=[]
# get content
orig_section_content = repo.get_contents(pr_filename, pr_prev).decoded_content.decode(
    "utf-8"
)
print(orig_section_content[:50])

# %% tags=[]
# split by paragraph
orig_section_paragraphs = orig_section_content.split("\n\n")
display(len(orig_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Modified

# %% tags=[]
# get content
mod_section_content = repo.get_contents(pr_filename, pr_curr).decoded_content.decode(
    "utf-8"
)
print(mod_section_content[:50])

# %% tags=[]
# split by paragraph
mod_section_paragraphs = mod_section_content.split("\n\n")
display(len(mod_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Match

# %% tags=[]
orig_section_paragraphs[0]

# %% tags=[]
mod_section_paragraphs[0]

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 00

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[1])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[1])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 01

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[2])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[2])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 02

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[3])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[3])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 03

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[4])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[4:8])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ## Results (framework)

# %% tags=[]
section_name = "results"

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_filename = pr_files[2].filename
assert section_name in pr_filename
assert "framework" in pr_filename
print(pr_filename)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Original

# %% tags=[]
# get content
orig_section_content = repo.get_contents(pr_filename, pr_prev).decoded_content.decode(
    "utf-8"
)
print(orig_section_content[:50])

# %% tags=[]
# split by paragraph
orig_section_paragraphs = orig_section_content.split("\n\n")
display(len(orig_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Modified

# %% tags=[]
# get content
mod_section_content = repo.get_contents(pr_filename, pr_curr).decoded_content.decode(
    "utf-8"
)
print(mod_section_content[:50])

# %% tags=[]
# split by paragraph
mod_section_paragraphs = mod_section_content.split("\n\n")
display(len(mod_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Match

# %% tags=[]
orig_section_paragraphs[0]

# %% tags=[]
mod_section_paragraphs[0]

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 00

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[2])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[2])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 01

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[3])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[3])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 02

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[4])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[4])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 03

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[5])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[5])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 04

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[6])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[6])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ## Results (CRISPR)

# %% tags=[]
# section_name = "results"

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_filename = pr_files[3].filename
assert section_name in pr_filename
assert "crispr" in pr_filename
print(pr_filename)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Original

# %% tags=[]
# get content
orig_section_content = repo.get_contents(pr_filename, pr_prev).decoded_content.decode(
    "utf-8"
)
print(orig_section_content[:50])

# %% tags=[]
# split by paragraph
orig_section_paragraphs = orig_section_content.split("\n\n")
display(len(orig_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Modified

# %% tags=[]
# get content
mod_section_content = repo.get_contents(pr_filename, pr_curr).decoded_content.decode(
    "utf-8"
)
print(mod_section_content[:50])

# %% tags=[]
# split by paragraph
mod_section_paragraphs = mod_section_content.split("\n\n")
display(len(mod_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Match

# %% tags=[]
orig_section_paragraphs[0]

# %% tags=[]
mod_section_paragraphs[0]

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 00

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[1])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[1])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 01

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[3])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[3])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 02

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[4])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[4])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ## Results (drug-disease prediction)

# %% tags=[]
# section_name = "results"

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_filename = pr_files[4].filename
assert section_name in pr_filename
assert "drug_disease" in pr_filename
print(pr_filename)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Original

# %% tags=[]
# get content
orig_section_content = repo.get_contents(pr_filename, pr_prev).decoded_content.decode(
    "utf-8"
)
print(orig_section_content[:50])

# %% tags=[]
# split by paragraph
orig_section_paragraphs = orig_section_content.split("\n\n")
display(len(orig_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Modified

# %% tags=[]
# get content
mod_section_content = repo.get_contents(pr_filename, pr_curr).decoded_content.decode(
    "utf-8"
)
print(mod_section_content[:50])

# %% tags=[]
# split by paragraph
mod_section_paragraphs = mod_section_content.split("\n\n")
display(len(mod_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Match

# %% tags=[]
orig_section_paragraphs[0]

# %% tags=[]
mod_section_paragraphs[0]

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 00

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[1])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[1])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% scrolled=true tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 01

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[3])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[3])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 02

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[4])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[4])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 03

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[7])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[7])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 04

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[10])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[10])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ## Results (clustering)

# %% tags=[]
# section_name = "results"

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_filename = pr_files[5].filename
assert section_name in pr_filename
assert "traits_clustering" in pr_filename
print(pr_filename)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Original

# %% tags=[]
# get content
orig_section_content = repo.get_contents(pr_filename, pr_prev).decoded_content.decode(
    "utf-8"
)
print(orig_section_content[:50])

# %% tags=[]
# split by paragraph
orig_section_paragraphs = orig_section_content.split("\n\n")
display(len(orig_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Modified

# %% tags=[]
# get content
mod_section_content = repo.get_contents(pr_filename, pr_curr).decoded_content.decode(
    "utf-8"
)
print(mod_section_content[:50])

# %% tags=[]
# split by paragraph
mod_section_paragraphs = mod_section_content.split("\n\n")
display(len(mod_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Match

# %% tags=[]
orig_section_paragraphs[0]

# %% tags=[]
mod_section_paragraphs[0]

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 00

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[2])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[2])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% scrolled=true tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 01

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[4])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[4])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% scrolled=true tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 02

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[6])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[6:8])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 03

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[7])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[8])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 04

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[8])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[9])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ## Discussion

# %% tags=[]
section_name = "discussion"

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_filename = pr_files[6].filename
assert section_name in pr_filename
print(pr_filename)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Original

# %% tags=[]
# get content
orig_section_content = repo.get_contents(pr_filename, pr_prev).decoded_content.decode(
    "utf-8"
)
print(orig_section_content[:50])

# %% tags=[]
# split by paragraph
orig_section_paragraphs = orig_section_content.split("\n\n")
display(len(orig_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Modified

# %% tags=[]
# get content
mod_section_content = repo.get_contents(pr_filename, pr_curr).decoded_content.decode(
    "utf-8"
)
print(mod_section_content[:50])

# %% tags=[]
# split by paragraph
mod_section_paragraphs = mod_section_content.split("\n\n")
display(len(mod_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Match

# %% tags=[]
orig_section_paragraphs[0]

# %% tags=[]
mod_section_paragraphs[0]

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 00

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[1])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[1])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 01

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[2])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[2])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 02

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[3])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[3])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 03

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[4])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[4])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 04

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[5])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[5])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 05

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[6])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[6:8])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 06

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[7])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[8])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 07

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[8])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[9])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ## Methods

# %% tags=[]
section_name = "methods"

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_filename = pr_files[7].filename
assert section_name in pr_filename
print(pr_filename)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Original

# %% tags=[]
# get content
orig_section_content = repo.get_contents(pr_filename, pr_prev).decoded_content.decode(
    "utf-8"
)
print(orig_section_content[:50])

# %% tags=[]
# split by paragraph
orig_section_paragraphs = orig_section_content.split("\n\n")
display(len(orig_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Modified

# %% tags=[]
# get content
mod_section_content = repo.get_contents(pr_filename, pr_curr).decoded_content.decode(
    "utf-8"
)
print(mod_section_content[:50])

# %% tags=[]
# split by paragraph
mod_section_paragraphs = mod_section_content.split("\n\n")
display(len(mod_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Match

# %% tags=[]
orig_section_paragraphs[0]

# %% tags=[]
mod_section_paragraphs[0]

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 00

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[1])
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[1:4])
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 01

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[4])
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[8:11])
    .replace("$$", "\n$$")
    .replace("$$ \\tilde", "$$\n\\tilde")
    .replace("$$ {#eq:1} is", "$$ {#eq:1}\nis")
    # .replace("$$ For example", "$$\nFor example")
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 02

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[5:10])
    .replace("$$", "\n$$")
    .replace("$$ \\", "$$\n\\")
    .replace(":predixcan} where", ":predixcan}\nwhere")
    .replace(":spredixcan} where", ":spredixcan}\nwhere")
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[11:16])
    .replace("$$", "\n$$")
    .replace("$$ \\", "$$\n\\")
    .replace(":predixcan} where", ":predixcan}\nwhere")
    .replace(":spredixcan} where", ":spredixcan}\nwhere")
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 03

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[10:15])
    .replace("$$", "\n$$")
    .replace("$$ \\", "$$\n\\")
    .replace(":multixcan} where", ":multixcan}\nwhere")
    .replace(":smultixcan} where", ":smultixcan}\nwhere")
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[16:21])
    .replace("$$", "\n$$")
    .replace("$$ \\", "$$\n\\")
    .replace(":multixcan} where", ":multixcan}\nwhere")
    .replace(":smultixcan} where", ":smultixcan}\nwhere")
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 04

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[20:23])
    .replace("$$", "\n$$")
    .replace("$$ ||", "$$\n||")
    .replace(":plier_func} subject", ":plier_func}\nsubject")
    # .replace(":smultixcan} where", ":smultixcan}\nwhere")
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[30:33])
    .replace("$$", "\n$$")
    .replace("$$ ||", "$$\n||")
    .replace("$$ This opt", "$$\nThis opt")
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 05

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[23:26])
    .replace("$$", "\n$$")
    .replace("$$ \\", "$$\n\\")
    .replace(":proj} where", ":proj}\nwhere")
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[33:36])
    .replace("$$", "\n$$")
    .replace("$$ \\", "$$\n\\")
    .replace(":proj} Here", ":proj}\nHere")
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 06

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[31])
    # .replace("$$", "\n$$")
    # .replace("$$ \\", "$$\n\\")
    # .replace(":proj} Here", ":proj}\nHere")
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[45])
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 07

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[39])
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[53])
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 08

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[43])
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[58])
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 09

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[44])
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[59])
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 10

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[47])
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[63:67])
    .replace("$$", "\n$$")
    .replace("$$ \\", "$$\n\\")
    .replace("$$ where", "$$\nwhere")
    .replace("$$ M", "$$\nM")
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 11

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[48:51])
    .replace("$$", "\n$$")
    .replace("$$ \\", "$$\n\\")
    .replace(":obj_func} where", ":obj_func}\nwhere")
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[68:71])
    .replace("$$", "\n$$")
    .replace("$$ \\", "$$\n\\")
    .replace(":obj_func} where", ":obj_func}\nwhere")
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 12

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[51])
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[71:76])
    .replace("$$", "\n$$")
    .replace("$$ ", "$$\n")
    # .replace(":obj_func} where", ":obj_func}\nwhere")
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 13

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[52])
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[76])
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 14

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[53])
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph([
        mod_section_paragraphs[78],
        mod_section_paragraphs[80],
    ])
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 15

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[56])
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[83])
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 16

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[57])
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[84])
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 17

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[58])
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[85])
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 18

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[59])
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[87])
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 19

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[60])
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[90])
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 20

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[61])
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[91])
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 21

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[62])
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[92])
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 22

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[63])
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[94])
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 23

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[67])
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[98])
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 24

# %% tags=[]
par0 = (
    process_paragraph(orig_section_paragraphs[70])
)
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[104])
)
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ## Supplementary material

# %% tags=[]
section_name = "supplementary material"

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_filename = pr_files[8].filename
assert "supplementary" in pr_filename
print(pr_filename)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Original

# %% tags=[]
# get content
orig_section_content = repo.get_contents(pr_filename, pr_prev).decoded_content.decode(
    "utf-8"
)
print(orig_section_content[:50])

# %% tags=[]
# split by paragraph
orig_section_paragraphs = orig_section_content.split("\n\n")
display(len(orig_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Modified

# %% tags=[]
# get content
mod_section_content = repo.get_contents(pr_filename, pr_curr).decoded_content.decode(
    "utf-8"
)
print(mod_section_content[:50])

# %% tags=[]
# split by paragraph
mod_section_paragraphs = mod_section_content.split("\n\n")
display(len(mod_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Match

# %% tags=[]
orig_section_paragraphs[0]

# %% tags=[]
mod_section_paragraphs[0]

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 00

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[3])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[3])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 01

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[4])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[4])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 02

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[5])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[5])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 03

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[7])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[7])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 04

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[8])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[8])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 05

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[33])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[33])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 06

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[35])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[35])
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% tags=[]
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Close connections

# %% editable=true slideshow={"slide_type": ""} tags=[]
g.close()

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Save

# %% editable=true slideshow={"slide_type": ""} tags=[]
len(paragraph_matches)

# %% tags=[]
paragraph_matches[:2]

# %% tags=[]
df = pd.DataFrame(paragraph_matches).rename(
    columns={
        0: "section",
        1: "original",
        2: "modified",
    }
)

# %% tags=[]
df.shape

# %% tags=[]
df.head()

# %% tags=[]
df.to_pickle(OUTPUT_FILE_PATH)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Reverse original/modified columns

# %% editable=true slideshow={"slide_type": ""} tags=[]
df_reversed = df.rename(columns={"original": "modified2"}).rename(
    columns={"modified": "original", "modified2": "modified"}
)

# %% editable=true slideshow={"slide_type": ""} tags=[]
df_reversed.shape

# %% editable=true slideshow={"slide_type": ""} tags=[]
df_reversed.head()

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ## Save

# %% tags=[]
df_reversed.to_pickle(REVERSED_OUTPUT_FILE_PATH)

# %% editable=true slideshow={"slide_type": ""} tags=[]
