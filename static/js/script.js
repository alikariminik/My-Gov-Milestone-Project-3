$(document).ready(function () {
  $('.sidenav').sidenav();
  $('#modal1').modal();
  $('select').formSelect();
  $('.materialboxed').materialbox();
});


window.onload = function () {
  var pathArray = window.location.pathname.split('/');
  var name = pathArray[pathArray.length-1]
}

function removeFlash() {
  const element = document.getElementById("flash-message");
  element.remove();
}

