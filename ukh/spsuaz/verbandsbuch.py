from .components import SUnfallanzeigen, ISUnfallanzeige
from dolmen.forms.base.utils import set_fields_data
from uvc.unfallanzeige.uazwizard import Unfallanzeige
from uvc.unfallanzeige.verbandsbuch import AddVerbandsbuch, IVerbandbuchEintrag
from zope import interface
import grok
import uvcsite
import zope.component


grok.templatedir('templates')


class AddVerbandsbuch(AddVerbandsbuch):
    grok.context(SUnfallanzeigen)
    label = u"Verbandsbuch"

    @property
    def macros(self):
        return zope.component.getMultiAdapter(
            (self.context, self.request),
            name='fieldmacros'
        ).template.macros

    @uvcsite.action('Ins Versandbuch eintragen.')
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            return
        uaz = Unfallanzeige()
        set_fields_data(ISUnfallanzeige, uaz, data)
        interface.alsoProvides(uaz, IVerbandbuchEintrag)
        interface.alsoProvides(uaz, ISUnfallanzeige)
        self.context.add(uaz)
        self.flash(u'Ihr Eintrag wurde erstellt')
        self.redirect(self.url(self.context))
