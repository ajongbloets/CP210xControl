=============
CP210xControl
=============

A Simple GUI to the CP210x USB to UART Bridge of Silicon Labs

Tested with the Silicon Labs CP2104 chip on a `Conrad Relay Board`_.

Requirements
------------

* *tkinter*
* *ttk*
* `julesTk`_
* `pyUSB`_
* `Silicon Labs`_ VCP Driver

Installation
------------

1. Install the VCP Driver from `Silicon Labs`_
2. Install the packages via pip

.. code-block:: bash

	# install julesTk dependency
	pip install git+https://github.com/jjongbloets/julesTk/master
	# install CP210xControl
	pip install git+https://github.com/jjongbloets/CP210xControl/master

Running
-------

Upon installation, a small console script is generated. This script can be executed from the command-line::

	CP210xControl

Or via the python console

.. code-block:: python

	from CP210xControl import start_app
	start_app()


.. _julesTk: https://github.com/jjongbloets/julesTk
.. _pyUSB: https://github.com/walac/pyusb
.. _Silicon Labs: http://www.silabs.com/products/mcu/Pages/USBtoUARTBridgeVCPDrivers.aspx
.. _Conrad Relay Board: https://www.conrad.nl/nl/conrad-components-393905-relaiskaart-module-5-vdc-393905.html
