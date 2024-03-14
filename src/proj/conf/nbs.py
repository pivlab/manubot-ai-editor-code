"""
Contains configuration entries related to Jupyter Notebooks.
"""

# Jupyter server port
JUPYTER_SERVER_PORT = 8899

# when a notebook is run from the command line and it finished successfully, it
# indicates whether the original notebook should be overridden with the new one
RUN_OVERRIDE = 1

# indicates whether notebook run with papermill should use a custom kernel
# use this option if running several notebooks in the same node (such as in a cluster).
# This is necessary because otherwise Jupyter's selects the same ports and mess things
# up.
PAPERMILL_RUN_WITH_CUSTOM_KERNEL = 0
