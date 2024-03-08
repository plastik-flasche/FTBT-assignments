import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib

class OriginalGeneralElectricRules:
    def __init__(self, line, name):
        self.line = line
        self.name = name
        self.mean = np.mean(line)
        self.sigma = np.std(line, ddof=1)  # Sample standard deviation
        self.normalized_line = (line - self.mean) / self.sigma
        self.index = np.arange(1, len(line)+1)
        self._compute_failures()

    def _compute_failures(self):
        self.fail_reasons = {}

        # Rule 1: Check for points outside Sigma 3 zone
        for i, value in enumerate(self.normalized_line):
            if self._count_exceeding(self.normalized_line[i:i+1], 3) >= 1:
                if i+1 not in self.fail_reasons:
                    self.fail_reasons[i+1] = []
                self.fail_reasons[i+1].append("Rule 1")

        # Rule 2: Check for 2 out of 3 consecutive points outside Sigma 2 zone
        for i in range(len(self.normalized_line) - 2):
            if self._count_exceeding(self.normalized_line[i:i+3], 2) >= 2:
                for j in range(i+1, i+4):
                    if j not in self.fail_reasons:
                        self.fail_reasons[j] = []
                    self.fail_reasons[j].append("Rule 2")

        # Rule 3: Check for 4 out of 5 consecutive points outside Sigma 1 zone
        for i in range(len(self.normalized_line) - 4):
            if self._count_exceeding(self.normalized_line[i:i+5], 1) >= 4:
                for j in range(i+1, i+6):
                    if j not in self.fail_reasons:
                        self.fail_reasons[j] = []
                    self.fail_reasons[j].append("Rule 3")

        # Rule 4: Check for 8 consecutive points on the same side of the average
        for i in range(len(self.normalized_line) - 7):
            if all(value > 0 for value in self.normalized_line[i:i+8]) or all(value < 0 for value in self.normalized_line[i:i+8]):
                for j in range(i+1, i+9):
                    if j not in self.fail_reasons:
                        self.fail_reasons[j] = []
                    self.fail_reasons[j].append("Rule 4")

    def _count_exceeding(self, range, sigma):
        return sum(value > sigma or value < -sigma for value in range)

    def output(self):
        # Sigma zones calculation
        zone_c_upper = self.mean + self.sigma
        zone_c_lower = self.mean - self.sigma
        zone_b_upper = self.mean + 2*self.sigma
        zone_b_lower = self.mean - 2*self.sigma
        zone_upper = self.mean + 3*self.sigma
        zone_lower = self.mean - 3*self.sigma

        # Plot setup
        plt.figure(figsize=(10, 6))
        plt.axhline(y=self.mean, color='green', linestyle='-', label='Mittel')

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