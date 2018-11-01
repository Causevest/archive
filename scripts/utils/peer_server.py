from flask import Flask
import json
import threading
import os

app = Flask(__name__)

peer_list = set()


@app.route('/peers/<peer>')
def peers(peer):
    peer_list.add(peer)
    return json.dumps(list(peer_list)), 200


def host():
    os.system('ssh -R tiny_coin_seed:80:localhost:9090 serveo.net')


if __name__ == '__main__':
    threading.Thread(target=host, daemon=True).start()
    app.run(host='0.0.0.0', port=9090)
