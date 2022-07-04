from core.signal import *

class Random(Signal):
	def __init__(self):
		Signal.__init__(self)
		self._add("amg")

	def do_something(self):
		self._emit("amg")


class Consumer(object):
	def __init__(self):
		self._r = Random()
		print self
		self._r.connect("amg", self.callback_method)
		self._r.do_something()

	def callback_method(self, obj):
		print 'Holy shit!'
		print self
		print obj


c = Consumer()
