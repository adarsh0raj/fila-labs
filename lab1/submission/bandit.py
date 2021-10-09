import argparse
import sys
import math
import numpy as np
import warnings
from matplotlib import pyplot as plt
warnings.filterwarnings("ignore", category = RuntimeWarning)        # ignore runtime warnings

# Available Algorithms and Seeding
algorithms = ["epsilon-greedy-t1", "ucb-t1", "kl-ucb-t1", "thompson-sampling-t1", "ucb-t2", "alg-t3", "alg-t4"]

#print answer in correct format
def print_ans(ins, alg, rs, eps, sc, th, hor, reg, hi):
    print(ins+", "+alg+", "+str(rs)+", "+str(eps)+", "+str(sc)+", "+str(th)+", "+str(hor)+", "+str(reg)+", "+str(hi))

#random sample with a given probability p
def rand_samp(p):
    if np.random.uniform(0,1) < p:
        return 1
    else:
        return 0

# calculate KL(p,q)
def kl(p,q):
    if p == 0:
        p = 0.001
    if p == 1:
        p = 0.999
    if q == 0:
        q = 0.001
    if q == 1:
        q = 0.999
    
    return p*np.log(p/q) + (1-p)*np.log((1-p)/(1-q))


# Calculate UCB values and KL-ucb for given arm (depending on the flag, decide ucb-t1, kl-ucb or ucb-t2)
def calc_ucb(emp_mean, t, no_picks, flag, sc):
    if flag == 0:                                                    # ucb-t1
        return emp_mean + math.sqrt((2*np.log(t))/no_picks)
    elif flag == 1:                                                  #kl-ucb-t1
        c = 3
        err = 1.0e-3
        low = emp_mean
        high = 1.0
        val = (np.log(t) + c*np.log(np.log(t)))/no_picks
        mid = (low+high)/2.0

        while err < abs(high-low):
            if kl(emp_mean, mid) <= val:
                low = mid + err
            else:
                high = mid - err
            mid = (low+high)/2.0
        
        return mid
    else:                                                            # ucb-t2
        return emp_mean + math.sqrt((sc*np.log(t))/no_picks)
    
# Calculate Max Expected Reward for task 4, given instance file and threshold
def calc_max_exp_reward(support, probab, threshold):

    exp_rewards = np.zeros(len(probab))
    for i in range(len(support)):
        if support[i] > threshold:
            for j in range(len(probab)):
                exp_rewards[j] += probab[j][i]
    
    return max(exp_rewards)

# Epsilon Greedy Algorithm Implementation
def epsilon_greedy(instance, epsilon, horizon):

    n = len(instance)                          # No of arms
    count = np.zeros(n, dtype=int)             # Count for each arm how many times it was pulled
    arm_rewards = np.zeros(n)                  # rewards obtained by each arm
    emp_mean = np.zeros(n)                     # empirical mean of each arm
    cum_reward = 0                             # cumulative reward

    for i in range(horizon):                   

        idx = np.random.choice(n) if rand_samp(epsilon) else np.argmax(emp_mean)
        reward = rand_samp(instance[idx])
        cum_reward += reward
        arm_rewards[idx] += reward
        count[idx] += 1
        emp_mean[idx] = (arm_rewards[idx]/count[idx])

    return (horizon*max(instance) - cum_reward)

# UCB Algorithm (Kl and task2 depending on flag) (c = 3 for kl-ucb)
def ucb(instance, horizon, flag, sc):

    n = len(instance)                              # No of arms
    count = np.ones(n, dtype=int)                  # Count for each arm (set to one initially because of UCB)
    arm_rewards = np.zeros(n)                      # rewards obtained by each arm
    cum_reward = 0                                 # cumulative reward
    vec_calc = np.vectorize(calc_ucb)              # vectorize the calc_ucb function for np.arrays
    
    for i in range(n):
        rew = rand_samp(instance[i])
        cum_reward += rew
        arm_rewards[i] += rew

    for i in range(n, horizon):
        
        ucb = vec_calc(arm_rewards/count, i, count, flag, sc)
        idx = np.argmax(ucb)
        reward = rand_samp(instance[idx])
        cum_reward += reward
        arm_rewards[idx] += reward
        count[idx] += 1

    return (horizon*max(instance) - cum_reward)

# Thompson Sampling Algorithm 
def thompson(instance, horizon):
    n = len(instance)
    succ = np.zeros(n, dtype=int)          # success array
    fail = np.zeros(n, dtype=int)          # failure array

    cum_reward = 0
    for i in range(horizon):
        x = np.random.beta(succ+1, fail+1)
        idx = np.argmax(x)
        rew = rand_samp(instance[idx])
        cum_reward += rew
        succ[idx] += rew
        fail[idx] += (1-rew)
      
    return (horizon*max(instance) - cum_reward)

# Algorithm 3 (Modified Thompson Sampling)
def alg3(support, probab, horizon):
    n = len(probab)
    succ = np.zeros(n)
    fail = np.zeros(n)

    cum_reward = 0
    for i in range(horizon):
        x = np.random.beta(succ+1, fail+1)
        idx = np.argmax(x)
        choice = np.random.choice(support, p=probab[idx])
        succ[idx] += choice
        cum_reward += choice
        fail[idx] += (1-choice)
    
    support = np.array(support)
    probab = [np.array(x) for x in probab]
    exp_rewards = [np.dot(support, x) for x in probab]
    return (horizon*max(exp_rewards) - cum_reward)
      
# ALgotithm 4 (Thompson Algorithm with new definition of success and failure)
def alg4(support, probab, horizon, threshold):
    n = len(probab)
    succ = np.zeros(n)
    fail = np.zeros(n)
    high = 0
    cum_reward = 0

    for i in range(horizon):
        x = np.random.beta(succ+1, fail+1)
        idx = np.argmax(x)
        choice = np.random.choice(support, p=probab[idx])
        if choice > threshold:
            cum_reward += 1
            high += 1
            succ[idx] += 1
        else:
            fail[idx] += 1
    
    max_exp = calc_max_exp_reward(support, probab, threshold)
    return (horizon*max_exp - cum_reward), high


########### MAIN STARTS HERE ##############

# Argument Parser for parsing cmd lien args

parser = argparse.ArgumentParser()
parser.add_argument("--instance", type=str, required=True)
parser.add_argument("--algorithm", type=str, required=True)
parser.add_argument("--randomSeed", type=int, required=True)
parser.add_argument("--epsilon", type=float, default=0.02)
parser.add_argument("--scale", type=float, default=2)
parser.add_argument("--threshold", type=float, default=0)
parser.add_argument("--horizon", type=int, required=True)

args = parser.parse_args()

# Read Instance File and store data in list (try runs for task 1 and task 2, except for task 3 and 4)

try:
    instance = open(args.instance)
    instance = list(instance)
    instance = [float(x) for x in instance]
except:
    instance = open(args.instance)
    support = [float(x) for x in instance.readline().split(" ")]
    probab = []
    for x in instance.readlines():
        y = x.split(" ")
        y = [float(i) for i in y]
        probab.append(y)

# Check if algorithm given is in the available agorithms set or not
if args.algorithm not in algorithms:
    print("Wrong Algorithm")
    quit()

# Initialize high and regret variables
highs = int(0)
regret = float(0)

# Set Random Seed before calling all functions 
np.random.seed(args.randomSeed)

# Cases on algorithm type and their respective function calls
if args.algorithm == algorithms[0]:                                       # Epsilon-Greedy
    regret = epsilon_greedy(instance, args.epsilon, args.horizon)
    print_ans(args.instance, args.algorithm, args.randomSeed, args.epsilon, args.scale, args.threshold, args.horizon, regret, highs)
    
elif args.algorithm == algorithms[1]:                                     # UCB-t1
    regret = ucb(instance, args.horizon, 0, args.scale)
    print_ans(args.instance, args.algorithm, args.randomSeed, args.epsilon, args.scale, args.threshold, args.horizon, regret, highs)

elif args.algorithm == algorithms[2]:                                     # KL-UCB
    regret = ucb(instance, args.horizon, 1, args.scale)
    print_ans(args.instance, args.algorithm, args.randomSeed, args.epsilon, args.scale, args.threshold, args.horizon, regret, highs)

elif args.algorithm == algorithms[3]:                                     # Thompson Sampling 
    regret = thompson(instance, args.horizon)
    print_ans(args.instance, args.algorithm, args.randomSeed, args.epsilon, args.scale, args.threshold, args.horizon, regret, highs)

elif args.algorithm == algorithms[4]:                                     # UCB-t2
    regret = ucb(instance, args.horizon, 2, args.scale)
    print_ans(args.instance, args.algorithm, args.randomSeed, args.epsilon, args.scale, args.threshold, args.horizon, regret, highs)

elif args.algorithm == algorithms[5]:                                     # Algorithm 3
    regret = alg3(support, probab, args.horizon)
    print_ans(args.instance, args.algorithm, args.randomSeed, args.epsilon, args.scale, args.threshold, args.horizon, regret, highs)

elif args.algorithm == algorithms[6]:                                     # Algorithm 4
    regret, high = alg4(support, probab, args.horizon, args.threshold)
    print_ans(args.instance, args.algorithm, args.randomSeed, args.epsilon, args.scale, args.threshold, args.horizon, regret, high)

else:                                                                     # Dummy else statement
    print_ans(args.instance, args.algorithm, args.randomSeed, args.epsilon, args.scale, args.threshold, args.horizon, regret, highs)

