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
from github import Github, Auth

from proj import conf

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Settings/paths

# %% editable=true slideshow={"slide_type": ""} tags=["parameters"]
REPO = "quinlan-lab/mutator-epistasis-manuscript"
PR = 16

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
# # Get file content

# %% editable=true slideshow={"slide_type": ""} tags=[]
pr_filename = pr_files[0].filename
display(pr_filename)

# %% editable=true slideshow={"slide_type": ""} tags=[]
print(
    repo.get_contents(pr_filename, pr_prev).decoded_content.decode("utf-8")
)

# %% editable=true slideshow={"slide_type": ""} tags=[]
print(
    repo.get_contents(pr_filename, pr_curr).decoded_content.decode("utf-8")
)

# %% [markdown] editable=true slideshow={"slide_type": ""} tags=[]
# # Close connections

# %% editable=true slideshow={"slide_type": ""} tags=[]
g.close()

# %% editable=true slideshow={"slide_type": ""} tags=[]
