# /opt/jupyterhub/jupyterhub_config.py (v3.1 - Add Default URL)
import os

# --- Authenticator Configuration ---
from oauthenticator.generic import GenericOAuthenticator
c.JupyterHub.authenticator_class = GenericOAuthenticator

c.GenericOAuthenticator.client_id = os.environ.get('OAUTH_CLIENT_ID')
c.GenericOAuthenticator.client_secret = os.environ.get('OAUTH_CLIENT_SECRET')
c.GenericOAuthenticator.oidc_issuer = os.environ.get('OIDC_ISSUER')
c.GenericOAuthenticator.oauth_callback_url = 'https://jupyterhub.krasting.org/hub/oauth_callback'
c.GenericOAuthenticator.username_claim = "preferred_username"

# --- Spawner Configuration ---
from dockerspawner import DockerSpawner
c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = 'jupyter/scipy-notebook:latest'
c.DockerSpawner.network_name = 'jupyterhub-network'

# --- Network & URL Configuration ---
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = 'jupyterhub'

# THIS IS THE FIX:
# Tell JupyterHub where to send users by default.
# This creates the redirect from the root URL (/) to the hub's home page.
c.JupyterHub.default_url = '/hub/home'

# The settings 'c.JupyterHub.bind_url' and 'c.JupyterHub.base_url' have been
# removed as they are now redundant and the defaults are correct.
