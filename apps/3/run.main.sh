#!/bin/bash

PATH=$1
QUERY=$2

# Check if both arguments are provided
if [ -z "$PATH" ] || [ -z "$QUERY" ]; then
  echo "Usage: $0 <path_to_file> <query>"
  exit 1
fi

echo "Path of the file: $PATH"
echo "Query for the file: $QUERY"

# Run the Python script with the provided arguments
python main.py --input_pdf "$PATH" --query "$QUERY"

################################################################
# Example usage:
# create virtual environment using lsd-install-create.virtualenv or cond env
# Install required packages pip install -r requirement.txt
# Execute the commands
# python main.py --input_pdf /codehub/aihub/external/practice/apps/askpdf/data/yolov10-2405.14458v1.pdf --query "What is the conclusion of this documents"


# Output most Relevents chunks from docs 
# We can use prompt templating to streamline the Q&A with docs 
# Pass Docs and prompts TEMPLATE TO openAI API for answer !!!
