function step(img, width, height, margin) {
  img.style.width=width;
  img.style.height=height;
  img.style.margin=margin;
}

function larger(img, width, height) {
  img.style.zIndex = 2
  setTimeout(function() { step(img, width*1.1+'px', height*1.1+'px', '-1px -33px 0 0') }, 20);
  setTimeout(function() { step(img, width*1.2+'px', height*1.2+'px', '-2px -36px 0 0') }, 40);
  setTimeout(function() { step(img, width*1.3+'px', height*1.3+'px', '-3px -39px 0 0') }, 60);
  setTimeout(function() { step(img, width*1.4+'px', height*1.4+'px', '-4px -42px 0 0') }, 80);
  setTimeout(function() { step(img, width*1.5+'px', height*1.5+'px', '-5px -45px 0 0') }, 100);
  setTimeout(function() { step(img, width*1.6+'px', height*1.6+'px', '-6px -48px 0 0') }, 120);
  setTimeout(function() { step(img, width*1.7+'px', height*1.7+'px', '-7px -51px 0 0') }, 140);
  setTimeout(function() { step(img, width*1.8+'px', height*1.8+'px', '-8px -54px 0 0') }, 160);
  setTimeout(function() { step(img, width*1.9+'px', height*1.9+'px', '-9px -57px 0 0') }, 180);
  setTimeout(function() { step(img, width*2+'px',   height*2+'px',  '-10px -60px 0 0') }, 200);
}

function smaller(img, width, height) {
  img.style.zIndex = 1
  setTimeout(function() { step(img, width*1.9+'px', height*1.9+'px', '-9px -57px 0 0') }, 20);
  setTimeout(function() { step(img, width*1.8+'px', height*1.8+'px', '-8px -54px 0 0') }, 40);
  setTimeout(function() { step(img, width*1.7+'px', height*1.7+'px', '-7px -51px 0 0') }, 60);
  setTimeout(function() { step(img, width*1.6+'px', height*1.6+'px', '-6px -48px 0 0') }, 80);
  setTimeout(function() { step(img, width*1.5+'px', height*1.5+'px', '-5px -45px 0 0') }, 100);
  setTimeout(function() { step(img, width*1.4+'px', height*1.4+'px', '-4px -42px 0 0') }, 120);
  setTimeout(function() { step(img, width*1.3+'px', height*1.3+'px', '-3px -39px 0 0') }, 140);
  setTimeout(function() { step(img, width*1.2+'px', height*1.2+'px', '-2px -36px 0 0') }, 160);
  setTimeout(function() { step(img, width*1.1+'px', height*1.1+'px', '-1px -33px 0 0') }, 180);
  setTimeout(function() { step(img, width+'px',     height+'px',     '0 -30px 0 0') },    200);
}
