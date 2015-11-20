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
from PyQt4.QtCore import Qt, QVariant, QFileInfo, QObject, QDir
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QInputDialog

from qgis.core import *

from ..libarkqgis.map_tools import *
from ..libarkqgis import utils
from ..libarkqgis import processing

from ..georef.georef_dialog import GeorefDialog

from plan_dock import PlanDock
from edit_dock import EditDock
from schematic_dock import SchematicDock, SearchStatus
from select_drawing_dialog import SelectDrawingDialog

from filter import FilterType, FilterAction
from plan_util import *
from config import Config
from metadata import Metadata, FeatureData

import resources_rc

def _quote(string):
    return "'" + string + "'"

def _doublequote(string):
    return '"' + string + '"'

class Plan(QObject):

    # Project settings
    project = None # Project()

    dock = None # PlanDock()
    editDock = None # EditDock()
    schematicDock = None # SchematicDock()

    # Internal variables
    initialised = False
    _buffersInitialised = False

    _featureData = FeatureData()

    actions = {}
    mapTools = {}
    currentMapTool = None

    _definitiveCategories = set()
    _schematicContextIncludeFilter = -1
    _schematicContextHighlightFilter = -1
    _schematicSourceIncludeFilter = -1
    _schematicSourceHighlightFilter = -1

    def __init__(self, project):
        super(Plan, self).__init__(self.project)
        self.project = project

    # Create the gui when the plugin is first created
    def initGui(self):
        self.dock = PlanDock(self.project.dock)
        action = self.project.addDockAction(':/plugins/ArkPlan/plan/drawPlans.png', self.tr(u'Draw Archaeological Plans'), checkable=True)
        self.dock.initGui(self.project.iface, Qt.RightDockWidgetArea, action)
        self.dock.toggled.connect(self.run)

        for category in Config.featureCategories:
            #TODO Select by map tool type enum
            if category[2] == 'lvl' or category[2] == 'llv':
                self.addLevelTool(category[0], category[1], category[2], category[3], QIcon(category[4]))
            else:
                self.addDrawingTool(category[0], category[1], category[2], category[3], QIcon(category[4]), category[5])
            if category[6] == True:
                self._definitiveCategories.add(category[2])

        self.dock.loadRawFileSelected.connect(self._loadRawPlan)
        self.dock.loadGeoFileSelected.connect(self._loadGeoPlan)
        self.dock.loadContextSelected.connect(self._loadContextPlans)
        self.dock.loadPlanSelected.connect(self._loadPlans)
        self.dock.contextNumberChanged.connect(self._featureIdChanged)
        self.dock.featureIdChanged.connect(self._featureIdChanged)
        self.dock.featureNameChanged.connect(self._featureNameChanged)
        self.dock.autoSchematicSelected.connect(self._autoSchematicBufferSelected)

        self.dock.clearSelected.connect(self.clearBuffers)
        self.dock.mergeSelected.connect(self.mergeBuffers)

        self.schematicDock = SchematicDock(self.project.dock)
        action = self.project.addDockAction(':/plugins/ArkPlan/plan/checkSchematic.png', self.tr(u'Check Context Schematics'), checkable=True)
        self.schematicDock.initGui(self.project.iface, Qt.RightDockWidgetArea, action)
        self.schematicDock.addDrawingTool('sch', self.actions['sch'])
        self.schematicDock.addDrawingTool('lvl', self.actions['lvl'])
        self.schematicDock.toggled.connect(self.runSchematic)
        self.schematicDock.findContextSelected.connect(self._findContext)
        self.schematicDock.findSourceSelected.connect(self._findSource)
        self.schematicDock.copySourceSelected.connect(self._copySource)
        self.schematicDock.cloneSourceSelected.connect(self._cloneSource)
        self.schematicDock.autoSchematicSelected.connect(self._autoSchematicLayerSelected)
        self.schematicDock.resetSelected.connect(self._resetSchematic)
        self.schematicDock.clearSelected.connect(self.clearBuffers)
        self.schematicDock.mergeSelected.connect(self.mergeBuffers)
        self.project.filterModule.filterSetCleared.connect(self._resetSchematic)


        self.editDock = EditDock(self.project.iface, self.project.dock)
        action = self.project.addDockAction(':/plugins/ArkPlan/plan/editingTools.png', self.tr(u'Editing Tools'), checkable=True)
        self.editDock.initGui(self.project.iface, Qt.RightDockWidgetArea, action)
        self.editDock.toggled.connect(self.runEdit)

        self.metadata().metadataChanged.connect(self.updateMapToolAttributes)

    # Load the project settings when project is loaded
    def loadProject(self):
        self.initialiseBuffers()
        self.dock.initSourceCodes(Config.planSourceCodes)
        self.dock.initSourceClasses(Config.planSourceClasses)
        self.schematicDock.initSourceCodes(Config.planSourceCodes)
        self.schematicDock.initSourceClasses(Config.planSourceClasses)
        self.schematicDock.setContext(0, SearchStatus.Unknown, SearchStatus.Unknown)


    # Save the project
    def writeProject(self):
        pass

    # Close the project
    def closeProject(self):
        self._clearSchematicFilters()

    # Unload the module when plugin is unloaded
    def unloadGui(self):

        self.closeProject()

        for action in self.actions.values():
            if action.isChecked():
                action.setChecked(False)

        # Reset the initialisation
        self.initialised = False
        self._buffersInitialised = False

        # Unload the docks
        self.schematicDock.unloadGui()
        self.editDock.unloadGui()
        self.dock.unloadGui()

    def run(self, checked):
        if checked:
            if self.initialise():
                self.schematicDock.menuAction().setChecked(False)
                self.editDock.menuAction().setChecked(False)
            else:
                self.dock.menuAction().setChecked(False)

    def runEdit(self, checked):
        if checked:
            if self.initialise():
                self.schematicDock.menuAction().setChecked(False)
                self.dock.menuAction().setChecked(False)
            else:
                self.editDock.menuAction().setChecked(False)

    def runSchematic(self, checked):
        if checked:
            if self.initialise():
                self.dock.menuAction().setChecked(False)
                self.editDock.menuAction().setChecked(False)
            else:
                self.schematicDock.menuAction().setChecked(False)

    def initialiseBuffers(self):
        if self._buffersInitialised:
            return
        self.project.plan.createBuffers()
        self.project.plan.pointsBuffer.setFeatureFormSuppress(QgsVectorLayer.SuppressOn)
        self.project.plan.linesBuffer.setFeatureFormSuppress(QgsVectorLayer.SuppressOn)
        self.project.plan.polygonsBuffer.setFeatureFormSuppress(QgsVectorLayer.SuppressOn)
        self._buffersInitialised = True
        self.editDock.setBufferPoints(self.project.plan.pointsBuffer)
        self.editDock.setBufferLines(self.project.plan.linesBuffer)
        self.editDock.setBufferPolygons(self.project.plan.polygonsBuffer)
        self.editDock.setPlanPoints(self.project.plan.pointsLayer)
        self.editDock.setPlanLines(self.project.plan.linesLayer)
        self.editDock.setPlanPolygons(self.project.plan.polygonsLayer)
        self.editDock.setBasePoints(self.project.base.pointsLayer)
        self.editDock.setBaseLines(self.project.base.linesLayer)
        self.editDock.setBasePolygons(self.project.base.polygonsLayer)

    def metadata(self):
        if self.schematicDock.menuAction().isChecked():
            return self.schematicDock.metadata()
        return self.dock.metadata()

    # Plan Tools

    def _setPlanMetadata(self, pmd):
        self.metadata().setSiteCode(pmd.siteCode)
        self.metadata().setSourceCode('drw')
        self.metadata().setSourceClass(pmd.sourceClass)
        self.metadata().setSourceId(pmd.sourceId)
        self.metadata().setSourceFile(pmd.filename)
        if pmd.sourceClass == 'cxt':
            self.dock.setContextNumber(pmd.sourceId)
            self.dock.setFeatureId(0)
        else:
            self.dock.setContextNumber(0)
            self.dock.setFeatureId(pmd.sourceId)

    def _loadRawPlan(self):
        dialog = SelectDrawingDialog(self.project, 'cxt', self.project.siteCode())
        if (dialog.exec_()):
            for filePath in dialog.selectedFiles():
                self.georeferencePlan(QFileInfo(filePath))

    def _loadGeoPlan(self):
        dialog = SelectDrawingDialog(self.project, 'cxt', self.project.siteCode(), True)
        if (dialog.exec_()):
            for filePath in dialog.selectedFiles():
                geoFile = QFileInfo(filePath)
                self._setPlanMetadata(PlanMetadata(geoFile))
                self.project.loadGeoLayer(geoFile)

    def _loadContextPlans(self):
        context, ok = QInputDialog.getInt(None, 'Load Context Plans', 'Please enter the Context number to load all drawings for:', 1, 1, 99999)
        if (ok and context > 0):
            self.loadDrawing('cxt', self.project.siteCode(), context)

    def _loadPlans(self):
        plan, ok = QInputDialog.getInt(None, 'Load Plans', 'Please enter the Plan number to load all drawings for:', 1, 1, 99999)
        if (ok and plan > 0):
            self.loadDrawing('pln', self.project.siteCode(), plan)

    def loadDrawing(self, drawingType, siteCode, drawingId):
        drawingDir = self.project.georefDrawingDir(drawingType)
        drawingDir.setFilter(QDir.Files | QDir.NoDotAndDotDot)
        name = drawingType + '_' + siteCode + '_' + str(drawingId)
        nameList = []
        nameList.append(name + '.png')
        nameList.append(name + '.tif')
        nameList.append(name + '.tiff')
        nameList.append(name + '_*.png')
        nameList.append(name + '_*.tif')
        nameList.append(name + '_*.tiff')
        drawingDir.setNameFilters(nameList)
        drawings = drawingDir.entryInfoList()
        for drawing in drawings:
            self._setPlanMetadata(PlanMetadata(drawing))
            self.project.loadGeoLayer(drawing)

    def _featureIdChanged(self, featureId):
        self._featureData.setFeatureId(featureId)
        self.updateMapToolAttributes()

    def _featureNameChanged(self, featureName):
        if featureName is None or featureName.strip() == '':
            self._featureData.setFeatureName('')
        else:
            self._featureData.setFeatureName(featureName)
        self.updateMapToolAttributes()

    # Georeference Tools

    def georeferencePlan(self, rawFile):
        pmd = PlanMetadata(rawFile)
        georefDialog = GeorefDialog(rawFile, self.project.georefDrawingDir(pmd.sourceClass), self.project.projectCrs().authid(), self.project.pointsLayerName('grid'), self.project.fieldName('local_x'), self.project.fieldName('local_y'))
        if (georefDialog.exec_()):
            geoFile = georefDialog.geoRefFile()
            md = georefDialog.metadata()
            md.filename = geoFile.fileName()
            self._setPlanMetadata(md)
            self.project.loadGeoLayer(geoFile)

    # Layer Methods

    def mergeBuffers(self):
        self.project.plan.updateBufferAttribute(self.project.fieldName('created_on'), utils.timestamp())
        if self.project.plan.okToMergeBuffers():
            self.project.plan.mergeBuffers('Merge plan data')

    def clearBuffers(self):
        self.project.plan.clearBuffers('Clear plan buffer data')

    # Drawing tools

    def _newMapToolAction(self, classCode, category, toolName, icon):
        data = {}
        data['class'] = classCode
        data['category'] = category
        action = QAction(icon, category, self.dock)
        action.setData(data)
        action.setToolTip(toolName)
        action.setCheckable(True)
        return action

    def _newMapTool(self, toolName, featureType, buffer, action):
        mapTool = ArkMapToolAddFeature(self.project.iface, buffer, featureType, toolName)
        mapTool.setAction(action)
        mapTool.setPanningEnabled(True)
        mapTool.setZoomingEnabled(True)
        mapTool.setSnappingEnabled(True)
        mapTool.setShowSnappableVertices(True)
        mapTool.activated.connect(self.mapToolActivated)
        return mapTool

    def _addMapTool(self, classCode, category, mapTool, action):
        action.triggered.connect(self.validateFeature)
        self.dock.addDrawingTool(classCode, action)
        self.actions[category] = action
        self.mapTools[category] = mapTool

    def addDrawingTool(self, collection, classCode, category, toolName, icon, featureType):
        action = self._newMapToolAction(classCode, category, toolName, icon)
        layer = None
        if (featureType == FeatureType.Line or featureType == FeatureType.Segment):
            layer = self.project.collection(collection).linesBuffer
        elif featureType == FeatureType.Polygon:
            layer = self.project.collection(collection).polygonsBuffer
        else:
            layer = self.project.collection(collection).pointsBuffer
        mapTool = self._newMapTool(toolName, featureType, layer, action)
        self._addMapTool(classCode, category, mapTool, action)

    def addLevelTool(self, collection, classCode, category, toolName, icon):
        action = self._newMapToolAction(classCode, category, toolName, icon)
        mapTool = self._newMapTool(toolName, FeatureType.Point, self.project.collection(collection).pointsBuffer, action)
        mapTool.setAttributeQuery('elevation', QVariant.Double, 0.0, 'Add Level', 'Please enter the elevation in meters (m):', -1000, 1000, 2)
        self._addMapTool(classCode, category, mapTool, action)

    def addSectionTool(self, collection, classCode, category, toolName, icon):
        action = self._newMapToolAction(classCode, category, toolName, icon)
        mapTool = ArkMapToolAddBaseline(self.project.iface, self.project.collection(collection).linesBuffer, FeatureType.Line, self.tr('Add section'))
        mapTool.setAttributeQuery('id', QVariant.String, '', 'Section ID', 'Please enter the Section ID (e.g. S45):')
        mapTool.setPointQuery('elevation', QVariant.Double, 0.0, 'Add Level', 'Please enter the pin or string height in meters (m):', -100, 100, 2)
        self._addMapTool(classCode, category, mapTool, action)

    def mapToolActivated(self):
        for mapTool in self.mapTools.values():
            if mapTool.action().isChecked():
                if not mapTool.layer().isEditable():
                    mapTool.layer().startEditing()
                self.setMapToolAttributes(mapTool)

    def updateMapToolAttributes(self):
        for mapTool in self.mapTools.values():
            if mapTool.action().isChecked():
                self.setMapToolAttributes(mapTool)

    def setMapToolAttributes(self, mapTool):
        if mapTool is None:
            return
        toolData = mapTool.action().data()
        self._featureData.setClassCode(toolData['class'])
        self._featureData.setCategory(toolData['category'])
        attrs = self.featureAttributes(self.metadata(), self._featureData, mapTool.layer())
        mapTool.setDefaultAttributes(attrs)

    def featureAttributes(self, md, fd, layer):
        if (layer is None or not layer.isValid()):
            return
        defaults = {}
        defaults[layer.fieldNameIndex(self.project.fieldName('site'))] = md.siteCode(True)
        defaults[layer.fieldNameIndex(self.project.fieldName('class'))] = fd.classCode(True)
        defaults[layer.fieldNameIndex(self.project.fieldName('id'))] = fd.featureId(True)
        defaults[layer.fieldNameIndex(self.project.fieldName('name'))] = fd.name(True)
        defaults[layer.fieldNameIndex(self.project.fieldName('source_cd'))] = md.sourceCode(True)
        if md.sourceCode() != 'svy':
            defaults[layer.fieldNameIndex(self.project.fieldName('source_cl'))] = md.sourceClass(True)
            defaults[layer.fieldNameIndex(self.project.fieldName('source_id'))] = md.sourceId(True)
        defaults[layer.fieldNameIndex(self.project.fieldName('file'))] = md.sourceFile(True)
        defaults[layer.fieldNameIndex(self.project.fieldName('category'))] = fd.category(True)
        defaults[layer.fieldNameIndex(self.project.fieldName('comment'))] = md.comment(True)
        defaults[layer.fieldNameIndex(self.project.fieldName('created_by'))] = md.createdBy(True)
        return defaults

    def validateFeature(self):
        self._featureData.validate()
        if self._featureData.classCode() == 'cxt':
            self.dock.setContextNumber(self._featureData.featureId())
            self.dock.setFeatureId(0)
        else:
            self.dock.setContextNumber(0)
            self.dock.setFeatureId(self._featureData.featureId())
        self.dock.setFeatureName(self._featureData.name())
        if self.metadata().sourceClass() == self._featureData.classCode() and self.metadata().sourceId() <= 0:
            self.metadata().setSourceId(self._featureData.featureId())
        self.metadata().validate()

    def _autoSchematicBufferSelected(self, sourceId):
        self.actions['sch'].trigger()
        self._autoSchematic(sourceId, self._featureData, self.metadata(), self.project.plan.linesBuffer, self.project.plan.polygonsBuffer)

    def _autoSchematicLayerSelected(self, sourceId):
        self.actions['sch'].trigger()
        self._autoSchematic(sourceId, self._featureData, self.metadata(), self.project.plan.linesLayer, self.project.plan.polygonsBuffer)

    def _autoSchematic(self, sourceId, fd, md, inLayer, outLayer):
        definitiveFeatures = []
        if inLayer.selectedFeatureCount() > 0:
            definitiveFeatures = inLayer.selectedFeatures()
        else:
            featureIter = inLayer.getFeatures()
            for feature in featureIter:
                if feature.attribute(self.project.fieldName('id')) == sourceId and feature.attribute(self.project.fieldName('category')) in self._definitiveCategories:
                    definitiveFeatures.append(feature)
        schematicFeatures = processing.polygonizeFeatures(definitiveFeatures, outLayer.pendingFields())
        if len(schematicFeatures) <= 0:
            return
        attrs = self.featureAttributes(md, fd, outLayer)
        outLayer.beginEditCommand("Add Auto Schematic")
        for feature in schematicFeatures:
            for attr in attrs.keys():
                feature.setAttribute(attr, attrs[attr])
            outLayer.addFeature(feature)
        outLayer.endEditCommand()
        self.project.mapCanvas().refresh()

    # SchematicDock methods

    def _resetSchematic(self):
        self._clearSchematicFilters()
        self.schematicDock.setContext(0, SearchStatus.Unknown, SearchStatus.Unknown)

    def _clearSchematicFilters(self):
        self._clearSchematicContextIncludeFilter()
        self._clearSchematicContextHighlightFilter()
        self._clearSchematicSourceFilters()

    def _clearSchematicContextIncludeFilter(self):
        self.project.filterModule.removeFilter(self._schematicContextIncludeFilter)
        self._schematicContextIncludeFilter = -1

    def _clearSchematicContextHighlightFilter(self):
        self.project.filterModule.removeFilter(self._schematicContextHighlightFilter)
        self._schematicContextHighlightFilter = -1

    def _clearSchematicSourceFilters(self):
        self.project.filterModule.removeFilter(self._schematicSourceIncludeFilter)
        self._schematicSourceIncludeFilter = -1
        self.project.filterModule.removeFilter(self._schematicSourceHighlightFilter)
        self._schematicSourceHighlightFilter = -1

    def _findContext(self):
        self._clearSchematicFilters()

        filterModule = self.project.filterModule
        siteCode = self.schematicDock.metadata().siteCode()
        if siteCode == '':
            siteCode = self.project.siteCode()
        if filterModule.hasFilterType(FilterType.IncludeFilter) or filterModule.hasFilterType(FilterType.IncludeFilter):
            self._schematicContextFilter = filterModule.addFilter(FilterType.IncludeFilter, siteCode, 'cxt', str(self.schematicDock.context()), FilterAction.LockFilter)
        self._schematicContextHighlightFilter = filterModule.addFilter(FilterType.HighlightFilter, siteCode, 'cxt', str(self.schematicDock.context()), FilterAction.LockFilter)

        classExpr = '"' + self.project.fieldName('class') + '" = \'' + 'cxt' + '\''
        idExpr = '"' + self.project.fieldName('id') + '" = \'' + str(self.schematicDock.context()) + '\''
        schmExpr = '"' + self.project.fieldName('category') + '" = \'sch\''

        request = QgsFeatureRequest()
        request.setFilterExpression(classExpr + ' and ' + idExpr)
        haveFeature = SearchStatus.Found
        try:
            feature = self.project.plan.linesLayer.getFeatures(request).next()
            self._copyFeatureMetadata(feature)
        except StopIteration:
            haveFeature = SearchStatus.NotFound

        request.setFilterExpression(classExpr + ' and ' + idExpr + ' and ' + schmExpr)
        haveSchematic = SearchStatus.Found
        try:
            self.project.plan.polygonsLayer.getFeatures(request).next()
        except StopIteration:
            haveSchematic = SearchStatus.NotFound

        self.schematicDock.setContext(self.schematicDock.context(), haveFeature, haveSchematic)
        self._featureIdChanged(self.schematicDock.context())

    def _findSource(self):
        self._clearSchematicSourceFilters()

        filterModule = self.project.filterModule
        siteCode = self.schematicDock.metadata().siteCode()
        if siteCode == '':
            siteCode = self.project.siteCode()
        if filterModule.hasFilterType(FilterType.IncludeFilter) or filterModule.hasFilterType(FilterType.IncludeFilter):
            self._schematicSourceIncludeFilter = filterModule.addFilter(FilterType.IncludeFilter, siteCode, 'cxt', str(self.schematicDock.sourceContext()), FilterAction.LockFilter)
        self._clearSchematicContextHighlightFilter()
        self._schematicSourceHighlightFilter = filterModule.addFilter(FilterType.HighlightFilter, siteCode, 'cxt', str(self.schematicDock.sourceContext()), FilterAction.LockFilter)

        classExpr = '"' + self.project.fieldName('class') + '" = \'' + 'cxt' + '\''
        idExpr = '"' + self.project.fieldName('id') + '" = \'' + str(self.schematicDock.sourceContext()) + '\''
        schmExpr = '"' + self.project.fieldName('category') + '" = \'sch\''

        request = QgsFeatureRequest()
        request.setFilterExpression(classExpr + ' and ' + idExpr)
        haveFeature = SearchStatus.Found
        try:
            self.project.plan.linesLayer.getFeatures(request).next()
        except StopIteration:
            haveFeature = SearchStatus.NotFound

        request.setFilterExpression(classExpr + ' and ' + idExpr + ' and ' + schmExpr)
        haveSchematic = SearchStatus.Found
        try:
            feature = self.project.plan.polygonsLayer.getFeatures(request).next()
            self._copyFeatureMetadata(feature)
        except StopIteration:
            haveSchematic = SearchStatus.NotFound

        self.schematicDock.setSourceContext(self.schematicDock.sourceContext(), haveFeature, haveSchematic)

    def _attribute(self, feature, fieldName):
        val = feature.attribute(self.project.fieldName(fieldName))
        if val == NULL:
            return None
        else:
            return val

    def _copyFeatureMetadata(self, feature):
        self.schematicDock.metadata().setSiteCode(self._attribute(feature, 'site'))
        #TODO FIXME WTF???
        self.schematicDock.metadataWidget._setSiteCode(self.schematicDock.metadata().siteCode())
        self.schematicDock.metadata().setComment(self._attribute(feature, 'comment'))
        self.schematicDock.metadata().setSourceCode('cln')
        self.schematicDock.metadata().setSourceClass('cxt')
        self.schematicDock.metadata().setSourceId(self.schematicDock.sourceContext())
        self.schematicDock.metadata().setSourceFile('')

    def _classClause(self, classCode):
        return _doublequote(self.project.fieldName('class')) + ' = ' + _quote(classCode)

    def _idClause(self, num):
        return _doublequote(self.project.fieldName('id')) + ' = ' + str(num)

    def _categoryClause(self, category):
        return _doublequote(self.project.fieldName('category')) + ' = ' + _quote(category)

    def _copySource(self):
        request = QgsFeatureRequest()
        request.setFilterExpression(self._classClause('cxt') + ' and ' + self._idClause(self.schematicDock.sourceContext()) + ' and ' + self._categoryClause('sch'))
        fi = self.project.plan.polygonsLayer.getFeatures(request)
        for feature in fi:
            md = self.schematicDock.metadata()
            feature.setAttribute(self.project.fieldName('site'), md.siteCode(True))
            feature.setAttribute(self.project.fieldName('class'), 'cxt')
            feature.setAttribute(self.project.fieldName('id'), self.schematicDock.context(True))
            feature.setAttribute(self.project.fieldName('name'), None)
            feature.setAttribute(self.project.fieldName('category'), 'sch')
            feature.setAttribute(self.project.fieldName('source_cd'), md.sourceCode(True))
            feature.setAttribute(self.project.fieldName('source_cl'), md.sourceClass(True))
            feature.setAttribute(self.project.fieldName('source_id'), md.sourceId(True))
            feature.setAttribute(self.project.fieldName('file'), md.sourceFile(True))
            feature.setAttribute(self.project.fieldName('comment'), md.comment(True))
            feature.setAttribute(self.project.fieldName('created_by'), md.createdBy(True))
            feature.setAttribute(self.project.fieldName('created_on'), None)
            self.project.plan.polygonsBuffer.addFeature(feature)

    def _cloneSource(self):
        self._copySource()
        self.mergeBuffers()
