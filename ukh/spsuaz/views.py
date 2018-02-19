import grok
import uvcsite


grok.templatedir('templates')


class SelectUAZ(uvcsite.Page):
    grok.context(uvcsite.IUVCSite)

    def getLink(self, suffix):
        return "%s/Sunfallanzeigen/%s" %(uvcsite.getHomeFolderUrl(self.request), suffix)
