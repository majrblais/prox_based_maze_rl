#!/usr/bin/env python
# coding: utf-8
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "5"
from os import listdir
import json
from os.path import isfile, join
mypath="25_files"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
from environment.maze import Maze, Render
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import models
import logging
from enum import Enum, auto
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.set_option('display.max_colwidth', None)


for j in range(len(onlyfiles)):
    print(onlyfiles[j])
    with open('./'+mypath+'/'+onlyfiles[j]) as f:
        data = f.read()
        
    js = json.loads(data)
    js['Maze']=np.asarray(js['Maze'])
    game = Maze(js['Maze'],rew="Base", exit_cell=js['Out'],start_cell=tuple(js["In"][0]))
    game.render(Render.NOTHING)
    model = models.QTableModel(game)
    cummul,win_perc,ep, time,tot,count_tot = model.train(opt=False,discount=0.90, exploration_rate=0.1, learning_rate=0.1, episodes=250,stop_at_convergence=True,start_cell=tuple(js['In'][0]))
    game.render(Render.NOTHING)
    status, moves, totmoves= game.play(model, start_cell=tuple(js['In'][0]))
    df = pd.read_csv('bres_qtableno_base_25.csv',header=0)
    tmp=[onlyfiles[j],js['Maze'],js['Out'],js['In'],js['Obs'],cummul,count_tot,moves,time,totmoves,ep]
    a_series = pd.Series(tmp, index = df.columns)
    mydataframe = df.append(a_series, ignore_index=True)
    mydataframe.to_csv("bres_qtableno_base_25.csv",index=False)

