import uvcsite
import grok


class UnfallanzeigeRegistration(uvcsite.ProductRegistration):
    grok.name('KinderUnfallanzeige')
    grok.title('Kinder Unfallanzeige')
    grok.description('Kinder Unfallanzeige')
    grok.order(51)
    uvcsite.productfolder('ukh.spsuaz.components.SUnfallanzeigen')
    icon = "fanstatic/ukh.spsuaz/uaz_ki.png"

    def action(self):
        return "%sSunfallanzeigen/add" % uvcsite.getHomeFolderUrl(self.request)
