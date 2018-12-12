const hopperPane = d3.select("#hopper-pane")
            .append("svg")
            .attr("width", 300)
            .attr("height", 800);


function hopperPaneUpdate() {
  const cardSelector = () => hopperPane.selectAll(".card")

  cardSelector().remove()

  const cards = cardSelector().data(stack)

  console.log(stack)

  cards.enter()
    .merge(cards)
    .append("rect")
    .attr("class", "stack-card")
    .attr("x", (d, i) => 20)
    .attr("y", (d, i) => i * 100)
    .attr("stroke", (d, i) => "green")
    .attr("width", (d, i) => 300)
    .attr("height", (d, i) => 100)

  cards.exit().remove()
}
