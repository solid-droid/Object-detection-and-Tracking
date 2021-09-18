
let video;
let detector;
let detections = [];
let cap = true;
let prev_second = 0;
let current_second = 1;
let avgImg;
let M_IMG = new MarvinImage();

function setup() {
  createCanvas(2000, 1200);
  video = createVideo(['../Part1.mp4'],videoReady);
  video.hide();
}

function videoReady() {
  video.play();
  video.onended(()=>cap=false)
  detector = ml5.objectDetector('../yolo_model.json', modelReady);
}

function gotDetections(error, results) {
  if (error) {
    console.error(error);
  }
  detections = results;
  if(detections.length>0){
    console.log('per');
  } else {
    console.log('---')
  }

}

function modelReady() {
  detector.detect(video, gotDetections);
}

beginTimer = (time) => setTimeout(()=>{current_second+=1},time*1000);

let frameNo = 0;
function draw() {
  if(cap && current_second >= prev_second) {
    prev_second =current_second + 1;
    beginTimer(0.2);
    const img = video.get(0,0,video.width,video.height);  
    createSegments(img,video.width,video.height, 4, 2);
    for (let i = 0; i < detections.length; i += 1) {
      const object = detections[i];
      stroke(0, 255, 0);
      strokeWeight(4);
      noFill();
      rect(object.x, object.y, object.width, object.height);
      noStroke();
      fill(255);
      textSize(24);
      text(object.label, object.x + 10, object.y + 24);
    }
    detector?.detect(video, gotDetections);
  } 

}

createSegments = (img , width, height, colomns , rows) => {
  const cellWidth = width/colomns;
  const cellHeight = height/rows;
  const imgArr = [];
  for(let y =0; y<rows;++y){
    for(let x= 0; x < colomns; ++x){
      imgArr.push(img.get(x*cellWidth , y*cellHeight , cellWidth, cellHeight));
    }
  }
  let rowIndex = 0;
  let colIndex = 0;
  const maxCols = 4;
  imgArr.forEach((im, index) => {
    if(index >= maxCols * (rowIndex+1)){
      rowIndex++;
      colIndex = 0;
    }
    const _X = colIndex*cellWidth + colIndex*50;
    const _Y = rowIndex*cellHeight + rowIndex*50;
      image(im,  _X  , _Y );
    colIndex++;
  });
}

