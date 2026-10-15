---
title: "05. Authentication and SSH"
slug: "05-authentication-and-ssh"
estimated_time: 9
has_hands_on: false
---

## Authentication and SSH for Private Repositories

When cloning private repositories from GitHub, GitLab, or Bitbucket, target machines must authenticate securely.

### Authentication Methods

1. **SSH Deploy Keys (Recommended)**: A dedicated SSH key pair with read-only access to the specific repository.
2. **Personal Access Tokens (PAT) via HTTPS**: HTTPS URL containing an access token.
3. **SSH Agent Forwarding**: Forwarding your local control node's SSH credentials over the connection.

---

### Method 1: Using SSH Keys with `key_file`

The cleanest approach is providing a dedicated deploy private key on the remote machine:

```yaml
- name: Clone private repository using SSH key
  ansible.builtin.git:
    repo: 'git@github.com:myorg/private-repo.git'
    dest: /var/www/private-app
    key_file: /home/deployer/.ssh/id_ed25519_deploy
    accept_hostkey: yes
```

#### Key Parameters:
- `key_file`: Path to the private SSH key file on the remote host.
- `accept_hostkey: yes`: **Crucial!** If connecting to `github.com` for the first time, SSH prompts with:
  ```text
  The authenticity of host 'github.com' can't be established. Are you sure you want to continue connecting (yes/no)?
  ```
  Setting `accept_hostkey: yes` automatically adds the remote host key to `~/.ssh/known_hosts`, preventing tasks from hanging indefinitely waiting for interactive terminal input!

---

### Method 2: Custom SSH Options (`ssh_opts`)

You can pass custom SSH flags using `ssh_opts`:

```yaml
- name: Clone with custom SSH options
  ansible.builtin.git:
    repo: 'git@gitlab.internal.corp:devops/infra.git'
    dest: /opt/infra
    ssh_opts: "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
    key_file: /etc/ssl/deploy_key
```

---

### Method 3: HTTPS with Tokens & Ansible Vault

For HTTPS clones requiring authentication, you can embed tokens into the URL:

```yaml
# In production, store the token in an encrypted vault variable!
- name: Clone private repository via HTTPS token
  ansible.builtin.git:
    repo: "https://{{ github_token }}@github.com/myorg/private-app.git"
    dest: /var/www/app
```

> **Security Warning:** When using HTTPS credentials in URLs, Git stores the full URL (including the token) in `.git/config` on the remote host. Protect the `.git` folder permissions or prefer SSH deploy keys!

