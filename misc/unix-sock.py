import tornado.web
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_unix_socket


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    server = HTTPServer(application)
    unix_socket = bind_unix_socket('/tmp/foo.sock')
    server.add_socket(unix_socket)
    tornado.ioloop.IOLoop.instance().start()
