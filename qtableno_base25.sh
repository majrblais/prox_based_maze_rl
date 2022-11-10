#!/bin/bash
#SBATCH --account=def-akhloufi
#SBATCH --cpus-per-task=32
#SBATCH --mem=16G
#SBATCH --time=0-70:60:00

cd /home/emb9357/scratch
source maze/bin/activate

cd ./maze
python qtabletrainno_base25.py
