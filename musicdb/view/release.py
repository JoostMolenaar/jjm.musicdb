
import core

def release_list(ax, lx, fx, rx, arx):
    ax = dict((a.ArtistID, a) for a in ax)
    lx = dict((l.LabelID, l) for l in lx)
    fx = dict((f.FormatID, f) for f in fx)
    A = lambda a: ['a', ('ref', ax[a.ArtistID].ShortURL)]
    R = lambda r: ['release', 
                    ('uri', r.ShortURL),
                    ('format', fx[r.FormatID].ShortURL),
                    ('label', lx[r.LabelID].ShortURL),
                    ('cat', r.CatNo or ''),
                    ('year', r.Year or ''),
                    ('name', r.Name)] + map(A, arx[r.ReleaseID])
    return ['releases'] + map(R, sorted(rx, 
		cmp=lambda r1,r2: 0
				or cmp(r1.Year, r2.Year)
				or cmp(lx[r1.LabelID].Name, lx[r2.LabelID].Name)
				or cmp(r1.CatNo, r2.CatNo)))

def release_form(ax, lx, fx, r=None, arx=None):
    return ['release',
                ('mode', r and 'edit' or 'add'),
                ['uri', r and r.ShortURL or '/musicdb/release/new'],
                r and [core.xml.FRAGMENT] + [ ['artist', ('artistID', ar.ArtistID)] for ar in arx ] or ['artist'],
                r and ['label', ('labelID', r.LabelID)] or ['label'],
                r and ['format', ('formatID', r.FormatID)] or ['format'],
                r and ['catno', r.CatNo] or '',
                r and ['year', r.Year] or '',
                r and ['name', r.Name] or '',
                ['available']
                    + [ ['artist', ('artistID', a.ArtistID), ('name', a.Name)] for a in ax ]
                    + [ ['label', ('labelID', l.LabelID), ('name', l.Name)] for l in lx ]
                    + [ ['format', ('formatID', f.FormatID), ('name', f.Name)] for f in fx ]]

# <release mode="edit">
#   <artist>/musicDB/artist/2</artist>
#   <artist>/musicDB/artist/3</artist>
#   <label>/musicDB/label/1</artist>
#   <catno>BLA</catno>
#   <year>1999</year>
#   <name>Bla bla bla</name>
#   <available>
#       <artist uri="/artist/2" name="Burial"/>
#       ...
#       <label uri="/label/1" name="Texture"/>
#       ...
#   </available>
# </release>
