import jjm.core

SHORT_URL = '/musicdb/label/%d'

class Label(jjm.core.model.Model):
	@jjm.core.model.short_url('LabelID', SHORT_URL)
	@jjm.core.model.open_query
	def get(self):
		return ('SELECT * FROM label '
				'ORDER BY name', [])

	@jjm.core.model.short_url('LabelID', SHORT_URL)
	@jjm.core.model.open_query
	def get_parent(self, label_id):
		return ('SELECT * FROM label '
				'WHERE labelid = %s',
				[label_id])
	
	@jjm.core.model.short_url('LabelID', SHORT_URL)
	@jjm.core.model.open_query
	def get_children(self, label_id):
		return ('SELECT * FROM label '
				'WHERE parentid = %s',
				[label_id])
		
	@jjm.core.model.first
	@jjm.core.model.short_url('LabelID', SHORT_URL)
	@jjm.core.model.open_query
	def get_by_id(self, label_id):
		return ('SELECT * FROM label '
				'WHERE labelid = %s', 
				[label_id])

	@jjm.core.model.exec_query
	def add(self, name, parent_id):
		return ('INSERT INTO label (name, parentid) '
				'VALUES (%s, %s)',
				[name, parent_id or None])

	@jjm.core.model.exec_query
	def update(self, label_id, name, parent_id):
		return ('UPDATE label '
				'SET name = %s, parentid = %s '
				'WHERE labelID=%s',
				[name, parent_id or None, label_id])

	@jjm.core.model.exec_query
	def delete(self, label_id):
		return ('DELETE FROM label '
				'WHERE labelid = %s',
				[labelID])
