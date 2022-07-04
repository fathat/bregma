"""Signal file.  registering, attaching, and raising"""

class Signal(object):
	"""
	Responsible for aggregating a collection of signals for an object
	and allowing consumers to connect to a certain set of signals, and
	for the object to emit any of those signals
	"""

	def __init__(self):
		"""Initalize the signals dictionary"""
		self._signals = {}

	def _add(self, signal_name):
		"""Add a signal to the object.  Only to be used by derived types"""
		if not self._signals.has_key(signal_name):
			self._signals[signal_name] = []
	
	def _emit(self, signal_name):
		"""
		Emit a signal on the object, iterating over all connected callbacks. Only to be used by derived types.
		Raises an exception if signal_name is not part of the object
		"""
		try:
			for callback in self._signals[signal_name]:
				callback(self)
		except KeyException:
			raise Exception(signal_name + " could not be found")


	def connect(self, signal_name, func):
		"""
		Connect to a signal and save the given callback
		Raises an exception if signal_name is not part of the object
		"""	
		try:
			self._signals[signal_name].append(func)
		except KeyException:
			raise Exception(signal_name + " could not be found")
