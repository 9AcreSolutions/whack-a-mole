const holes = document.querySelectorAll('.hole');
const scoreBoard = document.querySelector('.score');
const moles = document.querySelectorAll('.mole');
let highScore = document.querySelector('.highScore');
let timerDisplay = document.querySelector('.timerDisplay');
let gameTime = 10000;
let bestScoreData;
highScore.textContent = window.localStorage.getItem('High Score')

let lastHole;
let timeUp = false;
let score = 0;

function randomTime(min, max) {
  return Math.round(Math.random() * (max - min) + min);

}

function randomHole(holes) {
  const idx = Math.floor(Math.random() * holes.length);
  const hole = holes[idx];
  if(hole === lastHole) {
    return randomHole(holes);
  }

  lastHole = hole;
  return hole;
}

function peep() {
  const time = randomTime(500, 1000);
  const hole = randomHole(holes);
  countDownTimer(gameTime);
  hole.classList.add('up');
  setTimeout(() => {
    gameTime --;
    hole.classList.remove('up');
    if(!timeUp) peep();

  }, time);

}

function startGame() {
  scoreBoard.textContent = 0;
  highScore.textContent = 0;
  timeUp = false;
  score = 0;
  peep();
  setTimeout(() => timeUp = true, gameTime);
}

function bonk(e) {
  if(!e.isTrusted) return;
  score++;
  this.classList.remove('up');
  scoreBoard.textContent = score;
  high_score(score);
}

function high_score(score) {
  //if scoreBoard text content is > highScore... make highScore == scoreBoard
  if(score > highScore.textContent) {
    highScore.textContent = score;
    bestScoreData = window.localStorage.setItem('High Score', score.toString());
  }
  //save highScore locally to remain if user returns
}

function countDownTimer(gameTime) {
  //timer textContent = time
  //publish countdown for player to see
  //change text color to red when < 10 seconds
  timerDisplay.textContent = gameTime;
  //convert to seconds/minutes
}

moles.forEach(mole => mole.addEventListener('click', bonk));
