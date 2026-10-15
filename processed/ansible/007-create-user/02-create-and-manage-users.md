---
title: "02. Creating, Modifying, and Removing Users"
slug: "02-create-and-manage-users"
estimated_time: 9
has_hands_on: false
---

## Creating, Modifying, and Removing Users

The `ansible.builtin.user` module offers rich parameters to control every aspect of an account's lifecycle.

---

### Creating a User with Custom Attributes

```yaml
- name: Create developer user with specific groups and bash shell
  ansible.builtin.user:
    name: john
    comment: "John Doe - Lead Developer"
    uid: 1042
    group: developers
    groups: sudo,docker
    append: yes
    shell: /bin/bash
    home: /home/john
    create_home: yes
    state: present
  become: yes
```

### Critical Parameters Explained

| Parameter | Type | Default | Explanation |
|---|---|---|---|
| `name` | String | *Required* | The username to create, modify, or remove. |
| `comment` | String | None | Real name or GECOS field in `/etc/passwd`. |
| `uid` | Integer | System assigned | Explicit numeric user ID. |
| `group` | String | Username | Primary group of the user. |
| `groups` | List/CSV | None | Comma-separated list or YAML list of secondary/supplementary groups. |
| **`append`** | Boolean | `no` | **CRITICAL!** If `yes`, adds the user to `groups` while keeping existing groups. If `no`, **removes** the user from all secondary groups not listed! |
| `shell` | Path | System default | Login shell (e.g. `/bin/bash` or `/sbin/nologin`). |
| `create_home` | Boolean | `yes` | Creates the home directory if it does not exist. |
| `home` | Path | `/home/<name>` | Custom home directory path. |
| `system` | Boolean | `no` | If `yes`, creates a system account with low UID (< 1000). |
| `state` | String | `present` | `present` to create/update; `absent` to delete. |
| `remove` | Boolean | `no` | When used with `state: absent`, deletes the user's home directory and mail spool (`userdel -r`). |

---

### The `append: yes` Gotcha!

> **Warning: The Most Common Ansible User Module Mistake**  
> If an existing user belongs to `sudo`, `adm`, and `developers`, and you run:
> ```yaml
> groups: docker
> ```
> Without `append: yes`, Ansible will **remove** the user from `sudo`, `adm`, and `developers`!  
> **Always specify `append: yes`** when adding supplementary groups.

---

### Removing Users Cleanly

To delete an account and completely wipe its home directory:

```yaml
- name: Delete former employee user and remove home directory
  ansible.builtin.user:
    name: bad_actor
    state: absent
    remove: yes
  become: yes
```

If `remove: no` (the default for absent), the user account is removed from `/etc/passwd`, but `/home/bad_actor` remains intact on disk.

