import os

peer_nodes = None

def print_peers():
    print(f"PEERS: { peer_nodes }")

if __name__ == "__main__":
    print("Tinycoin server started ...!\n")
    
    peers = os.getenv("PEERS", None)
    if(peers):
        peer_nodes = peers.split(",")
    else:
        peer_nodes = []
    host = os.getenv("HOST", "0.0.0.0")
    port = os.getenv("PORT", 5000)
    
    print_peers()
    print(f"host: { host }")
    print(f"port: { port }")