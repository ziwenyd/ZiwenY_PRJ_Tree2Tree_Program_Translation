# Tree-to-tree Neural Networks for Program Translation

This folder provides code implementation of Paper [[arXiv](https://arxiv.org/abs/1802.03691)][[NeurIPS](https://papers.nips.cc/paper/7521-tree-to-tree-neural-networks-for-program-translation)]

The code implementation was initially built by Chent et al. and published with their paper; further extended by Ziwen Yuan as BSc final year project (PRJ) at King's College London, supervised by Kevin Lano.

Chen et al. Paper Citation:

```
@inproceedings{chen2018tree,
  title={Tree-to-tree Neural Networks for Program Translation},
  author={Chen, Xinyun and Liu, Chang and Song, Dawn},
  booktitle={Proceedings of the 31st Advances in Neural Information Processing Systems},
  year={2018}
}
```

# Prerequisites

check `requirements.txt`.

# Datasets

## CS-JS dataset from Chen et al.

The datasets can be found [here](https://drive.google.com/open?id=1LDQOVcgFLrTRjIXH3Tc7kzmoAGK2vVKo).

## Python-JavaScript dataset for Ziwen Yuan's Final Project

/parser/data/train_data
/parser/data/validation_data
/parser/data/atom_test_data

# Usage

## Model architectures

The code includes the implementation of following models:

- Seq2seq: in `src/translate.py`, set `--network` to be `seq2seq`.
- Seq2tree: in `src/translate.py`, set `--network` to be `seq2tree`.
- Tree2seq: in `src/translate.py`, set `--network` to be `tree2seq`.
- Tree2tree: in `src/translate.py`, set `--network` to be `tree2tree`.
  - Without attention: set `--no_attention` to be `True`.
  - Without parent attention feeding: set `--no_pf` to be `True`.

## Run experiments

In the following we list some important arguments in `translate.py`:

- `--train_data`, `--val_data`, `--test_data`: path to the preprocessed dataset.
- `--load_model`: path to the pretrained model (optional).
- `--train_dir`: path to the folder to save the model checkpoints.
- `--input_format`, `--output_format`: can be chosen from `seq` (tokenized sequential program) and `tree` (parse tree).
- `--test`: add this command during the test time, and remember to set `--load_model` during evaluation.

## Train the model

```bash
python translate.py --network tree2tree --train_dir ../model_ckpts/tree2tree/ --input_format tree --output_format tree
```

#python3

```bash
python3 translate.py --network tree2tree --train_dir ../model_ckpts/tree2tree/ --input_format tree --output_format tree
```

```bash
python3 translate.py --network tree2tree \
--train_dir ../model_ckpts/tree2tree/ \
--input_format tree \
--output_format tree \
--num_epochs 25 \
--batch_size 5 \
--steps_per_checkpoint 5 \
--learning_rate_decay_steps 30 \
--train_data ../../parser/data/source_py_target_js_train.json \
--val_data ../../parser/data/source_py_target_js_validation.json
```

## Atom Test the Model

```bash
python3 translate.py --network tree2tree --test --load_model ../model_ckpts/tree2tree/translate_1.ckpt --input_format tree --output_format tree
```

### Run with best eval loss model:

```bash
python3 translate.py --network tree2tree \
--train_data ../../parser/data/source_py_target_js_train.json \
--batch_size 1 \
--test \
--load_model ../model_ckpts/tree2tree/final_best_eval_loss_translate_30.ckpt \
--test_data ../../parser/data/source_py_target_js_atom_test.json \
--input_format tree \
--output_format tree
```

### Run with best loss score model:

```bash
python3 translate.py --network tree2tree \
--train_data ../one_object_data/PY-JS/source_py_target_js_train.json \
--batch_size 1 \
--test \
--load_model ../model_ckpts/tree2tree/final_best_loss_translate_385.ckpt \
--test_data ../one_object_data/PY-JS/source_py_target_js_atom_test.json \
--input_format tree \
--output_format tree
```

# Experiment this Model on other dataset

## CS-JS small dataset

data size = 100, obtained using the data_splitter.py script.

### train

```bash
python3 translate.py --network tree2tree \
--train_dir ../model_ckpts/tree2tree/ \
--input_format tree \
--output_format tree \
--num_epochs 25 \
--batch_size 5 \
--steps_per_checkpoint 5 \
--train_data ../mini_data/CS-JS/BL/preprocessed_progs_train.json \
--val_data ../mini_data/CS-JS/BL/preprocessed_progs_valid.json
```

### test

```bash
python3 translate.py --network tree2tree \
--train_data ../mini_data/CS-JS/BL/preprocessed_progs_train.json \
--batch_size 5 \
--test \
--load_model ../model_ckpts/tree2tree/best_eval_loss_translate_5.ckpt \
--test_data ../mini_data/CS-JS/BL/preprocessed_progs_test.json \
--input_format tree \
--output_format tree
```

# Run this project (job) on Rosalind machine

ssh into Rosalind HPC cluster

```bash
ssh k18XXXXX@login.rosalind.kcl.ac.uk
cd src
```

with GPU:

```bash
sbatch -p shared_gpu rosalind_t2t_train.sh
```

without GPU:

```bash
sbatch -p shared rosalind_t2t_train.sh
```

result will be saved into the 'rosaline_t2t_train.out' file.

## Rosalind Brief Instruction

For official documentation, see: https://rosalind.kcl.ac.uk/hpc/running_jobs/

### submit a job to Rosalind cluster job scheduler

sbatch -p <partition> rosalind_t2t_train.sh

-p option: specifies the partition name.

### more memory

By default, one job can use at most 1GB memory, 1 CPU core, runtime 24 hours.
To specify an amount of memory to allocate per core, use the --mem-per-cpu=<MB> option.

For the Python-JavaScript data used in this project, it is less than 1GB (as small as around 15MB).

### run GPU job

One job can at most reserve a single GPU.

Your GPU enabled application will mostly likely make use of the NVidia CUDA libraries, to load the CUDA module use module load libs/cuda in your job submission script.

### check my running jobs

squeue --long -u k1802312

## Rosalind Environment Setup

The environment of this project is managed by python virtual machine with pip.
Required Python packages and version info are written in the 'requirement.txt' file.To build the same environment as me, do the following:

```bash
cd tree2tree
```

create a python virtual machine (if not have one already)

```bash
python3 -m venv virtual_environment_name
```

activate your python virtual machine

```bash
source virtual_environment_name/bin/activate
```

install the packages with desired version as recorded in the requirements.txt file

```bash
pip3 install -r requirements.txt
```

If you need to generate a new requirement file, use this command:

```bash
pip3 freeze > requirements.txt
```
