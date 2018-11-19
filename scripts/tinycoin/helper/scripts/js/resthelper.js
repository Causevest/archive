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
	/* Note these SN are not in sync with ReadMe.md file. These are just for counting purposes */
    /* SN */ //API,     [API Name, REST method, content-type, html id, next-operation]
	/* 01 */ "version": ["version", "get", "text", "version", ""],												

	/* 02 */ "get_miner_address": ["get_miner_address", "get", "text", "miner", ""],
	/* 03 */ "update_miner_address": ["update_miner_address", "post", "json", "miner", "get_miner_address"],
	/* 04 */ "all_miner_address": ["all_miner_address", "get", "json", "miner", "get_miner_address"],
	
	/* 05 */ "add_peers": ["add_peers", "post", "json", "peers", "connect_to_peers_of_peers"],
	/* 06 */ "append_peers": ["append_peers", "post", "json", "peers", "connect_to_peers_of_peers"],
	/* 07 */ "peer_addresses": ["peer_addresses", "get", "json", "results", ""],

	/* 08 */ "peers": ["peers", "get", "text", "peers", ""],
	/* 09 */ "connect_to_peers_of_peers": ["connect_to_peers_of_peers", "get", "text", "peers", ""],

	/* 10 */ "transaction": ["transaction", "post", "json", "", ""],

	/* 11 */ "coins": ["coins", "get", "json", "", ""], // v1.8

	/* 12 */ "mine": ["mine", "get", "text", "results", ""],
	/* 13 */ "blocks": ["blocks", "get", "text", "results", ""],
	/* 14 */ "consensus": ["consensus", "get", "text", "", ""],
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
	var url;
	if(serveraddress.trim().length > 0) {
		return serveraddress;
	}
	url = document.getElementById("url").value.trim();
	console.debug("URL Address: "+url);
	if(!url.startsWith('http://') && !url.startsWith('https://'))
		url = 'http://'+url;
	serveraddress = url;
	return url;
}
function makeUrl(api) {
	var u = getUrl();
	if(!u.endsWith('/'))
		u += "/";
	u += api;
	return u;
}

function processRq(rq,id,nxtopn) {
	
	fetch(rq)
	.then(function(rs) {
		if(!rs.clone().ok) {
			throw Error(rs.statusText);
		}
		return rs.clone().json();
	})
	.catch(function(err){ 
		results.value = makeResString("Error occured: "+err);
		results.style.color = 'red';
		results.style.font = '1em bold';
	})
	.then(function(rsp) {
		console.debug(rsp);
		if(id != null) {
			if(typeof(rsp['data']) == 'object'){
				id.value = Object.entries(rsp['data'])
			}
			else {
				id.value = rsp['data'];
			}
		}

		displayCoins(rsp['from']);
		results.value = makeResString(rsp['text']);
		results.style.color = 'green';
		results.style.font = '1em bold';
		if(nxtopn != '') {
			console.debug(nxtopn)
			perform(nxtopn,'')
		}
	})
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
