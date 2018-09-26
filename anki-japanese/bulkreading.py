# -*- coding: utf-8 -*-
# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Bulk update of readings.
#

from aqt.qt import *
from anki.hooks import addHook
from japanese.reading import mecab, sourceFieldToDestinationField
from .notetypes import isJapaneseNoteType
from aqt import mw

# Bulk updates
##########################################################################

def regenerateReadings(nids):
    global mecab
    mw.checkpoint("Bulk-add Readings")
    mw.progress.start()
    for nid in nids:
        note = mw.col.getNote(nid)
        # Amend notetypes.py to add your note types
        _noteName = note.model()['name'].lower()
        if not isJapaneseNoteType(_noteName):
            continue
        for sourceField, destinationField in sourceFieldToDestinationField.items():
            if sourceField not in note:
                continue
            elif destinationField not in note:
                continue
            elif note[destinationField]: # already contains data
                continue
            sourceFieldText = mw.col.media.strip(note[sourceField])
            if not sourceFieldText.strip():
                continue
            try:
                note[destinationField] = mecab.reading(sourceFieldText)
            except Exception as e:
                mecab = None
                raise
        note.flush()
    mw.progress.finish()
    mw.reset()

def setupMenu(browser):
    a = QAction("Bulk-add Readings", browser)
    a.triggered.connect(lambda: onRegenerate(browser))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)

def onRegenerate(browser):
    regenerateReadings(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
