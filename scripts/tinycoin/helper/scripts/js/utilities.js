
/* Remove white spaces and commas from peer input text area */
function peerList(data) {
	var data = data.split(/[,\s]/)
	var moddata = []
	for(var i=0; i<data.length; i++) {
		if(data[i].length > 0) {
			moddata.push(data[i]);
		}
	}
	return JSON.stringify(moddata)
}

/* Remove spaces, commas, double quotes, single quotes, braces etc from peers text area */
function beautifyPeers(data) {
	data = data.replace('[','');
	data = data.replace(']','');
	var dat = data.split(/[,\s\q]/)
	var moddata = ''
	for(var i=0; i<dat.length;i++) {
		if(dat[i].length > 0){
			dat[i] = dat[i].replace('\q','');
			moddata = moddata+dat[i]+"\n"
		}
	}
	return moddata;
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

function makeResString(strval) {
	var results = document.getElementById("results").value.trim();
	var resstr = ''; 
	if(results.length > 0) {
		resstr = results + "\n";
	}
	resstr = resstr + strval;
	return (resstr); 
}

function displayCoins(result) {
	earned = parseInt(document.getElementById('earned').value)
	spent = parseInt(document.getElementById('spent').value)

	coins = parseInt(result['coins'])
	if(coins >= 0) {
		earned = earned + coins;
	}
	else {
		spent = spent - coins;
	}

	balance = balance + coins;	
	document.getElementById('earned').value = earned
	document.getElementById('spent').value = spent
	document.getElementById('balance').value = balance
}
