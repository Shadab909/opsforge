---
title: "06. Variables & Environment Configuration"
slug: "06-variables"
estimated_time: 7
has_hands_on: false
---

## 08. Variables in playbooks
            

#### Defining Variables
            
              

```yaml
---
- name: Variable examples
  hosts: all
  vars:
    # Simple variables
    http_port: 80
    app_name: myapp

    # List variables
    packages:
      - nginx
      - git
      - curl

    # Dictionary variables
    database:
      host: db.example.com
      port: 5432
      name: mydb

  tasks:
    - name: Use variables
      debug:
        msg: "App {{ app_name }} runs on port {{ http_port }}"

    - name: Access dictionary
      debug:
        msg: "Database: {{ database.host }}:{{ database.port }}"

```

            
            

#### Variable Sources
            

              
1. **Playbook vars**: Defined in playbook
              
2. **vars_files**: External YAML files
              
3. **Command line**: `-e "var=value"`
              
4. **Inventory**: Host/group variables
              
5. **Facts**: Gathered from systems
              
6. **Environment**: `lookup('env', 'VAR')`
            

            

#### Variable Precedence (lowest to highest)
            

Understanding variable precedence helps you control which values take priority when the same variable is
              defined in multiple places.
            

**Quick Reference:**
            

              
1. Role defaults
              
2. Inventory file/script variables
              
3. Playbook vars
              
4. vars_files
              
5. Host facts
              
6. Registered variables
              
7. Set_facts
              
8. Play vars_prompt
              
9. Play vars
              
10. Extra vars (`-e`)
            

            

**Detailed Examples:**
            

              
1. **Role defaults** (lowest priority)
            

            
              

```bash
# roles/myapp/defaults/main.yml
app_port: 8080
app_env: development

```

            
            

              
1. **Inventory file/script variables**
            

            
              

```bash
# inventory
[webservers]
web1 ansible_host=192.168.1.10 app_port=8081

[webservers:vars]
app_env=staging

```

            
            

              
1. **Playbook vars**
            

            
              

```yaml
---
- hosts: webservers
  vars:
    app_port: 8082
    app_env: production

```

            
            

              
1. **vars_files**
            

            
              

```yaml
# vars/production.yml
app_port: 8083
app_env: production

# playbook
- hosts: webservers
  vars_files:
    - vars/production.yml

```

            
            

              
1. **Host facts** (discovered automatically)
            

            
              

```yaml
tasks:
  - name: Use discovered facts
    debug:
      msg: "OS: {{ ansible_distribution }}"

```

            
            

              
1. **Registered variables**
            

            
              

```yaml
tasks:
  - name: Get timestamp
    command: date +%s
    register: current_time

  - name: Use registered var
    debug:
      msg: "Time: {{ current_time.stdout }}"

```

            
            

              
1. **Set_facts**
            

            
              

```yaml
tasks:
  - name: Set custom fact
    set_fact:
      app_port: 8084
      calculated_value: "{{ ansible_hostname }}_app"

```

            
            

              
1. **Play vars_prompt**
            

            
              

```yaml
---
- hosts: webservers
  vars_prompt:
    - name: app_port
      prompt: "Enter the application port"
      private: no

```

            
            

              
1. **Play vars**
            

            
              

```yaml
---
- hosts: webservers
  vars:
    app_port: 8085 # Higher priority than playbook-level vars

```

            
            

              
1. **Extra vars (`-e`)** (highest priority) 
                  

```bash
ansible-playbook playbook.yaml -e "app_port=9000"
ansible-playbook playbook.yaml -e "@vars/override.yml"

```

                
              
            

            

#### Precedence Example
            

If you define `app_port` in multiple places, the highest precedence wins:
            
              

```yaml
# roles/myapp/defaults/main.yml
app_port: 8080  # Priority 1 (lowest)

# inventory
[webservers:vars]
app_port=8081   # Priority 2

# playbook.yml
- hosts: webservers
  vars:
    app_port: 8082  # Priority 3
  vars_files:
    - vars.yml      # Priority 4 (vars.yml contains app_port: 8083)

  tasks:
    - set_fact:
        app_port: 8084  # Priority 7

    - debug:
        msg: "Port: {{ app_port }}"  # Will use 8084 unless overridden

# Command line (highest)
$ ansible-playbook playbook.yaml -e "app_port=9000"
# Output: Port: 9000

```

## 07. Playbook demo
            

              
- Execute the playbook by adding the required parameters.
              
- This can be done by setting up the parameters prior to executing the playbook, or by adding the
                parameters to the playbook itself.
            

            

#### Setting the env variable in the Ansible
              controller
            
              

```bash
# Example:

# 01. Setting the env variable in the Ansible controller
export PORT=8080

# Use the -e/--extra-vars to inject environment variables into the playbook
ansible-playbook playbook.yaml -e "my_var=$MY_VAR"

# Using the lookup Plug to fetch the value of the environment variables
PORT: "{{ lookup('env','PORT') }}"

```

            
            

#### Passing the variable to the playbook
            
              

```bash
# Example:

# 02. Passing the variable to the playbook
PORT="8080" ansible-playbook playbook.yaml

```

            
            

#### Using the environment
            
              

```bash
# Example:

# 0.3 Using the environment keyword in a **task** to set variables for that task
- name: Open the port in firewall
  environment:
    PORT: "8080"
  ufw:
    rule: allow
    port: "{{ PORT }}"
    proto: tcp

```

            
            

#### Passing the environment
            
              

```yaml
# Example:

# 0.4 Passing the environment to all the tasks in Playbook
- hosts: all
  environment:
    PORT: "8080"
  tasks:
    - name: Open the port in firewall
    ...

```

            
            

#### Set environment
            
              

```yaml
# Example:

# 05. Permanently set environment variables on remote hosts to persist variables
#     (e.g., in .bashrc or /etc/environment)
- name: Set permanent environment variable
  lineinfile:
    path: /etc/environment
    line: 'PORT="8080"'
    state: present
  become: yes

```

            
            

#### Using `var_files` to include variables
            
              

```yaml
# Example

# 06. We can use a variable file to pass variables in a playbook
# Check the vars.yaml file in the same directory
- hosts: all
  vars_files:
    - vars.yaml # Include variables from vars.yaml
  tasks:
    - name: Print a variable
      debug:
        msg: "{{ http_port }}"

```

            
            
            
            

![Practice](/static/assets/images/practice.png)
