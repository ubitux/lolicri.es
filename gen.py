#!/usr/bin/env python
# -*- coding: utf-8 -*-

TPL_BASE = '''<!DOCTYPE html>
<html>
 <head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <title>%(title)s</title>
  <meta name="viewport" content="width=device-width" />
  <link rel="stylesheet" type="text/css" href="style.css" />
  <link rel="icon" type="image/png" href="favicon.png" />
 </head>
 <body>
  <header>
   <hgroup>
    <h1>Loli Cries!</h1>
    %(header)s
   </hgroup>
  </header>
  <nav>
   <ul>%(nav)s</ul>
  </nav>
  %(content)s
  <footer>
   <p>Comment/Submit/Request: #/dev/null @ irc.yozora-irc.net</p>
   <p class="loli❤">2010-2011 - The loli ❤ team</p>
  </footer>
 </body>
</html>'''

TPL_CRY = '''
<dt>%s</dt>
<dd><audio preload="none" src="%s" controls="controls"></audio></dd>'''

TPL_LOLI = '''
<article>
 <header>
  <hgroup>
   <h1>%(name)s</h1>
   <h2>%(anime)s</h2>
  </hgroup>
 </header>
 <img src="%(pic)s" alt="" />
 <dl>%(cries)s</dl>
</article>'''

def loli_list(src):
    from loli_list import lolis
    content = '<section id="lolis">'
    for loli in lolis:
        loli['cries'] = ''.join(TPL_CRY % cry for cry in loli['cries'])
        content += TPL_LOLI % loli
    content += '</section>'
    return content

def default_content(src):
    return open(src).read()

#
#   Page generation
#
#     'nav':    URL name which appears in the navigation bar. If not set,
#               the page won't appears in the bar.
#     'fname':  the source and destination filename. The source file must be
#               located in the src/ directory but may not exist (see "func").
#               The output file will be written in the www/ directory.
#     'func':   the function to call to get the content. If not set, it will
#               read the content of the source file using "fname".
#     'header': what appears as a sub title on top of the page (not mandatory)
#     'title':  HTML title tag content.
#
pages = [{
    'nav':    'Lolis',
    'header': 'The internet loli database',
    'fname': 'index.html',
    'func':   loli_list,
},{
    'nav':    'FAQ',
    'title':  'FAQ',
    'header': 'Freaking Atomic Questions',
    'fname':  'faq.html'
},{
    'title':  'Page not found',
    'header': 'Maho?',
    'fname':  '404.html',
}]

def nav_gen(page_name):
    nav = ''
    for page in pages:
        if 'nav' not in page: continue
        active = ' class="active"' if page_name.endswith(page['fname']) else ''
        nav += '<li><a href="%s" %s>%s</a></li>' % (page['fname'], active, page['nav'])
    return nav

for page in pages:
    src = 'src/' + page['fname']
    dst = 'www/' + page['fname']
    print('Write %s' % dst)

    data = {}
    data['content'] = page.get('func', default_content)(src)
    data['title'  ] = 'Loli Cries!' + (' - '+page['title'] if 'title' in page else '')
    data['header' ] = '<h2>%s</h2>' % page['header'] if 'header' in page else ''
    data['nav'    ] = nav_gen(dst)
    open(dst, 'w').write(TPL_BASE % data)
