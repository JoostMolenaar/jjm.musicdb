import core

import artist
import label
import format
import release
import artistrelease
import artistgroup

class DB(core.model.Model):
	def __init__(self, provider=core.model.MySQLProvider):
		core.model.Model.__init__(self, provider)

		self.artist = artist.Artist(self.provider)
		self.label = label.Label(self.provider)
		self.format = format.Format(self.provider)
		self.release = release.Release(self.provider)
		self.artistrelease = artistrelease.ArtistRelease(self.provider)
		self.artistgroup = artistgroup.ArtistGroup(self.provider)

if __name__ == '__main__':
	db = DB()
