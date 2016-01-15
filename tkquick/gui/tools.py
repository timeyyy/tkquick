import threading
import _thread as thread
from functools import wraps
import time
import sched

def unique_int(values):
	'''
	if a list looks like 3,6
	if repeatedly called will return 1,2,4,5,7,8
	'''
	last = 0
	for num in values:	#generate a unique number
		if last not in values:	#num is  uniquie (will return numbers if the list has skips so p1 p2 p5,
			#~ print('checking if last not in
			break
		else:				#number already exists
			last += 1
	return last				#looped till end, then it was plussed so just return new value

def tkinter_breaker(func):
	"""
	decorator to stop tkinter propagtion default bindings,
	tkinter clinds a ladder of bindings, see http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
	problem is if the user holds ctrl and presses i it will propgate up
	so i added kills for the higher levels
	"""
	#tbd, finish climb to higher levels,mmm probably just kill normally without decorator
	#, actually i think changeing the way the binding where done fixed it
	@wraps(func)
	def oncall(*args, **kwargs):
		try:
			func(*args, **kwargs)
		except Exception as err:
			raise err
		finally:
			return "break"
	return oncall

def toggle(btn,tog=[0]):
	'''
	a list default argument has a fixed address
	'''
	tog[0] = not tog[0]
	if not tog[0]:
		return False
	else:
		return True

def TkErrorCatcher(func):	
	'''
	Used To catch errors through functions raised from the event loop
	in tkinter. 
	
	More for tool builders
	
	when i send in the orignal args to the rror handle its passing in self again
	found out if its a method function or a normal function then delete the old self
	http://stackoverflow.com/questions/19227724/check-if-a-function-uses-classmethod
	
	sigh in the end all you accomplish is changing a raised error into a function call
	
	just call the function directly... 
	
	this is only useful for handling errors that i didnt invoke
	
	for a wrapped function on_key_press required setup
	
	self.on_key_press.__dict__['on_error'] = {DuplicateKeyPressed: self.duplicate_err_handle} # Bound function methods have to be accessed like this...
	self.on_key_press.__dict__['exceptions'] = (DuplicateKeyPressed,)
	
	than from in on_key_press you can do
	raise DuplicateKeyPressed and it will be handled by self.duplicate_err_handle
	'''								
	def on_call(*args,**kwargs):
		on_error = on_call.on_error 			# rebinding names so its cleaner code below
		err_args = on_call.err_args 
		exceptions = on_call.exceptions
		err_kwargs = on_call.err_kwargs
		try:
			print('trying func now')
			func(*args, **kwargs)
		except exceptions as err:
			if type(on_error) == dict:				# Either on_error is a dict mapping exceptions to handlers or a generic function
				print('dict')
				if err.__class__ in on_error:
					key = err.__class__
					print('using error type as key')
				else:
					key = 'default'
				if not err_args:				# Don't pass arguments in to recieve the original function arguments
					print('setting args')
					err_args = {key: args}
				if not err_kwargs:
					err_kwargs = {key: kwargs}
				print('running : %s' % (on_error[key]))
				print(len(err_args[key]))
				print()
				print(err_kwargs[key])
				on_error[key](*err_args[key],**err_kwargs[key])
			else:
				print('type on error not dict')					
				print(type(on_error))					
				if not err_args:				# Don't pass arguments in to recieve the original function arguments
					err_args =  args
					print('passing default args')
				if not err_kwargs:
					err_kwargs = kwargs
				print('running : %s' % (on_error))
				on_error(*err_args, **err_kwargs)
		else:
			pass
		finally:
			pass	
	on_call.on_error = lambda *args, **kwargs: 0					# Bound method variables
	on_call.err_args = ()
	on_call.exceptions = Exception
	on_call.err_kwargs = {}
	return on_call

def ttk_manual(style, widgets):
	@TraceCalls()
	def iseven(n):
		yield True if n == 0 else isodd(n - 1)
	@TraceCalls()
	def isodd(n):
		yield False if n == 0 else iseven(n - 1)
	print(list(iseven(7)))
	s = style
	if type(widgets) not in (list,tuple):
		widgets = [widgets]

	#~ return
	
	for item in widgets:	# widgets is the passed in items e.g TButton, TLabel etc
		#~ print(list(flatten(s.layout(item))))	
		print(flatten(s.layout(item)))
		#~ holder = []
		#~ for i in flatten(s.layout(item)):
			#~ holder.append(i)
		#~ print()
		#~ print(holder)
		return
	
		print('Layout of Elements: %s -s.layout()'%(item))
		print()
		layout = s.layout(item)
		print(layout[0])
		print()
		print(layout[0][0])
		print()
		print(layout[0][0])
		print()
		print(layout[0][1].keys())
		print()
		#~ print(layout[0][1].keys())
		print()
		for key,value in layout[0][1].items():
			print(key)
			print(	value)
		#~ print(layout[1][0])
		print()
		#~ print(layout[0][01])
			#~ print('printint')
			#~ print(layout)
			#~ print()
		#~ print(s.layout(item))


def rate_limited(max_per_second, mode='wait', delay_first_call=False):
	"""
	Decorator that make functions not be called faster than
	
	set mode to 'kill' to just ignore requests that are faster than the 
	rate.
	
	set mode to 'refresh_timer' to reset the timer on successive calls
	
	set delay_first_call to True to delay the first call as well
	"""
	lock = threading.Lock()
	min_interval = 1.0 / float(max_per_second)
	def decorate(func):
		last_time_called = [0.0]
		func_refresh_id = []
		scheduled_events = []
		@wraps(func)
		def rate_limited_function(*args, **kwargs):
			def run_func():
				lock.release()
				ret = func(*args, **kwargs)
				last_time_called[0] = time.perf_counter()
				return ret
			lock.acquire()
			elapsed = time.perf_counter() - last_time_called[0]
			left_to_wait = min_interval - elapsed
			if delay_first_call:	
				#~ print('delaymode: left to wait',left_to_wait)
				if left_to_wait > 0:
					if mode == 'wait':
						#~ print('sleeping:', left_to_wait)
						time.sleep(left_to_wait)
						return run_func()
					elif mode == 'kill':
						lock.release()
						return
				else:
					return run_func()
			else:										# Allows the first interval to not have to wait
				if not last_time_called[0] or elapsed > min_interval:	
					return run_func()		
				elif mode == 'refresh_timer':
					print('Ref timer')
					lock.release()
					#~ ret = func(*args, **kwargs)
					last_time_called[0] += time.perf_counter()
					#~ my_id = unique_int(func_refresh_id)
					#~ func_refresh_id.append(my_id)
					#~ while func_refresh_id.get(my_id):
					#~ print('ref timer',func_refresh_id)
					#~ lock.release()
					return 
				elif left_to_wait > 0:
					if mode == 'wait':
						time.sleep(left_to_wait)
						return run_func()
					elif mode == 'kill':
						#~ print('killing with time: ', left_to_wait)
						lock.release()
						return
		return rate_limited_function
	return decorate

def delay_call(seconds):
	'''Decorator to delay the runtime of your function,
	each succesive call to function will refresh the timer,
	canceling any previous functions
	'''
	my_scheduler = sched.scheduler(time.perf_counter, time.sleep)
	def delayed_func(func):	# this gets passed the function!
		def modded_func(*args, **kwargs):
			if len(my_scheduler.queue) == 1:
				my_scheduler.enter(seconds, 1, func, args, kwargs)
				my_scheduler.cancel(my_scheduler.queue[0])
			else:
				my_scheduler.enter(seconds, 1, func, args, kwargs)
				thread.start_new_thread(my_scheduler.run, ())
		thread.start_new_thread(my_scheduler.run, ())
		modded_func.scheduler = my_scheduler
		return modded_func
	return delayed_func
	
@rate_limited(2, mode='wait') # 2 per second at most
def print_num_wait(num):
	print (num )

@rate_limited(1/2, mode='kill') # 2 per second at most
def print_num_kill(num):
	print(num)

@rate_limited(2, mode='kill', delay_first_call=True) # 2 per second at most
def print_num_kill_delay(num):
	print(num)	

@rate_limited(1/3, mode='wait', delay_first_call=True) # 2 per second at most
def print_num_wait_delay(num):
	print(num)	
	
@rate_limited(1/5, mode='refresh_timer') # 2 per second at most
def print_num_wait_refresh(num):
	print(num)	
	
@delay_call(2)
def print_num_wait_refresh(num):
	#~ print('YEAH')
	print(num)	
if __name__ == "__main__":
	#~ print('Rate limited at 2 per second at most')	
	#~ print()	
	#~ print("Mode is Kill")
	#~ print("1 000 000 print requests sent to decorated function")
	#~ for i in range(1,1000000):
		#~ print_num_kill(i) 
#~ 
	#~ print()
	#~ print('Mode is Wait - default')
	#~ print("10 print requests sent to decorated function")
	#~ for i in range(1,11):
		#~ print_num_wait(i) 

	#~ print()
	#~ print('Mode is Kill with Delay on first request')
	#~ print("1 000 000 print requests sent to decorated function")
	#~ for i in range(1, 1000000):
		#~ print_num_kill_delay(i)					
	
	#~ print()
	#~ print('Mode is Wait with Delay on first request')
	#~ print("5 print requests sent to decorated function")
	#~ for i in range(1, 6):
		#~ print_num_wait_delay(i) 
	#~ print()

	print('Mode is refresh_timer')
	print("100 000 print requests sent to decorated function")
	for i in range(1,100001):
		print_num_wait_refresh(i) 
	print('Finished Printing')

	while 1:
		time.sleep(0.5)

