import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='multisnake-v0',
    entry_point='gym_multisnake.envs:MultiSnakeEnv',
)
