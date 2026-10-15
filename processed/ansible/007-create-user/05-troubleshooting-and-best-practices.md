---
title: "05. Troubleshooting, Verification & Best Practices"
slug: "05-troubleshooting-and-best-practices"
estimated_time: 8
has_hands_on: false
---

## Troubleshooting, Verification & Production Best Practices

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

