function multiCheck(prefix, checked) {
  var inputs=document.getElementsByTagName('input')
  for (var index=0; index<inputs.length; index++) {
    var checkbox=inputs[index];
    if (checkbox.name.indexOf(prefix)==0) checkbox.checked=checked;
  }
}

function updateMaster(prefix) {
  var master=prefix+'_all';
  var checked=true;
  var inputs=document.getElementsByTagName('input')
  for (var index=0; index<inputs.length; index++) {
    var checkbox=inputs[index];
    if (checkbox.name.indexOf(prefix)==0 && 
        checkbox.name!=master &&
        !checkbox.checked) {
      checked=false;
      break;
    }
  }
  document.getElementById(master).checked=checked;
}
