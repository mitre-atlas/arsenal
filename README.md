# CALDERA plugin: **Arsenal**

### This plugin will help store and create adversarial TTPs defined in [`ATLAS`](https://atlas.mitre.org/) to interfeace with [`CALDERA`](https://github.com/mitre/caldera). It can be used in conjuction with the plugin [`Almanac`](https://gitlab.mitre.org/advml/almanac/-/tree/develop). This is a mirror of the public repo: [`stockpile`](https://github.com/mitre/stockpile/tree/master) on its `master` branch

We recommend that you navigate to our [`DOCUMENTATION`](https://advml.pages.mitre.org/arsenal/intro.html#arsenal) for further details of the plugin and its purpose.

# Developers
## Installation with CALDERA app
 *`arsenal` is not yet a default CALDERA plugin, therefore there are additional steps to include this plugin into the app.*

 1. Install using **docker** (must have docker installed)
 ```code
 # run the following bash script

docker_script.sh
 ```

 - this will install all necessary repos: `caldera`, `almanac`, `ml-vulhub` 
 - build any/all docker containers to run the `caldera` app and start the server in a `tmux` session
 - build any/all docker containers to run and set up an initial "victim" using `ml-vulhub`

2. Install using a **linux** terminal and python 3.7+ (must have docker installed)

 ```code
 # run the following bash script

script.sh
 ```
  - this will install all necessary repos: `caldera`, `almanac`, `ml-vulhub` 
 - symlink all necessary repos to the caldera plugin directory so nesting repos is not required: `arsenal`, `almanac`
 - build any/all docker containers to run and set up an initial "victim" using `ml-vulhub`

 ## Navigate to the UI
 To navigate to the UI proceed to `localhost:8888` and you will be prompted to login into the `caldera` app. 

 Use the following credentials:

 Username: admin

 Password: admin

![overview](docs/assets/A.png)


- Do **NOT** push any code to `master` branch, this branch is reserved for pulling changes from the `stockpile` repo

- **All code relevant to `arsenal` that is not a development branch should be pushed to `main`**