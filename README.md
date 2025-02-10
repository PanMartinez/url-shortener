# URL-SHORTENER

## Description:
This is API backend for url shortener app.
It accepts long urls and returns shortened codes, that act like tokens for stored long urls.

Please note!
: This is Alpha version of the project. There are few missing parts that are still to do:

- We are missing frontend application with domain name so all shortened urls are in "code-only" mode. In Next iterations of the app shortened url will have domain attached to it as well.
- docker ndb configuration is using different host that local postgres one. There is need to tweak configuration.

## Development and testing
### Ensure you have following installed in your system
- poetry
- postgresql

After forking this app into your system add `.env` file to the root catalogue. You can use `.env-template` file for
reference:

To create JWT secret key you can use following script:
```python
import os

print(os.urandom(32).hex())
```

## Configure database
open psql shell
```shell
psql
```

create database user
```shell
CREATE ROLE username WITH LOGIN PASSWORD 'password';
```

add user privileges for creating test databases
```shell
ALTER USER username CREATEDB;
```

create database
```shell
CREATE DATABASE databasename OWNER username ENCODING UTF8;
```

Then run following commands from root catalogue:

### Install dependencies

```shell
poetry install
```

### Install pre-commit

```shell
pre-commit install
```

### Enter poetry virtualenv
```shell
poetry shell
```

### Run pytest
```shell
pytest
```

### Run fastapi localhost
```shell
fastapi dev
```


## Running docker:

### Ensure you have the following installed in your system:
- Docker
- Docker Compose

Before running docker commands, ensure that you have docker daemon running

Please note!
: Before building docker app change your `.env`

```
DB_HOST=db
```

Build application
```shell
docker-compose up --build
```


### Testing App
by default application is running on `http://localhost:8000/docs`

In order to create shortened urls, first create user using `api/auth/register` endpoint

With created credentials move to `Authenticate` section of swagger and use credentials of created user

To create shorten url go over to `api/urls/shorten_url` endpoint, and send desired url to shorten. You have to be authorized to use this endpoint

To retrieve url from DB, use `api/urls/get_url` endpoint. You don't have to be authorised to use this endpoint.
