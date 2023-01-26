# CALDERA plugin: **Arsenal**

### This plugin will help store and create adversarial TTPs defined in [`ATLAS`](https://atlas.mitre.org/) to interfeace with [`CALDERA`](https://github.com/mitre/caldera). It can be used in conjuction with the plugin [`Almanac`](https://github.com/mitre-atlas/almanac).

We recommend that you navigate to our [`DOCUMENTATION`](https://advml.pages.mitre.org/arsenal/intro.html#arsenal) for further details of the plugin and how to use it for adversary emulation.

# Developers

## System requirements: **Ubuntu 18.04** or **20.04** and **Python versions 3.7+**

## Installation with CALDERA app
 *`arsenal` is not yet a default CALDERA plugin, therefore there are additional steps to include this plugin into the app.*

 1. Navigate to [`caldera-atlas`](https://github.com/mitre-atlas/caldera-atlas) repository and follow steps for installation and setup.

 2. Navigate to the UI: `localhost:8888`

*JAN 2023 included abilities:*

- discover remote services
- discover local services
- discover available network services
- discover ML specific services
- exfiltrate ML model
- evade ML model using [`counterfit`](https://github.com/Azure/counterfit) library

![overview](docs/assets/A.png)

