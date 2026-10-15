#!/usr/bin/env python3
"""
Builder for 003-modules (Commands & Modules)
Generates 6 chunks with ~116 comprehensive questions.
"""

import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROC_MOD_DIR = BASE_DIR / "processed" / "ansible" / "003-modules"
PROC_MOD_DIR.mkdir(parents=True, exist_ok=True)
SUPP_DIR = PROC_MOD_DIR / "supplementary"
SUPP_DIR.mkdir(parents=True, exist_ok=True)

# Copy supplementary files
KB_DIR = BASE_DIR / "knowledge_base" / "ansible" / "003-modules"
if KB_DIR.exists():
    for f in KB_DIR.iterdir():
        if f.is_file() and f.name != "index.html" and not f.name.startswith("."):
            import shutil
            shutil.copy2(f, SUPP_DIR / f.name)

# ------------------------------------------------------------------------------
# Chunks definitions
# ------------------------------------------------------------------------------

CHUNKS = [
    {
        "slug": "01-what-is-a-module",
        "title": "01. What is a Module?",
        "estimated_time": 8,
        "has_hands_on": False,
        "content": """## What is an Ansible Module?

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
""",
        "quiz": {
            "passing_score": 70,
            "questions": [
                {
                    "type": "mcq",
                    "question": "What is the primary definition of an Ansible module?",
                    "options": [
                        "A discrete unit of executable code that performs a specific system task on managed nodes",
                        "A configuration file written in YAML that declares host inventory",
                        "A daemon running continuously in the background on target servers",
                        "A database schema used to track package versions across hosts"
                    ],
                    "correct": "A discrete unit of executable code that performs a specific system task on managed nodes",
                    "explanation": "Modules are the actual executable code units (often Python scripts) that perform specific tasks on remote hosts and return JSON."
                },
                {
                    "type": "mcq",
                    "question": "What format do Ansible modules use to return data back to the control machine?",
                    "options": ["JSON", "XML", "Plain raw text only", "Binary protocol buffers"],
                    "correct": "JSON",
                    "explanation": "Ansible modules output their results as a JSON string to stdout, which the control node parses into dictionaries."
                },
                {
                    "type": "true_false",
                    "question": "Ansible requires a persistent background daemon to be installed and running on remote managed hosts before modules can run.",
                    "correct": False,
                    "explanation": "Ansible is agentless. It transfers module scripts over SSH on demand, executes them with Python, and immediately cleans them up."
                },
                {
                    "type": "mcq",
                    "question": "What does the 'changed: false' return key signify?",
                    "options": [
                        "The target host was already in the desired state, so no modifications were made",
                        "The task failed to execute due to an SSH authentication error",
                        "The task encountered a syntax error in the YAML definition",
                        "Ansible skipped the task because the host was unreachable"
                    ],
                    "correct": "The target host was already in the desired state, so no modifications were made",
                    "explanation": "Idempotent modules check the current state; if the system is already configured as requested, 'changed' is set to false."
                },
                {
                    "type": "mcq",
                    "question": "What happens to the temporary module script on the remote host after execution completes?",
                    "options": [
                        "Ansible automatically removes the temporary files and directories",
                        "It is permanently stored in /usr/bin/ansible-modules for caching",
                        "It remains in /tmp indefinitely until reboot",
                        "It is committed to the local git repository"
                    ],
                    "correct": "Ansible automatically removes the temporary files and directories",
                    "explanation": "Ansible automatically deletes the temporary script from ~/.ansible/tmp/ after capturing the JSON output."
                },
                {
                    "type": "true_false",
                    "question": "Modules can only be written in Python and cannot be developed in any other programming language.",
                    "correct": False,
                    "explanation": "While most Linux modules are written in Python, Windows modules use PowerShell, and custom modules can be written in any language that outputs JSON."
                },
                {
                    "type": "mcq",
                    "question": "Which return key indicates the process exit status for command/shell executions, where 0 means success?",
                    "options": ["rc", "exit_status", "status_code", "error_level"],
                    "correct": "rc",
                    "explanation": "'rc' stands for return code. In Unix/Linux standards, rc=0 indicates successful command completion."
                },
                {
                    "type": "mcq",
                    "question": "Where are temporary module scripts typically staged on the target host during execution?",
                    "options": [
                        "In ~/.ansible/tmp/ under the connected user's home directory",
                        "In /etc/ansible/runtime/",
                        "In /var/log/ansible/",
                        "Directly in /dev/shm/ramdisk/"
                    ],
                    "correct": "In ~/.ansible/tmp/ under the connected user's home directory",
                    "explanation": "Ansible creates a temporary directory in ~/.ansible/tmp/ (configurable via ansible.cfg) to upload and execute module scripts."
                },
                {
                    "type": "true_false",
                    "question": "In a declarative automation model, modules specify the desired end state rather than the individual steps needed to reach it.",
                    "correct": True,
                    "explanation": "Declarative design allows you to specify 'state=present' or 'state=started', leaving the logic of reaching that state to the module."
                },
                {
                    "type": "mcq",
                    "question": "If a module fails during execution, which return key is set to true?",
                    "options": ["failed", "error", "broken", "critical"],
                    "correct": "failed",
                    "explanation": "When an unhandled exception or explicit fail_json() is called, Ansible marks 'failed: true' in the result dictionary."
                },
                {
                    "type": "mcq",
                    "question": "What protocol does Ansible primarily use to connect and transfer module scripts to Linux nodes?",
                    "options": ["SSH (SFTP / SCP)", "Telnet", "RDP", "SNMP"],
                    "correct": "SSH (SFTP / SCP)",
                    "explanation": "Ansible uses standard OpenSSH or Paramiko to connect to Linux systems and transfer payload files."
                },
                {
                    "type": "true_false",
                    "question": "Because Ansible modules are executed on the remote target host, that target host must have a compatible Python interpreter installed.",
                    "correct": True,
                    "explanation": "Standard Ansible modules require a Python runtime on the target host (typically Python 3.6+ on modern Linux distributions)."
                },
                {
                    "type": "mcq",
                    "question": "Which of the following is NOT a standard return field in Ansible module execution results?",
                    "options": ["git_commit_sha", "changed", "failed", "msg"],
                    "correct": "git_commit_sha",
                    "explanation": "'git_commit_sha' is not a standard common return key, whereas 'changed', 'failed', and 'msg' are standard."
                },
                {
                    "type": "true_false",
                    "question": "An idempotent task will produce the exact same system state whether executed once or run twenty consecutive times.",
                    "correct": True,
                    "explanation": "Idempotency ensures that subsequent runs with the same parameters do not alter an already compliant system."
                },
                {
                    "type": "mcq",
                    "question": "What is the primary role of the Ansible control node during module execution?",
                    "options": [
                        "Packaging module code, dispatching it to target nodes, and aggregating the returned JSON results",
                        "Compiling C binaries for remote kernel modules",
                        "Serving web pages for client browsers",
                        "Acting as the default gateway for remote network traffic"
                    ],
                    "correct": "Packaging module code, dispatching it to target nodes, and aggregating the returned JSON results",
                    "explanation": "The control node orchestrates execution by preparing module payloads, shipping them over SSH, and analyzing responses."
                },
                {
                    "type": "true_false",
                    "question": "If a module executes and detects that a file already has the exact requested permissions and content, 'changed' will be true.",
                    "correct": False,
                    "explanation": "If no modifications were needed or made to the file, 'changed' will be false."
                },
                {
                    "type": "mcq",
                    "question": "What return field provides standard error output from executed subcommands?",
                    "options": ["stderr", "err_output", "std_error", "system_log"],
                    "correct": "stderr",
                    "explanation": "'stderr' captures the standard error stream output from commands executed by the module."
                },
                {
                    "type": "mcq",
                    "question": "What is the key benefit of modules returning structured JSON instead of unstructured raw terminal text?",
                    "options": [
                        "Playbooks and conditional logic can easily inspect, register, and evaluate specific fields programmatically",
                        "JSON files run 50 times faster than binary code",
                        "Raw text cannot be transmitted over SSH connections",
                        "JSON automatically encrypts all passwords by default"
                    ],
                    "correct": "Playbooks and conditional logic can easily inspect, register, and evaluate specific fields programmatically",
                    "explanation": "Structured JSON allows Ansible to evaluate variables, conditionals (`when: result.changed`), and loop over return data easily."
                }
            ]
        }
    },
    {
        "slug": "02-the-ping-module",
        "title": "02. The Ping Module & Source Code",
        "estimated_time": 7,
        "has_hands_on": False,
        "content": """## The Ping Module (`ansible.builtin.ping`)

The `ping` module is the classic "Hello World" of Ansible. It verifies that:
1. Ansible can connect to the target host over SSH.
2. The user has valid login authentication (key or password).
3. The target node has a usable Python environment capable of executing Ansible payloads.

### Ping: ICMP vs Ansible Ping

> **Important Distinction:**  
> `ansible.builtin.ping` is **NOT** an ICMP network ping (the `ping` shell command).  
> Standard ICMP ping only verifies that an IP address responds to ICMP echo requests. It tells you nothing about whether SSH is running or whether Python is available.  
> Ansible's `ping` module actually transfers and runs Python code on the remote machine.

```text
ICMP ping 192.168.1.50   ───► Checks Network Layer 3 connectivity only
ansible all -m ping      ───► Tests SSH + Authentication + Python Interpreter execution
```

### Running the Ping Module via Ad-Hoc Command

To execute ping across all inventory hosts:

```bash
ansible all -m ping
```

#### Successful Output:
```json
server1 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```

Notice:
- `"changed": false`: Because checking connectivity does not modify the target system.
- `"ping": "pong"`: The standard handshake response proving the module ran and returned data.

### The Ping Module Source Code

The actual implementation of `ansible.builtin.ping` inside `ansible-core` is delightfully concise:

```python
# Part of ansible-core / lib/ansible/modules/ping.py
from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec=dict(
            data=dict(type='str', default='pong'),
        ),
        supports_check_mode=True
    )

    if module.params['data'] == 'crash':
        raise Exception("boom")

    result = dict(
        ping=module.params['data'],
    )

    module.exit_json(**result)

if __name__ == '__main__':
    main()
```

### Key Insights from Source Code

1. **`argument_spec`**: Defines the accepted arguments. `data` defaults to `'pong'`.
2. **`supports_check_mode=True`**: Because ping makes no changes, it safely runs in check mode (`--check`).
3. **Crash Simulation**: If you pass `data=crash`, the module raises an uncaught exception (`raise Exception("boom")`), which is handy for testing Ansible error handling!
   ```bash
   ansible all -m ping -a "data=crash"
   ```
4. **Custom Return Values**: You can supply any custom string in `data`:
   ```bash
   ansible all -m ping -a "data=hello_world"
   ```
   Output:
   ```json
   "ping": "hello_world"
   ```
""",
        "quiz": {
            "passing_score": 70,
            "questions": [
                {
                    "type": "mcq",
                    "question": "How does Ansible's 'ping' module differ from the traditional ICMP 'ping' command?",
                    "options": [
                        "Ansible ping connects via SSH and executes Python code; ICMP ping only sends network echo packets",
                        "Ansible ping only works on local Docker containers",
                        "Ansible ping checks web servers via HTTP GET requests",
                        "There is no difference; Ansible ping executes /bin/ping under the hood"
                    ],
                    "correct": "Ansible ping connects via SSH and executes Python code; ICMP ping only sends network echo packets",
                    "explanation": "Ansible's ping module requires SSH access, valid credentials, and a working Python interpreter on the remote host."
                },
                {
                    "type": "mcq",
                    "question": "What is the default return value key and message for a successful ping execution?",
                    "options": [
                        "\"ping\": \"pong\"",
                        "\"status\": \"online\"",
                        "\"alive\": true",
                        "\"icmp\": \"reply\""
                    ],
                    "correct": "\"ping\": \"pong\"",
                    "explanation": "By default, the ping module sets the key 'ping' to the string 'pong'."
                },
                {
                    "type": "true_false",
                    "question": "When 'ansible all -m ping' succeeds, the returned 'changed' property is set to true.",
                    "correct": False,
                    "explanation": "Testing connectivity does not modify the target system state, so 'changed' is always false."
                },
                {
                    "type": "mcq",
                    "question": "What occurs when you pass the argument 'data=crash' to the ping module?",
                    "options": [
                        "The module raises an unhandled exception ('boom') to simulate a module failure",
                        "The target host operating system triggers a kernel panic",
                        "Ansible reboots the remote server immediately",
                        "Ansible deletes the target from the inventory"
                    ],
                    "correct": "The module raises an unhandled exception ('boom') to simulate a module failure",
                    "explanation": "The ping source code explicitly checks if data == 'crash' and raises an exception for testing error handlers."
                },
                {
                    "type": "mcq",
                    "question": "Which command tests connectivity using the ping module against all managed nodes in inventory?",
                    "options": [
                        "ansible all -m ping",
                        "ansible-playbook ping all",
                        "ansible-galaxy ping --all",
                        "ansible-inventory -m ping"
                    ],
                    "correct": "ansible all -m ping",
                    "explanation": "The syntax for an ad-hoc command is: ansible <hosts> -m <module>."
                },
                {
                    "type": "true_false",
                    "question": "The ping module supports check mode ('--check') because it makes no permanent changes to target hosts.",
                    "correct": True,
                    "explanation": "The source code specifies 'supports_check_mode=True'."
                },
                {
                    "type": "mcq",
                    "question": "If you execute 'ansible all -m ping -a \"data=ready\"', what will the JSON response contain?",
                    "options": [
                        "\"ping\": \"ready\"",
                        "\"ping\": \"pong\"",
                        "\"status\": \"ready\"",
                        "Syntax Error: ping does not accept arguments"
                    ],
                    "correct": "\"ping\": \"ready\"",
                    "explanation": "The 'data' parameter overrides the default 'pong' value with whatever string is provided."
                },
                {
                    "type": "mcq",
                    "question": "If a target machine has port 22 blocked by a firewall, what result will 'ansible target -m ping' produce?",
                    "options": [
                        "UNREACHABLE with an SSH connection timeout error",
                        "SUCCESS with ping: pong",
                        "CHANGED with rc: 1",
                        "A successful ICMP echo reply"
                    ],
                    "correct": "UNREACHABLE with an SSH connection timeout error",
                    "explanation": "Because Ansible ping operates over SSH, blocked SSH ports cause an UNREACHABLE error."
                },
                {
                    "type": "true_false",
                    "question": "If a host responds to standard terminal 'ping 10.0.0.1', Ansible is guaranteed to be able to run tasks on it.",
                    "correct": False,
                    "explanation": "ICMP ping only proves network routing; SSH might be closed, credentials might be wrong, or Python might be missing."
                },
                {
                    "type": "mcq",
                    "question": "What Python helper function inside Ansible modules is used to send successful JSON results back to the control machine?",
                    "options": ["module.exit_json()", "module.return_success()", "sys.exit(0)", "print(json.dump())"],
                    "correct": "module.exit_json()",
                    "explanation": "The AnsibleModule class provides `module.exit_json(**result)` to format and return success data."
                },
                {
                    "type": "mcq",
                    "question": "What Fully Qualified Collection Name (FQCN) refers to the core built-in ping module?",
                    "options": ["ansible.builtin.ping", "community.general.ping", "ansible.core.ping", "core.network.ping"],
                    "correct": "ansible.builtin.ping",
                    "explanation": "Core modules distributed with ansible-core live under the `ansible.builtin` collection namespace."
                },
                {
                    "type": "true_false",
                    "question": "The ping module requires root/sudo privileges and must always be run with '--become'.",
                    "correct": False,
                    "explanation": "The ping module executes simple non-privileged Python code and does not require administrative privileges."
                },
                {
                    "type": "mcq",
                    "question": "What fact is often discovered and displayed in the ping output if Python interpreter discovery is active?",
                    "options": [
                        "discovered_interpreter_python",
                        "installed_kernel_headers",
                        "remote_root_password",
                        "current_battery_level"
                    ],
                    "correct": "discovered_interpreter_python",
                    "explanation": "Ansible automatically discovers the path to the remote Python binary (e.g. /usr/bin/python3)."
                },
                {
                    "type": "mcq",
                    "question": "What Python class forms the foundation of standard Ansible module development as seen in ping.py?",
                    "options": ["AnsibleModule", "BaseTaskRunner", "PluginEngine", "PlaybookContext"],
                    "correct": "AnsibleModule",
                    "explanation": "From `ansible.module_utils.basic import AnsibleModule`. It handles parsing arguments, check mode, and JSON output."
                },
                {
                    "type": "true_false",
                    "question": "Running 'ansible all -m ping' requires an existing playbook file on the control machine.",
                    "correct": False,
                    "explanation": "Ad-hoc commands run directly from the command line against an inventory without requiring a playbook YAML file."
                },
                {
                    "type": "mcq",
                    "question": "In the ping module code, what parameter type is defined for the 'data' argument?",
                    "options": ["str", "int", "bool", "dict"],
                    "correct": "str",
                    "explanation": "In argument_spec, data is defined as: `data=dict(type='str', default='pong')`."
                },
                {
                    "type": "mcq",
                    "question": "If Python is completely uninstalled on the remote host, which module can be used to bootstrap Python before using ping?",
                    "options": ["raw", "copy", "template", "setup"],
                    "correct": "raw",
                    "explanation": "The `raw` module bypasses the Python subsystem entirely and sends commands directly via SSH, perfect for `apt install python3`."
                },
                {
                    "type": "true_false",
                    "question": "Passing invalid arguments to ping (e.g. '-a foo=bar') will cause Ansible to reject the task with an unsupported parameter error.",
                    "correct": True,
                    "explanation": "AnsibleModule validates arguments against `argument_spec` and rejects unknown parameters."
                }
            ]
        }
    },
    {
        "slug": "03-discovering-and-documenting-modules",
        "title": "03. Discovering and Documenting Modules",
        "estimated_time": 8,
        "has_hands_on": False,
        "content": """## Discovering & Documenting Modules

Ansible ships with thousands of modules covering cloud providers (AWS, Azure, GCP), operating systems, networking devices, containers, databases, and monitoring systems.

### Fully Qualified Collection Names (FQCN)

Starting with **Ansible 2.10**, Ansible reorganized its monolithic codebase into **Collections**.
A module is addressed by its **FQCN** in the format:

```text
<namespace>.<collection_name>.<module_name>
```

Examples:
- `ansible.builtin.copy` (Core built-in module)
- `community.general.slack` (Community collection)
- `amazon.aws.ec2_instance` (AWS collection)

While short names like `copy` or `ping` still work for built-in modules due to backward compatibility, using the **FQCN** is the official best practice in modern Ansible.

---

### The `ansible-doc` Command Line Tool

The `ansible-doc` command is your built-in offline encyclopedia for Ansible modules, plugins, and collections.

#### 1. Listing All Available Modules
To list all modules currently installed on your control node:

```bash
ansible-doc -l
```

To list modules within a specific collection:
```bash
ansible-doc -l ansible.builtin
```

#### 2. Viewing Full Documentation for a Module
To view parameters, choices, default values, and requirements for a module:

```bash
ansible-doc copy
# Or using FQCN:
ansible-doc ansible.builtin.copy
```

Output includes:
- **SYNOPSIS**: Explanation of what the module does.
- **PARAMETERS**: Each parameter, its type, required status, and default value.
- **NOTES**: Gotchas and platform compatibility details.
- **EXAMPLES**: Copy-pasteable playbook snippets illustrating real-world use cases.
- **RETURN VALUES**: What data keys the module returns.

#### 3. Generating Playbook Snippets (`-s`)
The `-s` (snippet) flag prints a minimal, ready-to-use YAML skeleton with all parameters:

```bash
ansible-doc -s ping
```

Output:
```yaml
- name: Try to connect to host, verify a usable python and return `pong' on success
  ansible.builtin.ping:
    data:                  # Value provided with the `data' parameter.
```

---

### Finding the Right Module for Your Task

Different Linux distributions and platforms use specialized package and service managers:

| Domain | Debian/Ubuntu | RHEL/CentOS/Rocky | Generic/Cross-Platform |
|---|---|---|---|
| Package Manager | `ansible.builtin.apt` | `ansible.builtin.dnf` / `yum` | `ansible.builtin.package` |
| Service Manager | `ansible.builtin.systemd` | `ansible.builtin.systemd` | `ansible.builtin.service` |
| User Accounts | `ansible.builtin.user` | `ansible.builtin.user` | `ansible.builtin.user` |
| Firewalls | `community.general.ufw` | `ansible.posix.firewalld` | `ansible.builtin.iptables` |

> **Pro Tip:** When writing playbooks meant to run across different Linux distributions, using generic modules like `ansible.builtin.package` or `ansible.builtin.service` allows Ansible to automatically delegate to the correct underlying system tool.
""",
        "quiz": {
            "passing_score": 70,
            "questions": [
                {
                    "type": "mcq",
                    "question": "What does FQCN stand for in modern Ansible architecture?",
                    "options": [
                        "Fully Qualified Collection Name",
                        "Fast Query Configuration Node",
                        "File Queue Control Network",
                        "Format Query Command Notification"
                    ],
                    "correct": "Fully Qualified Collection Name",
                    "explanation": "FQCN stands for Fully Qualified Collection Name, structured as <namespace>.<collection>.<module>."
                },
                {
                    "type": "mcq",
                    "question": "Which command lists all installed modules available on the Ansible control node?",
                    "options": ["ansible-doc -l", "ansible-list-modules", "ansible all --show-modules", "ansible-galaxy list --all"],
                    "correct": "ansible-doc -l",
                    "explanation": "'ansible-doc -l' (or --list) lists all available plugins/modules."
                },
                {
                    "type": "mcq",
                    "question": "Which flag with 'ansible-doc' outputs a concise, copy-pasteable YAML task snippet?",
                    "options": ["-s (or --snippet)", "-y (or --yaml)", "-c (or --code)", "-t (or --template)"],
                    "correct": "-s (or --snippet)",
                    "explanation": "'ansible-doc -s <module>' outputs a formatted YAML skeleton of parameters."
                },
                {
                    "type": "true_false",
                    "question": "Starting with Ansible 2.10, modules were separated from the core engine into modular Collections.",
                    "correct": True,
                    "explanation": "The collection split allowed modules to be versioned, released, and maintained independently of ansible-core."
                },
                {
                    "type": "mcq",
                    "question": "What collection contains the core modules bundled directly with ansible-core?",
                    "options": ["ansible.builtin", "community.general", "ansible.legacy", "core.modules"],
                    "correct": "ansible.builtin",
                    "explanation": "All fundamental modules like copy, file, ping, command, and service belong to 'ansible.builtin'."
                },
                {
                    "type": "mcq",
                    "question": "If you want to install packages across mixed distributions (both Ubuntu and Rocky Linux), which generic module is ideal?",
                    "options": ["ansible.builtin.package", "ansible.builtin.apt", "ansible.builtin.dnf", "ansible.builtin.pip"],
                    "correct": "ansible.builtin.package",
                    "explanation": "The 'package' module acts as a proxy that detects the host OS and calls apt, dnf, yum, or pacman automatically."
                },
                {
                    "type": "true_false",
                    "question": "You need an active internet connection to read module documentation using 'ansible-doc'.",
                    "correct": False,
                    "explanation": "'ansible-doc' reads documentation directly from Python docstrings stored on your local control node offline."
                },
                {
                    "type": "mcq",
                    "question": "What section of 'ansible-doc <module>' provides working examples of how to configure the module in a playbook?",
                    "options": ["EXAMPLES", "SYNOPSIS", "RETURN VALUES", "PARAMETERS"],
                    "correct": "EXAMPLES",
                    "explanation": "The EXAMPLES section provides copy-pasteable playbook task examples."
                },
                {
                    "type": "mcq",
                    "question": "Which module would you use for managing services on modern Linux distributions running systemd?",
                    "options": ["ansible.builtin.systemd (or service)", "ansible.builtin.initd", "ansible.builtin.rc_service", "ansible.builtin.runlevel"],
                    "correct": "ansible.builtin.systemd (or service)",
                    "explanation": "'systemd' or generic 'service' manages systemd units, states, and boot enablement."
                },
                {
                    "type": "true_false",
                    "question": "Short module names like 'copy' and 'ping' are deprecated and will not work at all in playbooks.",
                    "correct": False,
                    "explanation": "Short names still work for built-in modules for backward compatibility, though FQCN is recommended."
                },
                {
                    "type": "mcq",
                    "question": "What is the standard FQCN format?",
                    "options": [
                        "namespace.collection_name.module_name",
                        "module_name://collection/namespace",
                        "namespace/module_name",
                        "collection::namespace::module"
                    ],
                    "correct": "namespace.collection_name.module_name",
                    "explanation": "E.g. community.general.slack or ansible.builtin.copy."
                },
                {
                    "type": "mcq",
                    "question": "Which package manager module is specific to Debian and Ubuntu systems?",
                    "options": ["apt", "dnf", "yum", "zypper"],
                    "correct": "apt",
                    "explanation": "`ansible.builtin.apt` manages packages on Debian/Ubuntu systems."
                },
                {
                    "type": "true_false",
                    "question": "'ansible-doc' can also display documentation for inventory plugins, callback plugins, and lookup plugins using the '-t' flag.",
                    "correct": True,
                    "explanation": "Yes, 'ansible-doc -t lookup <plugin>' or 'ansible-doc -t callback <plugin>' inspects other plugin types."
                },
                {
                    "type": "mcq",
                    "question": "In 'ansible-doc' output, what does a parameter marked with '= (required)' indicate?",
                    "options": [
                        "The task will fail with a validation error if this parameter is omitted",
                        "The parameter is optional and defaults to true",
                        "The parameter is only available in check mode",
                        "The parameter requires root privilege escalation"
                    ],
                    "correct": "The task will fail with a validation error if this parameter is omitted",
                    "explanation": "Required parameters must be supplied whenever the module is invoked."
                },
                {
                    "type": "mcq",
                    "question": "Which package manager module is the default on modern RHEL 8/9 and Fedora?",
                    "options": ["dnf", "apt", "pacman", "apk"],
                    "correct": "dnf",
                    "explanation": "DNF (Dandified YUM) is the package manager for modern RHEL/CentOS/Fedora systems."
                },
                {
                    "type": "true_false",
                    "question": "Custom collections installed from Ansible Galaxy are documented through 'ansible-doc' just like built-in modules.",
                    "correct": True,
                    "explanation": "Any installed collection in your collections path can be inspected via `ansible-doc namespace.collection.module`."
                },
                {
                    "type": "mcq",
                    "question": "Which section of 'ansible-doc' explains the keys returned by the module in JSON output?",
                    "options": ["RETURN VALUES", "PARAMETERS", "SYNOPSIS", "SEE ALSO"],
                    "correct": "RETURN VALUES",
                    "explanation": "The RETURN VALUES section lists the keys returned on success or failure."
                },
                {
                    "type": "true_false",
                    "question": "Using generic modules like 'service' guarantees identical parameter options as specialized modules like 'systemd'.",
                    "correct": False,
                    "explanation": "Generic modules provide lowest common denominator parameters; specialized modules expose distro-specific features like daemon_reload."
                }
            ]
        }
    },
    {
        "slug": "04-ad-hoc-commands-and-command-vs-shell",
        "title": "04. Ad-Hoc Commands: Module vs Command vs Shell",
        "estimated_time": 9,
        "has_hands_on": False,
        "content": """## Ad-Hoc Commands and Command vs Shell

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
""",
        "quiz": {
            "passing_score": 70,
            "questions": [
                {
                    "type": "mcq",
                    "question": "What is the default module used when 'ansible <hosts> -a \"command\"' is executed without the '-m' flag?",
                    "options": ["command", "shell", "raw", "ping"],
                    "correct": "command",
                    "explanation": "If no '-m' flag is specified in an ad-hoc command, Ansible defaults to 'command'."
                },
                {
                    "type": "mcq",
                    "question": "Why will the command 'ansible all -m command -a \"cat /etc/os-release | grep VERSION\"' fail to pipe output?",
                    "options": [
                        "The 'command' module executes directly without a shell, so pipes ('|') are not supported",
                        "The control node disables pipes for security reasons",
                        "The 'cat' command is not supported on Linux",
                        "Ansible requires Python 2 to evaluate pipe symbols"
                    ],
                    "correct": "The 'command' module executes directly without a shell, so pipes ('|') are not supported",
                    "explanation": "The 'command' module executes the executable directly without spawning a subshell, so pipe and redirection operators do not work."
                },
                {
                    "type": "mcq",
                    "question": "Which execution module should be used when you need pipe operations, stream redirection (>), or shell variables ($VAR)?",
                    "options": ["shell", "command", "copy", "file"],
                    "correct": "shell",
                    "explanation": "The 'shell' module runs commands through `/bin/sh -c`, enabling pipes, redirects, and environment variable expansion."
                },
                {
                    "type": "true_false",
                    "question": "By default, tasks using the 'command' or 'shell' module will always report 'changed: true' every time they run.",
                    "correct": True,
                    "explanation": "Because Ansible cannot inspect arbitrary command side-effects, it defaults to reporting changed: true unless controlled by creates/removes or changed_when."
                },
                {
                    "type": "mcq",
                    "question": "How can you make a 'command' or 'shell' task idempotent so it only runs if a target file is missing?",
                    "options": [
                        "Use the 'creates=/path/to/file' parameter",
                        "Use the 'removes=/path/to/file' parameter",
                        "Pass the '--idempotent' flag on the CLI",
                        "Set 'state=present' on the command module"
                    ],
                    "correct": "Use the 'creates=/path/to/file' parameter",
                    "explanation": "'creates' tells Ansible: 'If this file/directory already exists, skip running the command'."
                },
                {
                    "type": "mcq",
                    "question": "What is the purpose of the 'removes=/path/to/file' parameter in command and shell modules?",
                    "options": [
                        "The command will only execute if the specified file/directory already exists",
                        "Ansible automatically deletes the file before executing the command",
                        "Ansible deletes the file if the command returns a non-zero exit code",
                        "It removes temporary SSH keys after command completion"
                    ],
                    "correct": "The command will only execute if the specified file/directory already exists",
                    "explanation": "'removes' tells Ansible: 'Only run this command if this file exists (e.g. clean-up scripts)'."
                },
                {
                    "type": "mcq",
                    "question": "Which module allows command execution on a remote host that has NO Python installed at all?",
                    "options": ["raw", "command", "shell", "script"],
                    "correct": "raw",
                    "explanation": "The 'raw' module issues SSH commands directly without invoking the Ansible Python wrapper subsystem."
                },
                {
                    "type": "true_false",
                    "question": "The 'shell' module is safer than dedicated declarative modules (like apt, user, or copy) because it uses standard bash commands.",
                    "correct": False,
                    "explanation": "Shell is potentially dangerous, prone to injection vulnerabilities, and lacks built-in idempotence compared to declarative modules."
                },
                {
                    "type": "mcq",
                    "question": "What flag enables privilege escalation (sudo/root) in an ad-hoc command?",
                    "options": ["-b (or --become)", "-s (or --sudo)", "-r (or --root)", "-p (or --privilege)"],
                    "correct": "-b (or --become)",
                    "explanation": "The `-b` or `--become` flag tells Ansible to execute the task using privilege escalation."
                },
                {
                    "type": "mcq",
                    "question": "What flag prompts the administrator for the remote sudo/become password when running an ad-hoc command?",
                    "options": ["-K (or --ask-become-pass)", "-k (or --ask-pass)", "-P (or --password)", "-S (or --sudo-pass)"],
                    "correct": "-K (or --ask-become-pass)",
                    "explanation": "Uppercase `-K` prompts for the become/sudo password, whereas lowercase `-k` prompts for the SSH connection password."
                },
                {
                    "type": "true_false",
                    "question": "Ad-hoc commands are best suited for repeatable infrastructure provisioning rather than one-off tasks.",
                    "correct": False,
                    "explanation": "Ad-hoc commands are meant for quick one-off checks or emergencies; playbooks are used for structured, repeatable provisioning."
                },
                {
                    "type": "mcq",
                    "question": "In the ad-hoc command 'ansible webservers -m apt -a \"name=nginx state=present\" -b', what is 'webservers'?",
                    "options": [
                        "The host pattern / inventory group targeting specific servers",
                        "The module name being executed",
                        "The SSH username connecting to the hosts",
                        "The sudo password being passed"
                    ],
                    "correct": "The host pattern / inventory group targeting specific servers",
                    "explanation": "The first positional parameter after 'ansible' specifies the target host pattern or group."
                },
                {
                    "type": "mcq",
                    "question": "What happens if a command executed via the 'command' module returns exit code 1?",
                    "options": [
                        "Ansible reports the task as FAILED and halts execution on that host",
                        "Ansible ignores the failure and continues silently",
                        "Ansible automatically switches to the shell module and retries",
                        "The control node restarts the target server"
                    ],
                    "correct": "Ansible reports the task as FAILED and halts execution on that host",
                    "explanation": "Non-zero exit codes (rc != 0) cause the task to fail by default."
                },
                {
                    "type": "true_false",
                    "question": "The 'command' module allows you to change the working directory before executing the command using 'chdir=/path'.",
                    "correct": True,
                    "explanation": "'chdir' is a supported parameter for both command and shell modules."
                },
                {
                    "type": "mcq",
                    "question": "Which of the following is considered an anti-pattern when writing Ansible playbooks?",
                    "options": [
                        "Using the 'shell' module to run 'apt-get install nginx' instead of the dedicated 'apt' module",
                        "Using FQCN for module names",
                        "Running tasks with become: true",
                        "Grouping related servers into inventory groups"
                    ],
                    "correct": "Using the 'shell' module to run 'apt-get install nginx' instead of the dedicated 'apt' module",
                    "explanation": "Using shell commands when a dedicated, idempotent module (like apt) exists violates Ansible best practices."
                },
                {
                    "type": "true_false",
                    "question": "Redirecting output with '>' in the command module will work as expected because Linux kernels handle redirection natively.",
                    "correct": False,
                    "explanation": "Redirection is handled by the shell (/bin/sh or /bin/bash), not the kernel. Since 'command' skips the shell, '>' is ignored or treated as an argument."
                },
                {
                    "type": "mcq",
                    "question": "What is the recommended approach if a command you run changes state only under specific conditions?",
                    "options": [
                        "Use 'creates' or 'removes' parameters, or handle with 'changed_when' in playbooks",
                        "Always accept that it reports changed: true",
                        "Run the command twice",
                        "Use ping before running the command"
                    ],
                    "correct": "Use 'creates' or 'removes' parameters, or handle with 'changed_when' in playbooks",
                    "explanation": "'creates', 'removes', and 'changed_when' give you fine-grained control over idempotency reporting."
                },
                {
                    "type": "true_false",
                    "question": "The 'raw' module can be used to install python3-minimal on a newly provisioned Debian system that lacks Python.",
                    "correct": True,
                    "explanation": "Because 'raw' sends commands directly through the SSH connection, it is the standard tool to bootstrap Python."
                },
                {
                    "type": "mcq",
                    "question": "Which argument to the command module allows you to specify standard input directly as a string?",
                    "options": ["stdin", "input_data", "pipe_in", "content"],
                    "correct": "stdin",
                    "explanation": "The 'stdin' parameter passes string data directly into the command's standard input."
                },
                {
                    "type": "true_false",
                    "question": "Passing passwords directly inside '-a' arguments in bash history can expose secrets to other local users via the process table.",
                    "correct": True,
                    "explanation": "Arguments passed on the command line can be viewed via `ps aux` and saved in `~/.bash_history`."
                }
            ]
        }
    },
    {
        "slug": "05-file-and-download-modules",
        "title": "05. File Management & Download Modules",
        "estimated_time": 9,
        "has_hands_on": False,
        "content": """## File Management & Download Modules

Ansible provides a rich set of declarative file management modules. These modules verify file contents, hashes, permissions, and directories idempotently.

---

### 1. The `copy` Module (`ansible.builtin.copy`)

Copies files from the local control machine (or remote host) to a destination on managed nodes.

```yaml
- name: Copy configuration file with permissions
  ansible.builtin.copy:
    src: /local/path/app.conf
    dest: /etc/myapp/app.conf
    owner: www-data
    group: www-data
    mode: '0644'
    backup: yes
```

#### Key Parameters:
- `src`: Path to the source file on the local machine (relative or absolute).
- `dest`: Absolute path on the remote host where the file should be copied.
- `content`: Instead of `src`, you can provide inline text directly:
  ```yaml
  content: "managed_by: ansible\nenv: production\n"
  ```
- `backup: yes`: Creates a timestamped backup copy if the destination file already exists and is modified.
- `remote_src: yes`: Treats `src` as a path already located on the remote machine (similar to remote `cp`).
- `mode`: Unix file permissions (always quote octal values like `'0644'` or `'0755'`).

---

### 2. The `file` Module (`ansible.builtin.file`)

Manages file properties, directory structures, symlinks, and deletion.

```yaml
# 1. Create a directory
- name: Create app directory
  ansible.builtin.file:
    path: /var/www/myapp
    state: directory
    owner: nginx
    group: nginx
    mode: '0755'

# 2. Create a symbolic link
- name: Create symlink to latest release
  ansible.builtin.file:
    src: /var/www/releases/v2.1.0
    dest: /var/www/current
    state: link

# 3. Delete a file or directory recursively
- name: Remove obsolete directory
  ansible.builtin.file:
    path: /tmp/old_build
    state: absent

# 4. Touch an empty file
- name: Touch a heartbeat file
  ansible.builtin.file:
    path: /var/log/heartbeat.log
    state: touch
    mode: '0600'
```

#### The `state` Parameter in `file`:
- `directory`: Ensures the directory exists.
- `file`: Verifies/updates permissions on an existing file (does not create it).
- `link`: Creates a symbolic link (`src` points to target, `dest` is symlink path).
- `hard`: Creates a hard link.
- `touch`: Creates an empty file if missing, or updates the mtime/atime if it exists.
- `absent`: Removes the file or directory recursively.

---

### 3. The `lineinfile` Module (`ansible.builtin.lineinfile`)

Ensures a particular line is in a file, or modifies an existing line using regular expressions. Great for config files!

```yaml
- name: Ensure SSH PermitRootLogin is disabled
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^#?PermitRootLogin'
    line: 'PermitRootLogin no'
    state: present
    backup: yes
```

#### Key Parameters:
- `path`: Target file.
- `regexp`: Python regular expression to locate the line to replace.
- `line`: The exact line string to ensure.
- `insertafter` / `insertbefore`: Controls placement if line does not match `regexp`.
- `state: absent`: Removes any line matching `regexp`.

---

### 4. The `get_url` Module (`ansible.builtin.get_url`)

Downloads files from HTTP, HTTPS, or FTP directly onto target nodes.

```yaml
- name: Download Prometheus release binary
  ansible.builtin.get_url:
    url: https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus.tar.gz
    dest: /tmp/prometheus.tar.gz
    mode: '0644'
    checksum: sha256:d8c1c4e7f...
```

#### Key Parameters:
- `url`: Download URL.
- `dest`: Remote destination file or directory path.
- `checksum`: Cryptographic hash (`sha256:<hash>`) ensuring download integrity. If the remote file matches the checksum, download is skipped (idempotent!).
""",
        "quiz": {
            "passing_score": 70,
            "questions": [
                {
                    "type": "mcq",
                    "question": "What is the primary difference between the 'copy' module and the 'file' module?",
                    "options": [
                        "'copy' transfers file data and content; 'file' manages metadata, directories, symlinks, and deletion",
                        "'copy' only works on Windows; 'file' only works on Linux",
                        "'file' downloads files from the internet; 'copy' does not",
                        "They are identical and can be used interchangeably"
                    ],
                    "correct": "'copy' transfers file data and content; 'file' manages metadata, directories, symlinks, and deletion",
                    "explanation": "'copy' is used to deploy files with content; 'file' manipulates directory trees, permissions, links, and removals."
                },
                {
                    "type": "mcq",
                    "question": "Why should octal permissions (like mode: '0644') always be wrapped in quotes in YAML?",
                    "options": [
                        "YAML might interpret bare leading zeros as base-8 integers or decimal numbers, corrupting permissions",
                        "Quotes are required by the Linux filesystem kernel",
                        "Unquoted numbers cause an SSH disconnection",
                        "Permissions cannot exceed 3 digits without quotes"
                    ],
                    "correct": "YAML might interpret bare leading zeros as base-8 integers or decimal numbers, corrupting permissions",
                    "explanation": "In YAML parsers, unquoted 0644 is interpreted as an octal integer (420 in decimal), leading to unexpected file permissions."
                },
                {
                    "type": "true_false",
                    "question": "Setting 'remote_src: yes' in the copy module instructs Ansible to copy a file from the remote target to the local control machine.",
                    "correct": False,
                    "explanation": "'remote_src: yes' means both the source and destination are on the remote host (like a remote 'cp' command)."
                },
                {
                    "type": "mcq",
                    "question": "Which module allows you to download an archive from the internet directly onto managed nodes with checksum validation?",
                    "options": ["get_url", "fetch", "copy", "uri"],
                    "correct": "get_url",
                    "explanation": "`ansible.builtin.get_url` downloads files via HTTP/HTTPS/FTP and supports checksum validation for idempotency."
                },
                {
                    "type": "mcq",
                    "question": "What value of the 'state' parameter in the 'file' module ensures an entire directory and its contents are deleted?",
                    "options": ["absent", "deleted", "remove", "clean"],
                    "correct": "absent",
                    "explanation": "'state: absent' recursively removes the target file, directory, or symlink."
                },
                {
                    "type": "mcq",
                    "question": "Which module and parameter combination is best suited for modifying a single configuration line in /etc/ssh/sshd_config?",
                    "options": [
                        "lineinfile with 'regexp' and 'line'",
                        "file with 'state=touch'",
                        "get_url with 'force=yes'",
                        "raw with 'echo PermitRootLogin no'"
                    ],
                    "correct": "lineinfile with 'regexp' and 'line'",
                    "explanation": "`lineinfile` searches for lines matching the regex and replaces them with the desired line string."
                },
                {
                    "type": "true_false",
                    "question": "If 'get_url' runs and the destination file already exists and matches the provided 'checksum', it skips the download.",
                    "correct": True,
                    "explanation": "Checksum verification ensures idempotency by skipping downloads if the file is already present with matching hash."
                },
                {
                    "type": "mcq",
                    "question": "What does the 'backup: yes' parameter do when used in the copy or lineinfile module?",
                    "options": [
                        "Creates a timestamped backup copy of the original file before modifying it",
                        "Uploads the file to an external S3 bucket",
                        "Creates a git repository in the directory",
                        "Saves the backup to the control machine's desktop"
                    ],
                    "correct": "Creates a timestamped backup copy of the original file before modifying it",
                    "explanation": "'backup: yes' creates a backup file with a timestamp suffix (e.g. filename.12345.2026-10-15@12:00:00~)."
                },
                {
                    "type": "mcq",
                    "question": "How do you create a directory using the file module?",
                    "options": ["state: directory", "type: folder", "action: mkdir", "state: present"],
                    "correct": "state: directory",
                    "explanation": "Setting `state: directory` ensures the directory path exists with specified ownership and mode."
                },
                {
                    "type": "true_false",
                    "question": "To create a symbolic link with the file module, 'src' specifies the existing target file and 'dest' specifies the symlink path.",
                    "correct": True,
                    "explanation": "For `state: link`, `src` is the file to point to and `dest` (or `path`) is the symbolic link location."
                },
                {
                    "type": "mcq",
                    "question": "Which parameter in the copy module allows you to write raw text directly into a remote file without a local source file?",
                    "options": ["content", "text", "body", "inline"],
                    "correct": "content",
                    "explanation": "`content: 'Hello World'` writes string data directly to the destination file."
                },
                {
                    "type": "mcq",
                    "question": "What is the behavior of 'state: touch' in the file module if the target file already exists?",
                    "options": [
                        "It updates the access and modification times (mtime/atime) without altering content",
                        "It overwrites the file and truncates it to 0 bytes",
                        "It raises an error that the file exists",
                        "It creates a duplicate file with suffix .1"
                    ],
                    "correct": "It updates the access and modification times (mtime/atime) without altering content",
                    "explanation": "Like the Linux `touch` command, it creates an empty file if missing or updates timestamps if present."
                },
                {
                    "type": "true_false",
                    "question": "The 'fetch' module works in the opposite direction of 'copy' by retrieving files from remote hosts to the control node.",
                    "correct": True,
                    "explanation": "`fetch` copies files from remote targets to the control machine."
                },
                {
                    "type": "mcq",
                    "question": "In the lineinfile module, what happens if no line matches the 'regexp' parameter?",
                    "options": [
                        "The specified 'line' is appended to the end of the file by default",
                        "The task fails with a regular expression error",
                        "Ansible deletes the target file",
                        "Nothing happens and the file is unchanged"
                    ],
                    "correct": "The specified 'line' is appended to the end of the file by default",
                    "explanation": "If no line matches regexp, lineinfile appends the line to the end of the file (unless insertbefore/insertafter specifies otherwise)."
                },
                {
                    "type": "mcq",
                    "question": "Which parameter in the file module applies permission changes recursively to all child directories and files?",
                    "options": ["recurse: yes", "recursive: true", "all: yes", "depth: max"],
                    "correct": "recurse: yes",
                    "explanation": "The file module uses `recurse: yes` for recursive directory operations."
                },
                {
                    "type": "true_false",
                    "question": "If you copy a file using the 'copy' module and the destination file already has identical contents and hash, 'changed' will be false.",
                    "correct": True,
                    "explanation": "The copy module compares MD5/SHA256 checksums; if the remote file matches, it skips transfer and reports changed: false."
                },
                {
                    "type": "mcq",
                    "question": "What format is required when providing a checksum to the 'get_url' module?",
                    "options": ["<algorithm>:<hash> (e.g. sha256:abcd123...)", "Raw hex string only", "URL to checksum file only", "MD5 integer"],
                    "correct": "<algorithm>:<hash> (e.g. sha256:abcd123...)",
                    "explanation": "The checksum parameter expects `<algorithm>:<checksum_val>` or `<algorithm>:<checksum_url>`."
                },
                {
                    "type": "true_false",
                    "question": "The copy module automatically creates missing parent directories for the destination path if they do not exist.",
                    "correct": False,
                    "explanation": "If the parent directory of `dest` does not exist, the copy task will fail. You should create parent directories using the `file` module first."
                },
                {
                    "type": "mcq",
                    "question": "How can you remove a line from a file using lineinfile?",
                    "options": ["Set 'state: absent' with the matching regexp", "Set 'line: \"\"'", "Use line: null", "Use action: delete"],
                    "correct": "Set 'state: absent' with the matching regexp",
                    "explanation": "`state: absent` combined with `regexp` deletes all matching lines from the target file."
                },
                {
                    "type": "mcq",
                    "question": "What module is recommended for multi-line block insertions with start/end marker comments?",
                    "options": ["ansible.builtin.blockinfile", "ansible.builtin.lineinfile", "ansible.builtin.file", "ansible.builtin.append"],
                    "correct": "ansible.builtin.blockinfile",
                    "explanation": "`blockinfile` manages multi-line blocks bounded by marker comments (`# BEGIN ANSIBLE MANAGED BLOCK`)."
                },
                {
                    "type": "true_false",
                    "question": "Both the copy module and the get_url module can enforce ownership (owner) and group permissions on the target file.",
                    "correct": True,
                    "explanation": "Both modules accept `owner`, `group`, and `mode` parameters."
                },
                {
                    "type": "mcq",
                    "question": "When deploying files from Jinja2 templates containing dynamic variables, which module should be used instead of 'copy'?",
                    "options": ["ansible.builtin.template", "ansible.builtin.file", "ansible.builtin.jinja", "ansible.builtin.get_url"],
                    "correct": "ansible.builtin.template",
                    "explanation": "The `template` module parses `.j2` templates with Jinja2 variable substitution on the control node before copying."
                }
            ]
        }
    },
    {
        "slug": "06-system-and-service-modules",
        "title": "06. System, Package, and Service Modules",
        "estimated_time": 9,
        "has_hands_on": False,
        "content": """## System, Package, and Service Modules

Managing system packages, OS daemons/services, and user accounts are the most common administrative tasks in DevOps automation.

---

### 1. The `apt` Module (`ansible.builtin.apt`)

Manages packages on Debian and Ubuntu systems.

```yaml
- name: Install Nginx web server
  ansible.builtin.apt:
    name: nginx
    state: present
    update_cache: yes
    cache_valid_time: 3600
  become: yes
```

#### Package States:
- `present`: Ensures the package is installed (if already installed, makes no changes).
- `latest`: Upgrades the package to the newest version available in repositories.
- `absent`: Removes the package.
- `build-dep`: Installs build dependencies for the specified package.

#### Critical Parameters:
- `update_cache: yes`: Runs `apt-get update` before attempting installation.
- `cache_valid_time: 3600`: Only updates the apt cache if it is older than the specified seconds (avoids running slow `apt update` every single run).
- `autoremove: yes`: Cleans up unneeded package dependencies (`apt autoremove`).
- `purge: yes`: When removing (`state: absent`), purges config files as well.

---

### 2. The `service` and `systemd` Modules

Manages system daemons and services on remote hosts.

```yaml
- name: Ensure Nginx is running and enabled on boot
  ansible.builtin.service:
    name: nginx
    state: started
    enabled: yes
  become: yes
```

#### Service States:
- `started`: Ensures the service is currently running.
- `stopped`: Ensures the service is stopped.
- `restarted`: Unconditionally restarts the service (always reports `changed: true`).
- `reloaded`: Sends SIGHUP / reload signal to reread configuration without dropping connections.

#### Boot Enablement:
- `enabled: yes`: Service starts automatically at boot (`systemctl enable`).
- `enabled: no`: Service does not start at boot (`systemctl disable`).

> **systemd vs service:**  
> Use `ansible.builtin.service` for general, cross-platform playbooks.  
> Use `ansible.builtin.systemd` when you need specific systemd capabilities like `daemon_reload: yes` or managing user services.

---

### 3. The `user` Module (`ansible.builtin.user`)

Manages user accounts and group memberships.

```yaml
- name: Create deploy user with specific shell and groups
  ansible.builtin.user:
    name: deployer
    state: present
    shell: /bin/bash
    groups: sudo,docker
    append: yes
    create_home: yes
  become: yes
```

#### Critical Parameters:
- `name`: Username.
- `state`: `present` (create/update) or `absent` (delete).
- `groups`: Comma-separated list of secondary groups.
- **`append: yes`**: **CRITICAL!** If `append: yes` is omitted, the user will be removed from all secondary groups not explicitly listed!
- `shell`: Login shell (e.g. `/bin/bash` or `/sbin/nologin` for system service users).
- `create_home: yes`: Creates the home directory if missing.
- `remove: yes`: When used with `state: absent`, deletes the user's home directory and mail spool.

---

### Privilege Escalation: `become`

System modifications (installing packages, modifying services, creating users) require root privileges.

- In playbooks:
  ```yaml
  - name: Install Apache
    ansible.builtin.apt:
      name: apache2
      state: present
    become: yes
  ```
- In ad-hoc commands:
  ```bash
  ansible all -m apt -a "name=curl state=present" -b
  ```
""",
        "quiz": {
            "passing_score": 70,
            "questions": [
                {
                    "type": "mcq",
                    "question": "What is the difference between 'state: present' and 'state: latest' in package manager modules like apt or dnf?",
                    "options": [
                        "'present' ensures the package is installed without upgrading; 'latest' upgrades it to the newest available repository version",
                        "'latest' only works on beta packages",
                        "'present' installs packages from source code; 'latest' uses binary packages",
                        "There is no difference; both are synonyms"
                    ],
                    "correct": "'present' ensures the package is installed without upgrading; 'latest' upgrades it to the newest available repository version",
                    "explanation": "'present' is satisfied if any version is currently installed; 'latest' forces an upgrade if a newer version exists."
                },
                {
                    "type": "mcq",
                    "question": "In the user module, what critical risk occurs if you specify 'groups: docker' without setting 'append: yes'?",
                    "options": [
                        "The user will be removed from all other existing secondary groups (such as sudo or adm)",
                        "The user account will be locked immediately",
                        "The user's home directory will be deleted",
                        "The task will throw a syntax validation error"
                    ],
                    "correct": "The user will be removed from all other existing secondary groups (such as sudo or adm)",
                    "explanation": "By default, `groups` replaces the user's secondary group membership unless `append: yes` is explicitly set."
                },
                {
                    "type": "mcq",
                    "question": "What does the 'enabled: yes' parameter configure in the service module?",
                    "options": [
                        "Ensures the service is configured to start automatically at system boot",
                        "Starts the service immediately in the current session",
                        "Enables debugging logs for the daemon",
                        "Allows any unprivileged user to start and stop the service"
                    ],
                    "correct": "Ensures the service is configured to start automatically at system boot",
                    "explanation": "'enabled: yes' runs the equivalent of `systemctl enable <service>` for persistence across reboots."
                },
                {
                    "type": "true_false",
                    "question": "Setting 'state: restarted' on a service task will always report 'changed: true' every time it runs.",
                    "correct": True,
                    "explanation": "Because a restart forces an immediate process bounce, Ansible cannot make it idempotent and always marks changed: true."
                },
                {
                    "type": "mcq",
                    "question": "How can you prevent the 'apt' module from running a slow 'apt-get update' on every single playbook run?",
                    "options": [
                        "Set 'cache_valid_time: 3600' (or another duration in seconds)",
                        "Set 'update_cache: never'",
                        "Disable the apt module in ansible.cfg",
                        "Remove the sources.list file"
                    ],
                    "correct": "Set 'cache_valid_time: 3600' (or another duration in seconds)",
                    "explanation": "'cache_valid_time' instructs Ansible to skip updating the cache if it was updated within that time window."
                },
                {
                    "type": "mcq",
                    "question": "Which service state sends a SIGHUP or reload signal to reread configuration files without closing active connections?",
                    "options": ["reloaded", "restarted", "started", "refreshed"],
                    "correct": "reloaded",
                    "explanation": "'state: reloaded' reloads configuration without stopping or dropping active network connections."
                },
                {
                    "type": "true_false",
                    "question": "Privilege escalation with 'become: yes' can be defined at the play level, task level, or block level.",
                    "correct": True,
                    "explanation": "You can declare `become: yes` globally for the entire play or selectively on specific tasks."
                },
                {
                    "type": "mcq",
                    "question": "What parameter in the user module ensures that a service account cannot be used for interactive shell logins?",
                    "options": ["shell: /sbin/nologin (or /bin/false)", "login: disabled", "state: service", "interactive: no"],
                    "correct": "shell: /sbin/nologin (or /bin/false)",
                    "explanation": "Setting the shell to `/sbin/nologin` or `/bin/false` prevents terminal login for system users."
                },
                {
                    "type": "mcq",
                    "question": "When deleting a user with 'state: absent', how do you ensure their home directory is also removed from the disk?",
                    "options": ["remove: yes", "delete_home: true", "purge: yes", "force: true"],
                    "correct": "remove: yes",
                    "explanation": "The user module uses `remove: yes` to delete the user's home directory and mail spool when removing an account."
                },
                {
                    "type": "true_false",
                    "question": "Installing a package on Ubuntu using 'ansible.builtin.apt' requires administrative privileges (become: yes).",
                    "correct": True,
                    "explanation": "Installing system packages requires root permissions."
                },
                {
                    "type": "mcq",
                    "question": "Which parameter in the apt module removes configuration files alongside package binaries when deleting a package?",
                    "options": ["purge: yes", "clean: yes", "autoremove: yes", "force: yes"],
                    "correct": "purge: yes",
                    "explanation": "`purge: yes` (equivalent to `apt-get purge`) removes configuration files as well."
                },
                {
                    "type": "mcq",
                    "question": "What parameter in the 'systemd' module is used to reload the systemd manager configuration after editing unit files?",
                    "options": ["daemon_reload: yes", "reload_systemd: true", "refresh_units: yes", "systemctl_daemon: reload"],
                    "correct": "daemon_reload: yes",
                    "explanation": "`daemon_reload: yes` runs `systemctl daemon-reload` to pick up newly created or edited unit files."
                },
                {
                    "type": "true_false",
                    "question": "The generic 'service' module automatically works across systems using systemd, SysV init, OpenRC, or Upstart.",
                    "correct": True,
                    "explanation": "The generic `service` module detects the underlying init system and delegates commands accordingly."
                },
                {
                    "type": "mcq",
                    "question": "What parameter in the user module sets the user's numeric User ID (UID)?",
                    "options": ["uid", "user_id", "id", "numeric_uid"],
                    "correct": "uid",
                    "explanation": "The `uid` parameter assigns a specific numeric user ID to the account."
                },
                {
                    "type": "mcq",
                    "question": "How can you install multiple packages in a single task using the apt module?",
                    "options": [
                        "Pass a YAML list of package names to the 'name' parameter",
                        "Run the apt module multiple times in parallel threads",
                        "Separate package names with semicolons in a single string",
                        "The apt module can only install one package per task"
                    ],
                    "correct": "Pass a YAML list of package names to the 'name' parameter",
                    "explanation": "`name: [nginx, curl, git]` installs all listed packages in a single batch transaction."
                },
                {
                    "type": "true_false",
                    "question": "If a service is already running, executing a task with 'state: started' will report 'changed: false'.",
                    "correct": True,
                    "explanation": "Because the service is already in the requested state (started), no action is taken (idempotent)."
                },
                {
                    "type": "mcq",
                    "question": "What parameter in the user module specifies the primary group for a user?",
                    "options": ["group", "primary_group", "main_group", "gid"],
                    "correct": "group",
                    "explanation": "`group` sets the primary group, while `groups` sets secondary/supplementary groups."
                },
                {
                    "type": "true_false",
                    "question": "Setting 'update_cache: yes' without specifying a package 'name' in the apt module will run 'apt-get update' alone.",
                    "correct": True,
                    "explanation": "You can refresh repository indices without installing any packages by omitting `name`."
                },
                {
                    "type": "mcq",
                    "question": "What is the equivalent module for 'apt' on Red Hat Enterprise Linux and Fedora systems?",
                    "options": ["dnf (or yum)", "zypper", "apk", "pacman"],
                    "correct": "dnf (or yum)",
                    "explanation": "`ansible.builtin.dnf` (and legacy `yum`) manages packages on RHEL, CentOS, Rocky, and Fedora."
                },
                {
                    "type": "mcq",
                    "question": "How do you specify which user to become when privilege escalation is active (defaults to root)?",
                    "options": ["become_user: <username>", "sudo_user: <username>", "as_user: <username>", "run_as: <username>"],
                    "correct": "become_user: <username>",
                    "explanation": "`become_user` defines the target user for privilege escalation (e.g. `become_user: postgres`)."
                }
            ]
        }
    }
]

# Write chunks and quizzes
module_chunk_entries = []
for ch in CHUNKS:
    slug = ch["slug"]
    title = ch["title"]
    est_time = ch["estimated_time"]
    has_ho = ch["has_hands_on"]
    content = ch["content"]
    quiz = ch["quiz"]
    
    # 1. Write markdown
    md_content = f"""---
title: "{title}"
slug: "{slug}"
estimated_time: {est_time}
has_hands_on: {str(has_ho).lower()}
---

{content}
"""
    with open(PROC_MOD_DIR / f"{slug}.md", "w", encoding="utf-8") as f:
        f.write(md_content)
        
    # 2. Write quiz
    with open(PROC_MOD_DIR / f"{slug}.quiz.yaml", "w", encoding="utf-8") as f:
        yaml.dump(quiz, f, sort_keys=False, default_flow_style=False)
        
    module_chunk_entries.append({
        "slug": slug,
        "title": title,
        "file": f"{slug}.md",
        "estimated_time": est_time,
        "has_hands_on": has_ho
    })

# Write _module.yaml
mod_meta = {
    "name": "Commands & Modules",
    "slug": "003-modules",
    "description": "Master Ansible modules: core execution mechanics, ping internals, ansible-doc, command vs shell vs raw, and essential file & system modules.",
    "display_order": 3,
    "chunks": module_chunk_entries
}

with open(PROC_MOD_DIR / "_module.yaml", "w", encoding="utf-8") as f:
    yaml.dump(mod_meta, f, sort_keys=False, default_flow_style=False)

print(f"✅ Successfully built 003-modules with {len(CHUNKS)} chunks and {sum(len(c['quiz']['questions']) for c in CHUNKS)} questions!")
