$(document).ready(function () {
  $('.sidenav').sidenav();
  $('#modal1').modal();
  $('#modal2').modal();
  $('select').formSelect();
  $('.materialboxed').materialbox();
  $('.carousel').carousel();
});


window.onload = function () {
  var pathArray = window.location.pathname.split('/');
  var name = pathArray[pathArray.length-1]
}

function removeFlash() {
  const element = document.getElementById("flash-message");
  element.remove();
}

