__author__ = 'ahmetdal'


#!/usr/bin/env python
import os  
import sys

if __name__ == "__main__":  
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.with_sqlite3")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)