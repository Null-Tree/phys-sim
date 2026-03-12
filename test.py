
import time

class TestClass:
    def __init__(self):
        self.dict={1:1}
    def __getitem__(self, key):
        # return self.dict[key]

        # try:
        #     return self.dict[key]
        # except:
        #     raise Exception()

        if key in list(self.dict.keys()):
            return self.dict[key]

d=TestClass()

st=time.time()
for i in range(1000000):
    a=d[1]
et=time.time()
print(et-st)

print(list(4))