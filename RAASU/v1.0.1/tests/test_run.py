from escpos.printer import Usb
from datetime import datetime

# =========================
# TECH CLA58 Printer Config
# =========================
VENDOR_ID = 0x6868  # Your printer's Vendor ID
PRODUCT_ID = 0x0200  # Your printer's Product ID

try:
    # Connect to USB printer
    p = Usb(VENDOR_ID, PRODUCT_ID)

    # ==============
    # Receipt Header
    # ==============
    p.set(align='center', bold=True, height=2, width=2)
    p.text("Ra'asu venture\n")
    p.set(align='center', bold=False, height=1, width=1)
    p.text("Ceramics\n Ajaokuta\n 08083148289 - 08055216238")
    p.text("-----------------------------\n")

    # ============
    # Items
    # ============
    items = [
        ("Apple", 2, 150),   # (item, qty, price)
        ("Orange", 1, 100),
        ("Banana", 5, 50),
    ]

    total = 0
    for item, qty, price in items:
        line = f"{item:<10} {qty:>2} x {price:<4} = {qty*price}"
        p.text(line + "\n")
        total += qty * price

    p.text("-----------------------------\n")
    p.set(bold=True)
    p.text(f"TOTAL: {total}\n")
    p.set(bold=False)

    # ============
    # Footer
    # ============
    p.text("-----------------------------\n")
    p.text(f"Date: {datetime.now().strftime('%y-%m-%d %H:%M:%S')}\n")
    p.text("Thanks for your patronage!\n")
    p.text("\n\n")  # Add some spacing

    # Cut the receipt
    p.cut()

    print("Receipt printed successfully!")

except Exception as e:
    print("Error:", e)