// http://api.travelpayouts.com/v1/prices/monthly?currency=USD&origin=MOW&destination=HKT
// c4ae3203facd6e9ea55b3f7f3cf03cd6

let url = "http://api.travelpayouts.com/v1/prices/monthly"
var origin = "SYD"
var dest = "LAX"
var currency = "AUD"
var header = new Headers();
header.append('x-access-token', 'c4ae3203facd6e9ea55b3f7f3cf03cd6');


url += "?currency=" + currency + "&origin=" + origin + "&destination=" + dest
url = "https://api.travelpayouts.com/v1/prices/cheap?origin=MOW&destination=HKT"


/*const request = new Request(url);
request.headers = header;*/

var request = new Request(url);
var headers = new Headers();
headers.append('x-access-token', 'c4ae3203facd6e9ea55b3f7f3cf03cd6');
headers.append("Access-Control-Allow-Headers","*");
request.headers = headers

console.log(request.headers)



fetch(request)
	.then(response => {
		if (response.status == 200) {
			console.log("hi yeet")
			return response.json();
		} else {
			console.log("nope")
		}

	})