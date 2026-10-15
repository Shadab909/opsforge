---
title: "04. Disabling & Optimizing Fact Gathering"
slug: "04-disabling-fact-gathering"
estimated_time: 5
has_hands_on: false
---

## 04. Disabling Fact Gathering

By default, Ansible automatically runs the `setup` module at the beginning of each play (`TASK [Gathering Facts]`).

While helpful, fact gathering introduces execution overhead: Ansible connects to each target, inspects disks, queries hardware, parses `/proc`, and transfers the JSON payload back over SSH. In large fleets (hundreds or thousands of machines), this discovery phase can consume significant execution time.

### How to Disable Facts in a Play

To turn off fact gathering, set `gather_facts: no` (or `gather_facts: false`) at the play level:

```yaml
---
- name: Fast deployment without facts
  hosts: all
  gather_facts: no

  tasks:
    - name: Print deployment notice
      ansible.builtin.debug:
        msg: "Fact gathering is disabled! Playbook executes instantly."

    - name: Restart application daemon
      ansible.builtin.service:
        name: myapp
        state: restarted
```

---

## When Should You Disable Facts?

| Scenario | Recommendation | Rationale |
| :--- | :--- | :--- |
| **Large Fleet Execution** (100+ servers) | **Disable** | Cuts play startup delay by 70–90% across large batches. |
| **Simple Maintenance Tasks** (service restart, log rotation) | **Disable** | Tasks don't rely on OS/network/hardware facts. |
| **Air-gapped or Slow SSH Links** | **Disable** | Avoids transferring large JSON fact payloads over low-bandwidth connections. |
| **Cross-Platform Conditionals** (`apt` vs `dnf`) | **Keep Enabled** | Conditionals like `when: ansible_os_family == "Debian"` require facts. |

---

## On-Demand & Granular Fact Gathering

If most tasks in your play do not need facts, but one specific section does, you can disable fact gathering at the play level and invoke the `setup` module **on-demand**:

```yaml
---
- name: Selective fact gathering workflow
  hosts: all
  gather_facts: no

  tasks:
    - name: Perform quick preliminary task
      ansible.builtin.command: /usr/local/bin/pre_check.sh

    - name: Gather facts on-demand later in the play
      ansible.builtin.setup:

    - name: Access facts gathered on demand
      ansible.builtin.debug:
        msg: "Hostname is {{ ansible_hostname }}"
```

### Filtering Fact Subsets (`gather_subset`)

You can instruct the `setup` module to gather only a lightweight subset of facts (e.g. only network or only virtual), bypassing heavy hardware and mount queries:

```yaml
    - name: Gather only network facts
      ansible.builtin.setup:
        gather_subset:
          - '!all'
          - '!min'
          - 'network'
```

Available subsets include: `all`, `min`, `hardware`, `network`, `virtual`, `ohai`, and `facter`. Prepending `!` negates that subset.
