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

	eraseResults();
	perform("version", '')
}

/* Miner Address Handling */
var currtxnid="";
function getMiner(evt) {
	console.debug("Get Miner Address");
	resetActiveClass(evt);

	var id = document.getElementById("miner");
	console.debug("Displayed Miner Address: "+id.value);

	eraseResults();
	perform("get_miner_address", '')
}

function updateMiner(evt) {
	console.debug("Update Miner Address");
	resetActiveClass(evt);

	var id = document.getElementById("miner");
	console.debug("Displayed Miner Address: "+id.value);

	var options = {};
	var data = {}
	data['miner_address'] = id.value;

	eraseResults();
	perform("update_miner_address", JSON.stringify(data))
}

/* Peers Handling */
function alignPeers(evt) {
	console.debug("Beautify peers");
	resetActiveClass(evt);
	var peers = document.getElementById("peers")
	if(peers.value.length <= 0)
		return;
	var peerlst = beautifyPeers(peers.value);
	peers.value = peerlst;
}

function getPeers(evt) {
	console.debug("Get peers");
	resetActiveClass(evt);

	eraseResults();
	perform("peers", '')
}

function addPeers(evt) {
	console.debug("Add peers");
	resetActiveClass(evt);

	var input = document.getElementById("peerinput")
	var peerlst = input.value;

	var data = peerList(peerlst)

	eraseResults();
	perform("add_peers", data)
}

function appPeers(evt) {
	console.debug("Append peers")
	resetActiveClass(evt);

	var input = document.getElementById("peerinput")
	var peerlst = input.value;

	var data = peerList(peerlst);
	eraseResults();	
	perform("append_peers", data)
}

function detectPeers(evt) {
	console.debug("Detect peers");
	resetActiveClass(evt);

	eraseResults();
	perform("connect_to_peers_of_peers", '')
}

function connect(evt) {
	console.debug("Perform connect");
	resetActiveClass(evt);

	eraseResults();
	perform("connect_to_peers_of_peers", '')
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

	eraseResults();
	perform("transaction", JSON.stringify(data))
}

/* Other operations */
function mine(evt) {
	console.debug("Perform mine");
	resetActiveClass(evt);

	eraseResults();
	perform("mine", '')
}

function consensus(evt) {
	console.debug("Perform consensus");
	resetActiveClass(evt);

	eraseResults();
	perform("consensus", '')
}

function blocks(evt) {
	console.debug("Perform blocks");
	resetActiveClass(evt);

	eraseResults();
	perform("blocks", '')
}

/* Results */
function clearResults(evt) {
	console.debug("Clear the results");
	resetActiveClass(evt);
	eraseResults();
}
function eraseResults() {
	var results = document.getElementById("results");
	results.value = "";
}