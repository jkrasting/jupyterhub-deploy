# /opt/jupyterhub/jupyterhub_config.py (v4.0 - Host Integration)
import os

# --- Authenticator Configuration (no changes) ---
from oauthenticator.generic import GenericOAuthenticator
c.JupyterHub.authenticator_class = GenericOAuthenticator
c.GenericOAuthenticator.client_id = os.environ.get('OAUTH_CLIENT_ID')
c.GenericOAuthenticator.client_secret = os.environ.get('OAUTH_CLIENT_SECRET')
c.GenericOAuthenticator.oauth_callback_url = 'https://jupyterhub.krasting.org/hub/oauth_callback'
c.GenericOAuthenticator.oidc_issuer = os.environ.get('OIDC_ISSUER')
c.GenericOAuthenticator.authorize_url = os.environ.get('OAUTH_AUTHORIZE_URL')
c.GenericOAuthenticator.token_url = os.environ.get('OAUTH_TOKEN_URL')
c.GenericOAuthenticator.userdata_url = os.environ.get('OAUTH_USERDATA_URL')
c.GenericOAuthenticator.username_claim = "preferred_username"

# --- Authorization Configuration (no changes) ---
c.Authenticator.allowed_users = {'krasting'} # Make sure your test user is in this list!
c.Authenticator.admin_users = {'krasting'}

# --- Spawner Configuration (additions) ---
from dockerspawner import DockerSpawner
c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = 'jupyter/scipy-notebook:latest'
c.DockerSpawner.network_name = 'jupyterhub-network'

# --- NEW: User Persistence and Host Integration ---
# This is the key. It tells the spawner to mount a host volume.
# The `{username}` placeholder is automatically replaced by JupyterHub.
c.DockerSpawner.volumes = {
    '/home/{username}': '/home/jovyan/work'
}
# This ensures that the user's container is removed when they stop their server
c.DockerSpawner.remove = True

# --- Network & URL Configuration (no changes) ---
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = 'jupyterhub'
c.JupyterHub.default_url = '/hub/home'
