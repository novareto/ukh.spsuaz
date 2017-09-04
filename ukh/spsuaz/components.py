import re
import grok
import uvcsite

from uvc.unfallanzeige.uazwizard import Unfallanzeigen, Adder, Unfallanzeige
# from uvc.unfallanzeige.uazwizard import UnfallanzeigeWizard
from uvc.unfallanzeige.interfaces import IUnfallanzeige
from zope.interface import alsoProvides
from zope.lifecycleevent import ObjectCreatedEvent
from uvc.unfallanzeige import steps
from uvc.unfallanzeige.resources import uazjs, uazcss
from zope.schema import Text
from zeam.form.base.errors import Error
from zeam.form.base.markers import NO_VALUE


class ISUnfallanzeige(IUnfallanzeige):

    prsvtr = Text(
        title=u'Gesetzlicher Vertreter',
        description=u'Name und Anschrift der gesetzlichen Vertreter',
        required=False,
    )


class SUnfallanzeigen(Unfallanzeigen):
    pass


class Adder(Adder):
    grok.context(SUnfallanzeigen)

    def update(self):
        uaz = Unfallanzeige()
        alsoProvides(uaz, ISUnfallanzeige)
        self.uaz = uaz
        grok.notify(ObjectCreatedEvent(uaz))
        self.context.add(uaz)


class UnfallanzeigenWizard(uvcsite.Wizard):
    """ Wizard form."""
    grok.context(ISUnfallanzeige)
    grok.name('edit')
    label = u""

    def update(self):
        super(UnfallanzeigenWizard, self).update()
        uazjs.need()
        uazcss.need()


class Basic(steps.Basic):
    grok.context(ISUnfallanzeige)
    grok.view(UnfallanzeigenWizard)

    def update(self):
        super(Basic, self).update()


class Person(steps.Person):
    grok.context(ISUnfallanzeige)
    grok.view(UnfallanzeigenWizard)
    label = u'Angaben zur versicherten Person'
    fields = uvcsite.Fields(ISUnfallanzeige).select(
        'prsname', 'prsvor', 'ikstr', 'iknr', 'ikzplz', 'ikzort', 'lkz',
        'prsgeb', 'prssex', 'prssta')

    kifields = uvcsite.Fields(ISUnfallanzeige).select('prsvtr')
    fields = kifields + fields
    fields['prssex'].mode = 'radio'

    def update(self):
        super(Person, self).update()
        #kitextwidgetcss.need()
        #seite2js.need()

    def validateStep(self, data, errors):
        super(Person, self).validateStep(data, errors)
        plz = data.get('ikzplz')
        if plz != NO_VALUE:
            checkplz = re.compile(r'^([0]{1}[1-9]{1}|[1-9]{1}[0-9]{1})[0-9]{3}$').match
            if not bool(checkplz(plz)):
                errors.append(Error(
                    u'Die eingegebene Postleitzahl entspricht nicht dem geforderten Format.',
                    identifier='form.person.field.ikzplz'))
        return errors
