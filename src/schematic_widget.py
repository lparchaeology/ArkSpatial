# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
        email                : john@layt.net
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import uic
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QWidget, QPixmap, QToolButton

from qgis.core import QgsMessageLog

from ..libarkqgis.dock import ToolDockWidget
from ..libarkqgis.event_filters import ReturnPressedFilter

from plan_item import ItemKey

import schematic_widget_base

import resources

class SearchStatus():

    Unknown = 0
    Found = 1
    NotFound = 2

class SchematicWidget(QWidget, schematic_widget_base.Ui_SchematicWidget):

    findContextSelected = pyqtSignal()
    firstContextSelected = pyqtSignal()
    lastContextSelected = pyqtSignal()
    nextContextSelected = pyqtSignal()
    prevContextSelected = pyqtSignal()
    editContextSelected = pyqtSignal()
    findSourceSelected = pyqtSignal()
    copySourceSelected = pyqtSignal()
    cloneSourceSelected = pyqtSignal()
    editSourceSelected = pyqtSignal()
    contextChanged = pyqtSignal()
    resetSelected = pyqtSignal()

    _contextArkDataStatus = SearchStatus.Unknown
    _contextFeatureDataStatus = SearchStatus.Unknown
    _contextSchematicStatus = SearchStatus.Unknown
    _sourceDataStatus = SearchStatus.Unknown
    _sourceSchematicStatus = SearchStatus.Unknown

    def __init__(self, parent=None):
        super(SchematicWidget, self).__init__(parent)
        self.setupUi(self)

    def initGui(self):
        self.siteCodeCombo.currentIndexChanged.connect(self._contextChanged)
        self.contextSpin.valueChanged.connect(self._contextChanged)
        self._contextSpinFilter = ReturnPressedFilter(self)
        self.contextSpin.installEventFilter(self._contextSpinFilter)
        self._contextSpinFilter.returnPressed.connect(self.findContextSelected)
        self.findContextTool.clicked.connect(self.findContextSelected)
        self.firstContextTool.clicked.connect(self.firstContextSelected)
        self.lastContextTool.clicked.connect(self.lastContextSelected)
        self.nextContextTool.clicked.connect(self.nextContextSelected)
        self.prevContextTool.clicked.connect(self.prevContextSelected)
        self.editContextButton.clicked.connect(self.editContextSelected)
        self.sourceContextSpin.valueChanged.connect(self._sourceContextChanged)
        self._sourceSpinFilter = ReturnPressedFilter(self)
        self.sourceContextSpin.installEventFilter(self._sourceSpinFilter)
        self._sourceSpinFilter.returnPressed.connect(self.findSourceSelected)
        self.findSourceTool.clicked.connect(self.findSourceSelected)
        self.copySourceButton.clicked.connect(self.copySourceSelected)
        self.cloneSourceButton.clicked.connect(self.cloneSourceSelected)
        self.editSourceButton.clicked.connect(self.editSourceSelected)
        self.resetButton.clicked.connect(self.resetSelected)

    def unloadGui(self):
        pass

    def loadProject(self, project):
        self.siteCodeCombo.clear()
        for siteCode in sorted(set(project.siteCodes())):
            self.siteCodeCombo.addItem(siteCode, siteCode)
        idx = self.siteCodeCombo.findData(project.siteCode())
        if idx >= 0:
            self.siteCodeCombo.setCurrentIndex(idx)
        self.resetContext()

    def closeProject(self):
        pass

    # Context Tools

    def siteCode(self):
        return self.siteCodeCombo.itemData(self.siteCodeCombo.currentIndex())

    def contextItemKey(self):
        return ItemKey(self.siteCode(), 'cxt', self.context())

    def context(self):
        return self.contextSpin.value()

    def resetContext(self):
        self.setContext(ItemKey())

    def setContext(self, context, foundArkData=SearchStatus.Unknown, foundFeatureData=SearchStatus.Unknown, foundSchematic=SearchStatus.Unknown, foundSectionSchematic=SearchStatus.Unknown):
        if context.isValid():
            self.blockSignals(True)
            self.contextSpin.setValue(int(context.itemId))
            self._setContextStatus(foundArkData, foundFeatureData, foundSchematic, foundSectionSchematic)
            self.blockSignals(False)
        else:
            self.contextSpin.setValue(0)
            self._setContextStatus()
        self.resetSourceContext()

    def contextStatus(self):
        if self._contextFeatureDataStatus == SearchStatus.Unknown or self._contextSchematicStatus == SearchStatus.Unknown:
            return SearchStatus.Unknown
        if self._contextFeatureDataStatus == SearchStatus.Found or self._contextSchematicStatus == SearchStatus.Found:
            return SearchStatus.Found
        return SearchStatus.NotFound

    def _setContextStatus(self, foundArkData=SearchStatus.Unknown, foundFeatureData=SearchStatus.Unknown, foundSchematic=SearchStatus.Unknown, foundSectionSchematic=SearchStatus.Unknown):
        self._contextArkDataStatus = foundArkData
        self._contextFeatureDataStatus = foundFeatureData
        self._contextSchematicStatus = foundSchematic
        self._setStatusLabel(self.arkDataStatusLabel, foundArkData)
        self._setStatusLabel(self.featureDataStatusLabel, foundFeatureData)
        self._setStatusLabel(self.schematicStatusLabel, foundSchematic)
        self._setStatusLabel(self.sectionSchematicStatusLabel, foundSectionSchematic)
        self.editContextButton.setEnabled(self.contextStatus() == SearchStatus.Found)
        self._enableSource(foundSchematic == SearchStatus.NotFound)

    def sourceItemKey(self):
        return ItemKey(self.siteCode(), 'cxt', self.sourceContext())

    def sourceContext(self):
        return self.sourceContextSpin.value()

    def resetSourceContext(self):
        self.setSourceContext(ItemKey())

    def setSourceContext(self, context, foundData=SearchStatus.Unknown, foundSchematic=SearchStatus.Unknown):
        if context.isValid():
            self.sourceContextSpin.setValue(int(context.itemId))
            self._setSourceStatus(foundData, foundSchematic)
        else:
            self.sourceContextSpin.setValue(0)
            self._setSourceStatus()

    def sourceStatus(self):
        if self._sourceDataStatus == SearchStatus.Unknown or self._sourceSchematicStatus == SearchStatus.Unknown:
            return SearchStatus.Unknown
        if self._sourceDataStatus == SearchStatus.Found or self._sourceSchematicStatus == SearchStatus.Found:
            return SearchStatus.Found
        return SearchStatus.NotFound

    def _setSourceStatus(self, foundData=SearchStatus.Unknown, foundSchematic=SearchStatus.Unknown):
        self._sourceDataStatus = foundData
        self._sourceSchematicStatus = foundSchematic
        self._setStatusLabel(self.sourceDataStatusLabel, foundData)
        self._setStatusLabel(self.sourceSchematicStatusLabel, foundSchematic)
        self._enableClone(foundSchematic == SearchStatus.Found)
        self.editSourceButton.setEnabled(self.sourceStatus() == SearchStatus.Found)

    def _setStatusLabel(self, label, status):
        if status == SearchStatus.Found:
            label.setPixmap(QPixmap(':/plugins/ark/plan/statusFound.png'))
        elif status == SearchStatus.NotFound:
            label.setPixmap(QPixmap(':/plugins/ark/plan/statusNotFound.png'))
        else:
            label.setPixmap(QPixmap(':/plugins/ark/plan/statusUnknown.png'))

    def _enableSource(self, enable):
        self.sourceContextSpin.setEnabled(enable)
        if enable:
            self.sourceContextSpin.setFocus()
        self.findSourceTool.setEnabled(enable)
        if not enable:
            self._enableClone(enable)

    def _enableClone(self, enable):
        self.copySourceButton.setEnabled(enable)
        self.cloneSourceButton.setEnabled(enable)

    def _contextChanged(self):
        self._setContextStatus()
        self.resetSourceContext()
        self.contextChanged.emit()

    def _sourceContextChanged(self):
        self._setSourceStatus(SearchStatus.Unknown, SearchStatus.Unknown)
