const [white, black, green, yellow, blue, red] =
      [d3.rgb(255, 255, 255),
       d3.rgb(0, 0, 0),
       d3.rgb(185, 217, 45),
       d3.rgb(242, 213, 84),
       d3.rgb( 45, 192, 230),
       d3.rgb(227,  38, 38)];

const n_cols = 6
const n_rows = 12

const buttons =
      _.flatMap(_.range(n_rows), row =>
                _.range(n_cols).map(col =>
                                    ({row: row,
                                      col: col,
                                      eaten: false})));

const buttonSize = 15;
const buttonMargin = 50;


const buttonColor = button => {
  if (button.eaten) {
    return white;
  } else {
    const colors = [green, yellow, blue, red];

    return colors[_.floor(button.row/3)];
  }
}

const rowY = row_idx => (row_idx+1)*buttonMargin;
const buttonX = b => (b.col+1)*buttonMargin
const buttonY = b => rowY(b.row)

//////////////////////////////////////////////////////////////
//                         BCD Card
//////////////////////////////////////////////////////////////

const buttonRows = () =>
      _.map(_.groupBy(buttons, b => b.row), (v, k) => v)
      .map(row => _.sortBy(row, b => b.col))


const gbcd =
['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '[', '#', '@', ':', '>', '?',
 'S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', '&', '.', ']', '(', '<', '\\',
 '^', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', '-', '$', '*', ')', ';', "'",
 '+', '/', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_', ',', '%', '=', '"', '!']
const bcd = gbcd

const buttonToInt = b => (b.eaten ? 0 : 1) * Math.pow(2, (n_cols-1) - b.col)
const buttonRowToInt = buttonRow => _.sum(buttonRow.map(buttonToInt))
const buttonRowToBCD = buttonRow => bcd[buttonRowToInt(buttonRow)]

const buttonCard = d3.select("#button-card")
            .append("svg")
            .attr("width", 350)
            .attr("height", 651);

const bcdCard = d3.select("#bcd-card")
            .append("svg")
            .attr("width", 105)
            .attr("height", 651);

//buttonCard.on("click", function(b) { console.log("button card clicked") })

function buttonCardUpdate() {
  const selectDots = () => buttonCard.selectAll(".dot")
  const dots = selectDots()
        .data(buttons)

  dots.enter()
    .append("circle")
    .merge(dots)
    .attr("class", "dot")
    .attr("cx",   buttonX)
    .attr("cy",   buttonY)
    .attr("r",    buttonSize)
    .style("fill", buttonColor)

  dots.exit().remove()

  selectDots().on("click", function(b) {
      b.eaten = !b.eaten

      update()
    })
}

function bcdCardUpdate() {
  const charSelector = () => bcdCard.selectAll(".char")

  charSelector().remove()

  const chars = charSelector().data(buttonRows)

  chars.enter()
    .merge(chars)
    .append("text")
    .attr("class", "char")
    .attr("x", 10)
    .attr("y", (d, i) => rowY(i))
    .text(b => (buttonRowToInt(b).toString().padStart(2, " ") +
                " => " + buttonRowToBCD(b)))
    .attr("font-family", "courier")
    .attr("font-size", "20px")

  chars.exit().remove()

}

function update() {
  buttonCardUpdate();

  bcdCardUpdate();
}

///////////////////////////////////////////////////
update()
