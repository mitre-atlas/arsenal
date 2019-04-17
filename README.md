# CALDERA plugin: Open

This plugin contains open-source abilities and adversaries. The included filestore contains any
files used by the abilities. 

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
  command: whoami
```

### Adding new adversaries

New adversaries can be added to the adversaries.yml file.


