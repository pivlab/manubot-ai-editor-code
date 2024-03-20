#!/bin/bash
if [ -f .env ]; then
  set -o allexport
  source .env
  set +o allexport
fi

# This script runs a Jupyter notebook (.ipynb) from the command line using
# papermill.

# export the configuration as environmental variables; this allows to use configuration
# entries beyond python
eval `python src/proj/conf/main.py`

if [ -z "${1}" ]; then
    echo "Specify notebook to run"
    exit 1
fi

# If the notebook is an "output notebook" (*.run.ipynb), which are generated by
# papermill for instance, then do not run it.
pattern="*.run.ipynb"

input_notebook=$1
shift

if [[ $input_notebook == $pattern ]]; then
    echo "Not running output notebook"
    exit 0
fi

override_nbs="${PROJ_NBS_RUN_OVERRIDE:-0}"

# if second argument is a notebook, then it is the output
# notebook filename
if [[ $1 == *.ipynb ]]; then
    output_notebook=${input_notebook%/*}/$1
    shift

    # do not override if output was specified
    override_nbs=0
else
    output_notebook="${input_notebook%.*}.run.ipynb"
fi

# run papermill
if [ "${PROJ_NBS_PAPERMILL_RUN_WITH_CUSTOM_KERNEL}" = "1" ]; then
  # with custom kernel (avoids local ports conflicts)
  >&2 python << END
from proj.papermill_custom_kernel import run_papermill
run_papermill("${input_notebook}", "${output_notebook}", "$@")
END
else
  # run papermill from the command line, which is much simpler and preferred
  papermill \
    --log-output \
    --request-save-on-cell-execute \
    $@ \
    $input_notebook \
    $output_notebook
fi

# Convert to notebook
#
# This is to reduce the notebook final size, which is huge after
# running with papermill.
jupyter nbconvert --to notebook ${output_notebook} --output ${output_notebook##*/}

if [ "${override_nbs}" != "0" ]; then
  mv $output_notebook $input_notebook
  
  # jupytext: synchronize notebook and text representation
  jupytext --sync ${input_notebook} --check 'ruff format {}'
fi
