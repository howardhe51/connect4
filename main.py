import webapp2
import os
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

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

    #def post(self):


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
