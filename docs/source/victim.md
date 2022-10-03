# Victim: Arsenal

## Arsenal requires a victim system to attack (preferrably) hosting a machine learning algorithm.

However, hosting an algorithm is not required, an adversary may be interested in discovering hardware/compute capabilities of an adversary, exfiltrating data hosted on the system, etc. regardless of a hosted algorithm.

## Forensics

A large area of research coming out of Adversarial ML research is the idea of *forensics*. This could be:

- Discovering the intent of an adversary through attribution of attacks, frequency of API calls, iterative image data, etc.
- Discovering the underlying attacks used by an adversary

Arsenal can also be used in conjuntion with another MITRE plugin to analyze these attacks and report metrics and observations about the adversaries intent. This can be used by both the "victim" or a blue-team to analyze their robustness, and by adversaries or a red-team to analyze their vulnerabilities as an attacker.