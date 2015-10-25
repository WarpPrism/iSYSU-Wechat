import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type = int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

def main():
    # tornado.options.parse_command_line()

    APP = tornado.web.Application(
        handlers = [("/", IndexHandler)],
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        debug = True
    )

    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()