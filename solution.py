from os import stat
import random
import time
import math
from Pyro4 import expose


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        length = self.read_input()
        array_numbers = []
        step = length / len(self.workers)
        
        start = time.time()
        for i in range(length): 
            array_numbers.append(random.randint(1,length*100)) 
        end = time.time()
        
        mapped = []
        for i in range(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(array_numbers[i * step: i * step + step]))

        reduced = self.myreduce(mapped)
        self.write_output(reduced)
        self.write_output(start - end)

    @staticmethod
    @expose
    def mymap(array):
        minNum = array[0]
        for num in array:
            if num < minNum:
                minNum = num
        return minNum

    @staticmethod
    @expose
    def myreduce(mapped):
        res = mapped[0].value
        for num in mapped:
            if num.value < res:
                res = num.value
        return res

    def read_input(self):
        with open(self.input_file_name, 'r') as f:
            n = int(next(f))
        return n

    def write_output(self, output):
        with open(self.output_file_name, 'a') as f:
            f.write(str(output))
            f.write('\n')
