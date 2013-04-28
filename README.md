===============
django-spyglass
===============

Monitor real-time content through distributed web crawling.
Currently at pre-alpha development.

Features
===============

Basic Usage
--------------

* Specify a model of yours to be populated
* Add a collection of sites to be crawled
* For each site, specify an XPath for every field of the model
* Run any number of crawlers and watch your model populate with new content

Extra Goodies
--------------
* Search terms on each individual query which are satisfied with fuzzy string matching
* Notification hook for custom actions on new content availability

Requirements
===============

Installation
------------
* Python 2.7+
* Django 1.4.3+ (1.5.1 not tested)
* django-tastypie 0.9.11+

Deployment
------------
* spyglass-crawlie (http://github.com/mastergreg/spyglass-crawlie)

Installation and Usage
==============
