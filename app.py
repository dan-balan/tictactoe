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

from oophelpers import *
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


activeGamingRooms = []
connectetToPortalUsers = []

# players = {0:'', 1:''}
# playersReadyForStart = {0:False, 1:False}
# started = True
# activePlayer = randint(0, 1)
# onlineClients = []
# gameRoom = 'room#2100'
# maxNumberOfPlayers = 2

# ! server-client communication

# ################# handler(1') #################
# handler for player/client connect event
# emited events: tooManyPlayers(msg) OR clientId(msg),connected-Players(msg), status(msg)
@socketio.event
def connect():
    """

    """
    global connectetToPortalUsers
    player = Player(request.sid)
    connectetToPortalUsers.append(player)
    
    emit('connection-established', 'go', to=request.sid)


@socketio.on('check-game-room')
def checkGameRoom(data):
    global onlineClients
    global connectetToPortalUsers
    global activeGamingRooms
    # user index
    userIdx = getPlayerIdx(connectetToPortalUsers, request.sid)
    if userIdx is not None:
        connectetToPortalUsers[userIdx].name = data['username']
        connectetToPortalUsers[userIdx].requestedGameRoom = data['room']
    
    # check if room exists in activeGamingRooms
    roomIdx = getRoomIdx(activeGamingRooms, data['room'])
    # if room not existing
    if roomIdx is None:
        room = GameRoom(data['room'])
        room.add_player(connectetToPortalUsers[userIdx])
        activeGamingRooms.append(room)
        
        # join socketIO gameroom
        join_room( data['room'])
        emit('tooManyPlayers', 'go', to=request.sid)

    else:
        if activeGamingRooms[roomIdx].roomAvailable():
            activeGamingRooms[roomIdx].add_player(connectetToPortalUsers[userIdx])
            
            join_room( data['room'])
            emit('tooManyPlayers', 'go', to=request.sid)
        else:
            # print local to server console
            print('Too many players tried to join!')
            # send to client
            
            emit('tooManyPlayers', 'tooCrowdy', to=request.sid)
            disconnect()
            return
    
    session['username'] = data['username']
    session['room'] = data['room']


# ####### Server asyn
@socketio.event
def readyToStart():
    global activeGamingRooms
    
    roomIdx = getRoomIdx(activeGamingRooms, session['room'])
    playerId = activeGamingRooms[roomIdx].getPlayerIdx(request.sid)
    onlineClients = activeGamingRooms[roomIdx].getClientsInRoom('byName')
    
    emit('clientId', (playerId, session.get('room')))
    emit('connected-Players', [onlineClients], to=session['room'])
    emit('status', {'clientsNbs': len(onlineClients), 'clientId': request.sid}, to=session['room'])

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
    global activeGamingRooms
    global connectetToPortalUsers
    userIdx = getPlayerIdx(connectetToPortalUsers, request.sid)
    roomIdx = getRoomIdx(activeGamingRooms, session['room'])

    connectetToPortalUsers[userIdx].start_game_intention()
    started = activeGamingRooms[roomIdx].get_ready_for_game()

    activePlayer = activeGamingRooms[roomIdx].get_rand_active_player()
    if (started):
        emit('start', {'activePlayer':activePlayer, 'started': started}, to=session['room'])
    else:
        emit('waiting second player start', to=session['room'])

# ################# handler(3) #################
# start the game when 2 players pressed the Start button
# emited events: turn(msg)
@socketio.on('turn')
def turn(data):
    global activeGamingRooms
    roomIdx = getRoomIdx(activeGamingRooms, session['room'])

    activePlayer = activeGamingRooms[roomIdx].get_swap_player()


    # global activePlayer
    print('turn by {}: position {}'.format(data['player'], data['pos']))
      
    # swap activePlayer
    # activePlayer = int(not(bool(activePlayer)))

    # ! TODO set the fields
    # notify all clients that turn happend and over the next active id
    emit('turn', {'recentPlayer':data['player'], 'lastPos': data['pos'], 'next':activePlayer}, to=session['room'])

# ################# handler(3.1) #################
# information about game status
@socketio.on('game_status')
def game_status(msg):
    
    # get status for restart game
    global activeGamingRooms
    roomIdx = getRoomIdx(activeGamingRooms, session['room'])
    activeGamingRooms[roomIdx].startRound()
    
    print(msg['status'])


# get key by value from a dict
def getKeybyValue(obj, value):
    key = [k for k, v in obj.items() if v == value]
    return key

# get player's index from all players list
def getPlayerIdx(obj, sid):
    idx = 0
    for player in obj:
        if player.id == sid:
            return idx
        idx +=1

# get room's index from active rooms list
def getRoomIdx(obj, roomName):
    idx = 0
    for player in obj:
        if player.name == roomName:
            return idx
        idx +=1

@socketio.event
def disconnect():
    global activeGamingRooms
    global connectetToPortalUsers
    userIdx = getPlayerIdx(connectetToPortalUsers, request.sid)             # user position in connectedToPortalUsers
    roomIdx = getRoomIdx(activeGamingRooms, session['room'])                # active room of the user
    userIdxInRoom = activeGamingRooms[roomIdx].getPlayerIdx(request.sid)    # user index in active room
    
    del activeGamingRooms[roomIdx].onlineClients[userIdxInRoom]             # delete the user from active room
    del connectetToPortalUsers[userIdx]                                     # delete user from connectedToPortalUsers

    onlineClients = activeGamingRooms[roomIdx].get_players_nbr()
    print("client with sid: {} disconnected".format(request.sid))

    if onlineClients == 0:
        roomName = activeGamingRooms[roomIdx].name
        del activeGamingRooms[roomIdx]
        print ('room: {} closed'.format(roomName))
    else:
        # emit('status', {'clients': onlineClients}, to=session['room'])
        emit('disconnect-status', {'clientsNbs': onlineClients, 'clientId': request.sid}, to=session['room'])


if __name__ == '__main__':
    socketio.run(app, debug=True)
