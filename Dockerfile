#root user
#def name of the image that we are going to be using
#alpine - very light and does not have unnecessary dependencies witch make it great for docker containers
FROM python:3.9-alpine3.13
LABEL maintainer="ceca_pereca.com"

ENV PYTHONUNBUFFERED 1

#copy our requirments.txt file from our local machine 
#to /tmp/requirements.txt or in the other words to docker image
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
#copy thea app directory that contains django app to /app in container
COPY ./app /app
#working directory from which commands will be run on our Docker image
WORKDIR /app
#port exposed from container to our machine
#this is a way to connect to the django development server
EXPOSE 8000

#bice overrajdovana u dockerfile-u na true
#ali ovde je tsavljena ova linije na false da ne bi runovo u divelopmentu
ARG DEV=false

#runs command on alphine image
#python -m venv /py && \                            - creates new virtual env that we are going to use to store our dependencies
#/py/bin/pip install --upgrade pip && \             - full path to our virtual env to upgrade pip or pythpn package manager inside ou virtuel maschine
#/py/bin/pip install -r /tmp/requirements.txt && \  - install our requerments to our docker image
#    rm -rf /tmp && \                               - remove the tmp dir because we dont want any extra dependencies on our image once its being created to keep it light weight
#    adduser \                                      - calls func adduser command to make new user inside our image, because best pactise is to not use root user with full privilages
#        --disabled-password \                      - why? if app gets compromised the attacker may have full access to everything on the docker container
#        --no-create-home \                         - disable password and we dont want to people log on to our container using password
#        django-user                                -dont create home for user, we give user name or in this case django-user
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \ 
    /py/bin/pip install -r /tmp/requirements.txt && \
    #shell command conditionally
    if [ "$DEV" = "true" ]; then \
    /py/bin/pip install -r /tmp/requirements.dev.txt ;\
    fi
    RUN rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user 
    
#path is env variable that automatically created on linux os, 
#def all dir where our executables can be run
#when we run any command in our project we dont want to have to specify full path of our virtual env
#adds /py/bin:$PATH to system path and when we run pyuthon commands it will outomaticly run from our virtuel env
ENV PATH="/py/bin:$PATH"

#last line always
#user we are swithing to
#doent have root privilages
USER django-user 
