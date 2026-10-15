---
title: "04. Branches and Tags"
slug: "04-branches-and-tags"
estimated_time: 8
has_hands_on: false
---

## Working with Branches, Tags, and Commits

The `version` parameter in the `ansible.builtin.git` module determines exactly what state your repository should be in.

### The `version` Parameter

The `version` parameter accepts:
1. **Branch name**: e.g. `main`, `master`, `develop`, `release/2.0`
2. **Tag name**: e.g. `v1.2.0`, `release-2026.10`
3. **Commit SHA**: e.g. `4b825dc642cb6eb9a060e54bf8d69288fbee4904` (or short SHA `4b825dc`)
4. **Git reference**: e.g. `refs/pull/42/head`

---

### Examples

#### 1. Checking Out a Specific Branch
```yaml
- name: Deploy from staging branch
  ansible.builtin.git:
    repo: https://github.com/example/app.git
    dest: /var/www/app
    version: staging
```

#### 2. Pinning to a Release Tag (Best Practice for Production)
In production, deploying from dynamic branch names (like `main`) can lead to unintended updates if new commits are pushed. Pinning to an immutable **tag** ensures exact repeatability:

```yaml
- name: Deploy versioned release tag
  ansible.builtin.git:
    repo: https://github.com/example/app.git
    dest: /var/www/app
    version: v2.4.1
```

#### 3. Pinning to an Exact Commit SHA
For absolute immutability:

```yaml
- name: Checkout specific commit SHA
  ansible.builtin.git:
    repo: https://github.com/example/app.git
    dest: /var/www/app
    version: e5a8b79c3d4f128e67a90b1234567890abcdef12
```

---

### Understanding "Detached HEAD" State

When you checkout a **tag** or a specific **commit SHA**, Git places the working tree in a **"detached HEAD"** state.  
- This is completely **normal and expected** for deployment targets.
- It simply means HEAD points directly to a commit object rather than a named branch reference.
- Ansible handles detached HEAD states seamlessly and reports idempotent updates accurately.

### Switching Between Branches

If a server is currently on `version: staging` and you update your playbook to `version: production`, Ansible will:
1. Fetch the remote refs.
2. Switch branches from `staging` to `production`.
3. Check out the latest commit on `production`.
4. Report `changed: true`.

