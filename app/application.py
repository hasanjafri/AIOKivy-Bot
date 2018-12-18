from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from supreme_client import supreme_pick_and_fill

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
        supreme_pick_and_fill(self.ids.productsType_spinner.text, self.ids.productKeyword_ti.text)

class AIOKivyApp(App):
    def build(self):
        return AIOTabbed()

if __name__ == '__main__':
    AIOKivyApp().run()