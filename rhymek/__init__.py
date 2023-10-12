import os
import sys

from jinja2 import Template
from PySide6 import QtGui
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtGui import QFont, QPalette
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication


def run_app():
    app = QApplication(sys.argv)

    ui_file_name = "ui/main.ui"
    ui_file = QFile(ui_file_name)

    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)

    loader = QUiLoader()
    window = loader.load(ui_file)
    palette = window.style().standardPalette()
    ui_file.close()

    jinja2_vars = {
        "system_bg_color": palette.color(QPalette.Base).name(),
        "system_font_color": palette.color(QPalette.Text).name(),
        "font_size": (
            app.font().pointSizeF()
            if (px_size := app.font().pixelSize()) == -1
            else px_size
        ),
        "ending_color": palette.color(QPalette.Highlight).name(),
    }

    words = ("Hello",) * 128

    jinja2_template_string = open(os.path.join("ui", "template.html"), "r").read()
    template = Template(jinja2_template_string)
    html_template_string = template.render(words=words, **jinja2_vars)

    window.browser = QWebEngineView()
    window.setWindowIcon(QtGui.QIcon(os.path.join("ui", "favicon.svg")))

    if not window:
        print(loader.errorString())
        sys.exit(-1)

    window.webEngineView.page().setHtml(html_template_string)
    window.show()

    sys.exit(app.exec())
