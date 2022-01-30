# Writing the Tornado server to initiate the client request

import tornado.ioloop
import tornado.web
import tornado.websocket
import cv2
from processing.img_to_string import to_b64
from processing.balls import detect_balls
from processing.constants import camera, exposure

from tornado.options import define, options

define('port', default=8080, type=int)

cap = cv2.VideoCapture(camera)
cap.set(cv2.CAP_PROP_EXPOSURE, exposure)

# This handler handles a call to the base of the server \
# (127.0.0.1:8888/ -> 127.0.0.1:8888/index.html)
class IndexHandler(tornado.web.RequestHandler):
    # GET request to get the base webpage
    # from the Tornado server
    def get(self):
        self.render('./www/index.html')

# This handler handles a websocket connection
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    # function to open a new connection to the WebSocket
    def open(self, *args):
        print('cargo connection opened')
        # self.write_message('welcome!')

    # function to respond to a message on the WebSocket
    def on_message(self, message):
        _, frame = cap.read()
        
        # enter open cargo detection here
        output_image = detect_balls(frame, message)
        cv2.imwrite("frame.jpg", output_image)

        self.write_message(to_b64("frame.jpg"))

    # function to close a connection on the WebSocket
    def on_close(self):
        print('cargo connection closed')

class ShadowHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./www/line.html")

class ShadowSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        print("line websocket connection")
    
    def on_message(self, message):
        _, frame = cap.read()

        # enter shadow line code here
        
        cv2.imwrite('frame.jpg', frame)

        self.write_message(to_b64('frame.jpg'))

    def on_close(self):
        print('line connection closed')

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/ws/', WebSocketHandler),
    (r'/line/', ShadowHandler),
    (r'/line/ws/', ShadowSocketHandler)
])

if __name__ == '__main__':
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()