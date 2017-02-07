
from julesTk.app import Application
from controller import MainController


class CP210xControlApplication(Application):

    def setup(self):
        self.add_controller("main", MainController(self))
        self.get_controller("main").setup()
        self.wm_title("CP210x Control")

    def start(self):
        self.get_controller("main").start()


def start_app():
    app = CP210xControlApplication()
    app.run()
