---
title: "01. Git Module Basics"
slug: "01-git-module-basics"
estimated_time: 7
has_hands_on: false
---

## Git Module Basics (`ansible.builtin.git`)

The `ansible.builtin.git` module enables Ansible to manage Git repositories on remote target machines. It is one of the most widely used modules for continuous deployment (CD), application delivery, and infrastructure-as-code synchronization.

### Where Does Git Execute?

> **Fundamental Principle:**  
> The Git module executes `git` **on the remote managed node**, NOT on the Ansible control machine.  
> Therefore, the `git` binary **must be installed on target hosts** before calling this module.

```text
[Ansible Control Node] ──SSH──► [Remote Target Node]
                                       │
                                1. Runs 'git' CLI
                                2. Connects to GitHub/GitLab/Bitbucket
                                3. Pulls repo into destination path
```

### Basic Syntax

```yaml
- name: Deploy application repository
  ansible.builtin.git:
    repo: https://github.com/example/webapp.git
    dest: /var/www/webapp
    version: main
```

### Key Parameters Overview

| Parameter | Type | Default | Description |
|---|---|---|---|
| `repo` | String | *Required* | The URI of the Git repository (HTTPS, SSH, or local file path). |
| `dest` | Path | *Required* | The absolute destination path on the target host where the repo should be cloned. |
| `version` | String | `HEAD` | What version/branch/tag/commit to checkout. |
| `update` | Boolean | `true` | Whether to pull in new changes if the repository already exists. |
| `force` | Boolean | `false` | If `true`, discards any uncommitted local modifications on the remote host. |
| `key_file` | Path | None | Path to private SSH key for private repository authentication. |
| `accept_hostkey` | Boolean | `false` | Automatically accept unknown host keys (adds to `known_hosts`). |
| `depth` | Integer | None | Creates a shallow clone with a history truncated to the specified number of commits. |
| `recursive` | Boolean | `true` | Automatically initializes and clones git submodules. |

### Module Return Values

When the Git task executes, it returns:
- `changed`: `true` if files were cloned or commit updated; `false` if already at the requested version.
- `before`: The commit SHA prior to task execution (or `null` if fresh clone).
- `after`: The commit SHA after task execution.

