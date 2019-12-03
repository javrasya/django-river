.. django-river documentation master file, created by
   sphinx-quickstart on Sun Aug 30 00:15:25 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. |Build Status| image:: https://travis-ci.org/javrasya/django-river.svg
   :target: https://travis-ci.org/javrasya/django-river
.. |Coverage Status| image:: https://coveralls.io/repos/javrasya/django-river/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/javrasya/django-river?branch=master
.. |Health Status| image:: https://landscape.io/github/javrasya/django-river/master/landscape.svg?style=flat
   :target: https://landscape.io/github/javrasya/django-river/master
   :alt: Code Health
.. |Documentation Status| image:: https://readthedocs.org/projects/django-river/badge/?version=latest
   :target: https://readthedocs.org/projects/django-river/?badge=latest
.. |Quality Status| image:: https://api.codacy.com/project/badge/Grade/c3c73d157fe045e6b966d8d4416b6b17
   :alt: Codacy Badge
   :target: https://app.codacy.com/app/javrasya/django-river?utm_source=github.com&utm_medium=referral&utm_content=javrasya/django-river&utm_campaign=Badge_Grade_Dashboard
.. |Downloads| image:: https://img.shields.io/pypi/dm/django-river
    :alt: PyPI - Downloads   
.. |Logo| raw:: html
    :scale: 50%

   <div style="width:100%;text-align: center;"><svg style="width:200px" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0.0 0.0 189.65879265091863 181.498687664042" fill="none" stroke="none" stroke-linecap="square" stroke-miterlimit="10"><clipPath id="p.0"><path d="m0 0l189.6588 0l0 181.49869l-189.6588 0l0 -181.49869z" clip-rule="nonzero"/></clipPath><g clip-path="url(#p.0)"><path fill="#000000" fill-opacity="0.0" d="m0 0l189.6588 0l0 181.49869l-189.6588 0z" fill-rule="evenodd"/><path fill="#00ffff" d="m70.50117 92.47626l0 0c0 -13.766693 11.677338 -24.926804 26.082054 -24.926804l0 0c6.9173965 0 13.551468 2.626213 18.442802 7.3008957c4.8913345 4.6746826 7.6392517 11.014908 7.6392517 17.625908l0 0c0 13.766693 -11.67733 24.926804 -26.082054 24.926804l0 0c-14.4047165 0 -26.082054 -11.16011 -26.082054 -24.926804zm12.463402 0c0 6.8833466 6.0972824 12.463402 13.618652 12.463402c7.5213776 0 13.618652 -5.580055 13.618652 -12.463402c0 -6.8833466 -6.097275 -12.463402 -13.618652 -12.463402l0 0c-7.52137 0 -13.618652 5.580055 -13.618652 12.463402z" fill-rule="evenodd"/><path fill="#21cdd9" d="m141.79909 92.47626l0 0c0 -11.376289 9.561203 -20.598595 21.35553 -20.598595l0 0c5.6638336 0 11.095703 2.1702042 15.100647 6.033188c4.0049286 3.8629837 6.254883 9.102318 6.254883 14.565407l0 0c0 11.376289 -9.561188 20.598595 -21.35553 20.598595l0 0c-11.794327 0 -21.35553 -9.222305 -21.35553 -20.598595zm10.299301 0c0 5.6881485 4.9500427 10.299301 11.056229 10.299301c6.106186 0 11.056229 -4.6111526 11.056229 -10.299301c0 -5.6881485 -4.9500427 -10.299301 -11.056229 -10.299301l0 0c-6.106186 0 -11.056229 4.6111526 -11.056229 10.299301z" fill-rule="evenodd"/><path fill="#21cdd9" d="m128.6083 86.83943l17.232132 0l0 13.594223l-17.232132 0z" fill-rule="evenodd"/><path fill="#21cdd9" d="m51.367355 92.47626l0 0c0 11.376289 -9.561195 20.598595 -21.355526 20.598595l0 0c-5.6638374 0 -11.095701 -2.1702042 -15.100638 -6.033188c-4.004938 -3.8629837 -6.2548895 -9.102318 -6.2548895 -14.565407l0 0c0 -11.376289 9.561195 -20.598595 21.355528 -20.598595l0 0c11.794331 0 21.355526 9.222305 21.355526 20.598595zm-10.299297 0c0 -5.6881485 -4.9500427 -10.299301 -11.056229 -10.299301c-6.106188 0 -11.056229 4.6111526 -11.056229 10.299301c0 5.6881485 4.950041 10.299301 11.056229 10.299301l0 0c6.106186 0 11.056229 -4.6111526 11.056229 -10.299301z" fill-rule="evenodd"/><path fill="#21cdd9" d="m64.558136 98.11308l-17.232124 0l0 -13.594223l17.232124 0z" fill-rule="evenodd"/><path fill="#21cdd9" d="m96.58322 49.162712l0 0c-11.4850235 0 -20.795479 -9.470673 -20.795479 -21.153337l0 0c0 -5.610214 2.1909485 -10.990648 6.090851 -14.957669c3.89991 -3.96702 9.189323 -6.195669 14.704628 -6.195669l0 0c11.485031 0 20.795486 9.470672 20.795486 21.15334l0 0c0 11.682665 -9.310455 21.153337 -20.795486 21.153337zm0 -10.397739c5.7425156 0 10.397743 -4.815445 10.397743 -10.755598c0 -5.940151 -4.6552277 -10.755596 -10.397743 -10.755596c-5.742508 0 -10.397736 4.815445 -10.397736 10.755596l0 0c0 5.940153 4.6552277 10.755598 10.397736 10.755598z" fill-rule="evenodd"/><path fill="#21cdd9" d="m90.89252 62.228607l0 -17.068974l13.724159 0l0 17.068974z" fill-rule="evenodd"/><path fill="#21cdd9" d="m96.58322 135.7898l0 0c-11.4850235 0 -20.795479 9.470673 -20.795479 21.15335l0 0c0 5.610214 2.1909485 10.990646 6.090851 14.957657c3.89991 3.9670258 9.189323 6.1956787 14.704628 6.1956787l0 0c11.485031 0 20.795486 -9.470673 20.795486 -21.153336l0 0c0 -11.682678 -9.310455 -21.15335 -20.795486 -21.15335zm0 10.397751c5.7425156 0 10.397743 4.815445 10.397743 10.7556c0 5.94014 -4.6552277 10.755585 -10.397743 10.755585c-5.742508 0 -10.397736 -4.815445 -10.397736 -10.755585l0 0c0 -5.940155 4.6552277 -10.7556 10.397736 -10.7556z" fill-rule="evenodd"/><path fill="#21cdd9" d="m90.89252 122.72391l0 17.06897l13.724159 0l0 -17.06897z" fill-rule="evenodd"/><path fill="#21cdd9" d="m148.00731 140.94235l0 0c8.120071 -8.043198 21.464417 -7.865799 29.80542 0.39624023l0 0c4.005493 3.967575 6.2979126 9.307007 6.372925 14.843674c0.075027466 5.536682 -2.0734863 10.817078 -5.972885 14.679565l0 0c-8.120071 8.043182 -21.464417 7.8657837 -29.80542 -0.3962555l0 0c-8.341019 -8.262024 -8.520111 -21.480026 -0.40003967 -29.523224zm7.351349 7.2817383c-4.0600433 4.0216064 -3.8809357 10.719299 0.40003967 14.959747c4.28096 4.2404327 11.042679 4.4178314 15.102722 0.39624023l0 0c4.060028 -4.021591 3.8809357 -10.719299 -0.40003967 -14.959732l0 0c-4.28096 -4.240448 -11.042679 -4.4178467 -15.102722 -0.3962555z" fill-rule="evenodd"/><path fill="#21cdd9" d="m127.60528 112.76604l27.288307 27.029953l-9.699234 9.607391l-27.288292 -27.029945z" fill-rule="evenodd"/><path fill="#21cdd9" d="m44.890266 140.94235l0 0c-8.120075 -8.043198 -21.464418 -7.865799 -29.805424 0.39624023l0 0c-4.005492 3.967575 -6.2979 9.307007 -6.372921 14.843674c-0.07501984 5.536682 2.073492 10.817078 5.97289 14.679565l0 0c8.120075 8.043182 21.464417 7.8657837 29.805424 -0.3962555l0 0c8.341007 -8.262024 8.520107 -21.480026 0.40003204 -29.523224zm-7.351349 7.2817383c4.0600357 4.0216064 3.8809357 10.719299 -0.40003204 14.959747c-4.2809677 4.2404327 -11.04269 4.4178314 -15.102726 0.39624023l0 0c-4.0600376 -4.021591 -3.8809376 -10.719299 0.40003014 -14.959732l0 0c4.2809696 -4.240448 11.042692 -4.4178467 15.102728 -0.3962555z" fill-rule="evenodd"/><path fill="#21cdd9" d="m65.2923 112.76604l-27.288303 27.029953l9.699223 9.607391l27.288307 -27.029945z" fill-rule="evenodd"/><path fill="#21cdd9" d="m148.00731 44.473957l0 0c8.120071 8.043198 21.464417 7.8657913 29.80542 -0.39624405l0 0c4.005493 -3.9675674 6.2979126 -9.306999 6.372925 -14.843679c0.075027466 -5.53668 -2.0734863 -10.817074 -5.972885 -14.679552l0 0c-8.120071 -8.043196 -21.464417 -7.865792 -29.80542 0.39624405l0 0c-8.341019 8.262035 -8.520111 21.480038 -0.40003967 29.523232zm7.351349 -7.281746c-4.0600433 -4.021599 -3.8809357 -10.719301 0.40003967 -14.959738c4.28096 -4.2404385 11.042679 -4.417843 15.102722 -0.39624405l0 0c4.060028 4.021597 3.8809357 10.719301 -0.40003967 14.959738l0 0c-4.28096 4.2404366 -11.042679 4.417843 -15.102722 0.39624405z" fill-rule="evenodd"/><path fill="#21cdd9" d="m127.60528 72.65027l27.288307 -27.029945l-9.699234 -9.607395l-27.288292 27.029942z" fill-rule="evenodd"/><path fill="#21cdd9" d="m44.893845 44.470413l0 0c8.120075 -8.043198 7.940975 -21.2612 -0.40002823 -29.523235l0 0c-4.005493 -3.9675694 -9.395962 -6.2382736 -14.985563 -6.312584c-5.5895996 -0.0743103 -10.920464 2.0538607 -14.819862 5.91634l0 0c-8.120074 8.043195 -7.940974 21.2612 0.40003204 29.523235l0 0c8.341005 8.262035 21.68535 8.439438 29.805422 0.39624405zm-7.351345 -7.2817497c-4.0600395 4.021599 -10.82176 3.8441963 -15.102728 -0.39624405c-4.2809696 -4.2404366 -4.4600697 -10.938139 -0.40003204 -14.959738l0 0c4.0600376 -4.021597 10.82176 -3.8441925 15.102728 0.39624405l0 0c4.2809677 4.2404385 4.4600677 10.938139 0.40003204 14.959738z" fill-rule="evenodd"/><path fill="#21cdd9" d="m73.33947 64.67928l-27.288303 -27.029945l-9.699223 9.607395l27.2883 27.029942z" fill-rule="evenodd"/></g></svg></div>

Django River
============

|Logo|

|Build Status| |Coverage Status| |Documentation Status| |Quality Status| |Downloads|

River is an open source and always free workflow framework for ``Django`` which support on
the fly changes instead of hardcoding states, transitions and authorization rules.

The main goal of developing this framework is **to be able to edit any
workflow item on the fly.** This means that all the elements in a workflow like
states, transitions or authorizations rules are editable at any time so that no changes requires a re-deploying of your application anymore.

Donations
=========

This is a fully open source project and it can be better with your donations.

If you are using ``django-river`` to create a commercial product,
please consider becoming our `sponsor`_  , `patron`_ or donate over `PayPal`_

.. _`patron`: https://www.patreon.com/javrasya
.. _`PayPal`: https://paypal.me/ceahmetdal
.. _`sponsor`: https://github.com/sponsors/javrasya

Advance Admin
-------------

A very modern admin with some user friendly interfaces that is called `River Admin`_ has been published.

.. _`River Admin`: https://github.com/javrasya/river-admin

Getting Started
===============

You can easily get started with ``django-river`` by following :ref:`getting-started`.
    
Contents
========

.. toctree::
   :maxdepth: 2

   getting_started
   overview
   admin/index
   api/index
   authorization
   hooking/index
   faq
   migration/index
   changelog



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

