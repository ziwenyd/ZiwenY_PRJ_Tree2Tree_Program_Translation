#!/bin/bash -l
#SBATCH --job-name=train_t2t
#SBATCH --output=rosalind_train_output.txt
#SBATCH --gres=gpu
#SBATCH --constrain=v100
module load libs/cuda

cd dev_src

python3 translate.py --network tree2tree \
--train_dir ../model_ckpts/tree2tree/ \
--input_format tree \
--output_format tree \
--num_epochs 100 \
--batch_size 5 \
--steps_per_checkpoint 5 \
--train_data ../../parser/data/source_py_target_js_train.json \
--val_data ../../parser/data/source_py_target_js_validation.json