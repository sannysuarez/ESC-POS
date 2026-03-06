from escpos.printer import Serial

printer = Serial(devfile='/dev/rfcomm0', baudrate=9600)
printer.text("Hello Bluetooth\n")
printer.text("Hello Bluetooth\n")
printer.text("Hello Bluetooth\n")
printer.text("Hello Bluetooth\n")
printer.text("Hello Bluetooth\n")
printer.text("Hello Bluetooth\n")
printer.cut()