# coding: utf-8

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
from zope.schema import Text, TextLine
from zeam.form.base.errors import Error
from zeam.form.base.markers import NO_VALUE

from uvc.unfallanzeige.verbandsbuch import MetaTypeColumn
from resources import seite1css, seite2css, seite3css, seite4css, seite5css
from resources import seite2js, seite3js, seite4js
from resources import buttonjs
from uvcsite.viewlets.steps import StepsProgressBar
from zope.interface import Interface

grok.templatedir('templates')


class ISUnfallanzeige(IUnfallanzeige):

    traeger = TextLine(
        title=u'Träger der Einrichtung',
        description=u'Name des Trägers der Einrichtung',
        required=True
    )

    prsvtr = Text(
        title=u'Gesetzlicher Vertreter',
        description=u'Name und Anschrift der gesetzlichen Vertreter',
        required=False,
    )


class SUnfallanzeigen(Unfallanzeigen):
    pass


class MetaTypeColumn(MetaTypeColumn):
    grok.context(SUnfallanzeigen)


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


class StepsProgressBar1(StepsProgressBar):
    grok.context(Interface)
    grok.view(UnfallanzeigenWizard)
    grok.viewletmanager(uvcsite.IAboveContent)


#class Overview(steps.Overview):
#    grok.context(ISUnfallanzeige)
#    grok.view(UnfallanzeigenWizard)


class Basic(steps.Basic):
    grok.context(ISUnfallanzeige)
    grok.view(UnfallanzeigenWizard)

    @property
    def fields(self):
        fields1 = uvcsite.Fields(ISUnfallanzeige).select('title')
        fields3 = uvcsite.Fields(ISUnfallanzeige).select('anspname', 'anspfon')
        fields2 = uvcsite.Fields(ISUnfallanzeige).select('traeger')
        fields4 = uvcsite.Fields(ISUnfallanzeige).select('unfus2')
        fields1['title'].htmlAttributes = {'maxlength': 70}
        fields2['traeger'].htmlAttributes = {'maxlength': 70}
        fields3['anspname'].htmlAttributes = {'maxlength': 30}
        fields3['anspfon'].htmlAttributes = {'maxlength': 20}
        fields4['unfus2'].htmlAttributes = {'maxlength': 30}
        fields4['unfus2'].title = u'Leiter (Beauftragter) der Einrichtung'
        fields4['unfus2'].description = u''
        return fields1 + fields2 + fields3 + fields4

    def update(self):
        super(Basic, self).update()
        seite1css.need()


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
    fields['prsname'].htmlAttributes = {'maxlength': 30}
    fields['prsvor'].htmlAttributes = {'maxlength': 30}
    fields['ikstr'].htmlAttributes = {'maxlength': 30}
    fields['iknr'].htmlAttributes = {'maxlength': 10}
    fields['ikzplz'].htmlAttributes = {'maxlength': 5}
    fields['ikzort'].htmlAttributes = {'maxlength': 30}
    fields['prsgeb'].htmlAttributes = {'maxlength': 10}

    def update(self):
        super(Person, self).update()
        seite2css.need()
        seite2js.need()

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


class AccidentI(steps.AccidentI):
    grok.context(ISUnfallanzeige)
    grok.view(UnfallanzeigenWizard)

    fields = uvcsite.Fields(ISUnfallanzeige).select(
        'unfdatum', 'unfzeit', 'unfort', 'unfhg1', 'unfhg2', 'unfkn1',
        'unfkn2')

    fields['unfhg2'].mode = 'radio'
    fields['unfkn2'].mode = 'radio'

    def update(self):
        super(AccidentI, self).update()
        seite3css.need()
        seite3js.need()


class AccidentII(steps.AccidentII):
    grok.context(ISUnfallanzeige)
    grok.view(UnfallanzeigenWizard)

    fields = uvcsite.Fields(ISUnfallanzeige).select(
        'prstkz', 'unfae1', 'unfaedatum', 'unfaezeit',
        'unfwa1', 'unfwax', 'uadbavon', 'uadbabis',
        'diavkt', 'diaadv', 'unfeba', 'unfeba1')

    fields['prstkz'].mode = 'radio'
    fields['unfae1'].mode = 'radio'
    fields['unfwa1'].mode = 'radio'
    fields['unfeba'].mode = 'radio'
    fields['diavkt'].htmlAttributes = {'maxlength': 60}
    fields['diaadv'].htmlAttributes = {'maxlength': 60}

    def update(self):
        super(AccidentII, self).update()
        self.fields.get('unfae1').title = u'Hat der Versicherte den Besuch der Einrichtung unterbrochen?'
        self.fields.get('unfae1').description = u""
        self.fields.get('unfwa1').title = u'Hat der Versicherte den Besuch der Einrichtung wieder aufgenommen?'
        self.fields.get('unfwa1').description = u""
        self.fields.get('unfwax').title = u'Wenn ja: Aufgenommen am Datum (tt.mm.jjjj)'
        self.fields.get('unfwax').description = u""
        self.fields.get('uadbavon').title = u'Der Besuch der Einrichtung beginnt um Uhrzeit (hh:mm)'
        self.fields.get('uadbavon').description = u""
        self.fields.get('uadbabis').title = u'und endet um Uhrzeit (hh:mm)'
        self.fields.get('uadbabis').description = u""
        seite4css.need()
        seite4js.need()

    def validateStep(self, data, errors):
        super(AccidentII, self).validateStep(data, errors)
        if data.get('prstkz') == 'nein':
            if data.get('unfae1') == NO_VALUE:
                errors.append(Error(
                    u'Bitte machen Sie Angaben in diesem Feld.',
                    identifier='form.accidentii.field.unfae1'))
        if data.get('unfae1') == "ja, sofort":
            if data.get('unfwa1') == NO_VALUE:
                errors.append(Error(
                    u'Bitte machen Sie Angaben in diesem Feld.',
                    identifier='form.accidentii.field.unfwa1'))
            if data.get('unfwa1') == "ja":
                if data.get('unfwax') == NO_VALUE:
                    errors.append(Error(
                        u'Bitte machen Sie Angaben in diesem Feld.',
                        identifier='form.accidentii.field.unfwax'))
        if data.get('unfae1') == "ja, spaeter am:":
            if data.get('unfwa1') == NO_VALUE:
                errors.append(Error(
                    u'Bitte machen Sie Angaben in diesem Feld.',
                    identifier='form.accidentii.field.unfwa1'))
            if data.get('unfwa1') == "ja":
                if data.get('unfwax') == NO_VALUE:
                    errors.append(Error(
                        u'Bitte machen Sie Angaben in diesem Feld.',
                        identifier='form.accidentii.field.unfwax'))
            if data.get('unfaedatum') == NO_VALUE:
                errors.append(Error(
                    u'Bitte machen Sie Angaben in diesem Feld.',
                    identifier='form.accidentii.field.unfaedatum'))
            if data.get('unfaezeit') == NO_VALUE:
                errors.append(Error(
                    u'Bitte das Feld Zeit ausfüllen. Beispiel: hh:mm (h = Stunde, m = Minute), bitte beachten Sie den Doppelpunkt.',
                    identifier='form.accidentii.field.unfaedatum'))
            if data.get('unfaezeit') == None:
                errors.append(Error(
                    u'Die eingegebene Zeit entspricht nicht dem geforderten Format, bitte beachten Sie den Doppelpunkt.',
                    identifier='form.accidentii.field.unfaedatum'))
            if data.get('unfaezeit') == "":
                errors.append(Error(
                    u'Die eingegebene Zeit entspricht nicht dem geforderten Format, bitte beachten Sie den Doppelpunkt.',
                    identifier='form.accidentii.field.unfaedatum'))
        if data.get('uadbabis') == NO_VALUE:
            errors.append(Error(
                u'Bitte das Feld Zeit ausfüllen.',
                identifier='form.accidentii.field.uadbavon'))
        if data.get('uadbabis') == None :
            errors.append(Error(
                u'Die eingegebene Zeit entspricht nicht dem geforderten Format, bitte beachten Sie den Doppelpunkt.',
                identifier='form.accidentii.field.uadbavon'))
        return errors


class BasicInformation(steps.BasicInformation):
    grok.context(ISUnfallanzeige)
    grok.view(UnfallanzeigenWizard)
    label = u'Versand und Druck der Unfallanzeige'
    fields = uvcsite.Fields(ISUnfallanzeige).select('behandlung')
    #fields = uvcsite.Fields(ISUnfallanzeige).select('unfus2', 'behandlung')
    fields['behandlung'].mode = "radio"

    def update(self):
        super(BasicInformation, self).update()
        buttonjs.need()
        #self.fields.get('unfus2').title = u'Leiter (Beauftragter) der Einrichtung'
        #self.fields.get('unfus2').description = u""
        #seite5css.need()

    #@uvcsite.action(u'Abbrechen')
    #def handle_cancel(self):
    #    self.flash('Die Aktion wurde abgebrochen.')
    #    self.redirect(self.application_url())




class Index(uvcsite.Page):
    grok.require('uvc.ViewContent')
    grok.context(ISUnfallanzeige)
