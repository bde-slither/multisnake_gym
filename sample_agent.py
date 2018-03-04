import gym
import gym_multisnake
env = gym.make('multisnake-v0')

for k in range(1, 10):
    env.reset()
    for i in range(1, 100):
        ob, reward, done, _ = env.step(18)
        if done:
            print (done)
            break

env.close()