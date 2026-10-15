---
title: "06. Common Patterns and Best Practices"
slug: "06-patterns-and-best-practices"
estimated_time: 8
has_hands_on: false
---

## Common Patterns and Production Best Practices

Implementing the `git` module in production pipelines requires adhering to established patterns for performance, reliability, and security.

---

### Pattern 1: High-Performance Shallow Clones (`depth: 1`)

For large repositories with years of Git history, downloading every historical commit on every deployment node wastes massive bandwidth and disk I/O.

Use `depth: 1` to create a **shallow clone** containing only the latest revision:

```yaml
- name: Fast shallow deployment of web app
  ansible.builtin.git:
    repo: https://github.com/myorg/huge-monorepo.git
    dest: /var/www/app
    version: production
    depth: 1
```

Benefits:
- Up to **90% reduction** in download size and deployment duration.
- Keeps deployment servers lean by storing only active application files.

---

### Pattern 2: Atomic Zero-Downtime Deployments (Symlink Pattern)

Cloning or pulling directly into an active document root (e.g. `/var/www/html`) can cause race conditions or 500 errors while files are actively being rewritten during user requests.

The standard industry pattern uses versioned release folders and an atomic symlink:

```text
/var/www/app/
   ├── releases/
   │     ├── 20261015-v1.0/
   │     └── 20261015-v1.1/   <── Cloned via Git
   └── current ───(symlink)───► /var/www/app/releases/20261015-v1.1/
```

```yaml
- name: Create release directory
  ansible.builtin.file:
    path: "/var/www/app/releases/{{ release_id }}"
    state: directory

- name: Checkout release code
  ansible.builtin.git:
    repo: https://github.com/example/app.git
    dest: "/var/www/app/releases/{{ release_id }}"
    version: "{{ app_version }}"
    depth: 1

- name: Atomically switch current symlink
  ansible.builtin.file:
    src: "/var/www/app/releases/{{ release_id }}"
    dest: /var/www/app/current
    state: link
```

---

### Pattern 3: Single Branch Clones

If your repository contains dozens of feature branches that are never needed in production, configure `single_branch: yes`:

```yaml
- name: Clone only the production branch
  ansible.builtin.git:
    repo: https://github.com/example/app.git
    dest: /opt/app
    version: main
    single_branch: yes
```

---

### Summary of Git Module Best Practices

1. **Always use absolute paths** for `dest` (e.g. `/var/www/app`, never relative paths).
2. **Pin to Git Tags or Commit SHAs** in production to prevent unintended branch drift.
3. **Use `depth: 1`** on CI/CD pipelines and deployment targets for maximum speed.
4. **Use read-only SSH Deploy Keys** rather than personal developer tokens.
5. **Combine with Handlers** to restart daemons or build assets only when `changed: true`.

