import grok
import uvcsite
from megrok.z3ctable import Column, table
from uvcsite.interfaces import IFolderListingTable
from uvc.unfallanzeige.interfaces import IUnfallanzeigenFolder

grok.templatedir('templates')


class SelectUAZ(uvcsite.Page):
    grok.context(uvcsite.IUVCSite)

    def getLink(self, suffix):
        return "%s/Sunfallanzeigen/%s" % (
            uvcsite.getHomeFolderUrl(self.request), suffix)


class UTagColumn(Column):
    grok.name('utag')
    grok.context(IUnfallanzeigenFolder)
    header = u"Unfalltag"
    weight = 200
    table(IFolderListingTable)

    def renderCell(self, item):
        if item.unfdatum is not None:
            udat = item.unfdatum
        else:
            udat = ''
        return udat


class NamColumn(Column):
    grok.name('unam')
    grok.context(IUnfallanzeigenFolder)
    header = u"Name"
    weight = 200
    table(IFolderListingTable)

    def renderCell(self, item):
        if item.prsvor is not None:
            name = str(item.prsvor) + ' ' + str(item.prsname)
        else:
            name = ''
        return name
