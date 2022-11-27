#!/usr/bin/env python
# coding: utf-8

####
#BASIC CODE TO CREATE BLOCK MAZES OF SIZE 5,10,15,20 WITH OBSTACLE RATIOS OF 15,30,45 AND 60% WITH ONLY 1 I/O. Code modifiable for many i/o
####

import os
import itertools
import random
import json
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from gym_maze.envs.generators import SimpleMazeGenerator, RandomMazeGenerator, RandomBlockMazeGenerator, TMazeGenerator, WaterMazeGenerator

from environment.maze import Maze, Render
import models
import logging
from enum import Enum, auto

import matplotlib.pyplot as plt
import numpy as np
# In[42]:


#Create
from gym_maze.envs import MazeEnv
from gym_maze.envs.generators import SimpleMazeGenerator, RandomMazeGenerator, RandomBlockMazeGenerator, \
                                     UMazeGenerator, TMazeGenerator, WaterMazeGenerator
from gym_maze.envs.Astar_solver import AstarSolver

# In[43]:


def solvemaze(maze,posd, action_type='VonNeumann', render_trace=False, gif_file='video.gif'):
    env = MazeEnv(maze, action_type=action_type, render_trace=render_trace,pos=posd)
    env.reset()

    # Solve maze by A* search from current state to goal
    solver = AstarSolver(env,env.goal_states[0])
    if not solver.solvable():
        return False
        
    else:
        return True

    
#maze = RandomBlockMazeGenerator(maze_size=11, obstacle_ratio=0.3)
#x = np.pad(maze.maze, pad_width=1, mode='constant', constant_values=2)
#maze.maze=x
##lst_size=[11]
#print(x)
#print(([1,1],[[lst_size[0],lst_size[0]]]))
#anim = solvemaze(maze, action_type='VonNeumann',render_trace=False, gif_file='simple_empty_maze.gif',posd=([1,1],[[lst_size[0],lst_size[0]]]))
#results = maze.maze[1:-1,1:-1]
#maze.maze = results
#exit()

lst_size=[25]
lst_ins=[1]
lst_outs=[1]
lst_obs=[0.2,0.3,0.4,0.5]
s=[lst_ins,lst_outs,lst_obs]
fin=list(itertools.product(*s))



# In[47]:
totit=0
for m in range(len(lst_size)):
    print(lst_size[m])
    for l in range(len(fin)):
        print(fin[l][2])
        while totit<25:
            #print(lst_size[m])
            #print(fin[l])
            #print(totit)
            maze_size=lst_size[m]
            num_in=fin[l][0]
            num_out=fin[l][1]
            obs=fin[l][2]
            
            maze_gen = RandomBlockMazeGenerator(maze_size=maze_size, obstacle_ratio=obs)
            #maze=maze_gen.maze
            #maze_gen = RandomBlockMazeGenerator(maze_size=lst_size[m], obstacle_ratio=0.3)
            maze_gen.maze[0][0]=0
            maze_gen.maze[-1][-1]=0
            #print(maze_gen.maze)
            x = np.pad(maze_gen.maze, pad_width=1, mode='constant', constant_values=1)
            maze_gen.maze=x
            #print(maze_gen.maze)
            anim = solvemaze(maze_gen, action_type='VonNeumann',render_trace=False, gif_file='simple_empty_maze.gif',posd=([1,1],[[lst_size[m],lst_size[m]]]))
            if anim:
                
                
                results = maze_gen.maze[1:-1,1:-1]
                maze_gen.maze = results


                #tmt=maze_gen.maze.copy()
                #tmt[0][0]=2
                #tmt[-1][-1]=3
                #print(tmt)

                #print("valid?, enter 0 for yes")
                #if input() == '0' :
                tmp=dict={"Maze":maze_gen.maze.tolist(),"Obs":obs,"Size":maze_size}
                
                with open('./mz/Maze_'+str(maze_size)+'_'+(str(obs).replace(".",""))+'_'+str(num_in)+'_'+str(num_out)+'_'+str(totit)+'.txt', 'w') as convert_file:
                    convert_file.write(json.dumps(tmp))
                    
                print(totit)
                totit+=1
        totit=0



# In[ ]:





# In[ ]:


#Read


# In[135]:


#import json
  
# reading the data from the file
#with open('./txtfiles/Maze_'+str(maze_size)+'_'+(str(obs).replace(".",""))+'_'+str(num_in)+'_'+str(num_out)+'.txt') as f:
#    data = f.read()
      
# reconstructing the data as a dictionary
#js = json.loads(data)


# In[136]:


#js['Maze']=np.asarray(js['Maze'])


# In[137]:


#print(js)


# In[ ]:




