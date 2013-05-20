import webob
import webob.exc

import jjm.core
import jjm.musicdb.model.db
import jjm.musicdb.view.label

class LabelEditForm(jjm.core.Resource):
	@jjm.core.xslt
	def GET(self, request, labelID):
		db = jjm.musicdb.model.db.DB()
		l = db.label.get_by_id(labelID)
		lx = db.label.get()
		return webob.Response(body=jjm.musicdb.view.label.label_form(lx, l))

	@jjm.core.authenticated('EditData')
	def POST(self, request, labelID):
		db = jjm.musicdb.model.db.DB()
		if 'delete' in request.POST:
			db.label.delete(labelID)
			raise webob.exc.HTTPOk()
		elif 'update' in request.POST:
			db.label.update(labelID, 
                request.POST['LabelName'], 
                request.POST['ParentID'] if request.POST['ParentID'] != u'\u2002' else None)
			raise webob.exc.HTTPOk()
		else:
			raise webob.exc.HTTPNotImplemented(labelID + ': ' + repr(request.POST))

class LabelAddForm(jjm.core.Resource):
	@jjm.core.xslt
	def GET(self, request):
		db = jjm.musicdb.model.db.DB()
		lx = db.label.get()
		return webob.Response(body=jjm.musicdb.view.label.label_form(lx))

	@jjm.core.authenticated('EditData')
	def POST(self, request):
		db = jjm.musicdb.model.db.DB()
		db.label.add(
            request.POST['LabelName'], 
            request.POST['ParentID'] if request.POST['ParentID'] != u'\u2002' else None)
		raise webob.exc.HTTPCreated()

class LabelRoot(jjm.core.Resource):
	@jjm.core.xslt
	def GET(self, request):
		db = jjm.musicdb.model.db.DB()
		l = db.label.get()
		return webob.Response(body=jjm.musicdb.view.label.label_list(l))

