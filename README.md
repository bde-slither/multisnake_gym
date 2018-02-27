This repository contains a PIP package which is an OpenAI environment for
simulating an enironment in which multiplayer snake is played.


## Installation

Install the [OpenAI gym](https://gym.openai.com/docs/).

Then install this package via

```
pip install -e .
```

## Usage

```
import gym
import gym_multisnake
env = gym.make('multisnake-v0')
env.step([(100, 200), (600, 650)])

```

See https://github.com/matthiasplappert/keras-rl/tree/master/examples for some
examples.


## The Environment

