# wedding-website
A Python Flask app for our wedding
- [wedding-website](#wedding-website)
- [Introduction](#introduction)
  - [Tools](#tools)
- [Running the App](#running-the-app)
  - [Quick Start](#quick-start)
  - [With Linux Server](#with-linux-server)
- [Certbot](#certbot)
  - [Certbot certificate renewal](#certbot-certificate-renewal)
- [SQLite Database](#sqlite-database)
  - [Structure](#structure)
  - [Considerations](#considerations)
  - [Backups](#backups)
- [Docker Service](#docker-service)
  - [Docker Compose](#docker-compose)
    - [Run](#run)
    - [Monitoring](#monitoring)
    - [Restarting the Service](#restarting-the-service)


# Introduction
Having a good few years of Python experience I decided to set myself the challenge of building my own web app from scratch for our wedding. Specifically a way of managing RSVPs and a source of information for guests. I ended up learning a lot more than I initially thought I would, such as domains, nginx web hosting, docker compose, email APIs and much much more.

## Tools
* **Flask** and various flask addons including Flask-WTForms and Flask-SQLAlchemy.
* **SQLite** for RSVP responses and invitees.
* **Docker** and **Docker Compose** for running the multi-container application.
* **Nginx** and **Gunicorn** to handle incoming requests and set up the web server respectively.
* **SendGrid** and the **SendGridAPIClient** for sending emails.
* **HTML, CSS, Bootstrap** and **Jinja** for front-end development.
* **Digital Ocean** droplet Ubuntu virtual machine.

# Running the App
## Quick Start
The app can be launched using the native Flask web server. While this isn't suitable for a production application, it is useful for testing.
1. Clone this repository.
    ```bash
    git clone https://github.com/Lewis-Gallagher/wedding-website.git
    ```

2. Create a python virtual environment and install the requirements from within the project directory.
    ```bash
    python3 -m venv venv
    pip install -r requirements.txt
    ```
3. Create a `.env` file containing environmental variables for the app:
   1. **FLASK_APP** - the name of the python file that loads the app.
   2. **SENDGRID_API_KEY** - A [SendGrid](https://sendgrid.com/) API key for sending emails.
   3. **SECRET_KEY** - A secret key for CSRF protection to use the FLask-WTF FlaskForms.
   4. **MAIL_DEFAULT_SENDER** - The email address which will send emails to invitees.
   
   For example:
    ```bash
    FLASK_APP=wedding-website.py
    SENDGRID_API_KEY="********"
    SECRET_KEY="example-secret-key"
    MAIL_DEFAULT_SENDER=lewis@nplgwedding.com
    ```

    _N.B. The `FLASK_APP` variable is required. The app will still run without the bottom three variables, however the RSVP form and confirmation emails will not be operational._

4. Launch the app via Flask
    ```bash
    flask run
    ```

## With Linux Server
1. The website requires a Ubuntu server with a small number of prerequisites which are detailed in the [droplet setup file](droplet-setup.md).
2. Clone this repository.
    ```bash
    git clone https://github.com/Lewis-Gallagher/wedding-website.git
    ```
3. Set up environmental variables for the service.
   1. **SENDGRID_API_KEY** - A [SendGrid](https://sendgrid.com/) API key for sending emails.
   2. **SECRET_KEY** - A secret key for CSRF protection to use the FLask-WTF FlaskForms.
   3. **MAIL_DEFAULT_SENDER** - The email address which will send emails to invitees.
   
    A `.env` file should be created in the project directory in the following format:
    ```bash
    SENDGRID_API_KEY="********"
    SECRET_KEY="example-secret-key"
    MAIL_DEFAULT_SENDER=lewis@nplgwedding.com
    ```
    The flask service in the [`docker compose yaml`](docker-compose.yml#L18) file will use the `env_file: .env` argument to assign variables inside the `.env` file when the container is launched. 

    _N.B. This isn't the most secure method, as anybody with root access to the droplet can inspect the container while it's running to view any set environmental variables. An alternative would be to use docker secrets, however, this requires setting up docker as a swarm service._

4. Launch the app profile of the docker service from within the project directory (i.e. in the same directory as the `docker-compose.yml` file):
    ```bash
    sudo docker compose up --profile app -d
    ``` 

# Certbot
## Certbot certificate renewal
The certbot certificates require renewal every 90 days. I haven't figured out how to enforce automatic renweal of certificates so for now these commands are run within the virutal machine hosting the app.
```bash
sudo docker compose --profile certbot run certbot renew --cert-name nplgwedding.com --force-renewal
sudo docker compose --profile certbot run certbot renew --cert-name www.nplgwedding.com --force-renewal
```
The Docker service may need to be restarted after these commands are run.

# SQLite Database
The app uses an SQLite database as it is lightweight and traffic is expected to be very low. This is interacted with via the Flask SQLAlchemy package.

## Structure
The database contains one table: `Guest`. The `Guest` table contains attendee information including a unique ID, name, contact information, dietary requirements and an optional message. 

## Considerations
Due to the relatively static nature of the site and the reality that most guests will only visti it once to submit their RSVPs, I felt a login service was unnecessary. This does mean that literally anyone can submit an RSVP to the site, regardless if they were invited to the wedding or not. The database is protected from SQL injections, and therefore the main consideration is potential malicious spam submitions.
## Backups
Database backups are important to not erroneously lose attendee information. This is achieved manually every time the database is manually accessed by running the [sq3backup.sh](sq3backup.sh) script: 
```bash
cd db/
. sq3backup.sh app.db
``` 
This creates a backup file of the database, labelled with the date and time, within the `db/bak/` directory.

The database can be restored with:
 ```bash
 dbfile=bak/20221228-143151.app.db.sq3
 sqlite3 app.db ".restore $dbfile"
 ```

 Finally, the database can be exported to csv format with:
 ```bash
 sqlite3 -header -csv app.db "SELECT * from Guest;" > guests.csv
 ```

# Docker Service
I am using a Digital Ocean droplet running Ubuntu 20.04 to host the website. A small amount of set up is required to get things up and running. See [droplet-setup.md](droplet-setup.md) for details.

## Docker Compose
The service consists of two images. The first is built from the `Dockerfile` in the project directory, which contains the source code for the app. The second pulls the nginx container from Dockerhub. 

### Run
From there the service is run with docker compose in detached mode (`-d`) from the project directory, containing the `docker-compose.yml` file:
```bash
sudo docker compose --profile app up -d
```
### Monitoring
The status of each container can be viewed with:
```bash
sudo docker ps
```
 Docker compose logs can be inspected by running the following command from the project directory, containing the `docker-compose.yml` file.
```bash
sudo docker compose logs
```
Which will output a list of all running containers
```
CONTAINER ID   IMAGE                   COMMAND                  CREATED        STATUS          PORTS                               NAMES
6bc904c67b99   nginx:1.23              "/docker-entrypoint.…"   10 hours ago   Up 21 minutes   0.0.0.0:80->80/tcp, :::80->80/tcp   nginx
51fb1a63d09f   wedding-website-flask   "gunicorn --bind 0.0…"   10 hours ago   Up 21 minutes                                       flask
```
### Restarting the Service
If stopped for any reason, the Docker service will automatically attempt to restart unless it is explicitly stopped, via the `restart: unless-stopped` argument. So in the event of the droplet being rebooted, or the app crashing, the Docker service will restart automatically without the need for manual intervention.