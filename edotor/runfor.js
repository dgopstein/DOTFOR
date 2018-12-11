buttonChars = () => buttonCols().map(buttonColToBCD)
buttonStr = () => buttonChars().join('')

// 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'

function runFor(source) {
  $.post("https://5b4zahz6d2.execute-api.us-east-1.amazonaws.com/prod/dotfor",
         {"source": source},
         runForResult)
}

function runForResult(res) {
  console.log(res)
}

//runFor("program hello\n   Print *, \"Hello nargs!\"\nend program Hello")
//runFor("program sum\n    REAL X,Y,Z\n    X = 10\n    Y= 25\n    Z = X + Y\n    PRINT *,\"sum of x + y = \", Z\nend program sum\n")
