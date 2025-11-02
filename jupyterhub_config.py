# /opt/jupyterhub/jupyterhub_config.py

# --- Authenticator Configuration ---
# This part remains the same for now.
from jupyterhub.auth import DummyAuthenticator
c.JupyterHub.authenticator_class = DummyAuthenticator
c.DummyAuthenticator.password = "testpass"

# --- Spawner Configuration ---
# NEW: We are now using DockerSpawner
from jupyterhub.spawner import DockerSpawner
c.JupyterHub.spawner_class = DockerSpawner

# Tell DockerSpawner which Docker image to use for user containers.
# 'jupyter/scipy-notebook' is a great starting point with many libraries.
c.DockerSpawner.image = 'jupyter/scipy-notebook:latest'

# --- Network Configuration ---
# The Hub needs to be able to talk to the user containers.
# We will create a Docker network named 'jupyterhub-network' in our stack file.
c.DockerSpawner.network_name = 'jupyterhub-network'
c.JupyterHub.hub_ip = '0.0.0.0'
