import time
from function_record import *
from abstract_profiler import AbstractProfiler


class Profiler(AbstractProfiler):

    def __init__(self):
        self.records = {}
        self.callers_stack = []

    # search a record by name
    def get_record(self, functionName):
        if functionName not in self.records:
            self.records[functionName] = FunctionRecord(functionName)
        return self.records[functionName]

     # metodo se llama cada vez que se ejecuta una funcion
    def fun_call_start(self, functionName, args):
        record = self.get_record(functionName)
        record.start_times.append(time.time())
        record.freq += 1
        
        if record.previous_args != args and record.previous_args != 'EMPTY':
            record.is_cacheable = 0
        record.previous_args = args
        

        if self.callers_stack:
            current_caller = self.callers_stack[-1]
            if current_caller != functionName and current_caller not in record.callers:
                record.callers.append(current_caller)

        self.callers_stack.append(functionName)

    def fun_call_end(self, functionName, returnValue):
        record = self.get_record(functionName)
        record.end_times.append(time.time())
        if record.previous_return_val != returnValue and record.previous_return_val != 'EMPTY':
            record.is_cacheable = 0
        record.previous_return_val = returnValue
        self.callers_stack.pop()  # Eliminamos la función actual de la pila.

    # print report
    def print_fun_report(self):
        print("{:<30} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format('fun', 'freq', 'avg', 'max', 'min',
                                                                        'cache', 'callers'))
        for record in self.records.values():
            record.calculate_execution_times()
            record.print_report()
