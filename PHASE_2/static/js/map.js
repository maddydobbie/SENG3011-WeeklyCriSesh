function initMap() {
  const myLatlng = { lat: -25.363, lng: 131.044 };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 4,
    center: myLatlng,
  });

  // Create geocoder
  const geocoder = new google.maps.Geocoder();

  // Create the initial InfoWindow.
  let infoWindow = new google.maps.InfoWindow({
    content: "Click your destination to see information on diseases and outbreaks.",
    position: myLatlng,
  });
  infoWindow.open(map);

  // Configure the click listener.
  map.addListener("click", (mapsMouseEvent) => {
    // Close the current InfoWindow.
    infoWindow.close();
    // Create a new InfoWindow.
    infoWindow = new google.maps.InfoWindow({
      position: mapsMouseEvent.latLng,
    });

    const latlng = {
      lat: parseFloat(mapsMouseEvent.latLng.toJSON().lat),
      lng: parseFloat(mapsMouseEvent.latLng.toJSON().lng),
    };
    
    // This converts the latitude/longitude information to country
    geocoder.geocode({ location: latlng }, (results, status) => {
      if (status === "OK") {
        if (results[results.length - 2]) {
          // Country cannot be accessed outisde of this listener, 
          // so maybe put the function for location input in here
          // or save to local storage and use it that way.
          country = results[results.length - 2].formatted_address;
          infoWindow.setContent(country);
          infoWindow.open(map);
          // put country selected into location input box
          document.getElementById('location').value=country;
        } else {
          window.alert("No results found");
        }
      } else {
        infoWindow.setContent("Not a country!");
        infoWindow.open(map);
      }
    });

  });
}
