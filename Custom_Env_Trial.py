from enum import Enum 

import pygame
import numpy as np 
import gymnasium as gym

from gymnasium import spaces

#Creating a class of the possible actions in our environment
class Action(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3
#This is the mian environment class. Our environment class is called GridWorldEnv
class GridWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode = None, size = 5):
        self.size = size 
        self.window_size = 512

        self.observation_space = spaces.Dict (
            {
                "agent": spaces.box(0,size-1, shape = (2,), dtype = int),
                "target":spaces.box(0, size-1, shape=(2,), dtype = int),
            }
        )

        self.agent_location = np.array([-1,-1], dtype = int)
        self.target_location = np.array([-1,-1], dtype = int)

        self.action_space = spaces.Discrete(4) #Since we have 4 discrete actions in the Action class, we can use Dicrete(4)

        self.action_to_direction = {
            Action.RIGHT.value: np.array([1,0]),
            Action.UP.value: np.array([0,1]),
            Action.LEFT.value: np.array([-1,0]),
            Action.DOWN.value: np.array([0,-1]),
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None

        #Getting the observations
        def get_obs(self):
            return {
                "agent": self.agent_location,
                "target": self.target_location,
            }
        
        def get_info(self):
            return {
                "distance": np.linalg.norm(
                self._agent_location - self._target_location, ord=1
            )
        }

        #Writing the reset function for the environment
        def reset(self, seed = None,options = None):
            super().reset(seed = seed) #This needs to be the default first line

            self.agent_location = self.np_random.integers(0, self.size, size = 2, dtype = int)

            self.target_location = self.agent_location
            while np.array_equal(self.target_location, self.agent_location):
                self.target_location = self.np_random.integers(
                    0, self.size, size = 2, dtype = int
                )

            
            #Reset function returns the observation and info (Read reset under env in gym website)
            observation = self.get_obs()
            info = self.get_info()

            if self.render_mode == "human":
                self.render_frame()
            
            return observation, info
        
        def step(self, action):
            direction = self.action_to_direction[action]

            self.agent_location = self.np_clip(
                self.agent_location + direction, 0, self.size - 1
            )

            terminated = np.array_equal(self.agent_location, self.target_location)
            reward = 1 if terminated else 0

            observation = self.get_obs()
            info = self.get_info()

            if render_mode == "human":
                self.render_frame()

            return observation, reward, terminated, False, info
        
        #We define the gui using pygame inside this function
        def render(self):
            if self.render_mode == "rgb_array":
                return self.render_frame()
        
        def render_frame(self):
            if self.window is None and self.render_mode == "human":
                pygame.init()
                pygame.display.init()
                self.window = pygame.display.set_mode(
                    (self.window_size, self.window_size)
                )
            if self.clock is None and self.render_mode == "human":
                self.clock = pygame.time.Clock()

            canvas = pygame.Surface((self.window_size, self.window_size))
            canvas.fill((255,255,255))
            pix_square_size = (self.window_size/self.size)

            #Drawing the target
            pygame.draw.rect(
                canvas, 
                (255,0,0),
                pygame.Rect(
                    pix_square_size*self.target_location,
                    (pix_square_size, pix_square_size)
                ),
            )

            #Drawing the agent
            pygame.draw.circle(
                canvas,
                (0,0,255),
                (self.agent_location + 0.5)*pix_square_size,
                pix_square_size/3,
            )

            #Drawing the gridlines
            for x in range(self.size + 1):
                pygame.draw.line(
                    canvas,
                    0,
                    (0, pix_square_size * x),
                    (self.window_size, pix_square_size * x),
                    width=3,
                )
                pygame.draw.line(
                    canvas,
                    0,
                    (pix_square_size * x, 0),
                    (pix_square_size * x, self.window_size),
                    width=3,
                )
                
            if self.render_mode == "human":
                # The following line copies our drawings from `canvas` to the visible window
                self.window.blit(canvas, canvas.get_rect())
                pygame.event.pump()
                pygame.display.update()

                # We need to ensure that human-rendering occurs at the predefined framerate.
                # The following line will automatically add a delay to keep the framerate stable.
                self.clock.tick(self.metadata["render_fps"])
            else:  # rgb_array
                return np.transpose(
                    np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
                )
            
            def close(self):
                if self.window is not None:
                    pygame.display.quit()
                    pygame.quit()


# from gymnasium.envs.registration import register

# register (
#     id = "gymnasium_envs/GridWorld-v0",
#     entry_point="gymnasium_env.envs:GridWorldEnv",
# )
