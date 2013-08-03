import core

SHORT_URL = '/musicdb/artist/%d'

class Artist(core.model.Model):
	@core.model.short_url('ArtistID', SHORT_URL)
	@core.model.open_query
	def get(self):
		return ('SELECT * FROM artist ORDER BY name', [])

	@core.model.first
	@core.model.short_url('ArtistID', SHORT_URL)
	@core.model.open_query
	def get_by_id(self, artist_id):
		return ('SELECT * FROM artist WHERE artistid=%s', [artist_id])

	@core.model.short_url('ArtistID', SHORT_URL)
	@core.model.open_query
	def get_alias_by_id(self, artist_id):
		return ('SELECT * FROM artist WHERE %s IN (artistid, aliasid) '
				'UNION ' 
				'SELECT * FROM artist WHERE (SELECT aliasid FROM artist WHERE artistid=%s) IN (artistid, aliasid)',
				[artist_id, artist_id])

	@core.model.short_url('ArtistID', SHORT_URL)
	@core.model.open_query
	def get_related(self, artist_id):
		return ('SELECT a.* FROM artist a '
				'WHERE a.artistid = %s '
				'UNION DISTINCT '
				'SELECT a2.* FROM artist a1 '
				'JOIN artist a2 ON a1.aliasid = a2.artistid OR a1.artistid = a2.aliasid '
				'WHERE a1.artistid = %s '
				'UNION DISTINCT '
				'SELECT a2.* FROM artist a1 '
				'JOIN artist_group ag ON a1.artistid=ag.groupid '
				'JOIN artist a2 ON ag.memberid=a2.artistid '
				'WHERE a1.artistid = %s '
				'UNION DISTINCT '
				'SELECT a2.* FROM artist a1 '
				'JOIN artist_group ag ON a1.artistid=ag.memberid '
				'JOIN artist a2 ON ag.groupid=a2.artistid '
				'WHERE a1.artistid = %s',
				[artist_id, artist_id, artist_id, artist_id])
				
	@core.model.short_url('ArtistID', SHORT_URL)
	@core.model.open_query
	def get_real_name(self, artist_id):
		return ('SELECT a2.* FROM artist a1 '
				'JOIN artist a2 ON a1.aliasid = a2.artistid '
				'WHERE a1.artistid = %s',
				[artist_id])
		
	@core.model.short_url('ArtistID', SHORT_URL)
	@core.model.open_query
	def get_aliases(self, artist_id):
		return ('SELECT a2.* FROM artist a1 '
				'JOIN artist a2 ON a1.artistid = a2.aliasid '
				'WHERE a1.artistid = %s',
				[artist_id])
		
	@core.model.short_url('ArtistID', SHORT_URL)
	@core.model.open_query
	def get_group_members(self, artist_id):
		return ('SELECT a2.* FROM artist a1 '
				'JOIN artist_group ag ON a1.artistid = ag.groupid '
				'JOIN artist a2 ON ag.memberid = a2.artistid '
				'WHERE a1.artistid = %s',
				[artist_id])
		
	@core.model.short_url('ArtistID', SHORT_URL)
	@core.model.open_query
	def get_groups(self, artist_id):
		return ('SELECT a2.* FROM artist a1 '
				'JOIN artist_group ag ON a1.artistid = ag.memberid '
				'JOIN artist a2 ON ag.groupid = a2.artistid '
				'WHERE a1.artistid = %s',
				[artist_id])

	@core.model.exec_query
	def add(self, name, aliasID):
		return ('INSERT INTO artist (name, aliasID) VALUES (%s, %s)', [name, aliasID or None])

	@core.model.exec_query
	def update(self, artistID, name, aliasID):
		return ('UPDATE artist SET name=%s, aliasID=%s WHERE artistID=%s', [name, aliasID or None, artistID])

	@core.model.exec_query
	def delete(self, artistID):
		return ('DELETE FROM artist WHERE artistID=%s', [artistID])
