# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/schematic_widget_base.ui'
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

class Ui_SchematicWidget(object):
    def setupUi(self, SchematicWidget):
        SchematicWidget.setObjectName(_fromUtf8("SchematicWidget"))
        SchematicWidget.resize(284, 761)
        self.gridLayout = QtGui.QGridLayout(SchematicWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(14, 17, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.checkGroup = QtGui.QGroupBox(SchematicWidget)
        self.checkGroup.setObjectName(_fromUtf8("checkGroup"))
        self.gridLayout_4 = QtGui.QGridLayout(self.checkGroup)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem1, 2, 1, 1, 1)
        self.schematicStatusLabel = QtGui.QLabel(self.checkGroup)
        self.schematicStatusLabel.setText(_fromUtf8(""))
        self.schematicStatusLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/statusUnknown.png")))
        self.schematicStatusLabel.setObjectName(_fromUtf8("schematicStatusLabel"))
        self.gridLayout_5.addWidget(self.schematicStatusLabel, 2, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem2, 1, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem3, 3, 1, 1, 1)
        self.featureDataStatusLabel = QtGui.QLabel(self.checkGroup)
        self.featureDataStatusLabel.setText(_fromUtf8(""))
        self.featureDataStatusLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/statusUnknown.png")))
        self.featureDataStatusLabel.setObjectName(_fromUtf8("featureDataStatusLabel"))
        self.gridLayout_5.addWidget(self.featureDataStatusLabel, 1, 2, 1, 1)
        self.schematicLabel = QtGui.QLabel(self.checkGroup)
        self.schematicLabel.setObjectName(_fromUtf8("schematicLabel"))
        self.gridLayout_5.addWidget(self.schematicLabel, 2, 0, 1, 1)
        self.featureDataLabel = QtGui.QLabel(self.checkGroup)
        self.featureDataLabel.setObjectName(_fromUtf8("featureDataLabel"))
        self.gridLayout_5.addWidget(self.featureDataLabel, 1, 0, 1, 1)
        self.sectionSchematicStatusLabel = QtGui.QLabel(self.checkGroup)
        self.sectionSchematicStatusLabel.setText(_fromUtf8(""))
        self.sectionSchematicStatusLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/statusUnknown.png")))
        self.sectionSchematicStatusLabel.setObjectName(_fromUtf8("sectionSchematicStatusLabel"))
        self.gridLayout_5.addWidget(self.sectionSchematicStatusLabel, 3, 2, 1, 1)
        self.sectionSchematicLabel = QtGui.QLabel(self.checkGroup)
        self.sectionSchematicLabel.setObjectName(_fromUtf8("sectionSchematicLabel"))
        self.gridLayout_5.addWidget(self.sectionSchematicLabel, 3, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_5, 4, 0, 1, 1)
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.resetLabel = QtGui.QLabel(self.checkGroup)
        self.resetLabel.setObjectName(_fromUtf8("resetLabel"))
        self.gridLayout_6.addWidget(self.resetLabel, 2, 0, 1, 1)
        self.editContexLabel = QtGui.QLabel(self.checkGroup)
        self.editContexLabel.setObjectName(_fromUtf8("editContexLabel"))
        self.gridLayout_6.addWidget(self.editContexLabel, 0, 0, 1, 1)
        self.deleteSectionLabel = QtGui.QLabel(self.checkGroup)
        self.deleteSectionLabel.setObjectName(_fromUtf8("deleteSectionLabel"))
        self.gridLayout_6.addWidget(self.deleteSectionLabel, 1, 0, 1, 1)
        self.deleteSectionButton = QtGui.QPushButton(self.checkGroup)
        self.deleteSectionButton.setObjectName(_fromUtf8("deleteSectionButton"))
        self.gridLayout_6.addWidget(self.deleteSectionButton, 1, 2, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem4, 1, 1, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem5, 0, 1, 1, 1)
        self.editContextButton = QtGui.QPushButton(self.checkGroup)
        self.editContextButton.setObjectName(_fromUtf8("editContextButton"))
        self.gridLayout_6.addWidget(self.editContextButton, 0, 2, 1, 1)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem6, 2, 1, 1, 1)
        self.resetButton = QtGui.QPushButton(self.checkGroup)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.gridLayout_6.addWidget(self.resetButton, 2, 2, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_6, 5, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.contextSpin = QtGui.QSpinBox(self.checkGroup)
        self.contextSpin.setMaximum(99999)
        self.contextSpin.setObjectName(_fromUtf8("contextSpin"))
        self.horizontalLayout_2.addWidget(self.contextSpin)
        self.findContextTool = QtGui.QToolButton(self.checkGroup)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/search.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.findContextTool.setIcon(icon)
        self.findContextTool.setObjectName(_fromUtf8("findContextTool"))
        self.horizontalLayout_2.addWidget(self.findContextTool)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 2, 1, 1)
        self.siteCodeLabel = QtGui.QLabel(self.checkGroup)
        self.siteCodeLabel.setObjectName(_fromUtf8("siteCodeLabel"))
        self.gridLayout_2.addWidget(self.siteCodeLabel, 0, 0, 1, 2)
        self.siteCodeCombo = QtGui.QComboBox(self.checkGroup)
        self.siteCodeCombo.setObjectName(_fromUtf8("siteCodeCombo"))
        self.gridLayout_2.addWidget(self.siteCodeCombo, 0, 2, 1, 1)
        self.contextDescriptionEdit = QtGui.QLineEdit(self.checkGroup)
        self.contextDescriptionEdit.setReadOnly(True)
        self.contextDescriptionEdit.setObjectName(_fromUtf8("contextDescriptionEdit"))
        self.gridLayout_2.addWidget(self.contextDescriptionEdit, 3, 0, 1, 3)
        self.arkDataLabel = QtGui.QLabel(self.checkGroup)
        self.arkDataLabel.setObjectName(_fromUtf8("arkDataLabel"))
        self.gridLayout_2.addWidget(self.arkDataLabel, 2, 0, 1, 2)
        self.contextLabel = QtGui.QLabel(self.checkGroup)
        self.contextLabel.setObjectName(_fromUtf8("contextLabel"))
        self.gridLayout_2.addWidget(self.contextLabel, 1, 0, 1, 2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.contextTypeEdit = QtGui.QLineEdit(self.checkGroup)
        self.contextTypeEdit.setFrame(True)
        self.contextTypeEdit.setReadOnly(True)
        self.contextTypeEdit.setObjectName(_fromUtf8("contextTypeEdit"))
        self.horizontalLayout_4.addWidget(self.contextTypeEdit)
        self.openContextTool = QtGui.QToolButton(self.checkGroup)
        self.openContextTool.setEnabled(False)
        self.openContextTool.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/filter/web.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openContextTool.setIcon(icon1)
        self.openContextTool.setObjectName(_fromUtf8("openContextTool"))
        self.horizontalLayout_4.addWidget(self.openContextTool)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 2, 2, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.loadArkTool = QtGui.QToolButton(self.checkGroup)
        self.loadArkTool.setEnabled(False)
        self.loadArkTool.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/filter/loadData.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loadArkTool.setIcon(icon2)
        self.loadArkTool.setObjectName(_fromUtf8("loadArkTool"))
        self.horizontalLayout_3.addWidget(self.loadArkTool)
        self.firstContextTool = QtGui.QToolButton(self.checkGroup)
        self.firstContextTool.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/goFirstItem.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.firstContextTool.setIcon(icon3)
        self.firstContextTool.setObjectName(_fromUtf8("firstContextTool"))
        self.horizontalLayout_3.addWidget(self.firstContextTool)
        self.prevMissingTool = QtGui.QToolButton(self.checkGroup)
        self.prevMissingTool.setEnabled(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/goPrevMissing.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prevMissingTool.setIcon(icon4)
        self.prevMissingTool.setObjectName(_fromUtf8("prevMissingTool"))
        self.horizontalLayout_3.addWidget(self.prevMissingTool)
        self.prevContextTool = QtGui.QToolButton(self.checkGroup)
        self.prevContextTool.setEnabled(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/goPrevItem.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prevContextTool.setIcon(icon5)
        self.prevContextTool.setObjectName(_fromUtf8("prevContextTool"))
        self.horizontalLayout_3.addWidget(self.prevContextTool)
        self.nextContextTool = QtGui.QToolButton(self.checkGroup)
        self.nextContextTool.setEnabled(False)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/goNextItem.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextContextTool.setIcon(icon6)
        self.nextContextTool.setObjectName(_fromUtf8("nextContextTool"))
        self.horizontalLayout_3.addWidget(self.nextContextTool)
        self.nextMissingTool = QtGui.QToolButton(self.checkGroup)
        self.nextMissingTool.setEnabled(False)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/goNextMissing.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextMissingTool.setIcon(icon7)
        self.nextMissingTool.setObjectName(_fromUtf8("nextMissingTool"))
        self.horizontalLayout_3.addWidget(self.nextMissingTool)
        self.lastContextTool = QtGui.QToolButton(self.checkGroup)
        self.lastContextTool.setEnabled(False)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/goLastItem.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lastContextTool.setIcon(icon8)
        self.lastContextTool.setObjectName(_fromUtf8("lastContextTool"))
        self.horizontalLayout_3.addWidget(self.lastContextTool)
        self.gridLayout_4.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.checkGroup, 0, 0, 1, 1)
        self.cloneGroup = QtGui.QGroupBox(SchematicWidget)
        self.cloneGroup.setObjectName(_fromUtf8("cloneGroup"))
        self.gridLayout_8 = QtGui.QGridLayout(self.cloneGroup)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem7, 1, 1, 1, 1)
        self.sourceSchematicLabel = QtGui.QLabel(self.cloneGroup)
        self.sourceSchematicLabel.setObjectName(_fromUtf8("sourceSchematicLabel"))
        self.gridLayout_3.addWidget(self.sourceSchematicLabel, 1, 0, 1, 1)
        self.sourceSchematicStatusLabel = QtGui.QLabel(self.cloneGroup)
        self.sourceSchematicStatusLabel.setText(_fromUtf8(""))
        self.sourceSchematicStatusLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/statusUnknown.png")))
        self.sourceSchematicStatusLabel.setObjectName(_fromUtf8("sourceSchematicStatusLabel"))
        self.gridLayout_3.addWidget(self.sourceSchematicStatusLabel, 1, 2, 1, 1)
        self.sourceFeatureDataLabel = QtGui.QLabel(self.cloneGroup)
        self.sourceFeatureDataLabel.setObjectName(_fromUtf8("sourceFeatureDataLabel"))
        self.gridLayout_3.addWidget(self.sourceFeatureDataLabel, 0, 0, 1, 1)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem8, 0, 1, 1, 1)
        self.sourceFeatureDataStatusLabel = QtGui.QLabel(self.cloneGroup)
        self.sourceFeatureDataStatusLabel.setText(_fromUtf8(""))
        self.sourceFeatureDataStatusLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/plan/statusUnknown.png")))
        self.sourceFeatureDataStatusLabel.setObjectName(_fromUtf8("sourceFeatureDataStatusLabel"))
        self.gridLayout_3.addWidget(self.sourceFeatureDataStatusLabel, 0, 2, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_3, 1, 0, 1, 1)
        self.gridLayout_7 = QtGui.QGridLayout()
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.cloneSourceLabel = QtGui.QLabel(self.cloneGroup)
        self.cloneSourceLabel.setObjectName(_fromUtf8("cloneSourceLabel"))
        self.gridLayout_7.addWidget(self.cloneSourceLabel, 0, 0, 1, 1)
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem9, 0, 1, 1, 1)
        self.cloneSourceButton = QtGui.QPushButton(self.cloneGroup)
        self.cloneSourceButton.setObjectName(_fromUtf8("cloneSourceButton"))
        self.gridLayout_7.addWidget(self.cloneSourceButton, 0, 2, 1, 1)
        self.copySourceLabel = QtGui.QLabel(self.cloneGroup)
        self.copySourceLabel.setObjectName(_fromUtf8("copySourceLabel"))
        self.gridLayout_7.addWidget(self.copySourceLabel, 1, 0, 1, 1)
        spacerItem10 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem10, 1, 1, 1, 1)
        self.copySourceButton = QtGui.QPushButton(self.cloneGroup)
        self.copySourceButton.setObjectName(_fromUtf8("copySourceButton"))
        self.gridLayout_7.addWidget(self.copySourceButton, 1, 2, 1, 1)
        self.editSourceLabel = QtGui.QLabel(self.cloneGroup)
        self.editSourceLabel.setObjectName(_fromUtf8("editSourceLabel"))
        self.gridLayout_7.addWidget(self.editSourceLabel, 2, 0, 1, 1)
        spacerItem11 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem11, 2, 1, 1, 1)
        self.editSourceButton = QtGui.QPushButton(self.cloneGroup)
        self.editSourceButton.setObjectName(_fromUtf8("editSourceButton"))
        self.gridLayout_7.addWidget(self.editSourceButton, 2, 2, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_7, 2, 0, 1, 1)
        self.gridLayout_10 = QtGui.QGridLayout()
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.sourceContextTypeLabel = QtGui.QLabel(self.cloneGroup)
        self.sourceContextTypeLabel.setObjectName(_fromUtf8("sourceContextTypeLabel"))
        self.gridLayout_10.addWidget(self.sourceContextTypeLabel, 1, 0, 1, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.sourceContextTypeEdit = QtGui.QLineEdit(self.cloneGroup)
        self.sourceContextTypeEdit.setFrame(True)
        self.sourceContextTypeEdit.setReadOnly(True)
        self.sourceContextTypeEdit.setObjectName(_fromUtf8("sourceContextTypeEdit"))
        self.horizontalLayout_6.addWidget(self.sourceContextTypeEdit)
        self.openSourceContextTool = QtGui.QToolButton(self.cloneGroup)
        self.openSourceContextTool.setEnabled(False)
        self.openSourceContextTool.setText(_fromUtf8(""))
        self.openSourceContextTool.setIcon(icon1)
        self.openSourceContextTool.setObjectName(_fromUtf8("openSourceContextTool"))
        self.horizontalLayout_6.addWidget(self.openSourceContextTool)
        self.gridLayout_10.addLayout(self.horizontalLayout_6, 1, 1, 1, 2)
        self.sourceContextDescriptionEdit = QtGui.QLineEdit(self.cloneGroup)
        self.sourceContextDescriptionEdit.setReadOnly(True)
        self.sourceContextDescriptionEdit.setObjectName(_fromUtf8("sourceContextDescriptionEdit"))
        self.gridLayout_10.addWidget(self.sourceContextDescriptionEdit, 2, 0, 1, 3)
        self.sourceContextLabel = QtGui.QLabel(self.cloneGroup)
        self.sourceContextLabel.setObjectName(_fromUtf8("sourceContextLabel"))
        self.gridLayout_10.addWidget(self.sourceContextLabel, 0, 0, 1, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.sourceContextSpin = QtGui.QSpinBox(self.cloneGroup)
        self.sourceContextSpin.setMaximum(99999)
        self.sourceContextSpin.setObjectName(_fromUtf8("sourceContextSpin"))
        self.horizontalLayout_7.addWidget(self.sourceContextSpin)
        self.findSourceTool = QtGui.QToolButton(self.cloneGroup)
        self.findSourceTool.setIcon(icon)
        self.findSourceTool.setObjectName(_fromUtf8("findSourceTool"))
        self.horizontalLayout_7.addWidget(self.findSourceTool)
        self.gridLayout_10.addLayout(self.horizontalLayout_7, 0, 1, 1, 2)
        self.gridLayout_8.addLayout(self.gridLayout_10, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.cloneGroup, 1, 0, 1, 1)
        self.editContexLabel.setBuddy(self.editContextButton)
        self.siteCodeLabel.setBuddy(self.siteCodeCombo)
        self.cloneSourceLabel.setBuddy(self.cloneSourceButton)
        self.copySourceLabel.setBuddy(self.copySourceButton)
        self.editSourceLabel.setBuddy(self.editSourceButton)
        self.sourceContextLabel.setBuddy(self.sourceContextSpin)

        self.retranslateUi(SchematicWidget)
        QtCore.QMetaObject.connectSlotsByName(SchematicWidget)
        SchematicWidget.setTabOrder(self.cloneSourceButton, self.copySourceButton)
        SchematicWidget.setTabOrder(self.copySourceButton, self.editSourceButton)
        SchematicWidget.setTabOrder(self.editSourceButton, self.siteCodeCombo)

    def retranslateUi(self, SchematicWidget):
        SchematicWidget.setWindowTitle(_translate("SchematicWidget", "Form", None))
        self.checkGroup.setTitle(_translate("SchematicWidget", "Check Context", None))
        self.schematicLabel.setText(_translate("SchematicWidget", "Has Schematic:", None))
        self.featureDataLabel.setText(_translate("SchematicWidget", "Has Features:", None))
        self.sectionSchematicLabel.setText(_translate("SchematicWidget", "Has Section Schematic:", None))
        self.resetLabel.setText(_translate("SchematicWidget", "Reset Check:", None))
        self.editContexLabel.setText(_translate("SchematicWidget", "Edit Context:", None))
        self.deleteSectionLabel.setText(_translate("SchematicWidget", "Delete Section Schematic:", None))
        self.deleteSectionButton.setText(_translate("SchematicWidget", "Del", None))
        self.editContextButton.setText(_translate("SchematicWidget", "Edit", None))
        self.resetButton.setText(_translate("SchematicWidget", "Reset", None))
        self.contextSpin.setToolTip(_translate("SchematicWidget", "<html><head/><body><p>Enter Context to find</p></body></html>", None))
        self.findContextTool.setToolTip(_translate("SchematicWidget", "<html><head/><body><p>Pan to Context</p></body></html>", None))
        self.findContextTool.setText(_translate("SchematicWidget", "...", None))
        self.siteCodeLabel.setText(_translate("SchematicWidget", "Site Code:", None))
        self.arkDataLabel.setText(_translate("SchematicWidget", "Type:", None))
        self.contextLabel.setText(_translate("SchematicWidget", "Context:", None))
        self.firstContextTool.setToolTip(_translate("SchematicWidget", "Go First Context", None))
        self.firstContextTool.setText(_translate("SchematicWidget", "...", None))
        self.prevMissingTool.setToolTip(_translate("SchematicWidget", "Go Previous Missing Schematic", None))
        self.prevMissingTool.setText(_translate("SchematicWidget", "...", None))
        self.prevContextTool.setToolTip(_translate("SchematicWidget", "Go Previous Context", None))
        self.prevContextTool.setText(_translate("SchematicWidget", "...", None))
        self.nextContextTool.setToolTip(_translate("SchematicWidget", "Go Next Context", None))
        self.nextContextTool.setText(_translate("SchematicWidget", "...", None))
        self.nextMissingTool.setToolTip(_translate("SchematicWidget", "Go Next Missing Schematic", None))
        self.nextMissingTool.setText(_translate("SchematicWidget", "...", None))
        self.lastContextTool.setToolTip(_translate("SchematicWidget", "Go Last Context", None))
        self.lastContextTool.setText(_translate("SchematicWidget", "...", None))
        self.cloneGroup.setTitle(_translate("SchematicWidget", "Source Schematic", None))
        self.sourceSchematicLabel.setText(_translate("SchematicWidget", "Has Schematic:", None))
        self.sourceFeatureDataLabel.setText(_translate("SchematicWidget", "Has Features:", None))
        self.cloneSourceLabel.setText(_translate("SchematicWidget", "Clone and Save Schematic:", None))
        self.cloneSourceButton.setText(_translate("SchematicWidget", "Clone", None))
        self.copySourceLabel.setText(_translate("SchematicWidget", "Copy and Edit Schematic:", None))
        self.copySourceButton.setText(_translate("SchematicWidget", "Copy", None))
        self.editSourceLabel.setText(_translate("SchematicWidget", "Edit Source Context:", None))
        self.editSourceButton.setText(_translate("SchematicWidget", "Edit", None))
        self.sourceContextTypeLabel.setText(_translate("SchematicWidget", "Type:", None))
        self.sourceContextLabel.setText(_translate("SchematicWidget", "Context:", None))
        self.sourceContextSpin.setToolTip(_translate("SchematicWidget", "<html><head/><body><p>Enter Source Context to find</p></body></html>", None))
        self.findSourceTool.setToolTip(_translate("SchematicWidget", "<html><head/><body><p>Pan to Context</p></body></html>", None))
        self.findSourceTool.setText(_translate("SchematicWidget", "...", None))

import resources_rc
