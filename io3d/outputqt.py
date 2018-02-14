import logging

logger = logging.getLogger(__name__)
from PyQt4.QtGui import QGridLayout, QLabel, QPushButton, QLineEdit, QCheckBox, QFileDialog
from PyQt4 import QtGui
import os.path as op


class SelectOutputPathWidget(QtGui.QWidget):
    def __init__(self, path=None, widget_label=None, save_dialog_message="Save file",
                 save_dialog_filter="", *args, **kwargs):
        super(SelectOutputPathWidget, self).__init__()

        self.ui_slab = {}
        self.output_path = ""

        self.mainLayout = QGridLayout(self)
        # self.init_slab(*args, **kwargs)
        self.save_dialog_message = save_dialog_message
        self.save_dialog_filter = save_dialog_filter
        self.widget_label = widget_label
        self.init_ui()

        if path is not None:
            self.set_path(path)

    def set_path(self, path):
        dirname, filename = op.split(path)
        self.output_path = path

        self.ui_buttons["dirname"].setText(dirname)
        self.ui_buttons["filename"].setText(filename)

        # self._filename = filename
        # self._dirname = dirname

    def get_dirname(self):
        dirname = str(self.ui_buttons["dirname"].text())
        return dirname

    def get_filename(self):
        filename = str(self.ui_buttons["filename"].text())
        return filename

    def get_path(self):
        dirname = self.get_dirname()
        filename = self.get_filename()
        path = op.join(dirname, filename)
        return path

    def action_select_path(self):
        pth = op.expanduser(self.get_path())
        self.set_path(str(QFileDialog.getSaveFileName(
            self,
            self.save_dialog_message,
            pth,
            filter=self.save_dialog_filter
        )))


    # def update_ui(self):
    #     keyword = "dirname"
    #     self.ui_buttons[keyword].setText(str(self._dirname))
    #     keyword = "filename"
    #     self.ui_buttons[keyword].setText(str(self._filename))


    def init_ui(self):

        # self.mainLayout = QGridLayout(self)

        self._row = 0
        self.ui_buttons = {}

        self._row += 1
        if self.widget_label is not None:
            keyword = "label"
            vtk_fileQLabel= QLabel(self.widget_label)
            self.mainLayout.addWidget(vtk_fileQLabel, self._row, 2)
            print("-----------------")


        keyword = "dirname"
        self.ui_buttons[keyword] = QLineEdit()
        # self.ui_buttons[keyword].setText(str(self.output_path))
        self.mainLayout.addWidget(self.ui_buttons[keyword], self._row + 1, 2, 1, 2)
        vtk_fileQLabel= QLabel("dir")
        self.mainLayout.addWidget(vtk_fileQLabel, self._row + 1, 1)
        keyword = "filename"
        self.ui_buttons[keyword] = QLineEdit()
        # self.ui_buttons[keyword].setText(str(self.output_path))
        self.mainLayout.addWidget(self.ui_buttons[keyword], self._row + 2, 2)
        vtk_fileQLabel= QLabel("file")
        self.mainLayout.addWidget(vtk_fileQLabel, self._row + 2, 1)
        keyword = "path_button"
        self.ui_buttons[keyword] = QPushButton("Select", self)
        self.ui_buttons[keyword].clicked.connect(self.action_select_path)
        self.mainLayout.addWidget(self.ui_buttons[keyword], self._row + 2, 3, 1, 1)

        # self.update_ui()

