from random import seed

from actor import *
from population import *

gd1 = GroupDescription(5, 0.0, 0.3, 0.1, 0.3, "AMC")
gd2 = GroupDescription(5, 0.0, 0.3, 0.1, 0.3, "DNM")
gd3 = GroupDescription(2, 1.0, 0.3, 0.0, 0.3, "UOM")

pop = Population([gd1, gd2, gd3])
print(pop)