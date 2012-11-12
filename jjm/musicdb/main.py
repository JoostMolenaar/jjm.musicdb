import jjm.core
import jjm.musicdb
import jjm.musicdb.ctrl
import jjm.musicdb.ctrl.root

class MusicDBRouter(jjm.core.Router):
    dispatch = [
        (r'^/musicdb/$',                                    jjm.musicdb.ctrl.root.Root()),
        (r'^/musicdb/login/$',                              jjm.musicdb.ctrl.login.Login('/web', 'text/html')),
        (r'^/musicdb/artist\.xml$',                         jjm.musicdb.ctrl.artist.ArtistRoot()),
        (r'^/musicdb/artist/([1-9][0-9]*)$',                jjm.musicdb.ctrl.artist.ArtistEditForm()),
        (r'^/musicdb/artist/new$',                          jjm.musicdb.ctrl.artist.ArtistAddForm()),
        (r'^/musicdb/label\.xml$',                          jjm.musicdb.ctrl.label.LabelRoot()),
        (r'^/musicdb/label/([1-9][0-9]*)$',                 jjm.musicdb.ctrl.label.LabelEditForm()),
        (r'^/musicdb/label/new$',                           jjm.musicdb.ctrl.label.LabelAddForm()),
        (r'^/musicdb/format$',                              jjm.musicdb.ctrl.format.FormatRoot()),
        (r'^/musicdb/format/([1-9][0-9]*)$',                jjm.musicdb.ctrl.format.FormatEditForm()),
        (r'^/musicdb/format/new$',                          jjm.musicdb.ctrl.format.FormatAddForm()),
        (r'^/musicdb/release\.xml$',                        jjm.musicdb.ctrl.release.ReleaseRoot()),
        (r'^/musicdb/release\.json$',                       jjm.musicdb.ctrl.release.ReleaseJSON()),
        (r'^/musicdb/release/([0-9]+)$',                    jjm.musicdb.ctrl.release.ReleaseEditForm()),
        (r'^/musicdb/release/new$',                         jjm.musicdb.ctrl.release.ReleaseAddForm()), 
        (r'^/musicdb/related/artist/([1-9][0-9]*)$',        jjm.musicdb.ctrl.related.Artist()),
        (r'^/musicdb/related/artist/([1-9][0-9]*)\.png$',   jjm.musicdb.ctrl.related.ArtistAsGraph()),
        (r'^/musicdb/related/label/([1-9][0-9]*)$',         jjm.musicdb.ctrl.related.Label()),
        (r'^/musicdb/related/label/([1-9][0-9]*)\.png$',    jjm.musicdb.ctrl.related.LabelAsGraph()),
        (r'^/musicdb/discogs/search/$',                     jjm.musicdb.ctrl.discogs.DiscogsSearch()),
        (r'^/musicdb/discogs/release/$',                    jjm.musicdb.ctrl.discogs.DiscogsRelease()),
        (r'^/musicdb/(mobile\.html)$',                      jjm.core.FileServer('/web', 'application/xhtml+xml')),
        (r'^/musicdb/([a-z_]+.xsl)$',                       jjm.core.FileServer('/web', 'text/xsl')),
        (r'^/musicdb/([a-z]+\.css)$',                       jjm.core.FileServer('/web', 'text/css')),
        (r'^/musicdb/([a-z]+\.js)$',                        jjm.core.FileServer('/web', 'text/javascript')),
        (r'^/musicdb/(jquery.+\.js$)',                      jjm.core.FileServer('/web/jquery', 'text/javascript')),
        (r'^/musicdb/(jquery.+\.css$)$',                    jjm.core.FileServer('/web/jquery-css', 'text/css'))
    ]

app = MusicDBRouter()

if __name__ == '__main__':
    jjm.core.run_server(app)

