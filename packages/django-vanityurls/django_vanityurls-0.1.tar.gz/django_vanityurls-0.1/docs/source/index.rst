Welcome to django-vanityurls's documentation!
==============================================

**Django VanityURLs** is a Django app, allowing the user to create vanity URLs for their site via the Django admin.

.. note::

   This project is under active development, as is the documentation. Keep an eye on the `django-vanityurls GitHub pages <https://github.com/simonharris/django-vanityurls>`_ for source code and updates.

============
Installation
============

Download
~~~~~~~~

The preferred way to get hold of ``django-vanityurls`` is via ``pip``::

    $ pip install django-vanityurls

This may be a good time to add ``django-vanityurls`` to your project's ``requirements.txt``.

The ``django-vanityurls`` source code is also available via `the project's GitHub repository <https://github.com/simonharris/django-vanityurls>`_.

Initial Configuration
~~~~~~~~~~~~~~~~~~~~~

There are two changes to make to your project's ``settings.py``:

1) add the app and its dependencies to ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        ...
        'vanityurls',
        ...
    ]


2) enable the ``django-vanityurls`` middleware by adding the following entry to ``MIDDLEWARE``::

    MIDDLEWARE = [
        ...
        'vanityurls.middleware.VanityUrlsMiddleware',
        ...
    ]


Database Migrations
^^^^^^^^^^^^^^^^^^^

Apply the database migrations to create the table needed by ``django-vanityurls``:


.. code-block:: console

    $ python manage.py migrate vanityurls


You should now be good to go, and should have a VANITYURLS section in Django admin.
