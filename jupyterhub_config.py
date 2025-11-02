# /opt/jupyterhub/jupyterhub_config.py (v2.2 - Final Networking Fix)

# --- Authenticator Configuration ---
from jupyterhub.auth import DummyAuthenticator
c.JupyterHub.authenticator_class = DummyAuthenticator
c.DummyAuthenticator.password = "testpass"

# --- Spawner Configuration ---
from dockerspawner import DockerSpawner
c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = 'jupyter/scipy-notebook:latest'
c.DockerSpawner.network_name = 'jupyterhub-network'

# --- Network Configuration ---
# The IP address for the Hub to listen on. 0.0.0.0 is required inside a container.
c.JupyterHub.hub_ip = '0.0.0.0'

# THIS IS THE FIX:
# Tell the user containers to connect to the Hub via its service name
# on the Docker network.
c.JupyterHub.hub_connect_ip = 'jupyterhub'
