/* Helper functions for the index.html event handlers defined in handlers.js */
// Global constants
blank = "&nbsp;";

// Results
pbegin = "<p>";
pend = "</p>"
EndSpan = "</span>"+pend;
GreySpan = pbegin+"<p><span style='color:grey'>";
GreenSpan = pbegin+"<span style='color:green'>";
RedSpan = pbegin+"<span style='color:red'>";

RqRsDataType = {
	"text": "text/plain; charset=utf-8",
	"html": "text/html; charset=utf-8",
	"json": "application/json; charset=utf-8"
}

TinycoinAPI = 
{
	//API, [API Name, REST method, content-type]
	"version": ["version", "get", "text"],
	"get_miner_address": ["get_miner_address", "get", "text"],
	"update_miner_address": ["update_miner_address", "post", "json"],
	"add_peers": ["add_peers", "post", "json"],
	"append_peers": ["append_peers", "post", "json"],
	"transaction": ["transaction", "post", "json"],
	"peers": ["peers", "get", "text"],
	"mine": ["mine", "get", "text"],
	"blocks": ["blocks", "get", "text"],
	"consensus": ["consensus", "get", "text"],
	"connect_to_peers_of_peers": ["connect_to_peers_of_peers", "get", "text"],
}

function makePostRq(url,headers,data) {
	var rq = new Request(url,{
		method: 'POST',
		mode: 'cors',
		headers: headers,
		body: data
	});
	return rq;
}
function makePostHeaders(acctp,conttp) {
	var hjson = {}
	hjson['Accept'] = RqRsDataType[acctp]
	hjson['Content-Type'] = RqRsDataType[conttp]
	hjson['Access-Control-Allow-Origin'] = '*'
	console.debug(JSON.stringify(hjson))
	var h = new Headers(hjson);
	return h;
}

function makeGetRq(url,headers) {
	var rq = new Request(url,{
		method: 'GET',
		mode: 'cors',
		headers: headers
	});
	return rq;
}
function makeGetHeaders(conttp) {
	var hjson = {}
	hjson['Content-Type'] = RqRsDataType[conttp]
	hjson['Access-Control-Allow-Origin'] = '*'
	var h = new Headers(hjson);
	return h;
}

function getUrl() {
	var url = document.getElementById("url").value;
	console.debug("URL Address: "+url);
	return url;
}
function makeUrl(api) {
	var u = getUrl()+"/"+api;
	return u;
}

function processRq(rq,id) {
	var results = document.getElementById("results");
	try {
		fetch(rq)
		.then(function(rs) {
			var type;
			console.debug(rs);
			console.debug(rs.headers);
			console.debug(rs.headers.has("Content-Type"));
			if(rs.headers.has("Content-Type")){
				var conttp = rs.headers.get("Content-Type")
				if(conttp.indexOf("text/html")>=0) {
					type = 'text';
				}
				else if(conttp.indexOf("text/plain")>=0) {
					type = 'text';
				}
				else if(conttp.indexOf("application/json")>=0) {
					type = 'json';
				}
			}
			
			if(!rs.ok) {
				throw Error(rs.statusText);				
			}
			if(type=='text') {
				return rs.text()
			}
			else if(type=='json') {
				return JSON.stringify(rs.json())
			}
			else {
				console.log('What type it is?')
			}
		})
		.catch(function(err){ 
			results.value = "Error occured: "+err;
			results.style.color = 'red';
			results.style.font = '1em bold';
		})
		.then(function(rsp) {
			id.value = rsp;
			results.value = rsp;
			results.style.color = 'green';
			results.style.font = '1em bold';
		})
	}
	catch(error) {
		results.value = "Error: "+error;
		results.style.color = 'red';
		results.style.font = '1em bold';
	}
}

function perform(api, id, data) {
	console.debug("perform")
	var rq;
	var apiinfo = TinycoinAPI[api];
	var apiname = apiinfo[0];
	var method = apiinfo[1];
	var type = apiinfo[2];
	
	var url = makeUrl(apiname);
	console.debug("URL:"+url);

	switch(method) {
		case 'get': {
			var headers = makeGetHeaders(type);
			rq = makeGetRq(url, headers);
		}
		break;
		case 'post': {
			console.debug(data)
			var headers = makePostHeaders(type,type);
			rq = makePostRq(url, headers, data)
		}
		break;
		default: {
			console.log("Coming Sooooooooooon ...");
			return;
		}
		break;
	}
	processRq(rq,id)
}
