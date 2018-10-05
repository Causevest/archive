/* Handles all the events of index.html page */
/* Remove the style active from all the buttons and add the same to required button */
function resetActiveClass(evt) {
	var btns = document.getElementsByClassName("btn");
	var i;
	for(i = 0; i < btns.length; i++) {
		btns[i].className = btns[i].className.replace(" active", "");
	}
	evt.currentTarget.className += " active";
}
/* Tabbed control of the web-page */
function openDiv(evt, divName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    
    document.getElementById(divName).style.display = "flex";
    if(divName == 'transaction-division' )
    	document.getElementById(divName).style.display = "block";
    evt.currentTarget.className += " active";
}

/* Version Handling */
function getVersion(evt) {
	console.debug("Get tinycoin version");
	resetActiveClass(evt);

	var id = document.getElementById("version");
	perform("version", id)
}

/* Miner Address Handling */
var currtxnid="";
function getMiner(evt) {
	console.debug("Get Miner Address");
	resetActiveClass(evt);

	var id = document.getElementById("miner");
	console.debug("Displayed Miner Address: "+id.value);
	perform("get_miner_address", id)
}

function updateMiner(evt) {
	console.debug("Update Miner Address");
	resetActiveClass(evt);

	var id = document.getElementById("miner");
	console.debug("Displayed Miner Address: "+id.value);

	var data = {}
	data['miner_address'] = id.value;
	perform("update_miner_address", id, JSON.stringify(data))
}

/* Peers Handling */
function getPeers(evt) {
	console.debug("Get peers");
	resetActiveClass(evt);

	var id = document.getElementById("peers")
	perform("peers", id)
}

function addPeers(evt) {
	console.debug("Add peers");
	resetActiveClass(evt);

	var results = document.getElementById("results")
	var peers = document.getElementById("peers")
	var input = document.getElementById("peerinput")
	var peerlist = input.value;

	var data = peerList(peerlist)
	perform("add_peers", results, data)
}

function appPeers(evt) {
	console.debug("Append peers")
	resetActiveClass(evt);

	var results = document.getElementById("results")
	var peers = document.getElementById("peers")
	var input = document.getElementById("peerinput")
	var peerlist = input.value;

	var data = peerList(peerlist);
	perform("append_peers", results, data)
}

function detectPeers(evt) {
	console.debug("Detect peers");
	resetActiveClass(evt);

	var peers = document.getElementById("peers")
	var input = document.getElementById("peerinput")
	var data = {}
	var results = document.getElementById("results")
	results.value = "Work in progress !!!"
	results.style.color = "grey"
	results.style.font = "bold"
}

/* Transaction */
function transaction(evt) {
	console.debug("Perform transaction");
	resetActiveClass(evt);

	var src = document.getElementById("from")
	var tgt = document.getElementById("to")
	var amt = document.getElementById("amount")
	var results = document.getElementById("results")
	var mineraddr = document.getElementById("miner").value;

	var data = {}
	data['from'] = src.value;
	data['to'] = tgt.value;
	data['amount'] = parseInt(amt.value);
	data['timestamp'] = generateTimeStamp();
	if(currtxnid.length == 0)
		currtxnid = mineraddr;
	data['txnid'] = generateTxnid(mineraddr, currtxnid);
	data['signature'] = generateTxnSignature(mineraddr);

	perform("transaction", results, JSON.stringify(data))
}

/* Other operations */
function mine(evt) {
	console.debug("Perform mine");
	resetActiveClass(evt);

	var results = document.getElementById("results")
	perform("mine", results)
}

function consensus(evt) {
	console.debug("Perform consensus");
	resetActiveClass(evt);

	var results = document.getElementById("results")
	perform("consensus", results)
}

function blocks(evt) {
	console.debug("Perform blocks");
	resetActiveClass(evt);

	var results = document.getElementById("results")
	perform("blocks", results)
}

function connect(evt) {
	console.debug("Perform connect");
	resetActiveClass(evt);

	var results = document.getElementById("results")
	perform("connect_to_peers_of_peers", results)
}

/* Results */
function clearResults(evt) {
	console.debug("Clear the results");
	resetActiveClass(evt);

	var results = document.getElementById("results");
	results.value = "";
}
