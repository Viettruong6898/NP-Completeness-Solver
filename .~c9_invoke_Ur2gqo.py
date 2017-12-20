#!/usr/local/Cellar/pypy/5.9.0
from __future__ import print_function
import math
import random
from anneal import Annealer
from multiprocessing.dummy import Pool as ThreadPool 


class WizardSolver(Annealer):

    """Test annealer with a wizard sorting problem.
    """

    # pass extra data (the distance matrix) into the constructor
    
    # state = list of wizard names
    # constraints = list of constraints
    def __init__(self, state, constraints, constraint_dict):
        self.constraints = constraints
        self.constraint_dict = constraint_dict
        self.state = state
        self.previous_energy = 0
        super(WizardSolver, self).__init__(state)  # important!

    def move(self):
        """Swaps two wizards in the list."""
        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        wizard = self.state[a]

        #before you move wizard, how many of its constraints are broken?
        constraints_to_check = self.constraint_dict[wizard]
        num_of_constraints = len(constraints_to_check)
        num_violated = 0
        for i in range(num_of_constraints):
            constraint = constraints_to_check[i]
            if self.state.index(constraint[0]) < self.state.index(constraint[2]) and self.state.index(constraint[2]) < self.state.index(constraint[1]):
                num_violated += 1
            if self.state.index(constraint[1]) < self.state.index(constraint[2]) and self.state.index(constraint[2]) < self.state.index(constraint[0]):
                num_violated += 1

        self.state.remove(wizard)
        self.state.insert(b, wizard)
        return wizard, num_violated
        # self.state[a], self.state[b] = self.state[b], self.state[a]

    def all_energy(self):
        """Calculates the number of constraints violated""" 
        num_of_constraints = len(self.constraints)
        e =0
        for i in range(num_of_constraints):
            constraint = self.constraints[i]
            if self.state.index(constraint[0]) < self.state.index(constraint[2]) and self.state.index(constraint[2]) < self.state.index(constraint[1]):
                e += 1
            if self.state.index(constraint[1]) < self.state.index(constraint[2]) and self.state.index(constraint[2]) < self.state.index(constraint[0]):
                e += 1
        self.previous_energy = e
        return e

    def energy(self, wizard, original_num_violated):
        """Calculates the number of constraints violated""" 
        constraints_to_check = self.constraint_dict[wizard]
        num_of_constraints = len(constraints_to_check)
        num_violated =0
        for i in range(num_of_constraints):
            constraint = constraints_to_check[i]
            if self.state.index(constraint[0]) < self.state.index(constraint[2]) and self.state.index(constraint[2]) < self.state.index(constraint[1]):
                num_violated += 1
            if self.state.index(constraint[1]) < self.state.index(constraint[2]) and self.state.index(constraint[2]) < self.state.index(constraint[0]):
                num_violated += 1
        delta_violations = num_violated - original_num_violated
        # self.previous_energy += delta_violations
        # to_return = self.previous_energy
        # self.previous_energy = to_return
        return delta_violations
        
#-----------------------------------------------------------

with open("phase2_inputs/allsu/input20.in", "r") as f:
    read = []
    for line in f:
        read.append(line.strip())

# information we are given
num_of_wizards = read[0]
num_of_constraints = read[1]
constraints = []
wizards = set()
for line in read[2:]:
    for wizard in line.split():
        wizards.add(wizard)
    constraints.append(line.split())
state = list(wizards)

constraint_dict = {}
for wizard in wizards:
    specific_constraint_list = []
    for line in read[2:]:
        if wizard in line:
            constraint = []
            for each in line.split():
                constraint.append(each)
            specific_constraint_list.append(constraint)
    constraint_dict[wizard] = specific_constraint_list
# print(constraint_dict)

#state = ['d', 'm', 'g', 'q', 'f', 'n', 'r', 'o', 'h', 'i', 'a', 'j', 'e', 'k', 'b', 's', 'p', 'l', 'c', 't']

wiz = WizardSolver(state, constraints, constraint_dict)
auto_schedule = wiz.auto(minutes=3)
print(auto_schedule)
# {'tmin': ..., 'tmax': ..., 'steps': ...}
wiz.set_schedule(auto_schedule)


# Make the Pool of workers
# pool = ThreadPool(8) 
# Open the urls in their own threads
# and return the results
# results = pool.map(urllib2.urlopen, urls)
# close the pool and wait for the work to finish 
# pool.close()
# pool.join()


# wiz.Tmax = 75
# wiz.Tmin = .0005
# wiz.steps = 498200.0

best_state, energy = wiz.anneal()




# wiz.move()
# news= wiz.move()
# print(wiz.state)
# print(wiz.energy())

# wiz = WizardSolver(state, constraints)
# best_state, energy = wiz.anneal(num_of_constraints)

print (best_state)
print (energy)
print("Tmax: ", wiz.Tmax, "Tmin: ", wiz.Tmin, "Steps: ", wiz.steps)



