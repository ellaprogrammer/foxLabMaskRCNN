#!/bin/bash
#
#SBATCH --job-name=RURIKO_TENSORFLOW # Job name
#SBATCH --array=1
#SBATCH --nodes=1
#SBATCH --ntasks=1 # Number of cores
#SBATCH --output=train_network.out #File to which STDOUT will be written
#SBATCH --error=train_network.err # File to which STDERR will be written
#SBATCH --mail-type=ALL # Type of email notification- BEGIN,END,FAIL,ALL
#SBATCH --mail-user=raimai@ucdavis.edu # Email to which notification will be sent
#SBATCH --time=425:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=50000

source activate tensorflow

protoc /share/foxlab-backedup/monkeyface/models/research/object_detection/protos/*.proto --python_out=/share/foxlab-backedup/monkeyface/models/research/
export PYTHONPATH=$PYTHONPATH:/share/foxlab-backedup/monkeyface/models/research:/share/foxlab-backedup/monkeyface/models/research/slim

/share/foxlab-backedup/monkeyface/anaconda3/envs/tensorflow/*in/python setup.py install

pwd
which python
protoc --version

cd /share/foxlab-backedup/monkeyface/models/research/object_detection/
pwd

python train.py --logtostderr --train_dir=training/ --pipeline_config_path=training/ssd_mobilenet_v1_pets.config
