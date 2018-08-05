# Networking Research

This module describes research on networking module. 

## Implementation 1

This section contains information about `networking-1` 
directory in `scripts`. To build a stable blockchain, 
a good networking engine is necessary. This implementation 
describes a very basic stable networking infrastructure.

### Tracker

`Tracker` class acts as dns seed, it keep record of all 
full node peers. When a `Node` is started, it sends its 
listening port to `Tracker`, `Tracker` then registers 
`Node` in its peer list and sends a portion of peer list
back to `Node`. Then `Node` can connect to other peers.

