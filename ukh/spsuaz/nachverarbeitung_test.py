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
                pid = str(item.principal.id)
                if pid == "32519":
                    #print IWorkflowState(item).getState()
                    print '################################################################'
                    print "%s/%s" % (homefolder.__name__, item.title)
                    print '################################################################'
    print '################################################################'
    print '...Ende'
    print '################################################################'

if __name__ == "__main__":
    worker()
    exit()

