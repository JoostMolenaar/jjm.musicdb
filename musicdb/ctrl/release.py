import webob.exc

import core

import musicdb.model.db

import musicdb.view.artist
import musicdb.view.label
import musicdb.view.format
import musicdb.view.release

class ReleaseEditForm(core.Resource):
    @core.xslt
    def GET(self, request, releaseID):
        db = musicdb.model.db.DB()
        ax = db.artist.get()
        lx = db.label.get()
        fx = db.format.get()
        arx = dict(db.artistrelease.get_by_release_id(releaseID))[int(releaseID)]
        rx = db.release.get_by_id(releaseID)
        return webob.Response(body=musicdb.view.release.release_form(ax, lx, fx, rx, arx))

    @core.authenticated('EditData')
    def POST(self, request, releaseID):
        #raise webob.exc.HTTPNotImplemented(releaseID + ': ' + str(request.POST))
        db = musicdb.model.db.DB()
        if 'delete' in request.POST:
            db.artistrelease.delete_by_release_id(releaseID)
            db.release.delete(releaseID)
            raise webob.exc.HTTPOk()
        elif 'update' in request.POST:
            db.artistrelease.delete_by_release_id(releaseID)
            for artistID in request.POST.getall('ArtistID'):
                if artistID == u'\u2002': continue
                db.artistrelease.add(artistID, releaseID)
            db.release.update(releaseID,
                              request.POST['FormatID'] if request.POST['FormatID'] != u'\u2002' else None,
                              request.POST['LabelID'] if request.POST['LabelID'] != u'\u2002' else None,
                              request.POST['CatNo'],
                              request.POST['Year'],
                              request.POST['ReleaseName'])
            raise webob.exc.HTTPOk()

class ReleaseAddForm(core.Resource):
    @core.xslt
    def GET(self, request):
        db = musicdb.model.db.DB()
        ax = db.artist.get()
        lx = db.label.get()
        fx = db.format.get()
        return webob.Response(body=musicdb.view.release.release_form(ax, lx, fx))

    @core.authenticated('EditData')
    def POST(self, request):
        #raise webob.exc.HTTPNotImplemented(str(request.POST) + ' ArtistIDs:' + str(request.POST.getall('ArtistID')))
        db = musicdb.model.db.DB()
        _, releaseID = db.release.add(request.POST['FormatID'] if request.POST['FormatID'] != u'\u2002' else None, 
                                      request.POST['LabelID'] if request.POST['LabelID'] != u'\u2002' else None,
                                      request.POST['CatNo'],
                                      request.POST['Year'],
                                      request.POST['ReleaseName'])
        for artistID in request.POST.getall('ArtistID'):
            if artistID == u'\u2002': continue
            db.artistrelease.add(artistID, releaseID)
        raise webob.exc.HTTPCreated()

class ReleaseRoot(core.Resource):
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

class ReleaseJSON(core.Resource):
	@core.transformer
	def GET(self, request):
		db = musicdb.model.db.DB()
		ax = db.artist.get() ; aid = dict((a.ArtistID, a.ShortURL) for a in ax)
		lx = db.label.get() ; lid = dict((l.LabelID, l.ShortURL) for l in lx)
		fx = db.format.get() ; fid = dict((f.FormatID, f.ShortURL) for f in fx)
		rx = db.release.get()
		arx = dict(db.artistrelease.get())
		return 200, 'application/json', {
			'formats': dict((f.ShortURL, f.Name) for f in fx),
			'artists': dict((a.ShortURL, a.Name) for a in ax),
			'labels': dict((l.ShortURL, l.Name) for l in lx),
			'releases': dict(
				(r.ShortURL, {
					'name':r.Name, 
					'label':lid[r.LabelID], 
					'format':fid[r.FormatID], 
					'catno':r.CatNo, 
					'year':r.Year
				})
				for r in rx
			)}
