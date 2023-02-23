# Base image
#FROM postgres:latest

# Environment variables
#ENV POSTGRES_USER postgres
#ENV POSTGRES_PASSWORD mysecretpassword
#ENV POSTGRES_DB healthtracker

# Expose PostgreSQL port
#EXPOSE 5432

FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
