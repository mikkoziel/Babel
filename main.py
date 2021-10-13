import sys

from PyQt5.QtWidgets import QApplication

from babel_view import BabelView


def main():
    """Main function."""
    babel = QApplication(sys.argv)
    view = BabelView()
    view.show()
    # model = evaluateExpression
    # PyCalcCtrl(model=model, view=view)
    sys.exit(babel.exec_())


if __name__ == '__main__':
    main()
