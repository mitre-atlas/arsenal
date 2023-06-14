# ARSENAL

## **arsenal** is a Machine Learning (ML) plugin to [`CALDERA`](https://github.com/mitre/caldera), that implements Tactics, Techniques, and Procedures (TTPs) specific to ML operations described in [`MITRE ATLAS`](https://atlas.mitre.org/).

---

## Included ML Libraries

---
### Arsenal implements the following libraries for emulating AI/ML adversarial behavior:

 - [`Counterfit`](https://github.com/Azure/counterfit) - which wraps [`Adversarial Robustness Toolbox (ART)`](https://github.com/Trusted-AI/adversarial-robustness-toolbox), [`TextAttack`](https://github.com/QData/TextAttack), and [`Augly`](https://github.com/facebookresearch/AugLy)

 - [`Vulhub`](https://github.com/vulhub/vulhub) in conjunction with [`ML-Vulhub`](https://github.com/mitre-atlas/ml-vulhub) - deploy vulnerable environments via docker
 - [`torch-serve`](https://pytorch.org/serve/) - serve any type of model to emulate / red-team
 - [`MinIO`](https://github.com/minio/minio) - deploy object stores and S3 buckets to immitate a victim system hosting data and/or models
 - [`Almanac`](https://github.com/mitre-atlas/almanac) - generate adversary layers (sequences of operations) based on MITRE ATLAS TTPs.

---
Implemented Abilities
---

- [`Reconnaissance: Remote Services`](https://atlas.mitre.org/techniques/AML.T0006)

    This ability enables users to first scan a vicitm's system and collect information about IP addresses that are in use

- [`Reconnaissance: List Network Interfaces`](https://atlas.mitre.org/techniques/AML.T0006)

    This ability allows users to list available (physical or virtual) network interfaces

- [`Reconnaissance: Gather Information for Protocol Addresses`](https://atlas.mitre.org/techniques/AML.T0006)

    This ability allows users gather the IP address and netmask (in CIDR notation) for each IP address available on the machine. Only IPs with "scope global" (valid everywhere) are
    considered.

- [`Reconnaissance: Gather Information for TCP Sockets`](https://atlas.mitre.org/techniques/AML.T0006)

    Show TCP connections in listening state, without resolving the IP addresses and the port number.

- [`Collection: Find Tensorflow model checkpoint files`](https://atlas.mitre.org/techniques/AML.T0037)

    Locate Tensorflow model checkpoint files

- [`Collection: Search and Stage Tensorflow model files`](https://atlas.mitre.org/techniques/AML.T0035)

    Searches for Tensorflow directories and checkpoint files, and then stages

- [`Collection: CNN Image Classifier`](https://attack.mitre.org/techniques/T1074/001/)

    Searches for images and applies an image classifier

- [`Command and Control: Install Python`](https://attack.mitre.org/techniques/T1105/)


- [`Command and Control: Install Counterfit`](https://attack.mitre.org/techniques/T1105/)


- [`Command and Control: PIP Install Tensorflow-CPU`](https://attack.mitre.org/techniques/T1105/)


- [`Command and Control: PIP Install Tensorflow-GPU`](https://attack.mitre.org/techniques/T1105/)

- [`Discovery: Determine Python3 version`](https://attack.mitre.org/techniques/T1518/)

- [`Discovery: Discover GPUs present`](https://attack.mitre.org/techniques/T1082/)

- [`Discovery: Discover TorchServe API`](https://atlas.mitre.org/techniques/AML.T0007)

    This ability allows a user to discover IP address that host ML services (PyTorchServe) and the model file(s) they are serving.

- [`ML Model Access: Inference API Access`](https://atlas.mitre.org/techniques/AML.T0040)

    Gain access to TorchServe prediction endpoint

- [`ML Attack Staging: Build and Attack a Custom CFTarget`](https://atlas.mitre.org/techniques/AML.T0043)

    Creates an interface between a target model and the attacks included in a framework. This is done by creating a sub-class of counterfit.core.targets.CFTarget, where the collected target.model_server.prediction_endpoint fact will be used to specify the target_endpoint. Once the respective target is built, the attack is executed against the target.


---
Implemented Autonoumous Adversaries
---
For implemented autonomous adversaries, navigate to our [`page`](https://mitre-atlas.github.io/arsenal/adversary.html) for more details!

---
## Developers

If you are a developer and looking to contribute to `arsenal` or modify it for your needs, please navigate to the [`developers page`](https://mitre-atlas.github.io/arsenal/dev.html).

*Currently, `arsenal` is not a default plugin within `caldera`, and therefore additional setup to integrate with the app is required.*
