from flask import Flask

app = Flask(__name__)

peer_list = set()


@app.route('/peers/<peer>')
def peers(peer):
    peer_list.add(peer)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
