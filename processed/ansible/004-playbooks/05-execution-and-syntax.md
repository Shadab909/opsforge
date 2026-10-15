---
title: "05. Playbook Execution & Play Syntax"
slug: "05-execution-and-syntax"
estimated_time: 7
has_hands_on: false
---

## 06. Playbook execution
            

#### Running a Playbook
            
              

```bash
# Basic execution
ansible-playbook playbook.yaml

# With inventory file
ansible-playbook -i inventory playbook.yaml

# Limit to specific hosts
ansible-playbook playbook.yaml --limit webservers

# Check mode (dry run)
ansible-playbook playbook.yaml --check

# Show differences
ansible-playbook playbook.yaml --diff

# Verbose output
ansible-playbook playbook.yaml -v
ansible-playbook playbook.yaml -vv   # More verbose
ansible-playbook playbook.yaml -vvv  # Very verbose

```

            
            

#### Understanding Playbook Output
            
              

```text
PLAY [webservers] ****

TASK [Gathering Facts] ****
ok: [web1]
ok: [web2]

TASK [Install nginx] ****
changed: [web1]
changed: [web2]

PLAY RECAP ****
web1     : ok=2    changed=1    unreachable=0    failed=0    skipped=0
web2     : ok=2    changed=1    unreachable=0    failed=0    skipped=0

```

            
            

**Task Status:**
            

              
- **ok**: Task executed successfully, no changes made
              
- **changed**: Task executed and made changes
              
- **failed**: Task failed
              
- **skipped**: Task was skipped due to conditions
              
- **unreachable**: Host was unreachable
            

            
            

## 05. Playbook syntax
            

              
- In this section, we will learn further about playbook’s syntax.
            

            

#### `Play`
            

              
- [See
                  official documentation](https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html#play).
              
- The **top** part of the playbook is called `Play` and it
                **defines** the **global behavior** of for the **entire**
                playbook.
              
- Here are some definitions which are set in the `Play` section:
            

            
              

```yaml
---
- name: The name of the play
  # A list of groups, hosts or host pattern that translates into a list
  # of hosts that are the play’s target.
  hosts: localhost

  # Boolean that controls if privilege escalation is used or not on
  # Task execution.
  # Implemented by the become plugin
  become: yes

  # User that you ‘become’ after using privilege escalation.
  # The remote/login user must have permissions to become this user.
  become_user:

  # A dictionary that gets converted into environment vars to be provided
  # for the task upon execution.
  # This can ONLY be used with modules.
  # This is not supported for any other type of plugins nor Ansible itself
  # nor its configuration, it just sets the variables for the code responsible
  # for executing the task.
  # This is not a recommended way to pass in confidential data.
  environment:

  # Dictionary/map of variables
  vars:

```
