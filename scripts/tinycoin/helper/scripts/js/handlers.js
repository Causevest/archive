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

// OK for now, if required send element Id to a general function
/* Clear version textbox */
function clrVersion() {
	var ver = document.getElementById("version");
	ver.value = '';
}

/* Beautify peer list */
function alignPeers(evt) {
	console.debug("Beautify peers");
	resetActiveClass(evt);
	var peers = document.getElementById("peers")
	if(peers.value.length <= 0)
		return;
	var peerlst = beautifyPeers(peers.value);
	peers.value = peerlst;
}

/* Clear Peer Input List */
function clrPeerIp(evt) {
	var peers = document.getElementById("peerinput");
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
	resetActiveClass(evt);
	eraseResults();
}
function eraseResults() {
	var results = document.getElementById("results");
	results.value = "";
}