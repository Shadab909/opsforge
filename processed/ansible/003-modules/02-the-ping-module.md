---
title: "02. The Ping Module & Source Code"
slug: "02-the-ping-module"
estimated_time: 7
has_hands_on: false
---

## The Ping Module (`ansible.builtin.ping`)

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

