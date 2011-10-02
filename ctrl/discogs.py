import webob
import webob.exc

import core

import urllib2

def _get_discogs(url):
    req = urllib2.Request(url)
    req.add_header('Accept-Encoding', 'gzip')
    res = urllib2.urlopen(req)
    response = webob.Response()
    response.body = res.read()
    response.content_type = res.headers['Content-Type']
    if 'Content-Encoding' in res.headers:
        response.content_encoding = res.headers['Content-Encoding']
    return response


class DiscogsSearch(core.Resource):
    def GET(self, request):
        url = 'http://www.discogs.com/search?api_key=b53fa1f10b&f=xml&{0}'.format(request.query_string)
        return _get_discogs(url)

class DiscogsRelease(core.Resource):
    def GET(self, request):
        return webob.Response(body='release: ' + request.path_info, content_type='text/plain')
