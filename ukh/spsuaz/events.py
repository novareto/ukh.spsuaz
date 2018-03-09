#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ukh.kiunfallanzeige
# events.py

import os
import datetime
import grok
import grokcore.message
import uvcsite
import zope.app.appsetup.product
import transaction

from .components import ISUnfallanzeige
from hurry.workflow.interfaces import IWorkflowInfo
from uvcsite import IStammdaten
from zope.component import getMultiAdapter

#output = zope.app.appsetup.product.getProductConfiguration('outputdirs')


def getDaleDir():
    """
    Gibt das Directory für die Speicherung der DALE-Dokumente
    zurück und legt das Verzeichnis an, wenn es nicht
    bereits existiert.
    """
    # basepath = '/transfer/unfallanzeige/euaz'
    basepath = '/tmp/euaz'
    archdir = datetime.datetime.now().strftime('%y/%m/%d')
    path = '%s/%s' % (basepath, archdir)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def generateFilename(pfad, user, id, suffix):
    '''
    generiert den Dateinamen aus Datum, Mitgliedsnummer, Anwendung und Endung
    '''
    filename = "%s/%s_%s.%s" % (pfad, user, id, suffix)
    return filename


@grok.subscribe(ISUnfallanzeige, uvcsite.IAfterSaveEvent)
def handle_save(obj, event, transition='publish'):
    sp = transaction.savepoint()
    """
    Erzeugt die Exporte fuer die Kinder-Unfallanzeige
    """
    ####import pdb; pdb.set_trace()
    try:
        obj_state = uvcsite.workflow.basic_workflow.WorkflowState(obj)
        if obj_state.getState() != 1:
            principal = event.principal
            pdf_pfad = xml_pfad = getDaleDir()
            if (obj.behandlung == 'Versand'):
                # PDF Erstellen
                fnPDF = generateFilename(pdf_pfad, obj.principal.id, obj.__name__, 'pdf')
                mypdf = getMultiAdapter((obj, event.request), name=u'kipdf')
                mypdf.create(fn=fnPDF)
                # XML Erstellen
                fnXML = generateFilename(xml_pfad, obj.principal.id, obj.__name__, 'dale.xml')
                mydale = getMultiAdapter((obj, event.request), name=u'kixml')
                mydale.update(filename=fnXML)
                mydale.base_file.close()
                IWorkflowInfo(obj).fireTransition(transition)
                ####grokcore.message.send(u'Vielen Dank, Ihre Unfallanzeige wurde gespeichert und versendet!')
            else:
                ####grokcore.message.send(u'Vielen Dank, Ihre Unfallanzeige wurde als Entwurf  \
                ####                        gespeichert. Sie können zu \
                ####                        einem beliebigen Zeitpunkt mit der Bearbeitung fortfahren.')
                pass
        else:
            grokcore.message.send(u'Ihre Unfallanzeige wurde bereits versendet und befindet sich in dem Verzeichnis der Unfallanzeigen.')

    except StandardError:
        sp.rollback()
        IWorkflowInfo(obj).fireTransition('progress')
        uvcsite.logger.exception("Achtung FEHLER")
