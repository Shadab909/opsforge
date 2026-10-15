---
title: "01. Ansible's User Module Overview"
slug: "01-ansible-user-module"
estimated_time: 7
has_hands_on: false
---

## Ansible's User Module (`ansible.builtin.user`)

The `ansible.builtin.user` module is the standard declarative interface for managing user accounts on target operating systems.

Whether you are targeting Ubuntu, Debian, RHEL, CentOS, Rocky Linux, macOS, or FreeBSD, the `user` module abstracts away OS-specific commands (`useradd`, `usermod`, `userdel`, `pw`, `dscl`) into a unified, idempotent syntax.

### Why Use the User Module?

1. **Idempotence**: If the user already exists with the correct UID, shell, and groups, Ansible does nothing (`changed: false`).
2. **Cross-Platform**: Automatically calls the correct underlying operating system binary.
3. **Comprehensive Lifecycle Management**: Creates accounts, generates SSH keys, modifies group memberships, expires accounts, and cleans up home directories.

### Privilege Escalation Requirement

> **Rule:** Managing user accounts requires root/superuser privileges. Always include `become: yes` in user tasks.

```yaml
- name: Ensure deployer user exists
  ansible.builtin.user:
    name: deployer
    state: present
  become: yes
```

### Module Return Values

On execution, the module returns a dictionary containing the user's system attributes:

```json
{
    "changed": true,
    "name": "deployer",
    "uid": 1001,
    "gid": 1001,
    "home": "/home/deployer",
    "shell": "/bin/bash",
    "state": "present"
}
```

