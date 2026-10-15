---
title: "03. Password Management & Hashing"
slug: "03-password-management"
estimated_time: 8
has_hands_on: false
---

## Password Management & Hashing

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

