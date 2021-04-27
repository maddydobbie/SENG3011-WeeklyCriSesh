//src="https://maps.googleapis.com/maps/api/js?libraries=places&key=AIzaSyCWeQqmIBeMj0-HG79MNSNZe8Uxogxx8f4"
var map;
var infoWindow;

var request;
var service;
var markers = [];

function initMap() {
    var center = new google.maps.LatLng(-33.917347, 151.2290788);
    map = new google.maps.Map(document.getElementById('map'), {
        center: center,
        zoom: 15
    });

    request = {
        location: center,
        radius: 8000,
        types: ['lodging']
    };
    infoWindow = new google.maps.InfoWindow();

    service = new google.maps.places.PlacesService(map);
    service.nearbySearch(request, callback);

    google.maps.event.addListener(map, 'rightclick', function(event) {
    map.setCenter(event.LatLng)
    clearResults(markers)

    var request = {
        location: event.LatLng,
        radius: 8000,
        types: ['lodging']
    };
    service.nearbySearch(request, callback);
    })
}

function callback(results, status) {
    if(status == google.maps.places.PlacesServiceStatus.OK) {
        for (var i = 0; i < results.length; i++) {
            markers.push(createMarker(results[i]));
        }
    }
}

function createMarker(place) {
    var placeLoc = place.geometry.location;
    var marker = new google.maps.Marker({
    map: map,
    position: place.geometry.location
    });

    google.maps.event.addListener(marker, 'click', function() {
        infoWindow.setContent(place.name);
        infoWindow.open(map, this);
    });
    return marker;
}

function clearResults(markers) {
    for (var m in markers) {
    markers[m].setMap(null)
    }
    markers=[]
}
let submit = document.getElementById("submit")
//google.maps.event.addDomListener(submit, 'load', initMap);
submit.onclick = function() {
    initMap()
}