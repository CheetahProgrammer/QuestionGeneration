import random
import datetime

#linear interpolation, so that (a, x, b) form the same ratios as (A, y, B)
def linear_interpolation(a, x, b, A, B):
    y = A + (B - A) *  (x - a) / (b - a)
    return y

#TODO make randomising more modal (triangular, normal?)
#TODO make the same functions for ungrouped frequency tables
class GroupedFrequencyTable:

    def __init__(self, freqs = [], bdrs = []):
        
        self.groups = []
        self.n = 0

        for i in range(len(freqs)):
            f = freqs[i]
            self.n += f
            
            a, b = bdrs[i]
            
            self.groups.append(GroupedFrequencyTable.DataGroup(a, b, f))
   
    class DataGroup:

        def __init__(self, a, b, f):    
            self.a = a
            self.b = b
            self.f = f

    def printout(self):
        
        for dg in self.groups:
            print("Class {a} to {b}, frequency {f}".format(a = round(dg.a, 2), b = round(dg.b, 2), f = dg.f))

    def compute_class_boundaries(self, extend_boundary = True):
        
        for i in range(len(self.groups)):
            if(i == 0 and i == len(self.groups) - 1):
                self.groups[i].lb = self.groups[i].a
                self.groups[i].rb = self.groups[i].b
            elif(i == 0):
                if(extend_boundary):
                    self.groups[i].lb = self.groups[i].a - (self.groups[i+1].a - self.groups[i].b) / 2
                else:
                    self.groups[i].lb = self.groups[i].a
                self.groups[i].rb = (self.groups[i].b + self.groups[i+1].a) / 2
            elif(i == len(self.groups) - 1):
                self.groups[i].lb = (self.groups[i-1].b + self.groups[i].a) / 2
                if(extend_boundary):
                    self.groups[i].rb = self.groups[i].b + (self.groups[i].a - self.groups[i-1].b) / 2
                else:
                    self.groups[i].rb = self.groups[i].b
            else:
                self.groups[i].lb = (self.groups[i-1].b + self.groups[i].a) / 2
                self.groups[i].rb = (self.groups[i].b + self.groups[i+1].a) / 2

    #estimate element on the position pos
    def estimate_element(self, pos, extend_boundary = True):

        self.compute_class_boundaries(extend_boundary)

        cum_freq_l = 0
        cum_freq_r = 0
        for i in range(len(self.groups)):
            cum_freq_l = cum_freq_r
            cum_freq_r = cum_freq_l + self.groups[i].f

            if cum_freq_l < pos and pos <= cum_freq_r:
                
                return linear_interpolation(cum_freq_l , pos, cum_freq_r,
                                            self.groups[i].lb, self.groups[i].rb)

    
    def estimate_mean_var_std(self, extend_boundary = True):
        
        self.compute_class_boundaries(extend_boundary)

        est_sum = 0
        est_sum_sq = 0

        for group in self.groups:
            x = (group.lb + group.rb) / 2
            est_sum += group.f * x
            est_sum_sq += group.f * (x ** 2)

        est_mean = est_sum / self.n
        est_mean_sq = est_sum_sq / self.n
        est_var = est_mean_sq - est_mean ** 2
        est_std = est_var ** 0.5

        return est_mean, est_var, est_std

    #returns latex code representing the grouped frequency table
    def latex_table(self, precision = 2, vertical = False):

        #number of datagroups
        data_cols = len(self.groups)

        #start of table

        if vertical:
            pass
            # code_prefix = """\begin{table}[]\r\n\\begin{tabular}{"""
        if(not vertical):
            code_prefix = """\\begin{table}[]\r\n\\begin{tabular}{|l|""" + data_cols * "c|" + "}\r\n\\hline\r\n"
            
            first_row = """\\textbf{Data, $x$}"""
            for group in self.groups:
                first_row += "& " + "${a}\\leq x < {b}$".format(a=round(group.a, precision), 
                                                                b=round(group.b, precision))
            first_row += "\\\\ \\hline\r\n"

            second_row = """\\textbf{Frequency}"""
            for group in self.groups:
                second_row += "& " + str(group.f)
            second_row += "\\\\ \\hline\r\n"

            code_suffix = """\\end{tabular}\r\n\\end{table}\r\n"""
            
            result = code_prefix + first_row + second_row + code_suffix

        return result
    
    def randomize(self, seed_val = None, n_of_groups = None):
        if(seed_val != None):
            random.seed(seed_val)
        else:
            random.seed(datetime.datetime.now().timestamp())

        if(n_of_groups == None):
            n_of_groups = random.randint(6, 10)
        
        magnitude = random.choice([-2, -1, 0, 1, 2, 3])
        width = random.randint(2, 5) * (10 ** magnitude)
        gap = 10 ** magnitude

        if(magnitude >= 0):
            start = random.randint(1, 9) * (10 ** magnitude)
        else:
            start = random.randint(1, 9)

        current_left = start
        self.groups = []
        self.n = 0
        for i in range(n_of_groups):
            f = random.randint(10, 20)
            self.groups.append(GroupedFrequencyTable.DataGroup(current_left, current_left + width, f))
            self.n += f
            current_left += width + gap



# gpf = GroupedFrequencyTable([12, 23, 3], [(10, 20), (30, 40), (50, 60)])
# gpf = GroupedFrequencyTable([2, 10], [(1,2),(2,3)])
# gpf = GroupedFrequencyTable([3, 6, 10, 7, 5], [(300, 349), (350, 399), (400, 449), (450, 499), (500, 549)])
# gpf = GroupedFrequencyTable([5, 10, 26, 8, 1], [(90, 95), (95, 100), (100, 105), (105, 110), (110, 115)])
# gpf = GroupedFrequencyTable([5, 10, 36, 20, 9], [(20, 29), (30, 39), (40, 49), (50, 59), (60, 69)])
# gpf = GroupedFrequencyTable([4, 8, 6, 7, 5, 1], [(4, 8), (8, 10), (10, 11), (11, 12), (12, 15), (15, 16)])
gpf = GroupedFrequencyTable()
gpf.randomize()

gpf.printout()

def boundaries_presentation(table):
    print("No extension of boundaries")
    table.compute_class_boundaries(extend_boundary = False)
    for g in table.groups:
        print("Class boundaries: {a}, {b}".format(a=round(g.lb, 2), b=round(g.rb, 2)))

    print("Extension of boundaries")
    table.compute_class_boundaries(extend_boundary = True)
    for g in table.groups:
        print("Class boundaries: {a}, {b}".format(a=round(g.lb, 2), b=round(g.rb, 2)))

boundaries_presentation(gpf)

print(gpf.latex_table())
#gpf = GroupedFrequencyTable([2, 25, 30, 13], [(30, 31), (32, 33), (34, 36), (37, 39)])
# for i in range(1, gpf.n+1) :
    # print("Estimated {i}th element: {x}".format(i=i, x=gpf.estimate_element(i)))

print("n = " + str(gpf.n))
Q1 = gpf.estimate_element(gpf.n/4, extend_boundary = True)
print("Q1 = " + str(Q1))
Q2 = gpf.estimate_element(gpf.n/2, extend_boundary = True)
print("Q2 = " + str(Q2))
Q3 = gpf.estimate_element(3*gpf.n/4, extend_boundary = True)
print("Q3 = " + str(Q3))
IQR = Q3 - Q1
print("IQR = " + str(IQR))

m, v, s = gpf.estimate_mean_var_std(extend_boundary = True)
print("Estimated mean = " + str(m))
print("Estimated variance = " + str(v))
print("Estimated standard deviation = " + str(s))


# single_class_example = GroupedFrequencyTable([100], [(500, 1000)])
# boundaries_presentation(single_class_example)

