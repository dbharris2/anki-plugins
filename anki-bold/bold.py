# -*- coding: utf-8 -*-
# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Bulk update of readings.
#

from aqt.qt import *
from anki.hooks import addHook
from aqt import mw

def performBoldAction(noteIds):
    mw.checkpoint("Bulk-add Bold")
    mw.progress.start()
    for noteId in noteIds:
        note = mw.col.getNote(noteId)
        if 'Expression' not in note:
            continue
        elif 'Morphman_FocusMorph' not in note:
            continue
        expression = mw.col.media.strip(note['Expression'])
        word = mw.col.media.strip(note['Morphman_FocusMorph'])
        note['Expression'] = expression.replace(word, "<b>%s</b>" % word)
        note.flush()
    mw.progress.finish()
    mw.reset()

def onSelectBoldAction(browser):
    performBoldAction(browser.selectedNotes())

def setupMenu(browser):
    boldAction = QAction("Bulk-add Bold", browser)
    boldAction.triggered.connect(lambda: onSelectBoldAction(browser))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(boldAction)
    browser.form.menuEdit.addSeparator()

addHook("browser.setupMenus", setupMenu)
