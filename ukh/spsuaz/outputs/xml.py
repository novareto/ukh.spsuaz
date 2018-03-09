#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ukh.kiunfallanzeige
# eKIUAZXML.py

import grok
import lxml.etree as etree
import tempfile

from time import strftime, localtime
#from ukh.markers.interfaces import IMitglied, IEinrichtung
#from uvcsite.interfaces import IStammdaten
#from ukh.kiunfallanzeige.interfaces import IKiDatenDale
#from ukh.kiunfallanzeige.interfaces import IKiUnfallanzeige
from elementtree.SimpleXMLWriter import XMLWriter
from StringIO import StringIO
from uvcsite.utils.dataviews import BaseXML
from zope.dublincore.interfaces import IZopeDublinCore
from zope.pluggableauth.factories import Principal
#from z3c.saconfig import Session
#from sqlalchemy import and_
#from sqlalchemy.sql import select
#from ukh.schulportal.configs.database_setup import traegeruaz


class KiDatenDale(BaseXML):
    grok.name('kixml')
    grok.title('XML-Unfallanzeige')

    def getFile(self, fn):
        if fn:
            return open(fn, 'w+b')
        return tempfile.TemporaryFile()

    def generate(self):
        '''
        XML-File fuer Dale erzeugen
        '''
        context = self.context
        # Layout
        dc = IZopeDublinCore(context, None)
        if dc:
            creator = dc.creators[0]
            principal = Principal(creator, creator, creator)
        else:
            principal = self.request.principal
        principal = self.request.principal
        #stammdaten = IStammdaten(self.request.principal)
        adresse = principal.getAdresse()
        traegeroid = u''
        oid = str(adresse['oid']).strip()
        if len(oid) == 9:
            oid = '000000' + oid 
        #session = Session()
        #s = select([traegeruaz], and_(traegeruaz.c.trgrcd == str(oid)))
        #res = session.execute(s).fetchone()
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print oid 
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        #if res:
        #    traegeroid = str(res['trgmnr']).strip()
        xml_file = self.base_file
        io = StringIO()
        xml = XMLWriter(io, encoding = 'utf-8')
        bv = ''
        iknr = '' #Ik-Nummer des Mitgliedsunternehmens muss noch ermittelt werden
        ikdav = '99999999'
        iknum = '120692198'
        date = strftime("%d.%m.%Y",localtime())
        time = strftime("%H:%M",localtime())
        unb_6 = '0'
        docid = context.__name__
        if len(docid.split('-')) == 2:
            unb_6 = docid.split('-')[1]

        # Daten schreiben
        suaz = xml.start('suaz_file')

        xml.start("unb")
        xml.element("unb_2", iknr)
        xml.element("unb_3", ikdav)
        xml.element("unb_4", date)
        xml.element("unb_5", '00:00')
        xml.element("unb_6", unb_6)
        xml.element("unb_9", '01')
        xml.end("unb")

        xml.start("unh")
        xml.element("unh_2", 'SUAZ:09:1:01:UV')
        xml.element("unh_3", iknum)
        xml.end("unh")

        xml.start("uvt")
        xml.element("uvt_1", bv)
        xml.element("uvt_2", iknum)
        xml.element("uvt_3", date)
        uvt_4 = "%s.%s.20%s" % (context.unfdatum[0:2], context.unfdatum[3:5], context.unfdatum[8:11])
        xml.element("uvt_4", uvt_4)
        xml.element("uvt_5", '')
        xml.end("uvt")

        xml.start("vin")
        xml.element("vin_1", context.prsname[:30])
        xml.element("vin_2", context.prsvor[:30])
        xml.element("vin_3", context.prssta)
        xml.element("vin_4", context.prssex[0])
        xml.element("vin_5", context.ikzplz[:6])
        xml.element("vin_6", context.ikzort[:30])
        vin_7 = "%s %s" % (context.ikstr, context.iknr)
        xml.element("vin_7", vin_7[:46])
        xml.element("vin_8", '')
        if int(context.prsgeb[6:11]) > int(strftime("%Y",localtime())):
            vin_9 = "%s.%s.19%s" % (context.prsgeb[0:2], context.prsgeb[3:5], context.prsgeb[8:10])
        else:
            vin_9 = "%s.%s.%s" % (context.prsgeb[0:2], context.prsgeb[3:5], context.prsgeb[6:10])
        xml.element("vin_9", vin_9)
        xml.element("vin_10", '')
        xml.element("vin_11", '')
        xml.end("vin")

        xml.start("ufb")
        # Mitglied
        if False:
            pass
        #if IMitglied.providedBy(self.request.principal):
        #    enummer = context.enummer
        #    if enummer == None:
        #        enummer = ''
        #    name1 = context.ename
        #    name2 = context.estrasse + ' ' + enummer
        #    name3 = context.eplz + ' ' + context.eort
        #    stra = context.estrasse + ' ' + enummer
        #    plz = context.eplz
        #    ort = context.eort
        #    adressetraeger = adresse['iknam1'] # WICHTIG Hier noch die weitere Adresse einfuegen und testen
        # Einrichtung
        else:
            if 'iknam1' in adresse:
                name1 = adresse['iknam1']
                name2 = adresse['iknam2']
                name3 = adresse['iknam3']
                stra = adresse['ikstr'] + adresse['ikhnr']
                plz = str(adresse['ikhplz'])
                ort = adresse['ikhort']
            else:
                name1 = "fehlt:adresse['iknam1']"
                name2 = "fehlt:adresse['iknam2']"
                name3 = "fehlt:adresse['iknam3']"
                stra = "fehlt:adresse['ikstr'] + adresse['ikhnr']"
                plz = "fehlt:str(adresse['ikhplz'])"
                ort = "fehlt:adresse['ikhort']"

            adressetraeger = context.traeger
        # Daten einfuegen...
        ufb_1 = '%s %s %s %s' % (name1, name2, name3, adressetraeger)
        xml.element("ufb_1", ufb_1[:200])
        xml.element("ufb_2", '')
        xml.element("ufb_3", plz)
        xml.element("ufb_4", ort[:30])
        xml.element("ufb_5", stra[:46])
        xml.element("ufb_6", '')
        xml.element("ufb_7", '')
        xml.end("ufb")

        xml.start("eti")
        xml.element("eti_1", date)
        xml.element("eti_2", time)
        xml.end("eti")

        xml.start("ksd")
        xml.element("ksd_1", 'unbekannt')
        xml.element("ksd_5", '1')
        xml.element("ksd_2", '')
        xml.element("ksd_3", '')
        xml.element("ksd_4", '')
        xml.end("ksd")

        xml.start("ufd")
        xml.element("ufd_1", context.unfzeit)
        xml.element("ufd_2", context.uadbavon)
        xml.element("ufd_3", context.uadbabis)
        xml.end("ufd")

        xml.start("ebh")
        # ebh_1 Pseudodatum eigefuegt 30.11.2011
        xml.element("ebh_1", '99.99.9999')
        if context.unfeba1:
            xml.element("ebh_2", context.unfeba1[:30])
        else:
            xml.element("ebh_2", '')
        xml.end("ebh")

        xml.start("dis")
        dis_1 = "%s %s" % (context.diavkt, context.diaadv)
        if context.prstkz == 'ja':
            dis_1 = u'tödlicher Unfall: %s' %dis_1
        xml.element("dis_1", dis_1[:100])
        xml.element("dis_4", '')
        xml.element("dis_3", '')
        xml.end("dis")

        xml.start("afb")
        if context.unfae1:
            eingestellt = context.unfae1
        else:
            eingestellt = ' '
        toedlich = context.prstkz
        if eingestellt == 'nein':
            afb_1 = '0'
            afb_4 = ''
        elif toedlich == 'ja':
            afb_1 = '1'
            afb_4 = ''
        else:
            afb_1 = '1'
        xml.element("afb_1", afb_1)
        if 'sofort' in eingestellt:
            afb_4 = uvt_4
        elif 'spaeter' in eingestellt:
            afb_4 = '%s.%s.20%s' % (context.unfaedatum[0:2],context.unfaedatum[3:5],
                                       context.unfaedatum[8:11])
            #In der Unfallanzeige kann das Datum in afb_4 nicht verarbeitet werden
            #afb_4 = '%s.%s.20%s %s' % (context.unfaedatum[0:2],context.unfaedatum[3:5],
            #                           context.unfaedatum[8:11], context.unfaezeit)
        xml.element("afb_4", afb_4)
        arbeitsfaehig = context.unfwa1
        if arbeitsfaehig == 'nein' or arbeitsfaehig == None:
            afb_7 = ''
        else:
            if context.unfwax == None:
                afb_7 = ''
            else:
                afb_7 = '%s.%s.%s' % (context.unfwax[0:2], context.unfwax[3:5],
                                      context.unfwax[6:11])
        xml.element("afb_7", afb_7)
        xml.element("afb_8", '')
        xml.end("afb")

        xml.start("abs")
        xml.element("abs_1", context.unfus2[:81])
        xml.element("abs_2", '')
        xml.element("abs_3", '')
        xml.element("abs_4", 'Extranet')
        xml.element("abs_5", '')
        xml.element("abs_6", context.anspfon)
        xml.element("abs_7", context.anspname)
        xml.end("abs")

        xml.start("uaz")
        xml.element("uaz_1", context.unfhg1[:3000])
        uaz_2 = context.unfhg2
        if uaz_2 == 'des Versicherten':
            uaz_2 = '1'
        else:
            uaz_2 = '2'
        xml.element("uaz_2", uaz_2)
        xml.element("uaz_3", context.unfort[:200])

        if context.prstkz == 'ja':
            uaz_4 = '1'
        else:
            uaz_4 = '2'
        xml.element("uaz_4", uaz_4)
        xml.element("uaz_5", context.unfkn1)
        if context.unfkn2 == 'ja':
            uaz_6 = '1'
        else:
            uaz_6 = '2'
        xml.element("uaz_6", uaz_6)
        xml.element("uaz_7", 'nein')
        xml.element("uaz_8", '1')
        xml.element("uaz_9", '0')
        xml.element("uaz_10", context.prsvtr)
        xml.element("uaz_11", oid)
        xml.end("uaz")

        xml.close(suaz)
        io.seek(0)
        # utf-8 wurde auskommentiert, da cusa nur Dateien mit header iso-8859-1 verarbeiten kann (das verstehe wer will)
        # xml_file.write(etree.tostring(etree.parse(io), pretty_print=True, encoding="utf-8", xml_declaration=True))
        xml_file.write(etree.tostring(etree.parse(io), pretty_print=True, encoding="ISO-8859-1", xml_declaration=True))
        xml_file.close()
        return io
