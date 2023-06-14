# Autonomous Adversary Profiles

This plugin focuses on using **both** traditional cybersecurity TTPs with AI/ML specific TTPs to Red-Team a system that is AI-enabled. It is our collected understanding that AI/ML algorithms and artifacts are rarely stand-alone, and adversaries in-the-wild will use traditional cybersecurity tactics and techniques alongside AI/ML tactics and techniques in order to achieve their goals. For more examples of these attacks on real-workd systems, please navigate to the [`MITRE ATLAS Case Studies`](https://atlas.mitre.org/studies) page.

All `arsenal` adversaries use a combination of TTPs from MITRE ATT&CK (plugin: [`stockpile`](https://github.com/mitre/stockpile)) and MITRE ATLAS (plugin: arsenal).

Below is a description and example of the current autonomous adversary profiles currently implemented:

# Tensormancer
An adversary profile to demo neural network abilities using the Tensorflow library.

*Abilities*:

1. [`Create a staging directory`](https://github.com/mitre/stockpile/blob/master/data/abilities/collection/6469befa-748a-4b9c-a96d-f191fde47d89.yml) for exfiltration.
2. Discover GPUs present
3. Find Tensorflow model checkpoint files with the extension: `.ckpt` 
4. Search and Stage Tensorflow model files
    - Searches for Tensorflow directories and checkpoint files, and then stages for exfiltration.
5. Install Python
    - Download and install Python and it's dependencies (`Python 3.7+`) where the agent is deployed.
6. Determine Python3 version
    - Determine Python3 is installed and version (`Python 3.7+`) where the agent is deployed.
7. PIP Install Tensorflow-GPU
    - Use pip to install Tensorflow-GPU
8. PIP Install Tensorflow-CPU
    - Use pip to install Tensorflow-CPU
9. CNN Image Classifier
    - Searches for images and applies an image classifier
10. [`Compress staged directory`](https://github.com/mitre/stockpile/blob/master/data/abilities/exfiltration/300157e5-f4ad-4569-b533-9d1fa0e74d74.yml)
    - Compress a directory on the file system
11. [`Exfil staged directory`](https://github.com/mitre/stockpile/blob/master/data/abilities/exfiltration/ea713bc4-63f0-491c-9a6f-0b01d560b87e.yml)
    - exfiltrate over the C2 channel


# ML Model Thief
An adversary profile to find any hosted ML algorithms with file extensions matching: `.mar`, `.pth`, `.pt`, `.onnx`, `.pkl`, `.tflite`, `.pb`, `.hdf5` and exfiltrate the algorithm back to the C2 server. 

1. [`Find Files`](https://github.com/mitre/stockpile/blob/master/data/abilities/collection/90c2efaa-8205-480d-8bb6-61d90dbaf81b.yml)
2. [`Create staging directory`](https://github.com/mitre/stockpile/blob/master/data/abilities/collection/6469befa-748a-4b9c-a96d-f191fde47d89.yml)
3. [`Stage sensitive files`](https://github.com/mitre/stockpile/blob/master/data/abilities/collection/4e97e699-93d7-4040-b5a3-2e906a58199e.yml)
4. [`Compress staged directory`](https://github.com/mitre/stockpile/blob/master/data/abilities/exfiltration/300157e5-f4ad-4569-b533-9d1fa0e74d74.yml)
5. [`Exfil staged directory`](https://github.com/mitre/stockpile/blob/master/data/abilities/exfiltration/ea713bc4-63f0-491c-9a6f-0b01d560b87e.yml)
    - exfiltrate over the C2 channel

# ML Model Evader
An adversary profile to evade correction classification or detection of a machine learning algorithm using the Microsoft Counterfit library. It is recommended to use the [`ML-Vulhub Example-00`](https://github.com/mitre-atlas/ml-vulhub/tree/main/envs/example-00-ml-dev) or the [`ML-Vulhub Example-01`](https://github.com/mitre-atlas/ml-vulhub/tree/main/envs/example-01-ml-dev) example environments in conjuction with this adversary profile. The set-up of this example vulnerable environment is detailed in [`caldera-atlas`](https://github.com/mitre-atlas/caldera-atlas).

*Abilities*:

1. Find or Install Microsoft Counterfit package
    - This package is installed as a python-venv within the C2 server at installation via [`caldera-atlas`](https://github.com/mitre-atlas/caldera-atlas), this ability checks for the virtual environment and packages installed, and if not found will install the necessary dependencies. This is esspecially useful for installation on a victim system for processing externally to the C2 server.
2. Gather Information for Protocol Addresses
    - Gathers the IP address and netmask (in CIDR notation) for each IP address
    available on system where the agent is deployed. Only IPs with "scope global" (valid everywhere) are considered.
3. Gather Information for TCP sockets
    - Show TCP connections (-t) in listening (-l) state, without resolving the IP addresses and the port number (-n).
4. Gather Information for Remote Services
    - Gathers information on the status ("Up", "Down", etc.) of other hosts on the network where the agent is deployed by executing a "ping scan". Then, a "port scan" is executed on "Up" hosts to gather information for remote services.
5. Discover Torchserve API
    - This ability specifically looks for any Torshserve API endpoints that may be hosting models. If found, it will create Facts with the API endpoint and algorithm for future API access. Torchserve has two API endpoints, an Inference API and a Management API, both are needed information for gaining information about hosted algorithms and sending data for inference. A single API may host multiple algorithms.
6. ML Model Inference API Access
    - This ability maps the algorithms hosted via the Torchserve Management API to the prediction endpoint for the Torchserve Inference API.
7. Build and Attack a Custom CFTarget (Counterfit Target)
    - This ability creates Counterfit Targets from any and all found algorithms and API endpoints. From these targets, users can choose which endpoints and data (images) they would like to use to generate Adversarial Attacks using the Counterfit library. Current imagery attacks that are autonomously generated are the black-box optimizers: hop-skip-jump, boundary, and copycat-cnn.
