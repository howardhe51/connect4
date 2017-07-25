import webapp2
import os
import jinja2
import json

from google.appengine.api import users
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class User(ndb.Model):
    name = ndb.StringProperty()
    Bmonth = ndb.IntegerProperty()
    Bday = ndb.IntegerProperty()
    Byear = ndb.IntegerProperty()
    email = ndb.StringProperty()
    username = ndb.StringProperty()
    win = ndb.IntegerProperty()
    lose = ndb.IntegerProperty()
class Game(ndb.Model):
    board = ndb.JsonProperty()
    # Might want to have a `winner` UserProperty
    # Keep track of user1 and user2


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

# This handler will take in the column that the user selected
class SelectionHandler(webapp2.RequestHandler):
    def get(self):









class NewGameHandler(webapp2.RequestHandler):
    def get(self):
        board = [ [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0]]
        board1 = json.dumps(board)
        new_game = Game(board = board1)
        # 1. Create a new game when users go to /newgame
        # 2. Add handler (like /game/:id) to get an existing game, based on the Game id
        # 3. When the user clicks on a column (JS), run the /selectionHandler to update the game
        # 4. The Game should keep track of whose turn it is (Python), and auto-refresh the UI if it's no that person's turn (JS)


























class MoveHandler(webapp2.RequestHandler):
    def get(self):
    def post(self):









app = webapp2.WSGIApplication([
    ('/', MainHandler),

], debug=True)
