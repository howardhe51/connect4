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
    email = ndb.StringProperty()
    username = ndb.StringProperty()
    win = ndb.IntegerProperty()
    lose = ndb.IntegerProperty()


class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    image = ndb.BlobProperty()
    user_key = ndb.StringProperty()

class Game(ndb.Model):
    board = ndb.JsonProperty()
    player1 = ndb.StringProperty()
    player1email = ndb.StringProperty()
    player2 = ndb.StringProperty()
    player2email = ndb.StringProperty()
    current_player = ndb.StringProperty()
    winner = ndb.StringProperty()
    game_key = ndb.KeyProperty()
    game_key_string = ndb.StringProperty()

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
        games = Game.query().fetch()
        template_vars = {
            'current_user': current_user,
            'logout_url': logout_url,
            'login_url': login_url,
            'games': games,
        }
        template = jinja_environment.get_template('templates/main.html')
        self.response.write(template.render(template_vars))

class CreateGameHandler(webapp2.RequestHandler):
    def post(self):
        board = [ [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0]]
        current_user = users.get_current_user()
        game = Game(board = json.dumps(board),current_player = current_user.user_id(),player1 = current_user.user_id(),player1email = current_user.email())
        game_key = game.put()
        game.game_key = game_key
        game.game_key_string = game.key.urlsafe()
        game.put()
        url = "/game?key=" + game.game_key_string
        self.redirect(url)

class GameHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/game.html')
        self.response.write(template.render())
    def post(self):
        current_user = users.get_current_user()
        urlsafe_key = self.request.get("key")
        game_key = ndb.Key(urlsafe = urlsafe_key)
        game = game_key.get()
        url = "/game?key=" + urlsafe_key
        if(game.player2 == None and game.player1 != current_user.user_id()):
            game.player2= current_user.user_id()
	    game.player2email = current_user.user_id()
        game.put()
        self.redirect(url)

class DeleteHandler(webapp2.RequestHandler):
    def post(self):
        current_user = users.get_current_user()
        game = Game.query().filter(ndb.OR(Game.player1 == current_user.user_id(), Game.player2== current_user.user_id())).get()
        if(game == None ):
            string = "ARrrr"
        elif(game.player1 == current_user.user_id() or game.player2 == current_user.user_id()):
            game.key.delete()
        self.redirect("/")

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        # Get the current user's email
        current_user = users.get_current_user()
        # Only query for User models that have the email of the current user
        user = User.query().filter(User.email == current_user.email()).get()
        #user = user_query.get()
        template_vars = {
            "user": user
        }
        template = jinja_environment.get_template('templates/profile.html')
        self.response.write(template.render(template_vars))

    def post(self):
        image = self.request.get('img_link')
        # image is a "unicode" type, but we want it to be a string
        image = str(image)
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
    def get(self):
        current_user = users.get_current_user()
        # game = Game.query().get()
        game = Game.query().filter(Game.current_player == current_user.user_id()).get()
        logging.info(game)
        board = json.loads(game.board)
        self.response.write(json.dumps({'board':board, 'winner':game.winner, "player1":game.player1, "player2":game.player2}))

    def post(self):
        col = int(self.request.get('column'))
        current_user = users.get_current_user()
        game = Game.query().filter(Game.current_player == current_user.user_id()).get()
        logging.info(game)
        board = json.loads(game.board)
        #logging.info(board)
        if(game.player1 == users.get_current_user().user_id() and game.player2 != None):
            if(game.player1 == game.current_player):
                if(board[5][col] == 0):
                    board[5][col] = 1
                elif(board[4][col] == 0):
                    board[4][col] = 1
                elif(board[3][col] == 0):
                    board[3][col] = 1
                elif(board[2][col] == 0):
                    board[2][col] = 1
                elif(board[1][col] == 0):
                    board[1][col] = 1
                elif(board[0][col] == 0):
                    board[0][col] = 1
                game.current_player = game.player2
        elif(game.player2 == users.get_current_user().user_id() and game.player1 != None):
            if(game.player2 == game.current_player):
                if(board[5][col] == 0):
                    board[5][col] = 2
                elif(board[4][col] == 0):
                    board[4][col] = 2
                elif(board[3][col] == 0):
                    board[3][col] = 2
                elif(board[2][col] == 0):
                    board[2][col] = 2
                elif(board[1][col] == 0):
                    board[1][col] = 2
                elif(board[0][col] == 0):
                    board[0][col] = 2
                game.current_player = game.player1
        if(checkWin(board)==1):
            game.winner = game.player1
        if(checkWin(board)==2):
            game.winner = game.player2
        game.board = json.dumps(board)
        game.put()
        template = jinja_environment.get_template('templates/game.html')
        self.response.write(json.dumps({'board':board, 'winner':game.winner, "player1":game.player1, "player2":game.player2}))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/create', CreateGameHandler),
    ('/game', GameHandler),
    ('/column', ColumnHandler),
    ('/profile', ProfileHandler),
    ('/delete', DeleteHandler),
    ], debug=True)
