# How-To Guides for Development

This section includes practical, *how-to* guides, for a **developer** to achieve something.  
Guides on how to **run tests** against your code, how to **publish to PyPI**, how to build
a Docker Image and **publish it to Dockerhub**, how to do `Static Code Analysis`, etc.


## How to prevent any Image from being published to Dockerhub

1. Open your `.github/workflows/test.yaml`, and look for the **Worfklow Variables**
 
    **Worfklow Variables** are defined in the `env` *section*

2. Set `DOCKER_JOB_ON` value to **false**
    
    *key* and **set value to false**