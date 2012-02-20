import core.model

import musicdb.model.artist
import musicdb.model.label
import musicdb.model.format
import musicdb.model.release
import musicdb.model.artistrelease
import musicdb.model.artistgroup

class DB(core.model.Model):
	def __init__(self, provider=core.model.MySQLProvider):
		core.model.Model.__init__(self, provider)

		self.artist = musicdb.model.artist.Artist(self.provider)
		self.label = musicdb.model.label.Label(self.provider)
		self.format = musicdb.model.format.Format(self.provider)
		self.release = musicdb.model.release.Release(self.provider)
		self.artistrelease = musicdb.model.artistrelease.ArtistRelease(self.provider)
		self.artistgroup = musicdb.model.artistgroup.ArtistGroup(self.provider)

if __name__ == '__main__':
	db = DB()
