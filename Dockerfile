# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

EXPOSE 8000

# copy project
COPY ./source /app

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
