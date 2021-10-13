import json
import os
import sys
import collections.abc

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QGridLayout, QDialogButtonBox, QTreeWidget, \
    QFormLayout, QFileDialog, QPushButton, QTreeWidgetItem
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget

from functools import reduce  # forward compatibility for Python 3
import operator


class ApplicationData:

    def getFromDict(self, data_dict, map_list):
        return reduce(operator.getitem, map_list, data_dict)

    def setInDict(self, data_dict, map_list, value):
        self.getFromDict(data_dict, map_list[:-1])[map_list[-1]] = value


class BabelUi(QMainWindow):
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

        self.data = {}
        self.languages = []
        self._createCentralWidget()
        # self._createDisplay()
        # self._createButtons()

    def _createCentralWidget(self):
        bttns = QVBoxLayout()
        # bttns.setFixedHeight(40)
        self.btn1 = QPushButton("Choose files")
        self.btn1.setMaximumWidth(100)
        self.btn1.clicked.connect(self.getFiles)
        bttns.addWidget(self.btn1)
        # bttns.setStandardButtons(
        #     QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.generalLayout.addLayout(bttns, 0, 0, 1, 2)

        self.tree = QTreeWidget()
        self.tree.setMaximumWidth(400)
        self.generalLayout.addWidget(self.tree, 1, 0)

        self.form = QFormLayout()
        self.generalLayout.addLayout(self.form, 1, 1)

    def getFiles(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            print(filenames)
            data = {}
            for file in filenames:
                f = open(file, 'r')
                with f:
                    data[os.path.basename(file)] = json.loads(f.read())

            for key_dict, value_dict in data.items():
                self.languages.append(key_dict)
                self.data = self.update_(self.data, value_dict)

                # for key, value in value_dict:
                #     self.dict_iter([key], value)
            print(self.data)

    def update_(self, d, u):
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = self.update_(d.get(k, {}), v)
            else:
                x = d.get(k, [])
                x.append(v)
                d[k] = x
        return d

    def populateTreeWidget(self):
        items = []
        for key, values in self.data.items():

            item = QTreeWidgetItem([key])
            for value in values:
                # ext = value.split(".")[-1].upper()
                child = QTreeWidgetItem([value])
                item.addChild(child)
            items.append(item)

        self.tree.insertTopLevelItems(0, items)


def main():
    """Main function."""
    babel = QApplication(sys.argv)
    view = BabelUi()
    view.show()
    # model = evaluateExpression
    # PyCalcCtrl(model=model, view=view)
    sys.exit(babel.exec_())


if __name__ == '__main__':
    main()
