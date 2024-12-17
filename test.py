from random import seed

from actor import *
from population import *


NUM_SEEDS = 3

MAX_POPULATION = 200
RATIO_CHANGE = 0.05
NUM_PROPOSALS = 20
SMALL_AVG_RANGE = int(NUM_PROPOSALS * 0.2)

GROUP1_SVO = 1.0
GROUP2_SVO = 1.0
SD = 0.4
GROUP1_SVO_DELTA = 0.
GROUP2_SVO_DELTA = 0.

FILE_NAME = "output.txt"

output = ""

seed_avgs = {}
for seed_num in range(0, NUM_SEEDS):
    seed(seed_num)
    for group1_num_actors in range(0, MAX_POPULATION, int(MAX_POPULATION * RATIO_CHANGE)):
        groups = []
        
        if group1_num_actors != 0:
            groups.append(GroupDescription(group1_num_actors, GROUP1_SVO, SD, GROUP1_SVO_DELTA, "Group1"))
        if group1_num_actors != MAX_POPULATION:
            groups.append(GroupDescription(MAX_POPULATION - group1_num_actors, GROUP2_SVO, SD, GROUP2_SVO_DELTA, "Group2"))

        pop = Population(groups)
        for i in range(0, NUM_PROPOSALS):
            pop.iterate()

        total_avg_svo = 0.0
        small_avg_svo = 0.0
        policies_passed = 0
        avg_votes_diff = 0.0

        for i in range(1, len(pop.logs)):
            log = pop.logs[i]

            total_avg_svo += log.avg_svo

            if i <= SMALL_AVG_RANGE:
                small_avg_svo += log.avg_svo

            if log.votes[0] > log.votes[1]:
                policies_passed += 1

            avg_votes_diff = abs(log.votes[0] - log.votes[1])

        total_avg_svo /= NUM_PROPOSALS
        small_avg_svo /= SMALL_AVG_RANGE
        avg_votes_diff /= NUM_PROPOSALS

        if (group1_num_actors / MAX_POPULATION) in seed_avgs:
            seed_avgs[group1_num_actors / MAX_POPULATION][0] += total_avg_svo
            seed_avgs[group1_num_actors / MAX_POPULATION][1] += small_avg_svo
            seed_avgs[group1_num_actors / MAX_POPULATION][2] += policies_passed
            seed_avgs[group1_num_actors / MAX_POPULATION][3] += avg_votes_diff

        else:
            seed_avgs[group1_num_actors / MAX_POPULATION] = [total_avg_svo, small_avg_svo, policies_passed, avg_votes_diff]




for key,value in seed_avgs.items():
    output += f"{key:.2f}\t"

    output += f"{(value[0]/NUM_SEEDS):.2f}\t"
    output += f"{(value[1]/NUM_SEEDS):.2f}\t"
    output += f"{(value[2]/NUM_SEEDS):.2f}\t"
    output += f"{(value[3]/NUM_SEEDS):.2f}\n"


f = open(FILE_NAME, "w")
f.write(output)
f.close()