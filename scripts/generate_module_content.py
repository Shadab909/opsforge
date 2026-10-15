#!/usr/bin/env python3
"""
OpsForge Content Processor & Generator for Ansible Playbooks (004-playbooks)
Groups the HTML content into 8 clean, well-structured chunks and generates
comprehensive, high-quality quiz files with 5-10 questions per chunk.
"""

import os
import re
import sys
import shutil
from pathlib import Path
import html
import yaml

# Base paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
KB_DIR = PROJECT_ROOT / "knowledge_base"
PROCESSED_DIR = PROJECT_ROOT / "processed"

def clean_markdown_text(text):
    # Unescape HTML entities (&para;, &nbsp;, etc.)
    text = html.unescape(text)
    # Remove header anchor links like [](#section)
    text = re.sub(r'\[\]\(#[^)]*\)', '', text)
    # Remove leftover paragraph symbols
    text = text.replace('¶', '')
    # Remove standalone lines with only empty asterisks
    text = re.sub(r'^\s*\*{2,}\s*$', '', text, flags=re.MULTILINE)
    # Clean whitespace lines
    lines = [line.rstrip() for line in text.splitlines()]
    text = "\n".join(lines)
    # Collapse 3+ newlines to 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# 8 chunks specification with their source sections and handcrafted comprehensive quizzes
CHUNKS_DATA = [
    {
        "slug": "01-what-are-playbooks",
        "title": "01. What are Playbooks?",
        "estimated_time": 5,
        "has_hands_on": False,
        "keywords": ["01. what are playbooks"],
        "questions": [
            {
                "type": "mcq",
                "question": "What is the primary format used to write Ansible playbooks?",
                "options": ["XML", "YAML", "JSON", "INI"],
                "correct": "YAML",
                "explanation": "Ansible playbooks are blueprints of automation tasks written in YAML format."
            },
            {
                "type": "mcq",
                "question": "Which of the following is a major advantage of playbooks over ad-hoc commands?",
                "options": [
                    "Playbooks execute faster on a single host",
                    "Playbooks are fully repeatable, support conditionals, and orchestrate complex multi-step workflows",
                    "Playbooks do not require Python on target hosts",
                    "Playbooks cannot be tracked with Git"
                ],
                "correct": "Playbooks are fully repeatable, support conditionals, and orchestrate complex multi-step workflows",
                "explanation": "While ad-hoc commands are meant for quick one-off actions, playbooks provide repeatable, version-controlled multi-task orchestration."
            },
            {
                "type": "true_false",
                "question": "Playbooks are idempotent, meaning you can safely run them multiple times without unintended side effects.",
                "correct": True,
                "explanation": "Idempotency ensures that running the same playbook repeatedly brings the system to the desired state without making unnecessary changes."
            },
            {
                "type": "mcq",
                "question": "How are ad-hoc commands and playbooks different regarding error handling?",
                "options": [
                    "Ad-hoc commands offer automated rollbacks",
                    "Playbooks have advanced error handling, blocks, and rescue capabilities, unlike basic ad-hoc commands",
                    "Ad-hoc commands never fail",
                    "Playbooks cannot report failed tasks"
                ],
                "correct": "Playbooks have advanced error handling, blocks, and rescue capabilities, unlike basic ad-hoc commands",
                "explanation": "Playbooks support robust error handling such as ignore_errors, failed_when, blocks, rescue, and always sections."
            },
            {
                "type": "true_false",
                "question": "Conditionals (like `when`) are fully supported in Ansible ad-hoc commands.",
                "correct": False,
                "explanation": "Conditionals are not supported in ad-hoc commands; they require playbooks."
            },
            {
                "type": "mcq",
                "question": "Which command is used to execute an Ansible playbook from the terminal?",
                "options": ["ansible --play", "ansible-playbook", "ansible-exec", "ansible-orchestrate"],
                "correct": "ansible-playbook",
                "explanation": "`ansible-playbook <playbook.yaml>` is the dedicated command for running playbooks."
            }
        ]
    },
    {
        "slug": "02-key-points",
        "title": "02. Key Architecture & Execution Points",
        "estimated_time": 5,
        "has_hands_on": False,
        "keywords": ["02. key points"],
        "questions": [
            {
                "type": "mcq",
                "question": "What is the structural hierarchy of an Ansible playbook?",
                "options": [
                    "A playbook contains one or more plays; each play runs one or more tasks; each task invokes a module",
                    "A module contains tasks; tasks contain plays; plays contain playbooks",
                    "A task contains plays; each play executes a script",
                    "A playbook is a single module executed across all hosts"
                ],
                "correct": "A playbook contains one or more plays; each play runs one or more tasks; each task invokes a module",
                "explanation": "The hierarchy flows: Playbook (ordered list of plays) -> Play (maps hosts to tasks) -> Tasks (ordered steps) -> Module (the actual code executed)."
            },
            {
                "type": "mcq",
                "question": "In what order are plays and tasks executed in an Ansible playbook?",
                "options": [
                    "Parallel by default unless specified",
                    "Random order based on host availability",
                    "Sequential order from top to bottom",
                    "Alphabetical order of task names"
                ],
                "correct": "Sequential order from top to bottom",
                "explanation": "Both plays within a playbook and tasks within a play execute sequentially from top to bottom."
            },
            {
                "type": "true_false",
                "question": "A single playbook can contain multiple plays to configure different groups of servers (e.g. webservers, database servers) in a pre-defined order.",
                "correct": True,
                "explanation": "Multiple plays in one playbook allow orchestrating multi-tier deployments across different server groups."
            },
            {
                "type": "mcq",
                "question": "What is the recommended practice when referring to Ansible modules to prevent naming collisions?",
                "options": [
                    "Use short names only (e.g., `copy`)",
                    "Use the Fully Qualified Collection Name (FQCN), such as `ansible.builtin.copy`",
                    "Always use shell scripts instead of modules",
                    "Capitalize module names"
                ],
                "correct": "Use the Fully Qualified Collection Name (FQCN), such as `ansible.builtin.copy`",
                "explanation": "Using FQCN prevents naming collisions between builtin modules and community or custom collections."
            },
            {
                "type": "true_false",
                "question": "Playbooks can launch tasks either synchronously or asynchronously.",
                "correct": True,
                "explanation": "Ansible supports asynchronous task execution using the `async` and `poll` keywords."
            }
        ]
    },
    {
        "slug": "03-yaml-basics",
        "title": "03. YAML Basics for Playbooks",
        "estimated_time": 6,
        "has_hands_on": False,
        "keywords": ["03. yaml basics"],
        "questions": [
            {
                "type": "mcq",
                "question": "How must indentation be formatted in YAML files?",
                "options": [
                    "With tab characters only",
                    "With spaces only (tabs will cause syntax errors)",
                    "Either tabs or spaces, as long as it is consistent",
                    "YAML does not use indentation"
                ],
                "correct": "With spaces only (tabs will cause syntax errors)",
                "explanation": "YAML strictly forbids tabs for indentation; spaces must always be used."
            },
            {
                "type": "mcq",
                "question": "What marker standardly indicates the start of a YAML document?",
                "options": ["---", "===", "###", "START"],
                "correct": "---",
                "explanation": "Three dashes (`---`) denote the start of a YAML document."
            },
            {
                "type": "mcq",
                "question": "In YAML, which character denotes a literal block scalar that preserves newlines and trailing spaces?",
                "options": [">", "|", "&", "*"],
                "correct": "|",
                "explanation": "The pipe `|` denotes a literal block scalar (preserves newlines), while `>` folds newlines into spaces."
            },
            {
                "type": "true_false",
                "question": "In YAML dictionaries, the colon `:` after a key must immediately be followed by a space.",
                "correct": True,
                "explanation": "A colon followed by a space (`key: value`) is required for proper key-value dictionary syntax in YAML."
            },
            {
                "type": "mcq",
                "question": "How are list items indicated in YAML?",
                "options": [
                    "Surrounded by curly braces {}",
                    "Lines starting with a dash and a space `- ` at the same indentation level",
                    "Lines ending with a semicolon",
                    "Numbered with parenthesis (1), (2)"
                ],
                "correct": "Lines starting with a dash and a space `- ` at the same indentation level",
                "explanation": "A dash followed by a space (`- item`) denotes a list entry in YAML."
            },
            {
                "type": "true_false",
                "question": "YAML is case-insensitive, meaning `Hosts:` and `hosts:` are treated identically by Ansible.",
                "correct": False,
                "explanation": "YAML and Ansible keywords are case-sensitive."
            }
        ]
    },
    {
        "slug": "04-first-playbook",
        "title": "04. Writing Your First Playbook",
        "estimated_time": 6,
        "has_hands_on": False,
        "keywords": ["05. our first playbook"],
        "questions": [
            {
                "type": "mcq",
                "question": "In a basic playbook play, which directive specifies the target machines where tasks will execute?",
                "options": ["targets:", "hosts:", "nodes:", "servers:"],
                "correct": "hosts:",
                "explanation": "The `hosts:` directive defines the target hosts or groups for that play."
            },
            {
                "type": "mcq",
                "question": "Which builtin Ansible module is commonly used to print values or debug messages during playbook execution?",
                "options": ["echo", "ansible.builtin.debug", "ansible.builtin.print", "console"],
                "correct": "ansible.builtin.debug",
                "explanation": "The `ansible.builtin.debug` module prints statements and variable values during execution."
            },
            {
                "type": "mcq",
                "question": "What is the purpose of the `register` keyword in a task?",
                "options": [
                    "To register the playbook with Ansible Galaxy",
                    "To save the result and output of a task into a variable for later use",
                    "To authenticate with the remote host",
                    "To declare a new user account"
                ],
                "correct": "To save the result and output of a task into a variable for later use",
                "explanation": "`register: <var_name>` captures the return values (stdout, stderr, rc, etc.) of a task."
            },
            {
                "type": "true_false",
                "question": "When debugging a registered variable that contains multiple lines of terminal output, `files.stdout_lines` provides an easy-to-read list of lines.",
                "correct": True,
                "explanation": "`stdout_lines` breaks the standard output into a list of strings split by newline."
            },
            {
                "type": "mcq",
                "question": "How are variables interpolated into task arguments in an Ansible playbook?",
                "options": [
                    "$(variable_name)",
                    "{{ variable_name }}",
                    "%{variable_name}",
                    "${variable_name}"
                ],
                "correct": "{{ variable_name }}",
                "explanation": "Ansible uses Jinja2 templating syntax with double curly braces: `{{ var }}`."
            }
        ]
    },
    {
        "slug": "05-execution-and-syntax",
        "title": "05. Playbook Execution & Play Syntax",
        "estimated_time": 7,
        "has_hands_on": False,
        "keywords": ["06. playbook execution", "05. playbook syntax"],
        "questions": [
            {
                "type": "mcq",
                "question": "Which flag performs a dry run (check mode) of a playbook without making actual changes to target hosts?",
                "options": ["--dry", "--check", "--test", "--verify"],
                "correct": "--check",
                "explanation": "`ansible-playbook playbook.yaml --check` runs the playbook in check mode (dry run)."
            },
            {
                "type": "mcq",
                "question": "Which command-line option limits playbook execution to a specific host or group in your inventory?",
                "options": ["--target", "--limit", "--only", "--host"],
                "correct": "--limit",
                "explanation": "The `--limit` (or `-l`) option restricts execution to matching hosts."
            },
            {
                "type": "mcq",
                "question": "In the Ansible play recap, what does `changed=1` mean?",
                "options": [
                    "One host failed to connect",
                    "One task was skipped",
                    "One or more tasks modified system state on that host",
                    "The playbook file was modified during execution"
                ],
                "correct": "One or more tasks modified system state on that host",
                "explanation": "A status of `changed` indicates that Ansible applied changes to bring the host to the desired state."
            },
            {
                "type": "mcq",
                "question": "Which directive in a play enables privilege escalation (such as sudo)?",
                "options": ["privilege: true", "become: yes", "sudo: true", "admin: yes"],
                "correct": "become: yes",
                "explanation": "`become: yes` activates privilege escalation via the become plugin."
            },
            {
                "type": "true_false",
                "question": "The `--diff` option can be combined with `--check` to preview exactly what file modifications will occur before running the playbook.",
                "correct": True,
                "explanation": "`--check --diff` provides a safe preview of configuration and template changes."
            },
            {
                "type": "mcq",
                "question": "How do you increase verbosity when running a playbook to debug errors?",
                "options": [
                    "Use flags like `-v`, `-vv`, `-vvv`, or `-vvvv`",
                    "Add `--debug-level=max`",
                    "Use `--trace`",
                    "Edit `/etc/ansible/debug`"
                ],
                "correct": "Use flags like `-v`, `-vv`, `-vvv`, or `-vvvv`",
                "explanation": "Adding multiple `-v` flags increases Ansible's logging verbosity."
            }
        ]
    },
    {
        "slug": "06-variables",
        "title": "06. Variables & Environment Configuration",
        "estimated_time": 7,
        "has_hands_on": False,
        "keywords": ["08. variables in playbooks", "07. playbook demo"],
        "questions": [
            {
                "type": "mcq",
                "question": "Which variable source has the HIGHEST precedence in Ansible?",
                "options": [
                    "Playbook `vars:` section",
                    "Group variables (`group_vars`)",
                    "Extra variables passed on the command line via `-e` or `--extra-vars`",
                    "Role defaults"
                ],
                "correct": "Extra variables passed on the command line via `-e` or `--extra-vars`",
                "explanation": "Extra variables (`-e`) always take top precedence over all other variable definitions."
            },
            {
                "type": "mcq",
                "question": "Which directive allows importing an external YAML file containing variables into a play?",
                "options": ["import_vars:", "vars_files:", "include_env:", "load_vars:"],
                "correct": "vars_files:",
                "explanation": "`vars_files:` accepts a list of external YAML files containing variable mappings."
            },
            {
                "type": "mcq",
                "question": "How can you read an environment variable from the Ansible controller machine inside a playbook?",
                "options": [
                    "{{ env.MY_VAR }}",
                    "{{ lookup('env', 'MY_VAR') }}",
                    "$MY_VAR",
                    "{{ system('MY_VAR') }}"
                ],
                "correct": "{{ lookup('env', 'MY_VAR') }}",
                "explanation": "The Jinja lookup plugin `lookup('env', 'VAR_NAME')` retrieves controller environment variables."
            },
            {
                "type": "true_false",
                "question": "The `environment:` keyword can be applied at the task level or the play level to set environment variables for task execution.",
                "correct": True,
                "explanation": "The `environment:` dictionary provides environment variables to modules during execution."
            },
            {
                "type": "mcq",
                "question": "Which module can be used to set a permanent environment variable on a target remote host by editing `/etc/environment`?",
                "options": ["ansible.builtin.set_env", "ansible.builtin.lineinfile", "ansible.builtin.env", "ansible.builtin.touch"],
                "correct": "ansible.builtin.lineinfile",
                "explanation": "`ansible.builtin.lineinfile` manages single line entries in configuration files such as `/etc/environment`."
            }
        ]
    },
    {
        "slug": "07-handlers-register-conditionals",
        "title": "07. Handlers, Output Register & Conditionals",
        "estimated_time": 8,
        "has_hands_on": False,
        "keywords": ["09. handlers and notifications", "10. understanding the register keyword", "11. conditionals"],
        "questions": [
            {
                "type": "mcq",
                "question": "When do Ansible handlers execute by default?",
                "options": [
                    "Immediately when notified",
                    "At the very end of the play, after all normal tasks have run",
                    "Before any tasks run",
                    "In a separate background thread"
                ],
                "correct": "At the very end of the play, after all normal tasks have run",
                "explanation": "Handlers run once at the end of the play, provided that at least one task notifying them reported a `changed` state."
            },
            {
                "type": "true_false",
                "question": "If a task reports `ok` (no change made), any handlers notified by that task will NOT be triggered.",
                "correct": True,
                "explanation": "Handlers only trigger when the notifying task reports a status of `changed`."
            },
            {
                "type": "mcq",
                "question": "If three different tasks notify the same handler `restart nginx` in a single play, how many times will the handler run?",
                "options": ["3 times", "1 time", "0 times", "Depends on host count"],
                "correct": "1 time",
                "explanation": "Handlers are de-duplicated by name and run only once per play, even if notified multiple times."
            },
            {
                "type": "mcq",
                "question": "Which keyword controls conditional execution of a task in Ansible?",
                "options": ["if:", "condition:", "when:", "case:"],
                "correct": "when:",
                "explanation": "The `when:` statement evaluates a condition (e.g. `when: ansible_os_family == 'Debian'`)."
            },
            {
                "type": "true_false",
                "question": "Inside a `when:` condition string, variable names must always be enclosed in `{{ }}` braces.",
                "correct": False,
                "explanation": "Variables in `when:` statements are evaluated directly as Python/Jinja2 expressions without `{{ }}` (e.g., `when: file_stat.stat.exists`)."
            },
            {
                "type": "mcq",
                "question": "How can you check if a file exists using Ansible without executing a raw shell command?",
                "options": [
                    "Use the `ansible.builtin.stat` module and check `stat_result.stat.exists`",
                    "Use `find` module only",
                    "Use `file` module with `state=check`",
                    "Ansible cannot check file existence without shell"
                ],
                "correct": "Use the `ansible.builtin.stat` module and check `stat_result.stat.exists`",
                "explanation": "`stat` retrieves file or file-system status, storing attributes in `.stat`."
            }
        ]
    },
    {
        "slug": "08-loops-tags-best-practices",
        "title": "08. Loops, Tags & Playbook Best Practices",
        "estimated_time": 8,
        "has_hands_on": True,
        "keywords": ["12. loops", "13. tags", "14. playbook best practices", "15. practical examples"],
        "questions": [
            {
                "type": "mcq",
                "question": "What is the standard keyword used to iterate over a list in modern Ansible playbooks?",
                "options": ["with_items", "loop", "iterate", "for_each"],
                "correct": "loop",
                "explanation": "`loop:` is the modern, recommended syntax in Ansible for iterating over lists."
            },
            {
                "type": "mcq",
                "question": "What default variable holds the current iteration value within a loop task?",
                "options": ["{{ value }}", "{{ item }}", "{{ element }}", "{{ self }}"],
                "correct": "{{ item }}",
                "explanation": "By default, Ansible exposes the current iteration element as `item`."
            },
            {
                "type": "mcq",
                "question": "How do you execute only tasks that have the tag `install` when running a playbook?",
                "options": [
                    "ansible-playbook playbook.yaml --only install",
                    "ansible-playbook playbook.yaml --tags install",
                    "ansible-playbook playbook.yaml -t:install",
                    "ansible-playbook playbook.yaml --filter=install"
                ],
                "correct": "ansible-playbook playbook.yaml --tags install",
                "explanation": "The `--tags` (or `-t`) flag filters execution to tasks matching the specified tags."
            },
            {
                "type": "true_false",
                "question": "You can skip specific tagged tasks during execution using the `--skip-tags` option.",
                "correct": True,
                "explanation": "`--skip-tags <tag_name>` tells Ansible to bypass tasks labeled with those tags."
            },
            {
                "type": "mcq",
                "question": "Which of the following is considered an Ansible playbook best practice?",
                "options": [
                    "Avoid naming tasks to keep files shorter",
                    "Always give every task a descriptive `name:` that explains its intent",
                    "Store plain-text passwords directly in playbook variables",
                    "Use `command:` instead of dedicated modules whenever possible"
                ],
                "correct": "Always give every task a descriptive `name:` that explains its intent",
                "explanation": "Descriptive task names provide clear, self-documenting logs and easy debugging during playbook execution."
            },
            {
                "type": "true_false",
                "question": "It is best practice to use `command` or `shell` modules even when a dedicated module (like `apt`, `service`, or `user`) exists.",
                "correct": False,
                "explanation": "Dedicated modules provide idempotency, parameter validation, and consistent return formats, whereas raw shell/command modules should be a last resort."
            }
        ]
    }
]

def main():
    print("==================================================")
    print("🔥 OpsForge: Processing Ansible Playbooks (004)...")
    print("==================================================")
    
    topic_slug = "ansible"
    module_slug = "004-playbooks"
    
    kb_mod_dir = KB_DIR / topic_slug / module_slug
    proc_mod_dir = PROCESSED_DIR / topic_slug / module_slug
    proc_mod_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy supplementary files
    supp_dir = proc_mod_dir / "supplementary"
    supp_dir.mkdir(exist_ok=True)
    for f in kb_mod_dir.iterdir():
        if f.is_file() and f.name != "index.html" and not f.name.startswith("."):
            shutil.copy2(f, supp_dir / f.name)
            print(f"  [+] Copied supplementary file: {f.name}")

    # Read the raw HTML
    html_file = kb_mod_dir / "index.html"
    with open(html_file, 'r', encoding='utf-8') as f:
        html_raw = f.read()

    # Load existing converted text chunks from previous run or convert fresh
    module_chunks_meta = []
    
    for chunk in CHUNKS_DATA:
        slug = chunk["slug"]
        title = chunk["title"]
        est_time = chunk["estimated_time"]
        has_hands_on = chunk["has_hands_on"]
        
        md_file = proc_mod_dir / f"{slug}.md"
        quiz_file = proc_mod_dir / f"{slug}.quiz.yaml"
        
        # Check if we have source chunk file generated
        content_lines = []
        for cand in proc_mod_dir.glob("*.md"):
            # Check matching keyword
            cand_name = cand.name.lower()
            if any(k in cand_name for k in chunk["keywords"]):
                with open(cand, 'r', encoding='utf-8') as cf:
                    c_text = cf.read()
                    # Strip frontmatter
                    c_text = re.sub(r'^---\n.*?\n---\n', '', c_text, flags=re.DOTALL)
                    content_lines.append(c_text)
                    
        if not content_lines:
            content_body = f"## {title}\n\nComprehensive review of {title}."
        else:
            content_body = clean_markdown_text("\n\n".join(content_lines))

        # Add hands-on note if applicable
        if has_hands_on:
            content_body += "\n\n> [!NOTE]\n> **Interactive Hands-On Lab**: A browser-based terminal environment for live practice will be integrated into this section."

        # Write clean markdown with frontmatter
        md_content = f"""---
title: "{title}"
slug: "{slug}"
estimated_time: {est_time}
has_hands_on: {str(has_hands_on).lower()}
---

{content_body}
"""
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"  [✓] Written clean markdown: {md_file.name}")

        # Write quiz YAML
        quiz_data = {
            "passing_score": 70,
            "questions": chunk["questions"]
        }
        with open(quiz_file, 'w', encoding='utf-8') as f:
            yaml.dump(quiz_data, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
        print(f"  [✓] Written quiz ({len(chunk['questions'])} Qs): {quiz_file.name}")

        module_chunks_meta.append({
            "slug": slug,
            "title": title,
            "file": f"{slug}.md",
            "quiz_file": f"{slug}.quiz.yaml",
            "estimated_time": est_time,
            "question_count": len(chunk["questions"]),
            "has_hands_on": has_hands_on
        })

    # Clean up old temporary markdown files with 'para' in name
    for old_f in proc_mod_dir.glob("*para.md"):
        old_f.unlink()

    # Generate _module.yaml
    module_meta = {
        "name": "Ansible Playbooks",
        "slug": module_slug,
        "description": "Master writing, executing, and structuring Ansible playbooks, variables, handlers, conditionals, and loops.",
        "display_order": 4,
        "total_chunks": len(module_chunks_meta),
        "total_questions": sum(c["question_count"] for c in module_chunks_meta),
        "chunks": module_chunks_meta
    }
    with open(proc_mod_dir / "_module.yaml", 'w', encoding='utf-8') as f:
        yaml.dump(module_meta, f, sort_keys=False, default_flow_style=False)
    print(f"\n[✓] Generated _module.yaml with {len(module_chunks_meta)} chunks ({module_meta['total_questions']} total quiz questions).")

    # Generate _topic.yaml
    topic_meta = {
        "name": "Ansible",
        "slug": "ansible",
        "description": "Master enterprise infrastructure automation, configuration management, and orchestration with Ansible.",
        "icon": "🔧"
    }
    with open(PROCESSED_DIR / topic_slug / "_topic.yaml", 'w', encoding='utf-8') as f:
        yaml.dump(topic_meta, f, sort_keys=False, default_flow_style=False)
    print("[✓] Generated _topic.yaml.")

if __name__ == "__main__":
    main()
