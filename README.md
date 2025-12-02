# Habit Tracking System
A smart habit-tracking backend built with Django, featuring:

    ✔ Habit management
    ✔ Habit completion logs
    ✔ Environment-based suggestions
    ✔ Scoring, mood tracking, and streak logic
    ✔ Extensible validation and analytics

## Project Overview
This project provides backend models for a personalized habit-tracking application.
It collects user habits, tracks completions, analyzes environment triggers, and enables smart habit recommendations.

## Implemented Features
### 1.Habit Management
    .CRUD operation for Habit
        .Endpoints:
            .GET /api/habits/ – List all habit
            .POST /api/habits/ – Add a new habit
            .PUT /api/habits/{id}/ – Update habit details
            .DELETE /api/habits/{id}/ – Delete a habit
### 2.HabitCompletion Management
    .CRUD operation for HabitCompletion
        .Endpoints:
            .GET /api/completions/ – List all completion
            .POST /api/completions/ – Add a new completion
            .PUT /api/completions/{id}/ – Update completion details
            .DELETE /api/completions/{id}/ – Delete a completion
### 3.EnvironmentTrigger Management
    .CRUD operation for EnvironmentTrigger
        .Endpoints:
            .GET /api/triggers/ – List all triggers
            .POST /api/triggers/ – Add a new triggers
            .PUT /api/triggers/{id}/ – Update triggers details
            .DELETE /api/triggers/{id}/ – Delete a triggers

### 4.Security & Enhancements
    .JWT authentication for secure API access
    .Basic validation in serializers
## Setup Instructions

## 1. Clone the Repository
git clone https://github.com/aayushmapokhrel/Habit-Coach.git

## 2. Create a virtual environment
python -m venv venv source venv/bin/activate # macOS/Linux venv\Scripts\activate # Windows

## 3. Install dependencies
pip install -r requirements.txt

## 4. Configure Postgresql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}

## 5. Apply Migrations
python manage.py makemigrations
python manage.py migrate

## 6. Create Superuser (Optional)
python manage.py createsuperuser

## 7. Run the Development Server
python manage.py runserver

