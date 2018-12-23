from dialogs import LoadDialog, SaveDialog
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import os
from pathlib import Path
from supreme_client import supreme_pick_and_fill
from sys import platform

class AIOTabbed(TabbedPanel):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.getSupremeProductTypes()
        super(AIOTabbed, self).__init__(**kwargs)

    def getSupremeProductTypes(self):
        self.supremeProductTypes = ['Jackets', 'Shirts', 'Tops/Sweaters', 'Sweatshirts', 'Pants', 'T-Shirts', 'Hats', 'Accessories', 'Shoes', 'Skate']

    def updateProductsTypeSpinner(self, text):

        for productType in self.supremeProductTypes:
            if productType == text:
                self.ids.productsType_spinner.text = text

    def launchSupreme(self):
        self.configValues = {}        
        for inputId in self.ids.keys():
            if 'Input' in inputId:
                if self.ids[inputId].text == '':
                    self.ids.responseLabel.text = "Error! You can't leave {} blank!".format(inputId)
                    return
                else:
                    self.configValues[inputId] = self.ids[inputId]

        if platform == 'win32':
            if not Path('./chromedriver.exe').is_file():
                self.ids.responseLabel.text = "Error! No chromedriver executable found for your system."
                return
        else:
            if not Path('./chromedriver').is_file():
                self.ids.responseLabel.text = "Error! No chromedriver executable found for your system." 
                return
        
        supreme_pick_and_fill(self.ids.productsType_spinner.text, self.ids.productKeyword_ti.text, self.configValues)
        self.ids.responseLabel.text = "Please follow your transaction on the Chromedriver itself."

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()

        self.dismiss_popup()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()

class AIOKivyApp(App):
    def build(self):
        return AIOTabbed()

if __name__ == '__main__':
    AIOKivyApp().run()