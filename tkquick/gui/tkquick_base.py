import tkinter as tk
import tkinter.ttk as ttk

from timstools import ignored

class TkquickBase():
	'''
	Mix In class
	'''
	def __init__(self,parent=None,app=None):
		self.parent = parent
		self.app = app
		
		self.start()
		with ignored(AttributeError):
			self.use_border
			self.border = tk.Frame(parent)
			self.parent = self.border
			self.border.config(**self.border_cfg)
			self.border.pack(**self.border_gm_cfg)
	
	def start(self):
		'''Config Options to be subclassed'''
		self.make()
	def make(self):
		'''Build Widgets and config etc here'''
	def finish(self):
		'''This is run after make is called'''
