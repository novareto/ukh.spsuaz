#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ukh.kiunfallanzeige
# nachverarbeitung....py

import grok
import transaction
import zope.app.appsetup.product

from zope import component
from zope.publisher.browser import TestRequest
from zope.app.homefolder.interfaces import IHomeFolderManager
from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowState, InvalidTransitionError
from uvc.layout.forms.event import AfterSaveEvent
from ukh.markers.interfaces import IMitglied, IEinrichtung
from zope.interface.declarations import alsoProvides

output = zope.app.appsetup.product.getProductConfiguration('outputdirs')


def geteventobject(principal):
    myevent = TestRequest()
    myevent.setPrincipal(principal)
    return myevent


def worker():
    print '################################################################'
    print 'Start...'
    print '################################################################'
    uvcsite = root['app']
    component.hooks.setSite(uvcsite)
    hfm = component.getUtility(IHomeFolderManager).homeFolderBase
    for homefolder in hfm.values():
        #for item in homefolder:
        #    print item
        if 'Sunfallanzeigen' in homefolder:
            for item in homefolder['Sunfallanzeigen'].values():
                #pid = str(item.principal.id)
                #print pid
                #print IWorkflowState(item).getState()
                if IWorkflowState(item).getState() == 2:
                    print '################################################################'
                    print 'Fehlerhafte Unfallanzeige gefunden:'
                    print "%s/%s" % (homefolder.__name__, item.title)
                    print '################################################################'
                    print 'Bitte Dokument anschauen und Fehler beheben !'
                    print 'Dann Code der Nachverarbeitung aendern:'
                    print '1. Dokument neu erstellen und versenden, NICHT fixen !!!'
                    print '2. Dokument fixen, OHNE Erstellung !!!'
                    print '################################################################'
                    ##### Status: 0 = Nur schauen, was laeuft falsch
                    #####         1 = Dokument neu erstellen
                    #####         2 = Dokument fixen (Status gesendet)
                    ##### Nachfolgenden Status setzen:
                    status = 0  # <----- Dort: 0, 1 oder 2
                    if status == 0:
                        print "-----> Es wurde noch keine Aktion ausgeführt"
                        print "Status: ", status
                    elif status == 1:
                        modprincipal = item.principal
                        alsoProvides(modprincipal, MoE)
                        event_obj = geteventobject(modprincipal)
                        try:
                            grok.notify(AfterSaveEvent(item, event_obj))
                        except InvalidTransitionError:
                            print "-----> Dokumente wurden erstellt, Status umstellen zum fixen !!!"
                            print "Status: ", status
                        except Exception, e:
                            print e
                            pass
                    elif status == 2:
                        IWorkflowInfo(item).fireTransition('fix')
                        print "-----> Dokumente gefixt !!!"
                        print "       Status umstellen auf --> 0 <--"
                        print "Status: ", status
                        print 'FIX of object %s' % item
    print '################################################################'
    print '...Ende'
    print '################################################################'
    transaction.commit()

if __name__ == "__main__":
    worker()
    exit()

