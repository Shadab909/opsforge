---
title: "06. Fact Filtering & Practical Automation"
slug: "06-filtering-and-cli-practices"
estimated_time: 7
has_hands_on: true
---

## 06. Fact Filtering & Practical Automation

In production environments containing thousands of facts per host, filtering fact output directly at the command line or saving discovered system profiles is critical for rapid diagnostics.

---

## Command-Line Fact Filtering

The `setup` module accepts a `filter` argument that uses shell-style wildcard matching to return only the specific facts you need:

### 1. Filtering Network Facts
```bash
# Query only default IPv4 attributes across all hosts
ansible all -m setup -a "filter=ansible_default_ipv4*"

# Query specifically the default IP address of all machines
ansible all -m setup -a "filter=ansible_default_ipv4.address"
```

### 2. Targeting Specific Hosts Without Inventory Changes
You can narrow execution to a single machine by replacing the host pattern `all` with the target host name or IP:

```bash
# Query the IP address of linux-server-2 only
ansible linux-server-2 -m setup -a "filter=ansible_default_ipv4.address"
```

### 3. Filtering Operating System Details
```bash
# Inspect all distribution-related facts
ansible all -m setup -a "filter=ansible_distribution*"
```

---

## Archiving Facts to the Controller via Playbook

You can automate fact collection and archive all remote system specifications to JSON files on your Ansible controller node using `delegate_to: localhost`:

```yaml
---
- name: Collect and archive system facts to controller
  hosts: all
  gather_facts: yes

  tasks:
    - name: Show available facts summary
      ansible.builtin.debug:
        var: ansible_facts

    - name: Ensure local backup directory exists
      ansible.builtin.file:
        path: /labs-scripts/facts
        state: directory
        mode: '0755'
      delegate_to: localhost
      run_once: true

    - name: Save host facts to JSON file on controller
      ansible.builtin.copy:
        content: "{{ ansible_facts | to_nice_json }}"
        dest: "/labs-scripts/facts/{{ inventory_hostname }}_facts.json"
        mode: '0644'
      delegate_to: localhost
```

---

## Practical Multi-Tier Automation Playbooks

### Pattern 1: Dynamic Dual-Family Package Management
```yaml
---
- name: Heterogeneous package installation
  hosts: all
  become: yes

  tasks:
    - name: Install Nginx on Debian family (Ubuntu, Debian)
      ansible.builtin.apt:
        name: nginx
        state: present
        update_cache: yes
      when: ansible_os_family == "Debian"

    - name: Install HTTPD on RedHat family (RHEL, CentOS, Rocky)
      ansible.builtin.dnf:
        name: httpd
        state: present
      when: ansible_os_family == "RedHat"
```

### Pattern 2: Memory-Based Service Safeguards
```yaml
---
- name: Restart service if system is low on RAM
  hosts: all
  become: yes

  tasks:
    - name: Restart memory-intensive daemon
      ansible.builtin.service:
        name: my_service
        state: restarted
      when: ansible_memory_mb.real.total < 4096
```

### Pattern 3: Dynamic Flagging and Conditional Tasks
```yaml
---
- name: Staged deployment with custom fact flags
  hosts: all

  tasks:
    - name: Determine if database backup is required
      ansible.builtin.set_fact:
        backup_required: "yes"

    - name: Trigger backup script when required
      ansible.builtin.command: /usr/local/bin/backup_db.sh
      when: backup_required == "yes"
```
