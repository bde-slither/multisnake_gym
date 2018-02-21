#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This environment for gym is wriiten as a wrapper over https://github.com/Loonride/slither.io-clone"""
from __future__ import print_function
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from PIL import Image

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

playDuration = 5
driver = None

class MultiSnakeEnv(gym.Env):
    # step reset render close seed
    # action_space: The Space object corresponding to valid actions
    # observation_space: The Space object corresponding to valid observations
    # reward_range: A tuple corresponding to the min and max possible rewards

    def __init__(self):
        # initialize the Game, raise error if not implemented.
        global driver
        action_space = None
        observation_space = None
        reward_range = None

        driver = webdriver.Firefox()
        driver.get("http://localhost:8080/slither-io/")
        driver.execute_script("window.game.paused = true;")
        print('Śtarted')

    def step(self, x, y):
        global driver
        gameObj = dict()

        driver.execute_script("window.targetX = " + str(x) + ";")
        driver.execute_script("window.targetY = " + str(y) + ";")
        driver.execute_script("window.game.paused = false;")
        try:
            print("playing")
            element = WebDriverWait(driver, playDuration).until(
                EC.presence_of_element_located((By.ID, "doesNotExist"))
            )
        except:
            pass
        
        driver.execute_script("window.game.paused = true;")
        try:
            print("paused")
            
            canvasEle = driver.find_elements_by_css_selector('canvas')[0]
            location = canvasEle.location
            size = canvasEle.size
            driver.save_screenshot('gamescreenshot.png')
            
            im = Image.open('gamescreenshot.png')
            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']
            im = im.crop((left, top, right, bottom))
            gameObj['image'] = im
            # im.save('gamescreenshot.png')
            
            driver.execute_script("window.getGameStats();")
            try:
                elementD1 = WebDriverWait(driver, 0.5).until(
                    EC.presence_of_element_located((By.ID, "doesNotExist"))
                )
            except:
                print('pause exception 1')
            finally:
                print('gameStats')
                gameStatsEle = driver.find_element_by_id('gameStats')
                gameObj['stats'] = gameStatsEle.get_attribute('innerHTML')
                #print(gameStatsEle)
        except:
            print('pause exception 2')

        return gameObj

    def reset(self):
        global driver
        driver.refresh()
        driver.execute_script("window.game.paused = true;")
        print('Restart')

    def render(self, mode='human'):
        print('Render')

    def close(self):
        driver.close()
        print('Close')

    def seed(self):
        print('Seed')