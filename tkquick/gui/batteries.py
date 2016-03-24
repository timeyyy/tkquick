#~ Copyright 2015 Timothy C Eichler (c) , All rights reserved.
#~ Restrictive license being used whereby the following apply.
#~ 1. Non-commercial use only
#~ 2. Cannot modify source-code for any purpose (cannot create derivative works)
#~ The full license can be viewed at the link below
#~ http://www.binpress.com/license/view/l/9dfa4dbfe85c336d16d1dd71a2e2cfb2
import tkinter as tk
import tkinter.ttk as ttk
import time
from pprint import pprint
import functools
from collections import defaultdict

from timstools import ignored
try:
	from .style_defaults import * 
except SystemError:
	from style_defaults import *
	
class TimedOut(Exception):
	pass
class MaxInput(Exception):
	pass
class FirstInput(Exception):
	pass
	
def event_clock(event,timevar,timemax,entries=None,maxentries=None):	
	'''
	returns False when time between events is greater then time specified
	returns False when entries is equal to the max entries
	timevar is a list that has the time of the event/events
	'''
	timevar.append(event.time)	#at least two time variables
	if len(timevar) > 1:		
		if timevar[-1]-timevar[-2] >= timemax:	# time to exit
			raise TimedOut('maximum time beweent input exceeded :  %d seconds' % (timemax *0.001))
	if len(entries) == maxentries:		# Also time to exit
		raise MaxInput('maximum input exceeded : %s' % maxentries)

tk_no_state = {
	35: 'KP_End',
	40: 'KP_Down',
	34: 'KP_Prior',
	37: 'KP_Left',
	12: 'KP_Clear',			#this is kp_5 with no numlock
	39: 'KP_Right',
	36: 'KP_Home',
	38: 'KP_Up',
	33: 'KP_Next',
	45: 'KP_Insert',
	46: 'KP_Delete'}
	
tk_keycode = {
	96: 'KP_0', 
	97: 'KP_1', 
	98: 'KP_2', 
	99: 'KP_3', 
	100: 'KP_4', 
	101: 'KP_5', 
	102: 'KP_6', 
	103: 'KP_7', 
	104: 'KP_8', 
	105: 'KP_9', 
	109: 'KP_Subtract', 
	107: 'KP_Add', 
	106: 'KP_Multiply', 
	111: 'KP_Divide', 
	110: 'KP_Comma'}
	
tk_modifiers = ['Alt_L',		#tbd make this tuple
				'Alt_R', 
				'Control_L', 
				'Control_R', 
				'Shift_L', 
				'Shift_R',
				'Win_L',
				'Win_R']

def validate_hk(func):
		'''
		validate, then if it fails do not input or reset	
		self.max_mod_after_key = 0
		self.max_mod_before_key = 0
		self.max_key_after_mod = 1
		self.max_key_before_mod = 1
		self.reset_on_validate_fail = 0
		'''		
		#~ @functools.wraps(func)	# wtf wraps not chaning te name back to validate... TBD
		def on_call(self, event):
			if not hasattr(self, '_MOD_BEFORE_KEY'):
				self._MOD_BEFORE_KEY = 0
				self._MOD_AFTER_KEY = 0
				self._KEYS_BEFORE = 0
				self._KEYS_AFTER = 0
			
			event = self._parse_tkevent(event)
			hk = event.keysym
			try:
				self.captured[-1]
			except IndexError:
				# This code takes care of First key input into widget after reset
				if not self.max_mod_before_key and hk in self.tk_modifiers:	# No Modifiyers before keys aloud
					self.max_mod_before_key_hook()
					if self.reset_on_validate_fail:
						self.reset()
					return
				elif not self.max_key_before_mod and hk not in self.tk_modifiers: # No keys before mods aloud
					self.max_key_before_mod_hook()
					if self.reset_on_validate_fail:
						self.reset()
					return
			if hk in self.tk_modifiers:
				if not self._KEYS_BEFORE and not self._KEYS_AFTER:
					self._MOD_BEFORE_KEY = self._MOD_BEFORE_KEY + 1
					if self._MOD_BEFORE_KEY > self.max_mod_before_key:
						self.max_mod_before_key_hook()
						if self.reset_on_validate_fail:
							self.reset()
						return
				else:
					self._MOD_AFTER_KEY = self._MOD_AFTER_KEY + 1
					if self._MOD_AFTER_KEY > self.max_mod_after_key:
						self.max_mod_after_key_hook()
						if self.reset_on_validate_fail:
							self.reset()
						return
			else:
				if not self._MOD_BEFORE_KEY and not self._MOD_AFTER_KEY:
					self._KEYS_BEFORE = self._KEYS_BEFORE + 1
					if self._KEYS_BEFORE > self.max_key_before_mod:
						self.max_key_before_mod_hook()
						if self.reset_on_validate_fail:
							self.reset()
						return
				else:
					self._KEYS_AFTER = self._KEYS_AFTER + 1
					if self._KEYS_AFTER > self.max_key_after_mod:
						self.max_key_after_mod_hook()
						if self.reset_on_validate_fail:
							self.reset()
						return
			return func(self, event)
		return on_call
	
class HotKeyGrabber(tk.Frame):
	'''
	Used for getting user input from the keyboard.
	Subclass this function and change the variables in a start
	method to change options, defaults shown below
	
	self.format_start
	self.format_end
	self.text = 'Click to enter a hot key..'
	self.conf = {'width':30}
	self.custom_input = {'Space':'You Pressed Space!'} change how the keysym property is handled #TBD CHANGE NAME TO CUSTOM_INPUT_KEY_MAP?
	self.default_case can be set to lower or upper, or pass in lower or upper to the set method
	
	self.time_out = 3000
	self.max_keys = 4
	self.max_mod_after_key = 0
	self.max_mod_before_key = 3
	self.max_key_after_mod = 1
	self.max_key_before_mod = 1
	self.reset_on_validate_fail = 1
	self.capture_mouse = [1,2,3], whicho mouse buttons to capture, defaults to none 
	self.reset_on_click = False
	self.reset_on_focus = False
	self.validate_multiple_grabbers = False			Set this to the class/subclassed "ValidateGrabbers" class to use the multiple hotkeygrabber validator

	self.previous_entry # hotkey that existed before the user focused in
	use self.original_keys to access the unchanged versions
	
	Make sure to bind using  , add="+", for button 1 or button double or key otherwise will overide behavior
	binding to Key will not work without all of effort as it stops the tkinter bind propergation,
	so that tkingetr doesnt put in the charachter... u would need to get the bind id and
	then add your bind first, then readd the original...
	
	list of tkinter modifyer symbols can be gotten from self.tk_modifiers
	
	Styling
	
	The widget is a entry widget set to disabled to remove the cursor,
	etier find another way to remove the cursour.. or use a label, and style the label
	accoridingly, That would probablyt be better, i ddid it once but changed probably because it didnt look so good
	the problem with using a imagestyle is that u have to change the fig totchange the highlight ring or sth
	
	Otherwise we cannot use mappings...
	'''
	def __init__(self, parent=None,app = None):
		self.time = []						# holds time between key presses
		self.captured = []					# holds results      
		self.original_keys = []				# the original tkinter key_sym 
		self.tk_modifiers = tk_modifiers
		self.format_start, self.format_end = ('<','>')	
		self.text = 'Click to enter a hot key..'
		self.conf = {'width':25}
		self.reset_on_click = True
		self.reset_on_focus = True
		self.time_out = 3000
		self.max_keys = 4
		self.max_mod_after_key = 0
		self.max_mod_before_key = 3
		self.max_key_after_mod = 1
		self.max_key_before_mod = 1
		self.reset_on_validate_fail = 1
		self.validate_multiple_grabbers = False
		self.capture_mouse = []
		self.previous_entry = []		 # Previous hk entry before the user focused into the widget
		self.default_case = None
		#~ tk.Frame.__init__(self, parent, relief='flat',borderwidth=0)
		#~ self.pack(expand=1, fill='both')   		
		self.app = app
		self.parent = parent
		self.start()
		self.make_widgets()
		with ignored(AttributeError):
			#~ self.ent.config(**self.conf)	
			self.config(**self.conf)
		if self.validate_multiple_grabbers:
			self.bind('<FocusOut>', lambda event: self.validate_multiple_grabbers.validate(self, self.get(), self.previous_entry),'+')
			self.bind('<FocusIn>', lambda event: self.validate_multiple_grabbers.validate(self, self.get(), self.previous_entry),'+')
		self.finish()
	def start(self):pass				# inherit this from a superclass that gives the docs etc 
	def finish(self):pass
	def duplicate_err_hook(self,event,**kwargs):
		'''
		Subclass this to handle what happens when duplicate keys are pressed
		'''
	def max_timed_err_hook(self,event,**kwargs):
		'''
		Subclass this to contorl what hapends on timeout
		'''
	def max_mod_after_key_hook(self):
		'''
		Sublass this to control what happens on max modifyers after key press
		'''
		#~ print('raise MaxModifyerAfterKey')
	def max_key_after_mod_hook(self):
		'''
		Subclass this to contro what happens on max keys after a modifyer rare pressed
		'''
		#~ print('raise MaxKeyAfterModifyers')
	def max_mod_before_key_hook(self):
		'''
		Subclass this to control what happesad.fsa
		'''
		#~ print('raise MaxModifyersBeforeKey')
	def max_key_before_mod_hook(self):
		'''
		Subclass this to control what happesad.fsa
		'''
		#~ print('raise MakKeyBeforeModifyers')
	def _custom_input(self,event):
		with ignored(KeyError, AttributeError):
			new_keysym = self.custom_input[event.keysym]
			event.keysym = new_keysym
		return event 
	
	def _parse_tkevent(self,event):
		'''tkinter doesnt' apply the .keysym method to every event properly so here we modify it,
		essentially just giving all events a keysym property that is correct'''		
		new_keysym = tk_keycode.get(event.keycode)
		if new_keysym: 
			print('new_keysym', new_keysym)
			event.keysym = new_keysym
		elif not event.state:
			if not event.keysym:	#PUT this in recently for uncrumpled to work, still needs work here
				new_keysym = tk_no_state.get(event.keycode)
				event.keysym = new_keysym
		elif event.keysym == 'Return' and event.state != 8:		# exceptions with the KP_Return
			event.keysym = 'KP_Return'
		elif event.num != '??':									# Mouse Buttons
			event.keysym = 'Button-'+str(event.num)
		return event
	
	@validate_hk
	def on_key_press(self,event):
		event = self._parse_tkevent(event)		
		try:
			print(self.captured)
			event_clock(event,
						timevar=self.time,
						timemax=self.time_out,
						entries=self.captured,
						maxentries=self.max_keys)
		except(MaxInput,TimedOut) as err:
			# Reset condition Reached
			self.var.set('')
			self.time = []
			self.original_keys = [event.keysym]
			event = self._custom_input(event)
			self.captured = [event.keysym]	
			msg = 'Field reset - {0}'.format(err)		#move this to the subclassed function 
			self.max_timed_err_hook(msg)
		else:
			self.original_keys.append(event.keysym)
			event = self._custom_input(event)
			self.captured.append(event.keysym)
			# if the user holds down a key, prevents it from spammin in multiple times
			with ignored(IndexError):			
				if self.captured[-1] == self.captured[-2]:
					del self.captured[-1]
					self.duplicate_err_hook(event)
					return 'break'
		x = self.format_start +' %s %s ' % (self.captured[-1], self.format_end)	#the last added char is formated 
		self.var.set(self.var.get()+x)
		return 'break'				
	
	def reset(self,event=None):
		self.var.set('')
		self.time = []
		self.captured = []								
		self.original_keys = []	
		with ignored(AttributeError):		
			del self._MOD_BEFORE_KEY
			del self._MOD_AFTER_KEY
			del self._KEYS_BEFORE
			del self._KEYS_AFTER
		# Undisable on reset (user doesn't have to wait until clicking out) 
		if self.validate_multiple_grabbers:		
			self.config(state='normal')
	@staticmethod
	def uniform_key(hotkey):
		'''use to get the hotkey in a hashable form for using as a dict key'''
		if type(hotkey) == list:
			hotkey = tuple(hotkey)
			if len(hotkey) == 1:
				hotkey = hotkey[0]
		return hotkey
			
	def get(self):
		'''Get a list of the entered keys without formating,
		If still set to starting text i.e click to enter hotkey,
		then returns none'''
		if self.var.get() == self.text:
			return None
		else:
			chars = [char for char in self.var.get().split() 
					if char not in (self.format_start,self.format_end)]  
			return chars
	
	def set(self, hotkeyvalues, case=None):
		'''set a str with formatting
		pass in a list! with each entry as a key'''
		if type(hotkeyvalues) == str:
			hotkeyvalues = [hotkeyvalues]
		formatted = (self.format_start +' %s %s ' % (item, self.format_end) 
										 for item in hotkeyvalues)
		if not case:
			case == self.default_case
		if case == 'lower':
			formatted = (key.lower() for key in formatted)
		elif case == 'upper':
			formatted = (key.upper() for key in formatted)
		formatted = ''.join(formatted)
		self.var.set(formatted)
		if len(hotkeyvalues) < self.max_keys+1:
			for key in hotkeyvalues:
				self.captured.append(key)
		else:
			raise MaxInput('Hotkey being set is longer than set value for self.max_keys, currently: '+str(self.max_keys))
		
	def make_widgets(self):
		def on_focus():												
			#~ self.ent.focus()
			self.focus()
			if self.reset_on_focus:
				self.reset()
		#~ self.ent = ttk.Entry(self, **c_pentry)
		
		#~ self.ent = ttk.Label(self)
		ttk.Label.__init__(self, self.parent, style='hotkeygrabber.TLabel')
		#~ ttk.Style(self.app.root).configure(self['style'],background='pink')
		#~ ttk.Style().map(self.ent['style'], background=[('disabled','white')],
											#~ foreground=[('disabled','black')])
		#~ self.ent = SimpleEntry(self)
		#~ ttk.Style().map(self.ent['style'],
						#~ foreground=[('!disabled', 'pink'),('disabled', 'green')])
						#~ foreground=[('!disabled', 'pink'),('disabled', 'green')])
		#~ ttk.Style().map(self.ent['style'],
							#~ foreground=[('disabled','black')],
							#~ fieldbackground=[('!disabled','green')])	# making disabled state not dull text
		#~ self.ent.config(state='disabled')						# removing cursor 
		#~ self.config(state='disabled')						# removing cursor 
		self.var = tk.StringVar()
		self.var.set(self.text)
		#~ self.ent.config(textvariable=self.var, takefocus=True)
		self.config(textvariable=self.var, takefocus=True)
		#~ self.ent.bind('<Key>',  self.on_key_press)
		self.bind('<Key>',  self.on_key_press)
		#~ self.ent.bind('<Button-1>',lambda event: on_focus())
		self.bind('<Button-1>',lambda event: on_focus())
		self.bind('<Button-1>',lambda event: on_focus())
		#~ self.ent.bind('<Double-Button-1>',lambda event: self.reset())
		self.bind('<Double-Button-1>',lambda event: self.reset())
		if self.capture_mouse:
			for numb in self.capture_mouse:
				button = '<Button-{0}>'.format(numb)
				#~ self.ent.bind(button, lambda event: self.on_key_press(event))
				self.bind(button, lambda event: self.on_key_press(event))
		if self.reset_on_focus:
			#~ self.ent.bind('<FocusIn>', self.reset)
			self.bind('<FocusIn>', self.reset, '+')
		def prev(event):
			self.previous_entry = self.get()
		self.bind('<FocusIn>', prev, '+')
		#~ self.ent.pack(expand=1, fill='both',padx=1,pady=1)
		self.pack(expand=1, fill='both')

	def key_parser(self, hk_to_check, mapping=None, v=False):	# TBD find a way to allow acces to this function out of the class
		'''
		If you are using a custom input mapping this function
		will return either the parsed value or original tkinter key depending onwht you pass in ffs
		
		TBD,can't i just use the self.original_keys.... wtf man
		This is useful for pputting in hotkeys that need to be converted where as
		self.orignal_keys is only avaliable if the user has just put in the keys
		'''
		if not mapping:
			mapping = self.custom_input
		#~ pprint(mapping)
		try:
			try:
				parsed_key = mapping[hk_to_check]
				return parsed_key
			except TypeError:		# hk was passed in as a list not a str
				if v:
					print('in the list comprehension')
				parsed_key = []
				for akey in hk_to_check:
					if mapping.get(akey):
						#~ print('conv method 1')
						parsed_key.append(mapping.get(akey))
					else:
						#~ print('conv method 2')
						for key, value in mapping.items():
							#~ print('value!,', value)
							if akey == value:
								#~ print('converted to ',key)
								parsed_key.append(key)			# going from parsed_key to a tkinter key
								break
						else:
							#~ print('no match adding self, ',akey)
							parsed_key.append(akey)		
				#~ print('parsed_key', parsed_key)
				if len(parsed_key) == 1:
					return parsed_key[0]
				else:
					return parsed_key
		except KeyError:
			if v:
				print('threw a fucing keyerror')
			hotkey_list = []
			if type(hk_to_check) == str:
				hk_to_check = [hk_to_check]
			for akey in hk_to_check:
				#~ print('akey',akey)
				for key, value in mapping.items():
					if akey == value:
						#~ print('converted to ',key)
						hotkey_list.append(key)			# going from parsed_key to a tkinter key
						break
				else:
					#~ print('no match adding self')
					hotkey_list.append(akey)
			#~ print('hotkey_list', hotkey_list)
			if len(hotkey_list) == 1:					#TBD REMOVE THIS, just always return a list and use the unifrom key function
				return hotkey_list[0]
			else:
				return hotkey_list
	
class ValidateGrabbers():
	'''
	Validation for multiple hotkeygrabbers
	To use , set the instance with your required options to 
	the validate_multiple_grabbers attribute in the HotKeyGrabber
	class in question.
	
	You can set the bellow options in the __init__ method
	options include
	NORMAL = {}
	DISABLED = {}
	
	#max_duplicates = 0 not implemented
	disable_blanks = False			if multiple empty fields blank em
	
	automatic_disable = True
	automatic_enable = True
	grabber_name_attrib			an attribute containing a unique name for each grabber	
	get_grabber_from_name				function that accepts a grabber name and returns the widget. 
	
	no_disabled_entries_attrib = 		if nothing disabled this will be True, otherwise False 
							# FUCK MAN HOW TO PASS AN ATTRIBUTE AND NOT A VALUE!
	'''	
	def __init__(self, NORMAL, DISABLED, automatic_disable=True,
				automatic_enable=True, grabber_name_attrib=None,
				no_disabled_entries_attrib=None, get_grabber_from_name=None,
				disable_blanks=False):
		self.NORMAL = NORMAL
		self.DISABLED = DISABLED
		self.automatic_disable = automatic_disable
		self.automatic_enable = automatic_enable
		self.disable_blanks = disable_blanks
		if grabber_name_attrib:
			self.grabber_name_attrib = grabber_name_attrib
		if no_disabled_entries_attrib:
			self.no_disabled_entries_attrib = no_disabled_entries_attrib
	
	def add_key(self, hotkey, setting):
		'''Call this function when you load up values into your grabbers'''
		hotkey = HotKeyGrabber.uniform_key(hotkey)
		if not self.NORMAL.get(hotkey):
			self.NORMAL[hotkey] = setting
		else:
			print('DUPLICATE IN YOUr file wtf MATE: ', hotkey)

	def validate(self, hk_grabber, hotkey, previous_hotkey):
		# This part does the automatic popping and unpopping behavior, 
		# makes use of the indent_or unindent function
		hotkey = HotKeyGrabber.uniform_key(hotkey)
		previous_hotkey = HotKeyGrabber.uniform_key(previous_hotkey) 
		try:
			if not self.indent_or_unindent(hotkey, hk_grabber.form_name, previous_hotkey):
				#~ print('Failure')
				hk_grabber.config(state='disabled')
				if not self.automatic_disable:
					return
				with ignored(AttributeError):
					exec('hk_grabber.'+self.no_disabled_entries_attrib+' = False')
				if len(self.DISABLED[hotkey]) == 2: 						# Disabling the original key instance
					original_index = self.DISABLED[hotkey].index(eval('hk_grabber.'+self.grabber_name_attrib))
					other_index = not original_index
					setting = self.DISABLED[hotkey][other_index]
					widget = self.get_grabber_from_name(setting)
					if widget:
						widget.config(state='disabled')
			else:
				#~ print('success')
				hk_grabber.config(state='normal')
				if not self.automatic_enable:
					return	
				with ignored(KeyError):												# Unpoping the last blocked key if its alone	
					if len(self.DISABLED[previous_hotkey]) == 1:
						setting = self.DISABLED[previous_hotkey]
						widget = self.get_grabber_from_name(setting[0])
						if widget:
							widget.config(state='normal')
							self.NORMAL[previous_hotkey] == setting
				
				if not self.get_disabled_states():
					with ignored(AttributeError):						
						exec('hk_grabber.'+self.no_disabled_entries_attrib+' = True')			
		except SystemError:															# used to break out of the indent_or_unindent function 
			return
	def indent_or_unindent(self, hotkey, setting, previous_hotkey):
		'''Retursn True or False if the button should be indented or unindented'''
		def hotkey_disabled():
			try:
				disabled_settings = self.DISABLED[hotkey]
				if disabled_settings != []:
					#~ print(9)
					return True	
				#~ print(11)
				return False
			except KeyError:
				#~ print(10)
				return False

		with ignored(KeyError):					
			del self.NORMAL[previous_hotkey]		# Previous hotkey has been changed so remove it from list
		with ignored(KeyError, ValueError):			# Freeup the previous hotkey if it was disabled
			index = self.DISABLED[previous_hotkey].index(setting)
			del self.DISABLED[previous_hotkey][index]
		print('HOTKEY', hotkey, not hotkey)
		if not self.disable_blanks and not hotkey:
			raise SystemError					
		
		value_assigned = self.NORMAL.get(hotkey)
		if not value_assigned and not hotkey_disabled():			
			#~ print(1)
			self.NORMAL[hotkey] = setting
			return True
		elif value_assigned:						# Handling a conflict
			#~ print(3)
			del self.NORMAL[hotkey]				
			self.DISABLED[hotkey] = [value_assigned, setting]	
			return False
		else:
			#~ print(4)
			disabled_settings = self.DISABLED[hotkey]				
			self.DISABLED[hotkey].append(setting)
			return False
	
	def get_disabled_states(self):
		''' Returns disabled Buttons, other wise returns None if there are no disabled buttons,
		if you have to build into another api or something you can set the attrib to be set using
		no_disabled_entries_attrib
		
		Values are returned in a dict with the values as a list of the conflicting settings'''
		disabled_dudes = defaultdict(list)
		for key, value in self.DISABLED.items():				# Unfortunaley this isn't reliable, check the statees of all buttons
			if len(value) > 1:
				for setting in value:
					widget = self.get_grabber_from_name(setting)
					if str(widget.cget('state')) =='disabled':
						disabled_dudes[key].append(setting)	
		if not disabled_dudes:
			return None
		else:
			pprint(disabled_dudes)
			return disabled_dudes
		
if __name__ == '__main__':
	root = tk.Tk()
	loadStyle(root)
	a = HotKeyGrabber(root)
	a.set(['ass'])
	#~ b = HotKeyGrabber(root)
	#~ b.set(['ass2'])
	root.mainloop()
