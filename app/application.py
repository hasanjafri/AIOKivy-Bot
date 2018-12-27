from dialogs import LoadDialog, SaveDialog
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import os
from pathlib import Path
from supreme_client import supreme_pick_and_fill
from utils import generate_safe_config_file, decrypt_config_file, check_keyfile_exists
from sys import platform

class AIOTabbed(TabbedPanel):
    def __init__(self, **kwargs):
        check_keyfile_exists()
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
                    self.configValues[inputId] = self.ids[inputId].text

        if platform == 'win32':
            if not Path('./chromedriver.exe').is_file():
                self.ids.responseLabel.text = "Error! No chromedriver executable found for your system."
                return
        else:
            if not Path('./chromedriver').is_file():
                self.ids.responseLabel.text = "Error! No chromedriver executable found for your system." 
                return
        
        resp = supreme_pick_and_fill(self.ids.productsType_spinner.text, self.ids.productKeyword_ti.text, self.configValues)
        self.ids.responseLabel.text = resp

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load Config File", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        self.configValues = {}        
        for inputId in self.ids.keys():
            if 'Input' in inputId:
                if self.ids[inputId].text == '':
                    self.ids.file_inputLabel.text = "Error! You can't leave {} blank!".format(inputId)
                    return
                else:
                    self.configValues[inputId] = self.ids[inputId].text

        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save Config File", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0]), "rb") as stream:
            encrypted_dict = stream.read()
        
        decrypted_dict = decrypt_config_file(encrypted_dict)

        for inputId in decrypted_dict.keys():
            self.ids[inputId].text = decrypted_dict[inputId]

        self.ids.file_inputLabel.text = "Success! Config file loaded from:"
        self.ids.file_inputTitle.text = os.path.join(path, filename[0])
        self.dismiss_popup()

    def save(self, path, filename):
        print(self.configValues)
        data = generate_safe_config_file(self.configValues)

        with open(os.path.join(path, filename), 'wb') as stream:
            stream.write(data)

        self.ids.file_inputLabel.text = "Success! Config file saved at:"
        self.ids.file_inputTitle.text = os.path.join(path, filename)
        self.dismiss_popup()

class AIOKivyApp(App):
    def build(self):
        return AIOTabbed()

if __name__ == '__main__':
    AIOKivyApp().run()