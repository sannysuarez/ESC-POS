# Supports USB & Bluetooth
from escpos.printer import Usb, Serial, Bluetooth
from datetime import datetime

# =========================
# Configuration
# =========================

# USB Config
USB_VENDOR_ID = 0x6868
USB_PRODUCT_ID = 0x0200

# Bluetooth Config (optional)
BLUETOOTH_ADDR = "DC:0D:51:32:FC:F2"  # printer's Bluetooth MAC
BLUETOOTH_PORT = 1  # Usually 1

# =========================
# Sample Items (Dynamic)
# =========================
# Each item: (name, qty, unit_price)
items = [
    ("Apple", 2, 150),
    ("Orange", 1, 100),
    ("Banana", 5, 50),
]

# =========================
# Helper Functions
# =========================
def format_line(name, qty, price, width=32):
    """Format item line for receipt"""
    total = qty * price
    # Adjust spacing
    name_part = f"{name:<12}"
    qty_part = f"{qty:>2} x {price:<4}"
    total_part = f"{total:>6}"
    return f"{name_part}{qty_part}{total_part}"

# =========================
# Connect to Printer
# =========================
printer = None

# Try USB first
try:
    printer = Usb(USB_VENDOR_ID, USB_PRODUCT_ID)
    print("Connected via USB")
except Exception as e:
    print("USB failed:", e)
    # Try Bluetooth
    try:
        printer = Bluetooth(BLUETOOTH_ADDR, port=BLUETOOTH_PORT)
        print("Connected via Bluetooth")
    except Exception as e2:
        print("Bluetooth failed:", e2)

if not printer:
    print("No printer connected. Exiting...")
    exit(1)

# =========================
# Print Header
# =========================
printer.set(align='center', bold=True, width=2, height=2)
printer.text("RA'ASU VENTURES\n")
printer.set(align='center', bold=False, width=1, height=1)
printer.text("New site - Ceramics\nAjaokuta\n")
printer.set(align='center', width=1, height=1)
printer.text("08083148289 - 08055216238")
printer.text("-" * 32 + "\n")

# =========================
# Print Items
# =========================
total_amount = 0
for name, qty, price in items:
    line = format_line(name, qty, price)
    printer.text(line + "\n")
    total_amount += qty * price

printer.text("-" * 32 + "\n")
printer.set(bold=True)
printer.text(f"TOTAL: {total_amount}\n")
printer.set(bold=False)

# =========================
# Footer
# =========================
printer.text("-" * 32 + "\n")
printer.text(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
printer.set(align='center', bold=True)
printer.text("Thanks for your patronage!\n")
printer.set(bold=False)
printer.text("\n\n")

# Cut receipt
printer.cut()

print("Receipt printed successfully!")