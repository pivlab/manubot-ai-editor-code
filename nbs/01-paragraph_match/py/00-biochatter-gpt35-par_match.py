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
REPO = "pivlab/manubot-ai-editor-code-test-biochatter-manuscript"
PR = (2, "gpt-3.5-turbo")

OUTPUT_FILE_PATH = None
REVERSED_OUTPUT_FILE_PATH = None

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
# par1 = " ".join(mod_section_paragraphs[2:5]).strip()
par1 = process_paragraph(mod_section_paragraphs[2:5])
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
# par1 = " ".join(mod_section_paragraphs[2:5]).strip()
par1 = process_paragraph(mod_section_paragraphs[5:6])
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
# ## Results

# %% tags=[]
section_name = "results"

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_filename = pr_files[2].filename
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

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 01

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[2:10]).replace(" - ", "\n- ")
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
par0 = process_paragraph(orig_section_paragraphs[13:14])  # .replace(" - ", "\n- ")
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
# ####  Paragraph 03

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[15])  # .replace(" - ", "\n- ")
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
par0 = process_paragraph(orig_section_paragraphs[17])  # .replace(" - ", "\n- ")
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
# ####  Paragraph 05

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[19])  # .replace(" - ", "\n- ")
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[12])
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
par0 = process_paragraph(orig_section_paragraphs[21])  # .replace(" - ", "\n- ")
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[14])
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
par0 = process_paragraph(orig_section_paragraphs[23])  # .replace(" - ", "\n- ")
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[16])
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
par0 = process_paragraph(orig_section_paragraphs[24])  # .replace(" - ", "\n- ")
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[17])
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
par0 = process_paragraph(orig_section_paragraphs[25])  # .replace(" - ", "\n- ")
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[18])
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
par0 = process_paragraph(orig_section_paragraphs[26])  # .replace(" - ", "\n- ")
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[19])
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
pr_filename = pr_files[3].filename
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
# ####  Paragraph 06

# %% tags=[]
par0 = process_paragraph(orig_section_paragraphs[9])
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
pr_filename = pr_files[4].filename
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
    process_paragraph(mod_section_paragraphs[1:3])
    .replace("$$", "\n$$")
    .replace("\\text", "\n\\text")
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
par1 = process_paragraph(
    mod_section_paragraphs[5]
)  # .replace("$$", "\n$$").replace("\\text", "\n\\text")
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
par1 = process_paragraph(
    mod_section_paragraphs[6]
)  # .replace("$$", "\n$$").replace("\\text", "\n\\text")
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
par0 = process_paragraph(orig_section_paragraphs[8])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[9:11]).replace(
    "$$", "\n$$"
)  # .replace("\\text\{LLM", "\n\\text\{LLM")
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
par0 = process_paragraph(orig_section_paragraphs[9:19]).replace(" - ", "\n- ")
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[11:21]).replace(" - ", "\n- ")
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
par0 = process_paragraph(orig_section_paragraphs[20])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[24])
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
par0 = process_paragraph(orig_section_paragraphs[22])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[26])
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
par0 = process_paragraph(orig_section_paragraphs[23])
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(mod_section_paragraphs[27:28])
    .replace("$$", "\n$$")
    .replace("\\text", "\n\\text")
    + "\n"
    + process_paragraph(mod_section_paragraphs[28:31])
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
par0 = process_paragraph(orig_section_paragraphs[24])
print(par0)

# %% tags=[]
par1 = process_paragraph(
    [
        process_paragraph(mod_section_paragraphs[31:32])
        .replace("$$", "\n$$")
        .replace("\\text", "\n\\text"),
        process_paragraph(mod_section_paragraphs[32:33]),
    ]
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
par0 = process_paragraph(orig_section_paragraphs[26])
print(par0)

# %% tags=[]
par1 = process_paragraph(
    [
        process_paragraph(
            mod_section_paragraphs[34:35]
        ),  # .replace("$$", "\n$$").replace("\\text", "\n\\text"),
        # process_paragraph(mod_section_paragraphs[32:33]),
    ]
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
par0 = process_paragraph(orig_section_paragraphs[27])
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(
        [
            process_paragraph(mod_section_paragraphs[35:36]),
            process_paragraph(mod_section_paragraphs[36:37]),
        ]
    )
    .replace("Model $$", "Model\n$$")
    .replace("LLM:", "\nLLM:")
    .replace("The contextual", "\nThe contextual")
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
par0 = process_paragraph(orig_section_paragraphs[28])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[38])
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
par0 = process_paragraph(orig_section_paragraphs[29])
print(par0)

# %% tags=[]
par1 = process_paragraph(mod_section_paragraphs[40:43])
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
par0 = process_paragraph(orig_section_paragraphs[32])
print(par0)

# %% tags=[]
par1 = (
    process_paragraph(
        [
            process_paragraph(mod_section_paragraphs[45:46]),
            mod_section_paragraphs[46],
            process_paragraph(mod_section_paragraphs[47]),
        ]
    )
    .replace(" $$ X", "\n\n$$\nX")
    .replace("$$ {", "\n$$ {")
    .replace("On Mac OS", "\n\nOn Mac OS")
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
par0 = process_paragraph(orig_section_paragraphs[34])
print(par0)

# %% tags=[]
par1 = process_paragraph(
    [
        process_paragraph(mod_section_paragraphs[49]),
        # mod_section_paragraphs[46],
        # process_paragraph(mod_section_paragraphs[47])
    ]
)  # .replace(" $$ X", "\n\n$$\nX").replace("$$ {", "\n$$ {").replace("On Mac OS", "\n\nOn Mac OS")
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
par0 = process_paragraph(orig_section_paragraphs[35])
print(par0)

# %% tags=[]
par1 = process_paragraph(
    [
        process_paragraph(mod_section_paragraphs[51]),
        # mod_section_paragraphs[46],
        # process_paragraph(mod_section_paragraphs[47])
    ]
)  # .replace(" $$ X", "\n\n$$\nX").replace("$$ {", "\n$$ {").replace("On Mac OS", "\n\nOn Mac OS")
print(par1)

# %% tags=[]
paragraph_matches.append(
    (
        section_name,
        par0,
        par1,
    )
)

# %% editable=true slideshow={"slide_type": ""} tags=[]
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
