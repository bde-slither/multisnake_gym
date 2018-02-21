from __future__ import print_function
import gym
import gym_multisnake
import time
import random
import PIL

env = gym.make('multisnake-v0')
#env.reset()

for i in range(1, 5):
    gObj = env.step(0, -400) #env.step(random.randint(1, 400), random.randint(1, 400))
    if gObj != None and gObj['stats'] != None:
        print(gObj['stats'])
        f = open('steps/gameStats_' + str(i) + '.txt', 'w')
        f.write(gObj['stats'])
        f.close()
        gObj['image'].save('steps/gameScreenshot_' + str(i) + '.png')

    time.sleep(5)

env.close()