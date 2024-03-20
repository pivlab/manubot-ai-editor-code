# Code for the Manubot AI Editor manuscript

The manuscript repository is at 

## Setup

### Conda environment

You can two options to setup the conda environment: 1) local environment or 2) Docker container.

#### Option 1: local environment

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

#### Option 2: Docker container

(coming soon)

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