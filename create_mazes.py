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


# In[43]:


lst_size=[11,25]
lst_ins=[1]
lst_outs=[1]
lst_obs=[0.15,0.30,0.45,0.60]
s=[lst_ins,lst_outs,lst_obs]
fin=list(itertools.product(*s))


# In[44]:


def random_start_exit(maze,num_in=1,num_out=1):
    idx_empty=[]
    idx_in=[]
    idx_out=[]
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j]==0.0:
                idx_empty.append(tuple((j,i))) #us (j,i) rather than i,j since Maze in (game = Maze(js['Maze'], exit_cell=js['Out'])) uses j to signifie the the X posiition and the I to signifie the Y position. We used I to select every row so our I is Y and J is Y
                
            
    
    print(maze)
    #print(idx_empty)
    #choose entrance
    print(idx_empty)
    idx_in=random.sample(idx_empty,k=num_in)
    #print(idx_in)
    print(idx_in)
    
    if not all(elem in idx_empty for elem in idx_in):
        print("failed")
        exit()    
    #
    idx_empty = [ele for ele in idx_empty if ele not in idx_in]
    
    print(idx_empty)

    idx_out=random.sample(idx_empty,k=num_out)
    
    print(idx_out)
    
    if not all(elem in idx_empty for elem in idx_out):
        print("failed")
        exit()   

    
    return idx_in,idx_out


# In[47]:
totit=0
for m in range(len(lst_size)):
    for l in range(len(fin)):
    #creates 25 mazes
        while totit<25:
            maze_size=lst_size[m]
            num_in=fin[l][0]
            num_out=fin[l][1]
            obs=fin[l][2]
            
            maze_gen = RandomBlockMazeGenerator(maze_size=maze_size, obstacle_ratio=obs)
            maze=maze_gen.maze
            
            #i,o=random_start_exit(maze,num_in=num_in,num_out=num_out)
            maze[0][0]=0
            maze[-1][-1]=0
            i=[[0,0]]
            o=[[maze_size-1,maze_size-1]]
            #create spcaes near start/end
            maze[1][1]=0
            maze[0][1]=0
            maze[1][0]=0
            maze[0][2]=0
            maze[1][2]=0
            maze[2][2]=0
            maze[2][1]=0
            maze[2][0]=0

            maze[-1][-2]=0
            maze[-2][-2]=0
            maze[-2][-1]=0
            maze[-3][-1]=0
            maze[-3][-2]=0
            maze[-3][-3]=0
            maze[-2][-3]=0
            maze[-1][-3]=0

            tmt=maze.copy()
            tmt[0][0]=2
            tmt[-1][-1]=3
            print(tmt)
            print(o[0])
            print(i[0])
            game = Maze(maze,exit_cell=o,start_cell=tuple(i[0]))
            game.render(Render.NOTHING)
            model = models.QTableModel(game)
            #changed ep to larger
            cummul,win_perc,_, time,tot,count_tot = model.train(discount=0.90, exploration_rate=0.1, learning_rate=0.1, episodes=1000,stop_at_convergence=False,start_cell=tuple(o[0]))
            
            
            game.render(Render.NOTHING)
            status, moves, totmoves= game.play(model, start_cell=tuple(i[0]))
            #print(moves)
            #print(totmoves)
            #print((totmoves[-1][1][0][0],totmoves[-1][1][0][1]))
            #print((maze_size-1,maze_size-1))
            if (totmoves[-1][1][0][0],totmoves[-1][1][0][1])==((maze_size-1,maze_size-1)):
                print("accepted")
                tmp=dict={"Maze":maze.tolist(),"In":i,"Out":o,"Obs":obs,"Size":maze_size}
                
                with open('./realmazefiles/Maze_'+str(maze_size)+'_'+(str(obs).replace(".",""))+'_'+str(num_in)+'_'+str(num_out)+'_'+str(totit)+'.txt', 'w') as convert_file:
                    convert_file.write(json.dumps(tmp))
                    
                
                totit+=1



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




