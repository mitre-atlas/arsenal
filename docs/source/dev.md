# Developers

There are multiple ways to run the Arsenal plugin within CALDERA. The recommended way is mounting the plugin as a *volume* in a Docker container, which allows for active development and modification of hte plugin without restarting the CALDERA server.

*For more information on the Adversary or the Victim services, navigate to those pages.*

## 1. Clone Arsenal repo and Almanac repo:

**Arsenal**: MITRE ATLAS TTPs

```
git clone git@gitlab.mitre.org:advml/arsenal.git
```

**Almanac**: repo containing MITRE ATLAS and ability to create adversary profiles that can be loaded via `Arsenal` (coming).
```
git clone git@gitlab.mitre.org:advml/almanac.git

```


## 2. HARBOR: Docker images
We recommend using the container-manager resources for development, which includes a host of pre-built docker images. The images most used with this plugin will be:

 - caldera-dev:4.0.0
 - caldera-dev:4.1.0

To request access to Harbor, navigate to: `butler.mitre.org/harbor`

 - Use your MITRE SUI and password to login
 - Navigate to the `ATLAS` project page (you must be given access first)
    
Use the ```PULL``` tab to copy the command or pull directly using the `TAG`:

```
docker pull butler.mitre.org/atlas/<IMAGE>:<TAG>
```

You must periodically login into Harbor to pull new images and push new images (only certain users will be able to push to the atlas folder for obvious reasons). To login, in your terminal:

```code

docker login butler.mitre.org
 >>> MITRE SUI
 >>> MITRE Password

```

## 3. Automatically Run CALDERA + Arsenal:
### It is recommended to edit your `.bashrc` to instantiate a docker container with the `arsenal` and `almanac` plugins mounted to a running CALDERA container

To do so, run the following bash script, which will:

- install tmux
- edit `.bashrc` with the docker run command inside a persistent `tmux` session named "caldera"

```code 
script.sh
```

## 4. Setup a "Victim" System

Arsenal abilities, adversaries, and operations require a victim system to be running on another system that can be accessed via an API (Rest) or via SSH (curl) commands.

 To setup the basic `mmdet-serve`, a pytorch model trained for object detection, pull the latest docker image hosted on Harbor:

 ```
docker pull butler.mitre.org/atlas/mmdet-serve:retinanet

docker run -d -p <port>:<port> butler.mitre.org/atlas/mmdet-serve:retinanet
```

You can also choose to use [`ml-vulhub`](git@gitlab.mitre.org:advml/ml-vulhub.git) (**recommended**) which is an open-source collection of pre-built vulnerable docker environments running services:

