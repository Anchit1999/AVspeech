#!/bin/bash

module load ffmpeg/4.2.1
python3 avs.py --jobs 4 --file avspeech_train3.csv --output_dir /ssd_scratch/cvit/anchit/
