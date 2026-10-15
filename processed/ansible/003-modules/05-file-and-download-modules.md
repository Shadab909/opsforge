---
title: "05. File Management & Download Modules"
slug: "05-file-and-download-modules"
estimated_time: 9
has_hands_on: false
---

## File Management & Download Modules

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
  content: "managed_by: ansible
env: production
"
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

