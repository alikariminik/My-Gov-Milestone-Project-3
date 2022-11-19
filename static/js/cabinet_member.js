const getSynopsisUrl = (memberId) => `https://members-api.parliament.uk/api/Members/${memberId}/Synopsis`
const getVotingUrl = (memberId) => `https://members-api.parliament.uk/api/Members/${memberId}/Voting?house=1`
const getMemberUrl = (name) => `https://members-api.parliament.uk/api/Members/Search?Name=${name}&skip=0&take=20`
const getPhotoUrl = (memberId) => `https://members-api.parliament.uk/api/Members/${memberId}/ThumbnailUrl
`

const getParliamentMemberId = (name) => {
    return new Promise((resolve, reject) => {
        fetch(getMemberUrl(name))
            .then((response) => response.json())
            .then((data) => {
                if (data && data.items && data.items.length > 0) {
                    resolve(data.items[0].value.id);
                }
            })
            .catch((err) => reject(err));
    });
}


const getPhoto = (memberId) => {
    return new Promise((resolve, reject) => {
        fetch(getPhotoUrl(memberId))
        .then((response) => response.json())
        .then((data) => {
            resolve(data.value)
        })
        .catch((err) => reject(err));
    });
}


const getSynopsis = (memberId) => {
    return new Promise((resolve, reject) => {
        fetch(getSynopsisUrl(memberId))
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            console.log(data.value);
            resolve(data.value);
        })
        .catch((err) => reject(err));
    });
}

const getVotes = (memberId) => {
    return new Promise((resolve, reject) => {
        fetch(getVotingUrl(memberId))
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            console.log(data.items.slice(0, 5));
            dogs = data.items.slice(0, 5);

            resolve(dogs.map(dog => ({ 
                inAffirmativeLobby: dog.value.inAffirmativeLobby,
                numberAgainst: dog.value.numberAgainst,
                numberInFavour: dog.value.numberInFavour,
                title: dog.value.title,
                })));
        })
        .catch((err) => reject(err));
    });
}


const covertInAffirmativeLobby = (inAffirmativeLobby) => inAffirmativeLobby ? "Aye": "No";

function parliamentAPI(name) {
    
    getParliamentMemberId(name)
        .then((memberId) => {
            getSynopsis(memberId).then(synopsis => {
                synopsisElement = document.getElementById("synopsis");
                synopsisElement.innerHTML = `<h5>Profile</h5><br>${synopsis}`;
            });
            getVotes(memberId).then(votes => {
                console.log(votes)
                votes.forEach(function(vote) {
                    var li = document.createElement("li");
                    var text = document.createTextNode( 
                        `${vote.title}: ${covertInAffirmativeLobby(vote.inAffirmativeLobby)} (For: ${vote.numberInFavour} vs Against: ${vote.numberAgainst}) `);
                    li.appendChild(text);
                    document.getElementById("votes").appendChild(li);
                  });
            });
            getPhoto(memberId).then(photo => {
                photoElement = document.getElementById("cabphoto");
                photoElement.src = photo;
            });
        })
        .catch((err) => {
            console.error(err);
        })
  };

var pathArray = window.location.pathname.split('/');
var name = pathArray[pathArray.length-1];
if (name == "David%20T%20C%20Davies") {
    name= "David%20T%20C"
    parliamentAPI(name)
  } else {
    parliamentAPI(name)
  }
