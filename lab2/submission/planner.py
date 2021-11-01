import argparse
import pulp
import warnings
import numpy as np
from copy import deepcopy
warnings.filterwarnings("ignore", category = RuntimeWarning)        # ignore runtime warnings

def calc_action_val(v, s, a, transition, discount):
    try:
        return sum([b[2]*(b[1] + discount*v[b[0]]) for b in transition[(s,a)]])
    except:
        return -1

def calc_val(states, actions, pi, transition, discount, end):

    A = np.zeros((states, states))
    B = np.zeros(states)
    for s in range(states):
        A[s, s] += 1
        if s in end or (s, pi[s]) not in transition.keys():
            continue
        else:
            for branch in transition[(s, pi[s])]:
                B[s] += branch[2]*branch[1]
                A[s, branch[0]] -= (branch[2] * discount)

    v = np.linalg.solve(A, B)
    return v

def vi(states, actions, transition, discount, end):
    v_prev = np.ones(states)
    v = np.zeros(states)
    pi = np.zeros(states, dtype=int)
    prec = 1e-10

    while np.linalg.norm(v-v_prev) > prec:

        v_prev = deepcopy(v)
        for s in range(states):

            vals = np.zeros(actions)
            for a in range(actions):
                try:
                    vals[a] += sum([b[2]*(b[1] + discount*v_prev[b[0]]) for b in transition[(s,a)]])
                except:
                    continue

            v[s]  = np.max(vals)
            pi[s]  = np.argmax(vals)
        
    return v, pi

def lp(states, actions, transition, discount, end):

    problem = pulp.LpProblem("LinearProgrammingValueCalc", pulp.LpMinimize)
    lp_vars = [pulp.LpVariable(str(s)) for s in range(states)]
    problem += sum(lp_vars)

    for s in range(states):
        for a in range(actions):
            try:
                problem += (lp_vars[s] >= pulp.lpSum([b[2]*(b[1] + discount*lp_vars[b[0]]) for b in transition[(s,a)]]))
            except:
                continue
    
    if not end == [-1]:
        for s in end:
            problem += (lp_vars[s] == 0)
    
    value = problem.solve(pulp.PULP_CBC_CMD(msg=0))
    v = np.zeros(states)
    pi = np.zeros(states, dtype=int)

    for var in problem.variables():
        v[int(var.name)] = var.varValue
    
    for s in range(states):
        q = [calc_action_val(v, s, a, transition, discount) for a in range(actions)]
        ac = np.argmax(q)
        pi[s] = ac

    return v, pi

def hpi(states, actions, transition, discount, end):

    pi = np.random.randint(0, actions, size=states)
    while True:
        v = calc_val(states, actions, pi, transition, discount, end)
        temp_pi = deepcopy(pi)
        for s in range(states):
            q = np.array([calc_action_val(v, s, a, transition, discount) for a in range(actions)])
            temp_pi[s] = np.argmax(q - (v[s] + 1e-6))

        if (temp_pi == pi).all():
            break
        pi = deepcopy(temp_pi)

    v = calc_val(states, actions, pi, transition, discount, end)
    return v, pi
    
parser = argparse.ArgumentParser()
parser.add_argument("--mdp", type=str, required=True)
parser.add_argument("--algorithm", type=str, default="lp")
args = parser.parse_args()

mdp_file = open(args.mdp, "r")
states = int(mdp_file.readline().split(" ")[-1])
actions = int(mdp_file.readline().split(" ")[-1])
end = [int(x) for x in mdp_file.readline().split(" ")[1:]]
transition = dict()

for x in mdp_file.readlines():
    y = x.split(" ")
    if y[0] == "transition":
        if (int(y[1]), int(y[2])) not in transition.keys():
            transition[(int(y[1]), int(y[2]))] = [[int(y[3]), float(y[-2]), float(y[-1])]]
        else:
            transition[(int(y[1]), int(y[2]))].append([int(y[3]), float(y[-2]), float(y[-1])])
        continue
    elif y[0] == "mdptype":
        mdptype = str(y[-1][:-1])
        continue
    elif y[0] == "discount":
        discount = np.double(y[-1])

if args.algorithm == "vi":
    val, pi = vi(states, actions, transition, discount, end)
elif args.algorithm == "hpi":
    val, pi = hpi(states, actions, transition, discount, end)
elif args.algorithm == "lp":
    val, pi = lp(states, actions, transition, discount, end)
else:
    val, pi = lp(states, actions, transition, discount, end)

for i in range(states):
    print("{:.6f}".format(val[i]), pi[i])



