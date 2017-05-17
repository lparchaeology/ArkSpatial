# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/drawing_widget_base.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DrawingWidget(object):
    def setupUi(self, DrawingWidget):
        DrawingWidget.setObjectName(_fromUtf8("DrawingWidget"))
        DrawingWidget.resize(438, 324)
        self.planTab = QtGui.QWidget()
        self.planTab.setObjectName(_fromUtf8("planTab"))
        self.gridLayout = QtGui.QGridLayout(self.planTab)
        self.gridLayout.setContentsMargins(12, -1, 12, 12)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.autoSchematicTool = QtGui.QToolButton(self.planTab)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/autoSchematic.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.autoSchematicTool.setIcon(icon)
        self.autoSchematicTool.setObjectName(_fromUtf8("autoSchematicTool"))
        self.gridLayout.addWidget(self.autoSchematicTool, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 2)
        self.autoSchematiclLabel = QtGui.QLabel(self.planTab)
        self.autoSchematiclLabel.setObjectName(_fromUtf8("autoSchematiclLabel"))
        self.gridLayout.addWidget(self.autoSchematiclLabel, 3, 0, 1, 1)
        self.planPointGroup = QtGui.QGroupBox(self.planTab)
        self.planPointGroup.setFlat(True)
        self.planPointGroup.setObjectName(_fromUtf8("planPointGroup"))
        self.planPointLayout = QtGui.QGridLayout(self.planPointGroup)
        self.planPointLayout.setObjectName(_fromUtf8("planPointLayout"))
        self.gridLayout.addWidget(self.planPointGroup, 0, 0, 1, 2)
        self.planLineGroup = QtGui.QGroupBox(self.planTab)
        self.planLineGroup.setFlat(True)
        self.planLineGroup.setObjectName(_fromUtf8("planLineGroup"))
        self.planLineLayout = QtGui.QGridLayout(self.planLineGroup)
        self.planLineLayout.setObjectName(_fromUtf8("planLineLayout"))
        self.gridLayout.addWidget(self.planLineGroup, 1, 0, 1, 2)
        self.planPolygonGroup = QtGui.QGroupBox(self.planTab)
        self.planPolygonGroup.setFlat(True)
        self.planPolygonGroup.setObjectName(_fromUtf8("planPolygonGroup"))
        self.planPolygonLayout = QtGui.QGridLayout(self.planPolygonGroup)
        self.planPolygonLayout.setObjectName(_fromUtf8("planPolygonLayout"))
        self.gridLayout.addWidget(self.planPolygonGroup, 2, 0, 1, 2)
        DrawingWidget.addTab(self.planTab, _fromUtf8(""))
        self.sectionTab = QtGui.QWidget()
        self.sectionTab.setObjectName(_fromUtf8("sectionTab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.sectionTab)
        self.gridLayout_2.setContentsMargins(12, -1, 12, 12)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(118, 121, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 3, 0, 1, 2)
        self.sectionPolygonGroup = QtGui.QGroupBox(self.sectionTab)
        self.sectionPolygonGroup.setFlat(True)
        self.sectionPolygonGroup.setObjectName(_fromUtf8("sectionPolygonGroup"))
        self.sectionPolygonLayout = QtGui.QGridLayout(self.sectionPolygonGroup)
        self.sectionPolygonLayout.setObjectName(_fromUtf8("sectionPolygonLayout"))
        self.gridLayout_2.addWidget(self.sectionPolygonGroup, 2, 0, 1, 2)
        self.sectionLineGroup = QtGui.QGroupBox(self.sectionTab)
        self.sectionLineGroup.setFlat(True)
        self.sectionLineGroup.setObjectName(_fromUtf8("sectionLineGroup"))
        self.sectionLineLayout = QtGui.QGridLayout(self.sectionLineGroup)
        self.sectionLineLayout.setObjectName(_fromUtf8("sectionLineLayout"))
        self.gridLayout_2.addWidget(self.sectionLineGroup, 1, 0, 1, 2)
        self.sectionPointGroup = QtGui.QGroupBox(self.sectionTab)
        self.sectionPointGroup.setFlat(True)
        self.sectionPointGroup.setObjectName(_fromUtf8("sectionPointGroup"))
        self.sectionPointLayout = QtGui.QGridLayout(self.sectionPointGroup)
        self.sectionPointLayout.setObjectName(_fromUtf8("sectionPointLayout"))
        self.gridLayout_2.addWidget(self.sectionPointGroup, 0, 0, 1, 2)
        DrawingWidget.addTab(self.sectionTab, _fromUtf8(""))
        self.baseTab = QtGui.QWidget()
        self.baseTab.setObjectName(_fromUtf8("baseTab"))
        self.gridLayout_3 = QtGui.QGridLayout(self.baseTab)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(88, 134, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 3, 0, 1, 2)
        self.baseLineGroup = QtGui.QGroupBox(self.baseTab)
        self.baseLineGroup.setFlat(True)
        self.baseLineGroup.setObjectName(_fromUtf8("baseLineGroup"))
        self.baseLineLayout = QtGui.QGridLayout(self.baseLineGroup)
        self.baseLineLayout.setObjectName(_fromUtf8("baseLineLayout"))
        self.gridLayout_3.addWidget(self.baseLineGroup, 1, 0, 1, 2)
        self.basePolygonGroup = QtGui.QGroupBox(self.baseTab)
        self.basePolygonGroup.setFlat(True)
        self.basePolygonGroup.setObjectName(_fromUtf8("basePolygonGroup"))
        self.basePolygonLayout = QtGui.QGridLayout(self.basePolygonGroup)
        self.basePolygonLayout.setObjectName(_fromUtf8("basePolygonLayout"))
        self.gridLayout_3.addWidget(self.basePolygonGroup, 2, 0, 1, 2)
        self.basePointGroup = QtGui.QGroupBox(self.baseTab)
        self.basePointGroup.setFlat(True)
        self.basePointGroup.setObjectName(_fromUtf8("basePointGroup"))
        self.basePointLayout = QtGui.QGridLayout(self.basePointGroup)
        self.basePointLayout.setObjectName(_fromUtf8("basePointLayout"))
        self.gridLayout_3.addWidget(self.basePointGroup, 0, 0, 1, 2)
        DrawingWidget.addTab(self.baseTab, _fromUtf8(""))

        self.retranslateUi(DrawingWidget)
        DrawingWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DrawingWidget)

    def retranslateUi(self, DrawingWidget):
        DrawingWidget.setWindowTitle(_translate("DrawingWidget", "TabWidget", None))
        self.autoSchematicTool.setToolTip(_translate("DrawingWidget", "<html><head/><body><p>Auto Schematic</p></body></html>", None))
        self.autoSchematicTool.setText(_translate("DrawingWidget", "...", None))
        self.autoSchematiclLabel.setText(_translate("DrawingWidget", "Auto Schematic:", None))
        self.planPointGroup.setTitle(_translate("DrawingWidget", "Point", None))
        self.planLineGroup.setTitle(_translate("DrawingWidget", "Line", None))
        self.planPolygonGroup.setTitle(_translate("DrawingWidget", "Polygon", None))
        DrawingWidget.setTabText(DrawingWidget.indexOf(self.planTab), _translate("DrawingWidget", "Plan", None))
        self.sectionPolygonGroup.setTitle(_translate("DrawingWidget", "Polygon", None))
        self.sectionLineGroup.setTitle(_translate("DrawingWidget", "Line", None))
        self.sectionPointGroup.setTitle(_translate("DrawingWidget", "Point", None))
        DrawingWidget.setTabText(DrawingWidget.indexOf(self.sectionTab), _translate("DrawingWidget", "Section", None))
        self.baseLineGroup.setTitle(_translate("DrawingWidget", "Line", None))
        self.basePolygonGroup.setTitle(_translate("DrawingWidget", "Polygon", None))
        self.basePointGroup.setTitle(_translate("DrawingWidget", "Point", None))
        DrawingWidget.setTabText(DrawingWidget.indexOf(self.baseTab), _translate("DrawingWidget", "Base", None))

import resources_rc
