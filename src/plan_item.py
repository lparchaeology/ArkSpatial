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
        copyright            : 2016 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2016 by John Layt
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
from functools import total_ordering

from PyQt4.QtCore import QVariant

from qgis.core import QgsFeature, QgsFeatureRequest

from ..libarkqgis import utils

from config import Config

def _value(value):
    if isinstance(value, str) and value.strip() == '':
        return None
    return value

def _setAttribute(feature, field, value):
    try:
        feature.setAttribute(Config.fieldName(field), _value(value))
    except:
        pass

def _setDict(toDict, field, value):
    try:
        toDict[Config.fieldName(field)] = _value(value)
    except:
        pass

def _attribute(feature, field):
    try:
        return feature.attribute(Config.fieldName(field))
    except:
        return None

@total_ordering
class ItemKey():
    siteCode = ''
    classCode = ''
    itemId = ''

    def __init__(self, siteCode=None, classCode=None, itemId=None):
        if isinstance(siteCode, QgsFeature):
            self.fromFeature(siteCode)
        else:
            self.setKey(siteCode, classCode, itemId)

    def __eq__(self, other):
        if isinstance(other, ItemKey):
            return self.siteCode == other.siteCode and self.classCode == other.classCode and self.itemId == other.itemId
        else:
            return False

    def __lt__(self, other):
        if self.siteCode == other.siteCode and self.classCode == other.classCode:
            return self._lt(self.itemId, other.itemId)
        elif self.siteCode == other.siteCode:
            return self.classCode < other.classCode and self._lt(self.itemId, other.itemId)
        return self.siteCode < other.siteCode and self.classCode < other.classCode and self._lt(self.itemId, other.itemId)

    def _lt(self, id1, id2):
        if isinstance(id1, str) and id1.isdigit() and isinstance(id2, str) and id2.isdigit():
            return int(id1) < int(id2)
        else:
            return str(id1) < str(id2)

    def __hash__(self):
        return hash((self.siteCode, self.classCode, self.itemId))

    def __str__(self):
        return 'ItemKey(' + str(self.siteCode) + ', ' +  str(self.classCode) + ', ' +  str(self.itemId) + ')'

    def debug(self):
        return 'ItemKey(' + utils.printable(self.siteCode) + ', ' +  utils.printable(self.classCode) + ', ' +  utils.printable(self.itemId) + ')'

    def isValid(self):
        return (isinstance(self.siteCode, str) and self.siteCode
                and isinstance(self.classCode, str) and self.classCode
                and isinstance(self.itemId, str) and self.itemId)

    def isInvalid(self):
        return (not isinstance(self.siteCode, str) or self.siteCode == ''
                or not isinstance(self.classCode, str) or self.classCode == ''
                or not isinstance(self.itemId, str) or self.itemId == '')

    def isNull(self):
        return (self.siteCode == '' and self.classCode == '' and self.itemId == '')

    def isItemRange(self):
        return isinstance(self.itemId, str) and (self.itemId.contains('-') or self.itemId.contains(' '))

    def itemLabel(self):
        if self.classCode:
            return Config.classCodes[self.classCode]['label'] + ' ' + self.itemId
        return ''

    def name(self):
        return self.classCode + '_' + self.siteCode + '_' + self.itemId

    def itemValue(self):
        return self.siteCode + '_' + self.itemId

    def setKey(self, siteCode, classCode, itemId):
        if siteCode and classCode and itemId:
            self.setSiteCode(siteCode)
            self.setClassCode(classCode)
            self.setItemId(itemId)
        else:
            self.siteCode = ''
            self.classCode = ''
            self.itemId = ''

    def fromFeature(self, feature):
        siteCode = _attribute(feature, 'site')
        classCode = _attribute(feature, 'class')
        itemId = _attribute(feature, 'id')
        self.setKey(siteCode, classCode, itemId)

    def toFeature(self, feature):
        _setAttribute(feature, 'site', self.siteCode)
        _setAttribute(feature, 'class', self.classCode)
        _setAttribute(feature, 'id', self.itemId)

    def toAttributes(self):
        attrs = {}
        _setDict(attrs, 'site', self.siteCode)
        _setDict(attrs, 'class', self.classCode)
        _setDict(attrs, 'id', self.itemId)
        return attrs

    def toCsv(self):
        return utils.doublequote(self.siteCode) + ',' + utils.doublequote(self.classCode) + ',' + utils.doublequote(self.itemId)

    def setSiteCode(self, siteCode):
        self.siteCode = utils.string(siteCode)

    def setClassCode(self, classCode):
        self.classCode = utils.string(classCode)

    def setItemId(self, itemId):
        if isinstance(itemId, list) or isinstance(itemId, set):
            self.itemId = utils.listToRange(itemId)
        else:
            self.itemId = utils.string(itemId)

    def addItemId(self, itemId):
        if self.itemId == '':
            self.setItemId(itemId)
        else:
            lst = self.itemIdList()
            if isinstance(itemId, list) or isinstance(itemId, set):
                lst.extend(itemId)
            else:
                lst.append(utils.string(itemId))
            self.setItemId(lst)

    def itemIdList(self):
        return utils.rangeToList(self.itemId)

    def filterClause(self):
        if self.isInvalid():
            return ''
        clause = '("' + Config.fieldName('site') + '" = \'' + self.siteCode + '\''
        clause = clause + ' and "' + Config.fieldName('class') + '" = \'' + self.classCode + '\''
        subs = self.itemId.split()
        if len(subs) == 0:
            clause += ')'
            return clause
        clause += ' and ('
        first = True
        for sub in subs:
            if first:
                first = False
            else:
                clause = clause + ' or '
            field = Config.fieldName('id')
            if sub.find('-') >= 0:
                vals = sub.split('-')
                clause = clause + ' ("' + field + '" >= ' + vals[0] + ' and "' + field + '" <= ' + vals[1] + ')'
            else:
                clause = clause + '"' + field + '" = ' + sub
        clause += '))'
        return clause

    def featureRequest(self):
        request = QgsFeatureRequest()
        request.setFilterExpression(self.filterClause())
        return request


class ItemSource():
    sourceCode = ''
    key = ItemKey()
    filename = ''

    def __init__(self, sourceCode=None, sourceKey=None, filename=None):
        if isinstance(sourceCode, QgsFeature):
            self.fromFeature(sourceCode)
        else:
            self.setSource(sourceCode, sourceKey, filename)

    def __eq__(self, other):
        if isinstance(other, ItemSource):
            return self.sourceCode == other.sourceCode and self.key == other.key and self.filename == other.filename
        else:
            return False

    def __hash__(self):
        return hash((self.sourceCode, self.key, self.filename))

    def __str__(self):
        return 'ItemSource(' + str(self.sourceCode) + ', ' + str(self.key) + ', ' +  str(self.filename) + ')'

    def debug(self):
        return 'ItemSource(' + utils.printable(self.sourceCode) + ', ' +  self.key.debug() + ', ' +  utils.printable(self.filename) + ')'

    def isValid(self):
        if self.sourceCode == '':
            return False
        if Config.sourceCodes[self.sourceCode]['sourceItem']:
            return self.key.isValid()
        return isinstance(self.key, ItemKey) and (self.key.isValid() or self.key.isNull())

    def isInvalid(self):
        return not self.isValid()

    def isNull(self):
        return self.sourceCode == '' and isinstance(sourceKey, ItemKey) and self.key.isNull() and self.filename == ''

    def sourceCodeLabel(self):
        return Config.sourceCodes[self.sourceCode]['label']

    def setSource(self, sourceCode, sourceKey, filename):
        self.sourceCode = utils.string(sourceCode)
        if isinstance(sourceKey, ItemKey):
            self.key = sourceKey
        else:
            self.key = ItemKey()
        self.filename = utils.string(filename)

    def setSourceCode(self, sourceCode):
        self.sourceCode = utils.string(sourceCode)

    def setSiteCode(self, siteCode):
        self.key.setSiteCode(siteCode)

    def setSourceClass(self, classCode):
        self.key.setClassCode(classCode)

    def setSourceId(self, itemId):
        self.key.setItemId(itemId)

    def setFilename(self, filename):
        self.filename = utils.string(filename)

    def fromFeature(self, feature):
        sourceCode = _attribute(feature, 'source_cd')
        siteCode = _attribute(feature, 'site')
        classCode = _attribute(feature, 'source_cl')
        itemId = _attribute(feature, 'source_id')
        sourceKey = ItemKey(siteCode, classCode, itemId)
        filename = _attribute(feature, 'file')
        self.setSource(sourceCode, sourceKey, filename)

    def toFeature(self, feature):
        _setAttribute(feature, 'source_cd', self.sourceCode)
        _setAttribute(feature, 'source_cl', self.key.classCode)
        _setAttribute(feature, 'source_id', self.key.itemId)
        _setAttribute(feature, 'file', self.filename)

    def toAttributes(self):
        attrs = {}
        _setDict(attrs, 'source_cd', self.sourceCode)
        _setDict(attrs, 'source_cl', self.key.classCode)
        _setDict(attrs, 'source_id', self.key.itemId)
        _setDict(attrs, 'file', self.filename)
        return attrs

class ItemFeature():
    key = ItemKey()
    category = ''
    name = ''
    source = ItemSource()
    comment = ''
    createdBy = ''
    createdOn = ''

    def __init__(self, key=None, category=None, name=None, source=None, comment=None, createdBy=None, createdOn=None):
        if isinstance(key, QgsFeature):
            self.fromFeature(key)
        else:
            self.setFeature(key, category, name, source, comment, createdBy, createdOn)

    def __eq__(self, other):
        if isinstance(other, ItemFeature):
            return (self.key == other.key and self.category == other.category and self.name == other.name
                    and self.source == other.source and self.comment == other.comment
                    and self.createdBy == other.createdBy and self.createdOn == other.createdOn)
        else:
            return False

    def __lt__(self, other):
        if self.key == other.key:
            return self.category < other.category
        return self.key < other.key

    def __hash__(self):
        return hash((self.key, self.category, self.name, self.source, self.comment, self.createdBy, self.createdOn))

    def __str__(self):
        return 'ItemFeature(' + str(self.key) + ', ' +  str(self.key.category) + ', ' +  str(self.key.name) + ', ' + str(self.source) + ', ' + str(self.comment) + ', ' + str(self.createdBy) + ', ' + str(self.createdOn) + ')'

    def debug(self):
        return 'ItemFeature(' + self.key.debug() + ', ' +  utils.printable(self.category) + ', ' +  utils.printable(self.name) + ', ' + self.source.debug() + ', ' +  utils.printable(self.comment) + ', ' +  utils.printable(self.createdBy) + ', ' +  utils.printable(self.createdOn) + ')'

    def isValid(self):
        return isinstance(self.key, ItemKey) and self.key.isValid() and self.category and isinstance(self.source, ItemSource) and (self.source.isNull() or self.source.isValid())

    def isInvalid(self):
        return not self.isValid()

    def isNull(self):
        return (isinstance(self.key, ItemKey) and self.key.isNull() and self.category == '' and self.name == ''
                and isinstance(self.source, ItemSource) and self.source.isNull()
                and self.comment == '' and self.createdBy == '' and self.createdOn == '' )

    def setFeature(self, key, category, name, source, comment, createdBy, createdOn):
        if isinstance(key, ItemKey):
            self.key = key
        else:
            self.key = ItemKey()
        self.category = utils.string(category)
        self.name = utils.string(name)
        if isinstance(source, ItemSource):
            self.source = source
        else:
            self.source = ItemSource()
        self.comment = utils.string(comment)
        self.createdBy = utils.string(createdBy)
        self.createdOn = utils.string(createdOn)

    def setCategory(self, category):
        self.category = utils.string(category)

    def setName(self, name):
        self.name = utils.string(name)

    def setComment(self, comment):
        self.comment = utils.string(comment)

    def setCreatedBy(self, createdBy):
        self.createdBy = utils.string(createdBy)

    def setCreatedOn(self, createdOn):
        self.createdOn = utils.string(createdOn)

    def fromFeature(self, feature):
        key = ItemKey(feature)
        category = _attribute(feature, 'category')
        name = _attribute(feature, 'name')
        source = ItemSource(feature)
        comment = _attribute(feature, 'comment')
        createdBy = _attribute(feature, 'created_by')
        createdOn = _attribute(feature, 'created_on')
        self.setFeature(key, category, name, source, comment, createdBy, createdOn)

    def toFeature(self, feature):
        self.key.toFeature(feature)
        _setAttribute(feature, 'category', self.category)
        _setAttribute(feature, 'name', self.name)
        self.source.toFeature(feature)
        _setAttribute(feature, 'comment', self.comment)
        _setAttribute(feature, 'created_by', self.createdBy)
        _setAttribute(feature, 'created_on', self.createdOn)

    def toAttributes(self):
        attrs = {}
        attrs = self.key.toAttributes()
        _setDict(attrs, 'category', self.category)
        _setDict(attrs, 'name', self.name)
        attrs.update(self.source.toAttributes())
        _setDict(attrs, 'comment', self.comment)
        _setDict(attrs, 'created_by', self.createdBy)
        _setDict(attrs, 'created_on', self.createdOn)
        return attrs
