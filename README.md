# Fitness/Health Tracker Website
This is a website designed to help users track various health and fitness metrics, including weight, mood, macros, calories, and step count. It also allows users to log their workouts and view their progress over time.

### PLEASE SEE BELOW FOR INSTALLATION/SETUP INSTRUCTIONS


## HOMEPAGE

![Model](https://github.com/wallt28/health-tracker/blob/main/gitImages/homepage_1.png)

![Model](https://github.com/wallt28/health-tracker/blob/main/gitImages/homepage_2.png)

![Model](https://github.com/wallt28/health-tracker/blob/main/gitImages/homepage_3.png)

## DASHBOARD

![Model](https://github.com/wallt28/health-tracker/blob/main/gitImages/dashboard_average_metrics.png)

![Model](https://github.com/wallt28/health-tracker/blob/main/gitImages/dashboard_metric_view.png)

![Model](https://github.com/wallt28/health-tracker/blob/main/gitImages/delete_metrics.png)

## WORKOUT TRACKER

![Model](https://github.com/wallt28/health-tracker/blob/main/gitImages/workout_tracker.png)

## LOGIN

![Model](https://github.com/wallt28/health-tracker/blob/main/gitImages/login_page_updated.png)

## REGISTER

![Model](https://github.com/wallt28/health-tracker/blob/main/gitImages/register_page_updated.png)


## Running the Application in Docker
To run this application in Docker, you'll need to have Docker installed on your system. You can download Docker for your operating system from the official Docker website.

### Starting the Application
To start the application, run the following command in the root directory of the project:
```docker-compose up```
This command will start the Flask application and the PostgreSQL database in separate Docker containers.

Once the application is running, you can access it by opening a web browser and navigating to http://localhost:5000. This will display the homepage of the application.

### Stopping the Application
To stop the application, press ``Ctrl-C`` in the terminal where you started the docker-compose up command. This will stop the containers and shut down the application.

### Configuration
You can configure the Flask application using environment variables. The following environment variables can be used:

**DATABASE_URL:** The URL of the PostgreSQL database to use. Defaults to ``postgresql://myuser:mypassword@db/healthtracker``.

**FLASK_APP:** The name of the Flask application package. Defaults to app.

**FLASK_ENV:** The environment mode for the Flask application. Defaults to production.


You can set these environment variables using a .env file in the root directory of the project. Note that if you modify the environment variables in the docker-compose.yml file, you'll need to rebuild the Docker image for the changes to take effect:

```docker-compose build```


The website should now be accessible by navigating to ``http://localhost:5000`` in your web browser.

## Usage
To use the website, users can create an account by clicking on the ``Login`` button on the homepage navbar then navigate to ``Register``.

Once logged in, this will generate a JWT/Access Token, then users can view & add their daily personalised metrics. 

Entries can also be deleted by navigating to ``/health_metric_logs/<USERID>`` 

By Navigating to the ``Workouts`` section, you can see your past workouts and see what workout you have for that particular day.

## Technologies Used
* Flask: Python web framework
* PostgreSQL: open-source relational database
* Bootstrap: front-end framework for responsive design
* Docker: containerization platform
* Flask_Bcrypt: password hashing for Flask
* Flask_SQLAlchemy: SQL toolkit and ORM for Flask
* Flask_WTF: integration of Flask with WTForms
* Plotly: Python graphing library
* PyJWT: JSON Web Token implementation in Python
* WTForms: form handling and validation library for Python
* JavaScript: programming language used for front-end development


## Contributing
If you have suggestions for how to improve this website, please feel free to submit an issue or pull request.

## License
This project is licensed under the MIT License.

