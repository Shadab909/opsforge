---
title: "05. Custom Facts (Static & Dynamic)"
slug: "05-custom-facts"
estimated_time: 6
has_hands_on: false
---

## 05. Defining Custom Facts

While Ansible automatically discovers standard hardware and OS facts, you often need custom metadata specific to your applications, tiers, or datacenter locations.

Ansible provides two powerful mechanisms for custom facts:
1. **Local Custom Facts (`/etc/ansible/facts.d/`)**: Static or script-generated facts residing permanently on target machines.
2. **In-Play Dynamic Facts (`set_fact`)**: Variables set dynamically during playbook execution that persist across tasks.

---

## 1. Local Custom Facts (`facts.d`)

Managed target hosts can define their own permanent facts by placing files ending in `.fact` into the `/etc/ansible/facts.d/` directory.

### Step 1: Create the Fact File on the Target Host

Create the directory and a `.fact` file (e.g., `/etc/ansible/facts.d/custom.fact`):

#### INI Format:
```ini
# /etc/ansible/facts.d/custom.fact
[environment]
tier=production
cluster_id=us-east-cluster-01

[application]
app_version=2.4.1
service_owner=devops_team
```

#### JSON Format:
```json
{
  "environment": {
    "tier": "production",
    "cluster_id": "us-east-cluster-01"
  },
  "application": {
    "app_version": "2.4.1",
    "service_owner": "devops_team"
  }
}
```

> [!TIP]
> **Executable Fact Scripts**: If a `.fact` file has executable permissions (`chmod +x`), Ansible executes it at fact-gathering time and parses whatever JSON it writes to standard output!

---

### Step 2: Accessing Local Facts in Playbooks

Local facts are placed under the special `ansible_local` namespace, indexed by the file's base name:

```yaml
---
- name: Read local custom facts
  hosts: all

  tasks:
    - name: Display application version from custom facts
      ansible.builtin.debug:
        msg: "Target app version is {{ ansible_local.custom.application.app_version }}"

    - name: Ensure production-only hardening tasks run
      ansible.builtin.debug:
        msg: "Applying strict firewall rules to {{ ansible_local.custom.environment.cluster_id }}"
      when: ansible_local.custom.environment.tier == "production"
```

---

## 2. In-Play Dynamic Facts (`set_fact`)

The `ansible.builtin.set_fact` module allows you to compute, transform, or declare facts dynamically during playbook execution.

```yaml
---
- name: Dynamic custom facts example
  hosts: all

  tasks:
    - name: Compute and assign dynamic facts
      ansible.builtin.set_fact:
        deployment_stage: staging
        backup_required: yes
        api_endpoint: "https://{{ ansible_default_ipv4.address }}:8443/v1"

    - name: Use the dynamic fact in subsequent tasks
      ansible.builtin.debug:
        msg: "Endpoint configured at {{ api_endpoint }}"
      when: backup_required == "yes"
```

### Characteristics of `set_fact`
- **Host Scoped**: Assigned per target host, persisting across all remaining tasks for that host in the playbook run.
- **High Precedence**: Takes priority #7 in Ansible's variable precedence hierarchy, overriding role defaults, inventory variables, and gathered facts.
