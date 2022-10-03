# Adversary: Arsenal

## Arsenal takes the stand-point of an adversary attacking a victim system that hosts services. 

The adversary and victim relationship used in Arsenal with CALDERA can be used in many different ways:
- Red Teaming effort
- Blue Teaming effort
- Forensic analysis of ML algorithms and subsequent software underlying the algorithm

This plugin focuses on using **both** traditional cybersecurity TTPs with modern ML TTPs to attack a hosted victim system. It is our collected understanding that ML algorithms are rarely stand-alone, and adversaries in-the-wild will use traditional cybersecurity attacks alongside ML attacks in order to acheive their goals. 

Machine Learning algorithms are embedded into the underlying software stack, and therefore intensive research into only the various ML attacks is not representative of the real-world adversaries companies face. There may be various other areas of a companies software that opens up vulnerabilities to the ML algorithm that adversaries can exploit.

**Arsenal** has been developed for the Cybersecurity Engineer/Researcher, but will also benefit ML/MLOps Engineers in better understanding the entire end-to-end software stack that ML is deployed into.

This plugin is not designed for creating new adversarial attacks/defenses, but as a way to red-team or blue-team your current operational models against a myriad of cybersecurity and ML attacks described in MITRE ATT&CK and MITRE ATLAS.