# Online Multiplayer Tic-Tac-Toe

d-_-b

## Tools and technologies:

**Server side:**
- Python frameworks: Flask, Flask SocketIO

**Client Side:**
- JS (including SocketIO framework)
- HTML
- CSS

Server Client communication based on [Socket.IO](https://socket.io/docs/v4/) protocol
![Socket.IO](https://socket.io/images/bidirectional-communication2.png)

## Game specific
- 2 players (x|o);
- player with 1st move => place mark (x|o):
- Until (win or draw): player 2 place mark => swap turn => 1st player place mark;

## Implementation logic
---  

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