// Copyright (c) 2019 ml5
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

/* ===
ml5 Example
Real time Object Detection using objectDetector
=== */

let objectDetector;
let status;
let objects = [];
let video;
let canvas, ctx;
const width = '100%';
const height = 'auto';

// when the dom is loaded, call make();
window.addEventListener('DOMContentLoaded', async () => {
  video = document.getElementById('video');
  objectDetector = await ml5.objectDetector('../yolo_model.json', startDetecting)
});

function startDetecting(){
  console.log('model ready')
  video.play();
  detect();
}

function detect() {
  objectDetector.detect(video, function(err, results) {
    if(err){
      console.log(err);
      return
    }
    objects = results;

    if(objects.length>0){
      console.log(objects);
    }
    
    detect();
  });
}

