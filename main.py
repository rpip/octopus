import os
import uuid

# from bs4 import BeautifulSoup, Comment
import tornado.wsgi
from tornado.web import url

import database


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class HomeHandler(BaseHandler):
    def get(self):
        self.write('Hello')


class AdminHandler(BaseHandler):
    pass


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            url(r'/', HomeHandler, name='index'),
            url(r'/admin', AdminHandler, name='admin')
        ]

        settings = dict(
            title='Octopus Word Count',
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            xsrf_cookies=True,
            salt=os.getenv('OCTOPUS_SALT', '123456'),
            keyfile=os.getenv('OCTOPUS_KEY'),
            cookie_secret=uuid.uuid4()
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        # self.db = database.init_db()


# init app
application = tornado.wsgi.WSGIAdapter(Application())
