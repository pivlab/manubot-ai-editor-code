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
