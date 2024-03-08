import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib

class SchoolBook:
	def __init__(self, line, name, setpoint, tolerance):
		self.line = line
		self.name = name
		self.setpoint = setpoint
		self.tolerance = tolerance
		self.normalized_line = (np.array(line) - setpoint) / tolerance
		self.index = np.arange(1, len(line)+1)
		self._compute_failures()

	def _compute_failures(self):
		self.fail_reasons = {}

		# Rule 1: Check for points outside specified tolerance
		for i, value in enumerate(self.normalized_line):
			if self._count_exceeding(self.normalized_line[i:i+1], 1) >= 1:
				if i+1 not in self.fail_reasons:
					self.fail_reasons[i+1] = []
				self.fail_reasons[i+1].append("Rule 1")

		
		# Rule 2: Check for 8 consecutive points on the same side of the average
		for i in range(len(self.normalized_line) - 6):
			if all(value > 0 for value in self.normalized_line[i:i+7]) or all(value < 0 for value in self.normalized_line[i:i+7]):
				for j in range(i+1, i+8):
					if j not in self.fail_reasons:
						self.fail_reasons[j] = []
					self.fail_reasons[j].append("Rule 2")

		# Rule 3: Check for 2 out of 3 consecutive points outside 2/3 of the tolerances
		for i in range(len(self.normalized_line) - 2):
			if self._count_exceeding(self.normalized_line[i:i+3], 0.66) >= 2:
				for j in range(i+1, i+4):
					if j not in self.fail_reasons:
						self.fail_reasons[j] = []
					self.fail_reasons[j].append("Rule 3")

		# Rule 4: Check for 4 out of 5 consecutive points outside 1/3 of the tolerances
		for i in range(len(self.normalized_line) - 4):
			if self._count_exceeding(self.normalized_line[i:i+5], 0.33) >= 4:
				for j in range(i+1, i+6):
					if j not in self.fail_reasons:
						self.fail_reasons[j] = []
					self.fail_reasons[j].append("Rule 4")

	def _count_exceeding(self, range, sigma):
		return sum(value > sigma or value < -sigma for value in range)

	def output(self):
		# Sigma zones calculation
		zone_c_upper = self.setpoint + 0.33*self.tolerance
		zone_c_lower = self.setpoint - 0.33*self.tolerance
		zone_b_upper = self.setpoint + 0.66*self.tolerance
		zone_b_lower = self.setpoint - 0.66*self.tolerance
		zone_upper = self.setpoint + self.tolerance
		zone_lower = self.setpoint - self.tolerance

		# Plot setup
		plt.figure(figsize=(10, 6))
		plt.axhline(y=self.setpoint, color='green', linestyle='-', label='Sollwert')

		# Sigma zones
		plt.fill_between(self.index, zone_c_lower, zone_c_upper, color='green', alpha=0.5, label='Zone C')
		plt.fill_between(self.index, zone_b_lower, zone_c_lower, color='blue', alpha=0.5, label='Zone B')
		plt.fill_between(self.index, zone_c_upper, zone_b_upper, color='blue', alpha=0.5)
		plt.fill_between(self.index, zone_b_upper, zone_upper, color='red', alpha=0.5, label='Zone A')
		plt.fill_between(self.index, zone_b_lower, zone_lower, color='red', alpha=0.5)

		# Mark dataset failure
		if (self.fail_reasons):
			plt.title(f"{self.name} (FAIL)", color='red')
		else:
			plt.title(f"{self.name} (PASS)", color='green')

		# First, draw line segments
		for idx in range(1, len(self.line)):
			# Determine failure status for current and previous points
			curr_fail = idx + 1 in self.fail_reasons
			prev_fail = idx in self.fail_reasons

			# Determine line color
			if curr_fail and prev_fail:
				line_color = 'red'
			elif not curr_fail and not prev_fail:
				line_color = 'blue'
			else:
				line_color = 'black'

			plt.plot(self.index[idx-1:idx+1], self.line[idx-1:idx+1], linestyle='-', color=line_color, zorder=1)

		# Then, plot points to ensure they appear on top
		for idx, val in enumerate(self.line, start=1):
			is_fail = idx in self.fail_reasons
			point_color = 'red' if is_fail else 'blue'
			plt.plot(self.index[idx-1:idx], self.line[idx-1:idx], marker='o', linestyle='', color=point_color, zorder=2)


		plt.xlabel('Index')
		plt.ylabel('Wert')
		plt.legend()
		plt.grid(True)
		# tikzplotlib.save(file_name)
		tikz_code = tikzplotlib.get_tikz_code()
		print(tikz_code)