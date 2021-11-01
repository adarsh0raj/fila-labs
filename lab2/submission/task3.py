import os
import subprocess

os.system("rm -rf task3")
os.system("mkdir task3")

first_player = 1          
sec_player = 2
pol = 1

initial_pol = "./data/attt/policies/p{}_policy{}.txt".format(sec_player, pol)
states = ["./data/attt/states/states_file_p1.txt", "./data/attt/states/states_file_p2.txt"]

for i in range(10):
    if i == 0:
        cmd1 = "python encoder.py --states {} --policy {} > ./task3/mdpfile1".format(states[first_player - 1], initial_pol)
    else:
        cmd1 = "python encoder.py --states {} --policy {} > ./task3/mdpfile1"
    cmd2 = "python planner.py --algorithm vi --mdp ./task3/mdpfile1 > ./task3/vp1"
    cmd3 = "python decoder.py --player-id {} --states ./data/attt/states/states_file_p{}.txt --value-policy ./task3/vp1 > ./task3/pi{}_{}"

    cmd4 = "python encoder.py --states {} --policy {} > ./task3/mdpfile2"
    cmd5 = "python planner.py --algorithm vi --mdp ./task3/mdpfile2 > ./task3/vp2"
    cmd6 = "python decoder.py --player-id {} --states ./data/attt/states/states_file_p{}.txt --value-policy ./task3/vp2 > ./task3/pi{}_{}"

    if i==0:
        os.system(cmd1)
    else:
        os.system(cmd1.format(states[first_player-1], "./task3/pi{}_{}".format(sec_player, i)))

    os.system(cmd2)
    os.system(cmd3.format(first_player, first_player, first_player, i+1))
    os.system(cmd4.format(states[sec_player-1], "./task3/pi{}_{}".format(first_player, i+1)))
    os.system(cmd5)
    os.system(cmd6.format(sec_player, sec_player, sec_player, i+1))

os.system("rm ./task3/mdpfile1")
os.system("rm ./task3/mdpfile2")
os.system("rm ./task3/vp1")
os.system("rm ./task3/vp2")

print("Completed Calculating 10 policies each for Player 1 and Player 2")

# Checking the evaluated Policies
print("-----------------------------------------------------------------")
print("Taking Diff of the Files:")
print("-----------------------------------------------------------------")
print("Starting Player {}, Initial Policy for Player {} - {}".format(first_player, sec_player, initial_pol[21:]))
print("-----------------------------------------------------------------")
print("Player1 Policies    Difference in lines    |   Player2 Policies     Difference in lines")

for i in range(9):
    arch1 = subprocess.check_output("diff -y --suppress-common-lines ./task3/pi1_{} ./task3/pi1_{} | grep '^' | wc -l".format(i+2, i+1), shell=True)
    arch2 = subprocess.check_output("diff -y --suppress-common-lines ./task3/pi2_{} ./task3/pi2_{} | grep '^' | wc -l".format(i+2, i+1), shell=True)

    print("pi1_{} pi1_{}               {}       |        pi2_{}  pi2_{}           {} ".format(i+2, i+1, int(arch1),i+2, i+1, int(arch2)))
print("-----------------------------------------------------------------")
print("-----------------------------------------------------------------")
