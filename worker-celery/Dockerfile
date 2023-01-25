###########
# BUILDER #
###########

# pull official base image
FROM --platform=linux/amd64 python:3.10.8-slim-buster as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# lint
RUN pip install --upgrade pip

# copy project
COPY service-app1 /usr/src/app/
COPY worker-celery /usr/src/app/celery/

# copy celery TODO may be removed!!!
COPY worker-celery/start.sh /usr/src/app/start-celeryworker

# install python dependencies
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM --platform=linux/amd64 python:3.10.8-slim-buster

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint
COPY service-app1/entrypoint.sh $APP_HOME

# copy project
COPY service-app1 $APP_HOME
COPY worker-celery $APP_HOME/worker-celery/
# celery
COPY worker-celery/start.sh $APP_HOME/start-celeryworker
RUN sed -i 's/\r$//g' $APP_HOME/start-celeryworker
RUN chmod +x $APP_HOME/start-celeryworker

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run celery start.sh
CMD ["/home/app/web/start-celeryworker"]
