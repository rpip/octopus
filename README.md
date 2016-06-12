[![Build Status](https://travis-ci.org/rpip/octopus.svg?branch=master)](https://travis-ci.org/rpip/octopus)

Octopus
==========

Word cloud generator that runs on Goofle App Engine using MySQLdb and Tornado.

Installation
------------

First install the Google AppEngine toolkit.

.. code-block:: bash

    $ git clone https://github.com/rpip/octopus
    $ cd octopus
    $ # install deps
    $ pip install -t lib -r requirements.txt
    $ dev_appserver.py .

Usage
-----

The `WordCloud` class in `wordcloud.py` does the heavy lifting, and can be used indepently of the web app.

.. code-block:: python

    from wordcloud import WordCloud
    frequencies, word_cloud = WordCloud().generate('http://fsf.org')




Note
------
- Follow the [Twelve-Factor App](http://12factor.net/config), methodology and use environment variables for the configs
- Include digits in the word count?


TODO
------
- [x] Deploy app
- [] Handle redirects
- [] Encrypt/decrypt word saved in the DB
- [] Write unit tests for wordcloud.WordCloud
- [] Setup TravisCI
