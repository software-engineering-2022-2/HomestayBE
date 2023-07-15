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
   
   Create a `.env` file. You can copy the content of the .env.example file into the `.env` file. The content might look like this:

   ```
   DB_NAME=homestay
   DB_USER=06ff1pb80clj48uxwmki
   DB_PASSWORD=pscale_pw_xE8lHB8hdezASWc4vIhYdsgBHZ8EGBSVsFkmM35RSy6
   DB_HOST=aws.connect.psdb.cloud
   DB_PORT=3306
   MYSQL_ATTR_SSL_CA=/etc/ssl/certs/ca-certificates.crt
   DJANGO_SECRET_KEY=django-insecure-tvmo(-q3s1sosis=fi+rqc4$31e2%3j_k2s2+g!712++!o36t9
   DJANGO_DEBUG=True
   ```

   Remove all the images and containers related to the project to start a fresh download. This will prevent docker from using the older images.

   ```
   docker container rm <container_name>
   docker rmi <image_name>
   ```

3. Start the containers:

   ```shell
   docker compose up
   ```

   In the first run, it might not work as the database is not yet created. You should manually create the database by running the following command:

   ```
   docker exec -it <container_name> python manage.py migrate
   ```

   Then restart the containers by running the previous command again and it will work.

4. Access the web app in your browser:

   ```
   http://0.0.0.0:8000
   ```
