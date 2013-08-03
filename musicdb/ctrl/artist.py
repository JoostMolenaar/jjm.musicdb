import webob
import webob.exc

import core
import musicdb.model.db
import musicdb.view.artist

class ArtistEditForm(core.Resource):
    @core.xslt
    def GET(self, request, artistID):
        db = musicdb.model.db.DB()
        a = db.artist.get_by_id(artistID)
        ax = db.artist.get()
        g = db.artist.get_groups(artistID)
        return webob.Response(body=musicdb.view.artist.artist_form(ax, a, g))

    @core.authenticated('EditData')
    def POST(self, request, artistID):
        db = musicdb.model.db.DB()
        if 'delete' in request.POST:
            db.artist.delete(artistID)
            raise webob.exc.HTTPOk()
        elif 'update' in request.POST:
            db.artist.update(artistID, 
                request.POST['ArtistName'], 
                request.POST['AliasID'] if request.POST['AliasID'] != u'\u2002' else None)
            db.artistgroup.delete_by_member_id(artistID);
            for groupID in request.POST.getall('GroupID'):
                if groupID == u'\u2002': continue
                db.artistgroup.add(groupID, artistID)
            raise webob.exc.HTTPOk()
        else:
            raise webob.exc.HTTPNotImplemented(artistID + ': ' + repr(request.POST))

class ArtistAddForm(core.Resource):
    @core.xslt
    def GET(self, request):
        db = musicdb.model.db.DB()
        ax = db.artist.get()
        return webob.Response(body=musicdb.view.artist.artist_form(ax))

    @core.authenticated('EditData')
    def POST(self, request):
        db = musicdb.model.db.DB()
        db.artist.add(
            request.POST['ArtistName'], 
            request.POST['AliasID'] if request.POST['AliasID'] != u'\u2002' else None)
        for groupID in request.POST.getall('GroupID'):
            if groupID == u'\u2002': continue
            db.artist_group.add(groupID, artistID)
        raise webob.exc.HTTPCreated()

class ArtistRoot(core.Resource):
    @core.xslt
    def GET(self, request):
        db = musicdb.model.db.DB()
        ax = db.artist.get()
        return webob.Response(body=musicdb.view.artist.artist_list(ax))

