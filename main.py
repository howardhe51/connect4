import webapp2
import os
import jinja2
import json
import logging

from google.appengine.api import users
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Profile(ndb.Model):
    name = ndb.StringProperty()
    #Bmonth = ndb.IntegerProperty()
    #Bday = ndb.IntegerProperty()
    #Byear = ndb.IntegerProperty()
    email = ndb.StringProperty()
    username = ndb.StringProperty()
    win = ndb.IntegerProperty()
    lose = ndb.IntegerProperty()

class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    iden = ndb.IntegerProperty()
    user_key = ndb.KeyProperty(kind = Profile)

class Game(ndb.Model):
    board = ndb.JsonProperty()
    player = ndb.IntegerProperty()
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

class SelectionHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/game.html')
        self.response.write(template.render())

    def post(self):
        gamemode = self.request.get('dropbox')
        board = [ [0,0,0,0,0,0],
                  [0,0,0,0,0,0],
                  [0,0,0,0,0,0],
                  [0,0,0,0,0,0],
                  [0,0,0,0,0,0],
                  [0,0,0,0,0,0],
                  [0,0,0,0,0,0]]
        player = 1

        new_game = Game(board = json.dumps(board), player = player)
        new_game.put()
        self.redirect('/select')

class ProfileHandler(webapp2.RequestHandler):
    def get(self):

        template = jinja_environment.get_template('templates/profile.html')
        self.response.write(template.render())

    def post(self):
        self.redirect('/profile')


class NewGameHandler(webapp2.RequestHandler):
    def get(self):
        board = [ [0,0,0,0,0,0],
                  [0,0,0,0,0,0],
                  [0,0,0,0,0,0],
                  [0,0,0,0,0,0],
                  [0,0,0,0,0,0],
                  [0,0,0,0,0,0],
                  [0,0,0,0,0,0]]
        new_game = Game(board = board, player =1)
        # 1. Create a new game when users go to /newgame
        # 2. Add handler (like /game/:id) to get an existing game, based on the Game id
        # 3. When the user clicks on a column (JS), run the /columnHandler to update the game
        # 4. The Game should keep track of whose turn it is (Python), and auto-refresh the UI if it's no that person's turn (JS)



class ColumnHandler(webapp2.RequestHandler):
    '''def get(self):
            games = Game.query().fetch()
            template_vars = {
                'games': games,
            }

            template = jinja_environment.get_template('templates/game.html')
            self.response.write(template.render(template_vars))'''
    def post(self):
          col = int(self.request.get('column'))
          logging.info(col)
          game = Game.query().get()
          logging.info("board is %s", game.board)
          board = json.loads(game.board)

        # === 2: Interact with the database. ===

        # Use the URLsafe key to get the photo from the DB.
          if(board[col][5] == 0 and game.player == 1):
                board[col][5] = game.player;
                game.player = 2;

          elif(board[col][5] == 0 and game.player == 2):
            board[col][5] = game.player;
            game.player = 1;
          elif(board[col][4] == 0 and game.player == 1):
            board[col][4] = game.player;
            game.player = 2;
          elif(board[col][4] == 0 and game.player == 2):
            board[col][4] = game.player;
            game.player = 1;
          elif(board[col][3] == 0 and game.player == 1):
            board[col][3] = game.player;
            game.player = 2;
          elif(board[col][3] == 0 and game.player == 2):
            board[col][3] = game.player;
            game.player = 1;
          elif(board[col][2] == 0 and game.player == 1):
            board[col][2] = game.player;
            game.player = 2;
          elif(board[col][2] == 0 and game.player == 2):
            board[col][2] = game.player;
            game.player = 1;
          elif(board[col][1] == 0 and game.player == 1):
            board[col][1] = game.player;
            game.player = 2;
          elif(board[col][1] == 0 and game.player == 2):
            board[col][1] = game.player;
            game.player = 1;
          elif(board[col][0] == 0 and game.player == 1):
            board[col][0] = game.player;
            game.player = 2;
          elif(board[col][0] == 0 and game.player == 2):
            board[col][0] = game.player;
            game.player = 1;
          logging.info(board)
          logging.info(game.player)
          game.board = json.dumps(board)
          game.put()
          template = jinja_environment.get_template('templates/game.html')
          self.response.write(game.board)




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/select', SelectionHandler),
    ('/column', ColumnHandler),
#('/profile', ProfileHandler),
    ], debug=True)
#helloworld
