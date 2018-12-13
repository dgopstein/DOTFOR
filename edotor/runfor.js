const utf8decoder = new TextDecoder("utf-8")

const responseText = response =>
      response.body.getReader().read().then(x => x.value).then(x=>utf8decoder.decode(x))

const responseJson = response =>
      responseText(response).then(JSON.parse)

function runSrc(src) {
  const encodedSrc = encodeURIComponent(src)
  //console.log("encodedSrc: ", encodedSrc)
  return fetch("https://cors-anywhere.herokuapp.com/https://rextester.com/rundotnet/Run",
        {"credentials":"omit",
         "headers":
         {"accept":"text/plain, */*; q=0.01",
          "accept-language":"en-US,en;q=0.9",
          "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
          "x-requested-with":"XMLHttpRequest"
         },
         "referrer":"https://rextester.com/l/fortran_online_compiler",
         "referrerPolicy":"no-referrer-when-downgrade",
         "body":"LanguageChoiceWrapper=45&EditorChoiceWrapper=1&LayoutChoiceWrapper=1&Program=!gfortran%2C+gcc+version+5.4.0+20160609%0D%0A%0D%0A"+encodedSrc+"&Input=&ShowWarnings=false&Privacy=&PrivacyUsers=&Title=&SavedOutput=&WholeError=&WholeWarning=&StatsToSave=&CodeGuid=&IsInEditMode=False&IsLive=False",
         "method":"POST",
         "mode":"cors"}).then(responseJson)
}

function runDeckAndDisplay() {
  const src = deckStr()
  runSrc(src).then(displayResult)
}

var lastResult;
function displayResult(res) {
  lastResult = res;
  var displayText;
  if (res.Errors) {
    displayText = "There was an error parsing your code:<br /><pre>"+res.Errors+"</pre>"
  } else {
    displayText = "Result:<br /><pre>"+res.Result+"</pre>"
  }
  $('#result-pane').html(displayText)
}

////////////////////////////////////////////////////////////
//               Downloading/Saving Code
////////////////////////////////////////////////////////////

function uploadCode() {
  const file_input = $('#load-file-input')
  file_input.click()

  file_input.change(function (e) {
    const file = file_input.get(0).files[0]
    const fr = new FileReader()
    fr.onload = () => loadCode(fr.result)
    fr.readAsText(file)
  })
}

function loadCode(data)  {
  const lines = data.split("\n")
    .map(l => rpad_array(l.split(''), n_cols, ' ')
         .map(c => {
           const upchar = c.toUpperCase()
           const bcdChar = charToIntObj[c] ? c : '!'
           return bcdChar
         }))

  deck = lines
  currentCard = deck[0]
  update()
}

function saveCode() {
  const src = deckStr()
  download("dotfor.f", src)
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
