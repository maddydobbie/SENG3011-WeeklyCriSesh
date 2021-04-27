let submit = document.getElementById("submit")
//value = button.form.valueId.value;
submit.onclick = function() {
  // get rid of everything in the modal body
  const c = document.getElementById("modal-body")
  while(c.firstChild){
    c.removeChild(c.firstChild);
  }
  // add some text telling user we are searcing (maybe)
  let text = document.createTextNode("Searching...")
  c.appendChild(text)
  // take query params and make api call
  let keywords = document.getElementById("keywords").value
  var location = document.getElementById("location").value
  let start = document.getElementById("start").value + "T00:00:00"
  let end = document.getElementById("end").value + "T00:00:00"
  let toggle = document.getElementById("toggle")
  console.log(toggle.checked)
  // news api
  if (toggle.checked) {
    let api_key = "d9628b5beb2749218768167f98bc0819"
    // get country code
    if (location != "") {
      fetch("https://restcountries.eu/rest/v2/name/" + location)
      .then(resp=>{
        //console.log(resp.status)
        return resp.json();
      }).then(json=>{
        location = (json[0].alpha2Code.toLowerCase())
        console.log(location)
      })
    }
    // only allowing dates between now and a month ago
    var d1 = new Date();
    var y1= d1.getFullYear()// - 1; //remove - 1 later
    var m1 = d1.getMonth() + 1;
    var mnew = m1 - 1
    if(m1<10)
      m1="0"+m1;
    if(mnew<10)
      mnew="0"+mnew;
    var dt1 = d1.getDate();
    if(dt1<10)
      dt1 = "0"+dt1;
    var d2 = y1+"-"+m1+"-"+dt1; // end
    var d1 = y1+"-"+mnew+"-"+dt1; // start
    end = d2
    start = d1
    // the link at the beginning fixes cors problem with news api
    let url = "https://newsapi.org/v2/everything?"
    console.log(location)
    // no keywords - give them one
    if (keywords === "") {
      keywords = "outbreak"
    }
    if (keywords != "") {
      url += "q=" + keywords 
    } 
    /*
    TODO
    if (location != "") {
      url += "&country=" + location
    }*/
    url += "&language=en" + "&from=" + start + "&to=" + end + "&apiKey=" + api_key
    const request = new Request(url);
    fetch(request)
      .then(response => {
        console.log(response)
      if (response.status === 200) {
        console.log("hi")
        //console.log(response.json())
        console.log("hi")
        return response.json();
      }
      else {
        // no results!
        const c = document.getElementById("modal-body")
        let text = document.createTextNode("No search results for given parameters!")
        c.appendChild(text)
        throw new Error('Something went wrong on api server!');
      }
      }).then((json) => {
        console.log("h6767676i")
        console.log(json.articles[0])
        let i = 0
        const c = document.getElementById("modal-body")
        // clean up modal body again
        while(c.firstChild){
          c.removeChild(c.firstChild);
        }
        // for each article ... 
        while (json.articles[i]) {
          const article = document.createElement("div")
          if (i === 0) {
            //article.style.bordertopstyle = "2px solid black"; - correct practice - but doesnt work
            article.className += "article0 row"
          } else {
            article.className += "article row"
          }
          //article.setAttribute("class", "article");
          
          //article.setAttribute("class", "row");
          //article.setAttribute("style", "padding:10px");
          console.log(article.getAttribute("class"))
          c.appendChild(article)
          // image
          const imgdiv = document.createElement("div")
          imgdiv.setAttribute("class", "col-md-3");
          const img = document.createElement("img")
          img.src = json.articles[i].urlToImage;
          imgdiv.appendChild(img)
          article.appendChild(imgdiv)
          // title
          const textdiv = document.createElement("div")
          // not being used the next 3
          textdiv.setAttribute("style", "text-overflow:ellipsis");
          textdiv.setAttribute("style", "white-space: nowrap;");
          textdiv.setAttribute("style", "overflow: hidden");
          //textdiv.setAttribute("style", "height:100px");
          const link = document.createElement("a")
          link.setAttribute("style", "font-size:24px")
          link.setAttribute("target", "_blank")
          link.innerHTML = json.articles[i].title
          link.href = json.articles[i].url
          textdiv.appendChild(link)
          textdiv.appendChild(document.createElement("br"))
          // time
          const time = document.createElement("p")
          let clock = json.articles[i].publishedAt.split("T")
          let text1 = document.createTextNode("Posted " + clock[0])
          textdiv.appendChild(text1)
          // description
          const h5 = document.createElement("h5")
          // allowing around 4 lines of description before you get cut off
          //var maintext = json.articles[i].content.substr(0, 538) + " ... "
          var maintext = json.articles[i].description
          let text = document.createTextNode(maintext)
          h5.appendChild(text)
          textdiv.appendChild(h5)
          article.appendChild(textdiv)
          // source
          const source = document.createElement("p")
          source.innerHTML = "Source: " + json.articles[i].source.name
          textdiv.appendChild(source)
          i++;
        }
      })
      .then(response => {
        //console.debug(response);
      // ...
      }).catch(error => {
        console.error(error);
      })
    // our seng api
  } else {
    let url = "http://seng3011.pythonanywhere.com/articles?" + "startDate=" + start + "&endDate=" + end 
    if (keywords != "") {
      url += "&keywords=" + keywords 
    } 
    if (location != "") {
      url += "&location=" + location
    }
    const request = new Request(url);
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
        console.log(json[0])
        // console.log(json[5])
        
        // List of countries with articles on them
        for (let i = 0; i < json.length; i++) {
          for (let j = 0; j < json[i].reports.length; j++) {
            if (json[i].reports[j].locations.country.name) {
              console.log(json[i].reports[j].locations.country.name);
            } else if (json[i].reports[j].locations.country) {
              console.log(json[i].reports[j].locations.country);
            }
          }
        }
        let i = 0
        const c = document.getElementById("modal-body")
        // clean up modal body again
        while(c.firstChild){
          c.removeChild(c.firstChild);
        }
        // for each article ... 
        while (json[i]) {
          const article = document.createElement("div")
          //article.setAttribute("class", "article");
          //article.setAttribute("class", "row");
          // add classes. First article has top border, the rest do not
          if (i === 0) {
            //article.style.bordertopstyle = "2px solid black"; - correct practice - but doesnt work
            article.className += "article0 row"
          } else {
            article.className += "article row"
          }
          //article.setAttribute("style", "padding:10px");
          c.appendChild(article)
          // title
          const textdiv = document.createElement("div")
          // not being used the next 3
          textdiv.setAttribute("style", "text-overflow:ellipsis");
          textdiv.setAttribute("style", "white-space: nowrap;");
          textdiv.setAttribute("style", "overflow: hidden");
          //textdiv.setAttribute("style", "height:100px");
          const link = document.createElement("a")
          link.setAttribute("style", "font-size:30px")
          link.setAttribute("target", "_blank")
          link.innerHTML = json[i].headline
          link.href = json[i].url
          textdiv.appendChild(link)
          textdiv.appendChild(document.createElement("br"))
          // time
          const time = document.createElement("p")
          let clock = json[i].date_of_publication.split(" ")
          let text1 = document.createTextNode(clock[0])
          textdiv.appendChild(text1)
          // description
          const h5 = document.createElement("h5")
          // allowing around 4 lines of description before you get cut off
          var maintext = json[i].main_text.substr(0, 538) + " ... "
          let text = document.createTextNode(maintext)
          h5.appendChild(text)
          textdiv.appendChild(h5)
          article.appendChild(textdiv)
          // source
          const source = document.createElement("p")
          source.innerHTML = "Source: " + json[i].url
          textdiv.appendChild(source)
          i++;
        }
      })
      .then(response => {
        //console.debug(response);
      // ...
      }).catch(error => {
        console.error(error);
      })
  }
}
//$("#mymodal").modal()