FROM python:3.9

LABEL author="Lewis Gallagher" email="lewisjgallagher@gmail.com"

# Create new user named wedding-website.
RUN useradd wedding-website

# Set working directory where app will be installed.
WORKDIR /home/wedding-website

# Copy requirements file and build environment.
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

# Copy neccesary files.
COPY app app
COPY migrations migrations
COPY wedding-website.py config.py boot.sh ./

# Ensure boot.sh is executable.
RUN chmod +x boot.sh

# Sets FLASK_APP environmental variable inside the container.
ENV FLASK_APP wedding-website.py

# Sets ownership of all directories and files in ./ to wedding-website. 
RUN chown -R wedding-website:wedding-website ./

# Set default user.
USER wedding-website

# The EXPOSE command configures the port that this container will be using for its server. 
EXPOSE 5000

# ENTRYPOINT defines the default command that should be executed when the container is started. This is the command that will start the application web server.
ENTRYPOINT ["./boot.sh"]