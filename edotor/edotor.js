const [white, black, green, yellow, blue, red] =
      [d3.rgb(255, 255, 255),
       d3.rgb(0, 0, 0),
       d3.rgb(185, 217, 45),
       d3.rgb(242, 213, 84),
       d3.rgb( 45, 192, 230),
       d3.rgb(227,  38, 38)];

const n_rows = 6
const n_cols = 12

const buttons =
      _.flatMap(_.range(n_cols), col =>
                _.range(n_rows).map(row =>
                                    ({col: col,
                                      row: row,
                                      eaten: false})));

const buttonSize = 15;
const buttonMargin = 50;


const buttonColor = button => {
  if (button.eaten) {
    return white;
  } else {
    const colors = [green, yellow, blue, red];

    return colors[_.floor(button.col/3)];
  }
}

const colY = row_idx => (row_idx+1)*buttonMargin;
const buttonX = b => (b.col+1)*buttonMargin
const buttonY = b => colY(b.row)

//////////////////////////////////////////////////////////////
//                         BCD Card
//////////////////////////////////////////////////////////////

const buttonCols = () =>
      _.map(_.groupBy(buttons, b => b.col), (v, k) => v)
      .map(col => _.sortBy(col, b => b.row))


const gbcd =
['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '[', '#', '@', ':', '>', '?',
 ' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', '&', '.', ']', '(', '<', '\\',
 '^', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', '-', '$', '*', ')', ';', "'",
 '+', '/', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_', ',', '%', '=', '"', '!']
const bcd = gbcd

const buttonToInt = b => (b.eaten ? 0 : 1) * Math.pow(2, b.row)
const buttonColToInt = buttonCol => _.sum(buttonCol.map(buttonToInt))
const buttonColToBCD = buttonCol => bcd[buttonColToInt(buttonCol)]

const buttonCard = d3.select("#button-card")
            .append("svg")
            .attr("width", 651)
            .attr("height", 350);

const bcdCard = d3.select("#bcd-card")
            .append("svg")
            .attr("width", 651)
            .attr("height", 105);

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

  const chars = charSelector().data(buttonCols)

  chars.enter()
    .merge(chars)
    .append("text")
    .attr("class", "char")
    .attr("x", (d, i) => colY(i))
    .attr("y", 27)
    .text(b => //(buttonColToInt(b).toString().padStart(2, " ") + " => " +
                buttonColToBCD(b))
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
