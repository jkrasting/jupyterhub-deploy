# Dockerfile (v1.1)

# Use the official JupyterHub image as our starting point
FROM jupyterhub/jupyterhub:latest

# Install the dockerspawner package
RUN pip install dockerspawner oauthenticator

# NEW: Copy our configuration file into the image at the correct location
COPY jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py
