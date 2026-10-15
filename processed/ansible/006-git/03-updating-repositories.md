---
title: "03. Updating Repositories"
slug: "03-updating-repositories"
estimated_time: 7
has_hands_on: false
---

## Updating Repositories and Handling Changes

By default, the `ansible.builtin.git` module continuously keeps target repositories in sync with their upstream source.

### Default Update Behavior (`update: true`)

Every time the task runs:
1. It queries the remote Git server for the latest commit on the requested `version` branch.
2. If new commits exist upstream, it performs a fetch and fast-forward merge.
3. It sets `changed: true` and updates `after` with the new commit SHA.
4. If no new commits exist, it does nothing and sets `changed: false`.

```yaml
- name: Pull latest updates for web application
  ansible.builtin.git:
    repo: 'https://github.com/example/webapp.git'
    dest: /var/www/webapp
    version: production
    update: yes
```

---

### Handling Local Conflicts: `force: yes`

In real-world environments, someone might manually edit a config file on the target server, or an application might create uncommitted files in the working tree.

By default, Git will **refuse to pull** if uncommitted changes would be overwritten. The Ansible task will fail with:
```text
fatal: [web1]: FAILED! => {"msg": "Local changes would be overwritten by merge..."}
```

#### Discarding Remote Changes with `force: yes`
Setting `force: yes` forces Git to discard any local uncommitted changes, performing the equivalent of `git reset --hard` and checking out the clean upstream version:

```yaml
- name: Force pull and discard any dirty local changes
  ansible.builtin.git:
    repo: 'https://github.com/example/webapp.git'
    dest: /var/www/webapp
    version: main
    force: yes
```

> **Warning:** `force: yes` permanently wipes any uncommitted file changes in the remote working tree. Only use it when the target machine is strictly disposable or managed solely via Git.

---

### Triggering Handlers on Update

A common pattern is to restart the web server or rerun database migrations **only when new code is actually pulled**:

```yaml
- name: Deploy application code
  ansible.builtin.git:
    repo: 'https://github.com/example/app.git'
    dest: /opt/app
    version: main
  notify: Restart Application Service

handlers:
  - name: Restart Application Service
    ansible.builtin.service:
      name: myapp
      state: restarted
```

If `git` reports `changed: false` (code is already up to date), the handler is skipped and the service is not interrupted!

