def label_list(labels):
	l = lambda l: ['label', ('uri', l.ShortURL), ('name', l.Name)]
	return ['labels'] + map(l, labels)

def label_form(labels, label=None):
	l = lambda l: ['label', ('labelID', l.LabelID), ('name', l.Name)]
	return ['label',
		('mode', label and 'edit' or 'add'),
		['uri', label and label.ShortURL or '/musicdb/label/new'],
		['img', label and label.ShortURL.replace('/musicdb/', '/musicdb/related/') + '.png' or ''],
		['name', label and label.Name or ''],
		['parent', label and label.ParentID and ('labelID', label.ParentID) or ''],
		['available'] + map(l, labels)
	]

