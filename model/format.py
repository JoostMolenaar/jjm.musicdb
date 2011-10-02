import core.model

class Format(core.model.Model):
    @core.model.short_url('FormatID', '/musicdb/format/%d')
    @core.model.open_query
    def get(self):
        return ('SELECT * FROM format', [])

    @core.model.first
    @core.model.short_url('FormatID', '/musicdb/format/%d')
    @core.model.open_query
    def get_by_id(self, formatID):
        return ('SELECT * FROM format WHERE formatid=%s', [formatID])

    @core.model.exec_query
    def add(self, name):
        return ('INSERT INTO format (name) VALUES (%s)', [name])

    @core.model.exec_query
    def update(self, formatID, name):
        return ('UPDATE format SET name=%s WHERE formatid=%s',
                [formatID, name])

    @core.model.exec_query
    def delete(self, formatID):
        return ('DELETE FROM format WHERE formatid=%s',
                [formatID])