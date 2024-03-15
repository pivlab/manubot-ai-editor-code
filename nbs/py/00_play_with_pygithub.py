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

# %% [markdown] tags=[] editable=true slideshow={"slide_type": ""}
# TODO

# %% [markdown] tags=[] editable=true slideshow={"slide_type": ""}
# # Modules

# %% tags=[] editable=true slideshow={"slide_type": ""}
import os
from github import Github, Auth

from proj import conf

# %% [markdown] tags=[] editable=true slideshow={"slide_type": ""}
# # Settings/paths

# %% editable=true slideshow={"slide_type": ""} tags=["parameters"]
REPO = "greenelab/manubot-gpt-manuscript"
PR = 41

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Get Repo

# %% tags=[] editable=true slideshow={"slide_type": ""}
auth = Auth.Token(conf.github.API_TOKEN)

# %% tags=[] editable=true slideshow={"slide_type": ""}
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
display(pr_prev)

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_curr = pr_commits[0].sha
display(pr_curr)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Get file content

# %% editable=true slideshow={"slide_type": ""} tags=[]
print(repo.get_contents("content/01.abstract.md", pr_prev).decoded_content.decode("utf-8"))

# %% editable=true slideshow={"slide_type": ""} tags=[]
print(repo.get_contents("content/01.abstract.md", pr_curr).decoded_content.decode("utf-8"))

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Close connections

# %% editable=true slideshow={"slide_type": ""} tags=[]
g.close()

# %% editable=true slideshow={"slide_type": ""} tags=[]
