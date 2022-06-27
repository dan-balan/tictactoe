// ! VARIABLES DECLARATIONS
export const winningMessageElement = document.getElementById('winningMessage');
export const winningMessageTextElement = document.querySelector('[data-winning-message-text]');
export const WINNING_COMBINATIONS = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];
export const board = document.getElementById('board');
export const startGameButton = document.getElementById('gameStart');
export const roomName = document.getElementById('gameRoom');
export const playerName = document.getElementById('playerName');
export const connectedContainer = document.getElementById('connected_players');
export const cellElements = document.querySelectorAll('[data-cell]');
export const restartButton = document.getElementById('restartButton');
export const gameRoomTitle = document.querySelector('.modal-header-title')
export const joinButton = document.getElementById('joinRoom')
export const sendButton = document.getElementById('send')
export const X_CLASS = 'x';
export const CIRCLE_CLASS = 'circle';
