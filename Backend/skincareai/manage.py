#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
<<<<<<<< HEAD:Backend/skin_care_project/manage.py
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skin_care_project.settings')
========
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skincareai.settings')
>>>>>>>> 475dfdc22fca0bd96a514992bfe73800f011ee35:Backend/skincareai/manage.py
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
