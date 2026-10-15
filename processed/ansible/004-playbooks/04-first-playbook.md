---
title: "04. Writing Your First Playbook"
slug: "04-first-playbook"
estimated_time: 6
has_hands_on: false
---

## 05. Our first playbook
            

#### Simple Example
            

              
- Here is our first playbook example that will list files in a given directory.
            

            
              

```yaml
---
# Run on all the hosts
- hosts: all

  # Here we define our tasks
  tasks:
    # This is the first task
    - name: List files in a directory
      # As learned before this is the command module
      # This command will list files in the home directory
      command: ls ~

      # register is used whenever we wish to save the output
      # In this case it will be saved to a variable named 'files'
      register: files

    # This is the second task
    # In this case the tasks will run in the declared sequence
    - name: Print the list of files
      # Using the builtin debug module
      # The debug will print out our files list
      # ** We need to use `stdout_lines` for that
      debug:
        msg: "{{ files.stdout_lines }}"

```

            
            

#### Writing Your First Playbook
            

**Step 1**: Start with the document marker
            
              

```yaml
---

```

            
            

**Step 2**: Define the play with target hosts
            
              

```yaml
---
- name: My first playbook
  hosts: localhost

```

            
            

**Step 3**: Add tasks
            
              

```yaml
---
- name: My first playbook
  hosts: localhost
  tasks:
    - name: Print a message
      debug:
        msg: "Hello, Ansible!"

```

            
            

**Step 4**: Run the playbook
            
              

```bash
ansible-playbook my-first-playbook.yaml

```

            
            

##### **It’s as simple as that!**
