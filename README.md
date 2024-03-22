# Code for the Manubot AI Editor manuscript

The manuscript repository is at 

## Setup

### Conda environment

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or Anaconda.

1. Install main Python environment (allows to run most steps):

   ```bash
   conda env create --file environment.yml
   ```

1. Activate the environment:

    ```bash
    conda activate manubot-ai-editor-code
    ```

1. Install local package in editable mode (needs to be done only once):

    ```bash
    pip install -e .
    ```

### Ollama

These steps are only needed if you want to try local, open models.
We used this during development to test Mistral models.

1. Install [Ollama](https://ollama.ai/). The latest version we tested is [v0.1.18](https://github.com/jmorganca/ollama/releases/tag/v0.1.18), which in Linux (amd64) you can install with:
   ```bash
   sudo curl -L https://github.com/jmorganca/ollama/releases/download/v0.1.18/ollama-linux-amd64 -o /usr/bin/ollama
   sudo chmod +x /usr/bin/ollama
   ```
1. Start Ollama in a different terminal (no need to activate the conda environment), if not [already running automatically](https://github.com/jmorganca/ollama/issues/707):
   ```bash
   ollama serve
   ```
1. Pull Mistral models:
   ```bash
   ollama pull mistral:7b-instruct-fp16
   ```

### Configuration

Open file `.env` and add the following keys with the correct values:

```env
PROJ_GITHUB_AUTH_TOKEN="..."
OPENAI_API_KEY="..."
```

## Run analysis

To run all the analysis:

```bash
pytask
```

## Development

These are steps intended to be used by project mantainers.

### conda-libmamba-solver

Optionally, and before creating the conda environment, install libmamba solver which is a much faster dependency resolution:

```bash
# update conda
conda update conda -n base -c defaults

# install libmamba solver and set as default solver
conda install -n base -c defaults conda-libmamba-solver
conda config --set solver libmamba

# in case you want to switch back to the classic solver:
# conda config --set solver classic
```

### Pre-commit hooks

```bash
# (optional) install pre-commit git hooks
pre-commit install

# run pre-commit hooks on all files
pre-commit run --all-files
```