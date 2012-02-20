import webob
import webob.exc

import core
import core.xml

import musicdb.model.db

import musicdb.view.release
import musicdb.view.artist
import musicdb.view.label
import musicdb.view.format

class Root(core.Resource):
	@core.xslt
	def GET(self, request):
		db = musicdb.model.db.DB()
		ax = db.artist.get()
		lx = db.label.get()
		fx = db.format.get()
		rx = db.release.get()
		arx = dict(db.artistrelease.get())
		return webob.Response(body=
			['musicDB',
				musicdb.view.artist.artist_list(ax),
				musicdb.view.label.label_list(lx),
				musicdb.view.format.format_list(fx),
				musicdb.view.release.release_list(ax, lx, fx, rx, arx)])
