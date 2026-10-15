---
title: "06. System, Package, and Service Modules"
slug: "06-system-and-service-modules"
estimated_time: 9
has_hands_on: false
---

## System, Package, and Service Modules

Managing system packages, OS daemons/services, and user accounts are the most common administrative tasks in DevOps automation.

---

### 1. The `apt` Module (`ansible.builtin.apt`)

Manages packages on Debian and Ubuntu systems.

```yaml
- name: Install Nginx web server
  ansible.builtin.apt:
    name: nginx
    state: present
    update_cache: yes
    cache_valid_time: 3600
  become: yes
```

#### Package States:
- `present`: Ensures the package is installed (if already installed, makes no changes).
- `latest`: Upgrades the package to the newest version available in repositories.
- `absent`: Removes the package.
- `build-dep`: Installs build dependencies for the specified package.

#### Critical Parameters:
- `update_cache: yes`: Runs `apt-get update` before attempting installation.
- `cache_valid_time: 3600`: Only updates the apt cache if it is older than the specified seconds (avoids running slow `apt update` every single run).
- `autoremove: yes`: Cleans up unneeded package dependencies (`apt autoremove`).
- `purge: yes`: When removing (`state: absent`), purges config files as well.

---

### 2. The `service` and `systemd` Modules

Manages system daemons and services on remote hosts.

```yaml
- name: Ensure Nginx is running and enabled on boot
  ansible.builtin.service:
    name: nginx
    state: started
    enabled: yes
  become: yes
```

#### Service States:
- `started`: Ensures the service is currently running.
- `stopped`: Ensures the service is stopped.
- `restarted`: Unconditionally restarts the service (always reports `changed: true`).
- `reloaded`: Sends SIGHUP / reload signal to reread configuration without dropping connections.

#### Boot Enablement:
- `enabled: yes`: Service starts automatically at boot (`systemctl enable`).
- `enabled: no`: Service does not start at boot (`systemctl disable`).

> **systemd vs service:**  
> Use `ansible.builtin.service` for general, cross-platform playbooks.  
> Use `ansible.builtin.systemd` when you need specific systemd capabilities like `daemon_reload: yes` or managing user services.

---

### 3. The `user` Module (`ansible.builtin.user`)

Manages user accounts and group memberships.

```yaml
- name: Create deploy user with specific shell and groups
  ansible.builtin.user:
    name: deployer
    state: present
    shell: /bin/bash
    groups: sudo,docker
    append: yes
    create_home: yes
  become: yes
```

#### Critical Parameters:
- `name`: Username.
- `state`: `present` (create/update) or `absent` (delete).
- `groups`: Comma-separated list of secondary groups.
- **`append: yes`**: **CRITICAL!** If `append: yes` is omitted, the user will be removed from all secondary groups not explicitly listed!
- `shell`: Login shell (e.g. `/bin/bash` or `/sbin/nologin` for system service users).
- `create_home: yes`: Creates the home directory if missing.
- `remove: yes`: When used with `state: absent`, deletes the user's home directory and mail spool.

---

### Privilege Escalation: `become`

System modifications (installing packages, modifying services, creating users) require root privileges.

- In playbooks:
  ```yaml
  - name: Install Apache
    ansible.builtin.apt:
      name: apache2
      state: present
    become: yes
  ```
- In ad-hoc commands:
  ```bash
  ansible all -m apt -a "name=curl state=present" -b
  ```

