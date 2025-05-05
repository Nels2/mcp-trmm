import yaml
import json

# Load YAML data from a file
with open('rmm.yaml', 'r') as yaml_file:
    yaml_data = yaml.safe_load(yaml_file)

# Convert to JSON and print
json_data = json.dumps(yaml_data, indent=4)
print(json_data)

# Optionally, save to a new file
with open('rmm_schema.json', 'w') as json_file:
    json_file.write(json_data)
