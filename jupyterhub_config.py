# /opt/jupyterhub/jupyterhub_config.py (v3.2 - Explicit OIDC Endpoints)
import os

# --- Authenticator Configuration ---
from oauthenticator.generic import GenericOAuthenticator
c.JupyterHub.authenticator_class = GenericOAuthenticator

# Core OAuth details (no change)
c.GenericOAuthenticator.client_id = os.environ.get('OAUTH_CLIENT_ID')
c.GenericOAuthenticator.client_secret = os.environ.get('OAUTH_CLIENT_SECRET')
c.GenericOAuthenticator.oauth_callback_url = 'https://jupyterhub.krasting.org/hub/oauth_callback'

# OIDC discovery URL (we'll keep it for completeness)
c.GenericOAuthenticator.oidc_issuer = os.environ.get('OIDC_ISSUER')

# THIS IS THE FIX:
# Explicitly define the endpoints to bypass the failing auto-discovery.
c.GenericOAuthenticator.authorize_url = os.environ.get('OAUTH_AUTHORIZE_URL')
c.GenericOAuthenticator.token_url = os.environ.get('OAUTH_TOKEN_URL')
c.GenericOAuthenticator.userdata_url = os.environ.get('OAUTH_USERDATA_URL')

# How to find the username in the userdata response (no change)
c.GenericOAuthenticator.username_claim = "preferred_username"

# Authorize a specific list of users to access the hub.
# The usernames must match the 'preferred_username' from Authentik.
c.Authenticator.allowed_users = {'krasting'}
c.Authenticator.admin_users = {'krasting'}

# --- Spawner Configuration (no change) ---
from dockerspawner import DockerSpawner
c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = 'jupyter/scipy-notebook:latest'
c.DockerSpawner.network_name = 'jupyterhub-network'

# --- Network & URL Configuration (no change) ---
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = 'jupyterhub'
c.JupyterHub.default_url = '/hub/home'
