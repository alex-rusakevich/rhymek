import os
import sys

from jinja2 import Template
from PySide6 import QtGui
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtGui import QFont, QPalette
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication

from rhymek.processors import LANG_PROCESSORS


def render_and_set_words_html(window, jinja2_global_vars, words=()):
    processors = LANG_PROCESSORS[window.languageComboBox.currentText()]
    word_to_search = window.searchEdit.text().strip()

    results = []
    for proc in processors:
        results += proc(word_to_search)

    results = list(set(results))

    jinja2_template_string = open(os.path.join("ui", "template_words.html"), "r").read()
    template = Template(jinja2_template_string)
    html_template_string = template.render(words=results, **jinja2_global_vars)

    window.webEngineView.page().setHtml(html_template_string)


def render_and_set_hello_html(window, jinja2_global_vars):
    jinja2_template_string = open(os.path.join("ui", "template_hello.html"), "r").read()
    template = Template(jinja2_template_string)
    html_template_string = template.render(**jinja2_global_vars)

    window.webEngineView.page().setHtml(html_template_string)


def search_button_clicked(window, jinja2_global_vars):
    render_and_set_words_html(window, jinja2_global_vars, [])


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

    window.browser = QWebEngineView()
    window.setWindowIcon(QtGui.QIcon(os.path.join("ui", "favicon.svg")))

    for k, _ in LANG_PROCESSORS.items():
        window.languageComboBox.addItem(k)

    jinja2_global_vars = {
        "system_bg_color": palette.color(QPalette.Base).name(),
        "system_font_color": palette.color(QPalette.Text).name(),
        "font_size": (
            app.font().pointSizeF()
            if (px_size := app.font().pixelSize()) == -1
            else px_size
        ),
        "ending_color": palette.color(QPalette.Highlight).name(),
    }

    render_and_set_hello_html(window, jinja2_global_vars)

    window.searchButton.clicked.connect(
        lambda: search_button_clicked(window, jinja2_global_vars)
    )

    if not window:
        print(loader.errorString())
        sys.exit(-1)

    window.show()

    sys.exit(app.exec())
