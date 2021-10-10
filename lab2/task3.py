import os

initial_pol_p1 = "./data/attt/policies/p1_policy1.txt"
initial_pol_p2 = "./data/attt/policies/p2_policy2.txt"
states_p1 = "./data/attt/states/states_file_p1.txt"
states_p2 = "./data/attt/states/states_file_p2.txt"

os.system("rm -rf task3")
os.system("mkdir task3")

for i in range(10):
    if i == 0:
        cmd1 = "python3 encoder.py --states {} --policy {} > ./task3/mdpfile1".format(states_p1, initial_pol_p2)
    else:
        cmd1 = "python3 encoder.py --states {} --policy {} > ./task3/mdpfile1"
    cmd2 = "python3 planner.py --mdp ./task3/mdpfile1 > ./task3/vp1"
    cmd3 = "python3 decoder.py --player-id {} --states ./data/attt/states/states_file_p{}.txt --value-policy ./task3/vp1 > ./task3/pi{}_{}"

    cmd4 = "python3 encoder.py --states {} --policy {} > ./task3/mdpfile2"
    cmd5 = "python3 planner.py --mdp ./task3/mdpfile2 > ./task3/vp2"
    cmd6 = "python3 decoder.py --player-id {} --states ./data/attt/states/states_file_p{}.txt --value-policy ./task3/vp2 > ./task3/pi{}_{}"

    if i==0:
        os.system(cmd1)
    else:
        os.system(cmd1.format(states_p1, "./task3/pi2_{}".format(i)))

    os.system(cmd2)
    os.system(cmd3.format(1, 1, 1, i+1))
    os.system(cmd4.format(states_p2, "./task3/pi1_{}".format(i+1)))
    os.system(cmd5)
    os.system(cmd6.format(2, 2, 2, i+1))
