#!/usr/bin/env python
# -*- coding: utf-8 -*-
# hilfe.py
import grok
import uvcsite

from zope import interface
from uvc.unfallanzeige.interfaces import IUnfallanzeige
from components import ISUnfallanzeige
from zope.app.renderer.rest import ReStructuredTextToHTMLRenderer
from ukh.spsuaz.components import UnfallanzeigenWizard

# template dir
grok.templatedir('templates')


#class KiAllgemeineHilfeUAZ(uvcsite.HelpPage):
#    grok.context(ISUnfallanzeige)
#    ahuaz = ""
#    grok.order(200)
#    name = u"Allgemeine Erläuterung zur Unfallanzeige"
#
#    def update(self):
#        self.ahuaz = "templates/kiallgemeine-hilfe.rst"
#
#    def render(self):
#        template = grok.PageTemplateFile(self.ahuaz)
#        renderer = ReStructuredTextToHTMLRenderer(template.render(self), None)
#        return renderer.render()

class ContextBasedHelp(uvcsite.HelpPage):
    grok.context(ISUnfallanzeige)
    grok.view(UnfallanzeigenWizard)
    help_rst = ""

    def update(self):
        if hasattr(self.view, 'current'):
            self.help_rst = "templates/%s.rst" % str(self.view.current.id).replace('.', '-')

    def render(self):
        if self.help_rst:
            try:
                print self.help_rst
                template = grok.PageTemplateFile(self.help_rst)
                renderer = ReStructuredTextToHTMLRenderer(template.render(self), None)
                return renderer.render()
            except ValueError, e:
                pass
        return u"<h1> Keine Hilfe verfügbar </h1>"
