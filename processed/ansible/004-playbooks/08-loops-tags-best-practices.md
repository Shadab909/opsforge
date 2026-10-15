---
title: "08. Loops, Tags & Playbook Best Practices"
slug: "08-loops-tags-best-practices"
estimated_time: 8
has_hands_on: true
---

## 12. Loops
            

#### Using loop
            
              

```yaml
---
- name: Loop examples
  hosts: all
  tasks:
    - name: Install multiple packages
      apt:
        name: "{{ item }}"
        state: present
      loop:
        - nginx
        - git
        - curl
        - vim

    - name: Create multiple users
      user:
        name: "{{ item.name }}"
        state: present
        groups: "{{ item.groups }}"
      loop:
        - { name: "alice", groups: "admin,developers" }
        - { name: "bob", groups: "developers" }
        - { name: "charlie", groups: "users" }

```

            
            

#### Loop with dict
            
              

```yaml
tasks:
  - name: Set file permissions
    file:
      path: "{{ item.key }}"
      mode: "{{ item.value }}"
      state: touch
    loop: "{{ lookup('dict', file_permissions) }}"
    vars:
      file_permissions:
        /tmp/file1.txt: "0644"
        /tmp/file2.txt: "0600"
        /tmp/file3.txt: "0755"

```

            
            
            

## 13. Tags
            

#### Using Tags
            
              

```yaml
---
- name: Complete server setup
  hosts: all
  tasks:
    - name: Install packages
      apt:
        name: nginx
        state: present
      tags:
        - install
        - packages

    - name: Configure nginx
      copy:
        src: nginx.conf
        dest: /etc/nginx/nginx.conf
      tags:
        - config
        - nginx

    - name: Start nginx
      service:
        name: nginx
        state: started
      tags:
        - service
        - nginx

```

            
            

#### Running with Tags
            
              

```bash
# Run only tasks with 'install' tag
ansible-playbook playbook.yaml --tags install

# Run multiple tags
ansible-playbook playbook.yaml --tags "install,config"

# Skip tasks with specific tags
ansible-playbook playbook.yaml --skip-tags service

# List all tags
ansible-playbook playbook.yaml --list-tags

```

            
            
            

## 14. Playbook best practices
            

#### Naming Conventions
            

              
- Use descriptive play and task names
              
- Use consistent naming patterns
              
- Include verbs in task names
            

            
              

```bash
# ❌ Bad
- name: nginx
  apt:
    name: nginx

# ✅ Good
- name: Install nginx web server
  apt:
    name: nginx
    state: present

```

            
            

#### Organization
            
            

              
- Keep playbooks focused and modular
              
- Use roles for reusable content
              
- Separate variables into files
              
- Use inventory groups effectively
            

            

#### Security
            

              
- Use Ansible Vault for sensitive data
              
- Don’t hardcode credentials
              
- Use sudo/become only when necessary
              
- Validate user input
            

            

#### Testing
            

              
- Use `--check` mode for dry runs
              
- Test in non-production first
              
- Use `--diff` to see changes
              
- Implement proper error handling
            

            
            

## 15. Practical examples
            

#### Example 1: Complete Web Server Setup
            
              

```yaml
---
- name: Setup web server
  hosts: webservers
  become: yes
  vars:
    http_port: 80
    doc_root: /var/www/html

  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Create document root
      file:
        path: "{{ doc_root }}"
        state: directory
        mode: "0755"

    - name: Copy index page
      copy:
        content: "<h1>Welcome to {{ inventory_hostname }}</h1>"
        dest: "{{ doc_root }}/index.html"
      notify: restart nginx

    - name: Start and enable nginx
      service:
        name: nginx
        state: started
        enabled: yes

  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted

```

            
            

#### Example 2: System Updates and Maintenance
            
              

```yaml
---
- name: System maintenance
  hosts: all
  become: yes

  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
      when: ansible_os_family == "Debian"

    - name: Upgrade all packages
      apt:
        upgrade: dist
      when: ansible_os_family == "Debian"
      register: upgrade_result

    - name: Check if reboot required
      stat:
        path: /var/run/reboot-required
      register: reboot_required

    - name: Reboot if needed
      reboot:
        msg: "Rebooting for system updates"
        pre_reboot_delay: 10
      when: reboot_required.stat.exists

```
