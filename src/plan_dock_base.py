# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plan/plan_dock_base.ui'
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

class Ui_PlanDockWidget(object):
    def setupUi(self, PlanDockWidget):
        PlanDockWidget.setObjectName(_fromUtf8("PlanDockWidget"))
        PlanDockWidget.resize(337, 416)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PlanDockWidget.sizePolicy().hasHeightForWidth())
        PlanDockWidget.setSizePolicy(sizePolicy)
        self.PlanDockContents = QtGui.QWidget()
        self.PlanDockContents.setObjectName(_fromUtf8("PlanDockContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.PlanDockContents)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.scrollArea = QtGui.QScrollArea(self.PlanDockContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 313, 324))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_2 = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.loadRawButton = QtGui.QPushButton(self.groupBox_2)
        self.loadRawButton.setObjectName(_fromUtf8("loadRawButton"))
        self.horizontalLayout_4.addWidget(self.loadRawButton)
        self.loadGeoButton = QtGui.QPushButton(self.groupBox_2)
        self.loadGeoButton.setObjectName(_fromUtf8("loadGeoButton"))
        self.horizontalLayout_4.addWidget(self.loadGeoButton)
        self.loadContextButton = QtGui.QPushButton(self.groupBox_2)
        self.loadContextButton.setObjectName(_fromUtf8("loadContextButton"))
        self.horizontalLayout_4.addWidget(self.loadContextButton)
        self.loadPlanButton = QtGui.QPushButton(self.groupBox_2)
        self.loadPlanButton.setObjectName(_fromUtf8("loadPlanButton"))
        self.horizontalLayout_4.addWidget(self.loadPlanButton)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.metadataWidget = MetadataWidget(self.scrollAreaWidgetContents)
        self.metadataWidget.setObjectName(_fromUtf8("metadataWidget"))
        self.gridLayout = QtGui.QGridLayout(self.metadataWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout.addWidget(self.metadataWidget)
        self.tabWidget = QtGui.QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.contextsTab = QtGui.QWidget()
        self.contextsTab.setObjectName(_fromUtf8("contextsTab"))
        self.gridLayout_4 = QtGui.QGridLayout(self.contextsTab)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.contextNumberLabel = QtGui.QLabel(self.contextsTab)
        self.contextNumberLabel.setObjectName(_fromUtf8("contextNumberLabel"))
        self.gridLayout_4.addWidget(self.contextNumberLabel, 0, 0, 1, 1)
        self.contextNumberSpin = QtGui.QSpinBox(self.contextsTab)
        self.contextNumberSpin.setMaximum(9999)
        self.contextNumberSpin.setObjectName(_fromUtf8("contextNumberSpin"))
        self.gridLayout_4.addWidget(self.contextNumberSpin, 0, 1, 1, 2)
        self.contextToolsLayout = QtGui.QGridLayout()
        self.contextToolsLayout.setObjectName(_fromUtf8("contextToolsLayout"))
        self.gridLayout_4.addLayout(self.contextToolsLayout, 1, 0, 1, 3)
        self.autoSchematiclLabel = QtGui.QLabel(self.contextsTab)
        self.autoSchematiclLabel.setObjectName(_fromUtf8("autoSchematiclLabel"))
        self.gridLayout_4.addWidget(self.autoSchematiclLabel, 2, 0, 1, 1)
        self.autoSchematicTool = QtGui.QToolButton(self.contextsTab)
        self.autoSchematicTool.setObjectName(_fromUtf8("autoSchematicTool"))
        self.gridLayout_4.addWidget(self.autoSchematicTool, 2, 2, 1, 1)
        self.tabWidget.addTab(self.contextsTab, _fromUtf8(""))
        self.featuresTab = QtGui.QWidget()
        self.featuresTab.setObjectName(_fromUtf8("featuresTab"))
        self.gridLayout_5 = QtGui.QGridLayout(self.featuresTab)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.featureNameEdit = QtGui.QLineEdit(self.featuresTab)
        self.featureNameEdit.setObjectName(_fromUtf8("featureNameEdit"))
        self.gridLayout_5.addWidget(self.featureNameEdit, 1, 1, 1, 1)
        self.featureToolsLayout = QtGui.QGridLayout()
        self.featureToolsLayout.setObjectName(_fromUtf8("featureToolsLayout"))
        self.gridLayout_5.addLayout(self.featureToolsLayout, 2, 0, 1, 2)
        self.featureIdLabel = QtGui.QLabel(self.featuresTab)
        self.featureIdLabel.setObjectName(_fromUtf8("featureIdLabel"))
        self.gridLayout_5.addWidget(self.featureIdLabel, 0, 0, 1, 1)
        self.featureNameLabel = QtGui.QLabel(self.featuresTab)
        self.featureNameLabel.setObjectName(_fromUtf8("featureNameLabel"))
        self.gridLayout_5.addWidget(self.featureNameLabel, 1, 0, 1, 1)
        self.featureIdSpin = QtGui.QSpinBox(self.featuresTab)
        self.featureIdSpin.setMaximum(99999)
        self.featureIdSpin.setObjectName(_fromUtf8("featureIdSpin"))
        self.gridLayout_5.addWidget(self.featureIdSpin, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem, 3, 1, 1, 1)
        self.tabWidget.addTab(self.featuresTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        spacerItem1 = QtGui.QSpacerItem(17, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.clearButton = QtGui.QPushButton(self.PlanDockContents)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.horizontalLayout.addWidget(self.clearButton)
        self.mergeButton = QtGui.QPushButton(self.PlanDockContents)
        self.mergeButton.setObjectName(_fromUtf8("mergeButton"))
        self.horizontalLayout.addWidget(self.mergeButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        PlanDockWidget.setWidget(self.PlanDockContents)
        self.contextNumberLabel.setBuddy(self.contextNumberSpin)
        self.featureIdLabel.setBuddy(self.featureIdSpin)
        self.featureNameLabel.setBuddy(self.featureNameEdit)

        self.retranslateUi(PlanDockWidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PlanDockWidget)
        PlanDockWidget.setTabOrder(self.scrollArea, self.loadRawButton)
        PlanDockWidget.setTabOrder(self.loadRawButton, self.loadGeoButton)
        PlanDockWidget.setTabOrder(self.loadGeoButton, self.loadContextButton)
        PlanDockWidget.setTabOrder(self.loadContextButton, self.tabWidget)
        PlanDockWidget.setTabOrder(self.tabWidget, self.contextNumberSpin)
        PlanDockWidget.setTabOrder(self.contextNumberSpin, self.clearButton)
        PlanDockWidget.setTabOrder(self.clearButton, self.mergeButton)
        PlanDockWidget.setTabOrder(self.mergeButton, self.featureIdSpin)
        PlanDockWidget.setTabOrder(self.featureIdSpin, self.featureNameEdit)

    def retranslateUi(self, PlanDockWidget):
        PlanDockWidget.setWindowTitle(_translate("PlanDockWidget", "ArkPlan", None))
        self.groupBox_2.setTitle(_translate("PlanDockWidget", "Load Drawings", None))
        self.loadRawButton.setText(_translate("PlanDockWidget", "Raw", None))
        self.loadGeoButton.setText(_translate("PlanDockWidget", "Geo", None))
        self.loadContextButton.setText(_translate("PlanDockWidget", "Cxt", None))
        self.loadPlanButton.setText(_translate("PlanDockWidget", "Plan", None))
        self.contextNumberLabel.setText(_translate("PlanDockWidget", "Context:", None))
        self.contextNumberSpin.setToolTip(_translate("PlanDockWidget", "Context Number", None))
        self.autoSchematiclLabel.setText(_translate("PlanDockWidget", "Auto Schematic:", None))
        self.autoSchematicTool.setText(_translate("PlanDockWidget", "Auto", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.contextsTab), _translate("PlanDockWidget", "Contexts", None))
        self.featureIdLabel.setText(_translate("PlanDockWidget", "ID:", None))
        self.featureNameLabel.setText(_translate("PlanDockWidget", "Name:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.featuresTab), _translate("PlanDockWidget", "Features", None))
        self.clearButton.setToolTip(_translate("PlanDockWidget", "Clear unsaved changes from work layers", None))
        self.clearButton.setText(_translate("PlanDockWidget", "Clear", None))
        self.mergeButton.setToolTip(_translate("PlanDockWidget", "Move new context to main layers", None))
        self.mergeButton.setText(_translate("PlanDockWidget", "Merge", None))

from ..libarkqgis.dock import ArkDockWidget
from metadata_widget import MetadataWidget