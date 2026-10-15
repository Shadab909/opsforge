---
title: "03. Discovering and Documenting Modules"
slug: "03-discovering-and-documenting-modules"
estimated_time: 8
has_hands_on: false
---

## Discovering & Documenting Modules

Ansible ships with thousands of modules covering cloud providers (AWS, Azure, GCP), operating systems, networking devices, containers, databases, and monitoring systems.

### Fully Qualified Collection Names (FQCN)

Starting with **Ansible 2.10**, Ansible reorganized its monolithic codebase into **Collections**.
A module is addressed by its **FQCN** in the format:

```text
<namespace>.<collection_name>.<module_name>
```

Examples:
- `ansible.builtin.copy` (Core built-in module)
- `community.general.slack` (Community collection)
- `amazon.aws.ec2_instance` (AWS collection)

While short names like `copy` or `ping` still work for built-in modules due to backward compatibility, using the **FQCN** is the official best practice in modern Ansible.

---

### The `ansible-doc` Command Line Tool

The `ansible-doc` command is your built-in offline encyclopedia for Ansible modules, plugins, and collections.

#### 1. Listing All Available Modules
To list all modules currently installed on your control node:

```bash
ansible-doc -l
```

To list modules within a specific collection:
```bash
ansible-doc -l ansible.builtin
```

#### 2. Viewing Full Documentation for a Module
To view parameters, choices, default values, and requirements for a module:

```bash
ansible-doc copy
# Or using FQCN:
ansible-doc ansible.builtin.copy
```

Output includes:
- **SYNOPSIS**: Explanation of what the module does.
- **PARAMETERS**: Each parameter, its type, required status, and default value.
- **NOTES**: Gotchas and platform compatibility details.
- **EXAMPLES**: Copy-pasteable playbook snippets illustrating real-world use cases.
- **RETURN VALUES**: What data keys the module returns.

#### 3. Generating Playbook Snippets (`-s`)
The `-s` (snippet) flag prints a minimal, ready-to-use YAML skeleton with all parameters:

```bash
ansible-doc -s ping
```

Output:
```yaml
- name: Try to connect to host, verify a usable python and return `pong' on success
  ansible.builtin.ping:
    data:                  # Value provided with the `data' parameter.
```

---

### Finding the Right Module for Your Task

Different Linux distributions and platforms use specialized package and service managers:

| Domain | Debian/Ubuntu | RHEL/CentOS/Rocky | Generic/Cross-Platform |
|---|---|---|---|
| Package Manager | `ansible.builtin.apt` | `ansible.builtin.dnf` / `yum` | `ansible.builtin.package` |
| Service Manager | `ansible.builtin.systemd` | `ansible.builtin.systemd` | `ansible.builtin.service` |
| User Accounts | `ansible.builtin.user` | `ansible.builtin.user` | `ansible.builtin.user` |
| Firewalls | `community.general.ufw` | `ansible.posix.firewalld` | `ansible.builtin.iptables` |

> **Pro Tip:** When writing playbooks meant to run across different Linux distributions, using generic modules like `ansible.builtin.package` or `ansible.builtin.service` allows Ansible to automatically delegate to the correct underlying system tool.

