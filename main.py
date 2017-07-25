import webapp2
import os
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class User(ndb.Model):
    name = ndb.StringProperty()
    """
    Bmonth = ndb.IntegerProperty()
    Bday = ndb.IntegerProperty()
    Byear = ndb.IntegerProperty()
    """
    email = ndb.StringProperty()
    username = ndb.StringProperty()
    win = ndb.IntegerProperty()
    lose = ndb.IntegerProperty()


class MainHandler(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        login_url = users.create_login_url('/')
        template_vars = {
            'current_user': current_user,
            'logout_url': logout_url,
            'login_url': login_url,
        }
        template = jinja_environment.get_template('templates/main.html')
        self.response.write(template.render(template_vars))


class SelectionHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/select.html')
        self.response.write(template.render())


































#class MoveHandler(webapp2.RequestHandler):
#    def get(self):








app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/select', SelectionHandler),

], debug=True)
