"""The controllers for all the views"""

from julesTk import controller
from julesTk.utils.observe import Observer
from model import DeviceModel
from view import *

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class MainController(controller.ViewController):

    VIEW_CLASS = MainView

    def _prepare(self):
        super(MainController, self)._prepare()
        # add device controller
        if not self.application.has_controller("device"):
            c = DeviceController(self).prepare()
            self.application.add_controller("device", c)
        # add gpio controller
        if not self.application.has_controller("gpio"):
            c = GPIOController(self).prepare()
            self.application.add_controller("gpio", c)

    def _start(self):
        super(MainController, self)._start()
        self.application.get_controller("device").start()


# noinspection PyUnresolvedReferences
class DeviceController(controller.ViewController):
    """Manages a list of devices"""

    VIEW_CLASS = DeviceView

    @property
    def devices(self):
        return DeviceModel.get_devices()

    def _start(self):
        self.application.get_controller("gpio").view.hide()
        super(DeviceController, self)._start()
        self.load_devices()

    def load_devices(self):
        DeviceModel.find_devices()
        self.view.refresh_devices()

    def get_device(self, idx):
        if idx < 0 or idx > len(self.devices):
            raise ValueError("Invalid index: %s" % idx)
        return self.devices[idx]

    def load_gpio(self, selection):
        # get device
        model = self.get_device(selection)
        # hide view
        self.view.hide()
        # load device model
        self.application.get_controller("gpio").start(model)


# noinspection PyUnresolvedReferences
class GPIOController(controller.Controller, Observer):
    """Manages the gpio settings"""

    VIEW_CLASS = GPIOView

    def start(self, model=None):
        if not self._configured:
            self.prepare()
        return self._start(model)

    def _start(self, model=None):
        if not isinstance(model, DeviceModel):
            raise ValueError("Invalid Model")
        self._model = model
        self.model.register_observer(self)
        self.application.get_controller("device").view.hide()
        super(GPIOController, self).start()
        # now update
        self.model.update()

    def set_gpio(self, gpio, state):
        self.model.set_gpio(gpio, state)

    def update(self, observable):
        if isinstance(observable, DeviceModel):
            for idx, v in enumerate(self.model.data):
                self.view.set_gpio(idx, v)

