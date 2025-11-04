# /opt/jupyterhub/jupyterhub_config.py (v5.4 - WORKING VERSION)
import os
import pwd
import grp

# --- Pre-Spawn Hook for UID/GID Mapping ---
def pre_spawn_hook(spawner):
    username = spawner.user.name
    spawner.log.info(f"Pre-spawn hook called for user: {username}")
    
    try:
        # Look up the user on the host system
        user_info = pwd.getpwnam(username)
        uid = user_info.pw_uid
        gid = user_info.pw_gid
        
        spawner.log.info(f"Found user '{username}' with UID={uid}, GID={gid}")
        
        # Set the environment variables that jupyter/docker-stacks images use
        # We only set UID/GID, NOT the username - let it stay as 'jovyan'
        spawner.environment['NB_UID'] = str(uid)
        spawner.environment['NB_GID'] = str(gid)
        # DON'T set NB_USER - keep the default 'jovyan' username in the container
        spawner.environment['CHOWN_HOME'] = 'yes'
        spawner.environment['CHOWN_HOME_OPTS'] = '-R'
        
    except KeyError:
        spawner.log.error(
            f"User '{username}' not found in /etc/passwd on the host. "
            "Container will spawn with default UID/GID (1000)."
        )
        raise

c.DockerSpawner.pre_spawn_hook = pre_spawn_hook

# --- Authenticator Configuration ---
from oauthenticator.generic import GenericOAuthenticator
c.JupyterHub.authenticator_class = GenericOAuthenticator
c.GenericOAuthenticator.client_id = os.environ.get('OAUTH_CLIENT_ID')
c.GenericOAuthenticator.client_secret = os.environ.get('OAUTH_CLIENT_SECRET')
c.GenericOAuthenticator.oauth_callback_url = 'https://jupyterhub.krasting.org/hub/oauth_callback'
c.GenericOAuthenticator.authorize_url = os.environ.get('OAUTH_AUTHORIZE_URL')
c.GenericOAuthenticator.token_url = os.environ.get('OAUTH_TOKEN_URL')
c.GenericOAuthenticator.userdata_url = os.environ.get('OAUTH_USERDATA_URL')
c.GenericOAuthenticator.username_claim = "preferred_username"

# --- Authorization Configuration ---
c.Authenticator.allowed_users = {'krasting', 'another_user'}
c.Authenticator.admin_users = {'krasting'}

# --- Spawner Configuration ---
from dockerspawner import DockerSpawner
c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = 'jupyter/scipy-notebook:latest'
c.DockerSpawner.network_name = 'jupyterhub-network'
c.DockerSpawner.remove = True

# Volume mapping - mount host user's home to /home/jovyan/work
c.DockerSpawner.volumes = {
    '/home/{username}': '/home/jovyan/work'
}

# CRITICAL: Container must start as root for NB_UID/NB_GID to work
c.DockerSpawner.extra_create_kwargs = {'user': 'root'}

# Format the volume paths with the actual username
c.DockerSpawner.format_volume_name = lambda name, spawner: name.format(username=spawner.user.name)

# --- Network & URL Configuration ---
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = 'jupyterhub'
c.JupyterHub.default_url = '/hub/home'
