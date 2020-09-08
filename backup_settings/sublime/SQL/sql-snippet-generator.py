import platform
import os
import shutil

tex_key_list = [
# name, trigger, content
    # commands
    ['alter'],
    ['create'],
    ['delete'],
    ['drop'],
    ['insert'],
    ['replace'],
    ['rename'],
    ['select'],
    ['truncate'],
    ['update'],
    # preps
    ['add'],
    ['after'],
    ['as'],
    ['asc'],
    ['begin'],
    ['between'],
    ['by'],
    ['case'],
    ['desc'],
    ['distinct'],
    ['end'],
    ['following'],
    ['force index'],
    ['foreign'],
    ['from'],
    ['full join'],
    ['group by'],
    ['having'],
    ['ignore'],
    ['index'],
    ['indexed by'],
    ['inner join'],
    ['into'],
    ['join'],
    ['left join'],
    ['limit'],
    ['not'],
    ['on'],
    ['offset'],
    ['order by'],
    ['preceding'],
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
    ['unbounded'],
    ['union'],
    ['unique'],
    ['unique index'],
    # nouns
    ['datetime'],
    ['not null'],
    ['null'],
    ['function'],
    ['rows'],
    ['table'],
    ['trigger'],
    ['values'],
    ['view'],
    ['window'],
    # functions
    ['avg'],
    ['count'],
    ['datediff'],
    ['dense_rank'],
    ['ifnull'],
    ['length'],
    ['min'],
    ['max'],
    ['mod'],
    ['pivot'],
    ['rank'],
    ['row_number'],
    ['round'],
    ['strftime'],
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
    pc_name = platform.node()

    path_body = 'C:/Users/{}/AppData/Roaming/Sublime Text 3/Packages/SQL/'
    if pc_name == "DESKTOP-BQVCMQA":
        snippet_path = path_body.format("yuzeh") + "snippets/"
        syntax_path = path_body.format("yuzeh")
    else:
        snippet_path = path_body.format("yzh") + "snippets/"
        syntax_path = path_body.format("yzh")

    syntax_fname = "SQL.sublime-syntax"
    shutil.copyfile(syntax_path+syntax_fname, syntax_fname)
    if not os.path.exists(snippet_path):
        os.makedirs(snippet_path)
    fname = snippet_path + '{}.sublime-snippet'.format(name)
    with open(fname, 'w') as wf:
        snippet_str = """<snippet>\n<content><![CDATA[{}]]></content>\n<tabTrigger>{}</tabTrigger>\n<scope>{}</scope>\n<description>sql: {}</description>\n</snippet>""".format(content, trigger, scope, name)
        wf.write(snippet_str)