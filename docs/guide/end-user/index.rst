.. _enduser_guide:
.. |Timeline| image:: https://cloud.githubusercontent.com/assets/1279644/9934893/921b543a-5d5c-11e5-9596-a5e067db79ed.png

End User Guide
==============

* Define your states.
* Define your state transitions.
* Define your proceeding meta which contains permissions and groups authorization for transitions. Proceeding order is also given here.

.. note::
   There must be only one initial state candidate for your workflow scenarios. Because ``django-river`` is gonna try to detect it and initialize your objects workflow path. If there are more than one initial state, ``django-river`` will raise ``RiverException(error_code=3)`` which is ``MULTIPLE_INITIAL_STATE`` error.

Whenever an object of your model class is inserted in your system, all its workflow initialization is done by ``django-river``.


Timeline
--------

|Timeline|

.. toctree::
    :maxdepth: 2