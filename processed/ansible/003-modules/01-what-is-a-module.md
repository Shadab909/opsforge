---
title: "01. What is a Module?"
slug: "01-what-is-a-module"
estimated_time: 8
has_hands_on: false
---

## What is an Ansible Module?

In Ansible, **modules** (also referred to as "task plugins" or "library plugins") are the fundamental discrete units of code that can be used from the command line or in a playbook task.

Ansible executes each module, usually on the remote target node, and collects return values.

### How Ansible Modules Work Under the Hood

When you execute an Ansible task or ad-hoc command:

1. **Packaging**: The Ansible control node generates a temporary Python script containing the module code and its arguments.
2. **Transfer**: Ansible connects to the target host via SSH (or WinRM/local connection) and transfers this standalone script to a temporary directory (e.g. `~/.ansible/tmp/...`).
3. **Execution**: The script executes remotely on the target host using the target host's Python interpreter.
4. **JSON Response**: The module outputs a JSON payload containing execution results, which is streamed back to the control machine.
5. **Cleanup**: Ansible deletes the temporary script and directory from the target host.

```text
[Control Node]
      │
      ├─ 1. Package Module + Arguments into Python Script
      ├─ 2. Transfer via SSH (SFTP/SCP) to ~/.ansible/tmp/
      │
      ▼
[Managed Remote Node]
      │
      ├─ 3. Target Python executes module script
      ├─ 4. Emits JSON response to stdout
      │
      ▼
[Control Node]
      │
      ├─ 5. Parses JSON response (changed, failed, rc, stdout)
      └─ 6. Cleans up temporary remote files
```

### Core Characteristics of Modules

- **Declarative & Idempotent**: A well-written Ansible module is idempotent. It checks the current state of the remote system, and if the desired state is already satisfied, it makes no changes and returns `"changed": false`.
- **Agentless**: No permanent agent or daemon runs on the target machine.
- **Language Agnostic (Primarily Python)**: While 99% of Linux modules are implemented in Python, Ansible can execute modules written in any language (such as PowerShell for Windows or compiled binaries) as long as they accept JSON/arguments and output JSON.

### Standard Module Return Values

Every module returns a structured dictionary. The most common keys include:

| Return Key | Type | Description |
|---|---|---|
| `changed` | Boolean | `true` if the task modified the target system; `false` if system was already in the desired state. |
| `failed` | Boolean | `true` if module execution encountered an error or failed. |
| `msg` | String | A human-readable message explaining what the module did or why it failed. |
| `rc` | Integer | The return code / exit code (commonly for command, shell, or script executions; 0 indicates success). |
| `stdout` / `stderr` | String | Standard output and standard error streams captured from subprocesses. |

