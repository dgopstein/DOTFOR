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

  const colors = [green, yellow, blue, red];

  return colors[_.floor(button.row/3)];
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

const buttonToInt = b => (b.eaten ? 0 : 1) * (n_cols - b.col)
const buttonRowToInt = buttonRow => _.sum(buttonRow.map(buttonToInt))

const buttonCard = d3.select("#button-card")
            .append("svg")
            .attr("width", 350)
            .attr("height", 651);

const bcdCard = d3.select("#bcd-card")
            .append("svg")
            .attr("width", 100)
            .attr("height", 651);

function buttonCardUpdate() {
  const dots = buttonCard.selectAll(".dot")
        .data(buttons.filter(b => !b.eaten))

  dots.enter()
    .append("circle")
    .attr("cx",   buttonX)
    .attr("cy",   buttonY)
    .attr("r",    buttonSize)
    .style("fill", buttonColor);

  dots.exit().remove()

  dots.on("click", function(b) {
    b.eaten = !b.eaten

    // Make it invisible before removing
    if (b.eaten) {
      d3.select(this)
        .attr("r", buttonSize+1)
        .style("fill", "white")
    }

    update()
  })
}

function bcdCardUpdate() {
  const chars = bcdCard.selectAll(".char").data(buttonRows)

  chars.enter()
    .append("text")
    .merge(chars)
    .attr("x", 10)
    .attr("y", (d, i) => rowY(i))
    .text(buttonRowToInt)
    .attr("font-family", "sans-serif")
    .attr("font-size", "20px")

  chars.exit().remove()

}

function update() {
  buttonCardUpdate();

  bcdCardUpdate();
}

///////////////////////////////////////////////////
update()
