/* Handles all the events of index.html page */
// OK for now, if required send element Id to a general function
/* Clear version textbox */
function clrVersion() {
	var ver = document.getElementById("version");
	ver.value = '';
}

/* Beautify peer list */
function alignPeers(evt) {
	console.debug("Beautify peers");
	var peers = document.getElementById("peers")
	if(peers.value.length <= 0)
		return;
	var peerlst = beautifyPeers(peers.value);
	peers.value = peerlst;
}

/* Clear Peer Input List */
function clrPeers(evt) {
	var peers = document.getElementById("peers");
	peers.value = '';
}

/* Clear Transaction Fields */
function clearTxn(evt) {
	var src = document.getElementById("from")
	var tgt = document.getElementById("to")
	var amt = document.getElementById("amount")
	src.value = '';
	tgt.value = '';
	amt.value = '';
}


/* Results */
function clearResults(evt) {
	console.debug("Clear the results");
	eraseResults();
}
function eraseResults() {
	var results = document.getElementById("results");
	results.value = "";
}
