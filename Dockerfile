# Dockerfile (v1.3 - Added docker package for post-start hook)

# Use the official JupyterHub image as our starting point
FROM jupyterhub/jupyterhub:latest

# Install the dockerspawner package and docker for post-start hooks
RUN pip install dockerspawner oauthenticator docker

# NEW: Copy our configuration file into the image at the correct location
COPY jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py
