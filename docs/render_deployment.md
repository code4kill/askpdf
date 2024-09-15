---
title: How to deploy on render
---

# Deploying python API on render using docker 

Render provide a platform to productionize your application Build, deploy, and scale your apps with unparalleled ease.
[render.com](https://render.com/)


* Create your free account [render.com](https://render.com/).

## Creating docker file to build image for python app

* Create `Dockerfile` 
* Add the following code 

```bash
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container


# Copy the current directory contents into the container at /app
COPY ./apps/6 .

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements/install.txt

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run the FastAPI server using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

```

* Build docker image

```bash
docker build -t askpdf:dev .
```

* Run the image

```bash
docker run -d -t -e OPENAI_API_KEY=<API-KEY> -e FILE_UPLOAD_PATH=<PATH_TO_FOLDER> askpdf:dev
```

The above command will run application at PORT 8000.

`http://containerIP:8000/docs`.

## Push the image to dockerhub

Create an account on [dockerhub](https://hub.docker.com/)

* Create a repository on dockerhub for example `askpdf`.

* Login to dockerhub in terminal

```bash
docker login
```
authenticate your docker with dockerhub credentials.

* Tag the created image

```bash
# docker tag <local-image> <username>/<repository>:<tag>
docker tag askpdf:dev nirajsah17/askpdf:dev
```
* Push image to docker hub

```bash 
# docker push <username>/<repository>:<tag>
docker push nirajsah17/askpdf:dev
```
Now our app image is push to the **dockerhub**.

We will use this image to deploy our app.

## Deploy on the Render

* Login to Render

* Click on `+ new` in right side of nav bar.
* Then Choose `web services` from dropdown.
* Here we get three section `git provider`, `public git repo` and `Existing Image`.
* We will deploy using Image so choose `Existing Image`.
* Add the Image URL eg. `nirajsah17/askpdf:dev` and add credential if it's private repository.

* Then click on **connect**.

## Here is the deployed API

[swagger docs](https://askpdf-dev.onrender.com/docs)


