const card_aspect_ratio = 13/7

const hopperPane = d3.select("#deck-container")

function hopperPaneUpdate() {
  const cardSelector = () => hopperPane.selectAll(".deck-card")

  const cards = cardSelector().data(deck, c => c.join(''))

  const minicard = cards.enter()
        .append("div")
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
