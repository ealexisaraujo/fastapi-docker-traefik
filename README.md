# Dockerizing FastAPI with Postgres, Uvicorn, and Traefik

## Want to learn how to build this?

Check out the [post](https://testdriven.io/blog/fastapi-docker-traefik/).

## Want to use this project?

### Development

Build the images and spin up the containers:

```sh
$ docker-compose up -d --build
```

Test it out:

1. [http://fastapi.localhost:8008/](http://fastapi.localhost:8008/)
1. [http://fastapi.localhost:8081/](http://fastapi.localhost:8081/)

### Production

Update the domain in _docker-compose.prod.yml_, and add your email to _traefik.prod.toml_.

Build the images and run the containers:

```sh
$ docker-compose -f docker-compose.prod.yml up -d --build
```
