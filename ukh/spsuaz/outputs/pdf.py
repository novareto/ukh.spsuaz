#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ukh.kiunfallanzeige
# eKIUAZPDF.py

import grok
import tempfile

from reportlab.lib.units import cm
#from uvcsite import IStammdaten
#from ukh.markers.interfaces import IMitglied, IE2, IE3
from uvcsite.utils.dataviews import BasePDF
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.i18n import translate
from zope.dublincore.interfaces import IZopeDublinCore
from zope.pluggableauth.factories import Principal
from z3c.saconfig import Session
from sqlalchemy import and_
from sqlalchemy.sql import select
from ukh.schulportal.configs.database_setup import traegeruaz


def nN(value):
    if value == None:
        return ""
    return value


class KiDatenPDF(BasePDF):
    grok.name('kipdf')
    grok.title('Kinder-Unfallanzeige')

    def getFile(self, fn):
        if fn:
            return open(fn, 'w+b')
        return tempfile.TemporaryFile()

    def genpdf(self):
        '''
        PDF-File erzeugen
        '''
        context = self.context
        # Layout
        dc = IZopeDublinCore(context, None)
        if dc:
            creator = dc.creators[0]
            principal = Principal(creator, creator, creator)
        else:
            principal = self.request.principal
        #stammdaten = IStammdaten(self.request.principal)
        #adresse = stammdaten.getAdresse()
        adresse = self.request.principal.getAdresse()
        traegernr = u''
        oid = adresse['enroid']
        session = Session()
        s = select([traegeruaz], and_(traegeruaz.c.trgrcd == str(oid)))
        res = session.execute(s).fetchone()
        if res:
            traegernr = str(res['trgmnr']).strip()
        if res['trgna1'][:6] == 'PSEUDO':
            traegernr = ''
        c = self.c
        c.setAuthor("UKH")
        c.setTitle("Kinder-Unfallanzeige")
        schriftart = "Helvetica"
        schriftartfett = "Helvetica-Bold"
        # Titel
        c.setFont(schriftart, 12)
        # Datum
        date = context.modtime.strftime("%d.%m.%Y")
        # Grauer Hintergrund
        c.setFillGray(0.85)
        c.rect(1.4 * cm, 0.5 * cm, width=19.0 * cm, height=28.9 * cm, stroke=0, fill=1)
        # Weisse Rechtecke
        c.setLineWidth(0.5)
        c.setFillGray(1.0)
        c.rect(1.6 * cm, 27.6 * cm, width=9.0 * cm, height=1.6 * cm, stroke=1, fill=1)
        # 2 Traeger der Einrichtung
        c.rect(12.5 * cm, 25.4 * cm, width=7.6 * cm, height=1.6 * cm, stroke=1, fill=1)
        # 3 Unternehmensnummer des UV-Traegers
        c.rect(1.6 * cm, 22.5 * cm, width=9.0 * cm, height=4.5 * cm, stroke=0, fill=1)
        c.rect(1.6 * cm, 3.65 * cm, width=18.4 * cm, height=17.95 * cm, stroke=1, fill=1)
        c.rect(1.6 * cm, 0.9 * cm, width=18.4 * cm, height=1.9 * cm, stroke=1, fill=1)
        #if IMitglied.providedBy(self.request.principal):
        c.rect(12.5 * cm, 23.6 * cm, width=7.6 * cm, height=1.6 * cm, stroke=1, fill=1)
        # Linien fuer die Mitgliedsnummer
        x1 = 13.2
        x2 = 13.2
        y1 = 23.6
        y2 = 24.6
        for i in range(10):
            c.line(x1 * cm, y1 * cm, x2 * cm, y2 * cm)
            x1 = x1 + 0.7
            x2 = x2 + 0.7
        # Waagerechte Linien Felder 5-13
        x1 = 1.6
        x2 = 20.0
        y1 = 18.90
        y2 = 18.90
        for i in range(3):
            c.line(x1 * cm, y1 * cm, x2 * cm, y2 * cm)
            y1 = y1 + 0.85
            y2 = y2 + 0.85
        # Waagerechte Linie Felder 14
        c.line(x1 * cm, 17.60 * cm, x2 * cm, 17.60 * cm)
        # Waagerechte Linien Felder 15-20
        x1 = 1.6
        x2 = 20.0
        y1 = 4.85
        y2 = 4.85
        for i in range(5):
            c.line(x1 * cm, y1 * cm, x2 * cm, y2 * cm)
            y1 = y1 + 0.85
            y2 = y2 + 0.85
        # Linien in Feld 6
        c.line(13.7 * cm, 20.6 * cm, 13.7 * cm, 21.6 * cm)
        c.setStrokeGray(0.5)
        c.line(16.5 * cm, 20.6 * cm, 16.5 * cm, 21.1 * cm)
        c.line(17.5 * cm, 20.6 * cm, 17.5 * cm, 21.1 * cm)
        x1 = 16.0
        x2 = 16.0
        y1 = 20.6
        y2 = 21.6
        for i in range(3):
            c.line(x1 * cm, y1 * cm, x2 * cm, y2 * cm)
            x1 = x1 + 1.0
            x2 = x2 + 1.0
        x1 = 18.5
        x2 = 18.5
        y1 = 20.6
        y2 = 21.1
        for i in range(3):
            c.line(x1 * cm, y1 * cm, x2 * cm, y2 * cm)
            x1 = x1 + 0.5
            x2 = x2 + 0.5
        # Linien in Feld 7
        x1 = 10.5
        x2 = 10.5
        y1 = 19.75
        y2 = 20.2
        land = context.lkz
        if land == 'D':
            for i in range(4):
                c.line(x1 * cm, y1 * cm, x2 * cm, y2 * cm)
                x1 = x1 + 0.5
                x2 = x2 + 0.5
        c.setStrokeGray(0.0)
        c.line(10.0 * cm, 19.75 * cm, 10.0 * cm, 20.6 * cm)
        c.line(12.5 * cm, 19.75 * cm, 12.5 * cm, 20.6 * cm)
        # Rechtecke in Feld 8
        c.rect(1.8 * cm, 18.9 * cm, width=0.4 * cm, height=0.4 * cm, stroke=1, fill=1)
        c.rect(3.6 * cm, 18.9 * cm, width=0.4 * cm, height=0.4 * cm, stroke=1, fill=1)
        # Linie abwaerts von Feld 9
        c.line(5.5 * cm, 18.9 * cm, 5.5 * cm, 19.75 * cm)
        # Linie abwaerts von Feld 10
        c.line(10.0 * cm, 18.9 * cm, 10.0 * cm, 19.75 * cm)
        # Rechtecke in Feld 11
        c.rect(1.8 * cm, 18.05 * cm, width=0.4 * cm, height=0.4 * cm, stroke=1, fill=1)
        c.rect(3.6 * cm, 18.05 * cm, width=0.4 * cm, height=0.4 * cm, stroke=1, fill=1)
        # Linien in Feld 12
        c.setStrokeGray(0.5)
        u1 = 17.60
        c.line(4.9 * cm, u1 * cm, 4.9 * cm, 18.9 * cm)
        c.line(5.4 * cm, u1 * cm, 5.4 * cm, 18.05 * cm)
        c.line(5.9 * cm, u1 * cm, 5.9 * cm, 18.55 * cm)
        c.line(6.4 * cm, u1 * cm, 6.4 * cm, 18.05 * cm)
        c.line(6.9 * cm, u1 * cm, 6.9 * cm, 18.55 * cm)
        c.line(7.4 * cm, u1 * cm, 7.4 * cm, 18.05 * cm)
        c.line(7.9 * cm, u1 * cm, 7.9 * cm, 18.05 * cm)
        c.line(8.4 * cm, u1 * cm, 8.4 * cm, 18.05 * cm)
        c.line(8.9 * cm, u1 * cm, 8.9 * cm, 18.55 * cm)
        c.line(9.4 * cm, u1 * cm, 9.4 * cm, 18.05 * cm)
        c.line(9.9 * cm, u1 * cm, 9.9 * cm, 18.55 * cm)
        c.line(10.4 * cm, u1 * cm, 10.4 * cm, 18.05 * cm)
        c.line(10.9 * cm, u1 * cm, 10.9 * cm, 18.9 * cm)
        ### # Linie Feld 13
        ### c.setStrokeGray(0.0)
        ### c.line(13.6*cm,18.05*cm,13.6*cm,18.9*cm)
        # Rechtecke in Feld 14
        c.setStrokeGray(0.0)
        c.rect(7.9 * cm, 8.25 * cm, width=0.4 * cm, height=0.4 * cm, stroke=1, fill=1)
        c.rect(10.7 * cm, 8.25 * cm, width=0.4 * cm, height=0.4 * cm, stroke=1, fill=1)
        # Linie in Feld 15/16
        c.line(10.7 * cm, 7.4 * cm, 10.7 * cm, 8.25 * cm)
        # Rechtecke und Linien in Feld 17
        c.rect(7.9 * cm, 6.55 * cm, width=0.4 * cm, height=0.4 * cm, stroke=1, fill=1)
        c.rect(9.5 * cm, 6.55 * cm, width=0.4 * cm, height=0.4 * cm, stroke=1, fill=1)
        c.rect(14.3 * cm, 6.55 * cm, width=0.4 * cm, height=0.4 * cm, stroke=1, fill=1)
        c.setStrokeGray(0.5)
        c.line(17.5 * cm, 6.55 * cm, 17.5 * cm, 6.95 * cm)
        c.line(18.5 * cm, 6.55 * cm, 18.5 * cm, 6.95 * cm)
        c.line(19.0 * cm, 6.55 * cm, 19.0 * cm, 7.4 * cm)
        c.line(19.5 * cm, 6.55 * cm, 19.5 * cm, 6.95 * cm)
        # Rechtecke und Linien in Feld 18
        c.line(16.0 * cm, 5.7 * cm, 16.0 * cm, 6.55 * cm)
        c.line(16.5 * cm, 5.7 * cm, 16.5 * cm, 6.1 * cm)
        c.line(17.0 * cm, 5.7 * cm, 17.0 * cm, 7.4 * cm)
        c.line(17.5 * cm, 5.7 * cm, 17.5 * cm, 6.1 * cm)
        c.line(18.0 * cm, 5.7 * cm, 18.0 * cm, 7.4 * cm)
        c.line(18.5 * cm, 5.7 * cm, 18.5 * cm, 6.1 * cm)
        c.line(19.0 * cm, 5.7 * cm, 19.0 * cm, 6.1 * cm)
        c.line(19.5 * cm, 5.7 * cm, 19.5 * cm, 6.1 * cm)
        c.setStrokeGray(0.0)
        c.rect(9.5 * cm, 5.7 * cm, width=0.4 * cm, height=0.4 * cm, stroke=1, fill=1)
        c.rect(14.3 * cm, 5.7 * cm, width=0.4 * cm, height=0.4 * cm, stroke=1, fill=1)
        # Rechtecke in Feld 19
        c.rect(15.7 * cm, 4.85 * cm, width=0.4 * cm, height=0.4 * cm, stroke=1, fill=1)
        c.rect(17.2 * cm, 4.85 * cm, width=0.4 * cm, height=0.4 * cm, stroke=1, fill=1)
        # Linien in Feld 20/21
        c.line(13.3 * cm, 3.65 * cm, 13.3 * cm, 4.85 * cm)
        c.line(17.0 * cm, 3.65 * cm, 17.0 * cm, 4.45 * cm)
        c.setStrokeGray(0.5)
        c.line(15.0 * cm, 3.65 * cm, 15.0 * cm, 4.45 * cm)
        c.line(15.5 * cm, 3.65 * cm, 15.5 * cm, 4.05 * cm)
        c.line(16.0 * cm, 3.65 * cm, 16.0 * cm, 4.45 * cm)
        c.line(16.5 * cm, 3.65 * cm, 16.5 * cm, 4.05 * cm)
        c.line(18.0 * cm, 3.65 * cm, 18.0 * cm, 4.45 * cm)
        c.line(18.5 * cm, 3.65 * cm, 18.5 * cm, 4.05 * cm)
        c.line(19.0 * cm, 3.65 * cm, 19.0 * cm, 4.45 * cm)
        c.line(19.5 * cm, 3.65 * cm, 19.5 * cm, 4.05 * cm)
        #Linie in Feld 22
        c.line(1.7 * cm, 1.4 * cm, 19.9 * cm, 1.4 * cm)
        ###################################################################
        # Feldbeschriftungen                                              #
        ###################################################################
        c.setFillGray(0.0)
        # Formulartitel
        c.setFont(schriftartfett, 18)
        c.drawString(12.5 * cm, 28.4 * cm, "U N F A L L A N Z E I G E")
        c.setFont(schriftart, 11)
        c.drawString(12.5 * cm, 28.0 * cm, "für Kinder in Tageseinrichtungen,")
        c.drawString(12.5 * cm, 27.6 * cm, "Schüler, Studierende")
        # Beschriftung Feld 1
        c.setFont(schriftartfett, 7)
        c.drawString(1.8 * cm, 28.9 * cm, "1")
        c.setFont(schriftart, 7)
        c.drawString(2.1 * cm, 28.9 * cm, "Name und Anschrift der Einrichtung")
        # Beschriftung Feld 2
        c.setFont(schriftartfett, 7)
        c.drawString(12.7 * cm, 26.7 * cm, "2")
        c.setFont(schriftart, 7)
        c.drawString(13.0 * cm, 26.7 * cm, u"Träger der Einrichtung")
        # Beschriftung Feld 3
        c.setFont(schriftartfett, 7)
        c.drawString(12.7 * cm, 24.9 * cm, "3")
        c.setFont(schriftart, 7)
        c.drawString(13.0 * cm, 24.9 * cm, u"Unternehmensnummer des Unfallversicherungsträgers")
        # Adressdaten nach DIN 5008
        c.setFont(schriftart, 11)
        # Die ersten 3 Zeilen sind für Hinweise
        # c.drawString(1.75*cm,26.6*cm, '')
        # c.drawString(1.75*cm,26.1*cm, '')
        # c.drawString(1.75*cm,25.6*cm, '')
        # 6 Zeilen fuer die Adresse keine Leerzeile zwischen Strasse + Postleitzahl !!!
        c.drawString(1.75 * cm, 25.1 * cm, u'Unfallkasse Hessen')
        c.drawString(1.75 * cm, 24.6 * cm, u'Leonardo-da-Vinci-Allee 20')
        c.drawString(1.75 * cm, 24.1 * cm, u'60486 Frankfurt am Main')
        # c.drawString(1.75*cm,23.6*cm, '')
        # c.drawString(1.75*cm,23.1*cm, '')
        # c.drawString(1.75*cm,22.6*cm, '')
        # Beschriftung Feld 5
        c.setFont(schriftartfett, 7)
        c.drawString(1.8 * cm, 21.3 * cm, "5")
        c.setFont(schriftart, 7)
        c.drawString(2.1 * cm, 21.3 * cm, "Name, Vorname des Versicherten")
        # Beschriftung Feld 6
        c.setFont(schriftartfett, 7)
        c.drawString(13.9 * cm, 21.3 * cm, "6")
        c.setFont(schriftart, 7)
        c.drawString(14.2 * cm, 21.3 * cm, "Geburtsdatum")
        c.drawString(16.25 * cm, 21.3 * cm, "Tag")
        c.drawString(17.15 * cm, 21.3 * cm, "Monat")
        c.drawString(18.7 * cm, 21.3 * cm, "Jahr")
        # Beschriftung Feld 7
        c.setFont(schriftartfett, 7)
        c.drawString(1.8 * cm, 20.3 * cm, "7")
        c.setFont(schriftart, 7)
        c.drawString(2.1 * cm, 20.3 * cm, u"Straße, Hausnummer")
        c.drawString(10.1 * cm, 20.3 * cm, "Postleitzahl")
        c.drawString(12.6 * cm, 20.3 * cm, "Ort")
        # Beschriftung Feld 8
        c.setFont(schriftartfett, 7)
        c.drawString(1.8 * cm, 19.45 * cm, "8")
        c.setFont(schriftart, 7)
        c.drawString(2.1 * cm, 19.45 * cm, "Geschlecht")
        c.drawString(2.3 * cm, 19.0 * cm, u"männlich")
        c.drawString(4.1 * cm, 19.0 * cm, "weiblich")
        # Beschriftung Feld 9
        c.setFont(schriftartfett, 7)
        c.drawString(5.7 * cm, 19.45 * cm, "9")
        c.setFont(schriftart, 7)
        c.drawString(6.0 * cm, 19.45 * cm, u"Staatsangehörigkeit")
        # Beschriftung Feld 10
        c.setFont(schriftartfett, 7)
        c.drawString(10.1 * cm, 19.45 * cm, "10")
        c.setFont(schriftart, 7)
        c.drawString(10.5 * cm, 19.45 * cm, "Name und Anschrift der gesetzlichen Vertreter")
        # Beschriftung Feld 11
        c.setFont(schriftartfett, 7)
        c.drawString(1.8 * cm, 18.65 * cm, "11")
        c.setFont(schriftart, 7)
        c.drawString(2.2 * cm, 18.65 * cm, u"Tödlicher Unfall")
        c.drawString(2.3 * cm, 18.15 * cm, "ja")
        c.drawString(4.1 * cm, 18.15 * cm, "nein")
        # Beschriftung Feld 12
        c.setFont(schriftartfett, 7)
        c.drawString(5.0 * cm, 18.65 * cm, "12")
        c.setFont(schriftart, 7)
        c.drawString(5.4 * cm, 18.65 * cm, "Unfallzeitpunkt")
        c.drawString(5.2 * cm, 18.2 * cm, "Tag")
        c.drawString(6.05 * cm, 18.2 * cm, "Monat")
        c.drawString(7.65 * cm, 18.2 * cm, "Jahr")
        c.drawString(9.0 * cm, 18.2 * cm, "Stunde")
        c.drawString(10.05 * cm, 18.2 * cm, "Minute")
        # Beschriftung Feld 13
        c.setFont(schriftartfett, 7)
        c.drawString(11.05 * cm, 18.65 * cm, "13")
        c.setFont(schriftart, 7)
        c.drawString(11.45 * cm, 18.65 * cm, u"Unfallort (genaue Orts- und Straßenangabe mit PLZ)")
        # Beschriftung Feld 14
        c.setFont(schriftartfett, 7)
        c.drawString(1.8 * cm, 17.30 * cm, "14")
        c.setFont(schriftart, 7)
        c.drawString(2.2 * cm, 17.30 * cm, u"Ausführliche Schilderung des Unfallhergangs")
        c.setFont(schriftart, 6)
        c.drawString(7.4 * cm, 17.30 * cm, u"(insbesondere Art der Veranstaltung, bei Sportunfällen auch Sportart)")
        c.setFont(schriftart, 7)
        c.drawString(1.8 * cm, 8.35 * cm, u"Die Angaben beruhen auf der Schilderung")
        c.drawString(8.4 * cm, 8.35 * cm, u"des Versicherten")
        c.drawString(11.2 * cm, 8.35 * cm, u"anderer Personen")
        # Beschriftung Feld 15
        c.setFont(schriftartfett, 7)
        c.drawString(1.8 * cm, 7.95 * cm, "15")
        c.setFont(schriftart, 7)
        c.drawString(2.2 * cm, 7.95 * cm, u"Verletzte Körperteile")
        # Beschriftung Feld 16
        c.setFont(schriftartfett, 7)
        c.drawString(10.9 * cm, 7.95 * cm, "16")
        c.setFont(schriftart, 7)
        c.drawString(11.3 * cm, 7.95 * cm, u"Art der Verletzung")
        # Beschriftung Feld 17
        c.setFont(schriftartfett, 7)
        c.drawString(1.8 * cm, 6.95 * cm, "17")
        c.setFont(schriftart, 7)
        c.drawString(2.2 * cm, 6.95 * cm, u"Hat der Versicherte den Besuch der")
        c.drawString(2.2 * cm, 6.65 * cm, u"Einrichtung unterbrochen?")
        c.drawString(8.5 * cm, 6.65 * cm, u"nein")
        c.drawString(10.1 * cm, 6.65 * cm, u"sofort")
        c.drawString(14.9 * cm, 6.65 * cm, u"später, am")
        c.drawString(17.25 * cm, 7.1 * cm, u"Tag")
        c.drawString(18.15 * cm, 7.1 * cm, u"Monat")
        c.drawString(19.1 * cm, 7.1 * cm, u"Stunde")
        # Beschriftung Feld 18
        c.setFont(schriftartfett, 7)
        c.drawString(1.8 * cm, 6.1 * cm, "18")
        c.setFont(schriftart, 7)
        c.drawString(2.2 * cm, 6.1 * cm, "Hat der Versicherte den Besuch der")
        c.drawString(2.2 * cm, 5.8 * cm, "Einrichtung wieder aufgenommen?")
        c.drawString(10.1 * cm, 5.8 * cm, "nein")
        c.drawString(14.9 * cm, 5.8 * cm, "ja, am")
        c.drawString(16.25 * cm, 6.25 * cm, "Tag")
        c.drawString(17.15 * cm, 6.25 * cm, "Monat")
        c.drawString(18.75 * cm, 6.25 * cm, "Jahr")
        # Beschriftung Feld 19
        c.setFont(schriftartfett, 7)
        c.drawString(1.8 * cm, 5.4 * cm, "19")
        c.setFont(schriftart, 7)
        c.drawString(2.2 * cm, 5.4 * cm, u"Wer hat von dem Unfall zuerst Kenntnis genommen ?")
        c.setFont(schriftart, 6)
        c.drawString(8.2 * cm, 5.4 * cm, u"(Name, Anschrift des Zeugen)")
        c.setFont(schriftart, 7)
        c.drawString(15.7 * cm, 5.4 * cm, u"War diese Person Augenzeuge ?")
        c.drawString(16.2 * cm, 4.95 * cm, u"ja")
        c.drawString(17.7 * cm, 4.95 * cm, u"nein")
        # Beschriftung Feld 20
        c.setFont(schriftartfett, 7)
        c.drawString(1.8 * cm, 4.55 * cm, "20")
        c.setFont(schriftart, 7)
        c.drawString(2.2 * cm, 4.55 * cm, u"Name und Anschrift des erstbehandelnden Arztes/Krankenhauses")
        # Beschriftung Feld 21
        c.setFont(schriftartfett, 7)
        c.drawString(13.5 * cm, 4.55 * cm, "22")
        c.setFont(schriftart, 7)
        c.drawString(13.9 * cm, 4.55 * cm, u"Beginn und Ende des Besuchs der Einrichtung")
        c.drawString(13.9 * cm, 3.75 * cm, u"Beginn")
        c.drawString(15.1 * cm, 4.25 * cm, u"Stunde")
        c.drawString(16.1 * cm, 4.25 * cm, u"Minute")
        c.drawString(17.2 * cm, 3.75 * cm, u"Ende")
        c.drawString(18.1 * cm, 4.25 * cm, u"Stunde")
        c.drawString(19.1 * cm, 4.25 * cm, u"Minute")
        # Beschriftung Feld 28
        c.setFont(schriftartfett, 7)
        c.drawString(1.8 * cm, 1.1 * cm, "22")
        c.setFont(schriftart, 7)
        c.drawString(3.0 * cm, 1.1 * cm, "Datum")
        c.drawString(5.1 * cm, 1.1 * cm, u"Leiter (Beauftragter) der Einrichtung")
        c.drawString(14.65 * cm, 1.1 * cm, u"Telefon-Nr. für Rückfragen (Ansprechpartner)")
        c.setFont(schriftartfett, 12)
        c.drawString(7.0 * cm, 2.15 * cm, u"versandt über Extranet")
        ###################################################################
        # Variablen enfügen                                               #
        ###################################################################
        #
        #   (1) Name und Anschrift des Unternehmens
        #
        # EIN MITGLIED
        if False:
            pass
        #if IMitglied.providedBy(self.request.principal):
        #    c.setFont(schriftartfett, 8)
        #    x = 28.6
        #    c.drawString(1.7 * cm, x * cm, nN(context.ename))
        #    x = x - 0.3
        #    c.drawString(1.7 * cm, x * cm, nN(context.estrasse) + ' ' + nN(context.enummer))
        #    x = x - 0.3
        #    c.drawString(1.7 * cm, x * cm, nN(context.eplz) + ' ' + nN(context.eort))
        #    y = 26.4
        #    # Namensfelder werden nur ausgegeben wenn diese gefuellt sind
        #    if adresse[u'iknam1'] != '':
        #        c.drawString(12.6 * cm, y * cm, adresse[u'iknam1'])
         #       y = y - 0.3
        #    if adresse[u'iknam2'] != '':
        #        c.drawString(12.6 * cm, y * cm, adresse[u'iknam2'] + ' ' + adresse[u'iknam3'])
        #        y = y - 0.3
        #    c.drawString(12.6 * cm, y * cm, adresse[u'ikstr'] + ' ' + adresse[u'ikhnr'])
        #    y = y - 0.3
        #    c.drawString(12.6 * cm, y * cm, str(adresse['ikhplz']) + ' ' + adresse['ikhort'])
        # EINE EINRICHTUNG
        else:
            c.setFont(schriftartfett, 8)
            x = 28.6
            # Namensfelder werden nur ausgegeben wenn diese gefuellt sind
            #
            if 'iknam1' in adresse:
                if adresse['iknam1'] != '':
                    c.drawString(1.7 * cm, x * cm, adresse[u'iknam1'])
                    x = x - 0.3
                if adresse[u'iknam2'] != '':
                    c.drawString(1.7 * cm, x * cm, adresse[u'iknam2'] + ' ' + adresse[u'iknam3'])
                    x = x - 0.3
                c.drawString(1.7 * cm, x * cm, adresse[u'ikstr'] + ' ' + adresse[u'ikhnr'])
                x = x - 0.3
                c.drawString(1.7 * cm, x * cm, str(adresse['ikhplz']) + ' ' + adresse['ikhort'])
            else:
                print "KEINE Adresse...!!!"
                
            #   (2) Traeger der Einrichtung
            #
            c.setFont(schriftartfett, 8)
            traeger = nN(context.traeger)
            y = 26.4
            if len(traeger) > 40:
                n = 40
                if traeger is not None:
                    while len(traeger) > 0:
                        if len(traeger) > n:
                            if n > 0:
                                if traeger[n] == " ":
                                    nottraeger = traeger[0:n]
                                    c.drawString(12.6 * cm, y * cm, nottraeger)
                                    traeger = traeger[(n + 1):]
                                    y = y - 0.25
                                    n = 80
                                else:
                                    n = n - 1
                            else:
                                nottraeger1 = traeger[0:80]
                                c.drawString(12.6 * cm, y * cm, nottraeger1)
                                traeger = traeger[80:]
                                y = y - 0.35
                                n = 80
                        else:
                            c.drawString(12.6 * cm, y * cm, traeger)
                            traeger = ''
            else:
                c.drawString(12.6 * cm, y * cm, traeger)
            y = y - 0.50
            c.drawString(12.6 * cm, y * cm, traegernr)
        #
        #   (3) Mitgliedsnummer
        #
        #if IMitglied.providedBy(self.request.principal):
        x = 12.7
        y = 23.7
        c.setFont(schriftart, 10)
        mnr = str(adresse['enrlfd'])
        #    mitglied = mnr[0] + mnr[2:4] + mnr[5:7] + mnr[8:]
        for i in mnr:
            c.drawString(x * cm, y * cm, i)
            x = x + 0.7
        #
        #   (4) Empfänger (Unfallversicherungsträger)
        #
        #   (5) Name, Vorname des Versicherten
        #
        versname = nN(context.prsname)
        versvorname = nN(context.prsvor)
        c.setFont(schriftart, 10)
        c.drawString(1.7 * cm, 20.7 * cm, versname + ', ' + versvorname)
        #
        #   (6) Geburtsdatum
        #
        gebdatum = nN(context.prsgeb)
        if  len(gebdatum) != 0:
            gebdatum = gebdatum.split('.')
            gebtag = gebdatum[0]
            gebmonat = gebdatum[1]
            gebjahr = gebdatum[2]
            if len(gebtag) == 1:
                gebtag = '0%s' % gebtag
            if len(gebmonat) == 1:
                gebmonat = '0%s' % gebmonat
            c.setFont(schriftart, 10)
            c.drawString(16.1 * cm, 20.7 * cm, gebtag[0])
            c.drawString(16.6 * cm, 20.7 * cm, gebtag[1])
            c.drawString(17.1 * cm, 20.7 * cm, gebmonat[0])
            c.drawString(17.6 * cm, 20.7 * cm, gebmonat[1])
            c.drawString(18.1 * cm, 20.7 * cm, gebjahr[0])
            c.drawString(18.6 * cm, 20.7 * cm, gebjahr[1])
            c.drawString(19.1 * cm, 20.7 * cm, gebjahr[2])
            c.drawString(19.6 * cm, 20.7 * cm, gebjahr[3])
        #
        #   (7) Strasse Hausnummer
        #
        aplz = nN(context.ikzplz)
        ort = nN(context.ikzort)
        strasse = nN(context.ikstr)
        hausnummer = nN(context.iknr)
        c.setFont(schriftart, 10)
        c.drawString(12.6 * cm, 19.85 * cm, ort)
        c.drawString(1.7 * cm, 19.85 * cm, strasse + ' ' + hausnummer)
        if land == 'D':
            c.drawString(10.1 * cm, 19.85 * cm, aplz[0])
            c.drawString(10.6 * cm, 19.85 * cm, aplz[1])
            c.drawString(11.1 * cm, 19.85 * cm, aplz[2])
            c.drawString(11.6 * cm, 19.85 * cm, aplz[3])
            c.drawString(12.1 * cm, 19.85 * cm, aplz[4])
        elif land != 'D' and land != None:
            if len(land) >= 22:
                c.setFont(schriftart, 6)
                c.drawString(10.1 * cm, 20.05 * cm, aplz)
                c.drawString(10.1 * cm, 19.85 * cm, land[0:22])
            if len(land) < 22:
                if len(land) >= 4:
                    c.setFont(schriftart, 6)
                    c.drawString(10.1 * cm, 20.05 * cm, aplz)
                    c.drawString(10.1 * cm, 19.85 * cm, land)
                if len(land) < 4:
                    c.setFont(schriftart, 10)
                    c.drawString(10.1 * cm, 19.85 * cm, land + '-' + aplz)
        #
        #   (8) Geschlecht
        #
        c.setFont(schriftart, 10)
        sex = nN(context.prssex)
        if sex == 'maennlich':
            c.drawString(1.9 * cm, 19.0 * cm, 'x')
        elif sex == 'weiblich':
            c.drawString(3.7 * cm, 19.0 * cm, 'x')
        #
        #   (9) Staatsangehörigkeitt
        #
        staat = nN(context.prssta)
        vocab = getUtility(IVocabularyFactory, name='uvc.sta')(None)
        try:
            term = vocab.getTerm(staat)
            staat = translate(term.title, 'uvc.unfallanzeige', target_language="de")
        except LookupError, e:
            print e
        if len(staat) >= 26:
            c.setFont(schriftart, 6)
            c.drawString(5.6 * cm, 19.0 * cm, staat)
        if len(staat) < 26:
            c.setFont(schriftart, 10)
            c.drawString(5.6 * cm, 19.0 * cm, staat)
        #
        #   (10) gesetzlicher Vertreter
        #
        gesetzver = nN(context.prsvtr)
        gesetzver = gesetzver.replace('\r\n', ' ')
        gesetzver = gesetzver.replace('\r', ' ')
        gesetzver = gesetzver.replace('\n', ' ')
        if len(gesetzver) > 50:
            c.setFont(schriftart, 7)
            y = 19.20
        else:
            c.setFont(schriftart, 10)
            y = 19.02
        n = 80
        if gesetzver is not None:
            while len(gesetzver) > 0:
                if len(gesetzver) > n:
                    if n > 0:
                        if gesetzver[n] == " ":
                            notgesetzver = gesetzver[0:n]
                            c.drawString(10.5 * cm, y * cm, notgesetzver)
                            gesetzver = gesetzver[(n + 1):]
                            y = y - 0.25
                            n = 80
                        else:
                            n = n - 1
                    else:
                        notgesetzver1 = gesetzver[0:80]
                        c.drawString(10.5 * cm, y * cm, notgesetzver1)
                        gesetzver = gesetzver[80:]
                        y = y - 0.35
                        n = 80
                else:
                    c.drawString(10.5 * cm, y * cm, gesetzver)
                    gesetzver = ''
        else:
            pass
        #
        #   (11) Tödlicher Unfall
        #
        c.setFont(schriftart, 10)
        tod = nN(context.prstkz)
        if tod == 'ja':
            c.drawString(1.9 * cm, 18.1 * cm, 'x')
        elif tod == 'nein':
            c.drawString(3.7 * cm, 18.1 * cm, 'x')
        #
        #   (12) Unfallzeitpunkt
        #
        c.setFont(schriftart, 10)
        uzeit = nN(context.unfzeit)
        if uzeit != '':
            datum = nN(context.unfdatum)
            stunde = nN(context.unfzeit)
            datum = datum.split('.')
            tag = datum[0]
            monat = datum[1]
            jahr = datum[2]
            if len(tag) == 1:
                tag = '0%s' % tag
            if len(monat) == 1:
                monat = '0%s' % monat
            if len(jahr) == 1:
                jahr = '0%s' % jahr
            if stunde.find(':') != -1:
                stunde = stunde.split(':')
                if len(stunde[0]) == 1:
                    std = '0%s' % stunde[0]
                else:
                    std = stunde[0]
                if len(stunde[1]) == 1:
                    min = '0%s' % stunde[1]
                else:
                    min = stunde[1]
                z1 = 17.65
                c.drawString(5.0 * cm, z1 * cm, tag[0])
                c.drawString(5.5 * cm, z1 * cm, tag[1])
                c.drawString(6.0 * cm, z1 * cm, monat[0])
                c.drawString(6.5 * cm, z1 * cm, monat[1])
                c.drawString(7.0 * cm, z1 * cm, jahr[0])
                c.drawString(7.5 * cm, z1 * cm, jahr[1])
                c.drawString(8.0 * cm, z1 * cm, jahr[2])
                c.drawString(8.5 * cm, z1 * cm, jahr[3])
                c.drawString(9.0 * cm, z1 * cm, std[0])
                c.drawString(9.5 * cm, z1 * cm, std[1])
                c.drawString(10.0 * cm, z1 * cm, min[0])
                c.drawString(10.5 * cm, z1 * cm, min[1])
        #
        #   (13) Unfallort
        #
        uort = nN(context.unfort)
        uort = uort.replace('\r\n', ' ')
        uort = uort.replace('\r', ' ')
        uort = uort.replace('\n', ' ')
        if len(uort) > 60:
            c.setFont(schriftart, 8)
            y = 18.1
        else:
            c.setFont(schriftart, 10)
            y = 18.1
        n = 60
        if uort is not None:
            while len(uort) > 0:
                if len(uort) > n:
                    if n > 0:
                        if uort[n] == " ":
                            notuort = uort[0:n]
                            c.drawString(11 * cm, y * cm, notuort)
                            uort = uort[(n + 1):]
                            y = y - 0.35
                            n = 60
                        else:
                            n = n - 1
                    else:
                        notuort1 = uort[0:60]
                        c.drawString(11 * cm, y * cm, notuort1)
                        uort = uort[60:]
                        y = y - 0.35
                        n = 60
                else:
                    c.drawString(11 * cm, y * cm, uort)
                    uort = ''
        else:
            pass
        #
        #   (14) Ausführliche Schilderung des Unfalls
        #
        ubericht = nN(context.unfhg1)
        ubericht = ubericht.replace('\r\n', ' ')
        ubericht = ubericht.replace('\r', ' ')
        ubericht = ubericht.replace('\n', ' ')
        c.setFont(schriftart, 10)
        cutstring = ubericht[:5000]
        cut = 2500
        if len(cutstring) > 2500:
            while len(cutstring) > 0:
                if cutstring[cut] == " ":
                    hergang = cutstring[0:cut]
                    nextpage = cutstring[(cut + 1):]
                    break
                #harte Trennung nach 100 Zeichen ohne Leerzeichen
                elif cut == 2400:
                    hergang = cutstring[0:cut]
                    nextpage = cutstring[(cut + 1):]
                    break
                else:
                    cut = cut - 1
            else:
                pass
        else:
            hergang = cutstring
            nextpage = " "
        if len(hergang) > 1000:
            n = 125
            cpl = 125
            c.setFont(schriftart, 8)
        else:
            n = 105
            cpl = 105
            c.setFont(schriftart, 10)
        y = 16.7
        while len(hergang) > 0:
            if len(hergang) > n:
                if n > 0:
                    if hergang[n] == " ":
                        schilderung = hergang[0:n]
                        c.drawString(1.7 * cm, y * cm, schilderung)
                        hergang = hergang[(n + 1):]
                        y = y - 0.35
                        n = cpl
                    else:
                        n = n - 1
                else:
                    schilderung1 = hergang[0:cpl]
                    c.drawString(1.7 * cm, y * cm, schilderung1)
                    hergang = hergang[cpl:]
                    y = y - 0.35
                    n = cpl
            else:
                c.drawString(1.7 * cm, y * cm, hergang)
                hergang = ''
        else:
            pass
        c.setFont(schriftart, 10)
        schilderungen = nN(context.unfhg2)
        if schilderungen == 'des Versicherten':
            c.drawString(8.0 * cm, 8.3 * cm, 'x')
        elif schilderungen == 'einer anderen Person':
            c.drawString(10.8 * cm, 8.3 * cm, 'x')
        #
        #   (15) Verletztes Körperteile
        #
        kteile = nN(context.diavkt)
        if len(kteile) > 50:
            c.setFont(schriftart, 8)
        else:
            c.setFont(schriftart, 10)
        c.drawString(1.7 * cm, 7.49 * cm, kteile)
        #
        #   (16) Art der Verletzung
        #
        vart = nN(context.diaadv)
        if len(vart) > 50:
            c.setFont(schriftart, 8)
        else:
            c.setFont(schriftart, 10)
        c.drawString(10.8 * cm, 7.49 * cm, vart)
        #
        #   (17) Hat der Versicherte den besuch der Einrichtung eingestellt?
        #
        c.setFont(schriftart, 10)
        einstell = nN(context.unfae1)
        if einstell == 'nein':
            c.drawString(8.0 * cm, 6.6 * cm, 'x')
        elif einstell == 'ja, sofort':
            c.drawString(9.6 * cm, 6.6 * cm, 'x')
        elif einstell == u'ja, spaeter am:':
            c.drawString(14.4 * cm, 6.6 * cm, 'x')
            tagmonat = nN(context.unfaedatum)
            stunde = nN(context.unfaezeit)
            tagmonat = tagmonat.split('.')
            tag = tagmonat[0]
            monat = tagmonat[1]
            if len(tag) == 1:
                tag = '0%s' % tag
            if len(monat) == 1:
                monat = '0%s' % monat
            stunde = stunde.split(':')
            if len(stunde[0]) == 1:
                std = '0%s' % stunde[0]
            else:
                std = stunde[0]
            c.drawString(17.1 * cm, 6.6 * cm, tag[0])
            c.drawString(17.6 * cm, 6.6 * cm, tag[1])
            c.drawString(18.1 * cm, 6.6 * cm, monat[0])
            c.drawString(18.6 * cm, 6.6 * cm, monat[1])
            c.drawString(19.1 * cm, 6.6 * cm, std[0])
            c.drawString(19.6 * cm, 6.6 * cm, std[1])
        #
        #   (18) Hat der Versicherte den Besuch wieder aufgenommen?
        #
        c.setFont(schriftart, 10)
        aufnahme = nN(context.unfwa1)
        if aufnahme == 'nein':
            c.drawString(9.6 * cm, 5.75 * cm, 'x')
        elif aufnahme == 'ja':
            c.drawString(14.4 * cm, 5.75 * cm, 'x')
            azeit = nN(context.unfwax)
            if azeit == '':
		azeit = '00.00.0000'
            azeit = azeit.split('.')
            tag = azeit[0]
            monat = azeit[1]
            jahr = azeit[2]
            if len(tag) == 1:
                tag = '0%s' % tag
            if len(monat) == 1:
                monat = '0%s' % monat
            c.drawString(16.1 * cm, 5.75 * cm, tag[0])
            c.drawString(16.6 * cm, 5.75 * cm, tag[1])
            c.drawString(17.1 * cm, 5.75 * cm, monat[0])
            c.drawString(17.6 * cm, 5.75 * cm, monat[1])
            c.drawString(18.1 * cm, 5.75 * cm, jahr[0])
            c.drawString(18.6 * cm, 5.75 * cm, jahr[1])
            c.drawString(19.1 * cm, 5.75 * cm, jahr[2])
            c.drawString(19.6 * cm, 5.75 * cm, jahr[3])
        #
        #   (19) Wer hat von dem Unfall Kenntnis genommen?
        #
        wer = nN(context.unfkn1)
        wer = wer.replace('\r\n', ' ')
        wer = wer.replace('\r', ' ')
        wer = wer.replace('\n', ' ')
        if wer is not None:
            ### 1   bis 70  zeichen groesse 10
            if len(wer) <= 70:
                c.setFont(schriftart, 10)
                c.drawString(1.7 * cm, 4.9 * cm, wer)
            ### 71  bis 90  zeichen groesse 8
            if len(wer) > 70 and len(wer) <= 90:
                c.setFont(schriftart, 8)
                c.drawString(1.7 * cm, 4.9 * cm, wer)
            ### 91  bis 105 zeichen groesse 7
            if len(wer) > 90 and len(wer) <= 105:
                c.setFont(schriftart, 7)
                c.drawString(1.7 * cm, 4.9 * cm, wer)
            ### 106 bis 124 zeichen groesse 6
            if len(wer) > 105 and len(wer) <= 124:
                c.setFont(schriftart, 6)
                c.drawString(1.7 * cm, 4.9 * cm, wer)
            if len(wer) > 124:
                c.setFont(schriftart, 6)
                y = 5.20
                n = 124
                um = False
                if len(wer) > 230:
                    c.setFont(schriftart, 5)
                    n = 140
                    um = True
                while len(wer) > 0:
                    if len(wer) > n:
                        if n > 0:
                            if wer[n] == " ":
                                xwer = wer[0:n]
                                c.drawString(1.7 * cm, y * cm, xwer)
                                wer = wer[(n + 1):]
                                y = y - 0.25
                                n = 124
                                if um is True:
                                    n = 140
                            else:
                                n = n - 1
                    else:
                        c.drawString(1.7 * cm, y * cm, wer)
                        wer = ''
            else:
                pass
        ######################################################
        c.setFont(schriftart, 10)
        augenzeuge = nN(context.unfkn2)
        if augenzeuge == 'ja':
            c.drawString(15.8 * cm, 4.9 * cm, 'x')
        elif augenzeuge == 'nein':
            c.drawString(17.3 * cm, 4.9 * cm, 'x')
        #
        #   (20) Name und Anschrift des erstbehandelnden Arztes
        #
        # Keine Ärztliche Behandlung erforderlich:
        abehandlung = nN(context.unfeba)
        if abehandlung == 'Es ist keine aerztliche Behandlung erforderlich.':
            c.drawString(1.7 * cm, 3.8 * cm, u'Keine ärztliche Behandlung erforderlich')
        else:
            arzt = nN(context.unfeba1)
            arzt = arzt.replace('\r\n', ' ')
            arzt = arzt.replace('\r', ' ')
            arzt = arzt.replace('\n', ' ')
            if len(arzt) > 65:
                c.setFont(schriftart, 8)
                y = 4.2
            else:
                c.setFont(schriftart, 10)
                y = 3.8
            n = 75
            if arzt is not None:
                while len(arzt) > 0:
                    if len(arzt) > n:
                        if n > 0:
                            if arzt[n] == " ":
                                notarzt = arzt[0:n]
                                c.drawString(1.7 * cm, y * cm, notarzt)
                                arzt = arzt[(n + 1):]
                                y = y - 0.35
                                n = 75
                            else:
                                n = n - 1
                        else:
                            notarzt1 = arzt[0:75]
                            c.drawString(1.7 * cm, y * cm, notarzt1)
                            arzt = arzt[75:]
                            y = y - 0.35
                            n = 75
                    else:
                        c.drawString(1.7 * cm, y * cm, arzt)
                        arzt = ''
            else:
                pass
        #
        #   (21) Beginn und Ende des Besuches der Einrichtung
        #
        c.setFont(schriftart, 10)
        zeit = ""
        if zeit != ['', '']:
            beginn = nN(context.uadbavon)
            ende = nN(context.uadbabis)
            if beginn.find(':') != - 1:
                beginn = beginn.split(':')
                if len(beginn[0]) == 1:
                    std = '0%s' % beginn[0]
                else:
                    std = beginn[0]
                if len(beginn[1]) == 1:
                    min = '0%s' % beginn[1]
                else:
                    min = beginn[1]
                c.drawString(15.1 * cm, 3.7 * cm, std[0])
                c.drawString(15.6 * cm, 3.7 * cm, std[1])
                c.drawString(16.1 * cm, 3.7 * cm, min[0])
                c.drawString(16.6 * cm, 3.7 * cm, min[1])
            if ende.find(':') != - 1:
                ende = ende.split(':')
                if len(ende[0]) == 1:
                    std = '0%s' % ende[0]
                else:
                    std = ende[0]
                if len(ende[1]) == 1:
                    min = '0%s' % ende[1]
                else:
                    min = ende[1]
                c.drawString(18.1 * cm, 3.7 * cm, std[0])
                c.drawString(18.6 * cm, 3.7 * cm, std[1])
                c.drawString(19.1 * cm, 3.7 * cm, min[0])
                c.drawString(19.6 * cm, 3.7 * cm, min[1])
        #
        #   (22) Datum Unterschrift
        #
        c.setFont(schriftart, 8)
        c.drawString(2.8 * cm, 1.5 * cm, date)
        leiter = nN(context.unfus2)
        anspar = nN(context.anspname)
        tel = nN(context.anspfon)
        c.drawString(4.8 * cm, 1.5 * cm, leiter)
        if len(tel) != 0:
            c.drawString(15.0 * cm, 1.5 * cm, "Telefon:" + " " + tel)
            c.drawString(15.0 * cm, 2.0 * cm, anspar)
        else:
            c.drawString(15.0 * cm, 1.5 * cm, anspar)
        # Ende der Seite
        c.showPage()
        ###################################################################
        # Druck der Zusatzinformationen                                   #
        ###################################################################
        if len(nextpage) > 1:
            # Grauer Hintergrund
            c.setFillGray(0.85)
            c.rect(1.4 * cm, 0.5 * cm, width=19.0 * cm, height=28.9 * cm, stroke=0, fill=1)
            # Weisse Rechtecke
            c.setLineWidth(0.5)
            c.setFillGray(1.0)
            c.rect(1.6 * cm, 27.6 * cm, width=9.0 * cm, height=1.6 * cm, stroke=1, fill=1)
            #if IMitglied.providedBy(self.request.principal):
            c.rect(12.5 * cm, 27.6 * cm, width=7.6 * cm, height=1.6 * cm, stroke=1, fill=1)
            c.rect(1.6 * cm, 3.0 * cm, width=18.4 * cm, height=19.6 * cm, stroke=1, fill=1)
            c.rect(1.6 * cm, 22.8 * cm, width=18.4 * cm, height=1.6 * cm, stroke=1, fill=1)
            # Linien Mitgliedsnummer
            #if IMitglied.providedBy(self.request.principal):
            x1 = 13.2
            x2 = 13.2
            y1 = 27.6
            y2 = 28.0
            for i in range(10):
                c.line(x1 * cm, y1 * cm, x2 * cm, y2 * cm)
                x1 = x1 + 0.7
                x2 = x2 + 0.7
            # Titel fuer Seite2 des Formulars
            c.setFillGray(0.0)
            c.setFont(schriftartfett, 18)
            c.drawString(3.5 * cm, 25.7 * cm, "Zusatzinformationen zur U N F A L L A N Z E I G E")
            # Beschriftung Feld: Name und Anschrift des Unternehmens
            c.setFont(schriftart, 7)
            c.drawString(1.7 * cm, 28.9 * cm, "Name und Anschrift der Einrichtung")
            # Beschriftung Feld: Mitgliedsnummer
            #if IMitglied.providedBy(self.request.principal):
            c.setFont(schriftart, 7)
            c.drawString(12.6 * cm, 28.9 * cm, u"Unternehmensnummer des Unfallversicherungsträgers")
            # Name und Anschrift des Unternehmens
            c.setFont(schriftartfett, 8)
            x = 28.6
            # Namensfelder werden nur ausgegeben wenn diese gefuellt sind
            if adresse[u'iknam1'] != '':
                c.drawString(1.7 * cm, x * cm, adresse[u'iknam1'])
                x = x - 0.3
            if adresse[u'iknam2'] != '':
                c.drawString(1.7 * cm, x * cm, adresse[u'iknam2'] + ' ' + adresse[u'iknam3'])
                x = x - 0.3
            c.drawString(1.7 * cm, x * cm, adresse[u'ikstr'] + ' ' + adresse[u'ikhnr'])
            x = x - 0.3
            c.drawString(1.7 * cm, x * cm, str(adresse['ikhplz']) + ' ' + adresse['ikhort'])
            # Mitgliedsnummer
            x = 12.7
            y = 27.7
            c.setFont(schriftart, 10)
            for i in mnr:
                c.drawString(x * cm, y * cm, i)
                x = x + 0.7
            #if IMitglied.providedBy(self.request.principal):
            #    mnr = adresse['trgmnr']
            #    mitglied = mnr[0] + mnr[2:4] + mnr[5:7] + mnr[8:]
            #    for i in mitglied:
            #        c.drawString(x * cm, y * cm, i)
            #        x = x + 0.7
            # Empfänger (Unfallversicherungsträger)
            # Name, Vorname des Versicherten
            versname = nN(context.prsname)
            versvorname = nN(context.prsvor)
            c.setFont(schriftart, 10)
            c.drawString(1.7 * cm, 23.7 * cm, versname + ', ' + versvorname)
            # Beschriftung Feld: Unfallzeitpunkt
            c.setFont(schriftartfett, 10)
            c.drawString(14 * cm, 23.7 * cm, "Unfallzeitpunkt")
            # Unfallzeitpunkt
            c.setFont(schriftart, 10)
            uzeit = nN(context.unfzeit)
            udatum = nN(context.unfdatum)
            c.drawString(14 * cm, 23.2 * cm, udatum)
            c.drawString(16 * cm, 23.2 * cm, uzeit + " Uhr")
            # Beschreibung Unfallhergang
            c.setFont(schriftartfett, 10)
            c.drawString(1.8 * cm, 20 * cm, "Beschreibung des Unfallhergangs (Fortsetzung)")
            n = 125
            cpl = 125
            c.setFont(schriftart, 8)
            y = 19
            if nextpage:
                while len(nextpage) > 0:
                    if len(nextpage) > n:
                        if n > 0:
                            if nextpage[n] == " ":
                                schilderung = nextpage[0:n]
                                c.drawString(1.8 * cm, y * cm, schilderung)
                                nextpage = nextpage[(n + 1):]
                                y = y - 0.35
                                n = cpl
                            else:
                                n = n - 1
                        else:
                            schilderung1 = nextpage[0:cpl]
                            c.drawString(1.8 * cm, y * cm, schilderung1)
                            nextpage = nextpage[cpl:]
                            y = y - 0.35
                            n = cpl
                    else:
                        c.drawString(1.8 * cm, y * cm, nextpage)
                        nextpage = ''
                else:
                    pass
            # Informationen ??????
            # Nicht notwendig, wird ausgeblendet
            # c.setFont(schriftartfett, 12)
            # c.drawString(1.8 * cm, 10 * cm, "UNZBEZ:")
            # c.drawString(1.8 * cm, 9.5 * cm, "UNFORTUS:")
            # c.drawString(1.8 * cm, 9 * cm, "UNFHGTUS:")
            # c.drawString(1.8 * cm, 8.5 * cm, "UADBAD:")
            # c.drawString(1.8 * cm, 8 * cm, "UADEAD:")
            # c.setFont(schriftart, 12)
            # c.drawString(4.8 * cm, 10 * cm, nN(context.unzbez))
            # c.drawString(4.8 * cm, 9.5 * cm, nN(context.unfortus))
            # c.drawString(4.8 * cm, 9 * cm, nN(context.unfhgtus))
            # c.drawString(4.8 * cm, 8.5 * cm, nN(context.uadbad))
            # c.drawString(4.8 * cm, 8 * cm, nN(context.uadead))
            # ENDE
            c.showPage()
