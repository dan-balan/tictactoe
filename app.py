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
from flask_socketio import SocketIO, emit, join_room, disconnect

from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'
app.config['SESSION_TYPE'] = 'filesystem'
# login = LoginManager(app)
# Session(app)
# socketio = SocketIO(app, manage_session=False)
socketio = SocketIO(app)

# class User(UserMixin, object):
#     def __init__(self, id=None):
#         self.id = id

# @login.user_loader
# def load_user(id):
#     return User(id)


@app.route('/tictactoe')
def tictactoe():
    return render_template('tictactoe.html')

@app.route('/')
def tictactoe2():
    return render_template('tictactoe.html')


# ! game preparation

players = {0:'', 1:''}
playersReadyForStart = {0:False, 1:False}
started = True
activePlayer = randint(0, 1)
onlineClients = []
gameRoom = 'newGame'
maxNumberOfPlayers = 2

# ! server-client communication

# ################# handler(1') #################
# handler for player/client connect event
# get info about the player form Greetings form
# emited events: my_connection_trigger(msg)
@socketio.event
def my_connection_trigger(message):
    session['username'] = message['username']
    session['room'] = message['room']
    print('my_event @ connection :[username:{}],[room: {}]'.format(session.get('username'), session.get('room')))
    
    emit('my_response',
         {'data': message['data'], 'sessionId':session.get('sessionId')})

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
        emit('tooManyPlayers', {'status':'tooManyPlayers'})
        disconnect()
        return
    else:
        sid = request.sid
        onlineClients.append(sid)
        socketio.server.enter_room(sid, room=gameRoom)

        # get payer id
        playerId = onlineClients.index(sid, )
        print('Online Clients: ', onlineClients,' Last cliend sessionId:', sid )
        emit('clientId', playerId)
        emit('connected-Players', [onlineClients], broadcast=True)
        emit('status', {'clientsNbs': len(onlineClients), 'clientId': sid})


# ! CHAT BETWEEN PLAYERS
# Event handler for player/client message
# ################# handler(1c) #################
# emited events: player message(msg)
@socketio.event
def my_broadcast_event(message):
    emit('player message',
         {'data': message['data'], 'sender':message['sender']}, broadcast=True)

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
        emit('start', {'activePlayer':activePlayer, 'started': started}, broadcast=True)
    else:
        emit('waiting second player start', broadcast=True)

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
    emit('turn', {'recentPlayer':data['player'], 'lastPos': data['pos'], 'next':activePlayer}, broadcast=True)

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
