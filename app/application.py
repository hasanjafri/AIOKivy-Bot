from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel

class AIOTabbed(TabbedPanel):
    pass

class AIOKivyApp(App):
    def build(self):
        return AIOTabbed()

if __name__ == '__main__':
    AIOKivyApp().run()