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

## Tech stack

- **Python 3**, **Django 5.1**
- **SQLite**
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
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Apply migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
4. Open http://127.0.0.1:8000/ in your browser.

The repository includes a `db.sqlite3` file with sample exercises and plans. To use the admin panel, create an account with `python manage.py createsuperuser` and go to `/admin/`.

A project presentation (in Polish) is included: `GymHeplerPrez.pdf`.

> The interface is in Polish. This is a study project and runs with `DEBUG = True`; it is not configured for production.
