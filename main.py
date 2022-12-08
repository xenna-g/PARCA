from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        n = self.read_input()
        step = n / len(self.workers)
        mapped = []
        odd = len(self.workers) - 1

        for i in xrange(0, len(self.workers)-1):
            mapped.append(self.workers[i].mymap(i * step, i * step + step))


        mapped.append(self.workers[odd].mymap(odd * step, n))

        print('Map finished: ', mapped)

        reduced = self.myreduce(mapped)
        print("Reduce finished: " + str(reduced))

        self.write_output(reduced)
        print("Job Finished")

    @staticmethod
    @expose
    def mymap(a, b):
        print (a, b)
        res = float(1.0)
        for k in range(a, b):
            if k != 0:
                res *= (float(2*k)**2)/float((2*k-1)*(2*k+1))
        return res

    @staticmethod
    @expose
    def myreduce(mapped):
        output = float(1.0)
        for x in mapped:
            output *= float(x.value)
        return 2*output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readline()
        f.close()
        return int(line)

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()