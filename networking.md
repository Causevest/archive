# Networking Research

This module describes research on networking module. 

## Implementation 1

This section contains information about `networking-1` 
directory in `scripts`. To build a stable blockchain, 
a good networking engine is necessary. This implementation 
describes a very basic stable networking infrastructure. 
Note: `networking-1` only provides proof of concept 
implementation for networking. Using some software 
development effor it can be converted to proper functional 
implementation.

### Tracker

`Tracker` class acts as dns seed, it keep record of all 
full node peers. When a `Node` is started, it sends its 
listening port to `Tracker`, `Tracker` then registers 
`Node` in its peer list and sends a portion of peer list
back to `Node`. Then `Node` can connect to other peers. 
It can be made more secure by using some authentication 
mechanism, which can be helpful to avoid DoS attack.

### Node

`Node` uses well known tracker and discovers other `Node`s 
for communication of blockchain information. It also 
registers itself for receiving coommunication.

