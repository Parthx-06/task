# Django Quiz Application - Models

This directory contains the Django database models for an online course assessment platform.

## Models Defined in `models.py`

1. **Question**: Represents assessment questions linked to a lesson, containing question text, grade weighting, and score validation helper (`is_get_score`).
2. **Choice**: Represents answer choices associated with a specific question, including correctness indicators (`is_correct`).
3. **Submission**: Records learner choices submitted for grading.

## Quick Start
Add the app to your `INSTALLED_APPS` in Django `settings.py` and run:
```bash
python manage.py makemigrations
python manage.py migrate
```
