var white, black, green, yellow, blue, red;

const n_cols = 6
const n_rows = 12

const buttons =
      _.flatMap(_.range(n_rows), row =>
                _.range(n_cols).map(col =>
                                    ({row: row,
                                      col: col,
                                      eaten: false})));

const buttonMargin = 50;

const rowY = row_idx => (row_idx+1)*buttonMargin;

function buttonCard (p) {
  p.setup = () => {
    p.frameRate(10)
    p.createCanvas(400, 720);

    [white, black, green, yellow, blue, red] =
      [p.color(255, 255, 255),
       p.color(0, 0, 0),
       p.color(185, 217, 45),
       p.color(242, 213, 84),
       p.color( 45, 192, 230),
       p.color(227,  38, 38)];
  }

  p.buttons = buttons

  const buttonColor = button => {

    const colors = [green, yellow, blue, red];

    return colors[_.floor(button.row/3)];
  }

  const buttonSize = 30;

  function drawDot(x, y, clr) {
    p.fill(clr)
    p.strokeWeight(1)
    p.stroke(clr)
    p.ellipse(x, y, buttonSize, buttonSize)
  }

  const drawBlankDot = (x, y) => {
    p.fill(white)
    p.stroke(white)
    p.ellipse(x, y, buttonSize+1, buttonSize+1)
  }

  const buttonX = b => (b.col+1)*buttonMargin
  const buttonY = b => rowY(b.row+1)


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

    p.stroke(black)
    p.strokeWeight(3)
    p.fill(white)
    p.rect(buttonX(min) - buttonMargin, buttonY(min) - buttonMargin,
           (n_cols+1)*buttonMargin, (n_rows+1)*buttonMargin)

    drawButtons()
  }

  p.draw = () => {
    drawCard()
  }

  const buttonCollider = b => (m_x, m_y) =>
        p.dist(m_x, m_y, buttonX(b), buttonY(b)) < (buttonSize/2)

  p.mousePressed = () => {
    const clickedButton = _.find(buttons, b => buttonCollider(b)(p.mouseX, p.mouseY))

    if (clickedButton) {
      clickedButton.eaten = true;
    }
  }
}

var buttonCard_p5 = new p5(buttonCard, 'button-card');


//////////////////////////////////////////////////////////////
//                         BCD Card
//////////////////////////////////////////////////////////////

function bcdCard (p) {
  const buttons = buttonCard_p5.buttons

  const buttonRows = () =>
        _.map(_.groupBy(buttons, b => b.row), (v, k) => v)
         .map(row => _.sortBy(row, b => b.col))

  const buttonToInt = b => (b.eaten ? 0 : 1) * (n_cols - b.row)
  const buttonRowToInt = buttonRow => _.sum(buttonRow.map(buttonToInt))

  p.setup = () => {
    p.frameRate(10)
    p.createCanvas(400, 700);
  }

  p.draw = () => {
    p.fill(black)
    p.textSize(32);
    buttonRows().forEach((row, i) => p.text(buttonRowToInt(row).toString(), 0, rowY(i)))
  }

  p.mousePressed = () => {
    console.log("Mouse-Pressed 2")
    console.log(buttonRows())

  }
}

var bcdCard_p5 = new p5(bcdCard, 'bcd-card');
