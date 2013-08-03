import webob

import core
import musicdb.model.db
import musicdb.view.artist
import musicdb.view.label
import musicdb.view.graph

class ArtistBase(core.Resource):
	def get_related(self, db, artist_id):
		tried = [artist_id]
		result = db.artist.get_related(artist_id)
		while len(tried) < len(result):
			for related in result:
				if related.ArtistID not in tried:
					new_recs = db.artist.get_related(related.ArtistID)
					for new_rec in new_recs:
						if not any(r.ArtistID == new_rec.ArtistID for r in result):
							result.append(new_rec)
					tried.append(related.ArtistID)
		return result
		
class Artist(ArtistBase):
	@core.xslt
	def GET(self, request, artist_id):
		db = musicdb.model.db.DB()
		related = self.get_related(db, artist_id)
		core.debug(request, `related`+'\n')
		return webob.Response(body=musicdb.view.artist.artist_list(related))

class ArtistAsGraph(ArtistBase):
	def GET(self, request, artist_id):
		db = musicdb.model.db.DB()
		artists = self.get_related(db, artist_id)
		for artist in artists:
			if not artist.AliasID: # dan zal het wel een groep zijn, leden ophalen
				artist['Members'] = [a.ArtistID for a in db.artist.get_group_members(artist.ArtistID)]
			else:
				artist['Members'] = []
		graph = dict(
			(a.ArtistID, ([a.AliasID] if a.AliasID else []) + a.Members)
			for a in artists)
		node_text = dict((a.ArtistID, a.Name) for a in artists)
		core.debug(request, repr(graph)+'\n')
		core.debug(request, repr(node_text)+'\n')
		return webob.Response(
			body=musicdb.view.graph.draw_graph(graph, node_text, directed=False),
			content_type='image/png',
			cache_control='no-store, no-cache')			

class LabelBase(core.Resource):
	def get_all_children(self, db, label_node):
		yield label_node
		for label in db.label.get_children(label_node.LabelID):
			for label_child in self.get_all_children(db, label):
				yield label_child
				
	def find_related(self, db, label_id):
		root = db.label.get_by_id(label_id)
		while root.ParentID:
			root = db.label.get_by_id(root.ParentID)
		return list(self.get_all_children(db, root))

class Label(LabelBase):		
	@core.xslt
	def GET(self, request, label_id):
		db = musicdb.model.db.DB()
		return webob.Response(
			body=musicdb.view.label.label_list(self.find_related(db, label_id)))

class LabelAsGraph(LabelBase):
	def GET(self, request, label_id):
		db = musicdb.model.db.DB()
		labels = self.find_related(db, label_id)
		graph = dict(
			(l.LabelID, [l.ParentID] if l.ParentID else [])
			for l in labels)
		node_text = dict((l.LabelID, l.Name) for l in labels)
		return webob.Response(
			body=musicdb.view.graph.draw_graph(graph, node_text, selected=label_id),
			content_type='image/png',
			cache_control='no-store, no-cache')
			
