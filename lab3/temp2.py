import numpy as np

def change(weights):
    weights[10] -= np.ones(20)
    return weights

def get_table_features(obs):

    x_space = np.linspace(-1.2, 0.6, 18)
    v_space = np.linspace(-0.07, 0.07, 28)
    x_bin = np.digitize(obs[0], x_space)
    v_bin = np.digitize(obs[1], v_space)

    res = np.zeros((18*28), dtype=int)
    res[int((x_bin-1)*28 + (v_bin - 1))] = 1
    return res

weights = np.zeros((20, 20))
print(weights[10, :])
weights = change(weights)

print(get_table_features((-0.76, -0.035)))
print(np.random.choice(3))


# x_space = np.linspace(-1.2, 0.6, 18)
# v_space = np.linspace(-0.07, 0.07, 28)
# x_bin = np.digitize(0.6, x_space)
# v_bin = np.digitize(0.07, v_space)
# print(x_space)
# print(v_space)
# print(x_bin)
# print(v_bin)

