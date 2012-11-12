import webob
import webob.exc

import jjm.core
import jjm.musicdb.model.db
import jjm.musicdb.view.artist

class ArtistEditForm(jjm.core.Resource):
	@jjm.core.xslt
	def GET(self, request, artistID):
		db = jjm.musicdb.model.db.DB()
		a = db.artist.get_by_id(artistID)
		ax = db.artist.get()
		g = db.artist.get_groups(artistID)
		return webob.Response(body=jjm.musicdb.view.artist.artist_form(ax, a, g))

	@jjm.core.authenticated('EditData')
	def POST(self, request, artistID):
		db = jjm.musicdb.model.db.DB()
		if 'delete' in request.POST:
			db.artist.delete(artistID)
			raise webob.exc.HTTPOk()
		elif 'update' in request.POST:
			db.artist.update(artistID, request.POST['ArtistName'], request.POST['AliasID'])
			db.artistgroup.delete_by_member_id(artistID);
			for groupID in request.POST.getall('GroupID'):
				db.artistgroup.add(groupID, artistID)
			raise webob.exc.HTTPOk()
		else:
			raise webob.exc.HTTPNotImplemented(artistID + ': ' + repr(request.POST))

class ArtistAddForm(jjm.core.Resource):
	@jjm.core.xslt
	def GET(self, request):
		db = jjm.musicdb.model.db.DB()
		ax = db.artist.get()
		return webob.Response(body=jjm.musicdb.view.artist.artist_form(ax))

	@jjm.core.authenticated('EditData')
	def POST(self, request):
		db = jjm.musicdb.model.db.DB()
		db.artist.add(request.POST['ArtistName'], request.POST['AliasID'])
		for groupID in request.POST.getall('GroupID'):
			db.artist_group.add(groupID, artistID)
		raise webob.exc.HTTPCreated()

class ArtistRoot(jjm.core.Resource):
	@jjm.core.xslt
	def GET(self, request):
		db = jjm.musicdb.model.db.DB()
		ax = db.artist.get()
		return webob.Response(body=jjm.musicdb.view.artist.artist_list(ax))

