.. _admin-guide:

Administration
==============

Since ``django-river`` keeps all the data needed in a database, those should be pre-created before your first model 
object is created. Otherwise **your app will crash first time you create a model object.** Here are all needed models
that you need to provide. ``django-river`` will register an Administration for those model for you. All you need to do 
is to provide them by using their Django admin pages.

.. toctree::
    :maxdepth: 2

    state
    transition_meta
    transition_approval_meta
    