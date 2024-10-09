import sys

from fbs_runtime import PUBLIC_SETTINGS
from qtpy.QtCore import QObject
from qtpy.QtWidgets import QMessageBox, QWidget


class QAboutDialog(QObject):
    def __init__(self, parent: QWidget):
        super().__init__()
        self._parent = parent

    def show(self):
        """Build and show the about window"""
        version = PUBLIC_SETTINGS["full_version"]
        author = PUBLIC_SETTINGS["author"]
        environment = PUBLIC_SETTINGS["environment"]
        copyright = PUBLIC_SETTINGS["copyright"]
        app_name = PUBLIC_SETTINGS["app_name"]

        text = f"""<center>
                    <h1>{app_name}</h1>
                    </center>
                    <p>Version: {version}<br/>
                    Author: {author}<br/>
                    Enviroment: {environment}<br/>
                    Copyright &copy; {copyright}<br/>
                    Python: {sys.version}</p>
                    """

        QMessageBox.about(self._parent, "About", text)
