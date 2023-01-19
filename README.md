# __Online Multiplayer Tic-Tac-Toe__
#### Video Demo:  <URL HERE>
#### Description: This web app is intended to be the online "paper" for classical Tic Tac Toe paper game. The app serves as the platform that allow to play the TTT game, alongside which is provided also a basic chat feature in order to facilitate players communication.

## __Macro Specification:__ 
-	An online “game board” to play a TTT game;
    - Players must be able to communicate to each other;
-	Web App has to provide multi-rooms feature.

<h2 style="text-align: center;">d-_-b</h2>

![Online Multiplayer Tic-Tac-Toe](./static/assets/tictactoe-online-multiplayer.gif)

## Tools and technologies:

Server Client communication based on [Socket.IO](https://socket.io/docs/v4/) protocol
![Socket.IO](https://socket.io/images/bidirectional-communication2.png)


|**Client Side <sup>*</sup> :**                |**Server side:**                        |
|:---                                          |---:                                    |
|HTML, CSS, JS (including SocketIO framework)  |Python frameworks: Flask, Flask SocketIO|

_<sup>*</sup>front-end elements of Tic Tac Toe board inspired from Web Dev Simplified [Tic Tac Toe project](https://github.com/WebDevSimplified/JavaScript-Tic-Tac-Toe) - one side 2 player functionality_


## Game specific
- 2 players ( *x* | *o* );
- player with 1st move => place mark ( *x* | *o* ):
- Until (win or draw): player 2 place mark => swap turn => 1st player place mark;

## Implementation logic
---  

In **Online Multiplayer Tic-Tac-Toe** game, processing the moves, handling the connection of the players, players chat and gaming rooms management is provided by the server (in this case with the help of Flask, Flask SocketIO frameworks). As per tic tac toe  rules, there are only two players in one game. This mean that the server has to check the existence of gaming room and if there are already two players before connecting a new one.


Step 1 - Connection
* Two clients connect to the server. 
    * Initial check: existence of the room, number of players;

Step 2 - Player is informed
* Client receives information about their player id used to map player’s figure (e.g., cross or circle). 

Step 3 - startGame
* Server starts the match and informs the players about who will start the match when players have agreed to start game.
    * In the third step, the two players are playing against each other. 
First, the player will click on a field and that information is sent to the server. 
The information about the selected field and the next player are sent to the clients by the server in the room. 
This will be repeated until draw or one player won the game.



`app.py`

The file where all the fun starts...
Here is the configuration of Flask and Flask Socket IO frameworks.
Once configured, the Flask routes are _decorated_ with `@app.route()` and Flask SocketIO handlers are _decorated_ with `@socketio.event`.
At the bottom of the file, there's `socketio.run(app, debug=True)` that will start the server. 
_"The `socketio.run()` function encapsulates the startup of the web server and replaces the `app.run()` standard Flask development server start up."_ [Flask SocketIO](https://flask-socketio.readthedocs.io/en/latest/getting_started.html#initialization)

`oophelpers.py`

There’s the modeling of `Player()` and `GameRoom()` objects. Within itself, classes define behavior and needed attributes.

`templates/`

Basically, the `templates/index.html` is just an HTML page that describe the content of the page - board game and logs area. On top of the page there's "Greetings view" as a modal view that will change the state: `display: show` -> `display: none` when the server event is emit the room availability. 

`static/styles/`

That's where are the CSS files used to describe the aesthetics of the page.

`static/scripts/`

In the `main.js` file are the scripts that make webapp interaction possible.
The file starts with the "_VARIABLE DECLARATIONS_" at the top, afterwards on `joinButton`'s `addEventListener` anonymous function is verified the `roomAvailability()` by the mean of `async` & `await` functions. Once the room availability is confirmed, the `userConnectedHandlers()` are called. The chat and game function are provided throughout the EventListener attached to *sendButton*, *startGameButton*, *restartButton* buttons.


`requirements.txt`

That file simply prescribes the dependencies packages for this web app.



Reproduce web application
=========================

One way to run this application: 
- create a Python virtual environment;
```bash
python -m venv [directory]
```

- install the requirements in virtual environment;
```bash
pip install -r requirements.txt
```
- run `python app.py` or `flask run` and visit `http://localhost:5000` in two separate browser tabs.
```bash
python app.py
```
or
```bash
flask run
```

#### Containerization using docker

Build an Image from the Dockerfile
```bash
docker build -t <img_name> .        
```
```bash
docker build -t flask-tictactoe .        
```

Run a container in background with and publish a container’s port(s) to the host
```bash
docker run -d -p <host_port>:<container_port> <image_name>    
```
```bash
docker run -d -p 80:5000 flask-tictactoe  
```

Acces the container in browser using: `http://localhost` or `http://127.0.0.1`