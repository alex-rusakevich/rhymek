import os
import signal
import sys

from jinja2 import Environment, FileSystemLoader
from PySide6 import QtGui
from PySide6.QtCore import QFile, QIODevice, QTimer
from PySide6.QtGui import QPalette
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication

from rhymek.processors import LANG_PROCESSORS

jinja2_global_vars = {}


def render_to_webview(window, jinja2_vars, template_name):
    env = Environment(loader=FileSystemLoader("ui"))
    template = env.get_template("base_layout.html")

    jinja2_template_string = open(os.path.join("ui", template_name), "r").read()
    template = env.from_string(jinja2_template_string)
    html_template_string = template.render(**jinja2_vars)

    window.webEngineView.page().setHtml(html_template_string)


def render_and_set_words_html(window):
    processor = LANG_PROCESSORS[window.languageComboBox.currentText()]
    word_to_search = window.searchEdit.text().strip()

    results = processor.process(word_to_search)

    render_to_webview(
        window, {**jinja2_global_vars, "words": results}, "template_words.html"
    )


def search_button_clicked(window):
    render_and_set_words_html(window)


def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    sys.exit(0)


signal.signal(signal.SIGINT, keyboardInterruptHandler)


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

    global jinja2_global_vars

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

    render_to_webview(window, jinja2_global_vars, "template_hello.html")

    window.searchButton.clicked.connect(lambda: search_button_clicked(window))
    window.searchEdit.returnPressed.connect(lambda: search_button_clicked(window))

    if not window:
        print(loader.errorString())
        sys.exit(-1)

    window.show()

    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(512)

    sys.exit(app.exec())
