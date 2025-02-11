# URL-SHORTENER

## Description:
This is API backend for url shortener app.
It accepts long urls and returns shortened codes, that act like tokens for stored long urls.

Please note!
: This is Alpha version of the project. There are few missing parts that are still to do:

- We are missing frontend application with domain name so all shortened urls are in "code-only" mode. In Next iterations of the app shortened url will have domain attached to it as well.
- Docker configuration is NOT production ready. Fastapi dev mode is on, with life reload.
- Urls ownership idea is not 100% crystalized. More validation is required around urls CRUD services

## Local development
### Ensure you have following installed in your system
- Docker
- Docker Compose
- poetry
- postgresql

### Create `.env` file
After forking this app into your system add `.env` file to the root catalogue. You can use `.env-template` file for
reference


### Create poetry env
From the Root catalogue run following commands

```shell
poetry install
```
### Enter poetry virtualenv
```shell
poetry shell
```

### Env updates
After each update to env export it to requirements file, so docker can use them
```shell
poetry export --without-hashes --format=requirements.txt > requirements.txt
```

### Install pre-commit
```shell
pre-commit install
```


## Running docker:
Before running docker commands, ensure that you have docker daemon running


Build application
```shell
docker-compose up --build
```
Please Note!
: Docker application running in the DEV mode. This means that all of local development changes will be reflected in the container


## Running pytest
With url_shortener container running, enter it with following command:
```shell
docker exec -it url_shortener sh
```
inside container run following command to run all unittests from the app
```shell
pytest
```

## Testing App
by default application is running on `http://localhost:8000/docs`

In order to create shortened urls, first create user using `api/auth/register` endpoint

With created credentials move to `Authenticate` section of swagger and use credentials of created user

To create shorten url go over to `api/urls/shorten_url` endpoint, and send desired url to shorten. You have to be authorized to use this endpoint

To retrieve url from DB, use `api/urls/get_url` endpoint. You don't have to be authorised to use this endpoint.
