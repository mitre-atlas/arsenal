# ARSENAL

## **arsenal** is a Machine Learning (ML) plugin to [`CALDERA`](https://github.com/mitre/caldera), that implements Tactics, Techniques, and Procedures (TTPs) specific to ML operations described in [`MITRE ATLAS`](https://atlas.mitre.org/).

---

## Included ML Libraries

---
### Arsenal implements the following libraries for emulating ML adversarial behavior:

 - [`Counterfit`](https://github.com/Azure/counterfit) - which wraps [`Adversarial Robustness Toolbox (ART)`](https://github.com/Trusted-AI/adversarial-robustness-toolbox), [`TextAttack`](https://github.com/QData/TextAttack), and [`Augly`](https://github.com/facebookresearch/AugLy)

 - [`Vulhub`](https://github.com/vulhub/vulhub) in conjunction with [`ML-Vulhub`](https://github.com/mitre-atlas/ml-vulhub) - deploy vulnerable environments via docker
 - [`torch-serve`](https://pytorch.org/serve/) - serve any type of model to emulate / red-team
 - [`MinIO`](https://github.com/minio/minio) - deploy object stores and S3 buckets to immitate a victim system hosting data and/or models
 - [`Almanac`](https://github.com/mitre-atlas/almanac) - generate adversary layers (sequences of operations) based on MITRE ATLAS TTPs.

---
<!-- ## Emulation Diagram -->
Implemented Abilities
---

- **Reconnaissance: Remote Services**

    This ability enables users to first scan a vicitm's system and collect information about IP addresses that are in use

- **Reconnaissance: List Network Interfaces**

    This ability allows users to list available (physical or virtual) network interfaces

- **Discovery: Discover TorchServe API**

    This ability allows a user to discover IP address that host ML services (PyTorchServe) and the model file they are serving.

- **Evasion: Evade ML Model**

    This ability allows users to evade a ML model from correctly classifying an image by using the `counterfit` library to implement a broad range of ML image attacks.

---
Implemented Adversaries
---

- **Evasion**

    This adversary profile combines multiple abilities together to scan a victim system, find running ML services, and perform black-box evasion attacks.

<!-- The following diagram illustrates the basic usage of the Arsenal plugin within CALDERA: -->

<!-- ![arsenal](../assets/arsenal_diagram.png) -->

---

## Developers

---

If you are a developer and looking to contribute to `arsenal` or modify it for your needs, please navigate to the [`developers page`](https://advml.pages.mitre.org/arsenal/dev.html).

*Currently, `arsenal` is not a default plugin within `caldera`, and therefore additional setup to integrate with the app is required.*
