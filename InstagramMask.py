import os
from PIL import Image
from kivy.app import App
#from kivy.uix.image import Image
#from kivy.uix.label import Label
from kivy.lang.builder import Builder
#from kivy.uix.button import Button
#from kivy.uix.screenmanager import Screen
#from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel
from tkinter import filedialog, Tk

def getPath(relative):
	return str(os.path.join(os.path.dirname(os.path.abspath(__file__)), relative))

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio  = maxWidth/image.size[0]
    heightRatio = maxHeight/image.size[1]

    newWidth    = int(widthRatio*image.size[0])
    newHeight   = int(heightRatio*image.size[1])

    newImage    = image.resize((newWidth, newHeight))
    return newImage

class Page(TabbedPanel):
	def __init__(self, **kwargs):
		super(Page, self).__init__(**kwargs)
		self.export.disabled = True

	def browseFiles(self):
		root = Tk()
		root.withdraw()
		self.filename = filedialog.askopenfilename(initialdir =  "/", title = "Seleziona Immagine",
		filetype = (("jpeg files","*.jpg"), ("png files","*.png"),("all files","*.*")) )
		root.destroy()
		root = None
		self.img.source = self.filename

	def Export(self):
		root = Tk()
		root.withdraw()
		self.filename = filedialog.asksaveasfilename(initialdir =  "/", title = "Seleziona Destinazione",
		filetype = (("png files","*.png"),("all files","*.*")) )
		root.destroy()
		root = None
		final = Image.open(getPath('tmp/tmpImage.png'))

		if self.filename != None and self.filename != '':
			final.save(str(self.filename)+'.png', format='PNG')
			self.img.source = str(self.filename)+'.png'
			self.export.disabled = True
			self.apply.disabled = False

	def applyMask(self):
		imageToMask = self.img.source
		mask = getPath('mask.png')
		img1 = Image.open(imageToMask)
		img1 = changeImageSize(1080, 1080, img1)
		msk = Image.open(mask)
		final = Image.alpha_composite(img1.convert('RGBA'), msk.convert('RGBA'))

		final.save(getPath('tmp/tmpImage.png'), format='PNG')
		self.img.source = getPath('tmp/tmpImage.png')
		self.export.disabled = False
		self.apply.disabled = True


class MainApp(App):
	def build(self):
		self.title = "Instagram Mask"
		return Page()

if __name__ == '__main__':
	MainApp().run()
