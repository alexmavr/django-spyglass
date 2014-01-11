===============
django-spyglass
===============

Spyglass is a django application that provides real-time content monitoring of remote websites
through distributed web crawling.

Spyglass is configured by specifying a django Model to be populated, a series of websites to be crawled,
and an XPath for every combination of model fields and websites.

When a query is submitted to spyglass, a polling task is assigned to the crawler network for completion. 
The crawlers regularly poll the desired websites until a match is found. 
Then, a new model instance is created and the user is notified.

Spyglass is licenced under the BSD license.

Features
========

Basic Features
-----------
* A polling interval can be specified for each website to prevent continuous polling.
* User-specified search terms are satisfied with fuzzy string matching.
* Queries can be one-time only, or persistent (notifying the user on future changes).
* Notifications are performed with a generic hook which defaults to email notification.


Configuration in a nutshell
---------------------------
* Specify a django model to be populated
* Add a collection of sites to be crawled
* For each site, specify an XPath for every field of the model
* Deploy the application and run any number of crawlers


Requirements
============

Installation
------------
* Python 2.7+
* Django 1.4.3+ (1.5.1 not tested)
* django-tastypie 0.9.11+

Deployment
----------
* spyglass-crawlie_ is the default crawler that can be used with spyglass

Configuration
==============

For detailed instructions, please view the documentation_

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

6. Set up as the required amount of spyglass-crawlie_ instances by editing their serverconf and userconf files to target the spyglass server

Extras
======

Class diagram: https://raw2.github.com/afein/SoftEng/master/SDD/files/spyglass.png
Crawler state diagram: https://github.com/afein/SoftEng/blob/master/SDD/files/state.jpg

.. _documentation: http://spyglass.readthedocs.org/ 
.. _spyglass-crawlie: http://github.com/mastergreg/spyglass-crawlie.git
.. role:: python(code)
   :language: python
