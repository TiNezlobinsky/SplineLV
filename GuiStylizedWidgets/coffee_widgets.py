from PyQt5 import QtCore, QtWidgets

color_1 = "216, 218, 162"
color_2 = "134, 172, 176"
color_3 = "130, 113, 26"
color_4 = "232, 140, 90"
color_5 = "180, 212, 76"
color_6 = "196, 141, 195"
color_7 = "219, 189, 217"
back_rgb = color_1


class CoffeeButton(QtWidgets.QPushButton):
    _buttons_style_sheet = "background: rgb(%s);" \
                           "font-size: 14px;" \
                           "border-radius: 8px;" \
                           "border: 2px groove grey;" \
                           "min-height: 1.3em;" % back_rgb

    def __init__(self, title, parent=None):
        QtWidgets.QPushButton.__init__(self, title, parent)
        self.setStyleSheet(self._buttons_style_sheet)


class CoffeeColoredButton(CoffeeButton):
    def __init__(self, color, title, parent=None):
        CoffeeButton.__init__(self, title, parent)
        self._selected_buttons_style_sheet = "background: rgb(%s);" \
                                             "font-size: 14px;" \
                                             "border-radius: 8px;" \
                                             "border: 2px groove %s;" \
                                             "min-height: 1.3em;" % (back_rgb, color)
        self.clicked.connect(self._switch_state)
        self._button_selected = False

    def change_color(self, color):
        self._selected_buttons_style_sheet = "background: rgb(%s);" \
                                             "font-size: 14px;" \
                                             "border-radius: 8px;" \
                                             "border: 2px groove %s;" \
                                             "min-height: 1.3em;" % (back_rgb, color)

    def selected_On(self):
        self.setStyleSheet(self._selected_buttons_style_sheet)
        self._button_selected = True

    def default_On(self):
        self.setStyleSheet(self._buttons_style_sheet)
        self._button_selected = False

    def check_state(self):
        return self._button_selected

    def _switch_state(self):
        if self._button_selected:
            self.default_On()
        else:
            self.selected_On()


class CoffeeColoredRGBButton(CoffeeButton):
    def __init__(self, color_rgb, title, parent=None):
        CoffeeButton.__init__(self, title, parent)
        self._selected_buttons_style_sheet = "background: rgb(%s);" \
                                             "font-size: 14px;" \
                                             "border-radius: 8px;" \
                                             "border: 2px groove rgb(%s);" \
                                             "min-height: 1.3em;" % (back_rgb, color_rgb)
        self.clicked.connect(self._switch_state)
        self._button_selected = False

    def change_color(self, color):
        self._selected_buttons_style_sheet = "background: rgb(%s);" \
                                             "font-size: 14px;" \
                                             "border-radius: 8px;" \
                                             "border: 2px groove %s;" \
                                             "min-height: 1.3em;" % (back_rgb, color)
    def selected_On(self):
        self.setStyleSheet(self._selected_buttons_style_sheet)
        self._button_selected = True

    def default_On(self):
        self.setStyleSheet(self._buttons_style_sheet)
        self._button_selected = False

    def check_state(self):
        return self._button_selected

    def _switch_state(self):
        if self._button_selected:
            self.default_On()
        else:
            self.selected_On()


class CoffeeLineEdit(QtWidgets.QLineEdit):
    _lines_style_sheet = "border-radius: 8px;" \
                         "border: 2px groove grey;" \
                         "font-size: 14px;" \
                         "min-height: 1.3em;"

    def __init__(self, parent=None):
        QtWidgets.QLineEdit.__init__(self, parent)
        self.setStyleSheet(self._lines_style_sheet)


class CoffeeColoredLine(QtWidgets.QLineEdit):
    def __init__(self, color, parent=None):
        QtWidgets.QLineEdit.__init__(self, parent)
        self._lines_style_sheet = "border-radius: 8px;" \
                                  "border: 2px groove %s;" \
                                  "font-size: 14px;" \
                                  "max-height: 1.3em;" % color
        self.setStyleSheet(self._lines_style_sheet)
        self.setReadOnly(True)


class CoffeeFullColoredRGBLine(QtWidgets.QLineEdit):
    def __init__(self, rgb_string, parent=None):
        QtWidgets.QLineEdit.__init__(self, parent)
        self._lines_style_sheet = "background: rgb(%s);" \
                                  "border-radius: 9px;" \
                                  "font-size: 14px;" \
                                  "max-height: 1.0em;" % rgb_string
        self.setStyleSheet(self._lines_style_sheet)
        self.setReadOnly(True)

    def change_color(self, rgb_string):
        self._lines_style_sheet = "background: rgb(%s);" \
                                  "border-radius: 9px;" \
                                  "max-height: 1.0em;" % rgb_string
        self.setStyleSheet(self._lines_style_sheet)


class CoffeeListWidget(QtWidgets.QListWidget):
    _listwidget_style_sheet = "border-radius: 8px;" \
                              "font-size: 14px;" \
                              "border: 2px groove grey;" \
                              "min-height: 1.3em;"

    def __init__(self, parent=None):
        QtWidgets.QListWidget.__init__(self, parent)
        self.setStyleSheet(self._listwidget_style_sheet)
