function initMap() {
  const myLatlng = { lat: -25.363, lng: 131.044 };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 4,
    center: myLatlng,
  });
  
  let start = document.getElementById("start").value + "T00:00:00"
  let end = document.getElementById("end").value + "T00:00:00"
  let keywords = document.getElementById("keywords").value
  var location = document.getElementById("location").value
  let url = "http://seng3011.pythonanywhere.com/articles?" + "startDate=" + start + "&endDate=" + end;
  if (keywords != "") {
    url += "&keywords=" + keywords 
  } 
  if (location != "") {
    url += "&location=" + location
  }

  const request = new Request(url);
  // use our api to get a list of reports from the past year
  fetch(request)
    .then(response => {
      console.log(response)
      if (response.status === 200) {
        //console.log(response.headers)
        return response.json();
      } else {
        // no results!
        const c = document.getElementById("modal-body")
        let text = document.createTextNode("No search results for given parameters!")
        c.appendChild(text)
        throw new Error('Something went wrong on api server!');
      }
    }).then((json) => {
      // console.log(json[0])
      // console.log(json[5])
      let countries = [];
      // List of countries with articles on them
      for (let i = 0; i < json.length; i++) {
        for (let j = 0; j < json[i].reports.length; j++) {
          if (json[i].reports[j].locations.country.name) {
            // console.log(json[i].reports[j].locations.country.name);
            countries.push(json[i].reports[j].locations.country.name);
          } else if (json[i].reports[j].locations.country) {
            // console.log(json[i].reports[j].locations.country);
            countries.push(json[i].reports[j].locations.country);
          }
        }
      }
      console.log(countries)
      return countries;
    }).then(countries => {
      for (let c = 0; c < countries.length; c++) {
        let country = countries[c].replace(/ /g,"+");
        let url2 = `https://maps.googleapis.com/maps/api/geocode/json?components=country:${country}&key=AIzaSyDd9bxIZ8hJ0jI9ia6vAcrhyFyF0cCi7-I`;
        // console.log(countries[c].replace(/ /g,"+"));
        fetch (new Request(url2))
        .then(response => {
          if (response.status === 200) {
            return response.json();
          }
        }).then((json) => {
          console.log(json.results);
          // console.log(json.results.geometry.location);
          // new google.maps.Marker({
          //   position: json.results.geometry.location,
          //   map,
          // });
        })
      }
    })
  // use the results to place markers on all countries with articles

  // fetch(new Request(url))


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
