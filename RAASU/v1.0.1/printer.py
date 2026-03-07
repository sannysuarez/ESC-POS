from escpos.printer import Usb
import usb.core
from datetime import datetime


LINE_WIDTH = 32   # 58mm printers typically support 32 chars


def center(text):
    return text.center(LINE_WIDTH)


def line():
    return "-" * LINE_WIDTH


def detect_printer():

    PRINTER_VENDOR_ID = 0x6868
    PRINTER_PRODUCT_ID = 0x0200

    dev = usb.core.find(idVendor=PRINTER_VENDOR_ID, idProduct=PRINTER_PRODUCT_ID)

    if dev is None:
        return None, None

    return PRINTER_VENDOR_ID, PRINTER_PRODUCT_ID



def print_invoice(data):

    vendor, product = detect_printer()

    if vendor is None:
        raise Exception("Printer not detected")

    try:

        p = Usb(vendor, product, 0)

        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        def print_copy(copy_type):

            p._raw(b'\x1b\x40')  # reset printer
            
            p.set(align='center', bold=True, width=2, height=2)
            p.text("RA'ASU VENTURES\n")

            p.set(align='center', font='b', bold=False, width=1, height=1)
            p.text("Ceramics, trailer park\n")
            p.text("Ajaokuta\n")
            p.set(font='a')
            p.text("08065808288 - 08080626221\n")

            p.set(align='left')
            p.text(line() + "\n")

            p.text(f"***{copy_type}'s COPY***\n")
            p.text(f"Invoice: {data['invoice_no']}\n")
            p.text(f"Customer: {data['customer_name']}\n")
            p.text(f"Date: {now}\n")

            p.text(line() + "\n")
            p.text("Item        Qty  Price Total\n")

            for item in data["items"]:

                name = item["name"][:10].ljust(10)
                qty = str(item["qty"]).rjust(3)
                price = str(item["unit_price"]).rjust(5)
                total = str(item["qty"] * item["unit_price"]).rjust(5)

                p.text(f"{name} {qty} {price} {total}\n")

            p.text(line() + "\n")

            p.text(f"TOTAL: {data['total']:,}\n")
            p.text(f"Cashier: {data['cashier']}\n")

            p.text(line() + "\n")

            p.set(align='center')
            p.text("Ramadan Kareem!\n\n")
            p.set(align='center', font='b')
            p.text("Developer:\n")
            p.text("sanni.com.ng\n")
            p.text("v1.0.1\n")

            p.cut()

        # Print two copies
        print_copy("Customer")
        print_copy("Cashier")

    except Exception as e:
        raise Exception(str(e))