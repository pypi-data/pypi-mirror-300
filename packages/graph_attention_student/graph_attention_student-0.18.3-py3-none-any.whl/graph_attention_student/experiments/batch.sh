#!/bin/bash
#SBATCH --cpus-per-task=20
#SBATCH --mem=90G
#SBATCH --time=03:00:00
#SBATCH --priority=10000
#SBATCH --job-name=megan

# Making sure to use the correct python env
source /media/ssd/Programming/graph_attention_student/venv/bin/activate
which python

# ~ rb-dual-motifs
# python /media/ssd/Programming/graph_attention_student/graph_attention_student/experiments/vgd_torch__megan__rb_dual_motifs.py \
#     --__DEBUG__=False \
#     --__PREFIX__="'5_layers'" \
#     --UNITS="[64, 64, 64, 64, 64]" \
#     --EPOCHS=100

# ~ compas
# python /media/ssd/Programming/graph_attention_student/graph_attention_student/experiments/vgd_torch__megan__compas.py \
#     --__DEBUG__=False \
#     --__PREFIX__="'5_layers'" \
#     --UNITS="[64, 64, 64, 64, 64]" \
#     --EPOCHS=25

# ~ aqsol
python /media/ssd/Programming/graph_attention_student/graph_attention_student/experiments/vgd_torch__megan__aqsoldb.py \
    --__DEBUG__=False \
    --__PREFIX__="'5_layers'" \
    --UNITS="[64, 64, 64, 64, 64]" \
    --EPOCHS=100