from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from pathlib import Path
from supreme_client import supreme_pick_and_fill
from sys import platform

class AIOTabbed(TabbedPanel):
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
        if platform == 'win32':
            if not Path('./chromedriver.exe').is_file():
                self.ids.responseLabel.text = "Error! No chromedriver executable found for your system."
        else:
            if not Path('./chromedriver').is_file():
                self.ids.responseLabel.text = "Error! No chromedriver executable found for your system." 

        if not Path('./config.py').is_file():
            self.ids.responseLabel.text = "Error! No configuration file with user details to use with this transaction."
        
        else:
            supreme_pick_and_fill(self.ids.productsType_spinner.text, self.ids.productKeyword_ti.text)
            self.ids.responseLabel.text = "Please follow your transaction on the Chromedriver itself."

class AIOKivyApp(App):
    def build(self):
        return AIOTabbed()

if __name__ == '__main__':
    AIOKivyApp().run()