#!/bin/bash
if [ -f .env ]; then
  set -o allexport
  source .env
  set +o allexport
fi

# The script allows to run a JupyterLab server listening to local connections
# only by default. If the only optional argument is given, then the server will
# request a token from users and will listen to any address (*).

PORT="${PROJ_JUPYTER_SERVER_PORT:-8899}"
export PYTHONPATH=`pwd`
echo "PYTHONPATH=${PYTHONPATH}"

# export the configuration as environmental variables (this is
# helpful if the configuration is needed outside python)
eval `python src/proj/conf/main.py`

IP="127.0.0.1"
TOKEN=""
EXTRA_ARGS=""
if [ "$1" = "--container-mode" ]; then
  IP="*"
  EXTRA_ARGS="--allow-root"
elif [ ! -z "$1" ]; then
  IP="*"
  TOKEN="${1}"
fi

exec jupyter lab \
  --ip="${IP}" \
  --port="${PORT}" \
  --no-browser \
  --ContentsManager.allow_hidden=True \
  --ServerApp.port_retries=0 \
  --IdentityProvider.token="${TOKEN}" ${EXTRA_ARGS}

