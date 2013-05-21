#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loli_list import lolis
import sys, unicodedata

TPL_BASE = '''<!DOCTYPE html>
<html>
 <head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <title>%(title)s</title>
  <meta name="viewport" content="width=device-width" />
  <link rel="stylesheet" type="text/css"            href="%(baseurl)s/style.css" />
  <link rel="icon"       type="image/png"           href="%(baseurl)s/favicon.png" />
  <link rel="alternate"  type="application/rss+xml" href="%(baseurl)s/rss.xml" />
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
   <p class="loli❤">2010-2013 - The loli ❤ team</p>
  </footer>
 </body>
</html>'''

TPL_CRY = '''
<dt>%s</dt>
<dd><audio preload="none" src="%s" controls="controls"></audio></dd>'''

TPL_LOLI = '''
<article id="%(anchor)s">
 <header>
  <hgroup>
   <h1><a href="#%(anchor)s">%(name)s</a></h1>
   <h2>%(anime)s</h2>
  </hgroup>
 </header>
 <img src="%(pic)s" alt="" />
 <dl>%(cries)s</dl>
</article>'''

TPL_RSS = '''<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
 <channel>
  <title>%(title)s</title>
  <link>http://lolicri.es</link>
  <description>%(title)s</description>
  <atom:link href="http://lolicri.es/rss.xml" rel="self" type="application/rss+xml" />
  %(content)s
 </channel>
</rss>
'''

TPL_RSS_ITEM = '''
  <item>
   <title>%(title)s</title>
   <link>%(link)s</link>
   <guid>%(guid)s</guid>
  </item>
'''

def get_loli_anchor(loli):
    key  = '%(anime)s-%(name)s' % loli
    norm = unicodedata.normalize('NFKD', key.decode('utf-8')).encode('ascii', 'ignore')
    return '-'.join(norm.lower().split())

def loli_list(src):
    content = '<section id="lolis">'
    for loli in lolis:
        loli['cries'] = ''.join(TPL_CRY % cry for cry in loli['cries'])
        loli['anchor'] = get_loli_anchor(loli)
        content += TPL_LOLI % loli
    content += '</section>'
    return content

def rss_content(src):
    content = ''
    for loli in lolis[::-1]:
        loli['title'] = 'New wild loli appears: %s' % loli['name']
        loli['link']  = 'http://lolicri.es/#' + get_loli_anchor(loli)
        loli['guid']  = loli['link']
        content += TPL_RSS_ITEM % loli
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
#     'tpl':    template to use if not TPL_BASE
#
pages = [{
    'nav':    'Lolis',
    'header': 'The internet loli database',
    'fname':  'index.html',
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
},{
    'fname':  'rss.xml',
    'func':   rss_content,
    'tpl':    TPL_RSS,
}]

def nav_gen(baseurl, page_name):
    nav = ''
    for page in pages:
        if 'nav' not in page: continue
        active = ' class="active"' if page_name.endswith(page['fname']) else ''
        nav += '<li><a href="%s/%s" %s>%s</a></li>' % (baseurl, page['fname'], active, page['nav'])
    return nav

def page_gen(page):
    data = {}
    data['content'] = page.get('func', default_content)(src)
    data['title'  ] = 'Loli Cries!' + (' - '+page['title'] if 'title' in page else '')
    data['header' ] = '<h2>%s</h2>' % page['header'] if 'header' in page else ''
    data['nav'    ] = nav_gen(baseurl, dst)
    data['baseurl'] = baseurl
    open(dst, 'w').write(page.get('tpl', TPL_BASE) % data)

baseurl = sys.argv[1] if len(sys.argv) > 1 else '.'
print 'Using `%s` as base url' % baseurl
for page in pages:
    src = 'src/' + page['fname']
    dst = 'www/' + page['fname']
    print('Writing %s' % dst)
    page.get('gen', page_gen)(page)
