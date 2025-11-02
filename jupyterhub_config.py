# /opt/jupyterhub/jupyterhub_config.py (v2.1 - Corrected Import)

# --- Authenticator Configuration ---
from jupyterhub.auth import DummyAuthenticator
c.JupyterHub.authenticator_class = DummyAuthenticator
c.DummyAuthenticator.password = "testpass"

# --- Spawner Configuration ---
from dockerspawner import DockerSpawner
c.JupyterHub.spawner_class = DockerSpawner

c.DockerSpawner.image = 'jupyter/scipy-notebook:latest'
c.DockerSpawner.network_name = 'jupyterhub-network'
c.JupyterHub.hub_ip = '0.0.0.0'
