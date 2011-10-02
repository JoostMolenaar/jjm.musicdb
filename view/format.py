def format_list(formats):
    f = lambda f: ['format', ('uri', f.ShortURL), ('name', f.Name)]
    return ['formats'] + map(f, formats)

def format_form(format=None):
    return ['format',
            ('mode', format and 'edit' or 'add'),
            ['uri', format and format.ShortURL or '/musicDB/format/new'],
            ['name', format and format.Name or '']]


