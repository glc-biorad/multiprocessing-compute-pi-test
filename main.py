import argparse as ap
import multiprocessing as mp
import random
import math
import numpy as np
import time

from processor import Processor

if __name__ == '__main__':
	# Constants
	N = 10000000
	nprocs_max = mp.cpu_count()
	choices_nprocs = [(i + 1) for i in range(nprocs_max)]
	pi = 4.0 * math.atan(1.0)
	time_start = time.time()

	# Variables
	processes = list()
	queue = mp.Queue()
	inside, outside = np.zeros(2)
	err = 0

	# Parser
	parser = ap.ArgumentParser()	
	parser.add_argument('-p', '--nprocs', dest='nprocs', default=1, help="number of processors to use [defualt: {0}, Max: {1}]".format(1, nprocs_max))
	parser.add_argument('-r', '--nruns', dest='nruns', default=N, help="number of runs to use [defualt: {0}]".format(N))
	args = parser.parse_args()
	nprocs = int(args.nprocs)
	nruns = int(args.nruns)

	# Compute pi
	for i in range(0, nprocs):
		processor = Processor(pid=i, queue=queue, kwargs=int(nruns/nprocs))
		processor.start()
		processes.append(processor)

	# Join.
	[proc.join() for proc in processes]
	while not queue.empty():
		proc_inside, proc_outside, proc_time = queue.get()
		inside, outside = [int(inside + proc_inside), int(outside + proc_outside)]
	pi_estimate = (4.0 * inside) / (inside + outside)
	err = abs(pi - pi_estimate)
	print(f"Pi: {pi}\nEstimate Pi: {pi_estimate}\nError: {err}")
	print("Elapsed Time: {:.2f} s".format(time.time() - time_start))
