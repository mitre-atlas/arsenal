# CALDERA plugin: **Arsenal**

Arsenal is a plugin developed for adversary emulation of AI-enabled systems. This plugin will provide TTPs defined in [`MITRE ATLAS`](https://atlas.mitre.org/) to interfeace with [`CALDERA`](https://github.com/mitre/caldera).

[` Read the full documentation`](https://mitre-atlas.github.io/arsenal/intro.html#arsenal)

For ml-attack-staging and ml-model-access abilities (see list below), additional information and [`examples`](https://advml.pages.mitre.org/arsenal/adversary.html#adversary-arsenal) on using these abilities are detailed in the arsenal/docs/ folder


*JUNE 2023 included abilities:*

- discover remote services
- discover local services
- discover available network services
- discover ML specific services - Torchserve
- exfiltrate ML model
- stage a ML attack on a discovered ML model using[`counterfit`](https://github.com/Azure/counterfit) library

# Usage

## System requirements: 
 - **Ubuntu 18.04** or **20.04** 
 - **Python version 3.7+**

    ### Plugin Dependencies:
     - [`Microsoft Counterfit`](https://github.com/Azure/counterfit):  a reaquired dependency to create and run adversarial machine learning attacks

## Installation with CALDERA*:
 
 1. Navigate to [`caldera-atlas`](https://github.com/mitre-atlas/caldera-atlas) repository and follow steps for installation and setup.

 2. Navigate to the UI: `localhost:8888`

    **`arsenal` is not yet a default CALDERA plugin, therefore there are additional steps to include this plugin into the app.*


![overview](docs/assets/A.png)

