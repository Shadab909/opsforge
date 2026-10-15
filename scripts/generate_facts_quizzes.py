#!/usr/bin/env python3
"""
Generate comprehensive, exhaustive quiz questions for Ansible Facts (Module 005).
Ensures every concept, syntax rule, command flag, and edge case from the reading
sections is rigorously tested.
"""

import yaml
from pathlib import Path

FACTS_DIR = Path(__file__).resolve().parent.parent / "processed" / "ansible" / "005-facts"

CHUNKS_QUIZZES = {
    "01-how-to-view-facts": {
        "passing_score": 70,
        "questions": [
            {
                "type": "mcq",
                "question": "What are Ansible facts?",
                "options": [
                    "Dynamic system information automatically discovered from remote target nodes at runtime",
                    "Hardcoded configuration parameters inside ansible.cfg",
                    "License keys required to execute playbooks",
                    "Static comments written inside YAML files"
                ],
                "correct": "Dynamic system information automatically discovered from remote target nodes at runtime",
                "explanation": "Ansible facts are data points representing the remote target nodes (OS, IP, memory, disks, CPU) discovered dynamically at runtime."
            },
            {
                "type": "mcq",
                "question": "Which core Ansible module is responsible for discovering and gathering facts from remote nodes?",
                "options": ["ansible.builtin.setup", "ansible.builtin.facts", "ansible.builtin.discover", "ansible.builtin.system_info"],
                "correct": "ansible.builtin.setup",
                "explanation": "The `setup` module is the dedicated builtin module that inspects target machines and returns fact data."
            },
            {
                "type": "mcq",
                "question": "Which ad-hoc command gathers and displays all facts from all inventory hosts?",
                "options": [
                    "ansible all -m setup",
                    "ansible all -a 'facts'",
                    "ansible-playbook --facts all",
                    "ansible-setup all"
                ],
                "correct": "ansible all -m setup",
                "explanation": "Executing `ansible all -m setup` invokes the setup module across all target hosts in the inventory."
            },
            {
                "type": "true_false",
                "question": "Ansible facts are gathered by target nodes and sent back to the controller node.",
                "correct": True,
                "explanation": "Fact gathering executes on the managed nodes and the resulting system profile is returned as JSON to the control machine."
            },
            {
                "type": "mcq",
                "question": "What is the top-level JSON key containing all discovered system facts in Ansible output?",
                "options": ["ansible_facts", "host_data", "system_specs", "remote_info"],
                "correct": "ansible_facts",
                "explanation": "All discovered attributes are nested under the primary `ansible_facts` dictionary."
            },
            {
                "type": "mcq",
                "question": "Which CLI flag allows exporting gathered facts from all hosts into individual JSON files inside a local directory?",
                "options": ["--tree <directory>", "--export <directory>", "--save-facts <directory>", "--output-dir <directory>"],
                "correct": "--tree <directory>",
                "explanation": "The `--tree /path/to/dir` option instructs Ansible to save the JSON output for each host in a separate file named by hostname."
            },
            {
                "type": "true_false",
                "question": "Ansible requires installing a permanent background agent daemon on remote hosts to query facts.",
                "correct": False,
                "explanation": "Ansible is agentless; it uses SSH/WinRM and temporary Python execution to query system information."
            },
            {
                "type": "mcq",
                "question": "How do you view facts for a single host named `linux-server-1` without modifying your inventory file?",
                "options": [
                    "ansible linux-server-1 -m setup",
                    "ansible all -m setup --host linux-server-1",
                    "ansible-facts linux-server-1",
                    "ansible setup linux-server-1"
                ],
                "correct": "ansible linux-server-1 -m setup",
                "explanation": "Supplying the specific hostname as the pattern argument targets only that machine."
            },
            {
                "type": "mcq",
                "question": "What task automatically runs by default at the start of every Ansible play unless explicitly disabled?",
                "options": [
                    "TASK [Gathering Facts]",
                    "TASK [Checking SSH]",
                    "TASK [Validating Python]",
                    "TASK [Syncing Time]"
                ],
                "correct": "TASK [Gathering Facts]",
                "explanation": "At the start of each play, Ansible initiates `TASK [Gathering Facts]` to discover system properties before other tasks execute."
            },
            {
                "type": "mcq",
                "question": "Which module and argument would you use in a playbook task to print the entire gathered facts dictionary?",
                "options": [
                    "ansible.builtin.debug with `var: ansible_facts`",
                    "ansible.builtin.command with `print facts`",
                    "ansible.builtin.shell with `echo $FACTS`",
                    "ansible.builtin.setup with `display: true`"
                ],
                "correct": "ansible.builtin.debug with `var: ansible_facts`",
                "explanation": "`debug: var: ansible_facts` prints the full data structure of all discovered facts."
            },
            {
                "type": "true_false",
                "question": "Ansible facts can only be collected from Linux systems, not from Windows or macOS nodes.",
                "correct": False,
                "explanation": "Ansible discovers facts across Linux, macOS, BSD, and Windows machines (via PowerShell and WinRM)."
            },
            {
                "type": "mcq",
                "question": "When facts are collected by the controller, where can they be referenced?",
                "options": [
                    "Across all subsequent tasks, handlers, conditionals, and Jinja2 templates in that play",
                    "Only inside the inventory file",
                    "Only in shell scripts on the controller",
                    "Only inside `ansible.cfg`"
                ],
                "correct": "Across all subsequent tasks, handlers, conditionals, and Jinja2 templates in that play",
                "explanation": "Gathered facts populate variables that are immediately available for template rendering and task conditionals."
            },
            {
                "type": "mcq",
                "question": "In the JSON output of the setup module, what data type is `ansible_facts`?",
                "options": ["A JSON Object (dictionary)", "A JSON Array (list)", "A String", "An Integer"],
                "correct": "A JSON Object (dictionary)",
                "explanation": "`ansible_facts` is a hierarchical dictionary mapping fact names to values and nested dictionaries."
            },
            {
                "type": "true_false",
                "question": "Files created by `ansible all -m setup --tree /tmp/facts` are named after each target host's inventory name.",
                "correct": True,
                "explanation": "The `--tree` argument indexes output files using each machine's inventory hostname."
            },
            {
                "type": "mcq",
                "question": "Which command would you use to verify that the setup module is available and responsive on localhost?",
                "options": [
                    "ansible localhost -m setup",
                    "ansible-playbook setup.yml",
                    "setup --test",
                    "ansible --check-facts"
                ],
                "correct": "ansible localhost -m setup",
                "explanation": "Running `ansible localhost -m setup` queries facts locally on the controller node."
            }
        ]
    },
    "02-how-to-use-facts-in-playbooks": {
        "passing_score": 70,
        "questions": [
            {
                "type": "mcq",
                "question": "What is the recommended modern syntax for accessing the `distribution` fact in an Ansible task?",
                "options": [
                    "{{ ansible_facts['distribution'] }}",
                    "{{ facts.distribution }}",
                    "$(ansible_distribution)",
                    "@ansible_distribution"
                ],
                "correct": "{{ ansible_facts['distribution'] }}",
                "explanation": "Modern Ansible recommends using the scoped `ansible_facts['key']` syntax to prevent namespace collisions."
            },
            {
                "type": "mcq",
                "question": "How are facts formatted when using legacy top-level variable names?",
                "options": [
                    "They are prefixed with `ansible_` (e.g. `ansible_distribution`)",
                    "They are suffixed with `_fact`",
                    "They are capitalized (e.g. `UBUNTU_OS`)",
                    "They begin with a dollar sign `$ansible`"
                ],
                "correct": "They are prefixed with `ansible_` (e.g. `ansible_distribution`)",
                "explanation": "Legacy fact variables inject into the play scope prefixed with `ansible_` (e.g. `ansible_architecture`)."
            },
            {
                "type": "true_false",
                "question": "When using facts inside a `when:` conditional statement, you should wrap the fact in double curly braces `{{ }}`.",
                "correct": False,
                "explanation": "In `when:` clauses, variables must NOT be enclosed in `{{ }}`; they are evaluated directly as raw Python/Jinja2 expressions (e.g. `when: ansible_distribution == 'Ubuntu'`)."
            },
            {
                "type": "mcq",
                "question": "Which conditional expression correctly runs a task only when the target machine is running CentOS?",
                "options": [
                    "when: ansible_distribution == \"CentOS\"",
                    "when: {{ ansible_distribution == \"CentOS\" }}",
                    "if: ansible_distribution == \"CentOS\"",
                    "when: ansible_distribution is \"CentOS\""
                ],
                "correct": "when: ansible_distribution == \"CentOS\"",
                "explanation": "Standard Jinja2 equality `==` without curly braces is the correct syntax for `when:` directives."
            },
            {
                "type": "mcq",
                "question": "Which package manager module is typically paired with `when: ansible_os_family == 'Debian'`?",
                "options": ["ansible.builtin.apt", "ansible.builtin.dnf", "ansible.builtin.yum", "ansible.builtin.zypper"],
                "correct": "ansible.builtin.apt",
                "explanation": "Debian-family distributions (Debian, Ubuntu, Mint) utilize `apt` for package management."
            },
            {
                "type": "mcq",
                "question": "Which package manager module is typically paired with `when: ansible_os_family == 'RedHat'` on modern systems?",
                "options": ["ansible.builtin.dnf (or yum)", "ansible.builtin.apt", "ansible.builtin.pacman", "ansible.builtin.apk"],
                "correct": "ansible.builtin.dnf (or yum)",
                "explanation": "RedHat-family distributions (RHEL, CentOS, Fedora, Rocky) utilize `dnf` or `yum`."
            },
            {
                "type": "mcq",
                "question": "How do you access the total physical memory in megabytes from the `ansible_memory_mb` nested dictionary using dot notation?",
                "options": [
                    "ansible_memory_mb.real.total",
                    "ansible_memory_mb->real->total",
                    "ansible_memory_mb:real:total",
                    "ansible_memory_mb.total"
                ],
                "correct": "ansible_memory_mb.real.total",
                "explanation": "The total physical memory is accessed via `ansible_memory_mb.real.total`."
            },
            {
                "type": "mcq",
                "question": "Which conditional triggers a task only if the target machine has less than 4000 MB of total RAM?",
                "options": [
                    "when: ansible_memory_mb.real.total < 4000",
                    "when: ansible_memory_mb.real.total lt 4000",
                    "when: {{ ansible_memory_mb.real.total < 4000 }}",
                    "when: memory < 4000MB"
                ],
                "correct": "when: ansible_memory_mb.real.total < 4000",
                "explanation": "Numerical comparison operators (`<`, `>`, `<=`, `>=`) evaluate integer values directly in `when:` statements."
            },
            {
                "type": "true_false",
                "question": "Both dot notation (`ansible_memory_mb.real.total`) and bracket notation (`ansible_memory_mb['real']['total']`) are valid in Ansible.",
                "correct": True,
                "explanation": "Ansible's Jinja2 engine supports both dot and bracket syntax for traversing dictionaries."
            },
            {
                "type": "mcq",
                "question": "Why is bracket notation (`ansible_facts['default_ipv4']['address']`) sometimes preferred over dot notation?",
                "options": [
                    "Bracket notation safely handles keys containing hyphens, spaces, or Python reserved keyword names",
                    "Bracket notation executes 10 times faster",
                    "Dot notation is deprecated in Ansible 2.0",
                    "Dot notation only works on Windows"
                ],
                "correct": "Bracket notation safely handles keys containing hyphens, spaces, or Python reserved keyword names",
                "explanation": "When dictionary keys contain special characters (like hyphens or dots) or collide with Python methods, bracket notation avoids syntax errors."
            },
            {
                "type": "true_false",
                "question": "If you query an undefined fact in a `when:` conditional without checking if it is defined, Ansible will raise an 'undefined variable' error by default.",
                "correct": True,
                "explanation": "Ansible enforces strict variable evaluation, failing the task if an undefined fact is referenced without `| default` or `is defined`."
            },
            {
                "type": "mcq",
                "question": "What is the primary operational advantage of using facts in playbooks instead of writing separate playbooks for each OS?",
                "options": [
                    "A single playbook can dynamically manage heterogeneous environments (Ubuntu, CentOS, Debian) with conditional logic",
                    "It eliminates the need for an inventory file",
                    "It removes the need to use SSH keys",
                    "It compiles the playbook into machine bytecode"
                ],
                "correct": "A single playbook can dynamically manage heterogeneous environments (Ubuntu, CentOS, Debian) with conditional logic",
                "explanation": "Facts allow multi-platform playbooks to adapt dynamically to whichever distribution is running on the target node."
            },
            {
                "type": "true_false",
                "question": "You can combine multiple fact conditions in a single `when:` statement using `and` and `or` logical operators.",
                "correct": True,
                "explanation": "Standard boolean operators (`and`, `or`, `not`) allow complex composite conditions (e.g. `when: ansible_os_family == 'Debian' and ansible_memory_mb.real.total >= 2048`)."
            },
            {
                "type": "mcq",
                "question": "In the task snippet below, what happens if the target machine is running Rocky Linux?\n\n- name: Install web service\n  apt:\n    name: nginx\n    state: present\n  when: ansible_distribution == 'Ubuntu'",
                "options": [
                    "The task is skipped (`skipped=1`)",
                    "The task fails with a fatal error",
                    "The task installs nginx using dnf",
                    "Ansible reboots the machine"
                ],
                "correct": "The task is skipped (`skipped=1`)",
                "explanation": "Because `ansible_distribution == 'Ubuntu'` evaluates to false on Rocky Linux, Ansible skips the task without failure."
            },
            {
                "type": "mcq",
                "question": "How can you check if a target machine has an active default IPv4 gateway configured?",
                "options": [
                    "when: ansible_default_ipv4.gateway is defined",
                    "when: default_gateway == true",
                    "when: ping(gateway) == 0",
                    "when: has_gateway()"
                ],
                "correct": "when: ansible_default_ipv4.gateway is defined",
                "explanation": "The Jinja2 test `is defined` verifies whether the `gateway` property was discovered."
            },
            {
                "type": "true_false",
                "question": "Fact variables can be used inside Jinja2 template files (`.j2`) deployed with the `ansible.builtin.template` module.",
                "correct": True,
                "explanation": "All discovered facts are available inside templates, making it easy to populate configuration files with dynamic host IPs, hostnames, and memory limits."
            },
            {
                "type": "mcq",
                "question": "Which fact would you reference to configure an Nginx virtual host with the machine's primary IP address?",
                "options": [
                    "{{ ansible_default_ipv4.address }}",
                    "{{ ansible_ip }}",
                    "{{ host.primary_ip }}",
                    "{{ ip_address }}"
                ],
                "correct": "{{ ansible_default_ipv4.address }}",
                "explanation": "`ansible_default_ipv4.address` contains the IP address of the primary network interface."
            },
            {
                "type": "true_false",
                "question": "A task with `when: ansible_distribution in ['Ubuntu', 'Debian']` is valid Jinja2 syntax in Ansible.",
                "correct": True,
                "explanation": "The `in` operator checks for membership in a list of distributions."
            }
        ]
    },
    "03-commonly-used-facts": {
        "passing_score": 70,
        "questions": [
            {
                "type": "mcq",
                "question": "What is the difference between `ansible_distribution` and `ansible_os_family`?",
                "options": [
                    "`ansible_distribution` identifies the specific OS (e.g. 'Ubuntu', 'Rocky'), while `ansible_os_family` identifies the broader lineage (e.g. 'Debian', 'RedHat')",
                    "`ansible_distribution` is for Linux; `ansible_os_family` is only for Windows",
                    "`ansible_os_family` is deprecated",
                    "They are identical aliases for the exact same string"
                ],
                "correct": "`ansible_distribution` identifies the specific OS (e.g. 'Ubuntu', 'Rocky'), while `ansible_os_family` identifies the broader lineage (e.g. 'Debian', 'RedHat')",
                "explanation": "`ansible_os_family` groups distributions into broad families ('Debian', 'RedHat', 'Archlinux', 'Windows'), whereas `ansible_distribution` names the exact distro."
            },
            {
                "type": "mcq",
                "question": "If target node A is running Ubuntu 22.04 and target node B is running Debian 11, what will `ansible_os_family` evaluate to on both nodes?",
                "options": ["Debian", "Ubuntu", "Linux", "POSIX"],
                "correct": "Debian",
                "explanation": "Both Ubuntu and Debian belong to the `Debian` OS family."
            },
            {
                "type": "mcq",
                "question": "Which fact contains the short hostname of the target node without domain components?",
                "options": ["ansible_hostname", "ansible_fqdn", "ansible_nodename", "ansible_domain"],
                "correct": "ansible_hostname",
                "explanation": "`ansible_hostname` reports the short hostname, whereas `ansible_fqdn` reports the fully qualified domain name."
            },
            {
                "type": "mcq",
                "question": "Which fact reports the Fully Qualified Domain Name (e.g. `app1.us-east.example.com`)?",
                "options": ["ansible_fqdn", "ansible_hostname", "ansible_domain", "ansible_full_name"],
                "correct": "ansible_fqdn",
                "explanation": "`ansible_fqdn` contains the complete domain-qualified hostname."
            },
            {
                "type": "mcq",
                "question": "Which fact contains the CPU hardware architecture (e.g. `x86_64` or `aarch64`)?",
                "options": ["ansible_architecture", "ansible_cpu_type", "ansible_hardware", "ansible_arch_family"],
                "correct": "ansible_architecture",
                "explanation": "`ansible_architecture` reports CPU architecture like `x86_64`, `aarch64`, or `armv7l`."
            },
            {
                "type": "mcq",
                "question": "Which fact contains a list of all IPv4 addresses assigned to all network interfaces on the target host?",
                "options": ["ansible_all_ipv4_addresses", "ansible_interfaces_ip", "ansible_ips", "ansible_net_addresses"],
                "correct": "ansible_all_ipv4_addresses",
                "explanation": "`ansible_all_ipv4_addresses` returns a list of all IPv4 addresses across all interfaces on the node."
            },
            {
                "type": "mcq",
                "question": "Which fact contains the list of DNS nameserver IP addresses configured on the target machine?",
                "options": ["ansible_dns.nameservers", "ansible_nameservers", "ansible_network.dns", "ansible_resolv_conf"],
                "correct": "ansible_dns.nameservers",
                "explanation": "`ansible_dns.nameservers` extracts the list of DNS resolvers from `/etc/resolv.conf`."
            },
            {
                "type": "mcq",
                "question": "Which fact represents the total physical RAM of the host in Megabytes?",
                "options": ["ansible_memory_mb.real.total", "ansible_memtotal_mb", "ansible_memory.total", "ansible_ram_size"],
                "correct": "ansible_memory_mb.real.total",
                "explanation": "`ansible_memory_mb.real.total` provides the total physical memory in megabytes as an integer."
            },
            {
                "type": "mcq",
                "question": "Which fact reports the total amount of swap space in Megabytes?",
                "options": ["ansible_memory_mb.swap.total", "ansible_swap_mb", "ansible_swap_total", "ansible_virtual_memory.swap"],
                "correct": "ansible_memory_mb.swap.total",
                "explanation": "`ansible_memory_mb.swap.total` provides the configured swap capacity in megabytes."
            },
            {
                "type": "mcq",
                "question": "Which fact returns the total number of logical virtual CPUs (threads/vCPUs)?",
                "options": ["ansible_processor_vcpus", "ansible_processor_count", "ansible_processor_cores", "ansible_threads"],
                "correct": "ansible_processor_vcpus",
                "explanation": "`ansible_processor_vcpus` reports the total number of logical processors/vCPUs available to the operating system."
            },
            {
                "type": "mcq",
                "question": "What does `ansible_processor_count` report?",
                "options": [
                    "The number of physical CPU sockets",
                    "The number of CPU cores per socket",
                    "The clock speed in GHz",
                    "The processor cache size"
                ],
                "correct": "The number of physical CPU sockets",
                "explanation": "`ansible_processor_count` reports the count of physical CPU sockets."
            },
            {
                "type": "mcq",
                "question": "Which fact reports the primary network interface name associated with the default route (e.g. `eth0` or `ens3`)?",
                "options": ["ansible_default_ipv4.interface", "ansible_default_interface", "ansible_primary_nic", "ansible_interface_name"],
                "correct": "ansible_default_ipv4.interface",
                "explanation": "`ansible_default_ipv4.interface` provides the interface name for default IPv4 routing."
            },
            {
                "type": "mcq",
                "question": "Which fact reports the current remote login user account running the task?",
                "options": ["ansible_user (or ansible_user_id)", "ansible_login", "ansible_account", "ansible_whoami"],
                "correct": "ansible_user (or ansible_user_id)",
                "explanation": "`ansible_user` (and `ansible_user_id`) reports the username executing the task on the target host."
            },
            {
                "type": "true_false",
                "question": "On an AlmaLinux or Rocky Linux server, `ansible_os_family` will report 'RedHat'.",
                "correct": True,
                "explanation": "AlmaLinux, Rocky Linux, CentOS, Fedora, and RHEL all report `RedHat` as their `ansible_os_family`."
            },
            {
                "type": "mcq",
                "question": "Which fact contains the distribution major version string (such as '22.04' or '9.1')?",
                "options": ["ansible_distribution_version", "ansible_os_version", "ansible_version_id", "ansible_release_number"],
                "correct": "ansible_distribution_version",
                "explanation": "`ansible_distribution_version` holds the distribution version number."
            },
            {
                "type": "true_false",
                "question": "The fact `ansible_default_ipv4.gateway` contains the default gateway's IP address.",
                "correct": True,
                "explanation": "`ansible_default_ipv4.gateway` stores the default gateway IPv4 address."
            },
            {
                "type": "mcq",
                "question": "Which fact contains the distribution release codename (e.g. 'jammy' for Ubuntu 22.04)?",
                "options": ["ansible_distribution_release", "ansible_codename", "ansible_release_tag", "ansible_dist_name"],
                "correct": "ansible_distribution_release",
                "explanation": "`ansible_distribution_release` provides the official release codename."
            },
            {
                "type": "true_false",
                "question": "`ansible_memory_mb.real.free` provides the amount of unused RAM in megabytes.",
                "correct": True,
                "explanation": "`real.free` indicates free memory available in MB."
            },
            {
                "type": "mcq",
                "question": "If you want to configure an NTP or time service only on x86_64 machines, what condition should you use?",
                "options": [
                    "when: ansible_architecture == 'x86_64'",
                    "when: ansible_cpu == 'intel'",
                    "when: ansible_arch == 64",
                    "when: x86_64"
                ],
                "correct": "when: ansible_architecture == 'x86_64'",
                "explanation": "`ansible_architecture == 'x86_64'` checks the CPU architecture."
            },
            {
                "type": "true_false",
                "question": "`ansible_processor_cores` reports the number of cores per physical processor.",
                "correct": True,
                "explanation": "`ansible_processor_cores` reports cores per socket."
            }
        ]
    },
    "04-disabling-fact-gathering": {
        "passing_score": 70,
        "questions": [
            {
                "type": "mcq",
                "question": "What is the primary reason for disabling fact gathering in an Ansible playbook?",
                "options": [
                    "To significantly increase playbook execution speed and reduce network overhead across large inventories",
                    "Because facts are deprecated in Ansible",
                    "Because fact gathering requires root privileges",
                    "To prevent Ansible from connecting to remote hosts"
                ],
                "correct": "To significantly increase playbook execution speed and reduce network overhead across large inventories",
                "explanation": "Fact gathering inspects system devices and transfers JSON over SSH. Disabling it skips this overhead, speeding up runs across large server fleets."
            },
            {
                "type": "mcq",
                "question": "Which play-level directive disables fact gathering?",
                "options": [
                    "gather_facts: no (or gather_facts: false)",
                    "facts: disable",
                    "skip_facts: true",
                    "no_facts: yes"
                ],
                "correct": "gather_facts: no (or gather_facts: false)",
                "explanation": "Setting `gather_facts: no` or `gather_facts: false` at the play level disables automatic fact gathering."
            },
            {
                "type": "true_false",
                "question": "If a play has `gather_facts: no`, you cannot use any `ansible_*` system facts in tasks unless you manually invoke the setup module later.",
                "correct": True,
                "explanation": "Without fact gathering, system facts (`ansible_distribution`, `ansible_default_ipv4`, etc.) will be undefined unless explicitly gathered."
            },
            {
                "type": "mcq",
                "question": "How can you manually gather facts in the middle of a play that started with `gather_facts: no`?",
                "options": [
                    "Add a task calling the `ansible.builtin.setup` module",
                    "Add `gather_facts: yes` to a task",
                    "Run `ansible-facts --refresh`",
                    "You cannot gather facts once disabled"
                ],
                "correct": "Add a task calling the `ansible.builtin.setup` module",
                "explanation": "Executing the `setup` module as a task triggers fact gathering on-demand whenever needed."
            },
            {
                "type": "mcq",
                "question": "Which parameter of the `setup` module allows restricting fact collection to specific categories (e.g. only network facts)?",
                "options": ["gather_subset:", "categories:", "include_facts:", "scope:"],
                "correct": "gather_subset:",
                "explanation": "The `gather_subset:` parameter controls which subsets of facts are collected (e.g. `network`, `hardware`, `virtual`)."
            },
            {
                "type": "mcq",
                "question": "How do you exclude the default fact collection and gather ONLY network facts using `gather_subset`?",
                "options": [
                    "gather_subset: ['!all', '!min', 'network']",
                    "gather_subset: ['only_network']",
                    "gather_subset: 'network_only'",
                    "gather_subset: ['none', 'network']"
                ],
                "correct": "gather_subset: ['!all', '!min', 'network']",
                "explanation": "The exclamation mark `!` negates subsets (`!all`, `!min`), followed by `'network'` to collect only networking data."
            },
            {
                "type": "true_false",
                "question": "For a playbook that only copies a static configuration file and restarts a Docker container, disabling fact gathering is considered a performance best practice.",
                "correct": True,
                "explanation": "If tasks do not depend on system facts, skipping fact gathering saves startup time on every host."
            },
            {
                "type": "mcq",
                "question": "Which of the following is NOT a valid subset name for the `gather_subset` parameter?",
                "options": ["docker_containers", "hardware", "network", "virtual"],
                "correct": "docker_containers",
                "explanation": "Standard subsets in the setup module are `all`, `min`, `hardware`, `network`, `virtual`, `ohai`, and `facter`."
            },
            {
                "type": "true_false",
                "question": "Pre-pending an exclamation mark `!` to a subset name in `gather_subset` instructs Ansible to exclude that subset from collection.",
                "correct": True,
                "explanation": "`!` acts as a negation operator in `gather_subset` lists."
            },
            {
                "type": "mcq",
                "question": "In what configuration file can you configure persistent Fact Caching (e.g. using JSON or Redis) across playbook runs?",
                "options": ["ansible.cfg", "inventory.ini", "playbook.yaml", "facts.conf"],
                "correct": "ansible.cfg",
                "explanation": "Fact caching is configured in `ansible.cfg` under `[defaults]` using `fact_caching` and `fact_caching_connection`."
            },
            {
                "type": "true_false",
                "question": "When Fact Caching is enabled in `ansible.cfg`, Ansible can retrieve cached facts even when `gather_facts: no` is declared in a play.",
                "correct": True,
                "explanation": "Fact caching preserves fact data between runs so subsequent plays can access them without re-querying nodes."
            },
            {
                "type": "mcq",
                "question": "What happens if a play sets `gather_facts: no` but a task references `when: ansible_distribution == 'Ubuntu'` without fact caching?",
                "options": [
                    "The task fails with an 'AnsibleUndefinedVariable: ansible_distribution is undefined' error",
                    "Ansible automatically pauses and gathers facts silently",
                    "The conditional defaults to true",
                    "The task is converted to an ad-hoc command"
                ],
                "correct": "The task fails with an 'AnsibleUndefinedVariable: ansible_distribution is undefined' error",
                "explanation": "Because facts were not gathered, `ansible_distribution` does not exist, triggering an undefined variable error."
            },
            {
                "type": "mcq",
                "question": "Which fact gathering subset contains facts related to hypervisors, virtualization technology, and guest/host detection?",
                "options": ["virtual", "hypervisor", "cloud", "container"],
                "correct": "virtual",
                "explanation": "The `virtual` subset populates facts like `ansible_virtualization_type` and `ansible_virtualization_role`."
            },
            {
                "type": "true_false",
                "question": "`gather_facts: false` and `gather_facts: no` are functionally identical in Ansible YAML syntax.",
                "correct": True,
                "explanation": "In YAML, `false` and `no` parse to the same boolean false value."
            },
            {
                "type": "mcq",
                "question": "What minimal subset collects only basic identification facts without querying storage devices or network routes?",
                "options": ["min", "basic", "quick", "core"],
                "correct": "min",
                "explanation": "The `min` subset gathers minimal facts required for basic host identification."
            },
            {
                "type": "true_false",
                "question": "Disabling fact gathering has the highest performance benefit when managing hundreds of servers across high-latency networks.",
                "correct": True,
                "explanation": "Skipping SSH round-trips and payload transfers for hundreds of hosts saves substantial execution time."
            }
        ]
    },
    "05-custom-facts": {
        "passing_score": 70,
        "questions": [
            {
                "type": "mcq",
                "question": "On a remote managed host, in which directory must local custom fact files be located?",
                "options": [
                    "/etc/ansible/facts.d/",
                    "/etc/ansible/custom/",
                    "/var/lib/ansible/facts/",
                    "/usr/local/ansible/facts/"
                ],
                "correct": "/etc/ansible/facts.d/",
                "explanation": "Ansible automatically searches the `/etc/ansible/facts.d/` directory on target machines for custom `.fact` files."
            },
            {
                "type": "mcq",
                "question": "What file extension must local custom fact files have in `/etc/ansible/facts.d/`?",
                "options": [".fact", ".custom", ".yml", ".json"],
                "correct": ".fact",
                "explanation": "Custom fact files must end with the `.fact` extension."
            },
            {
                "type": "mcq",
                "question": "Which data formats are valid for static `.fact` files in `/etc/ansible/facts.d/`?",
                "options": [
                    "INI format and JSON format",
                    "XML format only",
                    "CSV format only",
                    "Plain unstructured text"
                ],
                "correct": "INI format and JSON format",
                "explanation": "Ansible natively parses `.fact` files written in either standard INI format or JSON format."
            },
            {
                "type": "true_false",
                "question": "If a `.fact` file in `/etc/ansible/facts.d/` is marked as executable (`chmod +x`), Ansible will execute it and parse the JSON returned on standard output.",
                "correct": True,
                "explanation": "Executable `.fact` scripts are run dynamically at fact gathering time, enabling custom dynamic hardware or application discovery."
            },
            {
                "type": "mcq",
                "question": "Under which top-level variable namespace are local custom facts exposed in playbooks?",
                "options": ["ansible_local", "custom_facts", "local_facts", "ansible_custom"],
                "correct": "ansible_local",
                "explanation": "All facts gathered from `/etc/ansible/facts.d/` are exposed under the `ansible_local` namespace."
            },
            {
                "type": "mcq",
                "question": "If you create `/etc/ansible/facts.d/custom.fact` containing:\n\n[environment]\ntier=production\n\nHow do you access the `tier` fact in a playbook?",
                "options": [
                    "{{ ansible_local.custom.environment.tier }}",
                    "{{ custom.environment.tier }}",
                    "{{ ansible_facts.tier }}",
                    "{{ ansible_custom.tier }}"
                ],
                "correct": "{{ ansible_local.custom.environment.tier }}",
                "explanation": "The hierarchy is `ansible_local.<filename_stem>.<section>.<key>`."
            },
            {
                "type": "mcq",
                "question": "Which builtin Ansible module allows you to define dynamic custom facts in memory during playbook execution?",
                "options": ["ansible.builtin.set_fact", "ansible.builtin.create_fact", "ansible.builtin.var", "ansible.builtin.export_fact"],
                "correct": "ansible.builtin.set_fact",
                "explanation": "`ansible.builtin.set_fact` assigns variables dynamically during runtime, scoped to the current host."
            },
            {
                "type": "true_false",
                "question": "Facts created with `set_fact` persist across subsequent tasks on that host for the duration of the play.",
                "correct": True,
                "explanation": "`set_fact` variables remain defined in memory for that host throughout remaining tasks in the playbook."
            },
            {
                "type": "mcq",
                "question": "What is the variable precedence of `set_fact` relative to gathered facts?",
                "options": [
                    "`set_fact` (level 7) has HIGHER precedence than gathered facts (level 5)",
                    "Gathered facts have higher precedence than `set_fact`",
                    "Both share the exact same precedence level",
                    "`set_fact` is lower than role defaults"
                ],
                "correct": "`set_fact` (level 7) has HIGHER precedence than gathered facts (level 5)",
                "explanation": "`set_fact` overrides gathered facts, role defaults, and inventory variables."
            },
            {
                "type": "mcq",
                "question": "Which of the following demonstrates valid syntax for defining a custom fact using `set_fact`?",
                "options": [
                    "- ansible.builtin.set_fact:\n    deployment_stage: staging\n    backup_required: yes",
                    "- set_fact = 'stage=staging'",
                    "- fact:\n    set: staging",
                    "<fact name='stage'>staging</fact>"
                ],
                "correct": "- ansible.builtin.set_fact:\n    deployment_stage: staging\n    backup_required: yes",
                "explanation": "`set_fact` takes a key-value dictionary of facts to register."
            },
            {
                "type": "true_false",
                "question": "If `/etc/ansible/facts.d/` does not exist on a managed node, Ansible will fail fact gathering with a fatal error.",
                "correct": False,
                "explanation": "If `/etc/ansible/facts.d/` does not exist, Ansible simply skips local facts without error."
            },
            {
                "type": "mcq",
                "question": "How can you create `/etc/ansible/facts.d/preferences.fact` on a remote host using an Ansible playbook task?",
                "options": [
                    "Using `ansible.builtin.copy` or `ansible.builtin.template` with destination `/etc/ansible/facts.d/preferences.fact`",
                    "Using `ansible.builtin.setup` with `create: true`",
                    "Using `ansible.builtin.git`",
                    "Local facts cannot be deployed via playbooks"
                ],
                "correct": "Using `ansible.builtin.copy` or `ansible.builtin.template` with destination `/etc/ansible/facts.d/preferences.fact`",
                "explanation": "Standard file modules (`file`, `copy`, `template`) can provision the directory and `.fact` files on remote hosts."
            },
            {
                "type": "true_false",
                "question": "Variables created with `set_fact` can reference existing facts gathered from the system.",
                "correct": True,
                "explanation": "You can interpolate existing facts (e.g. `api_url: 'https://{{ ansible_default_ipv4.address }}:8443'`)."
            },
            {
                "type": "mcq",
                "question": "What happens if a custom executable `.fact` script outputs non-JSON garbage text to standard error or standard output?",
                "options": [
                    "Ansible reports an error parsing the fact file or sets `ansible_local.<name>` to an error string",
                    "Ansible crashes the Python interpreter",
                    "The machine reboots immediately",
                    "Ansible silently converts the text to a dictionary"
                ],
                "correct": "Ansible reports an error parsing the fact file or sets `ansible_local.<name>` to an error string",
                "explanation": "Executable fact scripts must return valid JSON; non-JSON output causes parsing warnings or errors."
            },
            {
                "type": "true_false",
                "question": "Custom facts placed in `/etc/ansible/facts.d/` persist across system reboots because they are stored on disk on the managed host.",
                "correct": True,
                "explanation": "Files in `/etc/ansible/facts.d/` live on the persistent filesystem, surviving reboots."
            },
            {
                "type": "mcq",
                "question": "Which of the following JSON structures is valid for `/etc/ansible/facts.d/app.fact`?",
                "options": [
                    "{\n  \"settings\": {\n    \"version\": \"1.0.0\",\n    \"enabled\": true\n  }\n}",
                    "[version = 1.0.0]",
                    "<settings><version>1.0.0</version></settings>",
                    "version: 1.0.0"
                ],
                "correct": "{\n  \"settings\": {\n    \"version\": \"1.0.0\",\n    \"enabled\": true\n  }\n}",
                "explanation": "Valid JSON objects with nested key-values parse cleanly into the `ansible_local.app` dictionary."
            },
            {
                "type": "true_false",
                "question": "`set_fact` values are shared globally across all hosts in the inventory, even hosts where the task did not run.",
                "correct": False,
                "explanation": "`set_fact` is host-scoped; it assigns values only to the specific target hosts currently executing the task."
            },
            {
                "type": "mcq",
                "question": "Which parameter in `set_fact` allows making a fact persistent across plays in modern Ansible versions?",
                "options": ["cacheable: yes", "persist: true", "global: yes", "save_to_disk: true"],
                "correct": "cacheable: yes",
                "explanation": "Setting `cacheable: yes` on `set_fact` writes the fact into the configured fact cache for subsequent plays."
            }
        ]
    },
    "06-filtering-and-cli-practices": {
        "passing_score": 70,
        "questions": [
            {
                "type": "mcq",
                "question": "How do you filter fact output on the command line to display only default IPv4 networking facts?",
                "options": [
                    "ansible all -m setup -a \"filter=ansible_default_ipv4*\"",
                    "ansible all -m setup --grep ipv4",
                    "ansible all -m setup --filter-ipv4",
                    "ansible all -m setup -f ipv4"
                ],
                "correct": "ansible all -m setup -a \"filter=ansible_default_ipv4*\"",
                "explanation": "The `-a \"filter=<pattern>\"` argument allows filtering facts using shell-style wildcards."
            },
            {
                "type": "mcq",
                "question": "Which command displays specifically the default IP address of `linux-server-2` only?",
                "options": [
                    "ansible linux-server-2 -m setup -a \"filter=ansible_default_ipv4.address\"",
                    "ansible all -m setup linux-server-2 -a \"filter=ip\"",
                    "ansible-playbook setup -l linux-server-2 --ip",
                    "ansible linux-server-2 --show-ip"
                ],
                "correct": "ansible linux-server-2 -m setup -a \"filter=ansible_default_ipv4.address\"",
                "explanation": "Combining host targeting `linux-server-2` with `filter=ansible_default_ipv4.address` queries exactly that value."
            },
            {
                "type": "true_false",
                "question": "The `filter` argument in the setup module supports shell wildcard patterns such as `*`.",
                "correct": True,
                "explanation": "Wildcards like `ansible_distribution*` match `ansible_distribution`, `ansible_distribution_version`, `ansible_distribution_release`, etc."
            },
            {
                "type": "mcq",
                "question": "How can you save discovered facts to a file on the Ansible controller during playbook execution?",
                "options": [
                    "Use `copy` module with `delegate_to: localhost` and `content: \"{{ ansible_facts }}\"`",
                    "Use `ansible.builtin.save_facts`",
                    "Use `--export` in the playbook header",
                    "Facts cannot be saved to the controller from a playbook"
                ],
                "correct": "Use `copy` module with `delegate_to: localhost` and `content: \"{{ ansible_facts }}\"`",
                "explanation": "Delegating the copy task to localhost writes the remote host's `ansible_facts` to a local file on the controller machine."
            },
            {
                "type": "mcq",
                "question": "Which Jinja2 filter formats a dictionary into clean, indented JSON suitable for saving to disk?",
                "options": ["to_nice_json", "to_json_format", "as_json", "pretty_json"],
                "correct": "to_nice_json",
                "explanation": "`{{ ansible_facts | to_nice_json }}` formats the dictionary into indented, human-readable JSON."
            },
            {
                "type": "true_false",
                "question": "Running `ansible all -m setup -a \"filter=ansible_distribution*\"` will display CPU and memory facts.",
                "correct": False,
                "explanation": "The filter limits output to facts matching `ansible_distribution*`; CPU and memory facts will be excluded."
            },
            {
                "type": "mcq",
                "question": "In the context of multi-tier automation, what does `when: ansible_memory_mb.real.total < 4096` accomplish?",
                "options": [
                    "It ensures the task only runs on systems with less than 4GB (4096MB) of RAM",
                    "It upgrades system RAM to 4GB",
                    "It fails if the system has more than 4096MB of RAM",
                    "It sets memory usage to 4096MB"
                ],
                "correct": "It ensures the task only runs on systems with less than 4GB (4096MB) of RAM",
                "explanation": "The conditional evaluates memory capacity to protect resource-constrained systems from heavy workloads."
            },
            {
                "type": "mcq",
                "question": "Which task snippet safely checks if a dynamic backup fact was set before triggering a backup script?",
                "options": [
                    "when: backup_required == \"yes\"",
                    "if: backup_required",
                    "when: {{ backup_required == true }}",
                    "when: backup_required()"
                ],
                "correct": "when: backup_required == \"yes\"",
                "explanation": "Standard string equality in `when:` checks whether the fact equals `'yes'`."
            },
            {
                "type": "true_false",
                "question": "You can filter facts using exact names without wildcards (e.g. `filter=ansible_hostname`).",
                "correct": True,
                "explanation": "Exact string matches return only the specified fact."
            },
            {
                "type": "mcq",
                "question": "Which special variable represents the inventory hostname of the current node being processed in a task?",
                "options": ["inventory_hostname", "current_host", "node_name", "target_host"],
                "correct": "inventory_hostname",
                "explanation": "`inventory_hostname` is the name of the current host as defined in the Ansible inventory."
            },
            {
                "type": "true_false",
                "question": "The command `ansible webservers -m setup -a \"filter=ansible_all_ipv4_addresses\"` will run against all hosts in the `webservers` group.",
                "correct": True,
                "explanation": "Any valid inventory group name can be passed as the target pattern."
            },
            {
                "type": "mcq",
                "question": "Why is `run_once: true` often combined with `delegate_to: localhost` when creating an archive directory for fact files?",
                "options": [
                    "To prevent creating the same local directory multiple times across a batch of 50 remote hosts",
                    "Because directories can only be created once in Linux",
                    "To reboot localhost",
                    "To speed up SSH authentication"
                ],
                "correct": "To prevent creating the same local directory multiple times across a batch of 50 remote hosts",
                "explanation": "`run_once: true` ensures the directory creation task runs only once on localhost rather than once per inventory host."
            },
            {
                "type": "true_false",
                "question": "In a dual-family playbook, `ansible.builtin.apt` tasks will automatically run on CentOS hosts if `when: ansible_os_family == 'Debian'` is specified.",
                "correct": False,
                "explanation": "On CentOS, `ansible_os_family` is `'RedHat'`, so the `apt` task will be safely skipped."
            },
            {
                "type": "mcq",
                "question": "What is the primary benefit of testing fact filtering using ad-hoc commands before writing playbooks?",
                "options": [
                    "It allows you to inspect the exact structure and keys of the facts on target systems to write accurate conditionals",
                    "It installs the required Python libraries automatically",
                    "It compiles the playbook into YAML",
                    "It verifies the cloud billing account"
                ],
                "correct": "It allows you to inspect the exact structure and keys of the facts on target systems to write accurate conditionals",
                "explanation": "Checking fact names and types via ad-hoc CLI ensures you use the correct variable keys in your playbook `when:` statements."
            },
            {
                "type": "true_false",
                "question": "Discovered facts like `ansible_default_ipv4.address` can be used to dynamically generate an `/etc/hosts` file containing all cluster nodes.",
                "correct": True,
                "explanation": "Using `hostvars[host]['ansible_default_ipv4']['address']`, playbooks frequently build dynamic `/etc/hosts` files across entire server fleets."
            },
            {
                "type": "mcq",
                "question": "Which command would you run to find out what virtualization platform (e.g. kvm, docker, vmware) a remote host is running on?",
                "options": [
                    "ansible all -m setup -a \"filter=ansible_virtualization*\"",
                    "ansible all -m virt",
                    "ansible all -a 'uname -v'",
                    "ansible-virtual-check all"
                ],
                "correct": "ansible all -m setup -a \"filter=ansible_virtualization*\"",
                "explanation": "Filtering for `ansible_virtualization*` returns `ansible_virtualization_type` and `ansible_virtualization_role`."
            },
            {
                "type": "true_false",
                "question": "Ad-hoc setup commands execute changes on target systems and modify `/etc/environment` by default.",
                "correct": False,
                "explanation": "The setup module is read-only; it inspects system state without making any modifications."
            },
            {
                "type": "mcq",
                "question": "Which fact would you filter to quickly inspect the gateway IP address on all servers in an inventory?",
                "options": [
                    "ansible all -m setup -a \"filter=ansible_default_ipv4.gateway\"",
                    "ansible all -m setup -a \"filter=default_gateway\"",
                    "ansible all -m gateway",
                    "ansible all -a 'route'"
                ],
                "correct": "ansible all -m setup -a \"filter=ansible_default_ipv4.gateway\"",
                "explanation": "`ansible_default_ipv4.gateway` isolates the gateway attribute."
            }
        ]
    }
}

def main():
    total_q = 0
    chunks_meta = []
    
    # 1. Write individual .quiz.yaml files
    for slug, q_data in CHUNKS_QUIZZES.items():
        quiz_file = FACTS_DIR / f"{slug}.quiz.yaml"
        count = len(q_data["questions"])
        total_q += count
        with open(quiz_file, "w", encoding="utf-8") as f:
            yaml.dump(q_data, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
        print(f"✓ Saved {count:2d} questions to {quiz_file.name}")

    # 2. Build chunks list for _module.yaml
    chunk_order = [
        ("01-how-to-view-facts", "01. Viewing Facts & Architecture", 5, False),
        ("02-how-to-use-facts-in-playbooks", "02. Using Facts in Playbook Logic", 6, False),
        ("03-commonly-used-facts", "03. Commonly Used Facts Reference", 6, False),
        ("04-disabling-fact-gathering", "04. Disabling & Optimizing Fact Gathering", 5, False),
        ("05-custom-facts", "05. Custom Facts (Static & Dynamic)", 6, False),
        ("06-filtering-and-cli-practices", "06. Fact Filtering & Practical Automation", 7, True),
    ]

    for slug, title, est_time, has_hands_on in chunk_order:
        chunks_meta.append({
            "slug": slug,
            "title": title,
            "file": f"{slug}.md",
            "quiz_file": f"{slug}.quiz.yaml",
            "estimated_time": est_time,
            "question_count": len(CHUNKS_QUIZZES[slug]["questions"]),
            "has_hands_on": has_hands_on
        })

    # 3. Write _module.yaml
    mod_meta = {
        "name": "Ansible Facts",
        "slug": "005-facts",
        "description": "Discover, filter, and leverage dynamic system facts, optimize performance, and define custom local facts.",
        "display_order": 5,
        "total_chunks": len(chunks_meta),
        "total_questions": total_q,
        "chunks": chunks_meta
    }

    with open(FACTS_DIR / "_module.yaml", "w", encoding="utf-8") as f:
        yaml.dump(mod_meta, f, sort_keys=False, default_flow_style=False)
    print(f"\n🎉 Successfully created Module 005 'Ansible Facts'! Total questions: {total_q}")

if __name__ == "__main__":
    main()
