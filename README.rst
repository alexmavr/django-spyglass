===============
django-spyglass
===============

Monitor real-time content through distributed web crawling.

Currently at pre-alpha development.

For detailed instructions, view the documentation_

Features
========

Basic Usage
-----------

* Specify a model to be populated
* Add a collection of sites to be crawled
* For each site, specify an XPath for every field of the model
* Start the server and any number of crawlers and watch the model populate with new content!

Extra Goodies
-------------

* Search terms on each individual query which are satisfied with fuzzy string matching
* Notification hook for custom actions on new content availability

Requirements
============

Installation
------------
* Python 2.7+
* Django 1.4.3+ (1.5.1 not tested)
* django-tastypie 0.9.11+

Deployment
----------
* spyglass-crawlie_

Installation 
==============
1. Add ``spyglass`` to ``INSTALLED_APPS`` in your ``settings.py``.
   
2. Add ``METAMODEL='<path-to-your-model>'`` in ``settings.py`` for the model to be populated.

   For example, ``METAMODEL='core.models.NewsStory'`` 

3. Add 
   .. code-block:: python
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
