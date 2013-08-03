import webob
import webob.exc

import jjm.core
import jjm.musicdb.model.db
import jjm.musicdb.view.format

class FormatEditForm(jjm.core.Resource):
    @jjm.core.xslt
    def GET(self, request, formatID):
        db = jjm.musicdb.model.db.DB()
        fx = db.format.get_by_id(formatID)
        return webob.Response(body=jjm.musicdb.view.format.format_form(fx))

    @jjm.core.authenticated('EditData')
    def POST(self, request, formatID):
        db = jjm.musicdb.model.db.DB()
        if 'delete' in request.POST:
            db.format.delete(formatID)
            raise webob.exc.HTTPOk()
        elif 'updatex' in request.POST:
            db.format.update(formatID, request.POST['FormatName'])
            raise webob.exc.HTTPOk()
        else:
            raise webob.exc.HTTPNotImplemented(formatID + ': ' + repr(request.POST))

class FormatAddForm(jjm.core.Resource):
    @jjm.core.xslt
    def GET(self, request):
        return webob.Response(body=jjm.musicdb.view.format.format_form())

    @jjm.core.authenticated('EditData')
    def POST(self, request):
        db = musicdb.model.db.DB()
        db.format.add(request.POST['FormatName'])
        raise webob.exc.HTTPCreated()

class FormatRoot(jjm.core.Resource):
    @jjm.core.xslt
    def GET(self, request):
        db = jjm.musicdb.model.db.DB()
        f = db.format.get()
        return webob.Response(body=jjm.musicdb.view.format.format_list(f))

