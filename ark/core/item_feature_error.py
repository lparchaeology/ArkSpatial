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

from ArkSpatial.ark.lib import utils

from ArkSpatial.ark.core import ItemFeature


class ItemFeatureError:

    def __init__(self, fileInfo=None):
        self.layer = ''
        self.row = -1
        self.fid = -1
        self.feature = ItemFeature()
        self.field = ''
        self.message = ''
        self.ignore = False

    def toDict(self):
        d = {}
        d['layer'] = self.layer
        d['row'] = self.row
        d['fid'] = self.fid
        d['feature'] = self.feature
        d['field'] = self.field
        d['message'] = self.message
        return d

    def toCsv(self):
        return (utils.doublequote(self.layer) + ','
                + str(self.row) + ','
                + utils.doublequote(self.field) + ','
                + utils.doublequote(self.message))

    def toText(self):
        return (str(self.layer).ljust(20)
                + str(self.row).rjust(5) + '   '
                + str(self.field).ljust(20)
                + str(self.message))

    def toLog(self):
        return str(self.layer) + ' : ' + str(self.row) + ' : ' + str(self.field) + ' : ' + str(self.message)
