# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                      Ark
                                 A QGIS plugin
             QGIS Plugin for ARK, the Archaeological Recording Kit
                              -------------------
        begin                : 2015-03-02
        git sha              : $Format:%H$
        copyright            : (C) 2015 by L - P: Heritage LLP
        copyright            : (C) 2015 by John Layt
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
from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QMessageBox

from qgis.core import *

import utils

class LayerCollectionSettings:

    collectionDir = QDir()
    collectionCrs = ''
    collectionGroupName = ''
    bufferGroupName = ''

    pointsLayerName = ''
    pointsLayerPath = ''
    pointsStylePath = ''
    pointsLayerFields = QgsFields()

    linesLayerName = ''
    linesLayerPath = ''
    linesStylePath = ''
    linesLayerFields = QgsFields()

    polygonsLayerName = ''
    polygonsLayerPath = ''
    polygonsStylePath = ''
    polygonsLayerFields = QgsFields()

    # Scope, Boundary, Reach, Dimension, Schematic???
    scopeLayerName = ''
    scopeLayerPath = ''
    scopeStylePath = ''
    scopeLayerFields = QgsFields()


class LayerCollection:

    pointsLayer = None
    linesLayer = None
    polygonsLayer = None
    scopeLayer = None

    pointsBuffer = None
    linesBuffer = None
    polygonsBuffer = None
    scopeBuffer = None

    # Internal variables

    _iface = None # QgsInterface()
    _settings = LayerCollectionSettings()
    _collectionGroupIndex =-1
    _bufferGroupIndex = -1

    filter = ''

    def __init__(self, iface, settings):
        self._iface = iface
        self._settings = settings
        # If the legend indexes change make sure we stay updated
        self._iface.legendInterface().groupIndexChanged.connect(self._groupIndexChanged)

    def initialise(self):
        self.loadCollection()

    def unload(self):
        self.unloadBuffers()

    def unloadBuffers(self):
        if self.pointsBuffer is not None:
            QgsMapLayerRegistry.instance().removeMapLayer(self.pointsBuffer.id())
        if self.linesBuffer is not None:
            QgsMapLayerRegistry.instance().removeMapLayer(self.linesBuffer.id())
        if self.polygonsBuffer is not None:
            QgsMapLayerRegistry.instance().removeMapLayer(self.polygonsBuffer.id())
        if self.scopeBuffer is not None:
            QgsMapLayerRegistry.instance().removeMapLayer(self.scopeBuffer.id())
        if self._bufferGroupIndex >= 0:
            self._iface.legendInterface().removeGroup(self._bufferGroupIndex)

    def _groupIndexChanged(self, oldIndex, newIndex):
        if (oldIndex == self._collectionGroupIndex):
            self._collectionGroupIndex = newIndex
        elif (oldIndex == self._bufferGroupIndex):
            self._bufferGroupIndex = newIndex

    def _addLayerToLegend(self, layer, group):
        if (layer is not None and layer.isValid()):
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            self._iface.legendInterface().moveLayer(layer, group)
            self._iface.legendInterface().refreshLayerSymbology(layer)

    def _loadLayer(self, layerName, layerPath, stylePath, groupIndex):
        if (layerName is None or layerName == '' or layerPath is None or layerPath == ''):
            return None
        # If the layer is already loaded, use it and return
        layerList = QgsMapLayerRegistry.instance().mapLayersByName(layerName)
        if (len(layerList) > 0):
            self._iface.legendInterface().moveLayer(layerList[0], groupIndex)
            return layerList[0]
        # Otherwise load the layer and add it to the legend
        layer = QgsVectorLayer(layerPath, layerName, "ogr")
        if (layer is not None and layer.isValid()):
            self._setDefaultSnapping(layer)
            if (stylePath is not None and stylePath != ''):
                layer.loadNamedStyle(stylePath)
            self._addLayerToLegend(layer, groupIndex)
            return layer
        return None

    # Load the collection layers if not already loaded
    # TODO Ask to create if don't already exist
    def loadCollection(self):
        if (self._collectionGroupIndex < 0):
            self._collectionGroupIndex = utils.getGroupIndex(self._iface, self._settings._collectionGroupName)
        self.scopeLayer = self._loadLayer(self._settings.scopeLayerName, self._settings.scopeLayerPath, self._settings.scopeStylePath, self._collectionGroupIndex)
        self.polygonsLayer = self._loadLayer(self._settings.polygonsLayerName, self._settings.polygonsLayerPath, self._settings.polygonsStylePath, self._collectionGroupIndex)
        self.linesLayer = self._loadLayer(self._settings.linesLayerName, self._settings.linesLayerPath, self._settings.linesStylePath, self._collectionGroupIndex)
        self.pointsLayer = self._loadLayer(self._settings.pointsLayerName, self._settings.pointsLayerPath, self._settings.pointsStylePath, self._collectionGroupIndex)

    def _setDefaultSnapping(self, layer):
        # TODO Check if layer id already in settings, only set defaults if it isn't
        QgsProject.instance().setSnapSettingsForLayer(layer.id(), True, utils.defaultSnappingMode(), utils.defaultSnappingUnit(), utils.defaultSnappingTolerance(), False)

    # Setup the in-memory buffer layers
    def createBuffers(self):

        if (self._bufferGroupIndex < 0):
            self._bufferGroupIndex = utils.getGroupIndex(self._bufferGroupName)

        if (self.scopeBuffer is None or not self.scopeBuffer.isValid()):
            self.scopeBuffer = self._createBufferLayer(self.scopeLayer)

        if (self.polygonsBuffer is None or not self.polygonsBuffer.isValid()):
            self.polygonsBuffer = self._createBufferLayer(self.polygonsLayer)

        if (self.linesBuffer is None or not self.linesBuffer.isValid()):
            self.linesBuffer = self._createBufferLayer(self.linesLayer)

        if (self.pointsBuffer is None or not self.pointsBuffer.isValid()):
            self.pointsBuffer = self._createBufferLayer(self.pointsLayer)

    def _createBufferLayer(self, layer):
        if (layer is not None and layer.isValid()):
            buffer = self._createMemoryLayer(layer)
            if (buffer is not None and buffer.isValid()):
                self._addLayerToLegend(buffer, self._bufferGroupIndex)
                buffer.startEditing()
                return buffer
        return None

    def _createLayer(self, type, name, provider, attributes, layerPath, stylePath):
        layer = QgsVectorLayer(layerPath, name, provider)
        if (layer is not None and layer.isValid()):
            layer.dataProvider().addAttributes(attributes)
            layer.loadNamedStyle(stylePath)
            self._setDefaultSnapping(layer)
            # TODO save layer??? crs???
        return layer

    def _createMemoryLayer(self, layer):
        if (layer is not None and layer.isValid()):
            uri = utils.wkbToMemoryType(layer.wkbType()) + "?crs=" + layer.crs().authid() + "&index=yes"
            buffer = QgsVectorLayer(uri, layer.name() + self._settings.bufferSuffix, 'memory')
            if (buffer is not None and buffer.isValid()):
                buffer.dataProvider().addAttributes(layer.dataProvider().fields().toList())
                buffer.loadNamedStyle(layer.styleURI())
            return buffer
        return None

    def okToMergeBuffers(self):
        return self.isCollectionEditable()

    def isCollectionEditable(self):
        return self._isLayerEditable(self.pointsLayer) and self._isLayerEditable(self.linesLayer) and self._isLayerEditable(self.polygonsLayer) and self._isLayerEditable(self.scopeLayer)

    def _isLayerEditable(self, layer):
        if (layer.type() != QgsMapLayer.VectorLayer):
            self._settings.showCriticalMessage('Cannot edit layer ' + layer.name() + ' - Not a vector layer')
            return False
        if (layer.isModified()):
            self._settings.showCriticalMessage('Cannot edit layer ' + layer.name() + ' - Has pending modifications')
            return False
        # We don't check here as can turn filter off temporarily
        #if (layer.subsetString()):
        #    self._settings.showCriticalMessage('Cannot edit layer ' + layer.name() + ' - Filter is applied')
        #    return False
        if (len(layer.vectorJoins()) > 0):
            self._settings.showCriticalMessage('Cannot edit layer ' + layer.name() + ' - Layer has joins')
            return False
        return True

    def _clearBuffer(self, type, buffer, undoMessage=''):
        message = undoMessage
        if (not undoMessage):
            message = 'Clear buffer'
        message = message + ' - ' + type
        buffer.selectAll()
        if (buffer.selectedFeatureCount() > 0):
            if not buffer.isEditable():
                buffer.startEditing()
            buffer.beginEditCommand(message)
            buffer.deleteSelectedFeatures()
            buffer.endEditCommand()
            buffer.commitChanges()
            buffer.startEditing()
        buffer.removeSelection()

    def _copyBuffer(self, type, buffer, layer, undoMessage=''):
        ok = False
        message = undoMessage
        if (not undoMessage):
            message = 'Merge data'
        message = message + ' - ' + type
        filter = layer.subsetString()
        if filter:
            layer.setSubsetString('')
        buffer.selectAll()
        if (buffer.selectedFeatureCount() > 0):
            if layer.startEditing():
                layer.beginEditCommand(message)
                ok = layer.addFeatures(buffer.selectedFeatures(), False)
                layer.endEditCommand()
                if ok:
                    ok = layer.commitChanges()
        else:
            ok = True
        buffer.removeSelection()
        if filter:
            layer.setSubsetString(filter)
        return ok

    def mergeBuffers(self, undoMessage):
        if self._copyBuffer('levels', self.pointsBuffer, self.pointsLayer, undoMessage):
            self._clearBuffer('levels', self.pointsBuffer, undoMessage)
        if self._copyBuffer('lines', self.linesBuffer, self.linesLayer, undoMessage):
            self._clearBuffer('lines', self.linesBuffer, undoMessage)
        if self._copyBuffer('polygons', self.polygonsBuffer, self.polygonsLayer, undoMessage):
            self._clearBuffer('polygons', self.polygonsBuffer, undoMessage)
        if self._copyBuffer('scope', self.scopeBuffer, self.scopeLayer, undoMessage):
            self._clearBuffer('scope', self.scopeBuffer, undoMessage)

    def _clearBuffers(self, undoMessage):
        self._clearBuffer('levels', self.pointsBuffer, undoMessage)
        self._clearBuffer('lines', self.linesBuffer, undoMessage)
        self._clearBuffer('polygons', self.polygonsBuffer, undoMessage)
        self._clearBuffer('scope', self.scopeBuffer, undoMessage)


    def showPoints(self, status):
        self._iface.legendInterface().setLayerVisible(self.pointsLayer, status)

    def showLines(self, status):
        self._iface.legendInterface().setLayerVisible(self.linesLayer, status)

    def showPolygons(self, status):
        self._iface.legendInterface().setLayerVisible(self.polygonsLayer, status)

    def showScope(self, status):
        self._iface.legendInterface().setLayerVisible(self.scopeLayer, status)


    def applyFilter(self, filter):
        self.filter = filter
        self._applyLayerFilter(self.pointsLayer, self.filter)
        self._applyLayerFilter(self.linesLayer, self.filter)
        self._applyLayerFilter(self.polygonsLayer, self.filter)
        self._applyLayerFilter(self.scopeLayer, self.filter)


    def _applyLayerFilter(self, layer, filter):
        if (layer is None):
            return
        if (self._iface.mapCanvas().isDrawing()):
            self._settings.showMessage('Cannot apply filter: Canvas is drawing')
            return
        if (layer.type() != QgsMapLayer.VectorLayer):
            self._settings.showMessage('Cannot apply filter: Not a vector layer')
            return
        if (layer.isEditable()):
            self._settings.showMessage('Cannot apply filter: Layer is in editing mode')
            return
        if (not layer.dataProvider().supportsSubsetString()):
            self._settings.showMessage('Cannot apply filter: Subsets not supported by layer')
            return
        if (len(layer.vectorJoins()) > 0):
            self._settings.showMessage('Cannot apply filter: Layer has joins')
            return
        layer.setSubsetString(filter)
        self._iface.mapCanvas().refresh()
        self._iface.legendInterface().refreshLayerSymbology(layer)


    def zoomToCollection(self):
        self.pointsLayer.updateExtents()
        self.linesLayer.updateExtents()
        self.polygonsLayer.updateExtents()
        self.scopeLayer.updateExtents()
        self.pointsBuffer.updateExtents()
        self.linesBuffer.updateExtents()
        self.polygonsBuffer.updateExtents()
        self.scopeBuffer.updateExtents()
        extent = QgsRectangle()
        extent = self._extendExtent(extent, self.pointsLayer)
        extent = self._extendExtent(extent, self.linesLayer)
        extent = self._extendExtent(extent, self.polygonsLayer)
        extent = self._extendExtent(extent, self.scopeLayer)
        extent = self._extendExtent(extent, self.pointsBuffer)
        extent = self._extendExtent(extent, self.linesBuffer)
        extent = self._extendExtent(extent, self.polygonsBuffer)
        extent = self._extendExtent(extent, self.scopeBuffer)
        if (extent is not None and not extent.isNull()):
            extent.scale(1.05)
            self._iface.mapCanvas().setExtent(extent)
            self._iface.mapCanvas().refresh()


    def _extendExtent(self, extent, layer):
        layerExtent = QgsRectangle()
        if (layer is not None and layer.isValid() and layer.featureCount() > 0 and self._iface.legendInterface().isLayerVisible(layer)):
            layerExtent = layer.extent()
        if (extent is None and layerExtent is None):
            return QgsRectangle()
        elif (extent is None or extent.isNull()):
            return layerExtent
        elif (layerExtent is None or layerExtent.isNull()):
            return extent
        return extent.combineExtentWith(layerExtent)
