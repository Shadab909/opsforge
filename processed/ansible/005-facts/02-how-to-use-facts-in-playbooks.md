---
title: "02. Using Facts in Playbook Logic"
slug: "02-how-to-use-facts-in-playbooks"
estimated_time: 6
has_hands_on: false
---

## 02. Referencing Facts in Playbooks

Discovered facts empower you to write dynamic, multi-platform playbooks that adapt automatically to heterogeneous server environments.

### Variable Naming & Scoping

Ansible supports two complementary syntaxes for accessing facts:

1. **Modern Scoped Dictionary (Recommended)**:
   ```yaml
   {{ ansible_facts['distribution'] }}
   {{ ansible_facts['default_ipv4']['address'] }}
   ```
2. **Legacy Top-Level Fact Variables**:
   ```yaml
   {{ ansible_distribution }}
   {{ ansible_default_ipv4.address }}
   ```

Both formats remain supported across modern Ansible releases, with top-level variables prepending the `ansible_` prefix.

---

## Conditional Execution with `when:`

The most common use case for facts is conditional execution. When using facts in a `when:` directive, **do not** wrap the variable in double curly braces `{{ }}`:

### Example 1: Installing Packages Based on Operating System

```yaml
---
- name: Cross-platform web server installation
  hosts: all
  become: yes

  tasks:
    - name: Install Nginx on Debian/Ubuntu using APT
      ansible.builtin.apt:
        name: nginx
        state: present
        update_cache: yes
      when: ansible_distribution == "Ubuntu"

    - name: Install Nginx on RedHat/CentOS using DNF
      ansible.builtin.dnf:
        name: nginx
        state: present
      when: ansible_distribution == "CentOS"
```

Using `ansible_os_family` is often cleaner when targeting families of operating systems:
```yaml
    - name: Install Apache on Debian family (Ubuntu, Debian, Mint)
      ansible.builtin.apt:
        name: apache2
        state: present
      when: ansible_os_family == "Debian"

    - name: Install Apache on RedHat family (RHEL, CentOS, Rocky, Fedora)
      ansible.builtin.dnf:
        name: httpd
        state: present
      when: ansible_os_family == "RedHat"
```

---

## Example 2: Resource-Based Execution (Hardware Limits)

Facts provide exact numerical metrics on system resources, allowing safe, capacity-aware workflows:

```yaml
- name: Restart service if system memory is low
  ansible.builtin.service:
    name: my_service
    state: restarted
  when: ansible_memory_mb.real.total < 4000
```

### Accessing Nested Fact Dictionaries

Many facts are structured as nested dictionaries. You can navigate them using dot notation or bracket notation:

```yaml
# Dot notation:
when: ansible_memory_mb.real.total < 4096

# Bracket notation:
when: ansible_memory_mb['real']['total'] < 4096

# Accessing default IP address:
debug:
  msg: "Primary IPv4 address: {{ ansible_default_ipv4.address }}"
```
