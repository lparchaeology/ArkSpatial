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
from PyQt4.QtCore import QVariant, QFile
from PyQt4.QtGui import QMessageBox

from qgis.core import *

from settings import *
from layercollection import *

class LayerManager:

    geoLayer = None  #QgsRasterLayer()
    contexts = None  # LayerCollection()
    grid = None  # LayerCollection()

    # Internal variables

    _settings = None # Settings()


    def __init__(self, settings):
        self._settings = settings
        # If the legend indexes change make sure we stay updated
        self._settings.iface.legendInterface().groupIndexChanged.connect(self._groupIndexChanged)


    def initialise(self):
        self.contexts = self._createCollection('contexts')
        self.contexts.initialise()
        self.grid = self._createCollection('grid')
        self.grid.initialise()


    def unload(self):
        if self.contexts is not None:
            self.contexts.unload()
        if self.grid is not None:
            self.grid.unload()


    def _groupIndexChanged(self, oldIndex, newIndex):
        if (oldIndex == self._settings.projectGroupIndex):
            self._settings.projectGroupIndex = newIndex


    def loadGeoLayer(self, geoFile):
        #TODO Check if already loaded, remove old one?
        self.geoLayer = QgsRasterLayer(geoFile.absoluteFilePath(), geoFile.completeBaseName())
        self.geoLayer.renderer().setOpacity(self._settings.planTransparency()/100.0)
        QgsMapLayerRegistry.instance().addMapLayer(self.geoLayer)
        if (self._settings.planGroupIndex < 0):
            self._settings.planGroupIndex = self.getGroupIndex(self._settings.planGroupName)
        self._settings.iface.legendInterface().moveLayer(self.geoLayer, self._settings.planGroupIndex)
        self._settings.iface.mapCanvas().setExtent(self.geoLayer.extent())


    def applyContextFilter(self, contextList):
        self.contexts.applyFilter(self._settings.contextAttributeName, contextList)


    def _shapeFile(self, layerPath, layerName):
        return layerPath + '/' + layerName + '.shp'


    def _styleFile(self, layerPath, layerName, baseName, defaultName):
        # First see if the layer itself has a default style saved
        filePath = layerPath + '/' + layerName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Next see if the base name has a style in the styles folder (which may be a special folder, the site folder or the plugin folder)
        filePath = self._settings.stylePath() + '/' + baseName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Next see if the default name has a style in the style folder
        filePath = self._settings.stylePath() + '/' + defaultName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Finally, check the plugin folder for the default style
        filePath = self._settings.stylePath() + '/' + defaultName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # If we didn't find that then something is wrong!
        return ''


    def _createCollection(self, module):
        path = self._settings.modulePath(module)
        lcs = LayerCollectionSettings()
        lcs.collectionGroupName = self._settings.layersGroupName(module)
        lcs.buffersGroupName = self._settings.buffersGroupName(module)
        lcs.bufferSuffix = self._settings.bufferSuffix
        lcs.pointsLayerProvider = 'ogr'
        lcs.pointsLayerName = self._settings.pointsLayerName(module)
        lcs.pointsLayerPath = self._shapeFile(path, lcs.pointsLayerName)
        lcs.pointsStylePath = self._styleFile(path, lcs.pointsLayerName, self._settings.pointsBaseName(module), self._settings.pointsBaseNameDefault(module))
        lcs.linesLayerProvider = 'ogr'
        lcs.linesLayerName = self._settings.linesLayerName(module)
        lcs.linesLayerPath = self._shapeFile(path, lcs.linesLayerName)
        lcs.linesStylePath = self._styleFile(path, lcs.linesLayerName, self._settings.linesBaseName(module), self._settings.linesBaseNameDefault(module))
        lcs.polygonsLayerProvider = 'ogr'
        lcs.polygonsLayerName = self._settings.polygonsLayerName(module)
        lcs.polygonsLayerPath = self._shapeFile(path, lcs.polygonsLayerName)
        lcs.polygonsStylePath = self._styleFile(path, lcs.polygonsLayerName, self._settings.polygonsBaseName(module), self._settings.polygonsBaseNameDefault(module))
        lcs.schemaLayerProvider = 'ogr'
        lcs.schemaLayerName = self._settings.schemaLayerName(module)
        lcs.schemaLayerPath = self._shapeFile(self._settings.modulePath(module), lcs.schemaLayerName)
        lcs.schemaStylePath = self._styleFile(self._settings.modulePath(module), lcs.schemaLayerName, self._settings.schemaBaseName(module), self._settings.schemaBaseNameDefault(module))
        return LayerCollection(self._settings.iface, lcs)

