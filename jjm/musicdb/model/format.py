import jjm.core

class Format(jjm.core.model.Model):
    @jjm.core.model.short_url('FormatID', '/musicdb/format/%d')
    @jjm.core.model.open_query
    def get(self):
        return ('SELECT * FROM format', [])

    @jjm.core.model.first
    @jjm.core.model.short_url('FormatID', '/musicdb/format/%d')
    @jjm.core.model.open_query
    def get_by_id(self, formatID):
        return ('SELECT * FROM format WHERE formatid=%s', [formatID])

    @jjm.core.model.exec_query
    def add(self, name):
        return ('INSERT INTO format (name) VALUES (%s)', [name])

    @jjm.core.model.exec_query
    def update(self, formatID, name):
        return ('UPDATE format SET name=%s WHERE formatid=%s',
                [formatID, name])

    @jjm.core.model.exec_query
    def delete(self, formatID):
        return ('DELETE FROM format WHERE formatid=%s',
                [formatID])
