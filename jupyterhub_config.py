# /opt/jupyterhub/jupyterhub_config.py (v3.0 - Authentik Integration)
import os

# --- Authenticator Configuration ---
# Use the GenericOAuthenticator for Authentik
from oauthenticator.generic import GenericOAuthenticator
c.JupyterHub.authenticator_class = GenericOAuthenticator

# Use environment variables for secrets
c.GenericOAuthenticator.client_id = os.environ.get('OAUTH_CLIENT_ID')
c.GenericOAuthenticator.client_secret = os.environ.get('OAUTH_CLIENT_SECRET')

# This is the .well-known/openid-configuration URL from Authentik
c.GenericOAuthenticator.oidc_issuer = os.environ.get('OIDC_ISSUER')

# The URL that Authentik will redirect back to
c.GenericOAuthenticator.oauth_callback_url = 'https://jupyterhub.krasting.org/hub/oauth_callback'

# The claim in the OIDC token that contains the username
c.GenericOAuthenticator.username_claim = "preferred_username"

# --- Spawner Configuration (no changes needed) ---
from dockerspawner import DockerSpawner
c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = 'jupyter/scipy-notebook:latest'
c.DockerSpawner.network_name = 'jupyterhub-network'

# --- Network & URL Configuration ---
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = 'jupyterhub'

# CRITICAL: Tell the Hub its public-facing URL
# This is necessary for the reverse proxy to work correctly.
c.JupyterHub.bind_url = 'http://:8000'
c.JupyterHub.base_url = '/hub'
