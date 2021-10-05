import sys

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QGridLayout, QDialogButtonBox, QTreeWidget, \
    QFormLayout, QFileDialog, QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget


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
        # dlg.setFilter("Text files (*.txt)")

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            print(filenames)
            for file in filenames:
                f = open(file, 'r')
                with f:
                    data = f.read()
                    self.data[file] = data


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
