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
   Once project is configured to work with ``django-river``, calling ``syncdb`` or ``migrate`` management command would create all its model instances.