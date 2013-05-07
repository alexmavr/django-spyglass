===============
Getting Started
===============
Spyglass is a ready to use app that you can use to monitor new content across
several predefined websites.

After configuring spyglass, you may run several instances of crawlie_ that will
connect to your application's web server through a RESTful API provided by 
django-tastypie.

This tutorial assumes you have a basic understanding of Django.

Additionally, throughout this tutorial we will be referencing an example
configuration called News Spyglass. 
It monitors two news sites for news stories and can be found in the example
folder of spyglass' github repository.


Installation
============
first off, install the requirements. They can also be found in the pip-friendly
spyglass/requirements.txt:

* Python 2.7+
* Django 1.4.3
* django-tastypie 0.9.11+

Configuration
=============

1. Add ``spyglass`` to ``INSTALLED_APPS`` in your ``settings.py``.

2. Add ``METAMODEL='<path-to-your-model>'`` in ``settings.py`` for the metamodel. 
   In our example, it's ``METAMODEL=core.models.NewsStory``
   
   The metamodel is essentially a model in your application that will be
   populated when new results are found by the crawlers.

3. In your project's urls.py, add ``import spyglass.urls`` and 
    ``url(r'^', include(spyglass.urls))`` to add the spyglass urls 
    to the root level.
    
 Spyglass does not require root level urls, so you are free to add them
 wherever you want as long as you edit the crawler's serverconf appropriately.

 4. Add a Site


How many crawlers?
==================

.. _crawlie: http://github.com/mastergreg/spyglass-crawlie.git
