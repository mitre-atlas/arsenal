# CALDERA plugin: **Arsenal**

Arsenal is a plugin developed for adversary emulation of AI-enabled systems. This plugin will provide TTPs defined in [`MITRE ATLAS`](https://atlas.mitre.org/) to interface with [`CALDERA`](https://github.com/mitre/caldera).

[`Read the full documentation`](https://mitre-atlas.github.io/arsenal/intro.html#arsenal)

For ml-attack-staging and ml-model-access abilities (see list below), additional information and [`examples`](https://advml.pages.mitre.org/arsenal/adversary.html#adversary-arsenal) on using these abilities are detailed in the arsenal/docs/ folder.


*JUNE 2023 included abilities:*

- Discover remote services
- Discover local services
- Discover available network services
- Search and stage Tensorflow model files/checkpoints
- Discover ML specific services - Torchserve
- Discover GPUs on a system
- Stage a local image for classification
- Install ML-related tools (on C2-server or victim system): Python, [`Microsoft Counterfit`](https://github.com/Azure/counterfit), Tensorflow-CPU, Tesorflow-GPU
- Gain API access to a served model (Torchserve)
- Build a custom Microsoft Counterfit target and stage an attack

*JUNE 2023 included Adversaries:*
- "Tensormancer" - Discover a Tensorflow model or checkpoint and stage an image for classification
- Exfiltrate a model or checkpoint file
- Stage an adversarial ML attack on a discovered ML model or service using Microsoft Counterfit library

# Usage

## System requirements: 
 - **Ubuntu 18.04** or **20.04** 
 - **Python version 3.7+**

    ### Plugin Dependencies:
     - [`Caldera Stockpile`](https://github.com/mitre/stockpile):  Some Arsenal abilities and adversaries require addition TTPs and requirements include in the Caldera Stockpile. A version more recent than this commit is required for these capabilities: [Stockpile](https://github.com/mitre/stockpile/tree/d128da223aa93f71841bb160ccb09fb9cb590345).
     - [`Microsoft Counterfit`](https://github.com/Azure/counterfit):  a required dependency to create and run adversarial machine learning attacks. This dependency is used by the [`Build and Attack a Custom CFTarget`](data/abilities/ml-attack-staging/5e437f42-cd5f-400f-b65d-d78821f31c69.yml) ability and its [payload](./payloads/build_and_attack_counterfit_target.py). 
         - If following the [Installation with Caldera](#installation-with-caldera*), this dependency is installed automatically on the C2 server (host). 
         - It can also be installed locally using the `requirements.txt` located in this repository or installed on remote machines using the [`Install Counterfit`](data/abilities/command-and-control/8a1913ed-4ddf-497c-8f95-ebf1eb93b518.yml) ability.

## Installation with CALDERA*:
 
 1. Navigate to [`caldera-atlas`](https://github.com/mitre-atlas/caldera-atlas) repository and follow steps for installation and setup.

 2. Navigate to the UI: `localhost:8888`

    **`arsenal` is not yet a default CALDERA plugin, therefore there are additional steps to include this plugin into the app.*


*Contact us atlas@mitre.org*

![overview](docs/assets/A.png)
