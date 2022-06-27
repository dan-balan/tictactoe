"""

# Online Multiplayer Tic-Tac-Toe

d-_-b

## Tools and technologies:
Server side:
- Python frameworks: Flask, Flask SocketIO
Client Side:
- JS (including SocketIO framework)
- HTML
- CSS

## Game specific
- 2 players (x|o);
- player with 1st move;

On client `connect`:

|Client        |Server        |
|:---         |---:           |
|generated: `connect` event|received: `connect`|

> Steps
- `connect` event generated when Client connects to the server
    - Server side: 
        - readyForGameCheck
        - gamePreparation
        - `emit` the information to the client (clientId, startGame, activeId)

- client `receive` clientId, startGame, activeId
    - Client side: 
        - gamePreparation
        - startGame (eventListener & handleClick for each 3x3 cells)
        - `emit` the move to the server & check win or draw

"""

from flask import Flask, render_template, session, request
# from flask_login import LoginManager, UserMixin
# from flask_session import Session
from flask_socketio import SocketIO, emit, join_room, disconnect, leave_room

from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'
app.config['SESSION_TYPE'] = 'filesystem'
# login = LoginManager(app)
# Session(app)
# socketio = SocketIO(app, manage_session=False)
socketio = SocketIO(app)



@app.route('/tictactoe')
def tictactoe():
    return render_template('tictactoe.html')

@app.route('/')
def tictactoe2():
    return render_template('tictactoe.html')


# ! game preparation

class Player():
    """
    player modelisation

    """
    gameStart = False

    def __init__(self, name, room):
        self.name = name
        self.room = room
    
    def set_game_mark(self, gameMark):
        self.gameMark = gameMark

    def start_game_intention(self, gameStart = True):
        self.gameStart = gameStart

    def get_game_intention(self):
        return self.gameStart



class GameRoom():
    """
    
    modelisation of a game room
    
    """

    onlineClients = []
    gameRound = True


    def __init__(self, roomName):
        self.roomName = roomName
    
    def add_player(self, objPlayer):
        self.onlineClients.append(objPlayer)
    
    def get_players_nbr(self):
        return len(onlineClients)

    def check_players_game_start(self):
        for player in self.onlineClients:
            if player.get_game_intention() == False:
                self.gameRound = False
                return

    def get_rand_active_player(self):
        return randint(0, 1)


players = {0:'', 1:''}
playersReadyForStart = {0:False, 1:False}
started = True
activePlayer = randint(0, 1)
onlineClients = []
gameRoom = 'room#2100'
maxNumberOfPlayers = 2

# ! server-client communication

# ################# handler(1') #################
# handler for player/client connect event
# emited events: tooManyPlayers(msg) OR clientId(msg),connected-Players(msg), status(msg)
@socketio.event
def connect():
    """

    client connects to the server -> connect event generated
    if more than 2 clients in the gaming room: socket disconnect;
    else join gamming room;
    server emit the clientId;

    """
    global onlineClients
    
    # disconnect if 2 clients connected
    if len(onlineClients)>= maxNumberOfPlayers:
        # print local to server console
        print('Too many players tried to join!')
        # send to client
        emit('tooManyPlayers', 'tooCrowdy')

        disconnect()
        return
    else:
        onlineClients.append(request.sid)
        # socketio.server.enter_room(request.sid, room=gameRoom)
        
        emit('tooManyPlayers', 'go')

        # get payer id
        playerId = onlineClients.index(request.sid, )
        print('Online Clients: ', onlineClients,' Last cliend sessionId:', request.sid )
        # emit('user-connected')


# ####### Server asyn
@socketio.event
def readyToStart(data):
    global onlineClients
    session['username'] = data['username']
    session['room'] = data['room']
    join_room(session['room'])
    playerId = onlineClients.index(request.sid, )

    emit('clientId', (playerId, session.get('room')))
    emit('connected-Players', [onlineClients], to=session['room'])
    emit('status', {'clientsNbs': len(onlineClients), 'clientId': request.sid})

# #######

# ! CHAT BETWEEN PLAYERS
# Event handler for player/client message
# ################# handler(1c) #################
# emited events: player message(msg)
@socketio.event
def my_broadcast_event(message):
    emit('player message',
         {'data': message['data'], 'sender':message['sender']}, to=session['room'])

# ! CHAT BETWEEN PLAYERS

# ################# handler(2) #################
# start the game when 2 players pressed the Start (or Restart) button
# emited events: start(msg) OR <waiting second player start>
@socketio.event
def startGame(message):
    global activePlayer
    global started
    started = True
    playersReadyForStart[message['clientId']]= True
    print(playersReadyForStart)
    for k, v in playersReadyForStart.items():
        if v == False:
            started = False
            break
    # emit('start', (activePlayer, started))
    if (started):
        emit('start', {'activePlayer':activePlayer, 'started': started}, to=session['room'])
    else:
        emit('waiting second player start', to=session['room'])

# ################# handler(3) #################
# start the game when 2 players pressed the Start button
# emited events: turn(msg)
@socketio.on('turn')
def turn(data):
    global activePlayer
    print('turn by {}: position {}'.format(data['player'], data['pos']))
    
    # swap activePlayer
    activePlayer = int(not(bool(activePlayer)))

    # ! TODO set the fields
    # notify all clients that turn happend and over the next active id
    emit('turn', {'recentPlayer':data['player'], 'lastPos': data['pos'], 'next':activePlayer}, to=session['room'])

# ################# handler(3.1) #################
# information about game status
@socketio.on('game_status')
def game_status(msg):
    global playersReadyForStart
    playersReadyForStart = {0:False, 1:False}
    activePlayer = randint(0, 1)
    print(msg['status'])



# TODO: add socket id to player obj
def joinPlayer(sid, clients):
    for player in players:
        currentPlayer = player[player]
        if currentPlayer == "":
            players[player]= sid
    if sid not in onlineClients:
        onlineClients.append(sid)
    return

def getKeybyValue(obj, value):
    key = [k for k, v in obj.items() if v == value]
    return key

@socketio.event
def disconnect():
    global onlineClients
    sid = request.sid
    if sid in onlineClients:
        onlineClients.remove(sid)
    print("client with sid: {} disconnected".format(sid))
    emit('status', {'clients': len(onlineClients)})


if __name__ == '__main__':
    socketio.run(app, debug=True)
