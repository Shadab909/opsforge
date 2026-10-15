#!/usr/bin/env python3
"""
Generate comprehensive, exhaustive quiz questions for all 8 Ansible Playbook chunks.
Ensures every single concept, syntax rule, precedence level, command flag,
and edge case from the reading sections is rigorously tested.
"""

import yaml
from pathlib import Path

PROCESSED_DIR = Path(__file__).resolve().parent.parent / "processed" / "ansible" / "004-playbooks"

CHUNKS_QUIZZES = {
    "01-what-are-playbooks": {
        "passing_score": 70,
        "questions": [
            {
                "type": "mcq",
                "question": "What is the primary format used to write Ansible playbooks?",
                "options": ["XML", "YAML", "JSON", "INI"],
                "correct": "YAML",
                "explanation": "Ansible playbooks are blueprints of automation tasks written in human-readable YAML format."
            },
            {
                "type": "mcq",
                "question": "What is the primary operational difference between Ansible ad-hoc commands and playbooks?",
                "options": [
                    "Ad-hoc commands are for quick one-time tasks; playbooks orchestrate complex, multi-step workflows",
                    "Ad-hoc commands run on Linux; playbooks only run on Windows",
                    "Ad-hoc commands require YAML files; playbooks are CLI-only",
                    "Ad-hoc commands support conditionals; playbooks do not"
                ],
                "correct": "Ad-hoc commands are for quick one-time tasks; playbooks orchestrate complex, multi-step workflows",
                "explanation": "Ad-hoc commands are single-line actions ideal for quick checks, whereas playbooks orchestrate repeatable, multi-machine workflows."
            },
            {
                "type": "true_false",
                "question": "Ansible playbooks are idempotent, meaning you can safely run them multiple times without altering the desired final state.",
                "correct": True,
                "explanation": "Idempotency ensures that running a playbook repeatedly makes changes only when the target state diverges from the desired state."
            },
            {
                "type": "mcq",
                "question": "Which dedicated command-line tool is used to execute an Ansible playbook?",
                "options": ["ansible --play", "ansible-playbook", "ansible-exec", "ansible-run"],
                "correct": "ansible-playbook",
                "explanation": "The `ansible-playbook` command is the dedicated CLI utility for parsing and running playbooks."
            },
            {
                "type": "true_false",
                "question": "Conditionals (such as the `when:` keyword) are fully supported in Ansible ad-hoc commands.",
                "correct": False,
                "explanation": "Conditionals are not supported in ad-hoc commands; they require playbooks."
            },
            {
                "type": "mcq",
                "question": "How do playbooks handle version control compared to ad-hoc commands?",
                "options": [
                    "Ad-hoc commands are easily version controlled in Git repositories",
                    "Playbooks are structured YAML files that can be version-controlled, code-reviewed, and tracked in Git",
                    "Playbooks cannot be tracked with Git because they are compiled binaries",
                    "Both provide identical version control capabilities"
                ],
                "correct": "Playbooks are structured YAML files that can be version-controlled, code-reviewed, and tracked in Git",
                "explanation": "Playbooks live as plain text files, enabling team collaboration, pull requests, and Git revision history."
            },
            {
                "type": "mcq",
                "question": "Which of the following is NOT listed as a core benefit of using Ansible playbooks?",
                "options": [
                    "Repeatability across development, staging, and production",
                    "Multi-tier host orchestration",
                    "Requiring background agent daemons to run continuously on target hosts",
                    "Self-documenting configuration"
                ],
                "correct": "Requiring background agent daemons to run continuously on target hosts",
                "explanation": "Ansible is agentless; target hosts do not require background daemons, only SSH and Python."
            },
            {
                "type": "true_false",
                "question": "Playbooks allow advanced error handling, including blocks, rescues, and rollback capabilities.",
                "correct": True,
                "explanation": "Playbooks support blocks, rescue sections, and failure conditions, unlike basic ad-hoc commands."
            },
            {
                "type": "mcq",
                "question": "Why is the YAML format considered advantageous for documentation in playbooks?",
                "options": [
                    "It compiles directly into bytecode",
                    "It is human-readable and self-documenting, making automation clear to both developers and sysadmins",
                    "It hides infrastructure details from users",
                    "It encrypts all parameters by default"
                ],
                "correct": "It is human-readable and self-documenting, making automation clear to both developers and sysadmins",
                "explanation": "YAML uses clear indentation and plain English keys, acting as living documentation for your systems."
            },
            {
                "type": "mcq",
                "question": "What is the orchestration capability of an ad-hoc command?",
                "options": [
                    "Single task on specified hosts",
                    "Multi-tier rolling deployment across 50 heterogeneous server tiers",
                    "Automated database migrations with rollbacks",
                    "Complex DAG task graphs"
                ],
                "correct": "Single task on specified hosts",
                "explanation": "Ad-hoc commands invoke only a single module task at a time."
            },
            {
                "type": "true_false",
                "question": "Playbooks can orchestrate tasks across multiple groups of hosts in a single execution file.",
                "correct": True,
                "explanation": "A playbook can define multiple plays, each targeting a distinct host group (e.g. database servers, then load balancers, then web servers)."
            },
            {
                "type": "mcq",
                "question": "In what way does playbook reusability benefit enterprise DevOps teams?",
                "options": [
                    "Playbooks can be shared across teams, projects, and environments with parameterized inputs",
                    "Playbooks lock configurations to a specific IP address",
                    "Playbooks cannot be modified once executed",
                    "Playbooks require paying a license fee per run"
                ],
                "correct": "Playbooks can be shared across teams, projects, and environments with parameterized inputs",
                "explanation": "Parametric playbooks and roles allow teams to share battle-tested automation across the organization."
            },
            {
                "type": "mcq",
                "question": "Which of the following scenarios is an ideal candidate for an ad-hoc command rather than a playbook?",
                "options": [
                    "Quickly pinging 100 servers to verify SSH reachability before an outage window",
                    "Orchestrating a blue-green zero-downtime microservice deployment",
                    "Provisioning a 3-node PostgreSQL cluster with replication and backup cron jobs",
                    "Enforcing CIS compliance benchmarks with 200 security configuration steps"
                ],
                "correct": "Quickly pinging 100 servers to verify SSH reachability before an outage window",
                "explanation": "Ad-hoc commands are best suited for rapid, one-off diagnostic or status queries."
            },
            {
                "type": "true_false",
                "question": "An Ansible playbook is compiled into a native binary executable before being transferred to target servers.",
                "correct": False,
                "explanation": "Ansible playbooks are interpreted directly at runtime; Ansible transfers lightweight Python execution payloads dynamically over SSH."
            },
            {
                "type": "mcq",
                "question": "How does Ansible enforce the concept of Infrastructure as Code (IaC) with playbooks?",
                "options": [
                    "By declaring desired end-state configurations in version-controlled text files",
                    "By generating proprietary hardware microcode",
                    "By requiring manual GUI point-and-click interventions",
                    "By deleting all existing servers and creating new ones on each run"
                ],
                "correct": "By declaring desired end-state configurations in version-controlled text files",
                "explanation": "Playbooks express desired state declaratively as plain text code that can be audited, reviewed, and tracked."
            }
        ]
    },
    "02-key-points": {
        "passing_score": 70,
        "questions": [
            {
                "type": "mcq",
                "question": "What is the structural hierarchy of an Ansible playbook?",
                "options": [
                    "Playbook contains one or more plays; each play contains tasks; each task calls an Ansible module",
                    "Modules contain tasks; tasks contain plays; plays contain playbooks",
                    "Tasks contain plays; plays contain modules",
                    "A playbook is a single module executed across all hosts"
                ],
                "correct": "Playbook contains one or more plays; each play contains tasks; each task calls an Ansible module",
                "explanation": "The hierarchy flows: Playbook (ordered list of plays) -> Play (maps hosts to tasks) -> Tasks (ordered steps) -> Module (the actual code executed)."
            },
            {
                "type": "mcq",
                "question": "In what order are plays and tasks executed within a playbook by default?",
                "options": [
                    "Sequential order from top to bottom",
                    "Parallel execution across all plays simultaneously",
                    "Random order based on host response time",
                    "Alphabetical order of task names"
                ],
                "correct": "Sequential order from top to bottom",
                "explanation": "Both plays in a playbook and tasks within a play execute sequentially from top to bottom."
            },
            {
                "type": "true_false",
                "question": "Within a single play, task 2 will begin executing on a host before task 1 has completed on that host.",
                "correct": False,
                "explanation": "Tasks execute in strict sequence; each task completes across the targeted batch of hosts before the next task begins."
            },
            {
                "type": "mcq",
                "question": "What is the primary role of a 'Play' in an Ansible playbook?",
                "options": [
                    "To map a specific set of target hosts to a defined sequence of tasks",
                    "To install Python on the local machine",
                    "To compile YAML into C binaries",
                    "To create an SSH keypair"
                ],
                "correct": "To map a specific set of target hosts to a defined sequence of tasks",
                "explanation": "A play's core purpose is mapping a host group (e.g. `hosts: webservers`) to the tasks that should run against them."
            },
            {
                "type": "mcq",
                "question": "What is the recommended modern practice when referencing Ansible modules in tasks?",
                "options": [
                    "Use the Fully Qualified Collection Name (FQCN), such as `ansible.builtin.copy`",
                    "Use short names only (e.g. `copy`)",
                    "Always execute bash shell commands instead of modules",
                    "Prefix all modules with `sudo.`"
                ],
                "correct": "Use the Fully Qualified Collection Name (FQCN), such as `ansible.builtin.copy`",
                "explanation": "Using FQCN prevents module naming collisions between core builtins and community or custom collections."
            },
            {
                "type": "true_false",
                "question": "A single playbook can configure database servers in the first play and web servers in the second play.",
                "correct": True,
                "explanation": "A playbook can contain multiple plays, allowing multi-machine, multi-tier orchestration in a pre-defined sequence."
            },
            {
                "type": "mcq",
                "question": "Which keywords are used in Ansible to launch long-running tasks asynchronously?",
                "options": [
                    "`async` and `poll`",
                    "`background` and `wait`",
                    "`daemon: true`",
                    "`thread: spawn`"
                ],
                "correct": "`async` and `poll`",
                "explanation": "Ansible uses `async` (max run time) and `poll` (how often to check status) for asynchronous task execution."
            },
            {
                "type": "mcq",
                "question": "Which of the following infrastructure domains can Ansible playbooks automate?",
                "options": [
                    "Software packages, system users, network devices, and cloud infrastructure",
                    "Only Linux packages via apt",
                    "Only local shell scripts",
                    "Only web servers running Nginx"
                ],
                "correct": "Software packages, system users, network devices, and cloud infrastructure",
                "explanation": "Ansible automates full-stack infrastructure: packages, users, services, network gear, storage, and cloud providers."
            },
            {
                "type": "true_false",
                "question": "Playbooks can be parameterized with variables, allowing the same playbook to configure development, staging, and production environments.",
                "correct": True,
                "explanation": "By injecting environment-specific variables, a single playbook can manage multiple deployment tiers."
            },
            {
                "type": "mcq",
                "question": "What architectural unit is responsible for executing the actual action on target nodes in a task?",
                "options": [
                    "The Ansible module (e.g. `ansible.builtin.user`)",
                    "The inventory file",
                    "The playbook header",
                    "The YAML parser"
                ],
                "correct": "The Ansible module (e.g. `ansible.builtin.user`)",
                "explanation": "Modules are discrete units of code that Ansible ships to remote hosts to perform work."
            },
            {
                "type": "true_false",
                "question": "Zero-downtime rolling updates cannot be implemented with Ansible playbooks.",
                "correct": False,
                "explanation": "Ansible natively supports rolling updates using directives like `serial: 1` or `serial: 20%`."
            },
            {
                "type": "mcq",
                "question": "What is the key mechanism for structuring reusable playbook automation across multiple repositories?",
                "options": [
                    "Roles and collections",
                    "Monolithic 50,000-line playbook files",
                    "Cron jobs on controller",
                    "Ad-hoc shell history"
                ],
                "correct": "Roles and collections",
                "explanation": "Ansible Roles and Collections provide modular, distributable packaging for reusable tasks, vars, and handlers."
            },
            {
                "type": "mcq",
                "question": "When a task calls an Ansible module, how is the task evaluated on the remote host?",
                "options": [
                    "Ansible generates module code, transfers it over SSH, executes it, and retrieves JSON output",
                    "Ansible installs a permanent background agent that polls every second",
                    "Ansible converts the module into an RPM package",
                    "Ansible requires remote root login with telnet"
                ],
                "correct": "Ansible generates module code, transfers it over SSH, executes it, and retrieves JSON output",
                "explanation": "Ansible packages module code, streams it via SSH/WinRM, executes with target Python, and parses the JSON response."
            },
            {
                "type": "true_false",
                "question": "Synchronous task execution is the default behavior in Ansible.",
                "correct": True,
                "explanation": "Ansible runs tasks synchronously by default, waiting for each task to complete before advancing."
            },
            {
                "type": "mcq",
                "question": "Which of the following best describes an ordered list in YAML syntax?",
                "options": [
                    "A YAML Sequence (items preceded by a dash and space `- `)",
                    "A YAML Mapping (key-value pairs separated by colon)",
                    "A JSON Object",
                    "An XML Element"
                ],
                "correct": "A YAML Sequence (items preceded by a dash and space `- `)",
                "explanation": "A sequence (list) in YAML begins each element with `- ` at the same indentation level."
            },
            {
                "type": "mcq",
                "question": "What happens if a play contains multiple tasks and task 3 fails on `hostA` but succeeds on `hostB`?",
                "options": [
                    "`hostA` is dropped from remaining tasks in that play; `hostB` continues to task 4",
                    "The entire playbook immediately aborts for all hosts",
                    "Ansible ignores the failure and executes task 4 on `hostA` anyway",
                    "`hostA` is automatically rebooted"
                ],
                "correct": "`hostA` is dropped from remaining tasks in that play; `hostB` continues to task 4",
                "explanation": "Ansible tracks failures per host. By default, a failed host halts further task execution in that play, while healthy hosts proceed."
            },
            {
                "type": "true_false",
                "question": "A playbook must always contain at least one task to be syntactically valid and runnable.",
                "correct": True,
                "explanation": "A play without any tasks, roles, or import directives has nothing to execute and will raise an error or warning."
            },
            {
                "type": "mcq",
                "question": "Which of the following describes the relationship between Ansible Collections and Modules?",
                "options": [
                    "Collections are packaging formats that group related modules, plugins, roles, and playbooks into a single namespace",
                    "Collections are only for Python package management via pip",
                    "Modules contain Collections inside their source code",
                    "Collections have replaced playbooks completely"
                ],
                "correct": "Collections are packaging formats that group related modules, plugins, roles, and playbooks into a single namespace",
                "explanation": "Ansible Collections represent the distribution model for publishing and consuming modules and roles (e.g. `community.general`, `ansible.builtin`)."
            }
        ]
    },
    "03-yaml-basics": {
        "passing_score": 70,
        "questions": [
            {
                "type": "mcq",
                "question": "How must indentation be formatted in YAML files?",
                "options": [
                    "With spaces only (tabs will cause syntax errors)",
                    "With tab characters only",
                    "Either tabs or spaces, as long as it is consistent",
                    "YAML does not use indentation"
                ],
                "correct": "With spaces only (tabs will cause syntax errors)",
                "explanation": "YAML strictly forbids tab characters for indentation; spaces must always be used."
            },
            {
                "type": "mcq",
                "question": "What marker standardly indicates the start of a YAML document?",
                "options": ["---", "===", "###", "START"],
                "correct": "---",
                "explanation": "Three dashes `---` denote the beginning of a YAML document."
            },
            {
                "type": "true_false",
                "question": "In YAML dictionaries, the colon `:` after a key must immediately be followed by a space.",
                "correct": True,
                "explanation": "A colon followed by a space (`key: value`) is required for proper key-value dictionary syntax in YAML."
            },
            {
                "type": "mcq",
                "question": "What character denotes a literal block scalar in YAML that preserves newlines and trailing spaces?",
                "options": ["| (pipe)", "> (greater-than)", "& (ampersand)", "* (asterisk)"],
                "correct": "| (pipe)",
                "explanation": "The pipe `|` denotes a literal block scalar which preserves line breaks."
            },
            {
                "type": "mcq",
                "question": "What character denotes a folded block scalar in YAML that folds newlines into spaces?",
                "options": ["> (greater-than)", "| (pipe)", "$ (dollar)", "% (percent)"],
                "correct": "> (greater-than)",
                "explanation": "The greater-than `>` folds newlines into spaces, treating lines as a single wrapped paragraph."
            },
            {
                "type": "true_false",
                "question": "YAML is case-sensitive, meaning `Hosts:` and `hosts:` are treated as completely different keys by Ansible.",
                "correct": True,
                "explanation": "YAML and Ansible keywords are strictly case-sensitive."
            },
            {
                "type": "mcq",
                "question": "How should boolean values be specified in dictionaries to ensure compatibility with default yamllint rules?",
                "options": [
                    "Lowercase `true` or `false`",
                    "All-caps `TRUE` or `FALSE`",
                    "Yes / No only",
                    "1 / 0 integers only"
                ],
                "correct": "Lowercase `true` or `false`",
                "explanation": "Lowercase `true` and `false` are the standard recommended boolean representations in modern YAML."
            },
            {
                "type": "mcq",
                "question": "How are list members defined in YAML?",
                "options": [
                    "Lines at the same indentation level starting with a dash and a space `- `",
                    "Enclosed in curly braces `{}`",
                    "Comma-separated values surrounded by angle brackets `<>`",
                    "Numbered with parenthesis `(1)`, `(2)`"
                ],
                "correct": "Lines at the same indentation level starting with a dash and a space `- `",
                "explanation": "A dash followed by a space `- ` at equal indentation denotes an element of a list/sequence."
            },
            {
                "type": "true_false",
                "question": "Most string values in YAML require quotation marks to be valid.",
                "correct": False,
                "explanation": "YAML does not require quotes around most string values unless the string contains special characters like `:` or `{}`."
            },
            {
                "type": "mcq",
                "question": "Besides YAML, what alternative data serialization format can technically be used to write playbooks?",
                "options": ["JSON", "XML", "TOML", "CSV"],
                "correct": "JSON",
                "explanation": "YAML is a superset of JSON, meaning valid JSON is also valid YAML and can be parsed by Ansible."
            },
            {
                "type": "true_false",
                "question": "Comments in YAML start with a hash `#` symbol and extend to the end of the line.",
                "correct": True,
                "explanation": "`#` introduces a comment in YAML."
            },
            {
                "type": "mcq",
                "question": "What happens if you use a tab character for indentation in an Ansible playbook YAML file?",
                "options": [
                    "The parser raises a YAML syntax error (YAML does not allow tabs for indentation)",
                    "Ansible automatically replaces tabs with 4 spaces",
                    "Ansible ignores the line completely",
                    "The playbook executes normally"
                ],
                "correct": "The parser raises a YAML syntax error (YAML does not allow tabs for indentation)",
                "explanation": "YAML parsers will fail immediately with a syntax error if tabs are detected in indentation."
            },
            {
                "type": "true_false",
                "question": "In YAML, two spaces is the standard recommended indentation level for nested dictionaries and lists.",
                "correct": True,
                "explanation": "Two spaces per indentation level is the universal Ansible and YAML convention."
            },
            {
                "type": "mcq",
                "question": "Which of the following represents a dictionary with two keys in YAML?",
                "options": [
                    "name: test\nport: 80",
                    "- name: test\n- port: 80",
                    "(name=test, port=80)",
                    "[name: test, port: 80]"
                ],
                "correct": "name: test\nport: 80",
                "explanation": "`name: test` and `port: 80` at the same level form a key-value mapping (dictionary)."
            },
            {
                "type": "true_false",
                "question": "If a string in YAML begins with a template variable like `{{ app_name }}`, the entire string must be enclosed in quotes.",
                "correct": True,
                "explanation": "If a value starts with `{{`, YAML thinks it is an inline dictionary; therefore, the value must be quoted (e.g. `\"{{ app_name }}\"`)."
            },
            {
                "type": "mcq",
                "question": "What marker denotes the optional end of a YAML document?",
                "options": ["...", "---", "###", "END"],
                "correct": "...",
                "explanation": "Three periods `...` denote the end of a document in multi-document YAML files."
            },
            {
                "type": "mcq",
                "question": "Which of the following is an inline representation of a YAML dictionary?",
                "options": [
                    "{ name: 'nginx', port: 80 }",
                    "[ name: 'nginx', port: 80 ]",
                    "( name: 'nginx', port: 80 )",
                    "< name='nginx' port='80' />"
                ],
                "correct": "{ name: 'nginx', port: 80 }",
                "explanation": "Curly braces `{}` are valid YAML flow mapping (inline dictionary) syntax, matching JSON object notation."
            },
            {
                "type": "true_false",
                "question": "In YAML, numbers starting with leading zeroes (such as file modes like `0644`) should be quoted as strings `\"0644\"` to prevent accidental octal integer conversion bugs.",
                "correct": True,
                "explanation": "Unquoted `0644` can be parsed as an octal integer in older YAML specs or cause confusion; quoting it as `\"0644\"` preserves the exact string representation expected by file modules."
            }
        ]
    },
    "04-first-playbook": {
        "passing_score": 70,
        "questions": [
            {
                "type": "mcq",
                "question": "In a basic playbook play, which directive specifies the target machines where tasks will execute?",
                "options": ["hosts:", "targets:", "nodes:", "servers:"],
                "correct": "hosts:",
                "explanation": "The `hosts:` directive defines the targeted inventory hosts or groups for that play."
            },
            {
                "type": "mcq",
                "question": "Which builtin Ansible module is commonly used to print values or debug messages during playbook execution?",
                "options": ["ansible.builtin.debug", "ansible.builtin.echo", "ansible.builtin.print", "console"],
                "correct": "ansible.builtin.debug",
                "explanation": "The `ansible.builtin.debug` module prints statements and variable values during execution."
            },
            {
                "type": "mcq",
                "question": "What is the primary difference between `ansible.builtin.command` and `ansible.builtin.shell`?",
                "options": [
                    "`command` executes binaries directly without a shell, while `shell` executes through `/bin/sh` and supports pipes `|` and redirects",
                    "`command` runs as root; `shell` runs as guest",
                    "`shell` is idempotent; `command` is not",
                    "`command` works on Windows; `shell` does not"
                ],
                "correct": "`command` executes binaries directly without a shell, while `shell` executes through `/bin/sh` and supports pipes `|` and redirects",
                "explanation": "`command` is safer and faster because it does not invoke a shell, but `shell` is required if you need pipes `|`, redirects `>`, or environment expansion."
            },
            {
                "type": "mcq",
                "question": "What is the purpose of the `register:` keyword in a task?",
                "options": [
                    "To save the output and metadata of a task into a variable for later tasks to use",
                    "To register the playbook with Ansible Galaxy",
                    "To create a new user on the target system",
                    "To log in to the remote machine"
                ],
                "correct": "To save the output and metadata of a task into a variable for later tasks to use",
                "explanation": "`register: <var_name>` captures return attributes like stdout, rc, and changed state."
            },
            {
                "type": "true_false",
                "question": "When printing a registered variable's output with `ansible.builtin.debug`, `var_name.stdout_lines` outputs the lines as a formatted list rather than one unbroken string.",
                "correct": True,
                "explanation": "`stdout_lines` splits stdout by newlines into a JSON list of strings for readable output."
            },
            {
                "type": "mcq",
                "question": "How are variables interpolated into task arguments in an Ansible playbook?",
                "options": [
                    "{{ variable_name }}",
                    "$(variable_name)",
                    "%{variable_name}",
                    "${variable_name}"
                ],
                "correct": "{{ variable_name }}",
                "explanation": "Ansible uses Jinja2 templating syntax with double curly braces `{{ var }}`."
            },
            {
                "type": "mcq",
                "question": "In a registered task result named `output`, which attribute contains the numeric process exit status code?",
                "options": ["output.rc", "output.status", "output.code", "output.exit"],
                "correct": "output.rc",
                "explanation": "The return code is stored in `.rc` (return code), where 0 indicates success."
            },
            {
                "type": "true_false",
                "question": "Every task in an Ansible playbook should have a descriptive `name:` field.",
                "correct": True,
                "explanation": "Task names document the intent of each step and appear in terminal logs during execution."
            },
            {
                "type": "mcq",
                "question": "Which parameter of the `ansible.builtin.debug` module is used to print an existing variable directly without string interpolation?",
                "options": ["var:", "msg:", "text:", "value:"],
                "correct": "var:",
                "explanation": "`var: my_var` evaluates the variable directly without quotes or `{{ }}`; `msg: \"string\"` is used for interpolated text."
            },
            {
                "type": "true_false",
                "question": "Setting `hosts: localhost` combined with `connection: local` runs the playbook against the controller machine itself.",
                "correct": True,
                "explanation": "This tells Ansible to execute tasks locally on the machine driving the playbook."
            },
            {
                "type": "mcq",
                "question": "If a task does not specify privilege escalation (`become: yes`), what permissions will the task run with?",
                "options": [
                    "The permissions of the login/connecting user",
                    "Root permissions automatically",
                    "Guest read-only permissions",
                    "The playbook will refuse to run"
                ],
                "correct": "The permissions of the login/connecting user",
                "explanation": "Tasks execute with the unprivileged login user's permissions unless `become` is enabled."
            },
            {
                "type": "true_false",
                "question": "If a task fails in a play, Ansible will by default stop executing subsequent tasks on that failed host.",
                "correct": True,
                "explanation": "Ansible aborts task execution on a host immediately when a task fails, preserving the state for inspection."
            },
            {
                "type": "mcq",
                "question": "Which return key in a registered variable indicates whether the system state was altered?",
                "options": [".changed", ".modified", ".state", ".updated"],
                "correct": ".changed",
                "explanation": "The boolean `.changed` flag is `true` if changes were applied, `false` otherwise."
            },
            {
                "type": "true_false",
                "question": "The `tasks:` section of a play is formatted as a YAML list of dictionaries.",
                "correct": True,
                "explanation": "Each task is an item in the `tasks:` sequence, starting with `- name:`."
            },
            {
                "type": "mcq",
                "question": "Which builtin module would you use to list files in a directory on target hosts in an idempotent, structured way?",
                "options": ["ansible.builtin.find", "ansible.builtin.ls", "ansible.builtin.dir", "ansible.builtin.list"],
                "correct": "ansible.builtin.find",
                "explanation": "`ansible.builtin.find` is the dedicated module for querying files by pattern, size, and age."
            },
            {
                "type": "mcq",
                "question": "What is the key advantage of using `ansible.builtin.find` over executing `ls` or `find` with the `command` module?",
                "options": [
                    "It returns structured JSON dictionary objects with detailed file attributes (mtime, size, permissions)",
                    "It automatically deletes files",
                    "It works without Python installed on the remote machine",
                    "It creates backup copies of all matched files"
                ],
                "correct": "It returns structured JSON dictionary objects with detailed file attributes (mtime, size, permissions)",
                "explanation": "The `find` module produces typed data structures (`files` list with path, size, mode, etc.) that can easily be manipulated in subsequent tasks."
            },
            {
                "type": "true_false",
                "question": "A playbook file can contain multiple plays separated under the top-level YAML list.",
                "correct": True,
                "explanation": "A playbook is a list of plays: each item in the top-level list starts with `- name: <Play Name>`."
            },
            {
                "type": "mcq",
                "question": "In the example playbook `004-list-files.yaml`, which shell command is used to list files when testing the register keyword?",
                "options": [
                    "ls -la",
                    "cat /etc/passwd",
                    "df -h",
                    "ps aux"
                ],
                "correct": "ls -la",
                "explanation": "The introductory example runs `ls -la` to capture and register directory contents."
            }
        ]
    },
    "05-execution-and-syntax": {
        "passing_score": 70,
        "questions": [
            {
                "type": "mcq",
                "question": "Which flag performs a dry-run (check mode) of a playbook without making actual changes to target hosts?",
                "options": ["--check", "--dry", "--test", "--verify"],
                "correct": "--check",
                "explanation": "`ansible-playbook playbook.yaml --check` runs the playbook in check mode (dry run)."
            },
            {
                "type": "mcq",
                "question": "Which command-line option limits playbook execution to a specific host or group in your inventory?",
                "options": ["--limit (or -l)", "--only", "--target", "--filter"],
                "correct": "--limit (or -l)",
                "explanation": "`--limit <pattern>` restricts execution to matching hosts without modifying the inventory."
            },
            {
                "type": "mcq",
                "question": "Which flag displays file-level differences (before and after) when configuration templates or files change?",
                "options": ["--diff", "--compare", "--delta", "--show-changes"],
                "correct": "--diff",
                "explanation": "`--diff` displays unified diffs of changes made to files on remote systems."
            },
            {
                "type": "true_false",
                "question": "You can safely combine `--check` and `--diff` together to preview exact configuration changes without modifying anything.",
                "correct": True,
                "explanation": "`ansible-playbook playbook.yaml --check --diff` is the standard pre-flight audit combination in production."
            },
            {
                "type": "mcq",
                "question": "How do you specify a custom inventory file when running `ansible-playbook`?",
                "options": ["-i <inventory_path>", "-f <inventory_path>", "--inventory-file", "--hosts-path"],
                "correct": "-i <inventory_path>",
                "explanation": "The `-i` or `--inventory` flag specifies the path to an inventory file or directory."
            },
            {
                "type": "mcq",
                "question": "In the Ansible execution recap, what does `ok=2` mean?",
                "options": [
                    "Two tasks ran successfully without needing to make changes to the system",
                    "Two hosts failed to respond",
                    "Two tasks modified the system state",
                    "Two tasks were skipped"
                ],
                "correct": "Two tasks ran successfully without needing to make changes to the system",
                "explanation": "`ok` indicates tasks that verified the system was already in the desired state."
            },
            {
                "type": "mcq",
                "question": "In the Ansible execution recap, what does `changed=1` mean?",
                "options": [
                    "One or more tasks applied modifications to bring the host to the desired state",
                    "One playbook file was modified",
                    "One task failed",
                    "One host was rebooted"
                ],
                "correct": "One or more tasks applied modifications to bring the host to the desired state",
                "explanation": "`changed` means the system's state was altered by Ansible."
            },
            {
                "type": "mcq",
                "question": "In the Ansible execution recap, what does `unreachable=1` signify?",
                "options": [
                    "Ansible failed to establish a network/SSH connection to that host",
                    "The task timed out after execution",
                    "The module was missing on the remote host",
                    "Privilege escalation was denied"
                ],
                "correct": "Ansible failed to establish a network/SSH connection to that host",
                "explanation": "`unreachable` indicates an SSH, authentication, or network connectivity failure."
            },
            {
                "type": "mcq",
                "question": "In the Ansible execution recap, what does `skipped=1` indicate?",
                "options": [
                    "A task was bypassed because its `when:` conditional evaluated to false",
                    "The task had a syntax error",
                    "The host was unreachable",
                    "The user canceled the task interactively"
                ],
                "correct": "A task was bypassed because its `when:` conditional evaluated to false",
                "explanation": "Tasks are skipped when conditional expressions evaluate to false."
            },
            {
                "type": "mcq",
                "question": "Which verbosity flag level shows connection debugging and SSH client command details?",
                "options": ["-vvv", "-v", "-s", "--quiet"],
                "correct": "-vvv",
                "explanation": "Level `-vvv` enables connection and file transfer debugging."
            },
            {
                "type": "mcq",
                "question": "Which directive in a play enables privilege escalation (sudo)?",
                "options": ["become: yes", "sudo: true", "privilege: root", "admin: enable"],
                "correct": "become: yes",
                "explanation": "`become: yes` instructs Ansible to use become plugins (such as sudo) for privilege escalation."
            },
            {
                "type": "mcq",
                "question": "Which directive specifies the target user for privilege escalation (e.g. becoming `postgres`)?",
                "options": ["become_user: postgres", "as_user: postgres", "target_user: postgres", "user_switch: postgres"],
                "correct": "become_user: postgres",
                "explanation": "`become_user` sets the target account to switch to after privilege escalation."
            },
            {
                "type": "true_false",
                "question": "The `environment:` keyword in a play or task sets environment variables for the execution of modules.",
                "correct": True,
                "explanation": "The `environment:` dictionary injects environment variables into the process executing the module."
            },
            {
                "type": "mcq",
                "question": "Why is the `environment:` keyword NOT recommended for passing confidential passwords or API keys?",
                "options": [
                    "Environment variables may appear in system logs and process tables (`ps aux`) on target machines",
                    "Ansible blocks environment variables from reaching modules",
                    "Environment variables crash the Python interpreter",
                    "The keyword is deprecated"
                ],
                "correct": "Environment variables may appear in system logs and process tables (`ps aux`) on target machines",
                "explanation": "Process environment variables can be visible in `/proc/<pid>/environ` and system monitoring logs."
            },
            {
                "type": "true_false",
                "question": "A play can define local play-level variables directly using the `vars:` directive.",
                "correct": True,
                "explanation": "The `vars:` block at the play level defines variables scoped to that play."
            },
            {
                "type": "mcq",
                "question": "What is the maximum verbosity level flag supported by Ansible CLI for full connection plugin tracing?",
                "options": ["-vvvv (or -vvvvv in modern versions)", "-v", "-v10", "--max-debug"],
                "correct": "-vvvv (or -vvvvv in modern versions)",
                "explanation": "Four or five `-v` flags enable deep connection tracing, including SSH connection commands."
            },
            {
                "type": "true_false",
                "question": "Running `ansible-playbook` without `-i` will cause Ansible to fall back to the default inventory at `/etc/ansible/hosts`.",
                "correct": True,
                "explanation": "If no inventory is provided and none is configured in `ansible.cfg`, Ansible falls back to `/etc/ansible/hosts`."
            },
            {
                "type": "mcq",
                "question": "What does `failed=1` in the play recap mean?",
                "options": [
                    "One or more tasks failed on that host, causing Ansible to halt further execution on it",
                    "The inventory was missing that host",
                    "The playbook had a YAML syntax error",
                    "One file was deleted"
                ],
                "correct": "One or more tasks failed on that host, causing Ansible to halt further execution on it",
                "explanation": "A failure halts the host's execution unless `ignore_errors: yes` was declared."
            },
            {
                "type": "true_false",
                "question": "The `--syntax-check` flag validates the YAML and structural syntax of a playbook without contacting any hosts.",
                "correct": True,
                "explanation": "`ansible-playbook playbook.yaml --syntax-check` quickly validates syntax offline."
            },
            {
                "type": "mcq",
                "question": "What does `TASK [Gathering Facts]` do automatically at the start of a play?",
                "options": [
                    "It runs the `setup` module to gather system facts (OS, IP, CPU, memory) from the target hosts",
                    "It downloads packages from the internet",
                    "It checks if Git is installed",
                    "It creates user accounts"
                ],
                "correct": "It runs the `setup` module to gather system facts (OS, IP, CPU, memory) from the target hosts",
                "explanation": "Fact gathering is enabled by default and queries system attributes into `ansible_*` variables."
            },
            {
                "type": "mcq",
                "question": "Which flag prompts the user for the SSH password when connecting to remote hosts?",
                "options": ["--ask-pass (or -k)", "--password", "--ssh-key", "-P"],
                "correct": "--ask-pass (or -k)",
                "explanation": "The `-k` or `--ask-pass` flag triggers an interactive password prompt for SSH connections."
            },
            {
                "type": "mcq",
                "question": "Which flag prompts the user interactively for the privilege escalation (sudo) password?",
                "options": ["--ask-become-pass (or -K)", "--sudo-password", "--root-prompt", "-S"],
                "correct": "--ask-become-pass (or -K)",
                "explanation": "The `-K` or `--ask-become-pass` flag prompts for the sudo/become password."
            }
        ]
    },
    "06-variables": {
        "passing_score": 70,
        "questions": [
            {
                "type": "mcq",
                "question": "Which variable source has the absolute HIGHEST precedence in Ansible?",
                "options": [
                    "Extra variables passed on the command line via `-e` or `--extra-vars`",
                    "Playbook `vars:` section",
                    "Host facts",
                    "Role defaults"
                ],
                "correct": "Extra variables passed on the command line via `-e` or `--extra-vars`",
                "explanation": "Extra variables (`-e`) always override all other variable definitions in Ansible."
            },
            {
                "type": "mcq",
                "question": "Which variable source has the LOWEST precedence in Ansible?",
                "options": [
                    "Role defaults (`defaults/main.yml`)",
                    "Inventory file variables",
                    "Playbook vars",
                    "Registered variables"
                ],
                "correct": "Role defaults (`defaults/main.yml`)",
                "explanation": "Role defaults are intentionally designed to have the lowest priority so they can be easily overridden."
            },
            {
                "type": "mcq",
                "question": "How do you access the `port` property of a dictionary variable defined as `database: { host: 'db.local', port: 5432 }`?",
                "options": [
                    "{{ database.port }} or {{ database['port'] }}",
                    "{{ database->port }}",
                    "{{ database:port }}",
                    "{{ database.get(port) }}"
                ],
                "correct": "{{ database.port }} or {{ database['port'] }}",
                "explanation": "Ansible Jinja2 templates support both dot notation (`database.port`) and bracket notation (`database['port']`)."
            },
            {
                "type": "mcq",
                "question": "Which directive in a play allows importing an external YAML file containing variables?",
                "options": ["vars_files:", "import_vars:", "include_env:", "load_vars:"],
                "correct": "vars_files:",
                "explanation": "The `vars_files:` directive takes a list of external YAML files containing variable mappings."
            },
            {
                "type": "mcq",
                "question": "How can you read an environment variable from the controller machine inside a playbook?",
                "options": [
                    "{{ lookup('env', 'VARIABLE_NAME') }}",
                    "{{ env.VARIABLE_NAME }}",
                    "$VARIABLE_NAME",
                    "{{ system('VARIABLE_NAME') }}"
                ],
                "correct": "{{ lookup('env', 'VARIABLE_NAME') }}",
                "explanation": "The `lookup('env', 'VAR')` plugin reads environment variables from the Ansible controller."
            },
            {
                "type": "true_false",
                "question": "The `environment:` keyword can be applied at the task level to provide environment variables specifically for that task.",
                "correct": True,
                "explanation": "Applying `environment:` on a task supplies environment variables only during that task's execution."
            },
            {
                "type": "mcq",
                "question": "Which module is recommended to permanently set an environment variable on a target remote host by editing `/etc/environment`?",
                "options": ["ansible.builtin.lineinfile", "ansible.builtin.set_env", "ansible.builtin.touch", "ansible.builtin.export"],
                "correct": "ansible.builtin.lineinfile",
                "explanation": "`ansible.builtin.lineinfile` ensures specific lines (like `PORT=\"8080\"`) exist in configuration files like `/etc/environment`."
            },
            {
                "type": "mcq",
                "question": "In what order of precedence do Host Facts, Playbook Vars, and Registered Variables rank relative to each other?",
                "options": [
                    "Playbook vars (lower) -> Host facts -> Registered variables (higher)",
                    "Registered variables (lower) -> Playbook vars -> Host facts (higher)",
                    "Host facts (lower) -> Registered variables -> Playbook vars (higher)",
                    "All three have identical precedence"
                ],
                "correct": "Playbook vars (lower) -> Host facts -> Registered variables (higher)",
                "explanation": "According to the Ansible 10-level hierarchy: Playbook vars (#3) < Host facts (#5) < Registered variables (#6)."
            },
            {
                "type": "mcq",
                "question": "Which module allows creating or overriding variables dynamically during playbook execution across subsequent tasks?",
                "options": ["ansible.builtin.set_fact", "ansible.builtin.var", "ansible.builtin.define", "ansible.builtin.assign"],
                "correct": "ansible.builtin.set_fact",
                "explanation": "`set_fact` assigns dynamic variables during runtime that persist across subsequent tasks on that host."
            },
            {
                "type": "mcq",
                "question": "How can you prompt the user interactively in the terminal for variable values before a play runs?",
                "options": [
                    "Using the `vars_prompt:` directive in the play",
                    "Using `input:` in a task",
                    "Using `read:` in the inventory",
                    "Ansible does not support terminal prompts"
                ],
                "correct": "Using the `vars_prompt:` directive in the play",
                "explanation": "`vars_prompt:` prompts the user for sensitive or runtime values, with options like `private: yes` to hide typing."
            },
            {
                "type": "true_false",
                "question": "Variables defined in `[webservers:vars]` in an inventory file take higher precedence than `vars:` defined inside a playbook.",
                "correct": False,
                "explanation": "Playbook `vars:` take higher precedence than inventory group/host variables."
            },
            {
                "type": "mcq",
                "question": "How can you pass a JSON or YAML file containing extra variables directly via the command line?",
                "options": [
                    "ansible-playbook playbook.yaml -e \"@vars/override.yml\"",
                    "ansible-playbook playbook.yaml --include-vars vars/override.yml",
                    "ansible-playbook playbook.yaml -f vars/override.yml",
                    "ansible-playbook playbook.yaml --vars-file vars/override.yml"
                ],
                "correct": "ansible-playbook playbook.yaml -e \"@vars/override.yml\"",
                "explanation": "Prefixing the file path with an `@` symbol (`-e \"@file.yml\"`) tells Ansible to load extra variables from that file."
            },
            {
                "type": "mcq",
                "question": "How do you access an element of a list variable `packages: ['nginx', 'git', 'curl']` in a task?",
                "options": [
                    "{{ packages[0] }}",
                    "{{ packages(0) }}",
                    "{{ packages.first }}",
                    "{{ packages->0 }}"
                ],
                "correct": "{{ packages[0] }}",
                "explanation": "Lists use zero-based index access in brackets: `{{ packages[0] }}` evaluates to `'nginx'`."
            },
            {
                "type": "true_false",
                "question": "The `environment:` keyword set at the play level applies to all tasks in that play.",
                "correct": True,
                "explanation": "When declared at the play level, `environment:` supplies variables to every task within that play."
            },
            {
                "type": "mcq",
                "question": "If `app_port` is defined as 8080 in role defaults, 8081 in inventory, 8082 in playbook vars, and passed as `-e app_port=9000`, what will its value be?",
                "options": ["9000", "8082", "8081", "8080"],
                "correct": "9000",
                "explanation": "`-e` extra-vars always takes absolute highest priority over all other definitions."
            },
            {
                "type": "true_false",
                "question": "Facts gathered by Ansible automatically (like `ansible_distribution`) have higher precedence than role defaults.",
                "correct": True,
                "explanation": "Host facts rank at priority #5, whereas role defaults rank at priority #1 (lowest)."
            },
            {
                "type": "mcq",
                "question": "What is the variable precedence level of `set_fact` relative to `registered variables`?",
                "options": [
                    "`set_fact` (priority #7) is higher precedence than `registered variables` (priority #6)",
                    "`registered variables` is higher than `set_fact`",
                    "Both share the exact same precedence level",
                    "`set_fact` is lower than role defaults"
                ],
                "correct": "`set_fact` (priority #7) is higher precedence than `registered variables` (priority #6)",
                "explanation": "A fact set via `set_fact` will override a previously registered variable of the same name."
            },
            {
                "type": "true_false",
                "question": "You can prepend environment variables in the command line (e.g. `PORT=\"8080\" ansible-playbook playbook.yaml`) to set environment variables on the controller.",
                "correct": True,
                "explanation": "Standard shell syntax sets the env var for the controller process, accessible via `lookup('env', 'PORT')`."
            },
            {
                "type": "mcq",
                "question": "Which of the following is a valid way to define a list of multiple packages in playbook `vars:`?",
                "options": [
                    "packages:\n  - nginx\n  - git\n  - curl",
                    "packages = (nginx, git, curl)",
                    "packages -> [nginx, git, curl]",
                    "<packages><item>nginx</item></packages>"
                ],
                "correct": "packages:\n  - nginx\n  - git\n  - curl",
                "explanation": "A YAML list begins with `- ` for each element at equal indentation."
            },
            {
                "type": "mcq",
                "question": "What happens if a variable is referenced with `{{ undefined_var }}` but has never been defined anywhere?",
                "options": [
                    "The task fails with an 'undefined variable' error by default",
                    "Ansible silently replaces it with an empty string",
                    "Ansible prompts the user in the console",
                    "Ansible uses the string 'null'"
                ],
                "correct": "The task fails with an 'undefined variable' error by default",
                "explanation": "Ansible enforces strict variable evaluation by default and halts with an 'AnsibleUndefinedVariable' error."
            },
            {
                "type": "true_false",
                "question": "You can provide a default fallback value for a variable in Jinja2 using the filter `{{ my_var | default('fallback_value') }}`.",
                "correct": True,
                "explanation": "The `| default(...)` Jinja2 filter supplies a fallback if the variable is undefined."
            },
            {
                "type": "mcq",
                "question": "Where should host-specific variables be placed in a standard Ansible project directory structure?",
                "options": ["host_vars/<hostname>.yml", "etc/hosts.yml", "playbook_hosts/", "vars/global.yml"],
                "correct": "host_vars/<hostname>.yml",
                "explanation": "Ansible automatically discovers host-specific variables placed in `host_vars/<hostname>.yml`."
            },
            {
                "type": "mcq",
                "question": "Where should group-specific variables be placed in a standard Ansible project directory structure?",
                "options": ["group_vars/<groupname>.yml", "groups/<groupname>.yml", "vars/groups.yml", "inventory/vars.yml"],
                "correct": "group_vars/<groupname>.yml",
                "explanation": "Ansible automatically loads group variables from `group_vars/<groupname>.yml` matching inventory groups."
            },
            {
                "type": "true_false",
                "question": "Variables defined in `vars_prompt:` can hide password input by setting `private: yes`.",
                "correct": True,
                "explanation": "Setting `private: yes` masks the input characters in the terminal, ideal for credentials."
            },
            {
                "type": "mcq",
                "question": "In the precedence hierarchy, which has higher priority: `vars_files` or `playbook vars`?",
                "options": [
                    "`vars_files` (priority #4) is higher precedence than `playbook vars` (priority #3)",
                    "`playbook vars` is higher than `vars_files`",
                    "They are identical and conflict",
                    "Whichever file was created earliest"
                ],
                "correct": "`vars_files` (priority #4) is higher precedence than `playbook vars` (priority #3)",
                "explanation": "Variables loaded from external `vars_files` take precedence over inlined playbook `vars:`."
            },
            {
                "type": "mcq",
                "question": "What is the variable precedence level of `Play vars_prompt` relative to `Play vars`?",
                "options": [
                    "`Play vars` (priority #9) has higher precedence than `vars_prompt` (priority #8)",
                    "`vars_prompt` has higher precedence than `Play vars`",
                    "They are strictly identical in precedence",
                    "`vars_prompt` is lower than role defaults"
                ],
                "correct": "`Play vars` (priority #9) has higher precedence than `vars_prompt` (priority #8)",
                "explanation": "In the 10-level hierarchy, Play vars_prompt is #8 and Play vars is #9, right below Extra vars (#10)."
            },
            {
                "type": "true_false",
                "question": "When defining dictionary variables, nested keys can contain lists and further nested dictionaries.",
                "correct": True,
                "explanation": "YAML dictionaries can be nested to arbitrary depths containing lists, mappings, and scalar values."
            },
            {
                "type": "mcq",
                "question": "How can you inject an environment variable named `MY_VAR` from the shell directly into extra-vars when invoking `ansible-playbook`?",
                "options": [
                    "ansible-playbook playbook.yaml -e \"my_var=$MY_VAR\"",
                    "ansible-playbook playbook.yaml --import-env MY_VAR",
                    "ansible-playbook playbook.yaml -v MY_VAR",
                    "ansible-playbook playbook.yaml --env:MY_VAR"
                ],
                "correct": "ansible-playbook playbook.yaml -e \"my_var=$MY_VAR\"",
                "explanation": "Shell variable expansion `$MY_VAR` inside quotes evaluates before passing into `-e`."
            },
            {
                "type": "mcq",
                "question": "In the following playbook snippet, what will the debug task output?\n\nvars:\n  app_port: 8082\nvars_files:\n  - vars.yml # (contains app_port: 8083)",
                "options": [
                    "8083",
                    "8082",
                    "Both values separated by comma",
                    "Ansible throws a duplicate variable error"
                ],
                "correct": "8083",
                "explanation": "`vars_files` (#4) overrides playbook `vars:` (#3), so `app_port` will evaluate to 8083."
            },
            {
                "type": "true_false",
                "question": "In `vars_prompt:`, setting `private: no` allows the characters entered by the user to be visibly displayed on the console screen as they type.",
                "correct": True,
                "explanation": "`private: no` makes typing visible in the terminal (useful for non-secret values like ports or usernames)."
            }
        ]
    },
    "07-handlers-register-conditionals": {
        "passing_score": 70,
        "questions": [
            {
                "type": "mcq",
                "question": "When do Ansible handlers execute by default during a play?",
                "options": [
                    "At the very end of the play, after all regular tasks have executed",
                    "Immediately when the notifying task finishes",
                    "Before any regular tasks execute",
                    "In a background daemon thread"
                ],
                "correct": "At the very end of the play, after all regular tasks have executed",
                "explanation": "Handlers run once at the end of the play after all tasks succeed, ensuring batch operations like service restarts happen cleanly."
            },
            {
                "type": "mcq",
                "question": "In what order do multiple handlers execute when notified?",
                "options": [
                    "In the order they are defined in the `handlers:` section, NOT the order they were notified",
                    "In the exact order tasks notified them",
                    "In reverse order of notification",
                    "In alphabetical order of handler names"
                ],
                "correct": "In the order they are defined in the `handlers:` section, NOT the order they were notified",
                "explanation": "Handlers strictly run in the order defined within the `handlers:` section of the play."
            },
            {
                "type": "true_false",
                "question": "If a task reports status `ok` (no changes made), any handlers notified by that task will NOT be triggered.",
                "correct": True,
                "explanation": "Handlers are only notified when the notifying task reports a status of `changed`."
            },
            {
                "type": "mcq",
                "question": "If three separate tasks notify the same handler `restart nginx` in a single play, how many times will the handler run?",
                "options": [
                    "Only 1 time",
                    "3 times",
                    "0 times",
                    "Once per task"
                ],
                "correct": "Only 1 time",
                "explanation": "Ansible automatically de-duplicates handlers by name so they run only once per play."
            },
            {
                "type": "mcq",
                "question": "Which keyword in a task is used to trigger a handler?",
                "options": ["notify:", "trigger:", "handler:", "call:"],
                "correct": "notify:",
                "explanation": "The `notify:` keyword points to the name of a handler defined in the `handlers:` section."
            },
            {
                "type": "mcq",
                "question": "How can you force all pending notified handlers to execute immediately in the middle of a play?",
                "options": [
                    "Using the meta task: `ansible.builtin.meta: flush_handlers`",
                    "Calling `ansible.builtin.handler: run`",
                    "Using `--force-handlers` on the command line",
                    "Handlers cannot be forced before the end"
                ],
                "correct": "Using the meta task: `ansible.builtin.meta: flush_handlers`",
                "explanation": "`meta: flush_handlers` flushes and executes all queued handlers at that point in the playbook."
            },
            {
                "type": "true_false",
                "question": "If a play encounters a task failure and stops, pending notified handlers will be skipped by default.",
                "correct": True,
                "explanation": "By default, pending handlers do not run if a previous task fails, unless `--force-handlers` is supplied."
            },
            {
                "type": "mcq",
                "question": "Which keyword controls conditional execution of a task in Ansible?",
                "options": ["when:", "if:", "condition:", "check:"],
                "correct": "when:",
                "explanation": "The `when:` directive evaluates expressions to determine whether a task runs or is skipped."
            },
            {
                "type": "true_false",
                "question": "Inside a `when:` condition statement, variable names must always be enclosed in `{{ }}` braces.",
                "correct": False,
                "explanation": "In `when:` clauses, variables are evaluated directly as raw Python/Jinja expressions WITHOUT `{{ }}` (e.g. `when: result.rc == 0`)."
            },
            {
                "type": "mcq",
                "question": "How do you specify multiple conditions that must ALL be true (logical AND) in a `when:` statement?",
                "options": [
                    "Provide a list of conditions: `when: [cond1, cond2]` or use `when: cond1 and cond2`",
                    "Separate conditions with semicolons",
                    "Provide a comma-separated string `when: \"cond1, cond2\"`",
                    "Ansible only allows one condition per task"
                ],
                "correct": "Provide a list of conditions: `when: [cond1, cond2]` or use `when: cond1 and cond2`",
                "explanation": "Supplying a list under `when:` or using the `and` operator requires all conditions to be satisfied."
            },
            {
                "type": "mcq",
                "question": "How do you express a logical OR condition in a `when:` statement?",
                "options": [
                    "`when: ansible_os_family == 'Debian' or ansible_os_family == 'RedHat'`",
                    "`when: [Debian || RedHat]`",
                    "`when: either(Debian, RedHat)`",
                    "`when.or: [Debian, RedHat]`"
                ],
                "correct": "`when: ansible_os_family == 'Debian' or ansible_os_family == 'RedHat'`",
                "explanation": "The standard Python `or` operator handles logical OR evaluations in `when:` statements."
            },
            {
                "type": "mcq",
                "question": "Which module should you use to check whether a file exists on a target machine before deciding to run a task?",
                "options": ["ansible.builtin.stat", "ansible.builtin.file", "ansible.builtin.exists", "ansible.builtin.check"],
                "correct": "ansible.builtin.stat",
                "explanation": "`ansible.builtin.stat` retrieves file attributes and populates `.stat.exists`."
            },
            {
                "type": "mcq",
                "question": "If you register the result of `ansible.builtin.stat` into `file_info`, what conditional checks if the file exists?",
                "options": [
                    "when: file_info.stat.exists",
                    "when: file_info.exists == true",
                    "when: {{ file_info.stat.exists }}",
                    "when: file_info.found"
                ],
                "correct": "when: file_info.stat.exists",
                "explanation": "The boolean attribute is found at `file_info.stat.exists`."
            },
            {
                "type": "mcq",
                "question": "What is the purpose of the `failed_when:` directive?",
                "options": [
                    "To override Ansible's default failure criteria with a custom conditional expression",
                    "To reboot the system whenever a task fails",
                    "To automatically retry a failed task 10 times",
                    "To send an email when an error occurs"
                ],
                "correct": "To override Ansible's default failure criteria with a custom conditional expression",
                "explanation": "`failed_when:` allows defining custom failure criteria (e.g. `failed_when: \"'ERROR' in result.stderr\"`)."
            },
            {
                "type": "mcq",
                "question": "What is the purpose of the `changed_when:` directive?",
                "options": [
                    "To control whether a task reports a 'changed' status based on a conditional expression",
                    "To alter the system time",
                    "To change the target user dynamically",
                    "To re-run the task if changes occurred"
                ],
                "correct": "To control whether a task reports a 'changed' status based on a conditional expression",
                "explanation": "`changed_when:` customizes whether a task reports `changed=1`, which in turn controls handler notifications."
            },
            {
                "type": "true_false",
                "question": "Setting `changed_when: false` ensures a task will always report `ok` and will NEVER trigger any notified handlers.",
                "correct": True,
                "explanation": "Setting `changed_when: false` prevents read-only queries or status checks from reporting changes or firing handlers."
            },
            {
                "type": "mcq",
                "question": "Which attribute in a registered variable contains error output generated on standard error?",
                "options": [".stderr", ".error", ".stdout_error", ".err"],
                "correct": ".stderr",
                "explanation": "Standard error output is captured in the `.stderr` attribute."
            },
            {
                "type": "true_false",
                "question": "A handler can notify another handler.",
                "correct": True,
                "explanation": "Handlers can include `notify:` directives to trigger subsequent handlers."
            },
            {
                "type": "mcq",
                "question": "If you want a task to continue running even if it encounters an error, which directive should you add to the task?",
                "options": ["ignore_errors: yes", "continue_on_fail: true", "skip_failure: yes", "retry: always"],
                "correct": "ignore_errors: yes",
                "explanation": "`ignore_errors: yes` allows subsequent tasks in the play to continue executing despite task failure."
            },
            {
                "type": "mcq",
                "question": "In a condition like `when: my_var is defined`, what is `is defined`?",
                "options": [
                    "A Jinja2 test that evaluates whether the variable exists",
                    "A Python module call",
                    "An Ansible command-line flag",
                    "A YAML syntax keyword"
                ],
                "correct": "A Jinja2 test that evaluates whether the variable exists",
                "explanation": "`is defined` and `is not defined` are standard Jinja2 tests for checking variable presence."
            },
            {
                "type": "mcq",
                "question": "What is the purpose of the `listen:` keyword in an Ansible handler?",
                "options": [
                    "It binds the handler to an event/topic name, allowing multiple handlers to fire when that topic is notified",
                    "It monitors an audio stream on the server",
                    "It listens on a TCP socket for inbound HTTP requests",
                    "It runs the handler in an infinite listening loop"
                ],
                "correct": "It binds the handler to an event/topic name, allowing multiple handlers to fire when that topic is notified",
                "explanation": "The `listen` directive groups multiple handlers under an event name (e.g. `listen: system updated`), decoupling tasks from specific handler names."
            },
            {
                "type": "true_false",
                "question": "Can handlers have `when:` conditional statements applied directly to them?",
                "correct": True,
                "explanation": "Handlers support `when:` conditionals (e.g. `when: enable_ssl`); if the condition is false, the handler is skipped."
            },
            {
                "type": "mcq",
                "question": "Where are handlers organized when creating structured Ansible Roles?",
                "options": [
                    "In `roles/<role_name>/handlers/main.yml`",
                    "In `roles/<role_name>/tasks/handlers.yml`",
                    "In `roles/<role_name>/vars/handlers.yml`",
                    "In `roles/<role_name>/templates/main.yml`"
                ],
                "correct": "In `roles/<role_name>/handlers/main.yml`",
                "explanation": "Standard role directory structure places handlers in `handlers/main.yml`."
            },
            {
                "type": "mcq",
                "question": "In production service management, why is `state: reloaded` preferred over `state: restarted` when updating configuration files like `nginx.conf`?",
                "options": [
                    "`reloaded` applies new configuration gracefully without dropping active client connections",
                    "`reloaded` is the only state supported on Linux",
                    "`restarted` deletes the application logs",
                    "`reloaded` runs without root permissions"
                ],
                "correct": "`reloaded` applies new configuration gracefully without dropping active client connections",
                "explanation": "A reload instructs the daemon to re-read configuration files while maintaining worker processes for existing connections."
            },
            {
                "type": "mcq",
                "question": "How can a handler validate a configuration file (like `nginx -t`) before restarting the service?",
                "options": [
                    "By grouping validation and restart tasks inside a `block:` in the handler",
                    "By adding `--validate` to the service module",
                    "By running a cron job before the play",
                    "Ansible automatically validates all config files"
                ],
                "correct": "By grouping validation and restart tasks inside a `block:` in the handler",
                "explanation": "Using a `block:` in a handler executes the validation task first; if validation fails, the restart is aborted, protecting the live service."
            },
            {
                "type": "true_false",
                "question": "Handlers should be used for critical tasks that must run every time a playbook executes.",
                "correct": False,
                "explanation": "Handlers only run when a task reports `changed`. Critical tasks that must always execute belong in the main `tasks:` section."
            },
            {
                "type": "mcq",
                "question": "In the PostgreSQL example from the reading, why does the `pg_hba.conf` template task notify `reload postgresql` instead of `restart postgresql`?",
                "options": [
                    "Client authentication changes in `pg_hba.conf` can take effect with a reload, avoiding disruptive database restarts",
                    "PostgreSQL does not support restarting via Ansible",
                    "`pg_hba.conf` requires a complete operating system reboot",
                    "The `service` module cannot restart PostgreSQL"
                ],
                "correct": "Client authentication changes in `pg_hba.conf` can take effect with a reload, avoiding disruptive database restarts",
                "explanation": "`pg_hba.conf` rules can be reloaded on the fly without interrupting active database connections."
            },
            {
                "type": "mcq",
                "question": "In the PostgreSQL handler verification task, which parameters are used to retry checking database connectivity?",
                "options": [
                    "`retries: 3` and `delay: 5`",
                    "`loop: 3` and `sleep: 5`",
                    "`attempt: 3` and `wait: 5`",
                    "`timeout: 15`"
                ],
                "correct": "`retries: 3` and `delay: 5`",
                "explanation": "`retries: 3` and `delay: 5` instruct Ansible to retry the verification check up to 3 times with a 5-second pause between attempts."
            },
            {
                "type": "mcq",
                "question": "What is the result of setting `failed_when: false` on a task running `systemctl status nginx`?",
                "options": [
                    "The task will never report failure, even if systemctl returns a non-zero exit code (e.g. service stopped)",
                    "Ansible ignores all YAML syntax errors in the playbook",
                    "The task runs twice as fast",
                    "The task will never run"
                ],
                "correct": "The task will never report failure, even if systemctl returns a non-zero exit code (e.g. service stopped)",
                "explanation": "By disabling failure evaluation (`failed_when: false`), Ansible allows capturing non-zero exit status without halting the playbook."
            },
            {
                "type": "true_false",
                "question": "A single task can notify multiple handlers by providing a YAML list of handler names under `notify:`.",
                "correct": True,
                "explanation": "A task can specify a list under `notify:` (e.g. `notify: [restart app, clear cache, send notification]`)."
            }
        ]
    },
    "08-loops-tags-best-practices": {
        "passing_score": 70,
        "questions": [
            {
                "type": "mcq",
                "question": "What is the standard, modern keyword used to iterate over items in Ansible tasks?",
                "options": ["loop:", "with_items:", "for_each:", "iterate:"],
                "correct": "loop:",
                "explanation": "`loop:` is the modern, recommended syntax in Ansible for iterating over lists."
            },
            {
                "type": "mcq",
                "question": "What default variable holds the current item during loop execution in a task?",
                "options": ["{{ item }}", "{{ element }}", "{{ value }}", "{{ self }}"],
                "correct": "{{ item }}",
                "explanation": "Ansible exposes the current iteration element as `item`."
            },
            {
                "type": "mcq",
                "question": "How do you access properties when looping over a list of dictionaries (e.g. `[{name: 'alice', role: 'admin'}]`)?",
                "options": [
                    "{{ item.name }} and {{ item.role }}",
                    "{{ item[0] }}",
                    "{{ item->name }}",
                    "{{ this.name }}"
                ],
                "correct": "{{ item.name }} and {{ item.role }}",
                "explanation": "Properties of dictionary items in a loop are accessed via dot notation `{{ item.name }}`."
            },
            {
                "type": "mcq",
                "question": "Which directive allows you to rename the loop variable from `item` to something more descriptive (e.g. `user_account`)?",
                "options": [
                    "loop_control: { loop_var: user_account }",
                    "rename_item: user_account",
                    "var_name: user_account",
                    "as: user_account"
                ],
                "correct": "loop_control: { loop_var: user_account }",
                "explanation": "`loop_control: loop_var` renames the iteration variable, essential when nesting loops."
            },
            {
                "type": "mcq",
                "question": "How do you run only tasks tagged with `deploy` when executing a playbook from the terminal?",
                "options": [
                    "ansible-playbook playbook.yaml --tags deploy",
                    "ansible-playbook playbook.yaml --only deploy",
                    "ansible-playbook playbook.yaml -t:deploy",
                    "ansible-playbook playbook.yaml --filter deploy"
                ],
                "correct": "ansible-playbook playbook.yaml --tags deploy",
                "explanation": "The `--tags` (or `-t`) flag filters execution to tasks matching the specified tag(s)."
            },
            {
                "type": "mcq",
                "question": "How do you skip tasks tagged with `backup` during playbook execution?",
                "options": [
                    "ansible-playbook playbook.yaml --skip-tags backup",
                    "ansible-playbook playbook.yaml --exclude backup",
                    "ansible-playbook playbook.yaml --ignore-tags backup",
                    "ansible-playbook playbook.yaml --without backup"
                ],
                "correct": "ansible-playbook playbook.yaml --skip-tags backup",
                "explanation": "The `--skip-tags` flag bypasses all tasks tagged with the given label."
            },
            {
                "type": "mcq",
                "question": "What is the special behavior of the reserved tag `always` in Ansible?",
                "options": [
                    "Tasks tagged with `always` run by default unless explicitly skipped with `--skip-tags always`",
                    "The task runs in an infinite loop",
                    "The task runs on every computer in the world",
                    "The task cannot fail"
                ],
                "correct": "Tasks tagged with `always` run by default unless explicitly skipped with `--skip-tags always`",
                "explanation": "The `always` tag ensures a task executes even when `--tags` is specified, unless `--skip-tags always` is passed."
            },
            {
                "type": "mcq",
                "question": "What is the special behavior of the reserved tag `never` in Ansible?",
                "options": [
                    "Tasks tagged with `never` are skipped by default unless explicitly requested with `--tags never`",
                    "The task is permanently deleted from the YAML file",
                    "The task never reports changed",
                    "The task will never fail"
                ],
                "correct": "Tasks tagged with `never` are skipped by default unless explicitly requested with `--tags never`",
                "explanation": "The `never` tag acts as a feature flag for optional, on-demand tasks."
            },
            {
                "type": "true_false",
                "question": "It is an Ansible best practice to use dedicated modules (`apt`, `service`, `copy`) rather than generic `command` or `shell` modules whenever possible.",
                "correct": True,
                "explanation": "Dedicated modules enforce idempotency, input validation, and proper return structures, whereas raw shell scripts do not."
            },
            {
                "type": "mcq",
                "question": "Why is it best practice to provide a clear, descriptive `name:` for every task?",
                "options": [
                    "It documents the task's purpose in the playbook and clearly identifies what step is executing in the terminal logs",
                    "Ansible refuses to run unnamed tasks",
                    "It makes the task run twice as fast",
                    "It automatically creates a Git commit"
                ],
                "correct": "It documents the task's purpose in the playbook and clearly identifies what step is executing in the terminal logs",
                "explanation": "Descriptive task names provide clean audit trails in terminal logs and CI/CD pipelines."
            },
            {
                "type": "mcq",
                "question": "Which tool is commonly used to lint Ansible playbooks for best practices, deprecated syntax, and security smells?",
                "options": ["ansible-lint", "yamllint-strict", "flake8-ansible", "ansible-audit"],
                "correct": "ansible-lint",
                "explanation": "`ansible-lint` checks playbooks against official community best practices and rules."
            },
            {
                "type": "true_false",
                "question": "Plain-text passwords and sensitive private keys should be stored directly in playbook variables.",
                "correct": False,
                "explanation": "Secrets should never be stored in plain text; use Ansible Vault (`ansible-vault`) to encrypt sensitive variables."
            },
            {
                "type": "mcq",
                "question": "Can multiple tags be assigned to a single task?",
                "options": [
                    "Yes, by providing a YAML list under `tags:` (e.g. `tags: [deploy, nginx, frontend]`)",
                    "No, only one tag per task is permitted",
                    "Only two tags are allowed per task",
                    "Tags can only be defined at the play level"
                ],
                "correct": "Yes, by providing a YAML list under `tags:` (e.g. `tags: [deploy, nginx, frontend]`)",
                "explanation": "Tasks can be labeled with multiple tags to allow granular selective execution."
            },
            {
                "type": "true_false",
                "question": "When registering a variable inside a loop task, the registered variable will contain a `results` list containing output from every iteration.",
                "correct": True,
                "explanation": "Loop tasks record per-iteration execution data in the `.results` list attribute."
            },
            {
                "type": "mcq",
                "question": "What is the recommended tool for managing and encrypting sensitive secrets within an Ansible project?",
                "options": ["Ansible Vault (`ansible-vault`)", "GnuPG manually", "Base64 encoding", "MD5 hashing"],
                "correct": "Ansible Vault (`ansible-vault`)",
                "explanation": "Ansible Vault encrypts sensitive files and variables with AES-256 encryption."
            },
            {
                "type": "mcq",
                "question": "How can you loop over a dictionary (e.g. file paths and permission modes) in Ansible?",
                "options": [
                    "Using `loop: \"{{ lookup('dict', file_permissions) }}\"` and accessing `item.key` and `item.value`",
                    "Using `loop: file_permissions.keys()`",
                    "Using `with_dict: file_permissions` only (loop is unsupported for dicts)",
                    "Ansible cannot loop over dictionary mappings"
                ],
                "correct": "Using `loop: \"{{ lookup('dict', file_permissions) }}\"` and accessing `item.key` and `item.value`",
                "explanation": "The `lookup('dict', dict_var)` plugin transforms a dictionary into a list of key/value pairs accessible via `{{ item.key }}` and `{{ item.value }}`."
            },
            {
                "type": "mcq",
                "question": "Which command-line flag lists all available tags in a playbook without executing any tasks?",
                "options": ["--list-tags", "--show-tags", "--tags-list", "-l-tags"],
                "correct": "--list-tags",
                "explanation": "`ansible-playbook playbook.yaml --list-tags` outputs all tags declared across the plays."
            },
            {
                "type": "mcq",
                "question": "How do you specify multiple tags to execute simultaneously with the `--tags` flag?",
                "options": [
                    "--tags \"install,config\"",
                    "--tags install + config",
                    "--tags install AND config",
                    "--tags [install, config]"
                ],
                "correct": "--tags \"install,config\"",
                "explanation": "Multiple tags are passed as a comma-separated string: `--tags \"install,config\"`."
            },
            {
                "type": "mcq",
                "question": "According to Ansible naming conventions, what should be included in task names to make them clear and actionable?",
                "options": [
                    "Action verbs (e.g. 'Install nginx web server', 'Copy configuration file')",
                    "Host IP addresses",
                    "The author's initials",
                    "Timestamp of creation"
                ],
                "correct": "Action verbs (e.g. 'Install nginx web server', 'Copy configuration file')",
                "explanation": "Best practices dictate including verbs in task names to clearly describe the action being taken."
            },
            {
                "type": "true_false",
                "question": "In the web server practical example, setting `enabled: yes` on the service module ensures the service starts automatically upon system boot.",
                "correct": True,
                "explanation": "`enabled: yes` configures the init system (e.g. systemd) to start the service at boot."
            },
            {
                "type": "mcq",
                "question": "In the practical example for system maintenance, which module safely handles system reboot with delay and status checking?",
                "options": ["ansible.builtin.reboot", "ansible.builtin.command: /sbin/reboot", "ansible.builtin.shell: init 6", "ansible.builtin.restart"],
                "correct": "ansible.builtin.reboot",
                "explanation": "The dedicated `ansible.builtin.reboot` module reboots the host, disconnects cleanly, waits for the host to come back online, and verifies SSH responsiveness."
            },
            {
                "type": "mcq",
                "question": "In the maintenance example, what indicates on Debian/Ubuntu systems that a reboot is required after package upgrades?",
                "options": [
                    "The existence of `/var/run/reboot-required` file",
                    "An exit code of 99 from apt",
                    "The `/etc/reboot` directory",
                    "A pop-up message in syslog"
                ],
                "correct": "The existence of `/var/run/reboot-required` file",
                "explanation": "Debian and Ubuntu systems create the `/var/run/reboot-required` sentinel file when an installed package requires a reboot."
            },
            {
                "type": "true_false",
                "question": "Running `ansible-playbook playbook.yaml --check` on a playbook that uses raw `command` or `shell` tasks may still execute changes on the target system.",
                "correct": True,
                "explanation": "`command` and `shell` modules do not know what the underlying script does and cannot predict changes; by default, they do not run in check mode unless `check_mode: yes` is forced."
            },
            {
                "type": "mcq",
                "question": "What parameter in `ansible.builtin.reboot` specifies how many seconds to wait before rebooting the server?",
                "options": ["pre_reboot_delay", "delay_before", "wait_seconds", "sleep"],
                "correct": "pre_reboot_delay",
                "explanation": "`pre_reboot_delay: 10` waits 10 seconds before initiating the reboot."
            },
            {
                "type": "true_false",
                "question": "You can assign both `install` and `packages` tags to a single task simultaneously.",
                "correct": True,
                "explanation": "Tasks accept a YAML list of tags: `tags: [install, packages]`."
            }
        ]
    }
}

def main():
    total_q = 0
    for slug, q_data in CHUNKS_QUIZZES.items():
        quiz_file = PROCESSED_DIR / f"{slug}.quiz.yaml"
        count = len(q_data["questions"])
        total_q += count
        with open(quiz_file, "w", encoding="utf-8") as f:
            yaml.dump(q_data, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
        print(f"✓ Saved {count:2d} questions to {quiz_file.name}")

    # Update _module.yaml
    mod_file = PROCESSED_DIR / "_module.yaml"
    with open(mod_file, "r", encoding="utf-8") as f:
        mod_meta = yaml.safe_load(f)

    mod_meta["total_questions"] = total_q
    for ch in mod_meta["chunks"]:
        if ch["slug"] in CHUNKS_QUIZZES:
            ch["question_count"] = len(CHUNKS_QUIZZES[ch["slug"]]["questions"])

    with open(mod_file, "w", encoding="utf-8") as f:
        yaml.dump(mod_meta, f, sort_keys=False, default_flow_style=False)
    print(f"\n🎉 Successfully updated all quiz files! Total questions across 004-playbooks: {total_q}")

if __name__ == "__main__":
    main()
