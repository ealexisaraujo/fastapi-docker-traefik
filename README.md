# Dockerizing FastAPI with Postgres, Uvicorn, and Traefik

## Want to learn how to build this?

Check out the [post](https://testdriven.io/blog/fastapi-docker-traefik/).

## Want to use this project?

### Development

Build the images, start the containers, wait for the app, and print the local URLs:

```sh
make dev
```

Test it out through Traefik:

1. [http://fastapi.localhost:8008/](http://fastapi.localhost:8008/)
1. [http://fastapi.localhost:8008/openapi.json](http://fastapi.localhost:8008/openapi.json)
1. [http://localhost:8081/dashboard/](http://localhost:8081/dashboard/)

The FastAPI container listens on port `8000` inside Docker, but that port is not
published directly to the host. Use `http://fastapi.localhost:8008/` in the
browser. `http://localhost:8000/` will not connect unless you add a direct port
mapping to the `web` service:

```yaml
ports:
  - "8000:8000"
```

Useful Make commands:

```sh
make help          # list all commands
make dev           # build and start the local stack
make smoke         # check the app through Traefik
make verify        # run app, dependency, and database checks
make verify-clean  # verify with a temporary stack and remove it afterward
make logs          # follow all service logs
make down          # stop and remove containers, keeping volumes
make clean         # stop and remove containers plus volumes
```

If you have an old local Postgres volume from a previous major version, run
`make clean` before `make dev` to recreate the development database volume.

### Production

Update the domain in _docker-compose.prod.yml_, and add your email to _traefik.prod.toml_.

Build the images and run the containers:

```sh
$ docker-compose -f docker-compose.prod.yml up -d --build
```
