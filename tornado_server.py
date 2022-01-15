# Writing the Tornado server to initiate the client request

from socket import create_connection
import tornado.ioloop
import tornado.web
import tornado.websocket
import cv2
import numpy
from img_to_string import to_b64
from balls import detect_balls

from tornado.options import define, options, parse_command_line

define('port', default=8080, type=int)

cap = cv2.VideoCapture(0)

# This handler handles a call to the base of the server \
# (127.0.0.1:8888/ -> 127.0.0.1:8888/index.html)
class IndexHandler(tornado.web.RequestHandler):
    # GET request to get the base webpage
    # from the Tornado server
    def get(self):
        self.render('index.html')

# This handler handles a websocket connection
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    # function to open a new connection to the WebSocket
    def open(self, *args):
        print('new connection!')
        # self.write_message('welcome!')

    # function to respond to a message on the WebSocket
    def on_message(self, message):
        print('new message {}'.format(message))

        _, frame = cap.read()

        # enter open cv code here -- detect_balls(frame, message)

        self.write_message(to_b64("frame.jpg"))

    # function to close a connection on the WebSocket
    def on_close(self):
        print('connection closed')

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/ws/', WebSocketHandler)
])

if __name__ == '__main__':
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()