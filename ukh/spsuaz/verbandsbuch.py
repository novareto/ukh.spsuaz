
import grok
import uvcsite
import zope.component

from zope import interface
from ukhtheme.grok.layout import ILayer
from .resources import verbandbuch_js, verbandbuch_css
from dolmen.forms.base.utils import set_fields_data
from uvc.unfallanzeige.uazwizard import Unfallanzeige
from .components import SUnfallanzeigen, ISUnfallanzeige
from uvc.unfallanzeige.verbandsbuch import AddVerbandbuch, IVerbandbuchEintrag
from uvc.unfallanzeige.verbandsbuch import Edit as EditVerbandbuch


grok.templatedir('templates')


class AddVerbandbuch(AddVerbandbuch):
    grok.context(SUnfallanzeigen)
    label = u"Verbandbuch"

    def update(self):
        verbandbuch_js.need()
        verbandbuch_css.need()

    @property
    def macros(self):
        return zope.component.getMultiAdapter(
            (self.context, self.request),
            name='fieldmacros'
        ).template.macros

    @uvcsite.action('Eintrag ins Verbandbuch')
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            return
        data['title'] = u'Unfall ' + data['prsname'] + ' ' + data['prsvor']
        uaz = Unfallanzeige()
        set_fields_data(ISUnfallanzeige, uaz, data)
        interface.alsoProvides(uaz, IVerbandbuchEintrag)
        interface.alsoProvides(uaz, ISUnfallanzeige)
        self.context.add(uaz)
        self.flash(u'Ihr Eintrag wurde erstellt')
        self.redirect("%s?filter=vb" % self.url(self.context))

    @uvcsite.action(u'Abbrechen')
    def handle_cancel(self):
        self.flash('Die Aktion wurde abgebrochen.')
        self.redirect(self.application_url())


class EditVerbandbuch(EditVerbandbuch):
    grok.context(IVerbandbuchEintrag)
    label = u"Verbandbuch"
    grok.layer(ILayer)
    grok.name('edit')

    def update(self):
        verbandbuch_js.need()
        verbandbuch_css.need()

    @property
    def macros(self):
        return zope.component.getMultiAdapter(
            (self.context, self.request),
            name='fieldmacros'
        ).template.macros

    #@uvcsite.action(u'Abbrechen')
    #def handle_cancel(self):
    #    self.flash('Die Aktion wurde abgebrochen.')
    #    self.redirect(self.application_url())

