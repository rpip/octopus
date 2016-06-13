# -*- coding: utf-8 -*-
"""Main web app"""
import os
import uuid
import urllib2
import logging

import tornado.wsgi
from tornado.web import url

from wordcloud import WordCloud
import database
from sqlalchemy import desc
from database import WordCount

DB = database.init_db()


def fix_url(url):
    """Ensure's url is prefixed with 'http' or 'https'.

    Adds the prefix is it's missing
    """
    if url.startswith('http://') or url.startswith('https://'):
        return url
    else:
        return 'http://' + url


def save_wordcloud(wordcloud):
    """Insert new word count record or update count if it already exists"""
    for word, count in wordcloud:
        w_hash = database.generate_uuid(word)
        found_wc = DB.query(WordCount).get(w_hash)
        if found_wc:
            # update the count
            found_wc.count += count
            DB.commit()
        else:
            word_count = WordCount(uuid=w_hash, word=word, count=count)
            DB.add(word_count)
            DB.commit()


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        wordcloud = {}
        url = self.get_argument("url", None)
        error = None
        if url is not None:
            try:
                frequencies, wordcloud = WordCloud().generate(fix_url(url))
                # save the original word count
                save_wordcloud(frequencies)
            except (IOError, urllib2.URLError, ValueError):
                error = "Seems the URL is incorrect. Please try again"
            except Exception as _err:
                error = "Something went wrong..."
                # log the error
                logging.exception(error)

        self.render('home.html', url=url, wordcloud=wordcloud, error=error)


class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        word_cloud = DB.query(WordCount).order_by(desc('count')).all()
        self.render("admin.html", word_cloud=word_cloud)


settings = dict(
    title=u'Octopus Word Cloud',
    template_path=os.path.join(os.path.dirname(__file__), 'templates'),
    xsrf_cookies=True,
    keyfile=os.getenv('OCTOPUS_KEY'),
    cookie_secret=uuid.uuid4()
)

application = tornado.web.Application([
            url(r'/', HomeHandler, name='index'),
            url(r'/admin', AdminHandler, name='admin')
        ], **settings)


# init app
application = tornado.wsgi.WSGIAdapter(application)
