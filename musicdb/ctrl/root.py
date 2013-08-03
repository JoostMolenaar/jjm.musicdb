import webob
import webob.exc

import jjm.core
import jjm.musicdb.model.db
import jjm.musicdb.view.release
import jjm.musicdb.view.artist
import jjm.musicdb.view.label
import jjm.musicdb.view.format

class Root(jjm.core.Resource):
	@jjm.core.xslt
	def GET(self, request):
		db = jjm.musicdb.model.db.DB()
		ax = db.artist.get()
		lx = db.label.get()
		fx = db.format.get()
		rx = db.release.get()
		arx = dict(db.artistrelease.get())
		return webob.Response(body=
			['musicDB',
				jjm.musicdb.view.artist.artist_list(ax),
				jjm.musicdb.view.label.label_list(lx),
				jjm.musicdb.view.format.format_list(fx),
				jjm.musicdb.view.release.release_list(ax, lx, fx, rx, arx)])
