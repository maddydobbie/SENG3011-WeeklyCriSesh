//src="https://maps.googleapis.com/maps/api/js?libraries=places&key=AIzaSyCWeQqmIBeMj0-HG79MNSNZe8Uxogxx8f4"
var map;
var infoWindow;

var request;
var service;
var markers = [];
var dest = null;
var result = null;
function initMap() {
    // get destination from html
    dest = document.getElementById("mydiv").dataset.geocode;
    console.log(dest)
    // find latitude and 
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode( { 'address': dest}, function(results, status) {
    if (status == 'OK') {
        console.log(status)
        result = results[0].geometry.location
        console.log(result)
        //map.setCenter(results[0].geometry.location);
        //var marker = new google.maps.Marker({
        //    map: map,
        //    position: results[0].geometry.location
       // });
    } else {
        alert('Geocode was not successful for the following reason: ' + status);
        console.log('Geocode was not successful for the following reason: ' + status)
    }
    });
    //var center = new google.maps.LatLng(-33.917347, 151.2290788);
    //if (result != null) {
        var center = new google.maps.LatLng(result);
    //}
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
            console.log(results[i])
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