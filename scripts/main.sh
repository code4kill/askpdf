#!/bin/bash

## Copyright (c) 2024 mangalbhaskar. All Rights Reserved.
##__author__ = 'mangalbhaskar'
###----------------------------------------------------------

## Simple script to run the Python module with variable expansion for parameters

from_file=${1:-"data/2024-comprehensive_study_of_driver_behavior_monitoring_systems_using_computer_vision-qu_et_al.pdf"}  # First argument: PDF file path
to_dir=${2:-"logs/$(date +'%d%m%y_%H%M%S')"}  # Second argument: Output directory with default to logs/<timestamp>

python -m src.main --from "$from_file" --to "$to_dir"
