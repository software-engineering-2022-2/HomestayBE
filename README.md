# Homestay Backend Applcation
Backend for the Homestay Renting Website
This repository is the backend for the Homestay Renting Website that uses Django framework, utilizes PostgreSQL as the database and is containerized using Docker.

## Prerequisites

Before running the web app, ensure that you have the following dependencies installed on your system:

- Docker
- Docker Compose

## Getting Started

To run the Django web app locally with Docker, follow these steps:

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/HomestayBE.git
   ```
2. Go to the repository:

   ```shell
   cd HomestayBE
   ```
3. Start the containers:

   ```shell
   docker compose up
   ```
4. Access the web app in your browser:

   ```angular2html
   http://0.0.0.0:8000
   ```
## Configuration

The web app uses environment variables to configure certain settings. You can modify the environment variables in the `docker-compose.yml` file to suit your needs. The default configuration includes the following variables:

- `POSTGRES_NAME`: The name of the PostgreSQL database.
- `POSTGRES_USER`: The username for the PostgreSQL database.
- `POSTGRES_PASSWORD`: The password for the PostgreSQL database. 
- `DJANGO_SECRET_KEY`: The application secret key
- `DJANGO_DEBUG`: Option to run the application in the debugging mode

You can customize these variables according to your preferences or specific requirements.
