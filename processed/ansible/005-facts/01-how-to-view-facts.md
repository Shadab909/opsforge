---
title: "01. Viewing Facts & Architecture"
slug: "01-how-to-view-facts"
estimated_time: 5
has_hands_on: false
---

## 01. What are Ansible Facts?

**Ansible facts** are system data dynamically discovered from remote target systems at runtime. They constitute one of the fundamental building blocks of Ansible automation.

- **Dynamic Discovery**: Facts capture real-time information corresponding to remote systems, including operating system distributions, kernel versions, network interfaces, IP addresses, memory capacity, CPU architecture, and storage mounts.
- **Agentless Collection**: The Ansible controller executes the `setup` module on managed nodes over SSH (or WinRM) to extract system properties and return them formatted as JSON to the controller node.
- **Runtime Variables**: Once collected, facts are exposed as standard variables accessible throughout plays, tasks, handlers, and Jinja2 configuration templates.

---

## Viewing Facts via Ad-Hoc CLI

You can inspect the complete dictionary of facts gathered from any target machine by executing the `setup` module via the command line:

```bash
# Query all discovered facts across all inventory hosts
ansible all -m setup

# Query facts specifically from a single host (e.g. linux-server-1)
ansible linux-server-1 -m setup
```

### Fact JSON Output Structure

The output returned by the `setup` module is encapsulated within an `ansible_facts` JSON dictionary:

```json
{
  "ansible_facts": {
    "ansible_distribution": "Ubuntu",
    "ansible_distribution_version": "22.04",
    "ansible_distribution_release": "jammy",
    "ansible_architecture": "x86_64",
    "ansible_hostname": "web-node-01",
    "ansible_os_family": "Debian",
    "ansible_memory_mb": {
      "real": {
        "total": 7989,
        "used": 2034,
        "free": 5955
      },
      "swap": {
        "total": 2048,
        "used": 0,
        "free": 2048
      }
    },
    "ansible_default_ipv4": {
      "address": "192.168.1.10",
      "netmask": "255.255.255.0",
      "gateway": "192.168.1.1",
      "interface": "eth0",
      "macaddress": "00:16:3e:2f:1a:8b"
    }
  }
}
```

---

## Exporting Facts with `--tree`

When auditing or managing large fleets of servers, you can export facts for all hosts directly to local JSON files on your controller using the `--tree` argument:

```bash
# Gathers facts from all hosts and saves each host's JSON under ./facts/
ansible all -m setup --tree ./facts
```

This generates a structured directory of files named by hostname:
```text
facts/
├── web-node-01
├── web-node-02
└── db-node-01
```

Each file contains the complete, unadulterated JSON fact payload for that specific host, ideal for offline inventory auditing, compliance verification, and reporting.

---

## Viewing Facts Inside a Playbook

By default, every play begins with an implicit `TASK [Gathering Facts]`. You can print all gathered facts using the `ansible.builtin.debug` module:

```yaml
---
- name: Inspect discovered system facts
  hosts: all
  gather_facts: yes

  tasks:
    - name: Display entire facts dictionary
      ansible.builtin.debug:
        var: ansible_facts

    - name: Display specific operating system fact
      ansible.builtin.debug:
        msg: "Target OS is {{ ansible_facts['distribution'] }} {{ ansible_facts['distribution_version'] }}"
```
