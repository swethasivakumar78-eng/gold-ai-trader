import gymnasium as gym
from gymnasium import spaces
import numpy as np

class GoldTradingEnv(gym.Env):

    def __init__(self, df):
        super(GoldTradingEnv, self).__init__()

        self.df = df
        self.current_step = 0

        # Actions: 0=Hold, 1=Buy, 2=Sell
        self.action_space = spaces.Discrete(3)

        # Observation space
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(df.shape[1],),
            dtype=np.float32
        )

    # RESET FUNCTION
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.current_step = 0

        state = self.df.iloc[self.current_step].values.astype(np.float32)

        return state, {}

    # STEP FUNCTION
    def step(self, action):

        self.current_step += 1

        price_today = self.df.iloc[self.current_step]["Close"]
        price_prev = self.df.iloc[self.current_step - 1]["Close"]

        reward = price_today - price_prev

        terminated = self.current_step >= len(self.df) - 1
        truncated = False

        state = self.df.iloc[self.current_step].values.astype(np.float32)

        return state, reward, terminated, truncated, {}