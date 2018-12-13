const card_aspect_ratio = 13/7

const hopperPane = d3.select("#hopper-pane")
            .append("svg")
            .attr("width", 300)
            .attr("height", 800);


function hopperPaneUpdate() {
  const cardSelector = () => hopperPane.selectAll(".stack-card")

  const cards = cardSelector().data(stack)

  const minicard_width = 280
  const minicard_height = 40

  const minicard = cards.enter()
        .append("g")
        .attr("transform", function(d, i) { return "translate(10," + (10+i*1.2*minicard_height) + ")"; })
        .attr("class", "stack-card")

  minicard
    .append("rect")

  minicard
    .append("text")

  const minicard_update = minicard.merge(cardSelector())

  minicard_update.select("rect").attr("fill", "white")
    .attr("stroke", (d, i) => "black")
    .style("stroke-dasharray", ("1, 1"))
    .attr("width", (d, i) => minicard_width)
    .attr("height", (d, i) => minicard_height)


  minicard_update.select("text")
    .text((d, i) => {/*console.log("cardStr(i): ", i, d, cardStr(d));*/ return cardStr(d)})
    .attr("x", minicard_width * .15 )
    .attr("y", minicard_height * .8)
    .attr("fill", (d, i) => "black")
    .attr("font-family", "courier")
    .attr("font-size", "30px")

  minicard.on("click", function(b,i) {
    currentCard = b

    d3.select(this).select("text").attr("class", "selected-minicard");
    console.log("I just clicked this: ", this)

    console.log("clicked stack card: ", i)

    update()
  })

  cards.exit().remove()
}
