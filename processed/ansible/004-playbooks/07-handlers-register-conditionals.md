---
title: "07. Handlers, Output Register & Conditionals"
slug: "07-handlers-register-conditionals"
estimated_time: 8
has_hands_on: false
---

## 09. Handlers and notifications
            

#### What are Handlers?
            

              
- Special tasks that run only when notified by other tasks
              
- Typically used to restart services after configuration changes
              
- Run once at the end of a play, even if notified multiple times
              
- Execute in the order they are defined, not the order they are notified
              
- Only run if a task that notifies them reports a “changed” status
            

            

#### Key Characteristics

| Aspect | Description |
| --- | --- |
| Execution | Run at the end of the play |
| Trigger | Only when notified and task changed |
| Frequency | Once per play, even if notified multiple times |
| Order | Defined order, not notification order |
| Idempotency | Help maintain idempotent playbooks |

            

#### Basic Handler Example
            

**Purpose**:
            

              
- Demonstrates the fundamental concept of handlers in Ansible
              
- Shows how multiple tasks can notify the same handler
              
- Handler executes only once at the end of the play, even when notified multiple times
              
- Essential for efficient service management - avoids restarting a service multiple times
              
- Ideal when several configuration changes occur in sequence
            

            
              

```yaml
---
- name: Configure web server
  hosts: webservers
  become: yes

  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
      notify: restart nginx

    - name: Copy nginx config
      copy:
        src: nginx.conf
        dest: /etc/nginx/nginx.conf
      notify: restart nginx

  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted

```

            
            

**How it works:**
            

              
1. If either task changes something, it notifies the handler
              
2. Handler runs once at the end, even though notified twice
              
3. If neither task changes anything, handler doesn’t run
            

            
            

#### Multiple Handlers in Sequence
            

**Purpose**:
            

              
- Illustrates triggering multiple handlers from a single task using a list of handler names
              
- Allows you to notify all handlers at once when performing several related actions
              
- Handlers execute in the order they are defined in the handlers section
              
- Execution order is NOT based on the order in the notify list
              
- Useful for orchestrating complex post-change workflows (restart → clear cache → notify)
            

            
              

```yaml
---
- name: Update application
  hosts: appservers
  become: yes

  tasks:
    - name: Update application code
      copy:
        src: app.py
        dest: /opt/app/app.py
      notify:
        - restart app
        - clear cache
        - send notification

  handlers:
    - name: restart app
      service:
        name: myapp
        state: restarted

    - name: clear cache
      command: rm -rf /var/cache/myapp/*

    - name: send notification
      debug:
        msg: "Application updated and restarted"

```

            
            
            

#### Handler with Conditionals
            

**Purpose**:
            

              
- Shows how to apply conditional logic to handlers using the `when` statement
              
- Not all handlers need to run in every scenario
              
- Certain handlers execute only when specific conditions are met
              
- Example: SSL-specific restart handler only runs when SSL is enabled
              
- Allows flexible playbooks that adapt to different environments without duplication
            

            
              

```yaml
---
- name: Conditional handler example
  hosts: webservers
  become: yes
  vars:
    enable_ssl: true

  tasks:
    - name: Copy nginx config
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify:
        - reload nginx
        - restart nginx ssl

  handlers:
    - name: reload nginx
      service:
        name: nginx
        state: reloaded

    - name: restart nginx ssl
      service:
        name: nginx
        state: restarted
      when: enable_ssl

```

            
            
            

#### Listening to Handlers
            

**Purpose**:
            

              
- The `listen` directive groups related handlers under a common topic or event name
              
- Notify a single event name instead of notifying each handler individually
              
- All handlers listening to that event will execute automatically
              
- Particularly useful when multiple post-change actions always need to happen together
              
- Decouples tasks from specific handler names for better maintainability
              
- You can add or remove handlers without modifying the tasks that notify them
            

            
              

```yaml
---
- name: Handler listening example
  hosts: all
  become: yes

  tasks:
    - name: Update system configuration
      copy:
        content: "config changes"
        dest: /etc/myapp.conf
      notify: system updated

  handlers:
    - name: Restart application
      service:
        name: myapp
        state: restarted
      listen: system updated

    - name: Clear application cache
      command: /usr/local/bin/clear_cache.sh
      listen: system updated

    - name: Log the update
      shell: echo "System updated at $(date)" >> /var/log/updates.log
      listen: system updated

```

            
            

**Benefit**: All three handlers execute when any task notifies “system updated”
            
            
            

#### Forcing Handler Execution
            

**Purpose**:
            

              
- By default, handlers run at the end of a play
              
- Sometimes you need a handler to execute immediately before continuing
              
- `meta: flush_handlers` forces all notified handlers to run at that specific point
              
- Critical when later tasks depend on the handler’s actions
              
- Example scenarios: restart service before health check, apply config before tests
              
- Without this, verification tasks might run before the service has restarted
            

            
              

```yaml
---
- name: Force handler execution
  hosts: webservers
  become: yes

  tasks:
    - name: Update config file
      copy:
        src: app.conf
        dest: /etc/app.conf
      notify: restart app

    - name: Force handlers to run now
      meta: flush_handlers

    - name: Verify app is running
      uri:
        url: http://localhost:8080/health
        status_code: 200

```

            
            

**Use case**: When you need to ensure a service is restarted before continuing
            
            

#### Handlers in Roles
            

**Purpose**:
            

              
- Demonstrates organizing handlers within Ansible roles (recommended approach)
              
- Handlers are defined in the `handlers/main.yml` file, separate from tasks
              
- Separation of concerns makes roles cleaner and more maintainable
              
- Tasks within the role notify handlers just like in regular playbooks
              
- Handlers are scoped to that role for proper encapsulation
              
- Create self-contained roles that can be shared across projects
              
- No worries about handler name conflicts between roles
            

            
              

```bash
# roles/nginx/tasks/main.yml
---
- name: Install nginx
  apt:
    name: nginx
    state: present

- name: Copy nginx config
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: restart nginx

# roles/nginx/handlers/main.yml
---
- name: restart nginx
  service:
    name: nginx
    state: restarted

- name: reload nginx
  service:
    name: nginx
    state: reloaded

- name: check nginx config
  command: nginx -t
  listen: validate nginx

```

            
            
            

#### Handler Best Practices
            

**✅ Do:**
            

              
- Use descriptive handler names
              
- Keep handlers idempotent
              
- Use `listen` for grouping related handlers
              
- Place handlers after tasks in playbook
              
- Use `meta: flush_handlers` when order matters
            

            

**❌ Don’t:**
            

              
- Don’t use handlers for critical tasks that must run
              
- Don’t rely on handler execution order across different notifications
              
- Don’t use handlers for tasks that should run regardless of changes
              
- Don’t create handler dependencies (they run independently)
            

            
            

#### Common Handler Patterns
            

**Pattern 1: Service Management**
            

**Purpose**:
            

              
- Shows the most common handler use case - managing service states
              
- Having both `restart` and `reload` handlers provides flexibility
              
- Use `restart` for full service restart (after installing packages or major config changes)
              
              
- Use `reload` for configuration reloads without interrupting active connections
              
- Most production services support reload operations for graceful configuration updates
              
- Minimizes downtime by choosing the appropriate service state change
            

            
              

```bash
handlers:
  - name: restart nginx
    service:
      name: nginx
      state: restarted

  - name: reload nginx
    service:
      name: nginx
      state: reloaded

```

            
            

**Pattern 2: Configuration Validation**
            

**Purpose**:
            

              
- Demonstrates critical safety practice - validate configuration before applying changes
              
- Using a `block` in the handler allows testing configuration file syntax first
              
- Only proceeds with restart if validation passes
              
- Prevents breaking a running service with invalid configuration
              
- If validation fails, service continues running with old (working) configuration
              
- Essential for production environments where service uptime is critical
            

            
              

```bash
handlers:
  - name: validate and restart nginx
    block:
      - name: Test nginx config
        command: nginx -t

      - name: Restart nginx
        service:
          name: nginx
          state: restarted

```

            
            

**Pattern 3: Cascade Handlers**
            

**Purpose**:
            

              
- Advanced pattern showing handlers that notify other handlers (chain of actions)
              
- First handler executes, then notifies the next handler in the chain
              
- Useful for complex deployment scenarios requiring specific sequences
              
- Example flow: deploy code → restart → verify health → update load balancer → notify monitoring
              
- Use carefully as it can make execution flow harder to understand
              
- Ensure each handler can work independently and handle failures gracefully
            

            
              

```yaml
tasks:
  - name: Update app code
    copy:
      src: app.py
      dest: /opt/app/
    notify: restart app

handlers:
  - name: restart app
    service:
      name: myapp
      state: restarted
    notify: verify app

  - name: verify app
    uri:
      url: http://localhost:8080/health

```

            
            
            

#### Real-World Example: Database Configuration
            

**Purpose**:
            

              
- Comprehensive example bringing together multiple handler concepts in production scenario
              
- Demonstrates configuration validation before applying changes
              
- Uses different handlers for different change types (restart vs reload)
              
- Verifies service health after changes with automatic retries
              
- Orchestrates multiple handlers in response to configuration updates
              
- Production-ready pattern for safely managing critical database services
              
- Minimizes downtime by catching configuration errors before affecting running service
              
- `pg_hba.conf` changes trigger reload only (less disruptive)
              
- Main configuration changes trigger full restart after validation
            

            
              

```yaml
---
- name: Configure PostgreSQL
  hosts: databases
  become: yes

  tasks:
    - name: Install PostgreSQL
      apt:
        name: postgresql
        state: present

    - name: Configure PostgreSQL
      template:
        src: postgresql.conf.j2
        dest: /etc/postgresql/14/main/postgresql.conf
      notify:
        - validate postgresql config
        - restart postgresql
        - verify postgresql

    - name: Configure pg_hba
      template:
        src: pg_hba.conf.j2
        dest: /etc/postgresql/14/main/pg_hba.conf
      notify: reload postgresql

  handlers:
    - name: validate postgresql config
      command: /usr/lib/postgresql/14/bin/postgres -C config_file -D /var/lib/postgresql/14/main
      changed_when: false

    - name: restart postgresql
      service:
        name: postgresql
        state: restarted

    - name: reload postgresql
      service:
        name: postgresql
        state: reloaded

    - name: verify postgresql
      postgresql_ping:
        db: postgres
      retries: 3
      delay: 5

```

            
            
            

## 10. Understanding the register keyword
            

#### Capturing Task Output
            
              

```yaml
---
- name: Register examples
  hosts: localhost
  tasks:
    - name: Check if file exists
      stat:
        path: /etc/nginx/nginx.conf
      register: nginx_config

    - name: Display result
      debug:
        msg: "File exists: {{ nginx_config.stat.exists }}"

    - name: Run command
      shell: uname -r
      register: kernel_version

    - name: Show kernel version
      debug:
        var: kernel_version.stdout

```

            
            

#### Using Registered Variables
            
              

```yaml
tasks:
  - name: Get service status
    command: systemctl status nginx
    register: service_status
    failed_when: false
    changed_when: false

  - name: Restart if not running
    service:
      name: nginx
      state: restarted
    when: service_status.rc != 0

```

            
            
            

## 11. Conditionals
            

#### When Statements
            
              

```yaml
---
- name: Conditional examples
  hosts: all
  tasks:
    - name: Install nginx on Debian
      apt:
        name: nginx
        state: present
      when: ansible_os_family == "Debian"

    - name: Install nginx on RedHat
      yum:
        name: nginx
        state: present
      when: ansible_os_family == "RedHat"

    - name: Multiple conditions (AND)
      debug:
        msg: "This is a production Ubuntu server"
      when:
        - ansible_distribution == "Ubuntu"
        - env == "production"

    - name: Multiple conditions (OR)
      debug:
        msg: "This is either staging or development"
      when: env == "staging" or env == "development"

```
