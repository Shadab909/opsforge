---
title: "02. Cloning Repositories"
slug: "02-cloning-repositories"
estimated_time: 7
has_hands_on: false
---

## Cloning Repositories with Ansible

Cloning a Git repository onto target machines is the first step in automated deployments.

### Basic Clone Task

```yaml
- name: Clone web application repository
  ansible.builtin.git:
    repo: 'https://github.com/octocat/Hello-World.git'
    dest: /opt/hello-world
```

### Destination Directory Scenarios

When Ansible processes the `dest` path, several scenarios can occur:

1. **`dest` does not exist**: Ansible creates `/opt/hello-world` and performs `git clone`. (`changed: true`)
2. **`dest` exists and is already a Git clone of `repo`**: Ansible verifies the commit. If it matches, it skips cloning. (`changed: false`)
3. **`dest` exists but is an empty directory**: Ansible successfully clones the repo into it. (`changed: true`)
4. **`dest` exists, is NOT a Git repo, and is NOT empty**: **Error!** Git will refuse to clone into a non-empty directory that lacks a `.git` folder.

```text
Check dest: /opt/hello-world
     │
     ├─ Doesn't exist ──────────► Clone repo [CHANGED]
     ├─ Exists (.git present) ──► Check commits [OK / CHANGED]
     ├─ Exists (empty) ─────────► Clone repo [CHANGED]
     └─ Exists (non-git files) ─► Fatal Error! [FAILED]
```

---

### Controlling Cloning Behavior

#### 1. Cloning without Updating Later (`update: false`)
If you only want to clone the repository once during initial setup and never pull subsequent changes automatically:

```yaml
- name: Clone base configuration repository once
  ansible.builtin.git:
    repo: 'https://github.com/example/config.git'
    dest: /etc/app/config
    update: false
```

#### 2. Specifying Clone Permissions & Ownership
After cloning, you often need to ensure web server permissions (e.g. `www-data`):

```yaml
- name: Clone and set permissions
  ansible.builtin.git:
    repo: 'https://github.com/example/api.git'
    dest: /var/www/api
  become: yes

- name: Enforce ownership on cloned files
  ansible.builtin.file:
    path: /var/www/api
    owner: www-data
    group: www-data
    recurse: yes
  become: yes
```

#### 3. Bare Repositories (`bare: true`)
To create a bare repository (containing only Git metadata, without a working tree) for a central Git server:

```yaml
- name: Create bare central repository
  ansible.builtin.git:
    repo: 'https://github.com/example/repo.git'
    dest: /git/repo.git
    bare: yes
```

