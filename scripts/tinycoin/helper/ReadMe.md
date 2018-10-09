# Tiny Coin Helper

### A pure java script based web GUI targeting tiny coin Version 1.7

### API Supported as per the ReadMe.md of archive/scripts/tinycoin

### Cross origin headers challenge - install the flask_cors.

The index.html is the main page for accessing the tincycoin API.

##### Tinycoin server address box: This the ip address along with port number where the tincycoin python flask server is running.
#####            Tinycoin version: GUI support for tinycoin version. - "version" API call
#####               Miner address: Get Miner address button displays current miner address. - "miner_address" API call
                                   Update Miner Address button updates the miner address and displays new value - "update_miner_address" API call

##### Peers Tab: Displays the peer operations
		Get Peers button: Displays the current peers in the Peers text area. - "peers" API call
		Add Peers button: Clears the current list of peers and creates new peers. - "add_peers" API call
							New peers are to be entered in New Peers box one peer per line
		Append Peers button: Append Peers button: Adds new peers to the current list of peers. - "append_peers" API call
							  New peers are to be entered in New Peers box one peer per line
		Detect Peers button: Adds peers of all current peers to current peer list. - "connect_to_peers_of_peers" API call
		
		Peers button: Arranges the peers; one peer per line
		
##### Transaction Tab: Makes a transaction
		Perform Transaction button: Makes a transaction. - "transaction" API call
			The added new fields are managed internally.
			
##### Other Operations: Facilitates all the remaining operations.
		Perform Mine button: "mine" API call
		Perform Consensus: "consensus" API call
		All Blocks: "blocks" API call
		
##### Results: Shows the results of API calls.
