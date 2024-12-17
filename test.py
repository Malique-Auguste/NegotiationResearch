from random import seed

from actor import *
from population import *

seed(1)

gd1 = GroupDescription(190, 0.0, 0.4, 0.3, 0.3, "AMC")
gd2 = GroupDescription(10, 1.0, 0.4, 0.0, 0.3, "DNM")

pop = Population([gd1, gd2])

for i in range(0, 20):
    pop.iterate()

policies_passed = 0
for log in pop.logs:
    if log.votes != (None, None) and log.votes[0] > log.votes[1]:
        policies_passed += 1
    print(log)
    print()

print(f"Policies Passed: {policies_passed}")