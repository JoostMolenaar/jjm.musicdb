#!/usr/bin/python

import os

import pygraphviz as pg

def draw_graph(nodes, labels, selected=None, directed=False):
	nodes = dict((k, dict((e,None) for e in v))
		for (k,v) in nodes.items())

	filename = '/tmp/musicdb-graph-{0}.png'.format(os.getpid())

	graph = pg.AGraph(nodes, strict=False, directed=directed, overlap=False, rankdir='BT', charset='utf8')
	for key in nodes.keys():
		node = graph.get_node(key)
		node.attr['label'] = labels[key].encode('utf8')
		node.attr['shape'] = 'box'
		node.attr['height'] = 0.0
		node.attr['fontsize'] = 10.0
	
	if selected:
		graph.get_node(selected).attr['style'] = 'filled'
		graph.get_node(selected).attr['fillcolor'] = 'yellow'
		
	graph.layout(prog='dot')
	graph.draw(filename)

	try:
		with open(filename, 'rb') as f:
			return f.read()
	finally:
		os.remove(filename)

if __name__ == '__main__':
	d = {'1': ['Foo'],
		 'Foo': ['1', 'Bar'],
		 'Bar': ['Foo']}
	b = draw_graph(d)
	with open('graph.png','wb') as f:
		f.write(b)
