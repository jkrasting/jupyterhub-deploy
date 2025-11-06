# /opt/jupyterhub/jupyterhub_config.py (v6.6 - Fixed image pull policy)
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
        
        # Set Jupyter to look for kernels at the host path location
        spawner.environment['JUPYTER_DATA_DIR'] = f'/home/{username}/.local/share/jupyter'
        
        # Simple volume mounts - mount at the original paths
        spawner.volumes = {
            f'/home/{username}': f'/home/{username}',
            '/storage': '/storage'
        }
        
        # Set the notebook directory to the user's home
        spawner.notebook_dir = f'/home/{username}'
        
        # Allow container to access host's SSH tunnels
        # This gives access to ALL forwarded ports (6022, 6023, etc.)
        spawner.extra_host_config = {
            'extra_hosts': {
                'host.docker.internal': 'host-gateway'
            }
        }
        
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
# Use our custom notebook image with Dask pre-installed
c.DockerSpawner.image = 'jupyterhub-notebook-dask:latest'
c.DockerSpawner.network_name = 'jupyterhub-network'
c.DockerSpawner.remove = True

# Don't try to pull the image - use local image only
c.DockerSpawner.pull_policy = 'Never'

# Add a post-start command to create the SSH symlink
c.DockerSpawner.post_start_cmd = 'ln -sf /home/{username}/.ssh /home/jovyan/.ssh'

# CRITICAL: Container must start as root for NB_UID/NB_GID to work
c.DockerSpawner.extra_create_kwargs = {'user': 'root'}

# --- Network & URL Configuration ---
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = 'jupyterhub'
c.JupyterHub.default_url = '/hub/home'
