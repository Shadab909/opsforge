---
title: "04. SSH Key Setup & Authorization"
slug: "04-ssh-key-setup"
estimated_time: 8
has_hands_on: false
---

## SSH Key Setup and Authorization

Automating SSH key distribution is fundamental to managing secure, passwordless access for both human administrators and automated services.

Ansible provides two complementary capabilities:
1. **Generating SSH key pairs on the target host** (`ansible.builtin.user`).
2. **Deploying authorized public keys** (`ansible.posix.authorized_key`).

---

### 1. Generating an SSH Key Pair for a User

You can instruct the `user` module to generate a private/public key pair in the user's `.ssh` directory upon creation:

```yaml
- name: Create deployer user with auto-generated 4096-bit RSA SSH key
  ansible.builtin.user:
    name: deployer
    generate_ssh_key: yes
    ssh_key_bits: 4096
    ssh_key_type: rsa
    ssh_key_file: .ssh/id_rsa
    ssh_key_comment: "deployer@opsforge-cluster"
  become: yes
```

#### Parameters for Key Generation:
- `generate_ssh_key: yes`: Creates the key pair if it does not already exist (idempotent; will NOT overwrite existing keys).
- `ssh_key_type`: `rsa`, `ed25519`, `ecdsa`, `dsa` (default: `rsa`).
- `ssh_key_bits`: Key length (e.g. `4096` or `2048` for RSA; Ed25519 has a fixed size).
- `ssh_key_file`: Custom path relative to home or absolute path.
- `ssh_key_comment`: Comment added to the end of the public key.

---

### 2. Authorizing Public Keys (`ansible.posix.authorized_key`)

To allow someone to log into the remote server using their SSH public key, use the `authorized_key` module:

```yaml
- name: Add administrator public key to deployer authorized_keys
  ansible.posix.authorized_key:
    user: deployer
    state: present
    key: "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... admin@workstation"
  become: yes
```

#### Authorizing from a Local File:
```yaml
- name: Add local public key to remote user
  ansible.posix.authorized_key:
    user: deployer
    state: present
    key: "{{ lookup('file', '~/.ssh/id_ed25519.pub') }}"
  become: yes
```

#### Authorizing Directly from GitHub / URL:
```yaml
- name: Add GitHub user's public keys
  ansible.posix.authorized_key:
    user: deployer
    state: present
    key: "https://github.com/shadab.keys"
  become: yes
```

#### Exclusive Key Management (`exclusive: yes`):
```yaml
- name: Enforce that ONLY listed keys are allowed (deletes any unknown keys!)
  ansible.posix.authorized_key:
    user: deployer
    key: "{{ lookup('file', 'files/authorized_keys') }}"
    exclusive: yes
  become: yes
```

> **Security Note:** The `authorized_key` module automatically creates the `~/.ssh` directory with strict `0700` permissions and `authorized_keys` with `0600` permissions, satisfying OpenSSH security requirements.

