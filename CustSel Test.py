import random
import time
import numpy as np
import matplotlib.pyplot as plt


class RnadObj:
    def __init__(self, value):
        self.value = value
        self.match = ""


avgTimes = []

lSize = 5000
reps = 20


def test():
    l1 = [RnadObj(random.randint(1, 1_000_000)) for _ in range(lSize)]
    l2 = [RnadObj(random.randint(1, 1_000_000)) for _ in range(lSize)]

    start_time = time.time_ns()//1_000_000

    for feature1 in l1:
        for feature2 in l2:
            if feature1.value == feature2.value:
                # Set the Match field to 'match' if the fields match
                feature1.match = "match"
                feature2.match = "match"
            else:
                # Set the Match field to 'no match' if the fields don't match
                feature1.match = "match"
                feature2.match = "match"

    end_time = time.time_ns()//1_000_000

    execution_time = end_time - start_time
    print('Execution time in seconds:', execution_time/1000)
    avgTimes.append(execution_time)


for i in range(reps):
    test()

print("The average time is:", np.mean(avgTimes) /
      1000, "s for ", lSize, " list Size")

x = np.arange(0, reps, 1)

rangeArr = []

for i in range(reps):
    rangeArr.append(np.mean(avgTimes))


plt.plot(x, avgTimes)
plt.plot(x, rangeArr)
plt.show()
