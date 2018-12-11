buttonChars = () => buttonCols().map(buttonColToBCD)
buttonStr = () => buttonChars().join('')
function runFor() {
  console.log(buttonStr())
  $.post("https://cors-anywhere.herokuapp.com/rextester.com/l/fortran_online_compiler",
    "LanguageChoiceWrapper=45&EditorChoiceWrapper=1&LayoutChoiceWrapper=1&Program=!gfortran%2C+gcc+version+5.4.0+20160609%0D%0A%0D%0Aprogram+hello%0D%0A++++print+*%2C+%22Hello+World!%22%0D%0Aend+program+hello&Input=&ShowWarnings=false&Privacy=&PrivacyUsers=&Title=&SavedOutput=&WholeError=&WholeWarning=&StatsToSave=&CodeGuid=&IsInEditMode=False&IsLive=False",
          console.log)
}


function ajaxCallback(x) {
  con
}

//  $.post("https://cors-anywhere.herokuapp.com/www.jdoodle.com/api/execute",
//    {"script":"program sum\\n    REAL X,Y,Z\\n    X = 10\\n    Y= 25\\n    Z = X + Y\\n    PRINT *,\\\"sum of x + y = \\\", Z\\nend program sum\\n",
//           "args":"",
//           "stdin":"",
//           "language":"fortran",
//           "libs":"[]",
//     "versionIndex":"2"},
//          console.log)

//  $.post("https://cors-anywhere.herokuapp.com/www.tutorialspoint.com/compile_fortran_online.php",
//    "lang=fortran&device=&code=program+hello%0D%0A+++Print+*%2C+%22Hello+World!%22%0D%0Aend+program+Hello&stdinput=&ext=f95&compile=gfortran+-std%3Df95+*.f95+-o+main&execute=main&mainfile=main.f95&uid=8136047",
//          console.log)
