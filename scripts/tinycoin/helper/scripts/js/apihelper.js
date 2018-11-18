/* Handles all the events of API calls in index.html page */
/* Globals */
var currtxnid="";
var serveraddress=" ";

/* Version Handling */
function getVersion(evt) {
	console.debug("Get tinycoin version");

	eraseResults();
	clrVersion(); // OK for now, if required send element Id to a general function
	perform("version", '')
}

/* Miner Address Handling */
function getMiner(evt) {
	console.debug("Get Miner Address");

	var id = document.getElementById("miner");
	console.debug("Displayed Miner Address: "+id.value);

	eraseResults();
	perform("get_miner_address", '')
}

function updateMiner(evt) {
	console.debug("Update Miner Address");

	var id = document.getElementById("miner");
	console.debug("Displayed Miner Address: "+id.value);

	var options = {};
	var data = {}
	data['miner_address'] = id.value;

	eraseResults();
	perform("update_miner_address", JSON.stringify(data))
}

function getAllMinerAddr(evt) {
	console.debug("Get All Miner Addresses");

	var id = document.getElementById("miner");
	console.debug("Displayed Miner Address: "+id.value);

	eraseResults();
	perform("all_miner_address", '')
}


/* Peers Handling */
function getPeers(evt) {
	console.debug("Get peers");

	eraseResults();
	perform("peers", '')
}

function addPeers(evt) {
	console.debug("Add peers");

	var input = document.getElementById("peers")
	var peerlst = input.value;

	var data = peerList(peerlst)

	eraseResults();
	perform("add_peers", data)
}

function appPeers(evt) {
	console.debug("Append peers");

	var input = document.getElementById("peers")
	var peerlst = input.value;

	var data = peerList(peerlst);
	eraseResults();	
	perform("append_peers", data)
}

function peerAddresses(evt) {
	console.debug("Peer addresses");

	eraseResults();
	perform("peer_addresses", "")
}

function detectPeers(evt) {
	console.debug("Detect peers");

	eraseResults();
	perform("connect_to_peers_of_peers", '')
}

function connect(evt) {
	console.debug("Perform connect");

	eraseResults();
	perform("connect_to_peers_of_peers", '')
}

/* Transaction */
function transaction(evt) {
	console.debug("Perform transaction");

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

	eraseResults();
	perform("mine", '')
}

function consensus(evt) {
	console.debug("Perform consensus");

	eraseResults();
	perform("consensus", '')
}

function blocks(evt) {
	console.debug("Perform blocks");

	eraseResults();
	perform("blocks", '')
}
