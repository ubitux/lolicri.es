#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loli_list import lolis
import re, sys, unicodedata


LOLI_PER_PAGE = 10

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
   <h1><a href="%(link)s">%(name)s</a></h1>
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
    norm = re.sub('[^\w\s-]', '', norm).strip().lower()
    return re.sub('[-\s]+', '-', norm)

def loli_template(loli):
    l = dict(loli)
    l['cries'] = ''.join(TPL_CRY % cry for cry in l['cries'])
    l['anchor'] = get_loli_anchor(l)
    l['link']  = 'loli-' + l['anchor'] + '.html'
    return TPL_LOLI % l

def loli_list(src, start=0, count=0):
    content = ''
    for loli in lolis[start:start+count]:
        content += loli_template(loli)
    return content

def rss_content(src):
    content = ''
    for loli in lolis[::-1]:
        loli['title'] = 'New wild loli appears: %s' % loli['name']
        loli['guid']  = 'loli-' + get_loli_anchor(loli)
        loli['link']  = 'http://lolicri.es/%s.html' % loli['guid']
        content += TPL_RSS_ITEM % loli
    return content

def default_content(src):
    return open(src).read()

def nav_gen(baseurl, page_name):
    nav = ''
    for page in pages:
        if 'nav' not in page: continue
        active = ' class="active"' if page_name.endswith(page['fname']) else ''
        nav += '<li><a href="%s/%s" %s>%s</a></li>' % (baseurl, page['fname'], active, page['nav'])
    return nav

def page_gen(page, src, dst):
    src = src + page['fname']
    dst = dst + page['fname']
    print('Writing %s' % dst)

    data = {}
    data['content'] = page.get('func', default_content)(src)
    data['title'  ] = 'Loli Cries!' + (' - '+page['title'] if 'title' in page else '')
    data['header' ] = '<h2>%s</h2>' % page['header'] if 'header' in page else ''
    data['nav'    ] = nav_gen(baseurl, dst)
    data['baseurl'] = baseurl
    open(dst, 'w').write(page.get('tpl', TPL_BASE) % data)

def loli_index_gen(page, src, dst):
    def next_page(n, p):
        if (n != (p-1)) and (p > 1):
            url = '<a href="./index-%d.html">Next&thinsp;&gt;&gt;</a>' % (n+1)
        else:
            url = 'Next&thinsp;&gt;&gt;'
        return '<li>%s</li>' % url

    def prev_page(n, p):
        if n == 0:
            url = '&lt;&lt;&thinsp;Previous'
        elif n == 1:
            url ='<a href="./index.html">&lt;&lt;&thinsp;Previous</a>'
        else:
            url = '<a href="./index-%d.html">&lt;&lt;&thinsp;Previous</a>' % (n-1)
        return '<li>%s</li>' % url

    lolis.reverse()

    data = {}
    data['title'  ] = 'Loli Cries!' + (' - '+page['title'] if 'title' in page else '')
    data['header' ] = '<h2>%s</h2>' % page['header'] if 'header' in page else ''
    data['baseurl'] = baseurl

    l = len(lolis)
    l = l/LOLI_PER_PAGE if (l%LOLI_PER_PAGE) == 0 else (l/LOLI_PER_PAGE) + 1
    f, e = page['fname'].split('.')
    for p in range(l):
        if p == 0:
            fname = page['fname']
        else:
            fname = "%s-%d.%s" % (f, p, e)

        print('Writing %s' % dst + fname)
        pp = prev_page(p, l)
        np = next_page(p, l)
        data['content']  = '<section id="lolis">%s</section>' % loli_list(src, p*LOLI_PER_PAGE, LOLI_PER_PAGE)
        data['content'] += '<nav><ul>' + pp + '<li><a href="#lolis">*Top*</a></li>' + np + '</ul></nav>'
        data['nav'    ]  = pp + nav_gen(baseurl, dst) + np
        open(dst + fname, 'w').write(page.get('tpl', TPL_BASE) % data)

def loli_page_gen(page, src, dst):
    for loli in lolis:
        fname = dst + page['fname'] % get_loli_anchor(loli)
        print('Writing %s' % fname)

        data  = {}
        lname = '%(name)s from %(anime)s' % loli
        data['title'  ] = page['title'] % lname
        data['header' ] = '<h2>%s</h2>' % lname
        data['nav'    ] = nav_gen(baseurl, dst)
        data['baseurl'] = baseurl
        data['content'] = '<section id="lolis">%s</section>' % loli_template(loli)
        open(fname, 'w').write(page.get('tpl', TPL_BASE) % data)

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
#     'gen':    the function to actually write the page.
#     'header': what appears as a sub title on top of the page (not mandatory)
#     'title':  HTML title tag content.
#     'tpl':    template to use if not TPL_BASE
#
pages = [{
    'nav':    'Lolis',
    'header': 'The internet loli database',
    'fname':  'index.html',
    'func':   loli_list,
    'gen':    loli_index_gen,
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
    'title':  '%s - The internet loli database',
    'fname':  'loli-%s.html',
    'gen':    loli_page_gen,
},{
    'fname':  'rss.xml',
    'func':   rss_content,
    'tpl':    TPL_RSS,
}]


baseurl = sys.argv[1] if len(sys.argv) > 1 else '.'
print 'Using `%s` as base url' % baseurl
for page in pages:
    src = 'src/'
    dst = 'www/'
    page.get('gen', page_gen)(page, src, dst)
