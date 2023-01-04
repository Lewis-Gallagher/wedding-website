FROM python:3.10-slim

LABEL author="Lewis Gallagher" email="lewisjgallagher@gmail.com"

# App install location
ENV CONTAINER_HOME=/var/www

# Add all local files to install directory
ADD . ${CONTAINER_HOME}

# Set working directory where app will be installed.
WORKDIR ${CONTAINER_HOME}

# Install dependencies
RUN pip install -r ${CONTAINER_HOME}/requirements.txt