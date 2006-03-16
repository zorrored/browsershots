function step(img, width, height, margin, zIndex) {
  img.style.width=width;
  img.style.height=height;
  img.style.margin=margin;
  img.style.zIndex=zIndex;
}

function scheduleStep(img, width, height, i, delay) {
  width=width*(10+i)/20+'px';
  height=height*(10+i)/20+'px';
  margin=(-i)+'px '+(-30-3*i)+'px 0 0';
  zIndex=i;
  setTimeout(function() { step(img, width, height, margin, zIndex) }, delay);
}

function larger(img, width, height) {
  img.dir='rtl';
  setTimeout(function() { if (img.dir=='rtl') step(img, width*0.55+'px', height*0.55+'px', '-1px -33px 0 0', 1) }, 20);
  setTimeout(function() { if (img.dir=='rtl') step(img, width*0.60+'px', height*0.60+'px', '-2px -36px 0 0', 2) }, 40);
  setTimeout(function() { if (img.dir=='rtl') step(img, width*0.65+'px', height*0.65+'px', '-3px -39px 0 0', 3) }, 60);
  setTimeout(function() { if (img.dir=='rtl') step(img, width*0.70+'px', height*0.70+'px', '-4px -42px 0 0', 4) }, 80);
  setTimeout(function() { if (img.dir=='rtl') step(img, width*0.75+'px', height*0.75+'px', '-5px -45px 0 0', 5) }, 100);
  setTimeout(function() { if (img.dir=='rtl') step(img, width*0.80+'px', height*0.80+'px', '-6px -48px 0 0', 6) }, 120);
  setTimeout(function() { if (img.dir=='rtl') step(img, width*0.85+'px', height*0.85+'px', '-7px -51px 0 0', 7) }, 140);
  setTimeout(function() { if (img.dir=='rtl') step(img, width*0.90+'px', height*0.90+'px', '-8px -54px 0 0', 8) }, 160);
  setTimeout(function() { if (img.dir=='rtl') step(img, width*0.95+'px', height*0.95+'px', '-9px -57px 0 0', 9) }, 180);
  setTimeout(function() { if (img.dir=='rtl') step(img, width+'px',      height+'px',    '-10px -60px 0 0', 10) }, 200);
}

function smaller(img, width, height) {
  img.dir='ltr';
  setTimeout(function() { if (img.dir=='ltr') step(img, width*0.95+'px', height*0.95+'px', '-9px -57px 0 0', 9) }, 20);
  setTimeout(function() { if (img.dir=='ltr') step(img, width*0.90+'px', height*0.90+'px', '-8px -54px 0 0', 8) }, 40);
  setTimeout(function() { if (img.dir=='ltr') step(img, width*0.85+'px', height*0.85+'px', '-7px -51px 0 0', 7) }, 60);
  setTimeout(function() { if (img.dir=='ltr') step(img, width*0.80+'px', height*0.80+'px', '-6px -48px 0 0', 6) }, 80);
  setTimeout(function() { if (img.dir=='ltr') step(img, width*0.75+'px', height*0.75+'px', '-5px -45px 0 0', 5) }, 100);
  setTimeout(function() { if (img.dir=='ltr') step(img, width*0.70+'px', height*0.70+'px', '-4px -42px 0 0', 4) }, 120);
  setTimeout(function() { if (img.dir=='ltr') step(img, width*0.65+'px', height*0.65+'px', '-3px -39px 0 0', 3) }, 140);
  setTimeout(function() { if (img.dir=='ltr') step(img, width*0.60+'px', height*0.60+'px', '-2px -36px 0 0', 2) }, 160);
  setTimeout(function() { if (img.dir=='ltr') step(img, width*0.55+'px', height*0.55+'px', '-1px -33px 0 0', 1) }, 180);
  setTimeout(function() { if (img.dir=='ltr') step(img, width*0.50+'px', height*0.50+'px',    '0 -30px 0 0', 0) }, 200);
}
