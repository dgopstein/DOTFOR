const card_aspect_ratio = 13/7

const hopperPane = d3.select("#hopper-pane")
            //.append("svg")
            //.attr("width", 300)
            //.attr("height", 800);


function hopperPaneUpdate() {
  const cardSelector = () => hopperPane.selectAll(".stack-card")

  const cards = cardSelector().data(stack, c => c.join(''))

  const minicard_width = 280
  const minicard_height = 40

  const minicard = cards.enter()
        .append("div")
        .attr("class", "stack-card")

  cards.exit().remove()

  minicard
    .append("text")
    .attr("class", "stack-text")

  const minicard_update = cards.enter().merge(cards)

  const minicard_text = minicard_update.selectAll(".stack-text")
        .text((d, i) => cardStr(d))
        .classed("selected-minicard", b => b == currentCard)
        .style("text-align", "center")
        .style("font-family", "courier")
        .style("font-size", "22px")

  minicard_text.on("click", function(b,i) {
    currentCard = b

    update()
  })
}
