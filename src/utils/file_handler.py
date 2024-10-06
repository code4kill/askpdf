import yaml
import os
from config import OUTPUT_DIR

def save_to_yaml(data, filename):
  os.makedirs(OUTPUT_DIR, exist_ok=True)
  output_path = os.path.join(OUTPUT_DIR, filename)
  
  with open(output_path, 'w') as file:
    yaml.dump(data, file, default_flow_style=False)
  print(f"Saved extracted data to {output_path}")
