
function overlay(index) {
  var detailOverlay = document.getElementById(`overlay-${index}`);
  detailOverlay.style.visibility = (detailOverlay.style.visibility == "visible") ? "hidden" : "visible";
}

