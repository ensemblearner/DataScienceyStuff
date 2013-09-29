__author__ = 'Mohitdeep Singh'

class Pmf(object):
    
    def __init__(self, d=None):
        self.pmf = d if d else {}
        self.normalized = False

    def create_pmf(self, ele_list):
        for ele in ele_list:
            self.pmf[ele] = self.pmf.get(ele, 0) + 1

    def get_prob(self, key):
        return self.pmf.get(key, 0)

    def set_values(self, keys):
        self.create_pmf(keys)

    def normalize(self):
        total = sum(self.pmf.values())
        for k, v in self.pmf.items():
            self.pmf[k] = v/float(total)
        self.normalized = True

    def remove(self, key):
        self.pmf.pop(key, None)
        if self.normalized: self.normalize()

"""
pmf = Pmf()
pmf.create_pmf([1, 2, 3, 3, 4, 4, 4, 1])

print pmf.pmf
pmf.normalize()
print pmf.pmf
pmf.remove(2)
print pmf.pmf
pmf.remove(60)
print pmf.pmf
"""