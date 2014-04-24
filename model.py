import sklearn

class DataAggregator:
    x = 1
    y = None

    def p(self):
        print self.x

t1 = DataAggregator()
t2 = DataAggregator()

print t1.x
print t2.x

t1.x=2

print t1.x
print t2.x

t1.p()
t2.p()
