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
from IPython.display import display
from github import Github, Auth
import pandas as pd

from proj import conf
from proj.utils import process_paragraph

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Settings/paths

# %% editable=true slideshow={"slide_type": ""} tags=["parameters"]
REPO = "pivlab/manubot-ai-editor-code-test-biochatter-manuscript"
# PR 2: gpt-3.5-turbo
# PR 3: gpt-4-0125-preview
PR = 2

# %% editable=true slideshow={"slide_type": ""} tags=[]
MANUSCRIPT_CODE = REPO.split("-test-")[1]
display(MANUSCRIPT_CODE)

# %% editable=true slideshow={"slide_type": ""} tags=[]
OUTPUT_FILE_PATH = (conf.common.RESULTS_DIR / "paragraph_match" / MANUSCRIPT_CODE).with_suffix(".pkl")
OUTPUT_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
display(OUTPUT_FILE_PATH)

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
pr = repo.get_pull(PR)

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

# %%
# TODO: explain variable
paragraph_matches = []

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ## Abstract

# %%
section_name = "abstract"

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_filename = pr_files[0].filename
assert section_name in pr_filename
print(pr_filename)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Original

# %%
# get content
orig_section_content = repo.get_contents(pr_filename, pr_prev).decoded_content.decode("utf-8")
print(orig_section_content[:50])

# %%
# split by paragraph
orig_section_paragraphs = orig_section_content.split("\n\n")
display(len(orig_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Modified

# %%
# get content
mod_section_content = repo.get_contents(pr_filename, pr_curr).decoded_content.decode("utf-8")
print(mod_section_content[:50])

# %%
# split by paragraph
mod_section_paragraphs = mod_section_content.split("\n\n")
display(len(mod_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Match

# %%
orig_section_paragraphs[0]

# %%
mod_section_paragraphs[0]

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 00

# %%
par0 = process_paragraph(orig_section_paragraphs[1])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[1])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ## Introduction

# %%
section_name = "introduction"

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_filename = pr_files[1].filename
assert section_name in pr_filename
print(pr_filename)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Original

# %%
# get content
orig_section_content = repo.get_contents(pr_filename, pr_prev).decoded_content.decode("utf-8")
print(orig_section_content[:50])

# %%
# split by paragraph
orig_section_paragraphs = orig_section_content.split("\n\n")
display(len(orig_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Modified

# %%
# get content
mod_section_content = repo.get_contents(pr_filename, pr_curr).decoded_content.decode("utf-8")
print(mod_section_content[:50])

# %%
# split by paragraph
mod_section_paragraphs = mod_section_content.split("\n\n")
display(len(mod_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Match

# %%
orig_section_paragraphs[0]

# %%
mod_section_paragraphs[0]

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 00

# %%
par0 = process_paragraph(orig_section_paragraphs[1])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[1])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 01

# %%
par0 = process_paragraph(orig_section_paragraphs[2])
print(par0)

# %%
# par1 = " ".join(mod_section_paragraphs[2:5]).strip()
par1 = process_paragraph(mod_section_paragraphs[2:5])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 02

# %%
par0 = process_paragraph(orig_section_paragraphs[3])
print(par0)

# %%
# par1 = " ".join(mod_section_paragraphs[2:5]).strip()
par1 = process_paragraph(mod_section_paragraphs[5:6])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ## Results

# %%
section_name = "results"

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_filename = pr_files[2].filename
assert section_name in pr_filename
print(pr_filename)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Original

# %%
# get content
orig_section_content = repo.get_contents(pr_filename, pr_prev).decoded_content.decode("utf-8")
print(orig_section_content[:50])

# %%
# split by paragraph
orig_section_paragraphs = orig_section_content.split("\n\n")
display(len(orig_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Modified

# %%
# get content
mod_section_content = repo.get_contents(pr_filename, pr_curr).decoded_content.decode("utf-8")
print(mod_section_content[:50])

# %%
# split by paragraph
mod_section_paragraphs = mod_section_content.split("\n\n")
display(len(mod_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Match

# %%
orig_section_paragraphs[0]

# %%
mod_section_paragraphs[0]

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 00

# %%
par0 = process_paragraph(orig_section_paragraphs[1])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[1])
print(par1)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 01

# %%
par0 = process_paragraph(orig_section_paragraphs[2:10]).replace(" - ", "\n- ")
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[2])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 02

# %%
par0 = process_paragraph(orig_section_paragraphs[13:14])#.replace(" - ", "\n- ")
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[6])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 03

# %%
par0 = process_paragraph(orig_section_paragraphs[15])#.replace(" - ", "\n- ")
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[8])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 04

# %%
par0 = process_paragraph(orig_section_paragraphs[17])#.replace(" - ", "\n- ")
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[10])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 05

# %%
par0 = process_paragraph(orig_section_paragraphs[19])#.replace(" - ", "\n- ")
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[12])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 06

# %%
par0 = process_paragraph(orig_section_paragraphs[21])#.replace(" - ", "\n- ")
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[14])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 07

# %%
par0 = process_paragraph(orig_section_paragraphs[23])#.replace(" - ", "\n- ")
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[16])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 08

# %%
par0 = process_paragraph(orig_section_paragraphs[24])#.replace(" - ", "\n- ")
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[17])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 09

# %%
par0 = process_paragraph(orig_section_paragraphs[25])#.replace(" - ", "\n- ")
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[18])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 10

# %%
par0 = process_paragraph(orig_section_paragraphs[26])#.replace(" - ", "\n- ")
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[19])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ## Discussion

# %%
section_name = "discussion"

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_filename = pr_files[3].filename
assert section_name in pr_filename
print(pr_filename)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Original

# %%
# get content
orig_section_content = repo.get_contents(pr_filename, pr_prev).decoded_content.decode("utf-8")
print(orig_section_content[:50])

# %%
# split by paragraph
orig_section_paragraphs = orig_section_content.split("\n\n")
display(len(orig_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Modified

# %%
# get content
mod_section_content = repo.get_contents(pr_filename, pr_curr).decoded_content.decode("utf-8")
print(mod_section_content[:50])

# %%
# split by paragraph
mod_section_paragraphs = mod_section_content.split("\n\n")
display(len(mod_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Match

# %%
orig_section_paragraphs[0]

# %%
mod_section_paragraphs[0]

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 00

# %%
par0 = process_paragraph(orig_section_paragraphs[1])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[1])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 01

# %%
par0 = process_paragraph(orig_section_paragraphs[2])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[2])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 02

# %%
par0 = process_paragraph(orig_section_paragraphs[3])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[3])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 03

# %%
par0 = process_paragraph(orig_section_paragraphs[4])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[4])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 04

# %%
par0 = process_paragraph(orig_section_paragraphs[5])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[5])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 05

# %%
par0 = process_paragraph(orig_section_paragraphs[7])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[7])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 06

# %%
par0 = process_paragraph(orig_section_paragraphs[9])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[9])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ## Methods

# %%
section_name = "methods"

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_filename = pr_files[4].filename
assert section_name in pr_filename
print(pr_filename)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Original

# %%
# get content
orig_section_content = repo.get_contents(pr_filename, pr_prev).decoded_content.decode("utf-8")
print(orig_section_content[:50])

# %%
# split by paragraph
orig_section_paragraphs = orig_section_content.split("\n\n")
display(len(orig_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Modified

# %%
# get content
mod_section_content = repo.get_contents(pr_filename, pr_curr).decoded_content.decode("utf-8")
print(mod_section_content[:50])

# %%
# split by paragraph
mod_section_paragraphs = mod_section_content.split("\n\n")
display(len(mod_section_paragraphs))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ### Match

# %%
orig_section_paragraphs[0]

# %%
mod_section_paragraphs[0]

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 00

# %%
par0 = process_paragraph(orig_section_paragraphs[1])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[1:3]).replace("$$", "\n$$").replace("\\text", "\n\\text")
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 01

# %%
par0 = process_paragraph(orig_section_paragraphs[4])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[5])#.replace("$$", "\n$$").replace("\\text", "\n\\text")
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 02

# %%
par0 = process_paragraph(orig_section_paragraphs[5])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[6])#.replace("$$", "\n$$").replace("\\text", "\n\\text")
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 03

# %%
par0 = process_paragraph(orig_section_paragraphs[8])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[9:11]).replace("$$", "\n$$")#.replace("\\text\{LLM", "\n\\text\{LLM")
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 04

# %%
par0 = process_paragraph(orig_section_paragraphs[9:19]).replace(" - ", "\n- ")
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[11:21]).replace(" - ", "\n- ")
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 05

# %%
par0 = process_paragraph(orig_section_paragraphs[20])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[24])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 06

# %%
par0 = process_paragraph(orig_section_paragraphs[22])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[26])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 07

# %%
par0 = process_paragraph(orig_section_paragraphs[23])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[27:28]).replace("$$", "\n$$").replace("\\text", "\n\\text") + \
"\n" + process_paragraph(mod_section_paragraphs[28:31])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 08

# %%
par0 = process_paragraph(orig_section_paragraphs[24])
print(par0)

# %%
par1 = process_paragraph([
    process_paragraph(mod_section_paragraphs[31:32]).replace("$$", "\n$$").replace("\\text", "\n\\text"),
    process_paragraph(mod_section_paragraphs[32:33]),
])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 09

# %%
par0 = process_paragraph(orig_section_paragraphs[26])
print(par0)

# %%
par1 = process_paragraph([
    process_paragraph(mod_section_paragraphs[34:35]),#.replace("$$", "\n$$").replace("\\text", "\n\\text"),
    # process_paragraph(mod_section_paragraphs[32:33]),
])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 10

# %%
par0 = process_paragraph(orig_section_paragraphs[27])
print(par0)

# %%
par1 = process_paragraph([
    process_paragraph(mod_section_paragraphs[35:36]),
    process_paragraph(mod_section_paragraphs[36:37]),
]).replace("Model $$", "Model\n$$").replace("LLM:", "\nLLM:").replace("The contextual", "\nThe contextual")
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 11

# %%
par0 = process_paragraph(orig_section_paragraphs[28])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[38])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 12

# %%
par0 = process_paragraph(orig_section_paragraphs[29])
print(par0)

# %%
par1 = process_paragraph(mod_section_paragraphs[40:43])
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 13

# %%
par0 = process_paragraph(orig_section_paragraphs[32])
print(par0)

# %%
par1 = process_paragraph([
    process_paragraph(mod_section_paragraphs[45:46]),
    mod_section_paragraphs[46],
    process_paragraph(mod_section_paragraphs[47])
]).replace(" $$ X", "\n\n$$\nX").replace("$$ {", "\n$$ {").replace("On Mac OS", "\n\nOn Mac OS")
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 14

# %%
par0 = process_paragraph(orig_section_paragraphs[34])
print(par0)

# %%
par1 = process_paragraph([
    process_paragraph(mod_section_paragraphs[49]),
    # mod_section_paragraphs[46],
    # process_paragraph(mod_section_paragraphs[47])
])#.replace(" $$ X", "\n\n$$\nX").replace("$$ {", "\n$$ {").replace("On Mac OS", "\n\nOn Mac OS")
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

# %%
display(paragraph_matches[-1])

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# ####  Paragraph 15

# %%
par0 = process_paragraph(orig_section_paragraphs[35])
print(par0)

# %%
par1 = process_paragraph([
    process_paragraph(mod_section_paragraphs[51]),
    # mod_section_paragraphs[46],
    # process_paragraph(mod_section_paragraphs[47])
])#.replace(" $$ X", "\n\n$$\nX").replace("$$ {", "\n$$ {").replace("On Mac OS", "\n\nOn Mac OS")
print(par1)

# %%
paragraph_matches.append((
    section_name,
    par0,
    par1,
))

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

# %%
paragraph_matches[:2]

# %%
df = pd.DataFrame(paragraph_matches).rename(columns={
    0: "section",
    1: "original",
    2: "modified",
})

# %%
df.shape

# %%
df.head()

# %%
df.to_pickle(OUTPUT_FILE_PATH)

# %% editable=true slideshow={"slide_type": ""} tags=[]
