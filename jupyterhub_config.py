# /opt/jupyterhub/jupyterhub_config.py (v4.7 - The Complete Official Method)
import os
import pwd
import grp

# --- Pre-Spawn Hook for UID/GID Mapping ---
def pre_spawn_hook(spawner):
    username = spawner.user.name
    try:
        user_info = pwd.getpwnam(username)
        uid = user_info.pw_uid
        gid = user_info.pw_gid
        # Set the environment variables the jupyter/docker-stacks images expect
        spawner.environment['NB_UID'] = str(uid)
        spawner.environment['NB_GID'] = str(gid)
        spawner.environment['GRANT_SUDO'] = 'yes'
    except KeyError:
        spawner.log.warning(
            f"User '{username}' not found on the host. "
            "Spawning container with default UID/GID."
        )

# --- Authenticator Configuration (no changes) ---
from oauthenticator.generic import GenericOAuthenticator
c.JupyterHub.authenticator_class = GenericOAuthenticator
# ... (all your GenericOAuthenticator settings remain the same) ...
c.GenericOAuthenticator.client_id = os.environ.get('OAUTH_CLIENT_ID')
c.GenericOAuthenticator.client_secret = os.environ.get('OAUTH_CLIENT_SECRET')
c.GenericOAuthenticator.oauth_callback_url = 'https://jupyterhub.krasting.org/hub/oauth_callback'
c.GenericOAuthenticator.oidc_issuer = os.environ.get('OIDC_ISSUER')
c.GenericOAuthenticator.authorize_url = os.environ.get('OAUTH_AUTHORIZE_URL')
c.GenericOAuthenticator.token_url = os.environ.get('OAUTH_TOKEN_URL')
c.GenericOAuthenticator.userdata_url = os.environ.get('OAUTH_USERDATA_URL')
c.GenericOAuthenticator.username_claim = "preferred_username"

# --- Authorization Configuration (no changes) ---
c.Authenticator.allowed_users = {'krasting', 'another_user'}
c.Authenticator.admin_users = {'krasting'}

# --- Spawner Configuration ---
from dockerspawner import DockerSpawner
c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = 'jupyter/scipy-notebook:latest'
c.DockerSpawner.network_name = 'jupyterhub-network'
c.DockerSpawner.remove = True
c.DockerSpawner.volumes = {
    '/home/{username}': '/home/jovyan/work'
}
c.DockerSpawner.pre_spawn_hook = pre_spawn_hook

# THIS IS THE FIX:
# Re-add this line. The container MUST start as root for the
# NB_UID/NB_GID environment variables to be effective.
c.DockerSpawner.user = 'root'

# --- Network & URL Configuration (no changes) ---
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = 'jupyterhub'
c.JupyterHub.default_url = '/hub/home'
