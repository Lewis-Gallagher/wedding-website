# Droplet Setup
This file details the steps taken to set up the [Digial Ocean droplet](https://www.digitalocean.com/products/droplets) to run the application with Docker, Nginx, Gunicorn and Flask.

# User Setup
The frist step of setup is to add a new user, in this case `lgallagher`, and to add it to the sudo user group.

```bash
adduser lgallagher
addgroup lgallagher sudo
```

Now I can ssh into a the droplet with:
```bash
ssh lgallagher@159.89.98.147
```

...or, because my username on my local machine is also `lgallagher` I can simply run:

```bash
ssh 159.89.98.147
```

# Dependencies
Update package list and install SQLite on the Ubuntu droplet. 
```bash
sudo apt install update
sudo apt install upgrade
sudo apt install sqlite3
```

## Docker
The droplet does not come with docker installed, so we install this using a convenience script from the [docker docs](https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script).

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
Executing docker install script, commit: 7cae5f8b0decc17d6571f9f52eb840fbc13b2737
<...>
```
This installs `docker` and `docker compose`

## App setup
Simply clone the git repository to the new user `lgallagher` home directory.
```bash
cd
git clone https://github.com/Lewis-Gallagher/wedding-website.git
```