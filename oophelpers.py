from random import randint


# ! game preparation

class Player():
    """
    player modelisation

    """

    def __init__(self, sid):
        self.id = sid
        self.name = ''
        self.requestedGameRoom = ''
        self.gameMark = ''
        self.gameStartIntention = False

    def set_user_name(self, name):
        self.name = name
    
    def set_requested_game_room(self, room):
        self.requestedGameRoom = room

    def set_game_mark(self, gameMark):
        self.gameMark = gameMark

    def start_game_intention(self, gameStart = True):
        self.gameStartIntention = gameStart

    def get_game_intention(self):
       return self.gameStartIntention



class GameRoom():
    """
    
    modelisation of a game room
    
    """

    def __init__(self, roomName):
        self.name = roomName
        self.onlineClients = []
        self.gameRound = None
        self.activePlayer = 0
    
    def add_player(self, objPlayer):
        self.onlineClients.append(objPlayer)
    
    def get_players_nbr(self):
        return len(self.onlineClients)

    def check_players_game_start(self):
        for player in self.onlineClients:
            if player.get_game_intention() == False:
                self.gameRound = False
                return
            self.gameRound = True

    def get_rand_active_player(self):
        self.activePlayer = randint(0, 1)
        return self.activePlayer

    def get_swap_player(self):
        self.activePlayer =  int(not(bool(self.activePlayer)))
        return self.activePlayer

    def get_ready_for_game(self):
        self.check_players_game_start()
        return self.gameRound

    def roomAvailable(self):
        """
        check to have only 2 players joined
        """
        if len(self.onlineClients) < 2:
            return True
        else:
            return False

    def getPlayerIdx(self, sid):
        """
        return the player index from active game room
        Arguments:
        sid: id 
        """
        idx = 0
        for player in self.onlineClients:
            if player.id == sid:
                return idx
            idx +=1
    
    def getClientsInRoom(self, requestType = 'byID'):
        connectedPlayers = []

        for player in self.onlineClients:
            if requestType == 'byId':
                connectedPlayers.append(player.id)
            elif requestType == 'byName':
                connectedPlayers.append(player.name)
        return connectedPlayers

    def startRound(self):
        for player in self.onlineClients:
            player.gameStartIntention = False


