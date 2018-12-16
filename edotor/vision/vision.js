function onOpenCvReady() {
  console.log("opencv ready")

}


let imgElement = document.getElementById('imageSrc');
let inputElement = document.getElementById('fileInput');

inputElement.onchange = function() {
  imgElement.src = URL.createObjectURL(event.target.files[0]);
};


imgElement.onload = function() {
  let image = cv.imread(imgElement);
  cv.imshow('imageCanvas', image);
  image.delete();
};

document.getElementById('circlesButton').onclick = function() {
    this.disabled = true;
    document.body.classList.add("loading");

  let srcMat = cv.imread('imageCanvas');
  //let srcMat = new cv.Mat();
  //cv.resize(origMat, srcMat, new cv.Size(0, 0), 1, 1, cv.INTER_LANCZOS4);
  let displayMat = srcMat.clone();
  let circlesMat = new cv.Mat();

  cv.cvtColor(srcMat, srcMat, cv.COLOR_RGB2HSV);
  let hsv_split = new cv.MatVector();
  cv.split(srcMat, hsv_split)

  let satMat = hsv_split.get(1)

  cv.imshow('grayCanvas', satMat);


  console.log("starting hough")
  cv.HoughCircles(satMat, circlesMat, cv.HOUGH_GRADIENT, /*dp*/1, /*minDist*/45,
                  /*param1*/75, /*param2*/2, /*minRadius*/0, /*maxRadius*/0);
  console.log("finished hough, ncircles: ", circlesMat.cols)

  for (let i = 0; i < circlesMat.cols; ++i) {
    let x = circlesMat.data32F[i * 3];
    let y = circlesMat.data32F[i * 3 + 1];
    let radius = circlesMat.data32F[i * 3 + 2];

    let center = new cv.Point(x, y);
    cv.circle(displayMat, center, radius, [0, 0, 0, 255], 3);
  }

  cv.imshow('imageCanvas', displayMat);

  srcMat.delete();
  displayMat.delete();
  circlesMat.delete();

  console.log("done finding circles")

    this.disabled = false;
    document.body.classList.remove("loading");
};
