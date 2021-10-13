import json
import os
import collections.abc
from copy import deepcopy

from PyQt5.QtWidgets import QVBoxLayout, QMainWindow, QGridLayout, QDialogButtonBox, QTreeWidget, \
    QFormLayout, QFileDialog, QPushButton, QTreeWidgetItem, QLineEdit, QHBoxLayout
# from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget

from babel_controller import BabelController


class BabelView(QMainWindow):
    """PyCalc's View (GUI)."""
    def __init__(self):
        """View initializer."""
        super().__init__()
        self.setWindowTitle('Babel')
        self.setGeometry(0, 0, 800, 600)

        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.ctrl = BabelController()

        self.data = {}
        self.languages = []
        self.directory = ""
        self.activeTreeItem = None
        self._createCentralWidget()

    def _createCentralWidget(self):
        self._createBttnsLayout()
        self._createTreeWidget()
        self._createFormLayout()

    def _createBttnsLayout(self):
        bttns = QHBoxLayout()

        self.btn1 = QPushButton("Choose files")
        self.btn1.setMaximumWidth(100)
        self.btn1.clicked.connect(self.getFiles)
        bttns.addWidget(self.btn1)

        self.btn2 = QPushButton("Save files")
        self.btn2.setMaximumWidth(100)
        self.btn2.clicked.connect(self.saveFiles)
        bttns.addWidget(self.btn2)

        self.generalLayout.addLayout(bttns, 0, 0, 1, 2)

    def _createTreeWidget(self):
        self.tree = QTreeWidget()
        self.tree.setMaximumWidth(400)
        self.tree.setHeaderLabels(("Names",))
        self.tree.itemActivated.connect(self.treeItemClicked)
        self.generalLayout.addWidget(self.tree, 1, 0)

    def _createFormLayout(self):
        self.form = QFormLayout()
        self.generalLayout.addLayout(self.form, 1, 1)

    def getFiles(self):
        dlg = QFileDialog(directory=self.directory)
        dlg.setFileMode(QFileDialog.ExistingFiles)

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.directory = filenames[0]
            self.data = self.ctrl.read_data_from_file_chooser(filenames)
            self.languages = self.data.keys()
            self.populateTreeWidget()

    def populateTreeWidget(self):
        items = self.ctrl.create_item_tree(self.data)
        self.tree.insertTopLevelItems(0, items)

    def treeItemClicked(self, item, column_no):
        if item.childCount() == 0:
            self.activeTreeItem = item
            dict_path = self.ctrl.get_dict_path(item)

            translations = {}
            for key in self.languages:
                translations[key] = self.ctrl.getTranslation(self.data[key], deepcopy(dict_path))

            self.clearLayout(self.form)
            for key in self.languages:
                # for key, value in translations.items():
                editLine = QLineEdit()
                editLine.setText(translations[key])
                self.form.addRow(key, editLine)

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def saveFiles(self):
        self.ctrl.save_files(self.data, self.form, self.activeTreeItem)
