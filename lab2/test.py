import time
import subprocess

def run(states,policy,player, algo, pol_id):
    cmd_encoder = "python3","encoder.py","--policy",policy,"--states",states
    mdpfile = 'task2/mdp_{}_{}_{}'.format(player, pol_id, algo)
    f = open(mdpfile,'w')
    subprocess.call(cmd_encoder,stdout=f)
    f.close()

    cmd_planner = "python3","planner.py","--mdp",mdpfile,"--algorithm",algo
    valpol = 'task2/valpol_{}_{}_{}'.format(player, pol_id, algo)
    f = open(valpol,'w')
    subprocess.call(cmd_planner,stdout=f)
    f.close()

    cmd_decoder = "python3","decoder.py","--value-policy",valpol,"--states",states ,"--player-id",str(player)
    pol = 'task2/pol_{}_{}_{}'.format(player, pol_id, algo)
    f = open(pol, 'w')
    subprocess.check_output(cmd_decoder)
    f.close()

for player in [1,2]:
    for policy in [1,2]:
        for algo in ["vi", "hpi", "lp"]:
            t1 = time.time()
            print("Executing for player {} against player {}'s policy {} using algorithm {}".format(player, player^3, policy, algo))
            sp = "data/attt/states/states_file_p{}.txt".format(player)
            polpath = "data/attt/policies/p{}_policy{}.txt".format(player^3, policy)
            run(sp, polpath, player, algo, policy)
            t2 = time.time()
            print("That took {}s".format(t2-t1))