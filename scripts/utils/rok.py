from flask import Flask
import flask_ngrok


app = Flask(__name__)
flask_ngrok.run_with_ngrok(app)
print(flask_ngrok.ngrok_address)
