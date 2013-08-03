import webob

import core

class FileServer(core.Resource):
    def __init__(self, content_type, path):
        self.content_type = content_type
        self.path = path

    def GET(self, request, filename):
        with open(self.path + '/' + filename, 'rb') as f:
            return webob.Response(content_type=self.content_type,
                                  body=f.read())
