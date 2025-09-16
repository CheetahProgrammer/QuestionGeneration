#TODO rounding to 2sf and 3sf

#linear interpolation, so that (a, x, b) form the same ratios as (A, y, B)
def linear_interpolation(a, x, b, A, B):
    y = A + (B - A) *  (x - a) / (b - a)
    return y

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
            print("Class {a} to {b}, frequency {f}".format(a = dg.a, b = dg.b, f = dg.f))
            
    #estimate element on the position pos
    def estimate_element(self, pos, extend_boundary = True):

        cum_freq_l = 0
        cum_freq_r = 0
        for i in range(len(self.groups)):
            cum_freq_l = cum_freq_r
            cum_freq_r = cum_freq_l + self.groups[i].f

            if cum_freq_l < pos and pos <= cum_freq_r:
                
                if(i == 0):
                    bound_prev = None
                    extend_left = None
                else:
                    bound_prev = self.groups[i-1].b
                    extend_left = (self.groups[i].a - bound_prev)/2
                
                if(i == len(self.groups) - 1):
                    bound_next = None
                    extend_right = None
                else:
                    bound_next = self.groups[i+1].a
                    extend_right = (bound_next - self.groups[i].b)/2

                # print("Cases")
                if(extend_right == None and extend_right == None):
                    # print("C1")
                    extend_right = 0
                    extend_left = 0
                elif(extend_left == None):
                    # print("C2")
                    if(extend_boundary):
                        extend_left = extend_right
                    else:
                        extend_left = 0
                elif(extend_right == None):
                    # print("C3")
                    if(extend_boundary):
                        extend_right = extend_left
                    else:
                        extend_right = 0
                
                res = linear_interpolation(cum_freq_l , pos, cum_freq_r, 
                                           self.groups[i].a - extend_left, self.groups[i].b + extend_right)

                return res
    
    def estimate_mean(self):
        
        n = self.n
        est_sum = 0

        for group in self.groups:
            pass

    #returns latex code representing the grouped frequency table
    def latex_table(self):

        #number of datagroups
        data_cols = len(self.groups)

        #start of table
        code_prefix = """\\begin{table}[]\r\n\\begin{tabular}{|l|""" + data_cols * "c|" + "}\r\n\\hline\r\n"
        
        first_row = """\\textbf{Data, $x$}"""
        for group in self.groups:
            first_row += "& " + "${a}\\leq x < {b}$".format(a=group.a, b=group.b)
        first_row += "\\\\ \\hline\r\n"

        second_row = """\\textbf{Frequency}"""
        for group in self.groups:
            second_row += "& " + str(group.f)
        second_row += "\\\\ \\hline\r\n"

        code_suffix = """\\end{tabular}\r\n\\end{table}\r\n"""
        
        return code_prefix + first_row + second_row + code_suffix


    
# gpf = GroupedFrequencyTable([12, 23, 3], [(10, 20), (30, 40), (50, 60)])
# gpf = GroupedFrequencyTable([2, 10], [(1,2),(2,3)])
gpf = GroupedFrequencyTable([3, 6, 10, 7, 5], [(300, 349), (350, 399), (400, 449), (450, 499), (500, 549)])

print(gpf.latex_table())
#gpf = GroupedFrequencyTable([2, 25, 30, 13], [(30, 31), (32, 33), (34, 36), (37, 39)])
gpf.printout()
# for i in range(1, gpf.n+1) :
    # print("Estimated {i}th element: {x}".format(i=i, x=gpf.estimate_element(i)))

print("n = " + str(gpf.n))
print("Q1 = " + str(gpf.estimate_element(gpf.n/4, extend_boundary = True)))
print("Q2 = " + str(gpf.estimate_element(gpf.n/2, extend_boundary = True)))
print("Q3 = " + str(gpf.estimate_element(3*gpf.n/4, extend_boundary = True)))