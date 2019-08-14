"""Application entry point"""
from julesTk.app import Application
from .controller import MainController

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class CP210xControlApplication(Application):

    def _prepare(self):
        self.add_controller("main", MainController(self))
        self.root.title("CP210x Control")

    @property
    def main(self):
        return self.get_controller("main")

    def _start(self):
        self.main.start()


def start_app():
    app = CP210xControlApplication()
    app.run()
