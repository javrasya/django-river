.. _migration_31_to_32:

3.1.X to 3.2.X
==============

``django-river`` started to support **Microsoft SQL Server 17 and 19** after version 3.2.0 but the previous migrations didn't get along with it. We needed to reset all
the migrations to have fresh start. If you have already migrated to version `3.1.X` all you need to do is to pull your migrations back to the beginning.


   .. code:: bash

       python manage.py migrate --fake river zero
       python manage.py migrate --fake river
