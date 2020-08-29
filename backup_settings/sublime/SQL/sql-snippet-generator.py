tex_key_list = [
    # name, trigger, content
    ['select', 'select', 'select'],
    ['ifnull', 'ifnull', 'ifnull'],
    ['where'],
    ['create'],
    ['drop'],
    ['alter'],
    ['group by'],
    ['order by'],
    ['distinct'],
    ['limit'],
    ['delete'],
    ['drop'],
    ['insert'],
    ['update'],
    ['table'],
    ['view'],
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