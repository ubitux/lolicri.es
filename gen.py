#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loli_list import lolis

TPL_BASE = '''<!DOCTYPE html>
<html>
 <head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <title>Loli Cries!</title>
  <meta name="viewport" content="width=device-width" />
  <link rel="stylesheet" type="text/css" href="style.css" />
  <link rel="icon" type="image/png" href="favicon.png" />
 </head>
 <body>
  <header>
   <hgroup>
    <h1>Loli Cries!</h1>
    <h2>The internet loli database</h2>
   </hgroup>
  </header>
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

print('Build www/index.html')
content = '<section id="lolis">'
for loli in lolis:
    loli['cries'] = ''.join(TPL_CRY % cry for cry in loli['cries'])
    content += TPL_LOLI % loli
content += '</section>'
open('www/index.html','w').write(TPL_BASE % {'content': content})
