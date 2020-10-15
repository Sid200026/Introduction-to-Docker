# Introduction to Docker

### Table of Contents

- [ Terminologies ](#Terminologies)
- [ Nginx Image](#nginx)
- [ Dockerfile](#dockerfile)
- [ Development Build](#dev)
- [ Tags and Versions](#tagversion)
- [ Docker Hub](#dockerhub)
- [ Debugging Containers](#debugging)
- [ Docker Compose](#compose)

  <a name="Terminologies" />

## Terminologies

- Image : A Docker image is a read-only template that contains a set of instructions for creating a container that can run on the Docker platform. It provides a convenient way to package up applications and preconfigured server environments, which you can use for your own private use or share publicly with other Docker users.

- Container : A Docker Container is a running instance of an image. We download an image mostly from the docker hub registry and run in ( container )

- Volumes : Allows sharing of files and directories. Volume allows us to share data between host and container and also between containers.

- Dockerfile : Allow us to create our own images which can then be used to run as containers. Dockerfile contains a series of instruction which can be used for building the docker image.

- Docker Registry : A central repository similar to Github but for docker images which can be pulled onto a local system or a cloud for running it in containers. Most popular registry is Docker Hub.

- Docker Compose : A tool provided by Docker to run multicontainer applications.

---

<a name="nginx" />

## Nginx Image

### Pull the image

```docker
docker pull nginx
docker images
```

### Run the container

`docker pull nginx` downloads the image of nginx having the tag latest ( by default ) from the Docker Hub. `docker images` gives us a list of images available on the local system.

```docker
docker run -d nginx:latest
```

`-d` flag stands for detached mode. The above statement will run the nginx image in a container.To get the list of containers running on the system we can use

```docker
docker ps
# OR
docker container ls
```

From the above command, we can see that the nginx container exposes the port 80/tcp. To stop any container, we can use

```docker
docker stop <CONTAINER_ID OR CONTAINER_NAME>
```

Now the container has been stopped however it hasn't been removed. To start the container again

```docker
docker start <CONTAINER_ID OR CONTAINER_NAME>
```

To delete a container

```docker
docker rm <CONTAINER_ID OR CONTAINER_NAME>
```

To delete all the containers

```docker
docker rm $(docker ps -a --quiet)
# Quiet returns only the container id and -a gives us all the containers ( both running and exited )
```

Running containers need to be stopped first and then only it can be removed. If we directly try to remove without stopping, an error is thrown. We can also use the -f flag ( force ) to forcefully remove a running container.

```docker
docker rm -f <CONTAINER_ID OR CONTAINER_NAME>
```

Now we know the docker image of nginx exposes the port 80. What we want is to map the port 8080 of the local system to the port 80 on the docker image.

```docker
docker run -d -p 8080:80 nginx:latest
# 0.0.0.0:8080->80/tcp
```

Till now we we just exposed the port to 8080 of the system to 80 of the image. We can expose multiple ports to port 80 of the image.

```docker
docker run -d -p 8080:80 -p 3000:80 nginx:latest
# 0.0.0.0:3000->80/tcp, 0.0.0.0:8080->80/tc
```

If we see, everytime we run a container, a random name is provided to us for each running container. We want the name of the container to be based on our choice instead of a docker-allocated name. This also facilitates us see which container does what in a multi-container setup.

```docker
docker run -d -p 8080:80 --name sid nginx:latest
```

---

## Volumes

Nginx allows us to host some static sites via the following command

```docker
docker run -d -p 8080:80 --name nginx-example -v "/Users/apple/CS/Introduction to Docker/nginx-website":/usr/share/nginx/html:ro nginx
```

`ro` means read only.

Now since the directory is mounted, any change made to the file in the local system will be reflected in the container volume and ultimately in the running application. If any change is made inside the Docker file system, it will be reflected in the host system as well and vice-versa.

To execute commands inside the Docker container, we can use

```docker
docker exec -it nginx-example bash
```

We can also use volumes to communicate between containers

```docker
docker run -d -p 8080:80 --name nginx-example -v "/Users/apple/CS/Introduction to Docker/nginx-website":/usr/share/nginx/html:ro nginx
docker run --name nginx-copy -d -p 8000:80 --volumes-from nginx-example nginx
```

So far we have been using images from the docker hub registry. Now we'll learn how to develop custom Docker images.

_Bind Mounts vs Volumes_

- First, the big one is a behavior difference between named volumes and host volumes (aka bind mounts). Docker will initialize a named volume from the contents of the image. This includes the file owners and permissions. This means you can avoid worrying about permission issues that are commonly encountered with host volumes.

- Second, portability. Named volumes can be used from different docker hosts without worrying about the local filesystem paths or the user running the commands. Whether it's on a MacOS laptop, or a Linux server in production, you can just name a volume and assume it will work as part of the default docker install.

- Third, how they are managed. Host volumes are commonly managed outside of docker which is where the permission problems often come into play (since UID/GID on the host commonly doesn't match the UID/GID inside the container). With named volumes, you would manage them from within another docker container where you can control what tools are installed, users created, etc.

<a name="dockerfile" />

## Dockerfile

We rarely create dockerfile from scratch. Most Dockerfiles are based on images already available on Docker Hub.

- FROM : Used to specify the base image that is to be used to create the docker image
- ADD : The ADD instruction copies new files, directories or remote file URLs from source and adds them to the filesystem of the image at the path destination.
- WORKDIR : The WORKDIR instruction sets the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions that follow it in the Dockerfile. If the WORKDIR doesn’t exist, it will be created even if it’s not used in any subsequent Dockerfile instruction.
- RUN : The RUN instruction will execute any commands in a new layer on top of the current image and commit the results. The resulting committed image will be used for the next step in the Dockerfile.
- CMD : There can only be one CMD instruction in a Dockerfile. If you list more than one CMD then only the last CMD will take effect. The main purpose of a CMD is to provide defaults for an executing container. RUN is used when the image is being built whereas CMD is used when the container is being run.
- dockerignore : Some files that are not required in the resulting image.

To build an image

```docker
docker build --tag example_website:latest .
```

`.` asks docker to find the dockerfile in the current directory. Here the image name is example_website.

```docker
FROM node:latest
WORKDIR /app
ADD . .
RUN yarn install
CMD node index.js
```

The above Dockerfile consists of 5 layers where each line ( one command ) represents one layer. Layer is also used in caching. Suppose we are having an application which has the following dependencies

- React
- NextJS

The above packages takes more than a few minutes to install everytime. By default, Docker utitlizes caching to speedup subsequent image building. However suppose that we are changing the source code and adding an extra comment line. Now since the command `ADD . .` will produce a different output, all subsequent commands will need to be executed again. We need to take advantage of caching here. What we'll do is actually cache the package.json and package-lock.json files.

```docker
FROM node:latest
WORKDIR /app
ADD . .
RUN yarn install
CMD node index.js

FROM node:latest
WORKDIR /app
ADD package*.json .
RUN yarn install
ADD . .
CMD node index.js
```

The second approach heavily utilises caching. One key thing to remember here is once the a layer's output is changed, Docker will run all the subsequent layers again. The second stage utitlises the fact that any code change does not affect the project's dependency and node_modules.So moving the entire dependency commands above `ADD . .` ensures fast image building.

Generally we should try to use the alpine-distribution for each and every base images as it takes much less storage than the latest distribution.

<a name="dev" />

## Development Build

```docker
FROM node:alpine
WORKDIR /app
ADD package*.json ./
RUN yarn install
ADD . .
CMD yarn run dev

docker build -t custom_api:latest .
docker run -d -p 4000:4000 --name custom_api -v "$(pwd)":/app custom_api:latest
```

Utilises nodemon and volumes to ensure that any code changes results in updation of the container immediately.

<a name="tagversion" />

## Tags and Versions

Instead of using latest or alpine as a tag name for base image in the Dockerfile, a better alternative would be using the version for example node:13.4.3-alpine instead of node:alpine. This ensures that our application doesn't install the future versions of node. If we create another image with the same tag, the earlier image's tag is removed ( becomes none ).

```docker
docker build -t api_dev:latest
docker tag api_dev:latest api_dev:1.0.0
docker build -t api_dev:latest
```

---

<a name="dockerhub" />

## Docker Hub

Docker Hub is a central image register where we can push the images of the applications we create.

```docker
docker tag api_dev:latest sid200026/api_service:latest
docker push sid200026/api_service
```

Now the latest image will be uploaded in the docker register. To pull the image, we can use

```docker
docker pull sid200026/api_service
```

---

<a name="debugging" />

## Debugging Containers

- Inspect : Allows us to analyse the configuration of a docker container.

```docker
docker inspect dev-api
```

- Logs : Sometimes we want to know the logs that were generated during the container runtime. For example we may have some print statement that maybe important for our application.

```docker
docker logs -f dev-api
```

`-f` flag is used to ensure that we continuously get the logs as we run the application. Stands for follow.

- Exec : To get a sneak peak inside the docker container to see how things are operating internally.

```docker
docker exec -it dev-api /bin/sh
```

<a name="compose" />

## Docker Compose

A tool provided by Docker to run multicontainer applications. A docker compose can be run only on a single machine. Cannot be used in clusters ( Docker Swarm is used ). One of the most important functionality provided by docker-compose is state mapping for containers. Suppose we have 10 containers running and we change something in one of the containers. Now when we use `docker-compose up`, only that changed container will be recreated, others won't be touched.

```docker
docker-compose up -d --scale web=3
```

3 containers will be created for the service web. Doesn't work if it involves port mapping since all three containers will require the same port.