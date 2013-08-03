import core

class Release(core.model.Model):
    @core.model.short_url('ReleaseID', '/musicdb/release/%d')
    @core.model.open_query
    def get(self):
        return ('SELECT `release`.* FROM `release`'
				'JOIN `label` ON `release`.`labelid` = `label`.`labelid`'
				'ORDER BY `release`.`year`, `label`.`name`, `release`.`catno`', [])

    @core.model.first
    @core.model.short_url('ReleaseID', '/musicdb/release/%d')
    @core.model.open_query
    def get_by_id(self, releaseID):
        return ('SELECT * FROM `release` WHERE releaseID=%s', [releaseID])

    @core.model.exec_query
    def add(self, formatID, labelID, catNo, year, name):
        return ('INSERT INTO `release` (formatid, labelid, catno, `year`, name) '
                'VALUES (%s, %s, %s, %s, %s)',
                [formatID, labelID, catNo, year, name])

    @core.model.exec_query
    def update(self, releaseID, formatID, labelID, catNo, year, name):
        return ('UPDATE `release` '
                'SET formatid=%s, labelid=%s, catno=%s, `year`=%s, name=%s '
                'WHERE releaseid=%s',
                [formatID, labelID, catNo, year, name, releaseID])

    @core.model.exec_query
    def delete(self, releaseID):
        return ('DELETE FROM `release` WHERE releaseid=%s', [releaseID])

