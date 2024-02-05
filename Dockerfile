FROM python:3.11-alpine AS base
#alpine is the image, alpine is small enough to use
#each line of code here is a layer, and the image is the base

ARG ENVIRONMENT
# This mean that there is an env var called ENVIRONMENT that we get from the docker-compose
# This is to let the OS know are we in the local container or test container so that we can download the correct packages

ENV PYROOT /pyroot
# this mean we create an env var name PYROOT with the value /pyroot
ENV PYTHONUSERBASE ${PYROOT}
# create an env var name PYTHONUSERBASE with the value of the env var PYROOT
# this is important since it tells the system the base dir for user
ENV PATH=${PATH}:${PYROOT}/bin
# PATH referance the existing path $PATH that added on to with the things behind it
# this will be the list of places that our OS will look for excutables for

# => The point is we need the base usr dir where our installation will go and since we install them we want to make sure the OS is able to find the exc files
RUN PIP_USER=1 pip install pipenv
COPY Pipfile* ./
RUN if [ "$ENVIRONMENT" = "test" ]; then PIP_USER=1 pipenv install --system --deploy --ignore-pipfile --dev; \
  else PIP_USER=1 pipenv install --system --deploy --ignore-pipfile; fi
#--system allow us to install everything in system wide, so that later on if we need it we dont need to go to the VM again
#--deploy help abort anything that goes wrong
#PIP_USER=1 make the installation as the user installation
# Remember the space between square bracket because this is bash cmd

FROM python:3.11-alpine

ENV PYROOT /pyroot
ENV PYTHONUSERBASE ${PYROOT}
ENV PATH=${PATH}:${PYROOT}/bin

RUN addgroup -S myapp && adduser -S -G myapp user -u 1234
# Add a group to the system (-S) then add user (adduser) name "user" into group (-G) myapp

COPY --chown=user:myapp --from=base ${PYROOT}/ ${PYROOT}/
# We copy all the package that we downloaded from the pipenv isntall from the base


RUN mkdir -p /usr/src/app
#app here work just like the dir FirstPythonProject
WORKDIR /usr/src
#work dir automatically set the program to work with this dir
#this mean copy those file to current working dir
COPY --chown=user:myapp app ./app
# Copy the content of the app folder into the app folder (this one is a new created one) of this working directory

USER 1234
# Allow to run as user that name "user", it is no longer root user

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
# Do NOT use "reload" since it slows the system down


# So all step above help create the structure as same as what we have

# Now we have to build the image by: docker build -t <name>:latest <location>     (docker build -t <name>:latest .)
# latest tag keep the consistency of the image
# dot tag means cur dir

#Then run the image as the container: docker run --name <container name> -p <outsideport>:<containerport> <name from build>:latest
# -p flag allow to do port forwarding, means look at the outsideport that is looking at containerport
# Note: whenever we update the image we have to build it again, but to run it you need to run it as a "different container name" or u delete the prev one


