# ECIDA

```
usage: ecidacli [-h] [-f MAIN_FILE] COMMAND [args]

options:
  -h, --help            show this help message and exit
  -f MAIN_FILE, --main-file MAIN_FILE
                        Main file to process (example: main.py)

COMMAND:
   manifests            generate the kubernetes manifests
   build                build the container and push it to dockerhub

args:
  -u USERNAME, --username USERNAME
                        username for Dockerhub authentication
  -s SECRET, --secret SECRET
                        name of secret in the kubernetes-cluster
```