import pickle
import numpy as np
from IPython import embed



def compute_expert_perform(path):
    filename = path
    data = pickle.load(open(filename, "rb"))
    N_traj = len(data)

    T = len(data[0])
    d = data[0][0][0][0].shape[0]

    traj_total_rew = []
    
    success_times = 0

    for i in range(N_traj):
        traj_i = data[i]
        traj_i_t_rew = 0.
        success = False
        for t in range(T):
            rew = traj_i[t][2][0]
            obs = traj_i[t][0][0]
            if success == False and np.linalg.norm(obs[-3:]) <= 0.05:
                success = True
                success_times += 1
            traj_i_t_rew += rew
        traj_total_rew.append(traj_i_t_rew)


    #return np.sum([tr > -T for tr in traj_total_rew])/(1.*N_traj)
    return success_times*1./N_traj
    #return np.mean(traj_total_rew), np.std(traj_total_rew)


def extract_expert_traj_observations(path, num_of_trajs):
    '''
    input: the name of the env, and number of trajectories wanted
    return: a 3 d matrix, with size num_of_trajs X traj_len X dim_observation
    '''

    filename = path
    data = pickle.load(open(filename, "rb"))

    N_traj = len(data)
    T = len(data[0])
    d = data[0][0][0][0].shape[0]
    #da = data[0][0][1][0].shape[0]

    #embed()

    extract_num = np.min((N_traj, num_of_trajs))
    expert_traj_obs_mat = np.zeros((N_traj, T, d)) #num of traj X length X obs dim
    #expert_traj_act_mat = np.zeros((N_traj, T, da))

    total_reward = 0.

    for i in range(extract_num): #deterministically pick the first num_of_trajs trajectories
        traj_i = data[i]
        max_T = np.min((T, len(traj_i)))
        assert max_T == T
        for t in range(max_T):
            #obs_t = traj_i[t][0][0]
            expert_traj_obs_mat[i, t, :] = traj_i[t][0][0]
            #expert_traj_act_mat[i, t, :] = traj_i[t][1][0]
            total_reward += traj_i[t][2][0]

            if t > 1:
                assert np.linalg.norm(traj_i[t][0][0] - traj_i[t-1][-1][0]) <= 1e-2

    #exp_mean, exp_std = compute_expert_perform(path)
    success_rate = compute_expert_perform(path)

    print("number of expert traj: {0}, traj length: {1}, and observation dim: {2}, success_rate: {3}".format(extract_num, T, d, success_rate))

    return expert_traj_obs_mat[0:extract_num], success_rate #exp_mean, exp_std#, expert_traj_act_mat[0:extract_num]


if __name__ == "__main__":

    env_name = "Reacher-v2"
    env_name = "CartPole-v1"
    env_name = "Reacher-v2"
    num_of_trajs = 100

    expet_obs_mat, exp_mean, exp_std = extract_expert_traj_observations(path = './data/CartPole-v1expert_traj.p', num_of_trajs = num_of_trajs)




