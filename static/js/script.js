$(document).ready(function () {
  $('.sidenav').sidenav();
  $('#modal1').modal();
  $('select').formSelect();
  $('.materialboxed').materialbox();
});


window.onload = function () {
  var pathArray = window.location.pathname.split('/');
  var name = pathArray[pathArray.length-1]
  // lauchTest.addEventListener("click", parliamentAPI(name))
  parliamentAPI(name)
}


function parliamentAPI(name) {
  const url = `https://members-api.parliament.uk/api/Members/Search?Name=${name}&skip=0&take=20`

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      // console.log(data);
      //console.log(data.items[0].value.id);
    
    const memberId = data.items[0].value.id

const url2 = `https://members-api.parliament.uk/api/Members/${memberId}/Synopsis`

  fetch(url2)
    .then((response) => response.json())
    .then((data) => {
        console.log(data)
        console.log(data.value);
        const memberSynopsis = data.value

const url3 = `https://members-api.parliament.uk/api/Members/${memberId}/Voting?house=1`

  fetch(url3)
    .then((response) => response.json())
    .then((data) => {
        console.log(data)
        console.log(data.items.slice(0, 3));
        dogs = data.items.slice(0, 3)
        for dog in dogs
        const memberVotes = data.value});
    
let synopsis = document.getElementById("synopsis");
synopsis.innerHTML = `${memberSynopsis}`});

let votes = document.getElementById("votes");
votes.innerHTML = `${memberVotes}`});
};
