def artist_list(artists):
	a = lambda a: ['artist', ('uri', a.ShortURL), ('name', a.Name)]
	return ['artists'] + map(a, artists)

def artist_form(artists, artist=None, groups=None):
	a = lambda a: ['artist', ('artistID', a.ArtistID), ('name', a.Name)]
	return ['artist',
		('mode', artist and 'edit' or 'add'),
		['uri', artist and artist.ShortURL or '/musicdb/artist/new'],
		['img', artist and (artist.ShortURL.replace('/musicdb/', '/musicdb/related/') + '.png') or ''],
		['name', artist and artist.Name or ''],
		['alias', (artist and artist.AliasID) and ('artistID', artist.AliasID) or ''],
		['groups'] + (groups and [['artist', ('artistID', group.ArtistID)] for group in groups] or ['']),
		['available'] + map(a, artists)]
