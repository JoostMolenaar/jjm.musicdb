import jjm.core

class ArtistRelease(jjm.core.model.Model):
    @jjm.core.model.group_by('ReleaseID')
    @jjm.core.model.open_query
    def get(self):
        return ('SELECT * FROM artist_release', [])

    @jjm.core.model.exec_query
    def add(self, artistID, releaseID):
        return ('INSERT INTO artist_release (artistid, releaseid) VALUES (%s, %s)', [artistID, releaseID])

    @jjm.core.model.exec_query
    def delete_by_release_id(self, releaseID):
        return ('DELETE FROM `artist_release` WHERE `releaseID`=%s', [releaseID])

    @jjm.core.model.group_by('ReleaseID')
    @jjm.core.model.open_query
    def get_by_release_id(self, releaseID):
        return ('SELECT * FROM artist_release WHERE releaseID = %s', [releaseID])
