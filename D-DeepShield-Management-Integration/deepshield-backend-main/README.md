# Base Project - Back-End Implementation

This project is written using `Python version 3.13.2` and `Django version 5.0.6`.

## SETUP: 

### Prerequisites:
- [Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04) 20.10.08 or higher installed on your machine
- [Visual Studio Code](https://code.visualstudio.com/download) IDE
- [GitLab](https://about.gitlab.com/) account to access the project
- [Postman](https://www.postman.com/downloads/) for API development, testing, and access

### Source Code:
Obtain a copy of the source code by cloning this repository:
```sh
sudo git clone https://gitlab.com/secublox-platform/deepshield-backend.git
```

## Migrations in Django:
To apply migrations, run:
```sh
docker-compose run --rm deepshield_web_backend ./manage.py makemigrations base_app
docker-compose run --rm deepshield_web_backend ./manage.py migrate
```

### Create Superuser:
To create a superuser, run:
```sh
docker-compose run --rm deepshield_web_backend ./manage.py createsuperuser
```
After creating the superuser, add the wallet address and URI hash.

## Additional Setup Steps:

### Create User Groups:
Create two groups: `administrator` and `operator`.

### Create Node URL:
Set up the node URL for blockchain interaction.

### Create Blockchain URL:
Create the `blockchainBlockchainurl` for the blockchain explorer.

### Configure Global Settings:
Set up the global settings for the project version.

---

This should cover the initial setup and configuration needed to get the Base Project up and running. Make sure to follow each step carefully to ensure a smooth setup process.