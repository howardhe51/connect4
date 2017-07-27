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
    user_key = ndb.StringProperty()

class Game(ndb.Model):
    # TODO: Game will also need a key
    board = ndb.JsonProperty()
    player1 = ndb.StringProperty()
    player2 = ndb.StringProperty()
    current_player = ndb.StringProperty()
    winner = ndb.StringProperty()
    # Might want to have a `winner` UserProperty
    # Keep track of user1 and user2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        if (current_user == None):
            current_user_id = 'none'
        else:
            current_user_id = current_user.user_id()
        userID = current_user_id
        user = User(user_key = userID)
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
        game = Game.query().get()
        current_user = users.get_current_user()
        if(game== None):
            game = Game(board = json.dumps(board),current_player = current_user.user_id(),player1 = current_user.user_id())
        elif(game.player2==None):
            game.player2 = current_user.user_id()
        game.put()
        self.redirect('/game')

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        # Get the current user's email
        current_user = users.get_current_user()
        # Only query for User models that have the email of the current user
        user = User.query().filter(User.email == current_user.email()).get()
        #user = user_query.get()
        template_vars = {
            "user": user,
        }
        print "user is", user
        template = jinja_environment.get_template('templates/profile.html')
        self.response.write(template.render(template_vars))

    def post(self):
        image = self.request.get('img_link')
        # image is a "unicode" type, but we want it to be a string
        #image = str(image)
        current_user = users.get_current_user()
        user_email = current_user.email()
        user = User.query().filter(User.email == current_user.email()).get()
        if not user:
            user = User(email=user_email)
        user.image = image
        user.put()
        template_vars = {
            "img_link": image,
            "user": user
        }
        template = jinja_environment.get_template('templates/profile.html')
        self.response.write(template.render(template_vars))
        #self.redirect('/profile')

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
                    winner = checkSouthWest(board,row,col)
                    if(winner!=0):
                        return winner
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
    return 0
def checkSouthEast(board, row, col):
    if(board[row][col] == 0):
        return 0;
    count = 0
    for i in range(1,4):
        if(board[row][col]==board[row+i][col+i]):
            count = count + 1
            if(count==3):
                return board[row][col]
    return 0
def checkSouth(board, row, col):
    if(board[row][col] == 0):
        return 0;
    count = 0
    for i in range(1,4):
        if(board[row][col]==board[row+i][col]):
            count = count + 1
            if(count==3):
                return board[row][col]
    return 0
def checkSouthWest(board, row, col):
    if(board[row][col] == 0):
        return 0;
    count = 0
    for i in range(1,4):
        if(board[row][col]==board[row+i][col-i]):
            count = count + 1
            if(count==3):
                return board[row][col]
    return 0

class ColumnHandler(webapp2.RequestHandler):
    def post(self):
        col = int(self.request.get('column'))
        game = Game.query().get()
        board = json.loads(game.board)

        # === 2: Interact with the database. ===

        # Use the URLsafe key to get the photo from the DB.
        var = 0
        logging.info("Player 1 : %s", game.player1)
        logging.info("Player 2 : %s", game.player2)
        if(game.current_player == game.player1):
            var = 1
        elif(game.current_player == game.player2):
            var = 2
        if(game.player1 == game.current_player):
            if(board[5][col] == 0):
                board[5][col] = 1
                game.current_player = game.player2
            elif(board[4][col] == 0):
                board[4][col] == 1
                game.current_player = game.player2
            elif(board[3][col] == 0):
                board[3][col] == 1
                game.current_player = game.player2
            elif(board[2][col] == 0):
                board[2][col] == 1
                game.current_player = game.player2
            elif(board[1][col] == 0):
                board[1][col] == 1
                game.current_player = game.player2
            elif(board[0][col] == 0):
                board[0][col] == 1
                game.current_player = game.player2
        elif(game.player2 == game.current_player):
            if(board[5][col] == 0):
                board[5][col] = 2
                game.current_player = game.player1
            elif(board[4][col] == 0):
                board[4][col] == 2
                game.current_player = game.player1
            elif(board[3][col] == 0):
                board[3][col] == 2
                game.current_player = game.player1
            elif(board[2][col] == 0):
                board[2][col] == 2
                game.current_player = game.player1
            elif(board[1][col] == 0):
                board[1][col] == 2
                game.current_player = game.player1
            elif(board[0][col] == 0):
                board[0][col] == 2
                game.current_player = game.player1
        if(checkWin(board)==1):
            game.winner = 1
        if(checkWin(board)==2):
            game.winner = 2
        logging.info(board)
        logging.info(game.winner)
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
