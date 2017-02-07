from julesTk import view


class MainView(view.ViewSet):
    """Main view set"""

    def show(self):
        self.tkraise()

    def setup(self):
        # resize parent with window
        self.configure_row(self.parent, 0)
        self.configure_column(self.parent, 0)
        # resize frame with window
        self.configure_grid(self)
        self.configure_column(self, 0)
        self.configure_row(self, 0)

    def hide(self):
        pass


# noinspection PyUnresolvedReferences
class DeviceView(view.View):
    """View showing the list of devices"""

    @property
    def title(self):
        return self.get_variable("title").get()

    @title.setter
    def title(self, msg):
        self.get_variable("title").set(msg)

    @property
    def status(self):
        return self.get_variable("status").get()

    @status.setter
    def status(self, msg):
        self.get_variable("status").set(msg)

    def setup(self):
        self.configure_column(self, [0, 1, 2], uniform="foo")
        self.configure_row(self, [0, 1, 2])
        # add title
        var = self.add_variable("title", view.tk.StringVar())
        lbt = view.ttk.Label(self, textvariable=var)
        self.add_widget("title", lbt)
        self.configure_grid(lbt, row=0, column=0, columnspan=3, pady=10)
        # add list box
        lb = view.tk.Listbox(self, selectmode=view.tk.SINGLE)
        self.add_widget("devices", lb)
        self.configure_grid(lb, row=1, column=0, columnspan=3)
        # add close button
        btc = view.ttk.Button(self, text="Close", command=self.process_close)
        self.add_widget("close", btc)
        btc.grid(row=2, column=0)
        # add refresh button
        btr = view.ttk.Button(self, text="Refresh", command=self.refresh_devices)
        self.add_widget("refresh", btr)
        btr.grid(row=2, column=1)
        # add ok button
        bto = view.ttk.Button(self, text="Select", command=self.process_ok)
        self.add_widget("ok", bto)
        bto.grid(row=2, column=2)
        # add statusbar
        var = self.add_variable("status", view.tk.StringVar())
        lbs = view.ttk.Label(self, textvariable=var, relief=view.tk.SUNKEN)
        self.add_widget("status", lbs)
        self.configure_grid(lbs, row=3, column=0, columnspan=3)
        self.title = "Select a device"
        self.status = ""

    def show(self):
        super(DeviceView, self).show()
        self.configure_grid(self)
        self.refresh_devices()

    def refresh_devices(self):
        """updates the listbox to match the dictionary of devices"""
        lb = self.get_widget("devices")
        """:type: Tkinter.ListBox or tkinter.ListBox"""
        lb.delete(0, view.tk.END)
        """:type: list[usb.core.Device]"""
        for model in self.controller.devices:
            device = model.device
            msg = "BUS {}, Address {}".format(device.bus, device.address)
            lb.insert(view.tk.END, msg)

    def process_close(self):
        self.controller.application.stop()

    def process_ok(self):
        self.controller.load_gpio()


# noinspection PyUnresolvedReferences
class GPIOView(view.View):
    """View showing all the relays"""

    MAX_GPIO_INDEX = 8

    @property
    def status(self):
        return self.get_variable("status").get()

    @status.setter
    def status(self, msg):
        self.get_variable("status").set(msg)

    def setup(self):
        self.configure_grid(self)
        self.configure_column(self, 0)
        self.configure_row(self, 0)
        lbt = view.ttk.Label(self, text="Toggle GPIO Pins")
        self.add_widget("title", lbt)
        self.configure_grid(lbt, row=0, column=0, pady=10)
        frm = view.ttk.Frame(self)
        self.add_widget("frm_gpio", frm)
        self.configure_grid(frm, row=1, column=0)
        self.setup_gpio_frame(frm)
        var = self.add_variable("status", view.tk.StringVar())
        lbs = view.ttk.Label(self, textvariable=var, relief=view.tk.SUNKEN)
        self.add_widget("status", lbs)
        self.configure_grid(lbs, row=2, column=0, pady=10)
        self.status = ""

    def setup_gpio_frame(self, parent):
        self.configure_column(parent, [0, 1, 2], uniform="foo")
        self.configure_row(parent, [0, 1, 2])
        # add GPIO checkboxes
        for i in range(self.MAX_GPIO_INDEX):
            frm = view.ttk.Frame(parent)
            self.add_widget("gpio_frm_%s" % i, frm)
            frm.grid(row=i % 4, column=i // 4)
            self.setup_gpio(i, frm)

    def setup_gpio(self, idx, parent):
        var = view.tk.IntVar(self)
        self.add_variable("gpio_%s" % idx, var)
        cb = view.ttk.Checkbutton(
            parent, variable=var, command=lambda: self.toggle_gpio(idx))
        self.add_widget("gpio_cb_%s" % idx, cb)
        self.configure_grid(cb, row=0, column=0)
        lb = view.ttk.Label(parent, text="GPIO %s" % idx)
        self.add_widget("gpio_lb_%s" % idx, lb)
        self.configure_grid(lb, row=0, column=1)

    def show(self):
        super(GPIOView, self).show()
        self.configure_grid(self)

    def toggle_gpio(self, gpio):
        v = self.get_gpio(gpio)
        self.status = "Set GPIO %s to %s" % (gpio, v)
        self.controller.set_gpio(gpio, v)

    def get_gpio(self, gpio):
        if gpio < 0 or gpio >= self.MAX_GPIO_INDEX:
            raise ValueError("Invalid GPIO Value: %s" % gpio)
        v = self.get_variable("gpio_%s" % gpio).get()
        return v == 1

    def set_gpio(self, gpio, state):
        """Sets the GPIO Checkbox

        :param gpio: Index of GPIO To set
        :type gpio: int
        :param state: State to set GPIO Checkbox to
        :type state: bool
        :return:
        :rtype:
        """
        if gpio < 0 or gpio >= self.MAX_GPIO_INDEX:
            raise ValueError("Invalid GPIO Value: %s" % gpio)
        self.get_variable("gpio_%s" % gpio).set(1 if state else 0)
