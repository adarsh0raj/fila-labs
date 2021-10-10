import argparse
import warnings
import numpy as np
warnings.filterwarnings("ignore", category = RuntimeWarning)        # ignore runtime warnings

parser = argparse.ArgumentParser()
parser.add_argument("--value-policy", type=str, required=True)
parser.add_argument("--states", type=str, required=True)
parser.add_argument("--player-id", type=int, required=True)
args = parser.parse_args()


state_file = open(args.states, "r")
states = []

for line in state_file:
    states.append(str(line)[:9])

policy_file = open(args.value_policy, "r")
n = len(states)

print(args.player_id)
i = 0
for line in policy_file:
    temp = [0.0 for x in range(9)]
    y = int(line.split(" ")[-1])
    temp[y] = 1.0
    try:
        print(states[i], temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8])
        i += 1
    except:
        break

    
