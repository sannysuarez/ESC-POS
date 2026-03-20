import usb.core

devices = usb.core.find(find_all=True)

for d in devices:
    print(hex(d.idVendor), hex(d.idProduct))
