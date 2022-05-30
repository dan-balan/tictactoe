
// ! VARIABLES DECLARATIONS
const startGameButton = document.getElementById('gameStart')
const roomName = document.getElementById('gameRoom')
const playerName = document.getElementById('playerName')
const connectedContainer = document.getElementById('connected_players')

const X_CLASS = 'x'
const CIRCLE_CLASS = 'circle'
const WINNING_COMBINATIONS = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
const cellElements = document.querySelectorAll('[data-cell]')
const board = document.getElementById('board')
const winningMessageElement = document.getElementById('winningMessage')
const restartButton = document.getElementById('restartButton')
const winningMessageTextElement = document.querySelector('[data-winning-message-text]')
let circleTurn

const token = { 0: "circle", 1: "cross"};
let clientId;
let activeId;

// ! SERVER-CLIENT COMMUNICATION
// SOCKET.IO
var socket = io();

// ################# emit(1) #################
// Event handler for new connections.
// The callback function is invoked when a connection with the
// server is established.
socket.on('connect', function() {
  console.log('Event <<my_event>> was sent to server!')
});


var checkConnectedNb = ''

// ################# hadler (1.1) #################
// Event handler for server sent data
socket.on('tooManyPlayers', (msg) => {checkConnectedNb = msg['status']})

// alert if more than 2 players are join in the same room 
// if playersNb = 2 <Greetings view> hide 
document.getElementById('joinRoom').addEventListener('click', function(event) {
  event.preventDefault()
  console.log("Status: ", checkConnectedNb)
  if (checkConnectedNb == 'tooManyPlayers'){
    if (socket) {
      socket.disconnect()
      socket = null
    }
    // TODO: html modal view about "unable to join"
    alert('too many players in this Gaming Room!')
    return;
  } 
  if (playerName.value == '' || roomName.value == '') {
    alert('Please fill out Room Name and Player Name fields!')
    return;
  }
  document.getElementById('greetingsBackground').classList.remove('show')
  socket.emit('my_connection_trigger', {data: 'I\'m connected!', username: playerName.value, room : roomName.value});

})


// ! user pushed the StartGame button
// todo: handler for .close 
// document.querySelector('.close').addEventListener('click', function() {
//   document.getElementById('greetingsBackground').classList.remove('show')
// })



// ################# hadler (1.2) #################
// Event handler for server sent data
// get client id
socket.on('clientId', (id) => {
  clientId = id;
  let mark = (clientId == 0) ? CIRCLE_CLASS : X_CLASS
  console.log('Clog: Received playerId: ', id)

  t1 = `Received playerId: ${id}`
  addMsg(t1, 'msg-container center', 'msg-content refer')
})

// ################# hadler (1.2') #################
// Event handler for server sent data
// get connected-Players
var connectedPlayers = []
socket.on('connected-Players', (players) => {
  connectedPlayers = []
  for (var i = 0; i < players[0].length; i++) {
    connectedPlayers.push(players[0][i]);
  }
  console.log(connectedPlayers)
  
  connectedContainer.innerText = connectedPlayers 

})



// ################# hadler (1.3) #################
// Event handler for server sent data
socket.on('status', function(msg) {  
  console.log (`Clog: Last joined: ${msg['clientId']} || Clients Nbr.:${msg['clientsNbs']}`);
  
  t1 = `Last joined: ${msg['clientId']}. clients connected: ${msg['clientsNbs']}`
  addMsg(t1, 'msg-container center', 'msg-content refer')
});

// ! CHAT BETWEEN PLAYERS
// ################# event(1c) #################
// emited events: my_broadcast_event(msg)
// when at input #message and #send: send data to server  
document.getElementById('send').addEventListener('click', function(event) {
  event.preventDefault()
  if (document.getElementById('message').value === ''){
    return;
  }
  socket.emit('my_broadcast_event', {data: document.getElementById('message').value, sender: clientId});
  document.getElementById('message').value = ''
  return false;
});

// ################# handler(1c) #################
// Event handler for server sent data <player message>
socket.on('player message', function(msg) {  
  // console.log (`Clog: received from server: msg-data:${msg['data']} with sessionId ${msg.sessionId}`);
  t1 = `${msg.data}`
  if (msg.sender == clientId){
      addMsg(t1, 'msg-container right', 'msg-content refer')
  } else{
    addMsg(t1, 'msg-container', 'msg-content')
  }
  // scrollDownlogsWindow()
});

// ! CHAT BETWEEN PLAYERS

// ################# event(2) #################
// user pushed the StartGame button 
// emited events: startGame(msg)
startGameButton.addEventListener('click', function(){
  socket.emit('startGame', {'clientId':clientId})
  // startGame()
})

// ################# event(2.1) #################
// get the active player id and set up html for game
socket.on('start', (data) => {
  activeId = data['activePlayer'];
  var readyToStart = data['started'];
    console.log('Active user: ', activeId )
    alert("Game Started")
  t1 = `Active user: ${activeId}`
  addMsg(t1, 'msg-container center', 'msg-content refer')
  startGame()
});

// ################# event(2.2) #################
// Server Event: waiting for second player start
socket.on('waiting second player start', (data) => {
  t1 = `Waiting for second player's Start...`
  addMsg(t1, 'msg-container center', 'msg-content refer')
});


// ################# event(3) #################
// startGame() -> at player click -> <turn> event
// send turn event to server
// emited events: turn(msg)
function turn(e) {
  var pos = get_idx(e)
  console.log('send')
  socket.emit("turn", {"pos": pos, "player": activeId})
}

// ################# handler(3) & event(3) #################
// update field with turn information received from server
// emited events (if Win OR Draw): game_status(msg)

socket.on('turn', (turn) => {
  // let {recentPlayer, position, next} = turn;
  let currentMark = (turn['recentPlayer'] == 0) ? CIRCLE_CLASS : X_CLASS
  console.log(`Last Position by ${turn['recentPlayer']}, is ${turn['lastPos']}`)

  t1 = `Last Position by ${turn['recentPlayer']}, is ${turn['lastPos']}`
  addMsg(t1, 'msg-container center', 'msg-content refer')
  placeMark(cellElements[turn['lastPos']], currentMark);

  if (checkWin(currentMark)) {
    endGame(false, currentMark)
    socket.emit('game_status', {'status': 'Win' , 'player':turn['recentPlayer']})
  } else if (isDraw()) {
    endGame(true)
    socket.emit('game_status', {'status': 'Draw' , 'player':turn['recentPlayer']})

  }
  activeId = turn['next'];
})

// ################# event(4) #################
// send restart intention to server
// emited events: restartGame(msg) intention
restartButton.addEventListener('click', function() {
  socket.emit('startGame', {'clientId':clientId})
  // startGame()
});

// ! GAME LOGIC

function startGame() {
  circleTurn = (activeId == 0) ?  true : false
  cellElements.forEach(cell => {
    cell.classList.remove(X_CLASS)
    cell.classList.remove(CIRCLE_CLASS)
    
    let playerMark = (clientId == 0) ?  true : false
    setBoardHoverClass(playerMark)

    cell.removeEventListener('click', handleClick)
    cell.addEventListener('click', handleClick)

  })
  winningMessageElement.classList.remove('show')
}

function handleClick(e) {
  const cell = e.target
  
  let currentMark = (clientId == 0) ? CIRCLE_CLASS : X_CLASS
  if (activeId == clientId){
    placeMark(cell, currentMark);
    turn(e)
  }
  if (checkWin(currentMark)) {
    endGame(false, currentMark)
  } else if (isDraw()) {
    endGame(true)
  }  
  console.log('clicked index: ', get_idx(e));
  
}

// HELPERS

function placeMark(cell, currentClass) {
  cell.classList.add(currentClass)};

function swapTurns() {
  circleTurn = !circleTurn
}

function setBoardHoverClass(clientIdClass) {
  board.classList.remove(X_CLASS)
  board.classList.remove(CIRCLE_CLASS)
  if (clientIdClass) {
    board.classList.add(CIRCLE_CLASS)
  } else {
    board.classList.add(X_CLASS)
  }
}

function get_idx(e){
  var clickedtargetParent = e.target.parentElement;
  var idx = Array.prototype.indexOf.call(clickedtargetParent.children, e.target);
  return idx;
}


function endGame(draw, currentMark) {
  if (draw) {
    winningMessageTextElement.innerText = 'Draw!'
  } else {
    winningMessageTextElement.innerText = `${(currentMark == 'circle') ? "O's" : "X's"} Wins!`
  }
  winningMessageElement.classList.add('show')
}

function isDraw() {
  return [...cellElements].every(cell => {
    return cell.classList.contains(X_CLASS) || cell.classList.contains(CIRCLE_CLASS)
  })
}

function checkWin(currentClass) {
  return WINNING_COMBINATIONS.some(combination => {
    return combination.every(index => {
      return cellElements[index].classList.contains(currentClass)
    })
  })
}


// append newMsg to logs View
function addMsg(contText, msgPos, msgOriginator, parrentToAapped = 'msg-area') {
  aa = document.createElement('div')
  aa.className = 'message-in'
    bb = document.createElement('div')
    bb.className = msgPos
      cc = document.createElement('div')
      cc.className = msgOriginator
      cc.innerText = contText
    
      bb.appendChild(cc)
  aa.appendChild(bb)
  document.getElementById(parrentToAapped).appendChild(aa)
  scrollDownlogsWindow()
}

// Scroll chat window down
function scrollDownlogsWindow(scrollBox = ".msg") {
  const logsWindow = document.querySelector(scrollBox);
  logsWindow.scrollTop = logsWindow.scrollHeight;
}

