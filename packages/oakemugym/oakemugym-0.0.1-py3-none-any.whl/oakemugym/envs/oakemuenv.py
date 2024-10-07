from typing import Literal

import gymnasium as gym
import numpy as np
from gymnasium import error, spaces
from oakemu.machines.zxspectrum.game import Game
from oakemu.machines.zxspectrum.manicminer import ManicMiner


class OakEmuEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 50}
    _game: Game

    def __init__(
            self,
            game_type: Literal["Manic Miner"],
            obs_type: Literal["ram", "rgb", "spectrum"] = "spectrum",
            render_mode:Literal["human", "rgb_array"] | None = None
            # TODO: Add frameskip, repeat_action_probability, in common with the Atari envs.
    ):
        if game_type == "Manic Miner":
            self._game = ManicMiner()
        else:
            raise error.Error(f"Invalid game_type: {game_type}. Expecting: Manic Miner.")
    
        if obs_type not in {"ram", "rgb", "spectrum"}:
            raise error.Error(f"Invalid obs_type: {obs_type}. Expecting: ram, rgb, spectrum.")
    
        if render_mode is not None and render_mode not in self.metadata["render_modes"]:
            raise error.Error(f"Invalid render_mode: {render_mode}. Expecting: human, rgb_array.")
    
        self._obs_type = obs_type
        self.render_mode = render_mode
        self.action_space = spaces.Discrete(len(self._game.actions))
    
        if self._obs_type == "ram":
            self.observation_space = spaces.Box(low=0, high=255, dtype=np.uint8, shape=(6912,))
        else:   # rgb or spectrum
            image_shape = (192, 256,)
            if self._obs_type == "rgb":
                image_shape += (3,)
            self.observation_space = spaces.Box(low=0, high=255, dtype=np.uint8, shape=image_shape)

