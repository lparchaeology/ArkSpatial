# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARKspatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L - P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        copyright            : 2017 by L - P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2017 by John Layt
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

import bisect
import copy
import os

from PyQt4.QtCore import QDir, QFile, QFileInfo, QObject, Qt
from PyQt4.QtGui import QFileDialog, QInputDialog

from qgis.core import NULL, QgsFeatureRequest, QgsGeometry

from ArkSpatial.ark.lib import utils
from ArkSpatial.ark.lib.core import layers
from ArkSpatial.ark.lib.gui import TableDialog

from ArkSpatial.ark.core import Config, Drawing, Feature, FeatureError, Item, Source, Settings
from ArkSpatial.ark.core.enum import DrawingAction, FilterAction, MapAction, SearchStatus
from ArkSpatial.ark.georef import GeorefDialog
from ArkSpatial.ark.gui import FeatureErrorDialog, PlanDock, SelectDrawingDialog


class PlanModule(QObject):

    def __init__(self, plugin):
        super(PlanModule, self).__init__(plugin)

        # Project settings
        self.plugin = plugin  # Plugin()
        self.dock = None  # PlanDock()
        self.initialised = False
        self.metadata = None  # Metadata()

        # Internal variables
        self._editSchematic = False
        self._mapAction = MapAction.MoveMap
        self._filterAction = FilterAction.ExclusiveHighlightFilter
        self._drawingAction = DrawingAction.NoDrawingAction
        self._itemLogPath = ''

    # Create the gui when the plugin is first created
    def initGui(self):
        self.dock = PlanDock(self.plugin.iface.mainWindow())
        action = self.plugin.addDockAction(
            ':/plugins/ark/plan/drawPlans.png', self.tr(u'Drawing Tools'), callback=self.run, checkable=True)
        self.dock.initGui(self.plugin.iface, Qt.RightDockWidgetArea, action)

        self.dock.loadAnyFileSelected.connect(self._loadAnyPlan)
        self.dock.loadRawFileSelected.connect(self._loadRawPlan)
        self.dock.loadGeoFileSelected.connect(self._loadGeoPlan)

        self.dock.resetSelected.connect(self.resetBuffers)
        self.dock.mergeSelected.connect(self.mergeBuffers)

        self.dock.loadArkData.connect(self._loadArkData)
        self.dock.mapActionChanged.connect(self._mapActionChanged)
        self.dock.filterActionChanged.connect(self._filterActionChanged)
        self.dock.drawingActionChanged.connect(self._drawingActionChanged)
        self.dock.openContextData.connect(self._openContextData)
        self.dock.openSourceContextData.connect(self._openSourceContextData)
        self.dock.findContextSelected.connect(self._findContext)
        self.dock.firstContextSelected.connect(self._firstContext)
        self.dock.lastContextSelected.connect(self._lastContext)
        self.dock.prevContextSelected.connect(self._prevContext)
        self.dock.nextContextSelected.connect(self._nextContext)
        self.dock.prevMissingSelected.connect(self._prevMissing)
        self.dock.nextMissingSelected.connect(self._nextMissing)
        self.dock.schematicReportSelected.connect(self._showSchematicReport)
        self.dock.editContextSelected.connect(self._editSchematicContext)
        self.dock.deleteSectionSchematicSelected.connect(self._deleteSectionSchematic)
        self.dock.findSourceSelected.connect(self._findSource)
        self.dock.copySourceSelected.connect(self._editSourceSchematic)
        self.dock.cloneSourceSelected.connect(self._cloneSourceSchematic)
        self.dock.editSourceSelected.connect(self._editSource)
        self.dock.contextChanged.connect(self._clearSchematicFilters)
        self.dock.resetSchematicSelected.connect(self._resetSchematic)

        self.plugin.filterModule.filterSetCleared.connect(self._clearSchematic)

    # Load the project settings when project is loaded
    def loadProject(self):
        utils.debug('Plan loadProject')
        # Assume layers are loaded and filters cleared
        self.dock.loadProject(self.plugin)

        if self.plugin.plan.settings.log:
            self._itemLogPath = os.path.join(self.plugin.plan.projectPath,
                                             self.plugin.plan.settings.collectionPath,
                                             'log/itemLog.csv')
            if not QFile.exists(self._itemLogPath):
                fd = open(self._itemLogPath, 'a')
                fd.write('timestamp,action,siteCode,classCode,itemId\n')
                fd.close()

        # TODO Think of a better way...
        # self.metadata = Metadata(self.dock.widget.sourceWidget)
        # self.metadata.metadataChanged.connect(self.updateMapToolAttributes)

        self.plugin.data.dataLoaded.connect(self.dock.activateArkData)

        utils.debug('Plan set initialised')
        self.initialised = True

    # Save the project
    def writeProject(self):
        # We don't want to save the schematic serach or filters
        self._clearSchematic()

    # Close the project
    def closeProject(self):
        self._clearSchematicFilters()
        # TODO Unload the drawing tools!
        self.dock.closeProject()
        # self.metadata.metadataChanged.disconnect(self.updateMapToolAttributes)
        # self.plugin.data.dataLoaded.disconnect(self.dock.activateArkData)
        self.initialised = False

    # Unload the module when plugin is unloaded
    def unloadGui(self):
        # Unload the dock
        self.dock.unloadGui()
        del self.dock
        # Reset the initialisation
        self.initialised = False

    def run(self, checked):
        if checked and self.initialised:
            self.plugin.filterModule.showDock()
        else:
            self.dock.menuAction().setChecked(False)

    # Plan Tools

    def _setDrawing(self, pmd):
        self.metadata.setSiteCode(pmd.siteCode)
        self.metadata.setClassCode(pmd.sourceClass)
        if pmd.sourceId > 0:
            self.metadata.setItemId(pmd.sourceId)
            self.metadata.setSourceId(pmd.sourceId)
        self.metadata.setSourceCode('drawing')
        self.metadata.setSourceClass(pmd.sourceClass)
        self.metadata.setSourceFile(pmd.filename)
        self.metadata.setEditor(Settings.userFullName())

    def _loadAnyPlan(self):
        filePaths = QFileDialog.getOpenFileNames(
            self.dock, caption='Georeference Any File', filter='Images (*.png *.xpm *.jpg)')
        for filePath in filePaths:
            self.georeferencePlan(QFileInfo(filePath), 'free')

    def _loadRawPlan(self):
        dialog = SelectDrawingDialog('context', Settings.siteCode())
        if (dialog.exec_()):
            for filePath in dialog.selectedFiles():
                self.georeferencePlan(QFileInfo(filePath))

    def _loadGeoPlan(self):
        dialog = SelectDrawingDialog('context', Settings.siteCode(), True)
        if (dialog.exec_()):
            for filePath in dialog.selectedFiles():
                geoFile = QFileInfo(filePath)
                self._setDrawing(Drawing(geoFile))
                self.plugin.loadGeoLayer(geoFile)

    def loadDrawing(self, item, zoomToDrawing=True):
        if not Config.classCodes[item.classCode()]['drawing']:
            return
        drawingDir = Settings.georefDrawingDir(item.classCode())
        drawingDir.setFilter(QDir.Files | QDir.NoDotAndDotDot)
        name = item.name()
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
            self._setDrawing(Drawing(drawing))
            self.plugin.loadGeoLayer(drawing, zoomToDrawing)

    def loadSourceDrawings(self, item, clearDrawings=False):
        if item.isInvalid():
            return
        sourceKeys = set()
        sourceKeys.add(item)
        itemRequest = item.featureRequest()
        for feature in self.plugin.plan.layer('polygons').getFeatures(itemRequest):
            source = Source(feature)
            if source.item().isValid():
                sourceKeys.add(source.item())
        for feature in self.plugin.plan.layer('lines').getFeatures(itemRequest):
            source = Source(feature)
            if source.item.isValid():
                sourceKeys.add(source.item())
        for feature in self.plugin.plan.layer('points').getFeatures(itemRequest):
            source = Source(feature)
            if source.item().isValid():
                sourceKeys.add(source.item())
        if clearDrawings and len(sourceKeys) > 0:
            self.plugin.clearDrawings()
        for sourceKey in sorted(sourceKeys):
            self.loadDrawing(sourceKey)

    def _featureNameChanged(self, featureName):
        self.metadata.setName(featureName)
        self.updateMapToolAttributes()

    # Georeference Tools

    def georeferencePlan(self, sourceFile, mode='name'):
        drawings = Config.drawings
        for drawing in drawings:
            drawings[drawing]['raw'] = Settings.rawDrawingDir(drawing)
            drawings[drawing]['geo'] = Settings.georefDrawingDir(drawing)
            drawings[drawing]['suffix'] = '_r'
            drawings[drawing]['crs'] = self.plugin.projectCrs().authid()
            drawings[drawing]['grid'] = self.plugin.grid.layer('points')
            drawings[drawing]['local_x'] = 'local_x'
            drawings[drawing]['local_y'] = 'local_y'
        georefDialog = GeorefDialog(drawings)
        if georefDialog.loadImage(sourceFile) and georefDialog.exec_():
            geoFile = georefDialog.geoFile()
            md = georefDialog.metadata()
            md.filename = geoFile.fileName()
            self._setDrawing(md)
            self.plugin.loadGeoLayer(geoFile)

    # Layer Methods

    def mergeBuffers(self):
        self._mergeBuffers(self.plugin.plan)
        self._mergeBuffers(self.plugin.section)

    def _mergeBuffers(self, collection):
        # Check the layers are writable
        name = collection.settings.collectionGroupName
        if not collection.isWritable():
            self.plugin.showCriticalMessage(
                name + ' layers are not writable! Please correct the permissions and log out.', 0)
            return

        # Check the buffers contain valid data
        errors = self._preMergeBufferCheck(collection.buffer('points'))
        errors.extend(self._preMergeBufferCheck(collection.buffer('lines')))
        errors.extend(self._preMergeBufferCheck(collection.buffer('polygons')))
        if len(errors) > 0:
            dialog = FeatureErrorDialog()
            dialog.loadErrors(errors)
            dialog.exec_()
            if not dialog.ignoreErrors():
                return

        # Update the audit attributes
        timestamp = utils.timestamp()
        user = self.metadata.editor()
        self._preMergeBufferUpdate(collection.buffer('points'), timestamp, user)
        self._preMergeBufferUpdate(collection.buffer('lines'), timestamp, user)
        self._preMergeBufferUpdate(collection.buffer('polygons'), timestamp, user)

        # Finally actually merge the data
        if collection.mergeBuffers('Merge data', Settings.logUpdates(), timestamp):
            self.plugin.showInfoMessage(name + ' data successfully merged.')
            self._logItemAction(self.metadata.feature().item(), 'Merge Buffers', timestamp)
            if self._editSchematic:
                self._editSchematic = False
                self.dock.activateSchematicCheck()
                self._findContext()
        else:
            self.plugin.showCriticalMessage(
                name + ' data merge failed! Some data has not been saved, please check your data.', 5)

    def _preMergeBufferCheck(self, layer):
        errors = []
        row = 0
        for feature in layer.getFeatures():
            # Set up the error template
            error = FeatureError()
            error.layer = layer.name()
            error.row = row
            row = row + 1
            error.fid = feature.id()
            error.feature.fromFeature(feature)
            # Feature must be valid
            if not feature.isValid():
                error.field = 'feature'
                error.message = 'Invalid Feature'
                errors.append(copy.deepcopy(error))
            # Geometry must be valid
            error.field = 'geometry'
            if feature.geometry() is None:
                error.message = 'No Geometry'
                errors.append(copy.deepcopy(error))
            elif feature.geometry().isEmpty():
                error.message = 'Empty Geometry'
                errors.append(copy.deepcopy(error))
            else:
                error.message = 'Invalid Geometry'
                geomErrs = feature.geometry().validateGeometry()
                # Ignore the last error, it is just a total
                for err in geomErrs[:-1]:
                    error.message = err.what()
                    errors.append(copy.deepcopy(error))
            # Key attributes that must always be populated
            if self._isEmpty(feature.attribute('site')):
                error.field = 'site'
                error.message = 'Site Code is required'
                errors.append(copy.deepcopy(error))
            if self._isEmpty(feature.attribute('class')):
                error.field = 'class'
                error.message = 'Class Code is required'
                errors.append(copy.deepcopy(error))
            if self._isEmpty(feature.attribute('id')):
                error.field = 'id'
                error.message = 'ID is required'
                errors.append(copy.deepcopy(error))
            if self._isEmpty(feature.attribute('category')):
                error.field = 'category'
                error.message = 'Category is required'
                errors.append(copy.deepcopy(error))
            if self._isEmpty(feature.attribute('source_cd')):
                error.field = 'source_cd'
                error.message = 'Source Code is required'
                error.ignore = True
                # errors.append(copy.deepcopy(error))
            # Source attributes required depend on the source type
            if feature.attribute('source_cd') == 'creator' or feature.attribute('source_cd') == 'other':
                if self._isEmpty(feature.attribute('comment')):
                    error.field = 'source_cd'
                    error.message = 'Comment is required for Source type of Creator or Other'
                    error.ignore = True
                    # errors.append(copy.deepcopy(error))
            elif feature.attribute('source_cd') == 'survey':
                if self._isEmpty(feature.attribute('file')):
                    error.field = 'source_cd'
                    error.message = 'Filename is required for Source type of Survey'
                    error.ignore = True
                    # errors.append(copy.deepcopy(error))
            else:  # 'drw', 'unc', 'skt', 'cln', 'mod', 'inf'
                if ((feature.attribute('source_cd') == 'drawing' or feature.attribute('source_cd') == 'unchecked')
                        and self._isEmpty(feature.attribute('file'))):
                    error.field = 'source_cd'
                    error.message = 'Filename is required for Source type of Drawing'
                    error.ignore = True
                    # errors.append(copy.deepcopy(error))
                if (self._isEmpty(feature.attribute('source_cl')) or self._isEmpty(feature.attribute('source_id'))):
                    error.field = 'source_cd'
                    error.message = 'Source Class and ID is required'
                    error.ignore = True
                    # errors.append(copy.deepcopy(error))
        return errors

    def _isEmpty(self, val):
        if val is None or val == NULL:
            return True
        if isinstance(val, str) and (val == '' or val.strip() == ''):
            return True
        return False

    def _preMergeBufferUpdate(self, layer, timestamp, user):
        createdIdx = layer.fieldNameIndex('created')
        creatorIdx = layer.fieldNameIndex('creator')
        modifiedIdx = layer.fieldNameIndex('modified')
        modifierIdx = layer.fieldNameIndex('modifier')
        for feature in layer.getFeatures():
            if self._isEmpty(feature.attribute('created')):
                layer.changeAttributeValue(feature.id(), createdIdx, timestamp)
                layer.changeAttributeValue(feature.id(), creatorIdx, user)
            else:
                layer.changeAttributeValue(feature.id(), modifiedIdx, timestamp)
                layer.changeAttributeValue(feature.id(), modifierIdx, user)

    def resetBuffers(self):
        self.plugin.plan.resetBuffers('Clear Buffers')
        if self._editSchematic:
            self._editSchematic = False
            self.dock.activateSchematicCheck()

    # Drawing tools

    def _confirmDelete(self, itemId, title='Confirm Delete Item', label=None):
        if not label:
            label = 'This action ***DELETES*** item ' + \
                str(itemId) + ' from the saved data.\n\nPlease enter the item ID to confirm.'
        confirm, ok = QInputDialog.getText(None, title, label, text='')
        return ok and confirm == str(itemId)

    def _logItemAction(self, item, action, timestamp=None):
        if self.plugin.plan.settings.log:
            if not timestamp:
                timestamp = utils.timestamp()
            fd = open(self._itemLogPath, 'a')
            fd.write(utils.doublequote(timestamp) + ',' + utils.doublequote(action) + ',' + item.toCsv() + '\n')
            fd.close()

    def editInBuffers(self, item):
        # if self._confirmDelete(item.itemId(), 'Confirm Move Item'):
        request = item.featureRequest()
        timestamp = utils.timestamp()
        action = 'Edit Item'
        if self.plugin.plan.moveFeatureRequestToBuffers(request, action, Settings.logUpdates(), timestamp):
            self._logItemAction(item, action, timestamp)
            self._metadataFromBuffers(item)

    def deleteItem(self, item):
        if self._confirmDelete(item.itemId(), 'Confirm Delete Item'):
            request = item.featureRequest()
            timestamp = utils.timestamp()
            action = 'Delete Item'
            if self.plugin.plan.deleteFeatureRequest(request, action, Settings.logUpdates(), timestamp):
                self._logItemAction(item, action, timestamp)

    def applyItemActions(self,
                         item,
                         mapAction=MapAction.NoMapAction,
                         filterAction=FilterAction.NoFilterAction,
                         drawingAction=DrawingAction.NoDrawingAction):
        if drawingAction != DrawingAction.NoDrawingAction:
            self.loadSourceDrawings(item, drawingAction == DrawingAction.LoadDrawings)

        if filterAction != FilterAction.NoFilterAction:
            self.plugin.filterModule.applyItemAction(item, filterAction)

        if mapAction == MapAction.ZoomMap:
            self._zoomToItem(item)
        elif mapAction == MapAction.PanMap:
            self._panToItem(item)
        elif mapAction == MapAction.MoveMap:
            self._moveToItem(item)
        self.plugin.mapCanvas().refresh()

    def showItem(self, item, loadDrawings=True, zoom=True):
        self.plugin.showMessage('Loading ' + item.itemLabel())
        self.plugin.filterModule.filterItem(item)
        if loadDrawings:
            self.loadSourceDrawings(item, True)
        if zoom:
            self._zoomToItem(item)

    def panToItem(self, item, highlight=False):
        if highlight:
            self.plugin.filterModule.highlightItem(item)
        self._panToItem(item)
        self.plugin.mapCanvas().refresh()

    def zoomToItem(self, item, highlight=False):
        if highlight:
            self.plugin.filterModule.highlightItem(item)
        self._zoomToItem(item)
        self.plugin.mapCanvas().refresh()

    def moveToItem(self, item, highlight=False):
        ret = -1
        if highlight:
            ret = self.plugin.filterModule.highlightItem(item)
        self._moveToItem(item)
        self.plugin.mapCanvas().refresh()
        return ret

    def _moveToItem(self, item):
        self._moveToExtent(self.itemExtent(item))

    def _moveToExtent(self, extent):
        if extent is None or extent.isNull() or extent.isEmpty():
            return
        mapExtent = self.plugin.mapCanvas().extent()
        if (extent.width() > mapExtent.width() or extent.height() > mapExtent.height()
                or extent.width() * extent.height() > mapExtent.width() * mapExtent.height()):
            self._zoomToExtent(extent)
        else:
            self._panToExtent(extent)

    def _panToItem(self, item):
        self._panToExtent(self.itemExtent(item))

    def _panToExtent(self, extent):
        if extent is None or extent.isNull() or extent.isEmpty():
            return
        self.plugin.mapCanvas().setCenter(extent.center())

    def _zoomToItem(self, item):
        self._zoomToExtent(self.itemExtent(item))

    def _zoomToExtent(self, extent):
        if extent is None or extent.isNull() or extent.isEmpty():
            return
        extent.scale(1.05)
        self.plugin.mapCanvas().setExtent(extent)

    def filterItem(self, item):
        self.plugin.filterModule.filterItem(item)
        self.plugin.mapCanvas().refresh()

    def excludeFilterItem(self, item):
        self.plugin.filterModule.excludeItem(item)
        self.plugin.mapCanvas().refresh()

    def highlightItem(self, item):
        self.plugin.filterModule.highlightItem(item)
        self.plugin.mapCanvas().refresh()

    def addHighlightItem(self, item):
        self.plugin.filterModule.addHighlightItem(item)
        self.plugin.mapCanvas().refresh()

    def itemExtent(self, item):
        requestKey = self.plugin.data.nodesItem(item)
        request = requestKey.featureRequest()
        points = self._requestAsLayer(request, self.plugin.plan.layer('points'), 'points')
        lines = self._requestAsLayer(request, self.plugin.plan.layer('lines'), 'lines')
        polygons = self._requestAsLayer(request, self.plugin.plan.layer('polygons'), 'polygons')
        extent = None
        extent = self._combineExtentWith(extent, polygons)
        extent = self._combineExtentWith(extent, lines)
        extent = self._combineExtentWith(extent, points)
        return extent

    def _requestAsLayer(self, request, fromLayer, toName):
        toLayer = layers.cloneAsMemoryLayer(fromLayer, toName)
        layers.copyFeatureRequest(request, fromLayer, toLayer)
        toLayer.updateExtents()
        return toLayer

    def _combineExtentWith(self, extent, layer):
        if (layer is not None and layer.isValid() and layer.featureCount() > 0):
            layerExtent = layer.extent()
            if layerExtent.isNull() or layerExtent.isEmpty():
                return extent
            if extent is None:
                extent = layerExtent
            else:
                extent.combineExtentWith(layerExtent)
        return extent

    def _sectionItemList(self, siteCode):
        # TODO in 2.14 use addOrderBy()
        request = self._classItemsRequest(siteCode, 'sec')
        features = layers.getAllFeaturesRequest(request, self.plugin.plan.layer('lines'))
        lst = []
        for feature in features:
            lst.append(Feature(feature))
        lst.sort()
        return lst

    def _sectionLineGeometry(self, item):
        if item and item.isValid():
            request = self._categoryRequest(item, 'sln')
            features = layers.getAllFeaturesRequest(request, self.plugin.plan.layer('lines'))
            for feature in features:
                return QgsGeometry(feature.geometry())
        return QgsGeometry()

    def _sectionChanged(self, item):
        try:
            self.mapTools['scs'].setSectionGeometry(self._sectionLineGeometry(item))
        except Exception:
            pass

    def _metadataFromBuffers(self, item):
        feature = self._getFeature(self.plugin.plan.buffer('polygons'), item, 'sch')
        if feature:
            self.metadata.fromFeature(feature)
            return
        feature = self._getFeature(self.plugin.plan.buffer('polygons'), item, 'scs')
        if feature:
            self.metadata.fromFeature(feature)
            return
        feature = self._getFeature(self.plugin.plan.buffer('polygons'), item)
        if feature:
            self.metadata.fromFeature(feature)
            return
        feature = self._getFeature(self.plugin.plan.buffer('lines'), item)
        if feature:
            self.metadata.fromFeature(feature)
            return
        feature = self._getFeature(self.plugin.plan.buffer('points'), item)
        if feature:
            self.metadata.fromFeature(feature)

    def _getFeature(self, layer, item, category=''):
        req = None
        if category:
            req = self._categoryRequest(item, 'sch')
        else:
            req = self._itemRequest(item)
        try:
            return layer.getFeatures(req).next()
        except StopIteration:
            return None
        return None

    # Feature Request Methods

    def _eqClause(self, field, value):
        return utils.eqClause(field, value)

    def _neClause(self, field, value):
        return utils.neClause(field, value)

    def _categoryClause(self, category):
        return self._eqClause('category', category)

    def _notCategoryClause(self, category):
        return self._neClause('category', category)

    def _featureRequest(self, expr):
        request = QgsFeatureRequest()
        request.setFilterExpression(expr)
        return request

    def _itemRequest(self, item):
        return self._featureRequest(item.filterClause())

    def _categoryRequest(self, item, category):
        return self._featureRequest(item.filterClause() + ' and ' + self._categoryClause(category))

    def _notCategoryRequest(self, item, category):
        return self._featureRequest(item.filterClause() + ' and ' + self._notCategoryClause(category))

    def _classItemsRequest(self, siteCode, classCode):
        return self._featureRequest(self._eqClause('site', siteCode) + ' and ' + self._eqClause('class', classCode))

    # SchematicDock methods

    def _loadArkData(self):
        self.plugin.data.loadData()

    def _mapActionChanged(self, mapAction):
        self._mapAction = mapAction

    def _filterActionChanged(self, filterAction):
        self._filterAction = filterAction

    def _drawingActionChanged(self, drawingAction):
        self._drawingAction = drawingAction

    def _openContextData(self):
        self.openItemInArk(self.dock.contextItem())

    def _openSourceContextData(self):
        self.openItemInArk(self.dock.sourceItem())

    def openItemInArk(self, item):
        self.plugin.data.openItem(item)

    def _resetSchematic(self):
        self._clearSchematic()
        self.dock.activateSchematicCheck()

    def _clearSchematic(self):
        self._clearSchematicFilters()
        self.dock.resetContext()

    def _mergeSchematic(self):
        self.mergeBuffers()
        self._findContext()

    def _clearSchematicFilters(self):
        self.plugin.filterModule.clearSchematicFilter()

    def _firstContext(self):
        self._findContext(self.plugin.data.firstItem('context'))

    def _lastContext(self):
        self._findContext(self.plugin.data.lastItem('context'))

    def _prevContext(self):
        self._findContext(self.plugin.data.prevItem(self.dock.contextItem()))

    def _nextContext(self):
        self._findContext(self.plugin.data.nextItem(self.dock.contextItem()))

    def _prevMissing(self):
        context = self.dock.contextItem()
        idx = 0
        if context.isValid():
            idx = bisect.bisect_left(self.plugin.data.items['context'], context)
        schematics = self._getAllSchematicItems()
        for prv in reversed(range(idx)):
            item = self.plugin.data.items['context'][prv]
            if item not in schematics:
                self._findContext(item)
                return

    def _nextMissing(self):
        context = self.dock.contextItem()
        idx = 0
        if context.isValid():
            idx = bisect.bisect(self.plugin.data.items['context'], context)
        schematics = self._getAllSchematicItems()
        for item in self.plugin.data.items['context'][idx:]:
            if item not in schematics:
                self._findContext(item)
                return

    def _getAllSchematicItems(self):
        features = self._getAllSchematicFeatures()
        items = set()
        for feature in features:
            item = Item(feature)
            items.add(item)
        return sorted(items)

    def _getAllSchematicFeatures(self):
        req = self._featureRequest(self._categoryClause('sch'))
        return layers.getAllFeaturesRequest(req, self.plugin.plan.layer('polygons'))

    def _editSchematicContext(self):
        self._editSchematic = True
        self.editInBuffers(self.dock.contextItem())
        self.dock.widget.setCurrentIndex(0)

    def _deleteSectionSchematic(self):
        item = self.dock.contextItem()
        label = 'This action ***DELETES*** ***ALL*** Section Schematics from item ' + \
            str(item.itemId()) + '\n\nPlease enter the item ID to confirm.'
        if self._confirmDelete(item.itemId(), 'Confirm Delete Section Schematic', label):
            request = self._categoryRequest(item, 'scs')
            timestamp = utils.timestamp()
            action = 'Delete Section Schematic'
            if self.plugin.plan.deleteFeatureRequest(request, action, Settings.logUpdates(), timestamp):
                self._logItemAction(item, action, timestamp)
            self._findContext(item)

    def _arkStatus(self, item):
        haveArk = SearchStatus.NotFound
        contextType = 'None'
        contextDescription = ''
        try:
            if item in self.plugin.data.items['context']:
                haveArk = SearchStatus.Found
                vals = self.plugin.data.getItemFields(item, ['conf_field_cxttype', 'conf_field_short_desc'])
                if (u'conf_field_cxttype' in vals and vals[u'conf_field_cxttype']):
                    contextType = str(vals[u'conf_field_cxttype'])
                if u'conf_field_short_desc' in vals:
                    contextDescription = str(vals[u'conf_field_short_desc'][0][u'current'])
            else:
                contextDescription = 'Context not in ARK'
        except Exception:
            haveArk = SearchStatus.Unknown
        return haveArk, contextType, contextDescription

    def _featureStatus(self, item, copyMetadata=False):
        itemRequest = item.featureRequest()
        try:
            feature = self.plugin.plan.layer('lines').getFeatures(itemRequest).next()
            if copyMetadata:
                self._copyFeatureMetadata(feature)
        except StopIteration:
            return SearchStatus.NotFound
        return SearchStatus.Found

    def _schematicStatus(self, item):
        schRequest = self._categoryRequest(item, 'sch')
        try:
            self.plugin.plan.layer('polygons').getFeatures(schRequest).next()
        except StopIteration:
            return SearchStatus.NotFound
        return SearchStatus.Found

    def _findContext(self, context=Item()):
        self._clearSchematicFilters()

        if not context.isValid():
            context = self.dock.contextItem()

        self.plugin.filterModule.applySchematicFilter(context, self._filterAction)
        self.applyItemActions(context, self._mapAction, FilterAction.NoFilterAction, self._drawingAction)

        haveArk, contextType, contextDescription = self._arkStatus(context)
        haveFeature = self._featureStatus(context, True)

        if haveFeature == SearchStatus.NotFound:
            polyRequest = self._notCategoryRequest(context, 'sch')
            haveFeature = SearchStatus.Found
            try:
                self.plugin.plan.layer('polygons').getFeatures(polyRequest).next()
            except StopIteration:
                haveFeature = SearchStatus.NotFound

        haveSchematic = self._schematicStatus(context)

        scsRequest = self._categoryRequest(context, 'scs')
        haveSectionSchematic = SearchStatus.Found
        try:
            self.plugin.plan.layer('polygons').getFeatures(scsRequest).next()
        except StopIteration:
            haveSectionSchematic = SearchStatus.NotFound

        self.dock.setContext(context, haveArk, contextType, contextDescription,
                             haveFeature, haveSchematic, haveSectionSchematic)
        self.metadata.setItemId(context.itemId())

    def _editSource(self):
        self.editInBuffers(self.dock.sourceItem())
        self.dock.widget.setCurrentIndex(0)

    def _findSource(self, source=Item()):
        if not source.isValid():
            source = self.dock.sourceItem()

        self.plugin.filterModule.applySchematicFilter(source, self._filterAction)
        self.applyItemActions(source, self._mapAction, FilterAction.NoFilterAction, self._drawingAction)

        haveArk, contextType, contextDescription = self._arkStatus(source)
        haveFeature = self._featureStatus(source)
        haveSchematic = self._schematicStatus(source)

        self.dock.setSourceContext(source, haveArk, contextType, contextDescription, haveFeature, haveSchematic)

    def _attribute(self, feature, attribute):
        val = feature.attribute(attribute)
        if val == NULL:
            return None
        else:
            return val

    def _copyFeatureMetadata(self, feature):
        self.metadata.setSiteCode(self._attribute(feature, 'site'))
        self.metadata.setComment(self._attribute(feature, 'comment'))
        self.metadata.setClassCode('context')
        self.metadata.setItemId(self.dock.context())
        self.metadata.setSourceCode('cloned')
        self.metadata.setSourceClass('context')
        self.metadata.setSourceId(self.dock.sourceContext())
        self.metadata.setSourceFile('')

    def _copySourceSchematic(self):
        self.metadata.validate()
        request = self._categoryRequest(self.dock.sourceItem(), 'sch')
        features = layers.getAllFeaturesRequest(request, self.plugin.plan.layer('polygons'))
        for feature in features:
            feature.setAttribute('site', self.metadata.siteCode())
            feature.setAttribute('class', 'context')
            feature.setAttribute('id', self.dock.context())
            feature.setAttribute('label', None)
            feature.setAttribute('category', 'sch')
            feature.setAttribute('source_cd', self.metadata.sourceCode())
            feature.setAttribute('source_cl', self.metadata.sourceClass())
            feature.setAttribute('source_id', self.metadata.sourceId())
            feature.setAttribute('file', self.metadata.sourceFile())
            feature.setAttribute('comment', self.metadata.comment())
            feature.setAttribute('created', self.metadata.editor())
            feature.setAttribute('creator', None)
            self.plugin.plan.buffer('polygons').addFeature(feature)

    def _editSourceSchematic(self):
        self._clearSchematicFilters()
        self._copySourceSchematic()
        self._editSchematic = True
        self.dock.widget.setCurrentIndex(0)
        self.plugin.iface.setActiveLayer(self.plugin.plan.buffer('polygons'))
        self.plugin.iface.actionZoomToLayer().trigger()
        self.plugin.plan.buffer('polygons').selectAll()
        self.plugin.iface.actionNodeTool().trigger()

    def _cloneSourceSchematic(self):
        self._clearSchematicFilters()
        self._copySourceSchematic()
        self._mergeSchematic()

    def _showSchematicReport(self):
        features = set()
        for feature in self.plugin.plan.layer('points').getFeatures():
            features.add(Item(feature))
        for feature in self.plugin.plan.layer('lines').getFeatures():
            features.add(Item(feature))
        for feature in self.plugin.plan.layer('polygons').getFeatures():
            features.add(Item(feature))
        schRequest = self._featureRequest(self._categoryClause('sch'))
        scsRequest = self._featureRequest(self._categoryClause('scs'))
        schematics = set()
        for feature in self.plugin.plan.layer('polygons').getFeatures(schRequest):
            schematics.add(Item(feature))
        for feature in self.plugin.plan.layer('polygons').getFeatures(scsRequest):
            schematics.add(Item(feature))
        missing = []
        contexts = self.plugin.data.items['context']
        for context in contexts:
            if context not in schematics:
                row = {}
                row['Site Code'] = context.siteCode()
                row['Context'] = context.itemId()
                itemData = self.plugin.data.getItemData(context)
                try:
                    row['Type'] = itemData['context_type']
                except Exception:
                    row['Type'] = ''
                    try:
                        vals = self.plugin.data.getItemFields(context, ['conf_field_cxttype'])
                        row['Type'] = vals[u'conf_field_cxttype']
                    except Exception:
                        row['Type'] = ''
                if context in features:
                    row['GIS'] = 'Y'
                else:
                    row['GIS'] = 'N'
                missing.append(row)
        text = '<html><head/><body><p><span style=" font-weight:600;">Missing Schematics:</span></p><p>There are ' + \
            str(len(contexts)) + ' Contexts in ARK, of which ' + \
            str(len(missing)) + ' are missing schematics.<br/></p></body></html>'
        dialog = TableDialog('Missing Schematics', text, ['Site Code', 'Context', 'Type', 'GIS'], {
                             'Site Code': '', 'Context': '', 'Type': '', 'GIS': ''}, self.dock)
        dialog.addRows(missing)
        dialog.exec_()
