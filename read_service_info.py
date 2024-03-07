import yaml
import os

# Get the directory of the current script
script_directory = os.path.dirname(os.path.realpath(__file__))

# Construct the path to the YAML file in the same directory
yaml_file_path = os.path.join(script_directory, "service_info.yml")

def process_serviceInfo(yaml_file_path):
    # Read YAML file
    with open(yaml_file_path, "r") as file:
        data = yaml.safe_load(file)
        service_info_content = data.get("service_info", {})

    result_dict = {}

    # Process keys with "terraform" in their name
    for key, value in service_info_content.items():
        if "terraform" in key:
            result_dict[key] = value
    return result_dict