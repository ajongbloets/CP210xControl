"""Model the CP210x Device"""

from julesTk import model
import usb.core
from usb.util import CTRL_IN, CTRL_OUT, CTRL_TYPE_VENDOR

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class DeviceModel(model.Model):
    """Models a CP210X Device"""

    MAX_GPIO_INDEX = 8

    CP210X_VENDOR_ID = 0x10c4
    CP210X_PRODUCT_ID = 0xea60

    CP210X_REQUEST_TYPE_READ = CTRL_IN | CTRL_TYPE_VENDOR
    CP210X_REQUEST_TYPE_WRITE = CTRL_OUT | CTRL_TYPE_VENDOR

    CP210X_REQUEST_VENDOR = 0xFF
    CP210X_VALUE_READ_LATCH = 0x00C2
    CP210X_VALUE_WRITE_LATCH = 0x37E1

    _devices = []

    @classmethod
    def find_devices(cls, vendor_id=CP210X_VENDOR_ID, product_id=CP210X_PRODUCT_ID):
        """Finds all devices and creates a Model for them"""
        cls._devices = []
        devices = usb.core.find(idVendor=vendor_id, idProduct=product_id)
        if devices is None:
            devices = []
        devices = list(devices)
        for conf in devices:
            model = cls(conf.device)
            cls._devices.append(model)
        return cls._devices

    @classmethod
    def get_devices(cls):
        return cls._devices

    @classmethod
    def get_device(cls, index):
        if not index >= 0 or index >= len(cls._devices):
            raise KeyError("Invalid device index")
        return cls._devices[index]

    def __init__(self, device):
        if not isinstance(device, usb.core.Device):
            raise ValueError("Invalid device type: %s" % type(device))
        super(DeviceModel, self).__init__()
        self._connected = False
        self._device = device
        self.reset()

    @property
    def device(self):
        return self._device

    def connect(self):
        if self.device is not None:
            self.configure()
            self._connected = True
        return self._connected

    def is_connected(self):
        return self._connected is True

    def configure(self):
        if self.device.is_kernel_driver_active(0):
            cfg = self.device.get_active_configuration()
            intf = cfg[(0, 0)].bInterfaceNumber
            self.device.detach_kernel_driver(intf)
        # set config
        self.device.set_configuration()

    def query(self, request, value, index, length):
        return self.device.ctrl_transfer(
            self.CP210X_REQUEST_TYPE_READ, request, value, index, length
        )

    def write(self, request, value, index, data):
        return self.device.ctrl_transfer(
            self.CP210X_REQUEST_TYPE_WRITE, request, value, index, data
        )

    def reset(self):
        with self.lock:
            self._data = [False for __ in range(self.MAX_GPIO_INDEX)]

    def update(self):
        """Read all GPIO Settings"""
        states = self.get_gpio_states()
        for gpio in range(self.MAX_GPIO_INDEX):
            self._data[gpio] = states[gpio]
        self.notify_observers()

    def set_gpio(self, index, value):
        mask = 1 << index
        values = (0 if value else 1) << index
        msg = (values << 8) | mask
        return self.write(
            self.CP210X_REQUEST_VENDOR, self.CP210X_VALUE_WRITE_LATCH, msg, 0
        )

    def get_gpio_states(self):
        results = []
        response = self.query(
            self.CP210X_REQUEST_VENDOR, self.CP210X_VALUE_READ_LATCH, 0, 1
        )
        if len(response) > 0:
            response = response[0]
        for idx in range(self.MAX_GPIO_INDEX):
            results.append((response & (1 << idx)) == 0)
        return results
