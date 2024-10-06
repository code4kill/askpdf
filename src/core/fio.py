import yaml
import os

def save_to_yaml(data, file_path):
  with open(file_path, 'w') as file:
    yaml.dump(data, file, default_flow_style=False)

def write_to_file(file_path:str, content):
  with open(file_path, "w+") as file:
    file.write(content)
