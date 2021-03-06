#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This environment for gym is wriiten as a wrapper over https://github.com/Loonride/slither.io-clone"""
from __future__ import print_function
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from PIL import Image
import math
import json
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

class GameObservation(object):
    stats = None
    image = None

    # The class "constructor" - It's actually an initializer 
    def __init__(self, stats, image):
        self.stats = stats
        self.image = image

class MultiSnakeEnv(gym.Env):
    # step reset render close seed
    # action_space: The Space object corresponding to valid actions
    # observation_space: The Space object corresponding to valid observations
    # reward_range: A tuple corresponding to the min and max possible rewards
    playDuration = 0
    radius = 0
    driver = None
    gameObject = None
    curPosX = 0
    curPosY = 0
    stepCount = 0
    resetCount = 0

    def gamePause(self, duration):
        time.sleep(duration)
        #try:
        #    #print("pause", duration)
        #    element = WebDriverWait(self.driver, duration).until(
        #        EC.presence_of_element_located((By.ID, "doesNotExist"))
        #    )
        #except:
        #    pass

    def setNormalSpeed(self):
        self.driver.execute_script("setNormalSpeed();")
    
    def __init__(self):
        # initialize the Game, raise error if not implemented.
        # self.action_space = spaces.Tuple((spaces.Discrete(36), spaces.Discrete(36)))
        self.action_space = spaces.Discrete(36)
        self.observation_space = None
        self.viewer = None
        self.state = None
        self.radius = 200
        self.playDuration = 0.0075
        self.stepCount = 0
        self.resetCount = 0
        self.seed()
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(firefox_options=options)
        #self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 700)
        self.driver.get("http://127.0.0.1/slither-io/")
        #self.driver.get("http://localhost:8080/slither-io/")
        self.gamePause(0.5)
        while self.gameObject == None or self.gameObject.stats == None or 'done' not in self.gameObject.stats:
            self.getGameStats()
            self.gamePause(0.5)
        self.driver.execute_script("window.game.paused = true;")
        #self.getGameStats()
        self.setNormalSpeed()
        print('Started')

    def getTargetPos(self, action):
        #print ("getTargetPos")
        #print (self.gameObject.stats)
        #print (self.gameObject.stats['snakes'][0]['x'], self.gameObject.stats['snakes'][0]['y'])
        #print ("Ok")

        x = 0
        y = 0

        if not (self.gameObject and self.gameObject.stats and self.gameObject.stats['snakes'] and len(self.gameObject.stats['snakes']) > 0):
            return x, y
        if action >= 0 and action <= 9:        
            theta = 10 * (action)
            x = self.gameObject.stats['snakes'][0]['x'] + self.radius * math.sin(math.radians(theta))
            y = self.gameObject.stats['snakes'][0]['y'] - self.radius * math.cos(math.radians(theta))
        elif action >= 10 and action <= 18:
            theta = 10 * (action) - 90
            if (action == 18):
                rn = random.randint(1,2)
                if rn == 1:
                    theta = theta - 1
                else:
                    theta = theta + 1
            x = self.gameObject.stats['snakes'][0]['x'] + self.radius * math.cos(math.radians(theta))
            y = self.gameObject.stats['snakes'][0]['y'] + self.radius * math.sin(math.radians(theta))
        elif action >= 19 and action <= 27:
            theta = 10 * (action) - 180
            x = self.gameObject.stats['snakes'][0]['x'] - self.radius * math.sin(math.radians(theta))
            y = self.gameObject.stats['snakes'][0]['y'] + self.radius * math.cos(math.radians(theta))
        else:
            theta = 10 * (action) - 270
            x = self.gameObject.stats['snakes'][0]['x'] - self.radius * math.cos(math.radians(theta))
            y = self.gameObject.stats['snakes'][0]['y'] - self.radius * math.sin(math.radians(theta))
        
        #print (x, y)
        return x, y

    def getGameStats(self):
        self.driver.execute_script("window.getGameStats();")
        
        canvasEle = self.driver.find_elements_by_css_selector('canvas')[0]
        location = canvasEle.location
        size = canvasEle.size
        self.driver.save_screenshot('gamescreenshot.png')
        
        gameImage = Image.open('gamescreenshot.png')
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        gameImage = gameImage.crop((int(left), int(top), int(right), int(bottom)))
        
        stats = self.driver.find_element_by_id('gameStats').get_attribute('innerHTML')
        gameStats = json.loads(stats)
        #print (gameStats['snakes'][0]['x'], gameStats['snakes'][0]['y'])
        #print ('Again')
        #print (stats)
        
        gameImage.save('ss.png')
        self.gameObject = GameObservation(gameStats, gameImage)
        return self.gameObject
        
    def step(self, action):
        #print ("Step")
        self.stepCount = self.stepCount + 1
        #print(action)

        positions = []
        x, y = self.getTargetPos(action)
        positions.append((x, y))
        #for act in action:
        #    x, y = self.getTargetPos(act)
        #    positions.append((x, y))
        
        # print(positions)

        self.driver.execute_script("window.targetPositions = " + json.dumps(positions) + ";")
        # print (positions)
        #self.driver.execute_script("window.targetX = " + str(x) + ";")
        #self.driver.execute_script("window.targetY = " + str(y) + ";")
        self.driver.execute_script("window.game.paused = false;")
        self.gamePause(self.playDuration)
        self.driver.execute_script("window.game.paused = true;")
        self.getGameStats()
        
        done = self.gameObject.stats['done']
        reward = self.gameObject.stats['reward']
        #if self.stepCount >= 500:
        #    done = True
        #    self.stepCount = 0
        #print ("reward", reward)
        #print ("Step")
        return self.gameObject.image, reward, done, {}

    def reset(self):
        #print ("Reset")
        self.resetCount = self.resetCount + 1
        if self.resetCount == 10000:
            print ("Reload")
            self.resetCount = 0
            self.driver.close()
            options = Options()
            options.add_argument("--headless")
            self.driver = webdriver.Firefox(firefox_options=options)
            #self.driver = webdriver.PhantomJS()
            self.driver.set_window_size(1120, 700)
            self.driver.get("http://127.0.0.1/slither-io/")
            #self.driver.get("http://localhost:8080/slither-io/")
            self.gamePause(0.5)
        else:
            self.driver.execute_script("window.game.paused = false;")
            self.driver.execute_script("resetGame();")
            self.gameObject = None
            self.gamePause(0.5)
        while self.gameObject == None or self.gameObject.stats == None or 'done' not in self.gameObject.stats:
            self.getGameStats()
            self.gamePause(0.5)
        self.driver.execute_script("window.game.paused = true;")
        self.stepCount = 0
        self.setNormalSpeed()
        return self.gameObject.image

        #self.driver.refresh()
        ##self.driver.get("http://localhost:8080/slither-io/")
        #self.gamePause(0.1)
        #self.driver.execute_script("window.game.paused = true;")
        #gameObject = self.getGameStats()
        ##print('Reset E')
        #self.stepCount = 0
        #self.setNormalSpeed()
        #return gameObject.image

    def render(self, mode='human'):
        print('Render')

    def close(self):
        self.driver.close()
        print('Close')

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        print('Seed')
        return [seed]
