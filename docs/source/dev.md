# Developers

There are multiple ways to run the `ARSENAL` plugin within `CALDERA`. The recommended way is mounting the plugin as a *volume* in a Docker container, which allows for active development and modification of the plugin without restarting the CALDERA server.

Alternative deployment requires re-starting the `CALDERA` server when changes to the plugin are made.


## 1. Clone ARSENAL repo:

**ARSENAL**: MITRE ATLAS TTPs

```code
git clone git@gitlab.mitre.org:advml/arsenal.git
```

## 2. Run CALDERA + ARSENAL and setting up a Victim system:

*Recommended:

Run the bash script which will:

- clone the necessary repos: `caldera`, `alamanc`, `ml-vulhub` and install any dependencies
- install tmux
- run the necessary docker commands to build `caldera`
- edit the .bashrc to automatically start the `caldera` server and mount `arsenal` to the correct mount point in a persistent tmux session
- deploy a vulnerable environment via `ml-vulhub`

```code
# Run the script proved in the `arsenal` repo

docker_script.sh
```

Alternatively, users can also choose to run CALDERA and the Arsenal plugin by symlinking the Arsenal directory to CLADERA's plugin directory. This allows for active development of `arsenal` whilie keeping the repos separated. However, this will require users to restart the `caldera` server when changes are made to the `arsenal` plugin.  

To do so, run the following bash script, which will:
- clone the necessary repos: `caldera`, `alamanc`, `ml-vulhub` and install any dependencies
- deploy a vulnerable environment via `ml-vulhub`
- symlink `almanac` and `arsenal` to CALDERA's plugin directory
- start the `caldera` server


```code
# Run the script proved in the `arsenal` repo

script.sh
```

*For more information on the Adversary or the Victim services, navigate to those pages.*

**this requires docker to be installed on your machine*
