# CALDERA plugin: **Arsenal**

Arsenal is a plugin developed for adversary emulation of AI-enabled systems. This plugin will provide TTPs defined in [`MITRE ATLAS`](https://atlas.mitre.org/) to interface with [`CALDERA`](https://github.com/mitre/caldera).

[`Read the full documentation`](https://mitre-atlas.github.io/arsenal/intro.html#arsenal)

For ml-attack-staging and ml-model-access abilities (see list below), additional information and [`examples`](https://advml.pages.mitre.org/arsenal/adversary.html#adversary-arsenal) on using these abilities are detailed in the arsenal/docs/ folder.


*JUNE 2023 included abilities:*

- Discover remote services
- Discover local services
- Discover available network services
- Discover ML specific services - Torchserve
- Discover GPUs on a system
- Exfiltrate ML model
- Stage a ML attack on a discovered ML model using[`counterfit`](https://github.com/Azure/counterfit) library

# Usage

## System requirements: 
 - **Ubuntu 18.04** or **20.04** 
 - **Python version 3.7+**

    ### Plugin Dependencies:
     - [`Caldera Stockpile`](https://github.com/mitre/stockpile):  Some Arsenal abilities and adversaries require addition TTPs and requirements include in the Caldera Stockpile. A version more recent than this commit is required for these capabilities: --.
     - [`Microsoft Counterfit`](https://github.com/Azure/counterfit):  a required dependency to create and run adversarial machine learning attacks. This dependency is used by the [`Build and Attack a Custom CFTarget`](data/abilities/ml-attack-staging/5e437f42-cd5f-400f-b65d-d78821f31c69.yml) ability and its [payload](./payloads/build_and_attack_counterfit_target.py). This dependency can be installed locally using the `requirements.txt` located in this repository or installed on remote machines using the [`Install Counterfit`](data/abilities/command-and-control/8a1913ed-4ddf-497c-8f95-ebf1eb93b518.yml) ability.

## Installation with CALDERA*:
 
 1. Navigate to [`caldera-atlas`](https://github.com/mitre-atlas/caldera-atlas) repository and follow steps for installation and setup.

 2. Navigate to the UI: `localhost:8888`

    **`arsenal` is not yet a default CALDERA plugin, therefore there are additional steps to include this plugin into the app.*


![overview](docs/assets/A.png)
