
document.getElementById("id_icon_color").onchange = (event) => {
  var selectedColor = event.target.options[event.target.selectedIndex].dataset.color;
  document.getElementById("modalFormContainer").style.backgroundColor = selectedColor;
};
