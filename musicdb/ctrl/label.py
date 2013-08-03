import webob
import webob.exc

import core
import musicdb.model.db
import musicdb.view.label

class LabelEditForm(core.Resource):
	@core.xslt
	def GET(self, request, labelID):
		db = musicdb.model.db.DB()
		l = db.label.get_by_id(labelID)
		lx = db.label.get()
		return webob.Response(body=musicdb.view.label.label_form(lx, l))

	@core.authenticated('EditData')
	def POST(self, request, labelID):
		db = musicdb.model.db.DB()
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

class LabelAddForm(core.Resource):
	@core.xslt
	def GET(self, request):
		db = musicdb.model.db.DB()
		lx = db.label.get()
		return webob.Response(body=musicdb.view.label.label_form(lx))

	@core.authenticated('EditData')
	def POST(self, request):
		db = musicdb.model.db.DB()
		db.label.add(
            request.POST['LabelName'], 
            request.POST['ParentID'] if request.POST['ParentID'] != u'\u2002' else None)
		raise webob.exc.HTTPCreated()

class LabelRoot(core.Resource):
	@core.xslt
	def GET(self, request):
		db = musicdb.model.db.DB()
		l = db.label.get()
		return webob.Response(body=musicdb.view.label.label_list(l))

