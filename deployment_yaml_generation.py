import yaml
import os
import read_service_info as serviceInfo
import base64
import requests
import region_map as regionMap
import re
import copy
import ruamel.yaml

#-----------Git Repo Info--------------
base_url = "https://api.github.com/repos"
repo_owner = "namdevaman"
github_token = "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"
#----------------End--------------------
#-------Map Region-----------------
project_zone_map=[
 {
   "name": "North America",
   "region_continent": "us",
   "code": "us",
   "storage_location": "us",
   "values": [
                {
                  "region": "East",
                  "region_sector": "e1",
                  "code": "east",
                  "id": "01",
                  "details":
                    {
                      "zone_1":"1-B",
                      "zone_2":"1-C",
                      "zone_3":"1-D"
                    }
                },
                {
                  "region": "Central",
                  "region_sector": "c1",
                  "code": "central",
                  "id": "02",
                  "details":
                    {
                      "zone_1":"1-A",
                      "zone_2":"1-B",
                      "zone_3":"1-C"
                    }
                },
                {
                  "region": "West",
                  "region_sector": "w1",
                  "code": "west",
                  "id": "03",
                  "details":
                    {
                      "zone_1":"1-A",
                      "zone_2":"1-B",
                      "zone_3":"1-C"
                    }
                }
             ]
 },
 {
   "name": "Asia",
   "region_continent": "as",
   "code": "asia",
   "values": [
                {
                   "region": "East",
                   "region_sector": "e1",
                   "code": "east",
                   "id": "01",
                   "details":
                    {
                      "zone_1":"1-B",
                      "zone_2":"1-C",
                      "zone_3":"1-D"
                    }
                },
                {
                   "region": "South",
                   "region_sector": "s1",
                   "code": "south",
                   "id": "04",
                   "details":
                    {
                      "zone_1":"1-A",
                      "zone_2":"1-B",
                      "zone_3":"1-C"
                    }
                }
             ]
 },
 {
   "name": "Australia",
   "region_continent": "au",
   "code": "australia",
   "values": []
 },
   {
    "name": "Europe",
    "region_continent": "eu",
    "code": "europe",
    "storage_location": "eu",
    "values": [
      {
        "region": "West3",
        "region_sector": "w3",
        "code": "west3",
        "id": "03",
       "details": {
          "zone_1": "3-A",
          "zone_2": "3-B",
          "zone_3": "3-C"
        }
      },
    {
        "region": "West4",
        "region_sector": "w4",
        "code": "west4",
        "id": "04",
        "details": {
          "zone_1": "4-A",
          "zone_2": "4-B",
          "zone_3": "4-C"
        }
      }
    ]
  }
]
 
def isnumber(project_id,stack_id,env_id,instance_id,cluster_id):
  if not isinstance(project_id,(int,float)):
    print("project_id" +" should be number.")
    exit()
  if not isinstance(stack_id,(int,float)):
    print("stack_id" +" should be number.")
    exit()
  if not isinstance(env_id,(int,float)):
    print("env_id" +" should be number.")
    exit()
  if not isinstance(instance_id,(int,float)):
    print("instance_id" +" should be number.")
    exit()
  if not isinstance(cluster_id,(int,float)):
    print("cluster_id" +" should be number.")
    exit()
    
def isStr(project_name,project_code,stack_code,env_name,instance_name):
  if isinstance(project_name,str)==False:
    print("project_name should be alphabets only")
    exit()
  if isinstance(project_code,str)==False:
    print("project_code should be alphabets only")
    exit()
  if isinstance(stack_code,str)==False:
    print("stack_code should be alphabets only")
    exit()
  if isinstance(env_name,str)==False:
    print("env_name should be alphabets only")
    exit()
  if isinstance(instance_name,str)==False:
    print("instance_name should be alphabets only")
    exit()
  

def validate_input_data(project_name,project_code,project_id,stack_code,stack_id,env_name,env_id,instance_name,instance_id,cluster_id):
  
  isStr(project_name,project_code,stack_code,env_name,instance_name)
  isnumber(project_id,stack_id,env_id,instance_id,cluster_id)
  return
#-----------------------End-----------------------------
# -------------------Getting Input From Users---------------------
data_center = input("Data Center (e.g., North America, Asia, Europe): ")
data_region = input("Enter Region (e.g., East, West): ")
project_name=input("Enter project name (e.g., KENG, KACD, DACD, KCFN, DCUS11): ").upper()
project_code = input("Enter project code (e.g., keng): ").lower()
project_id = input("Enter project ID (e.g., 03): ")
stack_code = input("Enter stack code (e.g., gss): ").lower()
stack_id = input("Enter stack ID (e.g., 03): ")
env_name = input("Enter environment name (e.g., dev): ")
env_id = input("Enter environment ID (e.g., 03): ")
instance_name = input("Enter instance name (e.g., ins): ")
instance_id = input("Enter instance ID (e.g., 01): ")
service_name=""
cluster_id = input("Enter cluster ID (e.g., 08): ")
# validate_input_data(project_name,project_code,project_id,stack_code,stack_id,env_name,env_id,instance_name,instance_id,cluster_id)
#---------------------------End--------------------------------------
#---------------Making Custom Variables---------------------
region = regionMap.get_region_code(project_zone_map,data_center,data_region)
env_path = f'{env_name}{env_id}-'
project_path = f'{project_code}{project_id}-'
# for this purpose ---- https://selfservice-4.rightscale.com/manager/exe/65af521df727f1003671983e?ref=copy_inputs
#if instance code and id is not provided 
instance_path=""
if instance_name!="":
  instance_path = f'{instance_name}{instance_id}-'
stack_path = f'{stack_code}{stack_id}-'
if project_name in ['KENG', 'KACD', 'DACD']:
    project_folder = 'dev'
elif project_name in ['KCFN', 'DCUS11', 'DCUS14', 'DCUS21']:
    project_folder = 'prd'
#-----------------------------------------End---------------------------------------------
#------Authentication & Token Access & 'data' which will be injected in file at repo------
#folder_name= f'environments/{env_name}/{project_name}{project_id}/{env_name}{env_id}/{project_code}{project_id}-{env_path}{instance_name}{instance_id}-{service_name}{service_id}-dbs-{region}/inputs.yaml'
headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github+json"
}
repository_name = "GHA_Service"
branch = "main"
params = {'ref': branch}
data = {
    "message": f"Create folder ''",

    "content": base64.b64encode("".encode()).decode('utf-8'),  # Empty content for folder
    "committer": {
        "name": "Aman Namdev",
        "email": "amannamdev2809@gmail.com"
        }
}
#-----------------------------------------End---------------------------------------------
#--------Accessing the templates/inputs.yml file which will be injected in the file-------------
input_file_url = f'https://raw.githubusercontent.com/{repo_owner}/{repository_name}/main/templates/inputs.yml'
try:
    response = requests.get(input_file_url)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx status codes)
    
    
    placeholder_pattern = r'\b(\w+_STUB)\b'
    
    response = re.sub(placeholder_pattern, lambda match: input(f"Enter actual value for {match.group(1)}: "), response.text)

    # Assign the new column content in the "data" object
    data["content"] = base64.b64encode(response.encode()).decode('utf-8')

except requests.exceptions.RequestException as e:
    print(f"Failed to fetch file. Exception: {e}")
#--------------------------------------------End-------------------------------------------------
# # code for reading the content which will injected into input.yml
# content_file_path = os.path.join(script_directory, "input_file_template.yml")
# with open(content_file_path, "r") as content_file:
#     content = content_file.read()
    
# #here we assigning the new coloumn content in "data" object
# data["content"] = base64.b64encode(content.encode()).decode('utf-8')
#-----------Accessing the path of service_info.yml----------- 

script_directory = os.path.dirname(os.path.realpath(__file__))
yaml_file_path = os.path.join(script_directory, "service_info.yml")
#--------------------------End-----------------------------
service_path={}   #for storing the path of each service at any level.
# Getting the services information
service_data = serviceInfo.process_serviceInfo(yaml_file_path)
for service_name, service_info in service_data.items():
    print(f"Processing service: {service_name}")
    service_name_identifier=service_info['service_identifier']
    function_code=service_info['function_code']
    print(service_name)
    if service_info['service_level'] == 'stack':
        folder_name= f'environments/{project_folder}/{project_code}{project_id}/{stack_code}{stack_id}/{project_path}{stack_path}{service_name_identifier}{cluster_id}-{function_code}-{region}/inputs.yaml'
        service_path[service_name]=f"{project_path}{stack_path}{service_name_identifier}{cluster_id}-{function_code}-{region}"
    elif service_info['service_level'] == 'environment':
        folder_name= f'environments/{project_folder}/{project_code}{project_id}/{env_name}{env_id}/{project_path}{env_path}{service_name_identifier}{cluster_id}-{function_code}-{region}/inputs.yaml'
        service_path[service_name]=f"{project_path}{env_path}{service_name_identifier}{cluster_id}-{function_code}-{region}"
    elif service_info['service_level'] == 'instance':
        folder_name= f'environments/{project_folder}/{project_code}{project_id}/{env_name}{env_id}/{project_path}{env_path}{instance_path}{service_name_identifier}{cluster_id}-{function_code}-{region}/inputs.yaml'
        service_path[service_name]=f"{project_path}{env_path}{instance_path}{service_name_identifier}{cluster_id}-{function_code}-{region}"
    elif service_info['service_level'] == 'wfm':
        wfm_name = service_info['service_identifier']
        function_code=service_info['function_code']
        folder_name= f'environments/{project_folder}/{project_code}{project_id}/{env_name}{env_id}/{project_path}{env_path}{instance_path}{wfm_name}{cluster_id}-{function_code}-{region}/inputs.yaml'
        service_path[service_name]=f"{project_path}{env_path}{instance_path}{wfm_name}{cluster_id}-{function_code}-{region}"
    try:
        url = f'https://api.github.com/repos/{repo_owner}/{repository_name}/contents/{folder_name}'
        response = requests.put(url, headers=headers, params=params, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(f"Folder '{folder_name}' created successfully. Response: {response.json()}")
        for key,value in service_path.items(): 
          print(key + " : " + value)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        print(f"Response content: {response.content if 'response' in locals() else None}")

def fetch_operations_yaml(repo_owner, repository_name, branch, github_token):
    # GitHub API endpoint for retrieving file contents
    url = f"https://api.github.com/repos/{repo_owner}/{repository_name}/contents/templates/operations.yml"
    # Request headers including authentication
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }
    # Parameters for specifying the branch
    params = {'ref': branch}
    # Make GET request to retrieve file contents
    response = requests.get(url, headers=headers, params=params)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        content = response.json()
        # Decode the content (base64) and return
        return base64.b64decode(content['content']).decode('utf-8') 
    else:
        # If request was not successful, print error message and return None
        print(f"Error fetching operations.yml: {response.status_code} - {response.text}")
        return None
repo_owner = "namdevaman"
repository_name = "GHA_Service"
branch = "main"
github_token = "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"

# Load service_info.yml file
script_directory = os.path.dirname(os.path.realpath(__file__))
yaml_file_path = os.path.join(script_directory, "service_info.yml")
service_data = serviceInfo.process_serviceInfo(yaml_file_path)

operations_file_path = os.path.join(script_directory, "operations.yml")
with open(operations_file_path, 'r') as operations_file:
    operations_data = yaml.safe_load(operations_file)['operations']

# Initialize dictionary to store service data
services_info = {'general': {}, 'services': {}}
# Iterate over service entries in service_data
for service_name, service_info in service_data.items():
    operations_data=fetch_operations_yaml(repo_owner, repository_name, branch, github_token)
    operations_data=yaml.safe_load(operations_data)['operations']
    for action in operations_data['production_mode']:
      action['params']['APP_NAME'] = service_path[service_name]
    depends_on=service_info['depends_on']
    service_yaml ={
                'GUID': 'GUID_STUB',
                'deployment_name': 'ppas_tms 09.04.00 ...',
                'release_version': service_info['release_tag'],
                'repo_name': service_info['repo_name'],
                'input_folder_name': service_path[service_name],  # replacement needed
                'depends_on': copy.deepcopy(depends_on),
                'operations': copy.deepcopy(operations_data),
                'override_types': {}
    }
    # if 'operations' in service_yaml['operations']:
    #     service_yaml['operations'] = yaml.safe_load(service_yaml['operations'])

    services_info['services'][service_name] = service_yaml

file_path = 'services_github_tested.yaml'
with open(file_path, 'w') as file:
    yaml.dump(services_info, file, sort_keys=False)
# with open(file_path, 'w') as file:
#     yaml.dump(services_info, file, default_flow_style=False)
