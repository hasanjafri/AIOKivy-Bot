from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.dropdown import DropDown

class ProductListDropDown(DropDown):
    pass
class AIOTabbed(TabbedPanel):
    pass

class AIOKivyApp(App):
    def build(self):
        return AIOTabbed()

if __name__ == '__main__':
    AIOKivyApp().run()