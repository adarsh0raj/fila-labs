import argparse
import warnings
import numpy as np
warnings.filterwarnings("ignore", category = RuntimeWarning)        # ignore runtime warnings

def check_term_state(state, player):
    for row in [0, 3, 6]:
        if state[row] == state[row+1] and state[row] == state[row+2] and state[row] == str(player):
            return "lose"
        elif state[row] == state[row+1] and state[row] == state[row+2] and state[row] != '0':
            return "win"

    for col in range(3):
        if state[col] == state[col+3] and state[col] == state[col+6] and state[col] == str(player):
            return "lose"
        elif state[col] == state[col+3] and state[col] == state[col+6] and state[col] != '0':
            return "win"
    
    if state[0] == state[4] and state[4] == state[8] and state[4] == str(player): 
        return "lose"
    elif state[0] == state[4] and state[4] == state[8] and state[4] != '0':
        return "win"

    if state[2] == state[4] and state[4] == state[6] and state[4] == str(player):
        return "lose"
    elif state[2] == state[4] and state[4] == state[6] and state[4] != '0':
        return "win"
    
    if '0' not in state:
        return "draw"
        
    return "valid"
        
parser = argparse.ArgumentParser()
parser.add_argument("--policy", type=str, required=True)
parser.add_argument("--states", type=str, required=True)
args = parser.parse_args()

policy_file = open(args.policy, "r")
state_file = open(args.states, "r")

numStates = 0
numActions = 9
fixed_player = int(policy_file.readline())
policy = dict()

for x in policy_file.readlines():
    y = x.split(" ")
    policy[str(y[0])] = [float(y[i]) for i in range(1,10)]

states = dict()
for line in state_file:
    numStates += 1
    states[str(line)[:9]] = (numStates - 1)

end = numStates
numStates += 1
mdptype = "episodic"

transition = dict()

state_file.seek(0)

if fixed_player == 2:

    for line in state_file:
        s1 = str(line)[:9]
        for a1 in range(9):
            if s1[a1] == '0':
                s2 = s1[:a1] + '1' + s1[a1+1:]
                res = check_term_state(s2, 1)

                if res == "win":
                    transition[(states[s1], a1)] = [end, float(1), float(1)]
                elif res == "lose" or res == "draw":
                    transition[(states[s1], a1)] = [end, float(0), float(1)]
                elif res == "valid":
                    for a2 in range(9):
                        if s2[a2] == '0' and policy[s2][a2] != 0:
                            s3 = s2[:a2] + '2' + s2[a2+1:]
                            res2 = check_term_state(s3, 2)

                            if res2 == "lose" or res == "draw":
                                transition[(states[s1], a1)] = [end, float(1), policy[s2][a2]]
                            elif res2 == "valid":
                                transition[(states[s1], a1)] = [states[s3], float(0), policy[s2][a2]]

else:
    for line in state_file:
        s1 = str(line)[:9]
        for a1 in range(9):
            if s1[a1] == '0':
                s2 = s1[:a1] + '1' + s1[a1+1:]
                res = check_term_state(s2, 1)

                if res == "win":
                    transition[(states[s1], a1)] = [end, float(1), float(1)]
                elif res == "lose" or res == "draw":
                    transition[(states[s1], a1)] = [end, float(0), float(1)]
                elif res == "valid":
                    for a2 in range(9):
                        if s2[a2] == '0' and policy[s2][a2] != 0:
                            s3 = s2[:a2] + '2' + s2[a2+1:]
                            res2 = check_term_state(s3, 2)

                            if res2 == "lose" or res == "draw":
                                transition[(states[s1], a1)] = [end, float(1), policy[s2][a2]]
                            elif res2 == "valid":
                                transition[(states[s1], a1)] = [states[s3], float(0), policy[s2][a2]]

print("numStates", numStates)
print("numActions", numActions)
print("end", end)
for key in transition.keys():
    print("transition", key[0], key[1], transition[key][0], int(transition[key][1]), transition[key][2])  
print("mdptype", "episodic")
print("discount", 1)
        












