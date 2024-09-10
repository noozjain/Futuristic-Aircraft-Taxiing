#!/usr/bin/env python
# coding: utf-8

# In[174]:


import random
import gymnasium as gym 
import numpy as np
from copy import copy
import pettingzoo as pz
#from tutorial2_adding_game_logic import CustomEnvironment
#from tutorial3_action_masking import CustomActionMaskedEnvironment
from pettingzoo.test import parallel_api_test


# In[175]:


class taxienv(pz.ParallelEnv):
    metadata = {
            "name": "custom_environment_v0",
            "render_modes": ["human", "ansi", "rgb_array"],
                 "render_fps": 4
        }


# In[176]:


def __init__(self):
    self.agent = "aircraft"
    self.map
    self.node_points = np.array((1011,142),(1046,173),(1063,166),(1024,124), (1047,173),(1047,511),(1063,511),(1063,166),
   
                                (1008,107),(1030,90),(1082,147),(1071,157), (1071,157),(1082,147),(1082,511),(1071,511),
                                
                                (1063,166),(1071,166),(1071,185),(1063,185), (1063,202),(1071,202),(1071,215),(1063,215),
                                
                                (1063,308),(1071,308),(1071,322),(1063,322), (1046,308),(1046,322),(978,322),(978,308),
                                
                                (993,215),(984,215),(984,308),(993,308), (963,215),(978,215),(978,375),(963,375),
                                
                                (993,215),(1046,216),(1046,203),(993,203), (998,203),(982,203),(982,142),(998,142),
                                
                                (977,203),(963,203),(963,142),(977,142), (963,182),(963,196),(897,196),(897,183),
                                
                                (898,142),(878,142),(878,201),(898,201), (963,215),(877,213),(877,201),(963,203),
                                
                                (877,213),(878,194),(800,195),(800,213), (1011,142),(1024,124),(772,124),(772,142),
                                
                                (180,526),(1100,526),(1100,511), (180,511),(79,107),(93,107),(93,195), (79,195),
                                
                                (79,90), (1029,90) ,(1008,107), (79,107), (258,164),(273,164),(273,173), (258,173),
                                
                                (258,173),(800,173),(800,195),(258,195),
                                
                                (962,107),(983,107),(983,124),(962,124), (874,107),(904,107),(904,124),(874,124),
                                
                                (646,511), (672,511),(672,491),(646,491), (672,491), (672,504), (1047,504),(1047,491),
                                
                                (1120,526), (1120,491), (1100,491), (1100,526), (878,173), (878,194), (800,194), (800,173),
                                
                                (80,90),(100,90),(100,77),(80,77),(223,90),(247,90),(247,77),(223,77),
                                
                                (263,90),(302,90),(302,77),(263,77), (388,90), (433,90), (433,77),(388,77),
                                
                                (479,90),(514,90),(514,77),(479,77), (585,90),(623,90),(623,77),(585,77), 
                                
                                (692,90),(727,90),(727,77),(692,77), (728,90),(743,90),(743,77),(728,77), 
                                
                                (985,90),(1001,90),(1001,77),(985,77), (1008,90),(1022,90),(1022,77),(1008,77),
                                
                                (180,526),(195,526),(195,537),(180,537), (198,526),(215,526),(215,537),(198,537),
                                 
                                (325,526),(343,526),(343,537),(325,537), (462,526),(496,526),(496,537),(462,537),
                                 
                                (581,526),(615,526),(615,537),(581,537), (685,526),(718,526),(718,537),(685,537),
                                 
                                (803,526),(836,526),(836,537),(803,537), (936,526),(956,526),(956,537),(936,537),
                                 
                                (1084, 526),(1100,526),(1100,547),(1084, 547), (1104,526),(1120,526),(1120,549),(1104,549))
                                        
    self.agent_location = np.array(0,0)
    self.gates=np.array((285,173), (295,173), (700,173), (645,173))
    self.dest=np.array((80,40),(1120,560))
    self.agent_reward 
    self.agent_vector 
    #self.reward_space=gym.spaces.Discrete(11, start=-5, seed=42)
    self.timestep
    self.move_rate = 0.1


# In[177]:


def step(self):
    while(self.agent_location not in self.dest):
        if(self.agent_location not in self.gates and self.agent_location in self.node_points):
                for i in self.node_points:
                    if((i[0]==self.agent_location[0] and i[1]!=self.agent_location[1]) or (i[0]!=self.agent_location[0] and i[1]==self.agent_location[1])):
                        find_and_compare_coordinates(self.node_points, self.agent_location)
                        for j in results:
                            if(self.agent_vector!=j["searched_pair"]-j["next_pair"]):
                                self.agent_vector = j["searched_pair"]-j["next_pair"]
                self.agent_location += self.move_rate*(agent_vector)

        elif(self.agent_location not in self.gates and self.agent_location not in self.node_points):
            while(self.agent_location not in self.node_points):
                self.agent_location += self.move_rate*(self.agent_vector)
     # Check termination conditions
    terminations = {a: False for a in self.agents}
    rewards = {a: 0 for a in self.agents}
    if self.aricraft_location == self.dest:
        rewards = {"Aircraft": 1}
        terminations = {a: True for a in self.agents}

    else:
        rewards = {"Aircraft": 0}
        terminations = {a: True for a in self.agents}

    # Check truncation conditions (overwrites termination conditions)
    truncations = {a: False for a in self.agents}
    if self.timestep > 100:
        rewards = {"Aircraft": -1}
        truncations = {"Aircraft": True}
    self.timestep += 1


# In[178]:


def reset():
    self.agent_location = np.array(0,0)
    self.agent_reward  = 0
    self.agent_vector = 0
    self.timestep=0
    self.agent = copy(self.agent)
    


# In[179]:


'''
    def render(self):
            """Renders the environment."""
            grid = np.full((1200, 628), " ")
            grid[self.agent_location] = "A"
            grid[self.node_points] = "N"
            grid[self.dest] = "R"
            print(f"{grid} \n")
'''


# In[180]:


def render(self):
    """Renders the environment."""
    # Create an empty grid (characters, not strings of words)
    grid = np.full((1200, 628), " ")

    # Assign single characters for the entities
    grid[self.agent_location[0], self.agent_location[1]] = "A"  # 'A' for Agent
    for point in self.node_points:
        grid[point[0], point[1]] = "N"  # 'N' for Node
    grid[self.dest[0], self.dest[1]] = "R"  # 'R' for Runway

    # Print the grid row by row for visualization
    for row in grid:
        print("".join(row))
        


# In[181]:


def find_and_compare_coordinates(coords_list, search_pair):
    results = []
    for i in range(len(coords_list) - 1):
        if coords_list[i] == search_pair:
            if(i%2==0):
                next_pair = coords_list[i + 1]
            if(i%2==1):
                next_pair = coords_list[i - 1]
                # Calculate difference between the pairs
            diff = (
                next_pair[0] - search_pair[0],
                next_pair[1] - search_pair[1]
            )
            results.append({
                'searched_pair': search_pair,
                'next_pair': next_pair,
                'difference': diff
            })
    
    return results
'''
# Example usage 
search_pair = (993, 215)

results = find_and_compare_coordinates(coords_list, search_pair)

for result in results:
    print(f"Searched Pair: {result['searched_pair']}\t")
    print(f"Next Pair: {result['next_pair']}\t")
    print(f"Difference: {result['difference']}\n")
    print()
'''


# In[182]:


def action_space():
    return gym.spaces.Discrete(2)
    


# In[183]:


def observation_space():
    return gym.spaces.Box[1200,628]


# In[184]:


taxi_1 = taxienv()


# In[ ]:




