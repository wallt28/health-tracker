# Fitness/Health Tracker Website
This is a website designed to help users track various health and fitness metrics, including weight, mood, macros, calories, and step count. It also allows users to log their workouts and view their progress over time.

## Installation
1. Install Docker on your local machine.
2. Clone this repository to your local machine.
3. In the project directory, build the Docker container for the Flask application by running the following command:
``docker build -t healthtracker`` 
4. Build the Docker container for the Postgres database by running the following command:
``docker build -t postgres-db -f Dockerfile.postgres``
5. After the containers are built, start them using the following command:
``docker-compose up``


The website should now be accessible by navigating to ``http://localhost:5000`` in your web browser.

## Usage
To use the website, users can create an account by clicking on the ``Login`` button on the homepage navbar then navigate to ``Register``.

Once logged in, this will generate a JWT/Access Token, then users can view & add their daily personalised metrics. 

Entries can also be deleted by navigating to ``/health_metric_logs/<USERID>`` 

By Navigating to the ``Workouts`` section, you can see your past workouts and see what workout you have for that particular day.

## Technologies Used
Flask - Python web framework
PostgreSQL - open source relational database
Bootstrap - front-end framework for designing responsive websites
Docker - containerization platform

## Contributing
If you have suggestions for how to improve this website, please feel free to submit an issue or pull request.

## License
This project is licensed under the MIT License.

## Dockerfile.postgres
```
# Base image
FROM postgres:latest

# Environment variables
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD mysecretpassword
ENV POSTGRES_DB healthtracker

# Copy database initialization script
COPY init.sql /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432
```

In the Dockerfile.postgres file, we are using the official Postgres Docker image as a base and setting the environment variables POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB. 

We are also copying a database initialization script and exposing the Postgres port.

When running the containers with docker-compose, the postgres-db service will use this Dockerfile to build the Postgres container.
