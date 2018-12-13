const [white, black, green, yellow, blue, red] =
      [d3.rgb(255, 255, 255),
       d3.rgb(0, 0, 0),
       d3.rgb(185, 217, 45),
       d3.rgb(242, 213, 84),
       d3.rgb( 45, 192, 230),
       d3.rgb(227,  38, 38)];

const n_rows = 6
const n_cols = 12

//const newCard = () =>
//      _.flatMap(_.range(n_cols), col =>
//                _.range(n_rows).map(row =>
//                                    ({col: col,
//                                      row: row,
//                                      eaten: false})));

// https://stackoverflow.com/questions/8405453/is-there-a-shortcut-to-create-padded-array-in-javascript
const rpad_array = (arr,len,fill) =>
  arr.concat(Array(len).fill(fill)).slice(0,len);

const lpad_array = (arr,len,fill) =>
      Array(len - arr.length).fill(fill).concat(arr)

const newCard = () => _.range(n_cols).map(() => "!")

var currentCard = newCard()

var deck = [currentCard]

function mutateCurrentCard(newCard) {
  const currentIdx = deck.indexOf(currentCard)
  currentCard = newCard
  deck[currentIdx] = currentCard
}


function addCard() {
  currentCard = newCard()
  deck.push(currentCard)
  update()
}

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

const colX = row_idx => (row_idx+1)*buttonMargin;
const buttonX = b => colX(b.col)
const buttonY = b => (b.row+1)*buttonMargin

//////////////////////////////////////////////////////////////
//                         BCD Pane
//////////////////////////////////////////////////////////////

const gbcd =
['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '[', '#', '@', ':', '>', '?',
 ' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', '&', '.', ']', '(', '<', '\\',
 '^', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', '-', '$', '*', ')', ';', "'",
 '+', '/', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_', ',', '%', '=', '"', '!']
const bcd = gbcd
const charToIntObj = _.mapValues(_.invert(bcd), x => parseInt(x))

const buttonColToBCD = buttonCol => {
  const intVal = _.sum(buttonCol.map(b => (b.eaten ? 0 : 1) * Math.pow(2, b.row)))
  return bcd[intVal]
}

const buttonCols = card =>
      _.map(_.groupBy(card, b => b.col), (v, k) => v)
      .map(col => _.sortBy(col, b => b.row))

const buttonChars = card => buttonCols(card).map(buttonColToBCD)
const buttonStr = card => buttonChars(card).join('')


const cardStr = card => card.join('')
const cardChars = card => card
const deckStr = () => deck.map(cardStr).join("\n")

const charToInt = x => charToIntObj[x.toUpperCase()]
const intToBin = x => lpad_array(x.toString(2).split('').map(c => parseInt(c)), n_rows, 0)
const charToBin = c => intToBin(charToInt(c))
const cardBinMatrix = card => cardChars(card).map(charToBin)
const cardButtons = card => _.sortBy(cardBinMatrix(card).flatMap(
  (col, x) => col.map(
    (bin_val, y) => {return{
      col: x,
      row: (n_rows-1) - y,
      eaten: 0 == bin_val}
                    })), ['col', 'row'])

const cardPane = d3.select("#card-pane")
            .append("svg")
            .attr("width", 651)
            .attr("height", 350);

const bcdPane = d3.select("#bcd-pane")
            .append("svg")
            .attr("width", 651)
            .attr("height", 105);

function cardPaneUpdate() {
  const selectDots = () => cardPane.selectAll(".dot")

  const currentCardButtons = cardButtons(currentCard)

  const dots = selectDots()
        .data(currentCardButtons)

  dots.enter()
    .append("circle")
    .merge(dots)
    .attr("class", "dot")
    .attr("cx",   buttonX)
    .attr("cy",   buttonY)
    .attr("r",    buttonSize)
    .style("fill", buttonColor)

  dots.exit().remove()

  selectDots().on("click", function(b, i) {
    b.eaten = !b.eaten

    const btnChrs = buttonChars(currentCardButtons)

    mutateCurrentCard(btnChrs)

    update()
  })
}

function bcdPaneUpdate() {
  const charSelector = () => bcdPane.selectAll(".char")

  charSelector().remove()

  const chars = charSelector().data(x => cardChars(currentCard))

  chars.enter()
    .merge(chars)
    .append("text")
    .attr("class", "char")
    .attr("x", (d, i) => colX(i))
    .attr("y", 27)
    .text(b => b)
    .attr("font-family", "courier")
    .attr("font-size", "20px")

  chars.exit().remove()
}

function update() {
  cardPaneUpdate();
  bcdPaneUpdate();
  hopperPaneUpdate()
}

///////////////////////////////////////////////////
update()
