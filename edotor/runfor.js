cardChars = () => cardCols().map(cardColToBCD)
cardStr = () => cardChars().join('')

// 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'

function runFor(source) {
  const src = cardStr()
  $.post("https://5b4zahz6d2.execute-api.us-east-1.amazonaws.com/prod/dotfor",
         {"source": src},
         runForResult)
}

function runForResult(res) {
  console.log(res)
}

//runFor("program hello\n   Print *, \"Hello nargs!\"\nend program Hello")
//runFor("program sum\n    REAL X,Y,Z\n    X = 10\n    Y= 25\n    Z = X + Y\n    PRINT *,\"sum of x + y = \", Z\nend program sum\n")


function saveCode() {
  const src = cardStr()
  download("dotfor.f90", src)
}

function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}
