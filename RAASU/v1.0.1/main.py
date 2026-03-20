import sys
import os

# Detect base directory (works for Python and PyInstaller EXE)
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Fix Kivy dependency paths when running from PyInstaller
if getattr(sys, 'frozen', False):
    _MEIPASS = getattr(sys, "_MEIPASS", BASE_DIR)

    os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"
    os.environ["KIVY_HOME"] = os.path.join(_MEIPASS, "kivy_deps")

    sys.path.append(os.path.join(_MEIPASS, "kivy_deps", "angle"))
    sys.path.append(os.path.join(_MEIPASS, "kivy_deps", "glew"))
    sys.path.append(os.path.join(_MEIPASS, "kivy_deps", "sdl2"))
else:
    os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"


from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from datetime import datetime
import random

from models.invoice import Invoice
from excel_handler import save_invoice, get_today_summary
from printer import print_invoice


PRODUCT_NAME = "Fruits Mixed Salad"
UNIT_PRICE = 1500


class RaasuApp(App):

    def build(self):

        kv_path = os.path.join(BASE_DIR, "app.kv")
        self.root = Builder.load_file(kv_path)

        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_once(self.update_today_summary, 0)
        return self.root


    def update_time(self, dt):
        now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        self.root.ids.datetime_label.text = now


    def show_popup(self, title, message):

        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        label = Label(text=message)

        btn = Button(text="OK", size_hint=(1,0.3))

        layout.add_widget(label)
        layout.add_widget(btn)

        popup = Popup(title=title, content=layout,
                      size_hint=(None,None), size=(400,250))

        btn.bind(on_press=popup.dismiss)

        popup.open()


    def confirm_print(self):

        qty_text = self.root.ids.qty.text.strip()

        if qty_text == "":
            self.show_popup("Error", "Quantity is required.")
            return

        qty = int(qty_text)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        label = Label(text=f"Confirm printing {qty} Order?")

        buttons = BoxLayout(size_hint=(1,0.4), spacing=10)

        yes = Button(text="YES")
        no = Button(text="NO")

        buttons.add_widget(yes)
        buttons.add_widget(no)

        layout.add_widget(label)
        layout.add_widget(buttons)

        popup = Popup(title="Confirm Order",
                      content=layout,
                      size_hint=(None,None),
                      size=(420,250))

        yes.bind(on_press=lambda x: self.execute_print(popup))
        no.bind(on_press=popup.dismiss)

        popup.open()


    def execute_print(self, popup):

        popup.dismiss()

        try:

            qty = int(self.root.ids.qty.text)
            customer = self.root.ids.customer.text.strip()

            if customer == "":
                customer = "Walk-in"

            total = qty * UNIT_PRICE

            items = [{
                "name": PRODUCT_NAME,
                "qty": qty,
                "unit_price": UNIT_PRICE
            }]

            invoice_no = f"INV{random.randint(1000,9999)}"

            invoice = Invoice(invoice_no, customer, items, total, "Umar")

            data = invoice.to_dict()

            # try printing first
            print_invoice(data)

            # only save if printing worked
            save_invoice(data)

            self.root.ids.status.color = (0, 1, 0, 1)
            self.root.ids.status.text = "Printed successfully."

            self.clear_inputs()

            self.update_today_summary()

        except Exception as e:

            self.show_popup(
                "Printer Error",
                "Printer not detected.\nCheck USB cable or power."
            )


    def clear_inputs(self):

        self.root.ids.qty.text = ""
        self.root.ids.customer.text = ""


    def update_today_summary(self, *args):

        items, revenue = get_today_summary()

        self.root.ids.total_items.text = f"Total Items Sold: {items}"
        self.root.ids.total_revenue.text = f"Total Revenue: ₦{revenue:,}"


if __name__ == "__main__":
    RaasuApp().run()
