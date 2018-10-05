function peerList(data) {
	var data = data.split(/[,\s]/)
	var moddata = []
	for(var i=0; i<data.length; i++) {
		if(data[i].length > 0) {
			moddata.push(data[i]);
		}
	}
	console.debug(moddata)
	console.debug(JSON.stringify(moddata))
	return JSON.stringify(moddata)
}

function generateTxnid(mineraddr, lasttxnid) {
	var txidx = lasttxnid.lastIndexOf("-XCV");
	var xcv = "-XCV-ID";
	var txid = "0000";
	if(txidx == -1) {
		lasttxnid = mineraddr+xcv+txid;
		txidx = lasttxnid.lastIndexOf(xcv);
	}
	txid = parseInt(lasttxnid.substring(txidx+xcv.length))+1
	currtxnid = mineraddr+xcv+txid.toString().padStart(4,'0');
	return currtxnid;
}

function generateTimeStamp() {
	return new Date();
}

function generateTxnSignature(mineraddr) {
	return "Under research ...";
}