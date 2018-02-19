import grok
import uvcsite


class UnfallanzeigeRegistration(uvcsite.ProductRegistration):
    grok.name('KinderUnfallanzeige')
    grok.title('Kinder Unfallanzeige')
    grok.description('Kinder Unfallanzeige')
    grok.order(51)
    uvcsite.productfolder('ukh.spsuaz.components.SUnfallanzeigen')

    def action(self):
        return "%sSunfallanzeigen/add" % uvcsite.getHomeFolderUrl(self.request)
