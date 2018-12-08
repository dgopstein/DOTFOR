var white, black, green, yellow, blue, red;

function setup() {
  createCanvas(400, 720);

  [white, black, green, yellow, blue, red] =
    [color(255, 255, 255),
     color(0, 0, 0),
     color(185, 217, 45),
     color(242, 213, 84),
     color( 45, 192, 230),
     color(227,  38, 38)];
}

const n_cols = 6
const n_rows = 12

const buttons = _.flatMap(_.range(n_rows), row =>
    _.range(n_cols).map(col =>
      ({row: row,
        col: col,
        eaten: false})));

const buttonColor = button => {

  const colors = [green, yellow, blue, red];

  return colors[_.floor(button.row/3)];
}

const buttonSize = 30;
const buttonMargin = 50;

function drawDot(x, y, clr) {
  fill(clr)
  strokeWeight(1)
  stroke(clr)
  ellipse(x, y, buttonSize, buttonSize)
}

const drawBlankDot = (x, y) => {
  fill(white)
  stroke(white)
  ellipse(x, y, buttonSize+1, buttonSize+1)
}

const buttonX = b => (b.col+1)*buttonMargin;
const buttonY = b => (b.row+1)*buttonMargin;

const drawButtons = () => {
  buttons.forEach(b => {
    if (b.eaten) {
      drawBlankDot(buttonX(b), buttonY(b))
    } else {
      drawDot(buttonX(b), buttonY(b), buttonColor(b))
    }});
}

const drawCard = () => {
  const min = _.minBy(buttons, b => b.row + b.col)
  const max = _.maxBy(buttons, b => b.row + b.col)

  stroke(black)
  strokeWeight(3)
  fill(white)
  rect(buttonX(min) - buttonMargin, buttonY(min) - buttonMargin,
       (n_cols+1)*buttonMargin, (n_rows+1)*buttonMargin)

  drawButtons()
}

function draw() {
  drawCard()
}

const buttonCollider = b => (m_x, m_y) =>
      dist(m_x, m_y, buttonX(b), buttonY(b)) < (buttonSize/2)

function mousePressed() {
  const clickedButton = _.find(buttons, b => buttonCollider(b)(mouseX, mouseY))

  if (clickedButton) {
    clickedButton.eaten = true;
  }
}
