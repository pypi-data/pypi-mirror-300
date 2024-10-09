import argparse
import importlib.util
import os
import importlib
import yaml
import sys
import docker_interface
from pathlib import Path


dockerfile_commands = []
dockerfile_commands.append("FROM python:3.9-slim-buster")
dockerfile_commands.append("WORKDIR /app")
dockerfile_commands.append("RUN apt-get update")
dockerfile_commands.append("RUN apt-get install -y gcc")
dockerfile_commands.append("ENV PYTHONUNBUFFERED=1")
dockerfile_commands.append("COPY requirements.txt .")
dockerfile_commands.append("RUN pip install --no-cache-dir -r requirements.txt")
dockerfile_commands.append("COPY . .")

DEFAULTS = {
    "manifests_dir" : "manifests"
}

def create_deploy_docker_image(imageTag: str, mainfile:str):
    # Define the base image and working directory
    base_image = "python:3.9-slim-buster"
    workdir = "/app"

    # Define the Dockerfile commands
    dockerfile = []
    dockerfile.append(f"FROM {base_image}")
    dockerfile.append(f"WORKDIR {workdir}")
    dockerfile.append("COPY requirements.txt .")
    dockerfile.append("RUN pip install --no-cache-dir -r requirements.txt")
    dockerfile.append("COPY . .")
    dockerfile.append(f"CMD [\"python\", \"{mainfile}\"]")

    # Write the Dockerfile to disk
    with open("Dockerfile", "w") as f:
        f.write("\n".join(dockerfile))

    # Build the Docker image
    
    os.system(f"docker build -t {imageTag} .")
    os.system(f"docker push {imageTag}")
    os.remove("Dockerfile")
    

def apply_yaml(Module, imageTag:str, secret: str, dir_path: str):
    moduleName = f"{Module.name}-{Module.version}"
    files = {}
    
    for key, git in Module.directories.items():
        files[key] = {
            "localPath": key,
        }
        if "source" in git and git["source"] != "":
            git["secret"] = secret
            files[key]["preload"] = {
                "git" : {
                    "source" : git["source"],
                    "folder" : git["folder"],
                    "secret" : git["secret"]
                }
            }
    kafka = {}
    if len(Module.topics_envVars) > 0:
        kafka = {
                    "server": "KAFKA_BOOTSTRAP_SERVER",
                    "securityProtocol": "KAFKA_SECURITY_PROTOCOL",
                    "saslMechanism": "KAFKA_SASL_MECHANISM",
                    "username": "KAFKA_USERNAME",
                    "password": "KAFKA_PASSWORD",
                    "topics": Module.topics_envVars
                }
    
    
    data = {
        "apiVersion": "ecida.org/v5alpha1",
        "kind" : "Module",
        "metadata": {
            "name": moduleName,
            "namespace": "ecida-repository",
            "labels":{
                "template" : "default"
            },
            "annotations" :{
                "description": Module.description
            }
        },
        "spec":{
          "definitions": {
              "inputs": Module.inputs,
              "outputs": Module.outputs},
          "implementations":{
              "docker": {
                  "image": imageTag
              },
              "kafka":kafka,
              "file" : files,
              "env": {
                  "ECIDA_DEPLOY": "true"
              }
          }
        }
    }
    yamlFilename = f"auto_generated_{moduleName}.yaml"
    path = Path.joinpath(dir_path, yamlFilename)
    with open(path, "w") as f:
        yaml.dump(data, f)
        print(yamlFilename + " is generated")
    
def create_image_tag(username: str, M) -> str:
    imageName = username + "/" + M.name.lower()
    latest_tag, error = docker_interface.fetch_latest_tag(imageName)
    if error == None:
        imageTag, error = docker_interface.increment_tag(latest_tag)
        if error != None:
            imageTag = latest_tag + ".1"
    else:
        imageTag = M.version.lower()
    return imageName + ":" + imageTag

def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(prog="ecidacli")
    parser.add_argument("-f", "--main-file", help="main file to process (example: main.py)")
    
    subparsers = parser.add_subparsers(required= True, metavar="COMMAND", title="COMMAND", dest="command")
    parser_manifests = subparsers.add_parser('manifests', help='generate the kubernetes manifests')
    parser_build = subparsers.add_parser('build', help='build the container and push it to dockerhub')
    parser_version = subparsers.add_parser('version', help='print ecidacli version')
    
    # Add arguments to the parser
    parser_build.add_argument("-u", "--username", help="username for Dockerhub authentication")
    parser_manifests.add_argument("-u", "--username", help="username for Dockerhub authentication")
    parser_manifests.add_argument("-s", "--secret", help="name of secret in the kubernetes-cluster")
    parser_manifests.add_argument("-d", "--dir", help="directory to put yaml files [default: manifests]")

    # Parse the command line arguments
    
    args = parser.parse_args()
    
    
    # Import the module dynamically
    try:
        if args.command == "manifests":      
            manifests(args)
        elif args.command == "build":
            build(args)
        elif args.command == "version":
            print("ecidacli version: v0.0.23")
            
    except Exception as e:
        print(e)
        # print(f"{mainfile} does not contain an EcidaModule")
    
def common(main_file: str, username: str):
    module_name = Path(main_file).stem
    spec = importlib.util.spec_from_file_location(module_name, main_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
    M = module.create_module()
    imageTag = create_image_tag(username, M)
    return M, imageTag
    
def manifests(args):
    # Parsing arguments
    main_file = args.main_file    
    username = args.username
    secret = args.secret
    manifests_dir = args.dir
    if manifests_dir == None:
        manifests_dir = DEFAULTS["manifests_dir"]      
        
    # Creating Module
    M, imageTag = common(main_file, username)
    
    # Creating Path
    dir_path = Path(main_file).parent.absolute()
    dir_path = Path.joinpath(dir_path, manifests_dir)
    dir_path.mkdir(exist_ok=True, parents=True)
    
    # Create and dump yaml
    apply_yaml(M, imageTag, secret,dir_path)
    
    
def build(args):
    # Parsing Arguments
    main_file = args.main_file    
    username = args.username
    
    M, imageTag = common(main_file, username)
    dirname = os.path.dirname(main_file)
    os.chdir(dirname)
    basefile = os.path.basename(main_file)
    create_deploy_docker_image(imageTag, basefile)
    print(f"{main_file} built successfully")
    

if __name__ == "__main__":
    main()

