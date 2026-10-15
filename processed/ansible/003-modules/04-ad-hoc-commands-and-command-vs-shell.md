---
title: "04. Ad-Hoc Commands: Module vs Command vs Shell"
slug: "04-ad-hoc-commands-and-command-vs-shell"
estimated_time: 9
has_hands_on: false
---

## Ad-Hoc Commands and Command vs Shell

An **ad-hoc command** is a quick, one-line Ansible command used to execute a single module across target servers without writing a multi-line playbook YAML file.

### Anatomy of an Ad-Hoc Command

```bash
ansible <host-pattern> -m <module_name> -a "<module_arguments>" [options]
```

#### Key CLI Flags:
| Flag | Long Option | Description |
|---|---|---|
| `-m` | `--module-name` | Name of the module to execute (default is `command`). |
| `-a` | `--args` | Arguments passed to the module. |
| `-b` | `--become` | Escalate privileges (run as root / sudo). |
| `-u` | `--user` | Remote SSH username to connect as. |
| `-i` | `--inventory` | Specify custom inventory file or host list. |
| `-k` | `--ask-pass` | Prompt for SSH password. |
| `-K` | `--ask-become-pass` | Prompt for sudo password. |

---

### Command vs Shell vs Raw: Critical Differences

Ansible provides three different modules to run terminal commands. Understanding when to use each is essential for secure, idempotent automation:

| Feature | `command` | `shell` | `raw` |
|---|---|---|---|
| **Underlying Binary** | Executed directly | Spawned inside `/bin/sh` | Executed directly over SSH |
| **Shell Features (`|`, `>`, `<`)** | ❌ No | ✅ Yes (pipes, redirects) | ✅ Yes |
| **Environment Variables (`$HOME`, `$PATH`)** | ❌ No (not evaluated) | ✅ Yes (evaluated by shell) | ✅ Yes |
| **Requires Remote Python?** | ✅ Yes | ✅ Yes | ❌ **No** (Zero Python needed) |
| **Idempotent by Default?** | ❌ No (always reports changed) | ❌ No (always reports changed) | ❌ No |
| **Security Risk (Shell Injection)** | Low | High (caution with user inputs) | High |

#### 1. The `command` Module (Default)
The default module when `-m` is omitted:
```bash
ansible all -a "uname -r"
```
Because it does not invoke a shell, characters like `|`, `>`, `<`, `;`, and `&` will **NOT** work; they will be treated as literal string arguments.

#### 2. The `shell` Module
Used when you need pipe operations, shell redirects, or shell environment variables:
```bash
ansible all -m shell -a "cat /etc/passwd | grep nginx > /tmp/nginx_user.txt"
```

#### 3. Making Command & Shell Idempotent: `creates` and `removes`
By default, running `command` or `shell` will always report `"changed": true` because Ansible cannot know whether the script altered state.  
To restore idempotency, use `creates=` or `removes=`:

- `creates=/path/to/file`: Only run the command if this file **does NOT exist**.
- `removes=/path/to/file`: Only run the command if this file **DOES exist**.

```bash
# Only runs archive extraction if /opt/myapp/bin does not already exist
ansible all -m command -a "tar -xzf /tmp/app.tar.gz -C /opt/myapp creates=/opt/myapp/bin"
```

