const card_aspect_ratio = 13/7

const hopperPane = d3.select("#deck-container")

function hopperPaneUpdate() {
  const cardSelector = () => hopperPane.selectAll(".deck-card")

  const cards = cardSelector().data(deck, c => c.join(''))

  const minicard = cards.enter()
        .append("li")
        .attr("class", "deck-card")

  cards.exit().remove()

  minicard
    .append("text")
    .attr("class", "deck-text")

  const minicard_update = cards.enter().merge(cards)

  const minicard_text = minicard_update.selectAll(".deck-text")
        .text((d, i) => cardStr(d))
        .classed("selected-deck-card", b => b == currentCard)
        .style("font-family", "courier")
        .style("font-size", "22px")

  minicard_text.on("click", function(b,i) {
    currentCard = b

    update()
  })
}

const currentCardIdx = () => deck.indexOf(currentCard)

function nextCard() {
  currentCard = deck[_.min([currentCardIdx()+1, deck.length-1])]
  update()
}

function prevCard() {
  currentCard = deck[_.max([currentCardIdx()-1, 0])]
  update()
}

function addCard() {
  currentCard = newCard()
  deck.push(currentCard)
  update()
}

function removeCard() {
  if (deck.length > 1) {
    const oldIdx = currentCardIdx()
    deck = _.pull(deck, currentCard)
    currentCard = deck[_.min([oldIdx, deck.length])]
    update()
  }
}
