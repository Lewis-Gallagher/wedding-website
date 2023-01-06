# wedding-website
A Python Flask app for our wedding
- [wedding-website](#wedding-website)
- [Website](#website)
  - [Pages](#pages)
    - [Home Page](#home-page)
    - [RSVP Form](#rsvp-form)
    - [FAQ](#faq)
    - [Event Info](#event-info)
    - [The Story of Us](#the-story-of-us)
- [SQLite Database](#sqlite-database)
  - [Structure](#structure)
  - [Considerations](#considerations)
  - [Backups](#backups)
- [Web Service](#web-service)
  - [Docker Compose](#docker-compose)
    - [Run](#run)
    - [Logs](#logs)
    - [Monitoring](#monitoring)
    - [Restarting the Service](#restarting-the-service)
    - [Environmental variables](#environmental-variables)
- [To do](#to-do)

# Website
## Pages
1. [Home Page](#home-page)
2. [RSVP Form](#rsvp-form)
3. [FAQ](#faq)
4. [Event Info](#event-info)
5. [The Story of Us](#the-story-of-us)

### Home Page
Shows the digital invite card. All pages include a navigation bar with links to other areas of the site.

### RSVP Form
A form with numerous fields:
* Attending: yes/no.
* Name (must be unique).
* Email address (must be unique and be an invited email address).
* Phone number.
* Dietary requirements (if any).
* An optional message.

### FAQ
A list of frequently asked questions and answers. Self explanatory.
### Event Info
Information on the venue. Location, times, hotel recommendations and nearby towns.
### The Story of Us
A short story of our 5 years together, written by the bride.

# SQLite Database
The app uses an SQLite database as it is lightweight and traffic is expected to be very low.  This is interacted with via the Flask SQLAlchemy package.

## Structure
The database contains two tables: Invited and Guest. The Invited table contains the email addresses of all invitees and a unique ID which is a foreign key to the Guest table. The Guest table contains attendee information including a unique I, name, contact information, dietary requirements and an optional message. 

## Considerations
The flask forms are set up so an RSVP may only be submitted with an email address that exists in the Invited table. This is to ensure no uninvited guests may RSVP and also prevents me from having guests register with an email address and password. This is not the most secure option as one may easily RSVP with someone else's email address, however, I felt a user registration system would be unnecessary for an otherwise static and non-interactive website.

## Backups
Database backups are important to not erroneously lose attendee information. This is achieved manually every time the database is manually accessed by running the `sq3backup.sh` script: 
```bash
. sq3backup.sh
``` 
This creates a backup file of the database, labelled with the date and time, within the `./bak` directory.

The database can be restored with:
 ```bash
 dbfile=bak/20221228-143151.app.db.sq3
 sqlite3 app.db ".restore $dbfile"
 ```

 Finally, the database can be exported to csv format with:
 ```bash
 sqlite3 -header -csv app.db "SELECT * from Guest;" > guests.csv
 ```

# Web Service
I am using a Digital Ocean droplet to host the website. The droplet is running Ubuntu 20.04 and a small amount of set up is required to get things up and running. See droplet-setup.md.

## Docker Compose
The service consists of two images. The first is built from the `Dockerfile` in the project directory, which contains the source code for the app. The second pulls the nginx container from Dockerhub. 

### Run
From there the service is run with docker compose in detached mode (`-d`) from the project directory, containing the `docker-compose.yml` file:
```bash
sudo docker compose up -d
```
### Logs
 Docker compose logs can be inspected by running the following command from the project directory, containing the `docker-compose.yml` file.
```bash
sudo docker compose logs
```
### Monitoring
The status of each container can be viewed with:
```bash
sudo docker ps
```
Which will output a list of all running containers
```
CONTAINER ID   IMAGE                   COMMAND                  CREATED        STATUS          PORTS                               NAMES
6bc904c67b99   nginx:1.23              "/docker-entrypoint.…"   10 hours ago   Up 21 minutes   0.0.0.0:80->80/tcp, :::80->80/tcp   nginx
51fb1a63d09f   wedding-website-flask   "gunicorn --bind 0.0…"   10 hours ago   Up 21 minutes                                       flask
```
### Restarting the Service
The docker service will automatically attempt to restart unless it is explicitly stopped, via the `restart: unless-stopped` argument. So in the event of the droplet being rebooted, or the app crashing, the docker service will restart automatically wihtout the need for manual intervention.

### Environmental variables
The flask app requires a few environmental variables to be set including a secret key to use CSRF Flask-WTF forms and a SendGrid API key for emails, both of which should not be published publicly.

A `.env` file should be created in the project directory in the following format
```bash
FLASK_APP=wedding-website.py
SENDGRID_API_KEY="********"
MAIL_DEFAULT_SENDER=lewis@nplgwedding.com
SECRET_KEY="a-secret-key"
```
The flask service in the `docker-compose.yml` file will use the `env_file: .env` argument to assign any variables inside the `.env` file when the container is launched. 

This isn't the most secure method, as anybody with root access to the droplet can inspect the container while it's running to view any set environmental variables. An alternative would be to use docker secrets, however this requires setting up docker as a swarm service.

# To do
1. TLS/SSL Certificate for HTTPS encryption.
2. Mount persistant storage.