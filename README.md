# CALDERA plugin: Stockpile

This plugin contains:

* A collection of abilities
* Pre-built adversary profiles
* Payloads associated to abilities
* A basic planner 

## Abilities

You can quickly add your own abilities and adversaries to the stockpile, both of which are reloaded every time
the core server reboots. Stockpile abilities are located in the abilities/ directory.

To add new ones, add a .yml file in the abilities directory, named after a unique ID (UUID-4 is our standard). 
This file should include an ID, name, description, ATT&CK tactic and command.

Below is an example ability. Read this carefully, it will be referenced later on.
```
- id: a0676fe1-cd52-482e-8dde-349b73f9aa69
  name: Preferred WIFI
  description: See the most used WIFI networks of a machine
  tactic: discovery
  technique:
    attack_id: T1016
    name: System Network Configuration Discovery
  executors:
    darwin:
      command: |
        #{files}/wifi.sh pref
      payload: wifi.sh
    linux:
      command: |
        #{files}/wifi.sh pref
      payload: wifi.sh
    windows:
      command: |
        #{files}\wifi.ps1 -Pref
      payload: wifi.ps1
```

### Ability variables

As you write abilities, note that there are 3 global variables available, which can be used
inside an ability command:

> A variable is referenced with the syntax #{variable}.

* server: The location of CALDERA. Because each agent may have a different reference point
for where CALDERA is (IP, FQDN, etc), if an ability wants to reference CALDERA it should use #{server}. 
* group: The group used in the active operation.
* files: The location where payload files will be dropped; typically this is the TMP directory. 

In the ability example above, note the usage of the #{server}  and #{files} variables.

The group variable is a bit more advanced. This is useful primarily for lateral movement abilities where
the agent may move itself to a new host. 

### Download files from CALDERA to an agent

In the ability example, note the payload field. When this ability runs, it will
download this file from the CALDERA /file/download directory, putting it in the client's
files directory. The payload file itself must be located in the payloads directory as 
specified in the local.yml.

### Cleanup

Abilities can optionally include a cleanup block, which will execute automatically at the end of an operation. The
cleanup should be used in instances you want to reverse a mutable action, such as stopping a started process. 
Cleanup actions will occur in reverse order of the abilities that ran.

## Adversaries

New adversaries can be added to the adversaries.yml file.

## Planners

A basic planner, called sequential, runs all abilities on an adversary against all hosts in a group
