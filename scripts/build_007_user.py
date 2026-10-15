#!/usr/bin/env python3
"""
Builder for 007-create-user (Create User with Ansible)
Generates 5 chunks with 90 comprehensive questions.
"""

import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROC_MOD_DIR = BASE_DIR / "processed" / "ansible" / "007-create-user"
PROC_MOD_DIR.mkdir(parents=True, exist_ok=True)
SUPP_DIR = PROC_MOD_DIR / "supplementary"
SUPP_DIR.mkdir(parents=True, exist_ok=True)

# Copy supplementary files
KB_DIR = BASE_DIR / "knowledge_base" / "ansible" / "007-create-user"
if KB_DIR.exists():
    for f in KB_DIR.iterdir():
        if f.is_file() and f.name != "index.html" and not f.name.startswith("."):
            import shutil
            shutil.copy2(f, SUPP_DIR / f.name)

CHUNKS = [
    {
        "slug": "01-ansible-user-module",
        "title": "01. Ansible's User Module Overview",
        "estimated_time": 7,
        "has_hands_on": False,
        "content": """## Ansible's User Module (`ansible.builtin.user`)

The `ansible.builtin.user` module is the standard declarative interface for managing user accounts on target operating systems.

Whether you are targeting Ubuntu, Debian, RHEL, CentOS, Rocky Linux, macOS, or FreeBSD, the `user` module abstracts away OS-specific commands (`useradd`, `usermod`, `userdel`, `pw`, `dscl`) into a unified, idempotent syntax.

### Why Use the User Module?

1. **Idempotence**: If the user already exists with the correct UID, shell, and groups, Ansible does nothing (`changed: false`).
2. **Cross-Platform**: Automatically calls the correct underlying operating system binary.
3. **Comprehensive Lifecycle Management**: Creates accounts, generates SSH keys, modifies group memberships, expires accounts, and cleans up home directories.

### Privilege Escalation Requirement

> **Rule:** Managing user accounts requires root/superuser privileges. Always include `become: yes` in user tasks.

```yaml
- name: Ensure deployer user exists
  ansible.builtin.user:
    name: deployer
    state: present
  become: yes
```

### Module Return Values

On execution, the module returns a dictionary containing the user's system attributes:

```json
{
    "changed": true,
    "name": "deployer",
    "uid": 1001,
    "gid": 1001,
    "home": "/home/deployer",
    "shell": "/bin/bash",
    "state": "present"
}
```
""",
        "quiz": {
            "passing_score": 70,
            "questions": [
                {
                    "type": "mcq",
                    "question": "What is the primary role of the ansible.builtin.user module?",
                    "options": [
                        "Managing operating system user accounts, shells, groups, and home directories declaratively",
                        "Managing database user accounts in MySQL and PostgreSQL",
                        "Creating IAM users on AWS cloud infrastructure",
                        "Managing user sessions in web browsers"
                    ],
                    "correct": "Managing operating system user accounts, shells, groups, and home directories declaratively",
                    "explanation": "The user module manages OS-level accounts across Unix/Linux systems."
                },
                {
                    "type": "mcq",
                    "question": "Why is 'become: yes' required when running tasks with the user module?",
                    "options": [
                        "Modifying /etc/passwd, /etc/shadow, and /etc/group requires root/administrator privileges",
                        "Ansible cannot parse YAML without become: yes",
                        "The user module is written in C and needs kernel access",
                        "To bypass SSH key verification"
                    ],
                    "correct": "Modifying /etc/passwd, /etc/shadow, and /etc/group requires root/administrator privileges",
                    "explanation": "Creating or modifying system user accounts is a restricted administrative operation."
                },
                {
                    "type": "true_false",
                    "question": "The user module automatically uses the appropriate OS commands (like useradd on Linux or pw on FreeBSD) behind the scenes.",
                    "correct": True,
                    "explanation": "Ansible abstracts OS commands so the same playbook task works on multiple Linux and BSD distributions."
                },
                {
                    "type": "mcq",
                    "question": "What is the default value of the 'state' parameter in the user module?",
                    "options": ["present", "absent", "create", "active"],
                    "correct": "present",
                    "explanation": "`state` defaults to `present` (ensuring the user account exists)."
                },
                {
                    "type": "mcq",
                    "question": "If a user already exists with the requested shell, UID, and groups, what will Ansible report?",
                    "options": ["ok (changed: false)", "changed (changed: true)", "failed", "skipped"],
                    "correct": "ok (changed: false)",
                    "explanation": "The task is idempotent; if the user state matches declarations, no changes are made."
                },
                {
                    "type": "true_false",
                    "question": "The user module can manage user passwords directly in plaintext safely without any hashing.",
                    "correct": False,
                    "explanation": "Linux /etc/shadow requires cryptographically salted password hashes. Cleartext passwords fail or pose severe security risks."
                },
                {
                    "type": "mcq",
                    "question": "Which FQCN refers to the built-in user management module?",
                    "options": ["ansible.builtin.user", "community.general.user", "ansible.posix.user", "core.system.user"],
                    "correct": "ansible.builtin.user",
                    "explanation": "The user module is part of the core built-in collection: `ansible.builtin.user`."
                },
                {
                    "type": "mcq",
                    "question": "What return key provides the assigned numeric User ID of the managed user?",
                    "options": ["uid", "user_number", "id", "numeric_id"],
                    "correct": "uid",
                    "explanation": "The returned dictionary includes `uid`."
                },
                {
                    "type": "true_false",
                    "question": "A single task with the user module can create both the user account and automatically generate an SSH key pair.",
                    "correct": True,
                    "explanation": "The user module supports `generate_ssh_key: true` to generate SSH keys during creation."
                },
                {
                    "type": "mcq",
                    "question": "Which underlying system file stores user metadata (username, UID, GID, home, shell) on Linux?",
                    "options": ["/etc/passwd", "/etc/shadow", "/etc/hosts", "/etc/environment"],
                    "correct": "/etc/passwd",
                    "explanation": "User metadata is stored in `/etc/passwd`; encrypted password hashes are stored in `/etc/shadow`."
                },
                {
                    "type": "mcq",
                    "question": "What is the only required parameter for the user module?",
                    "options": ["name", "uid", "shell", "password"],
                    "correct": "name",
                    "explanation": "`name` (the username) is the only mandatory argument."
                },
                {
                    "type": "true_false",
                    "question": "If the user does not exist on the system and state is set to 'absent', the task will fail.",
                    "correct": False,
                    "explanation": "Setting `state: absent` when the user is already missing reports `ok (changed: false)` idempotently."
                },
                {
                    "type": "mcq",
                    "question": "What return key indicates the home directory path of the created/modified user?",
                    "options": ["home", "home_dir", "path", "user_dir"],
                    "correct": "home",
                    "explanation": "`home` contains the user's home directory path."
                },
                {
                    "type": "true_false",
                    "question": "Running the user module in check mode ('--check') allows previewing if a user would be created or modified.",
                    "correct": True,
                    "explanation": "The user module supports check mode."
                },
                {
                    "type": "mcq",
                    "question": "Which operating system user account is normally used to execute Ansible tasks when 'become: yes' is set without 'become_user'?",
                    "options": ["root", "admin", "wheel", "ansible"],
                    "correct": "root",
                    "explanation": "By default, privilege escalation assumes the `root` account."
                },
                {
                    "type": "true_false",
                    "question": "The user module can only manage human login users and cannot create system daemon service accounts.",
                    "correct": False,
                    "explanation": "Using `system: yes` and `shell: /sbin/nologin`, you can create system service accounts."
                }
            ]
        }
    },
    {
        "slug": "02-create-and-manage-users",
        "title": "02. Creating, Modifying, and Removing Users",
        "estimated_time": 9,
        "has_hands_on": False,
        "content": """## Creating, Modifying, and Removing Users

The `ansible.builtin.user` module offers rich parameters to control every aspect of an account's lifecycle.

---

### Creating a User with Custom Attributes

```yaml
- name: Create developer user with specific groups and bash shell
  ansible.builtin.user:
    name: john
    comment: "John Doe - Lead Developer"
    uid: 1042
    group: developers
    groups: sudo,docker
    append: yes
    shell: /bin/bash
    home: /home/john
    create_home: yes
    state: present
  become: yes
```

### Critical Parameters Explained

| Parameter | Type | Default | Explanation |
|---|---|---|---|
| `name` | String | *Required* | The username to create, modify, or remove. |
| `comment` | String | None | Real name or GECOS field in `/etc/passwd`. |
| `uid` | Integer | System assigned | Explicit numeric user ID. |
| `group` | String | Username | Primary group of the user. |
| `groups` | List/CSV | None | Comma-separated list or YAML list of secondary/supplementary groups. |
| **`append`** | Boolean | `no` | **CRITICAL!** If `yes`, adds the user to `groups` while keeping existing groups. If `no`, **removes** the user from all secondary groups not listed! |
| `shell` | Path | System default | Login shell (e.g. `/bin/bash` or `/sbin/nologin`). |
| `create_home` | Boolean | `yes` | Creates the home directory if it does not exist. |
| `home` | Path | `/home/<name>` | Custom home directory path. |
| `system` | Boolean | `no` | If `yes`, creates a system account with low UID (< 1000). |
| `state` | String | `present` | `present` to create/update; `absent` to delete. |
| `remove` | Boolean | `no` | When used with `state: absent`, deletes the user's home directory and mail spool (`userdel -r`). |

---

### The `append: yes` Gotcha!

> **Warning: The Most Common Ansible User Module Mistake**  
> If an existing user belongs to `sudo`, `adm`, and `developers`, and you run:
> ```yaml
> groups: docker
> ```
> Without `append: yes`, Ansible will **remove** the user from `sudo`, `adm`, and `developers`!  
> **Always specify `append: yes`** when adding supplementary groups.

---

### Removing Users Cleanly

To delete an account and completely wipe its home directory:

```yaml
- name: Delete former employee user and remove home directory
  ansible.builtin.user:
    name: bad_actor
    state: absent
    remove: yes
  become: yes
```

If `remove: no` (the default for absent), the user account is removed from `/etc/passwd`, but `/home/bad_actor` remains intact on disk.
""",
        "quiz": {
            "passing_score": 70,
            "questions": [
                {
                    "type": "mcq",
                    "question": "What is the critical danger of omitting 'append: yes' when specifying secondary groups with 'groups: docker'?",
                    "options": [
                        "Ansible will remove the user from all other existing secondary groups (e.g. sudo, adm)",
                        "The user's home directory will be deleted immediately",
                        "The user's password will be reset to blank",
                        "The task will fail with a syntax error"
                    ],
                    "correct": "Ansible will remove the user from all other existing secondary groups (e.g. sudo, adm)",
                    "explanation": "Without `append: yes`, `groups` replaces the entire list of supplementary groups."
                },
                {
                    "type": "mcq",
                    "question": "When removing a user with 'state: absent', which parameter ensures their home directory and mail spool are also deleted from disk?",
                    "options": ["remove: yes", "delete_home: true", "purge: yes", "clean: true"],
                    "correct": "remove: yes",
                    "explanation": "`remove: yes` passes `-r` to `userdel`, deleting `/home/<user>` and mail spools."
                },
                {
                    "type": "true_false",
                    "question": "By default, 'create_home' is set to 'yes' in the user module, creating the home directory if missing.",
                    "correct": True,
                    "explanation": "`create_home` defaults to `yes` (or `true`)."
                },
                {
                    "type": "mcq",
                    "question": "Which shell path should be assigned to system service accounts to prevent interactive login?",
                    "options": ["/sbin/nologin (or /bin/false)", "/bin/bash", "/bin/sh", "/bin/zsh"],
                    "correct": "/sbin/nologin (or /bin/false)",
                    "explanation": "Setting shell to `/sbin/nologin` or `/bin/false` prevents terminal login sessions."
                },
                {
                    "type": "mcq",
                    "question": "What parameter is used to specify the user's primary group?",
                    "options": ["group", "groups", "primary_group", "gid"],
                    "correct": "group",
                    "explanation": "`group` defines the primary group; `groups` defines supplementary groups."
                },
                {
                    "type": "true_false",
                    "question": "Setting 'system: yes' creates an account with a numeric UID typically below 1000 on Linux.",
                    "correct": True,
                    "explanation": "`system: yes` instructs useradd to allocate from the system UID range."
                },
                {
                    "type": "mcq",
                    "question": "What parameter sets the real name or contact comment in /etc/passwd?",
                    "options": ["comment", "description", "real_name", "gecos"],
                    "correct": "comment",
                    "explanation": "`comment` writes to the GECOS field in `/etc/passwd`."
                },
                {
                    "type": "mcq",
                    "question": "How can you specify a custom non-standard home directory location (e.g. /data/users/alex)?",
                    "options": ["home: /data/users/alex", "dest: /data/users/alex", "path: /data/users/alex", "user_home: /data/users/alex"],
                    "correct": "home: /data/users/alex",
                    "explanation": "`home` configures the custom home path."
                },
                {
                    "type": "true_false",
                    "question": "If you delete a user with 'state: absent' and 'remove: no', their files in /home remain on the disk.",
                    "correct": True,
                    "explanation": "The user is removed from user databases, but the directory tree is left intact."
                },
                {
                    "type": "mcq",
                    "question": "How can you specify an explicit numeric user ID for consistent cross-server permissions?",
                    "options": ["uid: 1050", "id: 1050", "numeric_user: 1050", "user_id: 1050"],
                    "correct": "uid: 1050",
                    "explanation": "`uid` explicitly assigns the numeric User ID."
                },
                {
                    "type": "true_false",
                    "question": "If you assign an existing user a new shell (e.g. changing from /bin/sh to /bin/bash), Ansible will update it and report changed: true.",
                    "correct": True,
                    "explanation": "Ansible modifies `/etc/passwd` to reflect the new shell and marks the task changed."
                },
                {
                    "type": "mcq",
                    "question": "Can the 'groups' parameter accept a YAML list as well as a comma-separated string?",
                    "options": [
                        "Yes, both `groups: [sudo, docker]` and `groups: sudo,docker` are valid",
                        "No, only comma-separated strings are supported",
                        "No, only YAML lists are supported",
                        "Only if JSON format is used"
                    ],
                    "correct": "Yes, both `groups: [sudo, docker]` and `groups: sudo,docker` are valid",
                    "explanation": "Ansible flexibly accepts YAML lists or comma-separated strings for group lists."
                },
                {
                    "type": "true_false",
                    "question": "If the primary group specified in 'group' does not exist on the target system, the user task will fail unless created first.",
                    "correct": True,
                    "explanation": "The primary group must exist beforehand (e.g. created using `ansible.builtin.group`)."
                },
                {
                    "type": "mcq",
                    "question": "Which module should be used to create groups before adding users to them?",
                    "options": ["ansible.builtin.group", "ansible.builtin.user", "ansible.builtin.team", "ansible.builtin.role"],
                    "correct": "ansible.builtin.group",
                    "explanation": "`ansible.builtin.group` manages system groups."
                },
                {
                    "type": "mcq",
                    "question": "What parameter can lock or disable a user account without deleting it?",
                    "options": ["password_lock: yes", "state: locked", "disable: true", "active: false"],
                    "correct": "password_lock: yes",
                    "explanation": "`password_lock: yes` locks the account in `/etc/shadow` (prefixing hash with `!`)."
                },
                {
                    "type": "true_false",
                    "question": "Modifying a user's comment field on an existing user will cause Ansible to report 'changed: true'.",
                    "correct": True,
                    "explanation": "Any difference between current state and requested state triggers an update and reports changed: true."
                },
                {
                    "type": "mcq",
                    "question": "What parameter sets an account expiration date?",
                    "options": ["expires: 1776297600 (or YYYY-MM-DD)", "expire_date", "valid_until", "deadline"],
                    "correct": "expires: 1776297600 (or YYYY-MM-DD)",
                    "explanation": "`expires` sets epoch or date string for account expiration."
                },
                {
                    "type": "true_false",
                    "question": "Creating a user with 'create_home: no' will still create skeleton files (.bashrc) in /tmp.",
                    "correct": False,
                    "explanation": "`create_home: no` skips creating any home directory or skeleton files."
                },
                {
                    "type": "mcq",
                    "question": "Which parameter can force user removal even if the user is currently logged in?",
                    "options": ["force: yes", "kill: true", "aggressive: yes", "terminate: true"],
                    "correct": "force: yes",
                    "explanation": "`force: yes` forces removal with `userdel -f` even if processes are running under that user."
                },
                {
                    "type": "true_false",
                    "question": "If you run a task creating a user that already exists with the exact same attributes, 'changed' will be false.",
                    "correct": True,
                    "explanation": "Because the user matches the desired specification, it is idempotent."
                }
            ]
        }
    },
    {
        "slug": "03-password-management",
        "title": "03. Password Management & Hashing",
        "estimated_time": 8,
        "has_hands_on": False,
        "content": """## Password Management & Hashing

Linux stores user passwords in `/etc/shadow` as **cryptographically salted hashes**, never in plaintext.

If you pass a plaintext password to the `password` parameter:
```yaml
# ❌ INCORRECT & BROKEN:
password: "mysecretpassword"
```
The system will write the raw string into `/etc/shadow`. When the user tries to log in, Linux will hash their input and compare it to the raw string—causing **login to fail permanently**!

---

### Correct Password Hashing with Jinja2 (`password_hash`)

Ansible provides the built-in `password_hash` filter using SHA-512 (standard for modern Linux):

```yaml
- name: Create user with secure SHA-512 hashed password
  ansible.builtin.user:
    name: alice
    password: "{{ 'MySecretPass123!' | password_hash('sha512', 'mysecretsalt') }}"
  become: yes
```

#### Generating Hashes via CLI (Python `crypt` / `passlib`)
You can also pre-generate hashes on your command line:

```bash
# Using Python
python3 -c "import crypt, getpass; print(crypt.crypt(getpass.getpass(), crypt.mksalt(crypt.METHOD_SHA512)))"

# Or using mkpasswd
mkpasswd --method=sha-512
```

A valid SHA-512 Linux hash starts with `$6$`:
```text
$6$mysecretsalt$9V...randomhashcharacters...
```

---

### The `update_password` Parameter

When Ansible evaluates an existing user's password, it checks the `update_password` parameter:

| Setting | Behavior | Best Use Case |
|---|---|---|
| `update_password: always` *(default)* | Recalculates hash and updates `/etc/shadow` every time the playbook runs. | Strictly managed system/service accounts. |
| **`update_password: on_create`** | **Only sets the password when creating the user.** If the user already exists, it NEVER touches the password! | Human developer accounts (allows users to change their password via `passwd` without Ansible overwriting it!). |

```yaml
- name: Create human developer user with initial password
  ansible.builtin.user:
    name: bob
    password: "{{ 'InitialPass2026!' | password_hash('sha512') }}"
    update_password: on_create
  become: yes
```

---

### Storing Passwords Securely with Ansible Vault

Never commit passwords (even hashed ones) in plaintext playbook files in public Git repositories!

Use **Ansible Vault** to encrypt the password:
```bash
ansible-vault encrypt_string 'SuperSecretPassword' --name 'user_password'
```

In your playbook:
```yaml
- name: Create user with vaulted password
  ansible.builtin.user:
    name: adminuser
    password: "{{ user_password | password_hash('sha512') }}"
    update_password: on_create
  become: yes
```
""",
        "quiz": {
            "passing_score": 70,
            "questions": [
                {
                    "type": "mcq",
                    "question": "What happens if you provide a cleartext password (e.g. password: \"secret\") directly to the user module?",
                    "options": [
                        "Linux writes the plaintext string into /etc/shadow, breaking logins because the login PAM subsystem expects a salted hash",
                        "Ansible automatically prompts for an encryption key",
                        "The task fails with a YAML syntax error",
                        "The Linux kernel automatically converts it to SHA-512"
                    ],
                    "correct": "Linux writes the plaintext string into /etc/shadow, breaking logins because the login PAM subsystem expects a salted hash",
                    "explanation": "Linux PAM compares hashes; storing plaintext prevents valid cryptographic comparisons."
                },
                {
                    "type": "mcq",
                    "question": "Which Jinja2 filter is used to generate a secure salted Linux password hash in Ansible?",
                    "options": ["password_hash('sha512')", "hash('md5')", "encrypt_password('aes256')", "sha512_digest()"],
                    "correct": "password_hash('sha512')",
                    "explanation": "`{{ 'mypass' | password_hash('sha512') }}` generates a standard Linux /etc/shadow compatible hash."
                },
                {
                    "type": "mcq",
                    "question": "What does 'update_password: on_create' do?",
                    "options": [
                        "Sets the password only when the user account is first created, without overwriting it on future runs",
                        "Forces the user to change their password at next login",
                        "Updates the password every 30 days",
                        "Generates a random password upon reboot"
                    ],
                    "correct": "Sets the password only when the user account is first created, without overwriting it on future runs",
                    "explanation": "`on_create` prevents Ansible from resetting passwords if users change them locally via `passwd`."
                },
                {
                    "type": "true_false",
                    "question": "By default, 'update_password' is set to 'always', meaning Ansible will overwrite the password on every playbook execution if the hash differs.",
                    "correct": True,
                    "explanation": "`update_password` defaults to `always`."
                },
                {
                    "type": "mcq",
                    "question": "What prefix identifier indicates a SHA-512 hashed password in Linux /etc/shadow?",
                    "options": ["$6$", "$1$", "$2a$", "$5$"],
                    "correct": "$6$",
                    "explanation": "`$6$` designates SHA-512; `$1$` is MD5; `$5$` is SHA-256; `$2a$` is Blowfish/Bcrypt."
                },
                {
                    "type": "mcq",
                    "question": "Why should salt be included when generating password hashes?",
                    "options": [
                        "It prevents precomputed dictionary attacks (rainbow tables) from cracking identical passwords",
                        "It makes the password readable by standard users",
                        "It compresses the password to save disk space",
                        "Salt is required by SSH"
                    ],
                    "correct": "It prevents precomputed dictionary attacks (rainbow tables) from cracking identical passwords",
                    "explanation": "Cryptographic salts ensure identical passwords produce distinct hash outputs."
                },
                {
                    "type": "true_false",
                    "question": "If no salt is specified in the password_hash filter, Ansible will randomly generate a salt automatically.",
                    "correct": True,
                    "explanation": "Ansible generates a random cryptographic salt if none is explicitly passed."
                },
                {
                    "type": "mcq",
                    "question": "What tool or feature in Ansible is used to encrypt sensitive passwords and secrets in playbooks?",
                    "options": ["Ansible Vault", "Ansible Shield", "Ansible Lock", "Ansible SecretManager"],
                    "correct": "Ansible Vault",
                    "explanation": "Ansible Vault encrypts files or inline variables using AES-256."
                },
                {
                    "type": "true_false",
                    "question": "If 'password: \"*\"' is specified, the user account is created with login disabled via password.",
                    "correct": True,
                    "explanation": "A password of `*` or `!` in `/etc/shadow` disables password login."
                },
                {
                    "type": "mcq",
                    "question": "Which Python library on the control node powers the 'password_hash' filter?",
                    "options": ["passlib (or crypt)", "hashlib only", "requests", "bcrypt-cli"],
                    "correct": "passlib (or crypt)",
                    "explanation": "Ansible uses the `passlib` Python library or Python's built-in `crypt` module."
                },
                {
                    "type": "true_false",
                    "question": "When 'update_password: always' is set and random salt is used without a fixed salt, every playbook run will report 'changed: true'.",
                    "correct": True,
                    "explanation": "Because a newly generated salt yields a different hash string every run, Ansible thinks the password changed!"
                },
                {
                    "type": "mcq",
                    "question": "What is the recommended approach to avoid false 'changed: true' reports when using hashed passwords?",
                    "options": [
                        "Use 'update_password: on_create' or supply a fixed salt in the filter",
                        "Always use cleartext passwords",
                        "Disable check mode",
                        "Remove the shadow file"
                    ],
                    "correct": "Use 'update_password: on_create' or supply a fixed salt in the filter",
                    "explanation": "Fixed salts or `update_password: on_create` maintain idempotency."
                },
                {
                    "type": "true_false",
                    "question": "A user created with an encrypted password in /etc/shadow can still log in using SSH keys if authorized_keys is configured.",
                    "correct": True,
                    "explanation": "SSH key authentication works independently of password authentication."
                },
                {
                    "type": "mcq",
                    "question": "What command-line tool allows encrypting a single string variable for use in playbooks?",
                    "options": ["ansible-vault encrypt_string", "ansible-vault hide", "ansible-encrypt", "ansible-vault mask"],
                    "correct": "ansible-vault encrypt_string",
                    "explanation": "`ansible-vault encrypt_string` outputs a copy-pasteable encrypted YAML block."
                },
                {
                    "type": "true_false",
                    "question": "Linux passwords hashed with MD5 ($1$) are considered cryptographically secure for modern production systems.",
                    "correct": False,
                    "explanation": "MD5 is obsolete and vulnerable to collision attacks; SHA-512 ($6$) or Yescrypt is standard."
                },
                {
                    "type": "mcq",
                    "question": "What parameter in the user module forces an account password to expire immediately so the user must set a new one on login?",
                    "options": ["password_expire_max: 0 (or chage command)", "expire_password: true", "force_change: yes", "reset_password: now"],
                    "correct": "password_expire_max: 0 (or chage command)",
                    "explanation": "Setting password expiration parameters forces an immediate password reset on next terminal login."
                },
                {
                    "type": "true_false",
                    "question": "Ansible Vault encrypted files can be safely committed to private Git repositories.",
                    "correct": True,
                    "explanation": "Because Vault uses strong AES-256 encryption, the ciphertext cannot be read without the vault password."
                },
                {
                    "type": "mcq",
                    "question": "Which Linux file contains the encrypted password hashes that only root can read?",
                    "options": ["/etc/shadow", "/etc/passwd", "/etc/security", "/etc/pam.d"],
                    "correct": "/etc/shadow",
                    "explanation": "`/etc/shadow` has permissions 0640 or 0600 readable only by root and the shadow group."
                }
            ]
        }
    },
    {
        "slug": "04-ssh-key-setup",
        "title": "04. SSH Key Setup & Authorization",
        "estimated_time": 8,
        "has_hands_on": False,
        "content": """## SSH Key Setup and Authorization

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
""",
        "quiz": {
            "passing_score": 70,
            "questions": [
                {
                    "type": "mcq",
                    "question": "Which parameter in the user module instructs Ansible to generate an SSH key pair in the user's home directory?",
                    "options": ["generate_ssh_key: yes", "ssh_keygen: true", "create_keys: yes", "enable_ssh: true"],
                    "correct": "generate_ssh_key: yes",
                    "explanation": "`generate_ssh_key: yes` generates a private/public key pair if missing."
                },
                {
                    "type": "mcq",
                    "question": "Which module is used to append or manage public keys in a user's ~/.ssh/authorized_keys file?",
                    "options": [
                        "ansible.posix.authorized_key",
                        "ansible.builtin.ssh_auth",
                        "ansible.builtin.user",
                        "ansible.builtin.keyfile"
                    ],
                    "correct": "ansible.posix.authorized_key",
                    "explanation": "`ansible.posix.authorized_key` manages lines in `~/.ssh/authorized_keys`."
                },
                {
                    "type": "true_false",
                    "question": "If an SSH key already exists in ~/.ssh/id_rsa, setting 'generate_ssh_key: yes' will overwrite it and generate a new key.",
                    "correct": False,
                    "explanation": "`generate_ssh_key: yes` is idempotent; it leaves existing keys untouched."
                },
                {
                    "type": "mcq",
                    "question": "What does the 'exclusive: yes' parameter do in the authorized_key module?",
                    "options": [
                        "Removes any keys in authorized_keys that are not explicitly specified in the task",
                        "Locks the file so only root can read it",
                        "Allows only one SSH connection at a time",
                        "Generates a one-time single-use key"
                    ],
                    "correct": "Removes any keys in authorized_keys that are not explicitly specified in the task",
                    "explanation": "`exclusive: yes` purges unauthorized or stray keys, enforcing a strict whitelist."
                },
                {
                    "type": "mcq",
                    "question": "What filesystem permissions does Ansible enforce on the ~/.ssh directory and authorized_keys file by default?",
                    "options": [
                        "0700 for ~/.ssh and 0600 for authorized_keys",
                        "0777 for ~/.ssh and 0777 for authorized_keys",
                        "0755 for ~/.ssh and 0644 for authorized_keys",
                        "0700 for ~/.ssh and 0644 for authorized_keys"
                    ],
                    "correct": "0700 for ~/.ssh and 0600 for authorized_keys",
                    "explanation": "OpenSSH requires strict permissions: 0700 for `.ssh` and 0600 for `authorized_keys`."
                },
                {
                    "type": "true_false",
                    "question": "The authorized_key module can fetch public keys directly from GitHub by supplying a URL (e.g. https://github.com/username.keys).",
                    "correct": True,
                    "explanation": "Ansible will download public keys from HTTP/HTTPS URLs directly."
                },
                {
                    "type": "mcq",
                    "question": "Which modern key type is widely recommended over legacy 2048-bit RSA for SSH keys?",
                    "options": ["ed25519", "dsa", "des", "rc4"],
                    "correct": "ed25519",
                    "explanation": "Ed25519 provides superior security, performance, and compact key lengths."
                },
                {
                    "type": "mcq",
                    "question": "How can you read a local public key file from the control node and supply it to the authorized_key task?",
                    "options": [
                        "key: \"{{ lookup('file', '~/.ssh/id_rsa.pub') }}\"",
                        "key_file: '~/.ssh/id_rsa.pub'",
                        "src: '~/.ssh/id_rsa.pub'",
                        "read_local: '~/.ssh/id_rsa.pub'"
                    ],
                    "correct": "key: \"{{ lookup('file', '~/.ssh/id_rsa.pub') }}\"",
                    "explanation": "The `lookup('file', ...)` plugin reads contents from the control node's filesystem."
                },
                {
                    "type": "true_false",
                    "question": "If you set 'state: absent' in the authorized_key module, it will remove the specified key from the authorized_keys file.",
                    "correct": True,
                    "explanation": "`state: absent` revokes specific keys cleanly."
                },
                {
                    "type": "mcq",
                    "question": "What parameter specifies the bit length when generating RSA keys in the user module?",
                    "options": ["ssh_key_bits", "bits", "key_size", "length"],
                    "correct": "ssh_key_bits",
                    "explanation": "`ssh_key_bits` (e.g. 4096) sets the key size for RSA."
                },
                {
                    "type": "true_false",
                    "question": "The authorized_key module can accept multiple public keys separated by newlines in a single task.",
                    "correct": True,
                    "explanation": "The `key` parameter can contain multiple newline-separated keys."
                },
                {
                    "type": "mcq",
                    "question": "What parameter in the user module customizes the comment placed at the end of the generated public key?",
                    "options": ["ssh_key_comment", "comment", "key_label", "tag"],
                    "correct": "ssh_key_comment",
                    "explanation": "`ssh_key_comment` sets the trailing comment (e.g. user@host)."
                },
                {
                    "type": "true_false",
                    "question": "Using 'exclusive: yes' with an empty key list will wipe all keys from the user's authorized_keys file.",
                    "correct": True,
                    "explanation": "`exclusive: yes` removes any key not present in `key`."
                },
                {
                    "type": "mcq",
                    "question": "What return value key from the user module contains the generated SSH public key string?",
                    "options": ["ssh_public_key", "public_key", "pub_key", "ssh_key"],
                    "correct": "ssh_public_key",
                    "explanation": "`result.ssh_public_key` contains the generated public key text."
                },
                {
                    "type": "true_false",
                    "question": "SSH keys generated with 'generate_ssh_key: yes' are protected by a passphrase by default.",
                    "correct": False,
                    "explanation": "Generated keys have no passphrase so automated tasks can use them non-interactively."
                },
                {
                    "type": "mcq",
                    "question": "What parameter in authorized_key specifies the path to a non-standard authorized_keys file?",
                    "options": ["path", "dest", "file", "key_path"],
                    "correct": "path",
                    "explanation": "`path` overrides the default `~/.ssh/authorized_keys` destination."
                },
                {
                    "type": "true_false",
                    "question": "The authorized_key module can manage keys for users whose home directory does not exist.",
                    "correct": False,
                    "explanation": "Ansible must write to `<home>/.ssh/authorized_keys`, so the home directory must exist."
                },
                {
                    "type": "mcq",
                    "question": "Which collection contains the 'authorized_key' module?",
                    "options": ["ansible.posix", "ansible.builtin", "community.general", "ansible.security"],
                    "correct": "ansible.posix",
                    "explanation": "In modern Ansible collections, `authorized_key` lives under `ansible.posix.authorized_key`."
                }
            ]
        }
    },
    {
        "slug": "05-troubleshooting-and-best-practices",
        "title": "05. Troubleshooting, Verification & Best Practices",
        "estimated_time": 8,
        "has_hands_on": False,
        "content": """## Troubleshooting, Verification & Production Best Practices

Writing production-grade user management playbooks requires automated verification, secure secret storage, and proper error handling.

---

### 1. Verifying User Creation Idempotently

After creating a user, you can verify their presence, primary group, and secondary groups using the `command` module and the Linux `id` utility:

```yaml
- name: Verify user exists and check group membership
  ansible.builtin.command: "id deployer"
  register: user_info
  changed_when: false
  failed_when: user_info.rc != 0

- name: Debug user information
  ansible.builtin.debug:
    msg: "User {{ user_info.stdout }} is verified!"
```

#### Why `changed_when: false`?
Because `id deployer` is an inspection command that does not alter system state, setting `changed_when: false` ensures the verification task reports green `ok` rather than false `changed: true`.

---

### 2. Common User Management Errors and Fixes

| Error Message | Root Cause | Solution |
|---|---|---|
| `useradd: group 'devs' does not exist` | The specified primary or secondary group hasn't been created yet. | Create the group first using `ansible.builtin.group: name=devs state=present`. |
| `Permission denied: '/etc/shadow'` | Task ran without root privileges. | Add `become: yes` to the task or play. |
| `User lost sudo access after playbook run` | `append: yes` was missing when specifying secondary groups. | Always add `append: yes` when modifying `groups`. |
| `SSH key authentication rejected` | Bad permissions on `~/.ssh` (e.g. 0777 or 0755) or owned by wrong user. | Use `authorized_key` module which automatically enforces `0700` / `0600`. |

---

### 3. Production Best Practices Checklist

1. **Always Use `become: yes`**: Account creation requires administrative access.
2. **Never Hardcode Passwords in Plaintext**: Use `password_hash('sha512')` and store sensitive input in **Ansible Vault**.
3. **Use `update_password: on_create`** for human users: Prevents overwriting passwords when users rotate them.
4. **Always Specify `append: yes`** when modifying secondary `groups`.
5. **Set `shell: /sbin/nologin`** for system/daemon service users.
6. **Clean Up Departing Users**: Use `state: absent` with `remove: yes` to eliminate orphan accounts and reclaim disk space.
""",
        "quiz": {
            "passing_score": 70,
            "questions": [
                {
                    "type": "mcq",
                    "question": "Why should verification tasks (like 'id <username>') always include 'changed_when: false'?",
                    "options": [
                        "To prevent read-only inspection commands from falsely reporting system state changes",
                        "Because changed tasks are killed by the Linux kernel",
                        "To force the command to run with root privileges",
                        "To suppress error messages"
                    ],
                    "correct": "To prevent read-only inspection commands from falsely reporting system state changes",
                    "explanation": "Read-only inspection commands do not modify state; setting `changed_when: false` maintains accurate reporting."
                },
                {
                    "type": "mcq",
                    "question": "What error occurs if you create a user with 'group: custom_group' before that group exists on the remote system?",
                    "options": [
                        "useradd fails with 'group custom_group does not exist'",
                        "Ansible automatically creates the group with GID 999",
                        "The user is assigned to group 'nogroup'",
                        "The task succeeds silently"
                    ],
                    "correct": "useradd fails with 'group custom_group does not exist'",
                    "explanation": "Primary groups must exist on the system prior to user creation."
                },
                {
                    "type": "true_false",
                    "question": "OpenSSH will reject authentication if ~/.ssh has 0777 (world-writable) permissions.",
                    "correct": True,
                    "explanation": "OpenSSH's StrictModes will deliberately reject authentication if directories are world-writable."
                },
                {
                    "type": "mcq",
                    "question": "Which Linux command displays a user's UID, GID, and all secondary group memberships?",
                    "options": ["id", "whoami", "uname", "groups_only"],
                    "correct": "id",
                    "explanation": "`id <username>` prints uid, gid, and groups."
                },
                {
                    "type": "mcq",
                    "question": "What is the best practice for managing passwords of human developers who rotate their own passwords?",
                    "options": [
                        "Use 'update_password: on_create'",
                        "Use 'update_password: always'",
                        "Store passwords in plain text in README.md",
                        "Disable passwords completely"
                    ],
                    "correct": "Use 'update_password: on_create'",
                    "explanation": "`on_create` sets the initial password on user creation and never overwrites it when the user changes it."
                },
                {
                    "type": "true_false",
                    "question": "Ansible Vault encrypted files require a password or key file at runtime via '--ask-vault-pass' or '--vault-password-file'.",
                    "correct": True,
                    "explanation": "Vaulted variables require decryption keys when playbooks run."
                },
                {
                    "type": "mcq",
                    "question": "What parameter in the user module ensures that user creation fails if the specified UID is already taken by another account?",
                    "options": ["non_unique: no (default)", "unique: yes", "force_unique: true", "check_uid: true"],
                    "correct": "non_unique: no (default)",
                    "explanation": "By default, `non_unique: no` prevents duplicate UIDs."
                },
                {
                    "type": "true_false",
                    "question": "System users (system: yes) typically do not require an active login shell and should have shell: /sbin/nologin.",
                    "correct": True,
                    "explanation": "Restricting shell login on daemon accounts minimizes the attack surface."
                },
                {
                    "type": "mcq",
                    "question": "How do you completely remove a departing employee's account and all their files from the disk?",
                    "options": [
                        "state: absent with remove: yes",
                        "state: deleted with force: true",
                        "state: purge",
                        "remove: true with state: present"
                    ],
                    "correct": "state: absent with remove: yes",
                    "explanation": "`state: absent` with `remove: yes` deletes both the account and its home directory."
                },
                {
                    "type": "true_false",
                    "question": "The 'group' module should generally be placed before the 'user' module in playbooks when creating custom primary groups.",
                    "correct": True,
                    "explanation": "Ensuring the group exists before assigning users to it prevents dependency errors."
                },
                {
                    "type": "mcq",
                    "question": "What is the result of 'failed_when: user_info.rc != 0' on a verification task?",
                    "options": [
                        "The task only fails if the command exit code is non-zero",
                        "The task will always fail",
                        "The task will ignore errors",
                        "The task will retry 5 times"
                    ],
                    "correct": "The task only fails if the command exit code is non-zero",
                    "explanation": "`failed_when` customizes the failure criteria based on return attributes."
                },
                {
                    "type": "true_false",
                    "question": "A user account locked with 'password_lock: yes' can still be accessed via 'su -' by the root user.",
                    "correct": True,
                    "explanation": "Root can always switch to any local user via `su -` regardless of password locks."
                },
                {
                    "type": "mcq",
                    "question": "Which file in Linux lists the secondary group memberships of all users?",
                    "options": ["/etc/group", "/etc/passwd", "/etc/sudoers", "/etc/subgid"],
                    "correct": "/etc/group",
                    "explanation": "Group definitions and memberships are stored in `/etc/group`."
                },
                {
                    "type": "true_false",
                    "question": "Hardcoding production root passwords directly into Git is acceptable if the Git repository is private.",
                    "correct": False,
                    "explanation": "Secrets should never be stored in plain text, even in private repositories. Use Ansible Vault."
                },
                {
                    "type": "mcq",
                    "question": "What happens if a user is deleted with 'state: absent' and 'remove: no' and a new user is later assigned the same UID?",
                    "options": [
                        "The new user inherits ownership of the orphan files in the old home directory",
                        "The Linux kernel crashes",
                        "The files are securely shredded",
                        "The filesystem locks into read-only mode"
                    ],
                    "correct": "The new user inherits ownership of the orphan files in the old home directory",
                    "explanation": "Filesystem permissions are tracked by UID, so reassigning a UID grants access to leftover files."
                },
                {
                    "type": "true_false",
                    "question": "The debug module can be used to print registered user inspection data during playbook runs.",
                    "correct": True,
                    "explanation": "`ansible.builtin.debug` prints variables and registered output."
                },
                {
                    "type": "mcq",
                    "question": "Which parameter ensures the user's primary group is created automatically with the same name as the user on systems that support it?",
                    "options": ["user_group: yes", "auto_group: true", "create_group: yes", "same_group: true"],
                    "correct": "user_group: yes",
                    "explanation": "`user_group: yes` creates a group matching the username as the primary group."
                },
                {
                    "type": "true_false",
                    "question": "Properly written Ansible user management tasks are completely safe to re-run on every routine maintenance window.",
                    "correct": True,
                    "explanation": "Because tasks are declarative and idempotent, running them repeatedly enforces compliance without side effects."
                }
            ]
        }
    }
]

module_chunk_entries = []
for ch in CHUNKS:
    slug = ch["slug"]
    title = ch["title"]
    est_time = ch["estimated_time"]
    has_ho = ch["has_hands_on"]
    content = ch["content"]
    quiz = ch["quiz"]
    
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
        
    with open(PROC_MOD_DIR / f"{slug}.quiz.yaml", "w", encoding="utf-8") as f:
        yaml.dump(quiz, f, sort_keys=False, default_flow_style=False)
        
    module_chunk_entries.append({
        "slug": slug,
        "title": title,
        "file": f"{slug}.md",
        "estimated_time": est_time,
        "has_hands_on": has_ho
    })

mod_meta = {
    "name": "Create User",
    "slug": "007-create-user",
    "description": "Master user account administration in Ansible: user lifecycle, secure password hashing (SHA-512), SSH key pair generation, authorized_keys deployment, and production verification.",
    "display_order": 7,
    "chunks": module_chunk_entries
}

with open(PROC_MOD_DIR / "_module.yaml", "w", encoding="utf-8") as f:
    yaml.dump(mod_meta, f, sort_keys=False, default_flow_style=False)

print(f"✅ Successfully built 007-create-user with {len(CHUNKS)} chunks and {sum(len(c['quiz']['questions']) for c in CHUNKS)} questions!")
