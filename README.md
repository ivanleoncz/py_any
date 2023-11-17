# PythonAnywhere (https://ivanleoncz.pythonanywhere.com)

![Action](https://github.com/ivanleoncz/python_anywhere/actions/workflows/tests.yml/badge.svg)

Website written in Django and its template engine for serving small projects, proudly hosted at [PythonAnywhere](https://www.pythonanywhere.com/).

[Library](https://ivanleoncz.pythonanywhere.com/apps/library/) is the only app available: other apps are under design.

### Python Anywhere Tips
1. Adding or changing static files, will always require collecting static files: `python3 manage.py collectstatic`.
2. Any change performed in terms of code, configuration or even static files, will always require the reload of the application on the Web Dashboard.