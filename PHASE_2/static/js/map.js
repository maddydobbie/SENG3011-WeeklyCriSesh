function initMap() {
  const myLatlng = { lat: 33, lng: 81 };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 2,
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
            countries.push(json[i].reports[j].locations.country.name);
          } else if (json[i].reports[j].locations.country) {
            countries.push(json[i].reports[j].locations.country);
          }
        }
      }
      // console.log(countries)
      return countries;
    }).then(countries => {
      for (let c = 0; c < countries.length; c++) {
        if (countries[c] === 'Congo') {
          countries[c] = 'Democratic Republic of the Congo';
        }
        let country = countries[c].replace(/ /g,"+");
        let key = 'AIzaSyDd9bxIZ8hJ0jI9ia6vAcrhyFyF0cCi7-I';
        // console.log(country);
        let url2 = `https://maps.googleapis.com/maps/api/geocode/json?components=country:${country}&key=${key}`;
        fetch (new Request(url2))
        .then(response => {
          if (response.status === 200) {
            return response.json();
          }
        }).then((json) => {
          if (json.results[0]) {
            let coords = json.results[0].geometry.location;
            let img = {
              url: "https://img.icons8.com/fluent/48/000000/virus.png", // url
              // scaledSize: new google.maps.Size(50, 50), // scaled size
              origin: new google.maps.Point(0,0), // origin
              anchor: new google.maps.Point(0, 0) // anchor
            };
            let marker = new google.maps.Marker({
              position: coords,
              map,
              icon: img
            });
            marker.addListener('click', () => {
              document.getElementById('location').value=countries[c];
              document.getElementById("submit").click();
            });
          }
        })
      }
    })

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
