tex_key_list = [
# name, trigger, content
    # commands
    ['alter'],
    ['create'],
    ['delete'],
    ['drop'],
    ['insert'],
    ['select'],
    ['truncate'],
    ['update'],
    # preps
    ['as'],
    ['asc'],
    ['begin'],
    ['between'],
    ['by'],
    ['case'],
    ['desc'],
    ['distinct'],
    ['end'],
    ['from'],
    ['full join'],
    ['group by'],
    ['having'],
    ['inner join'],
    ['into'],
    ['join'],
    ['left join'],
    ['limit'],
    ['on'],
    ['offset'],
    ['order by'],
    ['return'],
    ['returns'],
    ['right join'],
    ['set'],
    ['when'],
    ['where'],
    ['with'],
    ['outer join'],
    ['over'],
    ['partition by'],
    ['union'],
    # nouns
    ['null'],
    ['function'],
    ['table'],
    ['values'],
    ['view'],
    # functions
    ['avg'],
    ['count'],
    ['datediff'],
    ['dense_rank'],
    ['ifnull'],
    ['min'],
    ['max'],
    ['mod'],
    ['pivot'],
    ['rank'],
    ['row_number'],
    ['round'],
    ['sum'],
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