class FunctionRecord:
    def __init__(self, funName):
        self.functionName = funName
        self.freq = 0
        self.callers = []
        self.start_times = []
        self.end_times = []
        self.times_execution = []
        self.max_time_execution = 0
        self.min_time_execution = 0
        self.avg_time_execution = 0
        self.is_cacheable = True
        self.previous_args = 'EMPTY'
        self.previous_return_val = 'EMPTY'

    def print_report(self):
        print("{:<30} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(self.functionName, str(self.freq), "{:.5f}".format(
            self.avg_time_execution), "{:.5f}".format(self.max_time_execution), "{:.5f}".format(self.min_time_execution), str(self.is_cacheable), str(self.callers)))

    def calculate_execution_times(self):
        for i in range(len(self.start_times)):
            self.times_execution.append(
                self.end_times[i] - self.start_times[i])
        self.max_time_execution = max(self.times_execution)
        self.min_time_execution = min(self.times_execution)
        self.avg_time_execution = sum(
            self.times_execution)/len(self.times_execution)
