class HelloRPC(object):
    def hello(self, name):
        return "Hello, %s" % name

    def ping(self):
        return "ok"
