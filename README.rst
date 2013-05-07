===============
django-spyglass
===============

Spyglass is a django application that provides real-time content monitoring
through distributed web crawling.

After configuring a model, some sites to be crawled and an XPath for each field
of the model on every site, you are ready to run as many crawlers as you want.

When a user submits a query, spyglass will instruct some connected crawlers to
poll the related sites regularly and check for new content. When found, a new
model instance will be created, the query will be satisfied and the user will
be notified.

It's currently at pre-alpha development and licenced under the BSD license.

Features
========

Basic Usage
-----------

* Specify a model to be populated
* Add a collection of sites to be crawled
* For each site, specify an XPath for every field of the model
* Start the server and any number of crawlers and watch the model populate with
  new content from those XPaths

Extra Goodies
-------------

* Individual queries have search terms which are satisfied with fuzzy string
  matching and can be persistent or one-time only.
* There is a notification hook that is triggered on new content availability
  and allows for custom notification methods

Requirements
============

Installation
------------
* Python 2.7+
* Django 1.4.3+ (1.5.1 not tested)
* django-tastypie 0.9.11+

Deployment
----------
* spyglass-crawlie_ is the default crawler to be used with spyglass

Configuration
==============

For detailed instructions, view the documentation_

1. Add ``spyglass`` to ``INSTALLED_APPS`` in your ``settings.py``.
   
2. Add ``METAMODEL='<path-to-your-model>'`` in ``settings.py`` for the model to be populated.

   For example, ``METAMODEL='core.models.NewsStory'`` 

3. Add 
   :: 
      import spyglass.urls 

      url(r'^', include(spyglass.urls)) 
   to your urls.py
4. Add some sites on spyglass's Site model through fixtures or direct access

5. For each Site entry, create a DataField entry for each field of the metamodel with an XPath where the crawlers can find the data to populate the field. 
   This is explained in detail at the documentation_

6. Set up as many instances of spyglass-crawlie_ as you need and edit their serverconf and userconf files to target your server


.. _documentation: http://spyglass.readthedocs.org/ 
.. _spyglass-crawlie: http://github.com/mastergreg/spyglass-crawlie.git
.. role:: python(code)
   :language: python
