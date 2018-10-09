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
	//API, [API Name, REST method, content-type, html id, next-operation]
	"version": ["version", "get", "text", "version", ""],
	"get_miner_address": ["get_miner_address", "get", "text", "miner", ""],
	"update_miner_address": ["update_miner_address", "post", "json", "miner", "get_miner_address"],
	"add_peers": ["add_peers", "post", "json", "peers", "connect_to_peers_of_peers"],
	"append_peers": ["append_peers", "post", "json", "peers", "connect_to_peers_of_peers"],
	"connect_to_peers_of_peers": ["connect_to_peers_of_peers", "get", "text", "peers", ""],
	"transaction": ["transaction", "post", "json", "", ""],
	"peers": ["peers", "get", "text", "peers", ""],
	"mine": ["mine", "get", "text", "", ""],
	"blocks": ["blocks", "get", "text", "", ""],
	"consensus": ["consensus", "get", "text", "", ""],
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

function processRq(rq,id,nxtopn) {
	
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
			results.value = makeResString("Error occured: "+err);
			results.style.color = 'red';
			results.style.font = '1em bold';
		})
		.then(function(rsp) {
			id.value = rsp;
			results.value = makeResString(rsp);
			results.style.color = 'green';
			results.style.font = '1em bold';
			if(nxtopn != '') {
				console.debug(nxtopn)
				perform(nxtopn,'')
			}
		})
	}
	catch(error) {
		results.value = makeResString("Error: "+error);
		results.style.color = 'red';
		results.style.font = '1em bold';
	}
}

function perform(api, data) {
	console.debug("perform");

	var rq;

	var apiinfo = TinycoinAPI[api];
	var apiname = apiinfo[0];
	var method = apiinfo[1];
	var type = apiinfo[2];
	var id = apiinfo[3];
	var nxtopn = apiinfo[4];

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
	var docid = document.getElementById(id);
	processRq(rq, docid, nxtopn)
}
