# Gym Helper

A web application for gym training built with **Django**. Users can browse exercises, choose a ready-made training plan or create their own, log workouts set by set and track their body weight on a chart.

## Features

- **Registration and login** with a custom user model
- **Exercise library** grouped by category, with descriptions and videos
- **Training plans**: ready-made plans and your own custom plans (create / delete)
- **Workouts**: start a training from a plan and log every set (series, repetitions, weight)
- **Training history** of completed workouts
- **Body weight tracking**: add measurements and see your progress on a chart (matplotlib)
- Django admin panel for managing exercises, categories and plans
- **REST API** (Django REST Framework) for exercises, plans, trainings and sets

## Tech stack

- **Python 3**, **Django 5.2**
- **Django REST Framework** for the API
- **SQLite** for local development, **PostgreSQL** in Docker
- **Docker Compose** with **gunicorn** and **nginx**
- **matplotlib** for the weight progress chart
- HTML templates and static files (CSS, images)

## Project structure

```
gymHelper/             # Project settings and main URL config
reg_log/               # Registration, login, user and weight models
main/                  # Main page and user profile (weight chart)
exercises/             # Exercise categories and exercises
training_plans/        # Ready-made and custom training plans
completed_trainings/   # Starting workouts, logging sets, history
```

## Getting started

1. Clone the repository:
   ```bash
   git clone https://github.com/ViktorUw/Gym-Helper.git
   cd Gym-Helper
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate     # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your settings. Copy the example file:
   ```bash
   cp .env.example .env          # Windows: copy .env.example .env
   ```
   Generate a secret key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Open `.env` and replace the `SECRET_KEY` value with the generated key (keep the single quotes):
   ```
   SECRET_KEY='your-generated-key'
   ```
4. Create the database, load sample exercises, categories and training plans, and create an admin account:
   ```bash
   python manage.py migrate
   python manage.py loaddata fixtures/initial_data.json
   python manage.py createsuperuser
   ```
5. Start the server:
   ```bash
   python manage.py runserver
   ```
6. Open http://127.0.0.1:8000/ in your browser. The admin panel is at `/admin/` (log in with the email you used in `createsuperuser`).

## Running with Docker

Docker Compose runs the app the way it would run on a server: PostgreSQL, Django with gunicorn, and nginx in front serving the static files and videos.

1. Create `.env.docker` from the example and fill in `SECRET_KEY` and `POSTGRES_PASSWORD`:
   ```bash
   cp .env.docker.example .env.docker
   ```
2. Build and start:
   ```bash
   docker compose up -d --build
   ```
   On the first start the app applies migrations and loads the sample exercises and plans.
3. Create an admin account:
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```
4. Open http://localhost:8080/.

Useful commands:

```bash
docker compose logs -f web    # app logs
docker compose down           # stop (the database is kept)
docker compose down -v        # stop and delete the database
```

To serve the app on another address (for example a server's domain), add it to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` in `.env.docker`.

## REST API

All endpoints are under `/api/` and need a logged-in user. In the browser, log in on the website and open http://127.0.0.1:8000/api/ to browse the API. Apps log in with a token:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ -d "username=you@example.com" -d "password=your-password"
# {"token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"}
curl http://127.0.0.1:8000/api/trainings/ -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

The `username` field takes the account's email.

| Endpoint | Methods | Description |
|---|---|---|
| `/api/exercises/` | GET | Exercises with their category |
| `/api/plans/` | GET | Ready-made plans with exercise ids |
| `/api/custom-plans/` | GET | Your own plans |
| `/api/trainings/` | GET, POST, PUT, PATCH, DELETE | Your trainings with sets and a summary; create one with `training_name` and `training_plan` or `custom_plan` |
| `/api/sets/` | GET, POST, PUT, PATCH, DELETE | Your sets (`training`, `exercise`, `repetitions`, `weight`); filter with `?training=<id>` |

Each list endpoint also has a detail URL, for example `/api/trainings/<id>/`. Other users' data returns 404.

A project presentation (in Polish) is included: `GymHeplerPrez.pdf`.

> The interface is in Polish. This is a study project: `.env.example` sets `DEBUG=True` for local development. The Docker setup runs with `DEBUG=False` over plain HTTP; a public server also needs HTTPS in front of it.
