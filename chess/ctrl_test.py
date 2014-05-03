from flask import Flask
from flask_sockets import Sockets

application = Flask(__name__)
sockets = Sockets(application)

all_games = {}


@application.route("/")
def hello():
    return "Hello World!"


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)

# if __name__ == "__main__":
#    application.run(debug=True)

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), application, handler_class=WebSocketHandler)
    server.serve_forever()
