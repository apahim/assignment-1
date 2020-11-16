# Cloudy

Web Application created for the WIT module "Cloud Architecture", as part of the
activity "Assignment 1".

## Quickstart

To execute the application from Docker, run:

```bash
$ docker run --rm -it -p 8080:8080 docker.io/apahim/cloudy
```

## Develop

Run the PostgreSQL container:

```bash
$ docker run -d --rm -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres
```

Export the `DB_URI` environment variable:

```bash
$ export DB_URI='postgresql://postgres:postgres@localhost:5432/postgres'
```

Create a virtualenv and activate it:

```bash
$ python3 -v venv venv
# source venv/bin/activate
```

Install the package in develop mode:

```bash
(venv) $ pip install -e .
```

Run the service:

```bash
(venv) $ python cloudy/app.py 
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
INFO:werkzeug: * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
INFO:werkzeug: * Restarting with stat
WARNING:werkzeug: * Debugger is active!
INFO:werkzeug: * Debugger PIN: 737-434-267
```

## Build and Publish

The application is distributed as a Docker image. To build the image, run:

```bash
$ docker build -t <registry/repository/image:tag> .
``` 

To publish, run:

```bash
$ docker push <registry/repository/image:tag>
``` 