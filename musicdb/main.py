import core
import musicdb
import musicdb.ctrl
import musicdb.ctrl.root

class MusicDBRouter(core.Router):
    dispatch = [
        (r'^/musicdb/$',                                    musicdb.ctrl.root.Root()),
        (r'^/musicdb/login/$',                              musicdb.ctrl.login.Login('/web', 'text/html')),
        (r'^/musicdb/artist\.xml$',                         musicdb.ctrl.artist.ArtistRoot()),
        (r'^/musicdb/artist/([1-9][0-9]*)$',                musicdb.ctrl.artist.ArtistEditForm()),
        (r'^/musicdb/artist/new$',                          musicdb.ctrl.artist.ArtistAddForm()),
        (r'^/musicdb/label\.xml$',                          musicdb.ctrl.label.LabelRoot()),
        (r'^/musicdb/label/([1-9][0-9]*)$',                 musicdb.ctrl.label.LabelEditForm()),
        (r'^/musicdb/label/new$',                           musicdb.ctrl.label.LabelAddForm()),
        (r'^/musicdb/format$',                              musicdb.ctrl.format.FormatRoot()),
        (r'^/musicdb/format/([1-9][0-9]*)$',                musicdb.ctrl.format.FormatEditForm()),
        (r'^/musicdb/format/new$',                          musicdb.ctrl.format.FormatAddForm()),
        (r'^/musicdb/release\.xml$',                        musicdb.ctrl.release.ReleaseRoot()),
        (r'^/musicdb/release\.json$',                       musicdb.ctrl.release.ReleaseJSON()),
        (r'^/musicdb/release/([0-9]+)$',                    musicdb.ctrl.release.ReleaseEditForm()),
        (r'^/musicdb/release/new$',                         musicdb.ctrl.release.ReleaseAddForm()), 
        (r'^/musicdb/related/artist/([1-9][0-9]*)$',        musicdb.ctrl.related.Artist()),
        (r'^/musicdb/related/artist/([1-9][0-9]*)\.png$',   musicdb.ctrl.related.ArtistAsGraph()),
        (r'^/musicdb/related/label/([1-9][0-9]*)$',         musicdb.ctrl.related.Label()),
        (r'^/musicdb/related/label/([1-9][0-9]*)\.png$',    musicdb.ctrl.related.LabelAsGraph()),
        (r'^/musicdb/discogs/search/$',                     musicdb.ctrl.discogs.DiscogsSearch()),
        (r'^/musicdb/discogs/release/$',                    musicdb.ctrl.discogs.DiscogsRelease()),
        (r'^/musicdb/(mobile\.html)$',                      core.FileServer('/web', 'application/xhtml+xml')),
        (r'^/musicdb/([a-z_]+.xsl)$',                       core.FileServer('/web', 'text/xsl')),
        (r'^/musicdb/([a-z]+\.css)$',                       core.FileServer('/web', 'text/css')),
        (r'^/musicdb/([a-z]+\.js)$',                        core.FileServer('/web', 'text/javascript')),
        (r'^/musicdb/(jquery.+\.js$)',                      core.FileServer('/web/jquery', 'text/javascript')),
        (r'^/musicdb/(jquery.+\.css$)$',                    core.FileServer('/web/jquery-css', 'text/css'))
    ]

    #@core.session_loader
    #def __call__(self, request, *a, **k):
    #    super(MusicDBRouter)(request, *a, **k)

app = MusicDBRouter()
app = core.session_loader(app)

if __name__ == '__main__':
    core.run_server(app)

