tex_key_list = [
# name, trigger, content
    # commands
    ['alter'],
    ['create'],
    ['delete'],
    ['drop'],
    ['insert'],
    ['select'],
    ['update'],
    # preps
    ['as'],
    ['asc'],
    ['begin'],
    ['between'],
    ['by'],
    ['desc'],
    ['distinct'],
    ['end'],
    ['from'],
    ['group by'],
    ['having'],
    ['into'],
    ['limit'],
    ['on'],
    ['offset'],
    ['order by'],
    ['return'],
    ['returns'],
    ['set'],
    ['where'],
    # nouns
    ['null'],
    ['function'],
    ['table'],
    ['values'],
    ['view'],
    # functions
    ['avg',     'avg',      'avg($0)'],
    ['count',   'count',    'count'],
    ['ifnull',  'ifnull',   'ifnull($0)'],
    ['min',     'min',      'min($0)'],
    ['max',     'max',      'max($0)'],
    ['sum',     'sum',      'sum($0)'],
]

scope = "source.sql"
for item in tex_key_list:
    content = item[-1]
    if len(item) == 1:
        name, trigger, content = item[-1], item[-1], item[-1]
    elif len(item) == 2:
        name, trigger, content = item[0], item[-1], item[-1]
    else:
        name, trigger, content = item[0], item[1], item[2]
    fname = 'C:/Users/yzh/AppData/Roaming/Sublime Text 3/Packages/SQL/snippets/{}.sublime-snippet'.format(name)
    with open(fname, 'w') as wf:
        snippet_str = """<snippet>\n<content><![CDATA[{}]]></content>\n<tabTrigger>{}</tabTrigger>\n<scope>{}</scope>\n<description>sql: {}</description>\n</snippet>""".format(content, trigger, scope, name)
        wf.write(snippet_str)