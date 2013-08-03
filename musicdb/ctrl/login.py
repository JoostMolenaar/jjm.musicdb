import webob
import webob.exc

import core

class Login(core.FileServer):
    def GET(self, request):
        return super(Login, self).GET(request, 'login.html')

    def POST(self, request):
        for i in range(int(core.ini.auth.count)):
            u = core.ini.auth['username{0}'.format(i)]
            p = core.ini.auth['password{0}'.format(i)]
            r = core.ini.auth['rights{0}'.format(i)].split(',')

            if request.POST['Username'] == u and \
               request.POST['Password'] == p:
                response = webob.Response(content_type='text/plain', body='200 OK')
                core.session.start_session(request, response)
                request.session.rights = r
                return response
        else:
            raise webob.exc.HTTPForbidden('Bad username or password.')
