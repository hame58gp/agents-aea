# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Training environment for multi armed bandit."""

from typing import List, Tuple

import numpy as np
import gym
from gym import spaces

BanditId = int
Price = int
Action = [BanditId, Price]
Observation = None
Reward = bool
Done = bool
Info = dict
Feedback = Tuple[Observation, Reward, Done, Info]


class BanditEnv(gym.Env):
    """Base environment for n-armed bandits."""

    def __init__(self, nb_bandits: int, nb_prices_per_bandit: int, reward_params: List[Tuple[float, int]]):
        """
        Initialize the environment.

        :param nb_bandits: number of bandits
        :param nb_prices_per_bandit: number of prices per bandit
        :param reward_params: single param or tuple of params for the reward distribution
        """
        self.nb_bandits = nb_bandits
        self.nb_prices_per_bandit = nb_prices_per_bandit
        self.reward_params = reward_params

        self.action_space = spaces.Tuple((spaces.Discrete(self.nb_bandits), spaces.Discrete(self.nb_prices_per_bandit)))  # an action is specifying one of nb_bandits and specifying a price for the bandit.
        self.observation_space = spaces.Space()  # None type space. agents only get a reward back.

        self.seed()  # seed environment randomness

    def reset(self) -> Observation:
        """
        Reset the environment.

        :return: an observation
        """
        observation = None  # we purposefully make this explicit here
        return observation

    def step(self, action: Action) -> Feedback:
        """
        Execute one time step within the environment.

        :param action: the id of the bandit chosen
        :return: a Tuple containing the Feedback of Observation, Reward, Done and Info
        """
        assert self.action_space.contains(action), 'This is not a valid action.'

        bandit = action[0]
        offered_price = action[1]

        # defaults
        observation = None
        done = False
        info = {}

        cutoff_price = np.random.normal(self.reward_params[bandit][0], self.reward_params[bandit][1])
        reward = offered_price > cutoff_price

        return observation, reward, done, info

    def render(self, mode: str = 'human', close: int = False) -> None:
        """
        Render the environment to the screen.

        :param mode: the rendering mode
        :param close: a bool, true if ending
        :return: None
        """
        pass


class BanditNArmedRandom(BanditEnv):
    """N armed bandit randomly initialized."""

    def __init__(self, nb_bandits: int, nb_prices_per_bandit: int, stdev: int = 1, seed: int = 42):
        """
        Initialize the environment.

        :param nb_bandits: number of bandits.
        :param nb_prices_per_bandit: number of prices per bandit.
        :param stdev: standard deviation of the normal distribution.
        :param seed: the seed to initialize np random (not the env!)
        """
        np.random.seed(seed)

        reward_params = []  # type: List[Tuple[float, int]]
        for i in range(nb_bandits):
            # Mean m is pulled from a uniform distribution over [0, bound). To induce a normal distribution with params (m, 1).
            reward_params.append([np.random.uniform(0, nb_prices_per_bandit), stdev])

        BanditEnv.__init__(self, nb_bandits=nb_bandits, nb_prices_per_bandit=nb_prices_per_bandit, reward_params=reward_params)