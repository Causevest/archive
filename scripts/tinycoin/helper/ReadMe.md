# Tiny Coin Helper

### A pure java script based web GUI targeting tiny coin Version 1.8

### API Supported as per the ReadMe.md of archive/scripts/tinycoin

### Cross origin headers challenge - install the flask_cors.

The index.html is the main page for accessing the tincycoin API.

##### Tinycoin server address box: This the ip address along with port number where the tincycoin python flask server is running.
#####            Tinycoin version: GUI support for tinycoin version. - "version" API call
#####               Miner address: Get Miner address button displays current miner address. - "get_miner_address" API call
                                   Update Miner Address button generates new miner address and displays new value - "update_miner_address" API call

##### Peers Tab: Displays the peer operations
		Format button: Arranges the peers; one peer per line
		Clear button: Clears the content of peers list
		Get button: Displays the current peers in the Peers text area. - "peers" API call
		Add button: Adds list of peers replacing existing peers, if any. - "add_peers" API call
		Append button: Adds peers to the current list of peers. - "append_peers" API call
		Detect button: Adds peers of all current peers to current peer list. - "connect_to_peers_of_peers" API call	- Not enabled for now.
		PeerAddr button: Displays all the addresses used by this node in results area - "peer_addresses" API call
		
##### Transaction Tab: Makes a transaction
		Perform Transaction button: Makes a transaction. - "transaction" API call
		Clear Transaction button: Clears the contents of transaction fields.
			
##### Other Operations Tab: Facilitates all the remaining operations.
		Perform Mine button: "mine" API call
		Perform Consensus: "consensus" API call
		All Blocks: "blocks" API call

##### Coins: Displays coins earned due to mining, spent in transaction and current balance of coins.
		Refresh button: Fetches the current coins holdings - "coins" API call
			
##### Results: Shows the results of API calls.
