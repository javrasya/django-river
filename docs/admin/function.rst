.. _transition-meta-administration:

Function Administration
=======================

With dynamically created hookins, functions are kept in DB and they can be managed on an admin interface that django-river already offers out of the box.
You define them once and you can use them within multiple hooks. Just go to ``/admin/river/function/`` admin page and create your functions there.
The admin page also comes with code highlighting if you enable the ``codemirror2`` in the settings. Don't forget to collect statics for production deployments.


   .. code:: python

       INSTALLED_APPS=[
           ...
           codemirror2
           river
           ...
       ]

+-------+---------+----------+----------------------------+-------------+------------------------------+
| Field | Default | Optional |           Format           | Description |                              |
+=======+=========+==========+============================+=============+==============================+
| name  |         | False    | String ([\w\s]+)           |             | Name of the function.        |
+-------+---------+----------+----------------------------+-------------+------------------------------+
| body  |         | False    | Valid Python function that |             | Function body as string.     |
|       |         |          | is named as ``handle``     |             | see :ref:`Example Function`  |
+-------+---------+----------+----------------------------+-------------+------------------------------+

.. toctree::
    :maxdepth: 2