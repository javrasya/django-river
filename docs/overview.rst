
Overview
========
Main goal of developing this framework is **to be able to edit any workflow item on the fly.** This means, all elements in workflow like states, transitions, user authorizations(permission), group authorization are editable. To do this, all data about the workflow item is persisted into DB. **Hence, they can be changed without touching the code and re-deploying your application.**

There is ordering aprovments for a transition functionality in ``django-river``. It also provides skipping specific transition of a specific objects.

Requirements
------------
* Python (``2.7``, ``3.2``, ``3.3``, ``3.4``)
* Pypy (``2``, ``3``)
* Django (``1.7``, ``1.8``)