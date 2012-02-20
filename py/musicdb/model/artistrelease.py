import core.model

class ArtistRelease(core.model.Model):
    @core.model.group_by('ReleaseID')
    @core.model.open_query
    def get(self):
        return ('SELECT * FROM artist_release', [])

    @core.model.exec_query
    def add(self, artistID, releaseID):
        return ('INSERT INTO artist_release (artistid, releaseid) VALUES (%s, %s)', [artistID, releaseID])

    @core.model.exec_query
    def delete_by_release_id(self, releaseID):
        return ('DELETE FROM `artist_release` WHERE `releaseID`=%s', [releaseID])

    @core.model.group_by('ReleaseID')
    @core.model.open_query
    def get_by_release_id(self, releaseID):
        return ('SELECT * FROM artist_release WHERE releaseID = %s', [releaseID])
