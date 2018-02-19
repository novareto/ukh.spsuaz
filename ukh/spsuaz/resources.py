# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2011 NovaReto GmbH

import grok

from js.jquery import jquery
from uvc.widgets import masked_input
from fanstatic import Library, Resource

library = Library('ukh.spsuaz', 'static')
seite1css = Resource(library, 'seite1.css')
seite2css = Resource(library, 'seite2.css')
seite3css = Resource(library, 'seite3.css')
seite4css = Resource(library, 'seite4.css')
seite5css = Resource(library, 'seite5.css')
seite2js = Resource(library, 'seite2.js', depends=[jquery])
seite3js = Resource(library, 'seite3.js', depends=[jquery])
seite4js = Resource(library, 'seite4.js', depends=[jquery])
verbandbuch_css = Resource(library, 'verbandbuch.css')
verbandbuch_js = Resource(library, 'verbandbuch.js', depends=[masked_input], bottom=True)
buttonjs = Resource(library, 'uazbuttons.js', depends=[jquery])
