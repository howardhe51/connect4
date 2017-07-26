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
    image = ndb.StringProperty()


class Game(ndb.Model):
    board = ndb.JsonProperty()
    player = ndb.IntegerProperty()
    winner = ndb.IntegerProperty()
    # Might want to have a `winner` UserProperty
    # Keep track of user1 and user2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        login_url = users.create_login_url('/')
        logout_url = users.create_logout_url('/')
        template_vars = {
            'current_user': current_user,
            'logout_url': logout_url,
            'login_url': login_url,
        }
        template = jinja_environment.get_template('templates/main.html')
        self.response.write(template.render(template_vars))

class GameHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/game.html')
        self.response.write(template.render())

    def post(self):
        gamemode = self.request.get('dropbox')
        board = [ [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0]]
        player = 1
        winner = 0

        new_game = Game(board = json.dumps(board), player = player, winner = winner)
        new_game.put()
        self.redirect('/game')

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        # Get the current user's email
        current_user = users.get_current_user()
        # Only query for User models that have the email of the current user
        user_query = User.query().filter(User.email == current_user.email()).get()
        #user = user_query.get()
        template_vars = {
            "user": user_query
        }
        print "user is", user_query
        template = jinja_environment.get_template('templates/profile.html')
        self.response.write(template.render(template_vars))

    def post(self):
        image = self.request.get('filename')
        # image is a "unicode" type, but we want it to be a string
        image = str(image)
        current_user = users.get_current_user()
        user_email = current_user.email()
        user = User(email=user_email, image = image)
        user.put()
        self.redirect('/profile')

def checkWin(board):
    for row in range(0,6):
        for col in range(0,7):
            if(col<=3):
                winner = checkEast(board,row,col)
                if(winner!=0):
                    return winner
                    if(row<=2):
                        winner = checkSouthEast(board,row,col)
                        if(winner!=0):
                            return winner
            if(row<=2):
                winner = checkSouth(board,row,col)
                if(winner!=0):
                    return winner
                    if(col>=3):
                        checkSouthWest(board,row,col)
    return 0
def checkEast(board, row, col):
    if(board[row][col] == 0):
        return 0;
    count = 0
    for i in range(1,4):
        if(board[row][col]==board[row][col+i]):
            count = count + 1
            if(count==3):
                return board[row][col]
def checkSouthEast(board, row, col):
    if(board[row][col] == 0):
        return 0;
    count = 0
    for i in range(1,4):
        if(board[row][col]==board[row+i][col+i]):
            count = count + 1
            if(count==3):
                return board[row][col]
def checkSouth(board, row, col):
    if(board[row][col] == 0):
        return 0;
    count = 0
    for i in range(1,4):
        if(board[row][col]==board[row+i][col]):
            count = count + 1
            if(count==3):
                return board[row][col]
def checkSouthWest(board, row, col):
    if(board[row][col] == 0):
        return 0;
    count = 0
    for i in range(1,4):
        if(board[row][col]==board[row+i][col-i]):
            count = count + 1
            if(count==3):
                return board[row][col]

class ColumnHandler(webapp2.RequestHandler):

    def post(self):
        col = int(self.request.get('column'))
        game = Game.query().get()
        logging.info("board is %s", game.board)
        board = json.loads(game.board)

        # === 2: Interact with the database. ===

        # Use the URLsafe key to get the photo from the DB.
        if(board[5][col] == 0 and game.player == 1):
            board[5][col] = game.player;
            game.player = 2;

        elif(board[5][col] == 0 and game.player == 2):
            board[5][col] = game.player;
            game.player = 1;
        elif(board[4][col] == 0 and game.player == 1):
            board[4][col] = game.player;
            game.player = 2;
        elif(board[4][col] == 0 and game.player == 2):
            board[4][col] = game.player;
            game.player = 1;
        elif(board[3][col] == 0 and game.player == 1):
            board[3][col] = game.player;
            game.player = 2;
        elif(board[3][col] == 0 and game.player == 2):
            board[3][col] = game.player;
            game.player = 1;
        elif(board[3][col] == 0 and game.player == 1):
            board[3][col] = game.player;
            game.player = 2;
        elif(board[2][col] == 0 and game.player == 2):
            board[2][col] = game.player;
            game.player = 1;
        elif(board[2][col] == 0 and game.player == 1):
            board[2][col] = game.player;
            game.player = 2;
        elif(board[1][col] == 0 and game.player == 2):
            board[1][col] = game.player;
            game.player = 1;
        elif(board[0][col] == 0 and game.player == 1):
            board[0][col] = game.player;
            game.player = 2;
        elif(board[0][col] == 0 and game.player == 2):
            board[0][col] = game.player;
            game.player = 1;
        if(checkWin(board)==1):
            game.winner = 1
        if(checkWin(board)==2):
            game.winner = 2
        logging.info(game.winner)
        logging.info(board)
        game.board = json.dumps(board)
        game.put()
        template = jinja_environment.get_template('templates/game.html')
        self.response.write(game.board)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/game', GameHandler),
    ('/column', ColumnHandler),
    ('/profile', ProfileHandler),
    ], debug=True)
#helloworld
