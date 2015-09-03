.. _configuration:

Configuration
=============

After :ref:`installation <installation>` we can configure our project for it. In a settings module we need to add ``river`` to
``settings.py``::

   INSTALLED_APPS = (
       # ...
       'river',
   )

.. note::
   Once project is configured to work with ``django-river``, do not forget to make your migrations for your model have ``StateField``. Sometimes changes in ``django-river`` models happen. New versions of it migt require migrating.