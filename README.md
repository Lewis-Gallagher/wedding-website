# wedding-website
A Python Flask app for our wedding
- [wedding-website](#wedding-website)
  - [Tools](#tools)
- [Run the App](#run-the-app)
- [Website Structure](#website-structure)
  - [Home Page](#home-page)
  - [RSVP Form](#rsvp-form)
  - [FAQ](#faq)
  - [Event Info](#event-info)
  - [The Story of Us](#the-story-of-us)
- [Flask App](#flask-app)
- [SQLite Database](#sqlite-database)
  - [Structure](#structure)
  - [Considerations](#considerations)
  - [Backups](#backups)
- [Docker Service](#docker-service)
  - [Docker Compose](#docker-compose)
    - [Run](#run)
    - [Logs](#logs)
    - [Monitoring](#monitoring)
    - [Restarting the Service](#restarting-the-service)
- [To do](#to-do)

## Tools
* **Flask** and various flask addons including Flask-WTForms and Flask-SQLAlchemy.
* **SQLite** for RSVP responses and invitees.
* **Docker** and **Docker Compose** for running the multi-container application.
* **Nginx** and **Gunicorn** to handle incoming requests and set up the web server respectively.
* **SendGrid** and the **SendGridAPIClient** for sending emails.
* **HTML, CSS** and **Jinja** for front-end development.
* **Digital Ocean** droplet Ubuntu virtual machine.

# Run the App
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

4. Launch the docker compose service from within the project directory (i.e. in the same directory as the `docker-compose.yml` file):
    ```bash
    sudo docker compose up -d
    ``` 

# Website Structure
## Home Page
Shows the digital invite card. All pages include a navigation bar with links to other areas of the site.

## RSVP Form
A Flask-WTForm with numerous fields:
* Attending: yes/no.
* Name (must be unique).
* Email address (must be unique and be an invited email address).
* Phone number.
* Dietary requirements (if any).
* An optional message.
## FAQ
A list of frequently asked questions and answers. Self-explanatory.
## Event Info
Information on the venue. Location, times, hotel recommendations and nearby towns.
## The Story of Us
A short story of our 5 years together, written by the bride.

# Flask App
The Flask application front end is written with HTML, CSS and Bootstrap with Jinja to interact with Guest RSVP responses. The RSVP form takes information from the user and emails the user, via the SendGrid API, a confirmation email with a custom message and their RSVP details included. The user's RSVP data is then written to a local SQLite database. Details of the database are expanded upon in the following section.

# SQLite Database
The app uses an SQLite database as it is lightweight and traffic is expected to be very low.  This is interacted with via the Flask SQLAlchemy package.

## Structure
The database contains two tables: Invited and Guest. The Invited table contains the email addresses of all invitees and a unique ID which is a foreign key to the Guest table. The Guest table contains attendee information including a unique I, name, contact information, dietary requirements and an optional message. 

## Considerations
The flask forms are set up so an RSVP may only be submitted with an email address that exists in the Invited table. This is to ensure no uninvited guests may RSVP and also prevents me from having guests register with an email address and password. This is not the most secure option as one may easily RSVP with someone else's email address, however, I felt a user registration system would be unnecessary for an otherwise static and non-interactive website.

## Backups
Database backups are important to not erroneously lose attendee information. This is achieved manually every time the database is manually accessed by running the [sq3backup.sh](sq3backup.sh) script: 
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

# Docker Service
I am using a Digital Ocean droplet running Ubuntu 20.04 to host the website. A small amount of set up is required to get things up and running. See [droplet-setup.md](droplet-setup.md) for details.

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
The docker service will automatically attempt to restart unless it is explicitly stopped, via the `restart: unless-stopped` argument. So in the event of the droplet being rebooted, or the app crashing, the docker service will restart automatically without the need for manual intervention.

# To do
1. TLS/SSL Certificate for HTTPS encryption.
2. Mount persistent storage to prevent data loss.