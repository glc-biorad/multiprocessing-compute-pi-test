import multiprocessing as mp
import random
import numpy as np
import time

class Processor(mp.Process):
	def __init__(self, pid, queue, **kwargs):
		super(Processor, self).__init__()
		self.idx = pid
		self.queue = queue
		self.kwargs = kwargs

	def _is_inside_circle(self, location, radius):
		x, y = location
		return True if (x**2 + y**2) < radius else False

	def run(self):
		"""Compute pi"""
		time_start = time.time()
		# Constants.
		radius = 1.0
		N = self.kwargs['kwargs']

		# Variables.
		inside, outside = np.zeros(2, int)
		#location = np.random.rand(2)
		location = [random.random(), random.random()]

		# Check if this is in or out of the circle N times.
		for i in range(N):
			if self._is_inside_circle(location, radius):
				inside = inside + 1
			else:
				outside = outside + 1
			#location = np.random.rand(2)
			location = [random.random(), random.random()]
		time_elapsed = time.time() - time_start
		results = [inside, outside, time_elapsed]
		self.queue.put(results)
