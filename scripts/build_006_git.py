#!/usr/bin/env python3
"""
Builder for 006-git (Git Integration with Ansible)
Generates 6 chunks with 100 comprehensive questions.
"""

import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROC_MOD_DIR = BASE_DIR / "processed" / "ansible" / "006-git"
PROC_MOD_DIR.mkdir(parents=True, exist_ok=True)
SUPP_DIR = PROC_MOD_DIR / "supplementary"
SUPP_DIR.mkdir(parents=True, exist_ok=True)

# Copy supplementary files
KB_DIR = BASE_DIR / "knowledge_base" / "ansible" / "006-git"
if KB_DIR.exists():
    for f in KB_DIR.iterdir():
        if f.is_file() and f.name != "index.html" and not f.name.startswith("."):
            import shutil
            shutil.copy2(f, SUPP_DIR / f.name)

CHUNKS = [
    {
        "slug": "01-git-module-basics",
        "title": "01. Git Module Basics",
        "estimated_time": 7,
        "has_hands_on": False,
        "content": """## Git Module Basics (`ansible.builtin.git`)

The `ansible.builtin.git` module enables Ansible to manage Git repositories on remote target machines. It is one of the most widely used modules for continuous deployment (CD), application delivery, and infrastructure-as-code synchronization.

### Where Does Git Execute?

> **Fundamental Principle:**  
> The Git module executes `git` **on the remote managed node**, NOT on the Ansible control machine.  
> Therefore, the `git` binary **must be installed on target hosts** before calling this module.

```text
[Ansible Control Node] ──SSH──► [Remote Target Node]
                                       │
                                1. Runs 'git' CLI
                                2. Connects to GitHub/GitLab/Bitbucket
                                3. Pulls repo into destination path
```

### Basic Syntax

```yaml
- name: Deploy application repository
  ansible.builtin.git:
    repo: https://github.com/example/webapp.git
    dest: /var/www/webapp
    version: main
```

### Key Parameters Overview

| Parameter | Type | Default | Description |
|---|---|---|---|
| `repo` | String | *Required* | The URI of the Git repository (HTTPS, SSH, or local file path). |
| `dest` | Path | *Required* | The absolute destination path on the target host where the repo should be cloned. |
| `version` | String | `HEAD` | What version/branch/tag/commit to checkout. |
| `update` | Boolean | `true` | Whether to pull in new changes if the repository already exists. |
| `force` | Boolean | `false` | If `true`, discards any uncommitted local modifications on the remote host. |
| `key_file` | Path | None | Path to private SSH key for private repository authentication. |
| `accept_hostkey` | Boolean | `false` | Automatically accept unknown host keys (adds to `known_hosts`). |
| `depth` | Integer | None | Creates a shallow clone with a history truncated to the specified number of commits. |
| `recursive` | Boolean | `true` | Automatically initializes and clones git submodules. |

### Module Return Values

When the Git task executes, it returns:
- `changed`: `true` if files were cloned or commit updated; `false` if already at the requested version.
- `before`: The commit SHA prior to task execution (or `null` if fresh clone).
- `after`: The commit SHA after task execution.
""",
        "quiz": {
            "passing_score": 70,
            "questions": [
                {
                    "type": "mcq",
                    "question": "On which machine must the 'git' command-line binary be installed for the ansible.builtin.git module to function?",
                    "options": [
                        "On the remote managed host where the repository is cloned",
                        "Only on the Ansible control node",
                        "Only on the central GitHub/GitLab server",
                        "In the local Python site-packages directory"
                    ],
                    "correct": "On the remote managed host where the repository is cloned",
                    "explanation": "The git module delegates execution to the remote node's local git client over SSH."
                },
                {
                    "type": "mcq",
                    "question": "What are the two mandatory parameters required for any ansible.builtin.git task?",
                    "options": ["repo and dest", "repo and version", "dest and key_file", "url and branch"],
                    "correct": "repo and dest",
                    "explanation": "`repo` (the source repository URL) and `dest` (the target directory) are the only required arguments."
                },
                {
                    "type": "true_false",
                    "question": "The git module will automatically install the git package on the target node if it is missing.",
                    "correct": False,
                    "explanation": "Ansible will fail with an executable not found error. You must install git first (e.g. using the apt or dnf module)."
                },
                {
                    "type": "mcq",
                    "question": "What is the default value of the 'version' parameter if omitted?",
                    "options": ["HEAD", "main", "master", "latest"],
                    "correct": "HEAD",
                    "explanation": "If version is omitted, Ansible defaults to `HEAD` (the default branch of the remote repository)."
                },
                {
                    "type": "mcq",
                    "question": "What return key provides the Git commit hash of the repository BEFORE the task executed?",
                    "options": ["before", "previous_commit", "old_sha", "initial_head"],
                    "correct": "before",
                    "explanation": "The module returns `before` (old commit SHA) and `after` (new commit SHA)."
                },
                {
                    "type": "true_false",
                    "question": "If a repository is already at the target commit on the remote server, the git module reports 'changed: false'.",
                    "correct": True,
                    "explanation": "The git module is idempotent; if the local HEAD already matches the requested version, no changes are made."
                },
                {
                    "type": "mcq",
                    "question": "What FQCN refers to the built-in Git module in modern Ansible?",
                    "options": ["ansible.builtin.git", "community.general.git", "ansible.posix.git", "vcs.git.clone"],
                    "correct": "ansible.builtin.git",
                    "explanation": "The git module is bundled directly in core under `ansible.builtin.git`."
                },
                {
                    "type": "mcq",
                    "question": "What type of path is expected for the 'dest' parameter?",
                    "options": [
                        "An absolute filesystem path on the remote host",
                        "A relative path from the control node's current directory",
                        "A URL pointing to a storage bucket",
                        "An inventory hostname"
                    ],
                    "correct": "An absolute filesystem path on the remote host",
                    "explanation": "Best practice and standard convention requires an absolute path (e.g. /var/www/app) on the target host."
                },
                {
                    "type": "true_false",
                    "question": "The git module can clone repositories using both HTTPS and SSH protocols.",
                    "correct": True,
                    "explanation": "Both HTTPS URLs (https://github.com/...) and SSH URLs (git@github.com:...) are fully supported."
                },
                {
                    "type": "mcq",
                    "question": "What return value indicates the Git commit hash AFTER the task successfully completes?",
                    "options": ["after", "current_head", "new_commit", "target_sha"],
                    "correct": "after",
                    "explanation": "`after` contains the resulting 40-character SHA-1 commit hash."
                },
                {
                    "type": "mcq",
                    "question": "What happens if the 'dest' directory does not exist on the remote host prior to cloning?",
                    "options": [
                        "Ansible automatically creates the parent directories and clones the repo",
                        "The task fails because the folder must be manually created first",
                        "Ansible clones the repo into /tmp instead",
                        "Ansible prompts the user for directory creation"
                    ],
                    "correct": "Ansible automatically creates the parent directories and clones the repo",
                    "explanation": "Git creates the target directory during the clone operation."
                },
                {
                    "type": "true_false",
                    "question": "By default, the git module automatically clones submodules recursively.",
                    "correct": True,
                    "explanation": "`recursive` defaults to `true`, cloning any registered submodules."
                },
                {
                    "type": "mcq",
                    "question": "Which parameter controls whether new commits should be fetched from origin if the repo already exists on the remote node?",
                    "options": ["update", "pull", "fetch", "sync"],
                    "correct": "update",
                    "explanation": "`update: true` (default) checks for and pulls updates; `update: false` leaves existing clones untouched."
                },
                {
                    "type": "true_false",
                    "question": "If git on the remote host exits with a fatal error (such as repository not found), Ansible marks the task as failed.",
                    "correct": True,
                    "explanation": "Any non-zero exit code from git CLI commands triggers task failure."
                },
                {
                    "type": "mcq",
                    "question": "Which parameter creates a shallow clone by fetching only the most recent N commits?",
                    "options": ["depth", "shallow", "truncate", "history_limit"],
                    "correct": "depth",
                    "explanation": "`depth: 1` creates a shallow clone containing only the tip commit, saving bandwidth and disk."
                },
                {
                    "type": "true_false",
                    "question": "The git module can be used to commit and push changes from the remote server back to GitHub.",
                    "correct": False,
                    "explanation": "The git module is designed for deployment and checkout (pull/clone); it does not commit or push changes."
                }
            ]
        }
    },
    {
        "slug": "02-cloning-repositories",
        "title": "02. Cloning Repositories",
        "estimated_time": 7,
        "has_hands_on": False,
        "content": """## Cloning Repositories with Ansible

Cloning a Git repository onto target machines is the first step in automated deployments.

### Basic Clone Task

```yaml
- name: Clone web application repository
  ansible.builtin.git:
    repo: 'https://github.com/octocat/Hello-World.git'
    dest: /opt/hello-world
```

### Destination Directory Scenarios

When Ansible processes the `dest` path, several scenarios can occur:

1. **`dest` does not exist**: Ansible creates `/opt/hello-world` and performs `git clone`. (`changed: true`)
2. **`dest` exists and is already a Git clone of `repo`**: Ansible verifies the commit. If it matches, it skips cloning. (`changed: false`)
3. **`dest` exists but is an empty directory**: Ansible successfully clones the repo into it. (`changed: true`)
4. **`dest` exists, is NOT a Git repo, and is NOT empty**: **Error!** Git will refuse to clone into a non-empty directory that lacks a `.git` folder.

```text
Check dest: /opt/hello-world
     │
     ├─ Doesn't exist ──────────► Clone repo [CHANGED]
     ├─ Exists (.git present) ──► Check commits [OK / CHANGED]
     ├─ Exists (empty) ─────────► Clone repo [CHANGED]
     └─ Exists (non-git files) ─► Fatal Error! [FAILED]
```

---

### Controlling Cloning Behavior

#### 1. Cloning without Updating Later (`update: false`)
If you only want to clone the repository once during initial setup and never pull subsequent changes automatically:

```yaml
- name: Clone base configuration repository once
  ansible.builtin.git:
    repo: 'https://github.com/example/config.git'
    dest: /etc/app/config
    update: false
```

#### 2. Specifying Clone Permissions & Ownership
After cloning, you often need to ensure web server permissions (e.g. `www-data`):

```yaml
- name: Clone and set permissions
  ansible.builtin.git:
    repo: 'https://github.com/example/api.git'
    dest: /var/www/api
  become: yes

- name: Enforce ownership on cloned files
  ansible.builtin.file:
    path: /var/www/api
    owner: www-data
    group: www-data
    recurse: yes
  become: yes
```

#### 3. Bare Repositories (`bare: true`)
To create a bare repository (containing only Git metadata, without a working tree) for a central Git server:

```yaml
- name: Create bare central repository
  ansible.builtin.git:
    repo: 'https://github.com/example/repo.git'
    dest: /git/repo.git
    bare: yes
```
""",
        "quiz": {
            "passing_score": 70,
            "questions": [
                {
                    "type": "mcq",
                    "question": "What happens if the 'dest' directory on the remote host exists, is not empty, and does NOT contain a .git directory?",
                    "options": [
                        "The task fails because Git refuses to clone into a non-empty non-git directory",
                        "Ansible deletes all existing files without warning and clones the repo",
                        "Ansible creates a subfolder named repo_clone inside it",
                        "Ansible automatically converts the directory into a bare git repository"
                    ],
                    "correct": "The task fails because Git refuses to clone into a non-empty non-git directory",
                    "explanation": "Standard Git safety prevents overwriting existing directories containing foreign files."
                },
                {
                    "type": "mcq",
                    "question": "How do you configure the git task to clone a repository only once and never fetch new commits on subsequent runs?",
                    "options": ["update: false", "clone_only: true", "pull: never", "once: true"],
                    "correct": "update: false",
                    "explanation": "`update: false` tells Ansible: 'If the directory exists, leave it as is without checking remote origin'."
                },
                {
                    "type": "true_false",
                    "question": "If the destination folder already contains a valid git clone at the desired commit, re-running the task reports changed: false.",
                    "correct": True,
                    "explanation": "Ansible detects that HEAD already matches the requested state and performs no action (idempotent)."
                },
                {
                    "type": "mcq",
                    "question": "Which parameter creates a repository without a working directory (used for Git server mirrors)?",
                    "options": ["bare: yes", "no_worktree: true", "mirror_only: yes", "metadata: true"],
                    "correct": "bare: yes",
                    "explanation": "`bare: yes` creates a bare repository containing only objects and references."
                },
                {
                    "type": "mcq",
                    "question": "What is the recommended practice for enforcing web server ownership (www-data) on a cloned repository?",
                    "options": [
                        "Follow the git task with an ansible.builtin.file task with recurse: yes and owner/group set",
                        "Pass owner=www-data directly to the git module",
                        "Edit the .git/config file manually",
                        "Run chown with the raw module"
                    ],
                    "correct": "Follow the git task with an ansible.builtin.file task with recurse: yes and owner/group set",
                    "explanation": "The file module with `recurse: yes` ensures all cloned files and subdirectories have the correct ownership."
                },
                {
                    "type": "true_false",
                    "question": "Ansible git clone operations require root / become permissions even if cloning into the connecting user's home directory.",
                    "correct": False,
                    "explanation": "Privilege escalation is only needed if writing to system-protected paths like `/var/www/` or `/opt/`."
                },
                {
                    "type": "mcq",
                    "question": "What return value in the git task result shows whether a fresh clone occurred or an existing repo was updated?",
                    "options": [
                        "result.before is null on fresh clones, and contains a SHA on existing repositories",
                        "result.fresh_clone is true",
                        "result.is_new_repo is true",
                        "result.status == 'cloned'"
                    ],
                    "correct": "result.before is null on fresh clones, and contains a SHA on existing repositories",
                    "explanation": "On a newly cloned repository, `before` is `null` because no prior commit existed locally."
                },
                {
                    "type": "true_false",
                    "question": "You can clone a local repository on the remote machine by passing a filesystem path to the 'repo' parameter (e.g. repo: /git/myrepo).",
                    "correct": True,
                    "explanation": "Git supports local file paths as repositories (file:// or raw filesystem paths)."
                },
                {
                    "type": "mcq",
                    "question": "Which parameter specifies whether to clone submodules when cloning a repository?",
                    "options": ["recursive", "submodules", "clone_children", "all_modules"],
                    "correct": "recursive",
                    "explanation": "`recursive: yes` (the default) clones any nested submodules."
                },
                {
                    "type": "mcq",
                    "question": "What happens if 'clone: no' is specified when the destination directory does not exist?",
                    "options": [
                        "The task fails because it cannot operate on a non-existent destination without cloning",
                        "Ansible creates an empty directory",
                        "Ansible downloads a zip archive instead",
                        "Ansible prints a warning and skips"
                    ],
                    "correct": "The task fails because it cannot operate on a non-existent destination without cloning",
                    "explanation": "`clone: no` expects an existing repository to already be present at `dest`."
                },
                {
                    "type": "true_false",
                    "question": "Cloning via HTTPS from a public repository requires configuring SSH deploy keys on target servers.",
                    "correct": False,
                    "explanation": "Public HTTPS repositories require zero credentials or SSH keys to clone."
                },
                {
                    "type": "mcq",
                    "question": "What parameter allows you to pass custom git command-line options during clone operations?",
                    "options": ["archive_opts / clone_opts", "extra_flags", "cli_args", "git_custom"],
                    "correct": "archive_opts / clone_opts",
                    "explanation": "`clone_opts` (or module flags) allows passing extra arguments directly to `git clone`."
                },
                {
                    "type": "true_false",
                    "question": "If you change the 'repo' parameter to a completely different repository URL on an existing 'dest', Ansible automatically replaces the repo without error.",
                    "correct": False,
                    "explanation": "If the destination is already a git repo pointing to a different origin, Ansible will raise an error unless forced."
                },
                {
                    "type": "mcq",
                    "question": "How can you ensure destination parent directories exist with specific permissions before cloning?",
                    "options": [
                        "Use ansible.builtin.file with state: directory prior to the git clone task",
                        "Pass create_parents=yes to the git module",
                        "Set auto_mkdir=true",
                        "Run mkdir -p in a shell task"
                    ],
                    "correct": "Use ansible.builtin.file with state: directory prior to the git clone task",
                    "explanation": "Creating parent folders declaratively with `file: state=directory` ensures permissions and ownership are set properly."
                },
                {
                    "type": "mcq",
                    "question": "What is the result of 'git: repo=... dest=/opt/app' if /opt/app exists as an empty directory?",
                    "options": [
                        "Ansible successfully clones the repository into /opt/app",
                        "Ansible deletes /opt/app",
                        "Ansible skips the task",
                        "Ansible reports FAILED"
                    ],
                    "correct": "Ansible successfully clones the repository into /opt/app",
                    "explanation": "Git allows cloning into pre-existing directories as long as they are completely empty."
                },
                {
                    "type": "true_false",
                    "question": "Cloning large repositories without 'depth: 1' fetches the entire commit history, which can consume unnecessary disk space and time.",
                    "correct": True,
                    "explanation": "Full clones download every revision and historical blob; shallow clones (`depth: 1`) are much faster for deployments."
                }
            ]
        }
    },
    {
        "slug": "03-updating-repositories",
        "title": "03. Updating Repositories",
        "estimated_time": 7,
        "has_hands_on": False,
        "content": """## Updating Repositories and Handling Changes

By default, the `ansible.builtin.git` module continuously keeps target repositories in sync with their upstream source.

### Default Update Behavior (`update: true`)

Every time the task runs:
1. It queries the remote Git server for the latest commit on the requested `version` branch.
2. If new commits exist upstream, it performs a fetch and fast-forward merge.
3. It sets `changed: true` and updates `after` with the new commit SHA.
4. If no new commits exist, it does nothing and sets `changed: false`.

```yaml
- name: Pull latest updates for web application
  ansible.builtin.git:
    repo: 'https://github.com/example/webapp.git'
    dest: /var/www/webapp
    version: production
    update: yes
```

---

### Handling Local Conflicts: `force: yes`

In real-world environments, someone might manually edit a config file on the target server, or an application might create uncommitted files in the working tree.

By default, Git will **refuse to pull** if uncommitted changes would be overwritten. The Ansible task will fail with:
```text
fatal: [web1]: FAILED! => {"msg": "Local changes would be overwritten by merge..."}
```

#### Discarding Remote Changes with `force: yes`
Setting `force: yes` forces Git to discard any local uncommitted changes, performing the equivalent of `git reset --hard` and checking out the clean upstream version:

```yaml
- name: Force pull and discard any dirty local changes
  ansible.builtin.git:
    repo: 'https://github.com/example/webapp.git'
    dest: /var/www/webapp
    version: main
    force: yes
```

> **Warning:** `force: yes` permanently wipes any uncommitted file changes in the remote working tree. Only use it when the target machine is strictly disposable or managed solely via Git.

---

### Triggering Handlers on Update

A common pattern is to restart the web server or rerun database migrations **only when new code is actually pulled**:

```yaml
- name: Deploy application code
  ansible.builtin.git:
    repo: 'https://github.com/example/app.git'
    dest: /opt/app
    version: main
  notify: Restart Application Service

handlers:
  - name: Restart Application Service
    ansible.builtin.service:
      name: myapp
      state: restarted
```

If `git` reports `changed: false` (code is already up to date), the handler is skipped and the service is not interrupted!
""",
        "quiz": {
            "passing_score": 70,
            "questions": [
                {
                    "type": "mcq",
                    "question": "What is the default value of the 'update' parameter in the git module?",
                    "options": ["true (or yes)", "false (or no)", "force", "check"],
                    "correct": "true (or yes)",
                    "explanation": "`update` defaults to `true`, ensuring Ansible pulls upstream changes whenever the task runs."
                },
                {
                    "type": "mcq",
                    "question": "What error occurs if uncommitted local edits exist on the remote host and 'update: yes' runs with default settings?",
                    "options": [
                        "Git refuses to merge and Ansible fails with a 'Local changes would be overwritten' error",
                        "Ansible automatically commits the local changes to a new branch",
                        "Ansible deletes the remote repository and reclones",
                        "The task succeeds and ignores upstream changes"
                    ],
                    "correct": "Git refuses to merge and Ansible fails with a 'Local changes would be overwritten' error",
                    "explanation": "Git protects uncommitted changes from being silently clobbered unless force: yes is provided."
                },
                {
                    "type": "mcq",
                    "question": "Which parameter instructs the git module to discard local modifications and force a clean checkout?",
                    "options": ["force: yes", "clean: true", "overwrite: yes", "reset: hard"],
                    "correct": "force: yes",
                    "explanation": "`force: yes` discards local modifications (running git reset --hard) to align with upstream."
                },
                {
                    "type": "true_false",
                    "question": "Setting 'force: yes' will recover files that were deleted locally on the managed node.",
                    "correct": True,
                    "explanation": "Because `force: yes` resets to the target commit, missing tracked files are restored from the repository."
                },
                {
                    "type": "mcq",
                    "question": "How can you configure a service restart to execute ONLY when a new commit is pulled by the git task?",
                    "options": [
                        "Use the 'notify' directive on the git task pointing to a handler",
                        "Add 'restart_service: yes' to the git module",
                        "Always restart the service at the end of the playbook",
                        "Run systemctl restart in the same git task"
                    ],
                    "correct": "Use the 'notify' directive on the git task pointing to a handler",
                    "explanation": "Handlers only trigger when the notifying task reports `changed: true`."
                },
                {
                    "type": "true_false",
                    "question": "If you set 'update: false' on an existing repository, Ansible will check the remote origin for new commits.",
                    "correct": False,
                    "explanation": "`update: false` skips checking remote origin entirely if the destination folder exists."
                },
                {
                    "type": "mcq",
                    "question": "In the registered result of a git task, how can a conditional test if the code was actually updated?",
                    "options": [
                        "when: git_result.changed",
                        "when: git_result.status == 'updated'",
                        "when: git_result.before == git_result.after",
                        "when: git_result.pulled == true"
                    ],
                    "correct": "when: git_result.changed",
                    "explanation": "In Ansible, `result.changed` evaluates to `true` whenever modifications occurred."
                },
                {
                    "type": "mcq",
                    "question": "What Git command is roughly equivalent to what the git module does when 'update: yes' and 'force: yes' are set?",
                    "options": [
                        "git fetch && git reset --hard origin/<version>",
                        "git commit -am 'auto' && git push",
                        "git rebase --interactive",
                        "git stash pop"
                    ],
                    "correct": "git fetch && git reset --hard origin/<version>",
                    "explanation": "It fetches remote references and hard-resets the working directory to match the target commit."
                },
                {
                    "type": "true_false",
                    "question": "'force: yes' will also remove untracked files in the working directory that are not ignored by .gitignore.",
                    "correct": False,
                    "explanation": "By default, reset --hard only alters tracked files; removing untracked files requires git clean."
                },
                {
                    "type": "mcq",
                    "question": "What return value comparison proves that no new commits were pulled during task execution?",
                    "options": [
                        "git_result.before == git_result.after",
                        "git_result.changed == true",
                        "git_result.rc == 1",
                        "git_result.after is null"
                    ],
                    "correct": "git_result.before == git_result.after",
                    "explanation": "If `before` and `after` commit hashes are identical, no updates occurred."
                },
                {
                    "type": "true_false",
                    "question": "If upstream Git has force-pushed a rewritten commit history, 'update: yes' without 'force: yes' will fail fast-forward.",
                    "correct": True,
                    "explanation": "Standard git pulls require fast-forward merges; non-fast-forward histories fail unless `force: yes` is enabled."
                },
                {
                    "type": "mcq",
                    "question": "Which parameter controls whether the working tree files are actually updated to match the commit?",
                    "options": ["force", "verify_commit", "bare", "separate_git_dir"],
                    "correct": "force",
                    "explanation": "`force` controls overriding working tree state."
                },
                {
                    "type": "true_false",
                    "question": "A task with 'update: yes' will fail if the remote target node has lost internet or network connectivity to the Git server.",
                    "correct": True,
                    "explanation": "Because it attempts a remote network fetch, network failure will cause the git module to return a fatal error."
                },
                {
                    "type": "mcq",
                    "question": "What parameter is used to specify a custom remote name other than the default 'origin'?",
                    "options": ["remote", "origin_name", "upstream", "remote_name"],
                    "correct": "remote",
                    "explanation": "The `remote` parameter defines the remote repository name (default: `origin`)."
                },
                {
                    "type": "true_false",
                    "question": "Handlers notified by a git task run immediately before the next task in the playbook starts.",
                    "correct": False,
                    "explanation": "By default in Ansible, handlers run at the end of the play (or when flushed via meta: flush_handlers)."
                },
                {
                    "type": "mcq",
                    "question": "Why is 'force: yes' considered risky on development servers?",
                    "options": [
                        "It will overwrite and permanently destroy any uncommitted developer edits on that host",
                        "It causes Git to delete the remote repository on GitHub",
                        "It revokes SSH keys across the cluster",
                        "It requires a system reboot"
                    ],
                    "correct": "It will overwrite and permanently destroy any uncommitted developer edits on that host",
                    "explanation": "Any temporary fixes or test edits made directly on the server will be lost without recovery."
                }
            ]
        }
    },
    {
        "slug": "04-branches-and-tags",
        "title": "04. Branches and Tags",
        "estimated_time": 8,
        "has_hands_on": False,
        "content": """## Working with Branches, Tags, and Commits

The `version` parameter in the `ansible.builtin.git` module determines exactly what state your repository should be in.

### The `version` Parameter

The `version` parameter accepts:
1. **Branch name**: e.g. `main`, `master`, `develop`, `release/2.0`
2. **Tag name**: e.g. `v1.2.0`, `release-2026.10`
3. **Commit SHA**: e.g. `4b825dc642cb6eb9a060e54bf8d69288fbee4904` (or short SHA `4b825dc`)
4. **Git reference**: e.g. `refs/pull/42/head`

---

### Examples

#### 1. Checking Out a Specific Branch
```yaml
- name: Deploy from staging branch
  ansible.builtin.git:
    repo: https://github.com/example/app.git
    dest: /var/www/app
    version: staging
```

#### 2. Pinning to a Release Tag (Best Practice for Production)
In production, deploying from dynamic branch names (like `main`) can lead to unintended updates if new commits are pushed. Pinning to an immutable **tag** ensures exact repeatability:

```yaml
- name: Deploy versioned release tag
  ansible.builtin.git:
    repo: https://github.com/example/app.git
    dest: /var/www/app
    version: v2.4.1
```

#### 3. Pinning to an Exact Commit SHA
For absolute immutability:

```yaml
- name: Checkout specific commit SHA
  ansible.builtin.git:
    repo: https://github.com/example/app.git
    dest: /var/www/app
    version: e5a8b79c3d4f128e67a90b1234567890abcdef12
```

---

### Understanding "Detached HEAD" State

When you checkout a **tag** or a specific **commit SHA**, Git places the working tree in a **"detached HEAD"** state.  
- This is completely **normal and expected** for deployment targets.
- It simply means HEAD points directly to a commit object rather than a named branch reference.
- Ansible handles detached HEAD states seamlessly and reports idempotent updates accurately.

### Switching Between Branches

If a server is currently on `version: staging` and you update your playbook to `version: production`, Ansible will:
1. Fetch the remote refs.
2. Switch branches from `staging` to `production`.
3. Check out the latest commit on `production`.
4. Report `changed: true`.
""",
        "quiz": {
            "passing_score": 70,
            "questions": [
                {
                    "type": "mcq",
                    "question": "Which parameter in the git module specifies the target branch, tag, or commit to checkout?",
                    "options": ["version", "branch", "tag", "commit"],
                    "correct": "version",
                    "explanation": "`version` is the unified parameter that accepts branch names, tag names, or commit SHAs."
                },
                {
                    "type": "mcq",
                    "question": "Why is deploying by immutable Git tags (e.g. version: v1.5.0) recommended over dynamic branches (version: main) in production?",
                    "options": [
                        "Tags guarantee that the exact same tested code is deployed across all servers without unexpected updates",
                        "Branches require root privileges to checkout",
                        "Tags run faster than branches in Python",
                        "Git disables branches on remote Linux machines"
                    ],
                    "correct": "Tags guarantee that the exact same tested code is deployed across all servers without unexpected updates",
                    "explanation": "Tags represent static release milestones, preventing unexpected code changes from breaking production."
                },
                {
                    "type": "true_false",
                    "question": "Checking out a specific Git tag or commit SHA results in a 'detached HEAD' state on the remote machine.",
                    "correct": True,
                    "explanation": "Detached HEAD simply means HEAD points directly to a specific commit rather than a branch pointer."
                },
                {
                    "type": "mcq",
                    "question": "What happens if a target server is on branch 'staging' and you run a playbook task with 'version: main'?",
                    "options": [
                        "Ansible fetches remote changes, switches to branch 'main', and checks out the latest commit",
                        "The task fails because branch switching is forbidden in Ansible",
                        "Ansible deletes the directory and reclones",
                        "Ansible creates a merge conflict"
                    ],
                    "correct": "Ansible fetches remote changes, switches to branch 'main', and checks out the latest commit",
                    "explanation": "Ansible cleanly handles switching branches and updates the working tree."
                },
                {
                    "type": "mcq",
                    "question": "Can you specify a 7-character short commit SHA (e.g. version: 8a3f2bc) in the version parameter?",
                    "options": [
                        "Yes, Git and Ansible accept both short and full 40-character commit hashes",
                        "No, only full 40-character SHAs are valid",
                        "No, only branch names are permitted",
                        "Only if the commit starts with 000"
                    ],
                    "correct": "Yes, Git and Ansible accept both short and full 40-character commit hashes",
                    "explanation": "Git resolves short SHAs as long as they are unique within the repository."
                },
                {
                    "type": "true_false",
                    "question": "A detached HEAD state in a deployment directory prevents web servers (like Nginx or Apache) from reading the files.",
                    "correct": False,
                    "explanation": "Detached HEAD is purely an internal Git reference state; filesystem files are regular readable files."
                },
                {
                    "type": "mcq",
                    "question": "What happens if you specify a non-existent branch name (e.g. version: does-not-exist)?",
                    "options": [
                        "The task fails with a 'Remote branch does-not-exist not found' error",
                        "Ansible automatically creates a new empty branch with that name",
                        "Ansible falls back to main",
                        "Ansible creates a tag instead"
                    ],
                    "correct": "The task fails with a 'Remote branch does-not-exist not found' error",
                    "explanation": "If the reference cannot be resolved on the remote, the git command exits with code 128 (failure)."
                },
                {
                    "type": "true_false",
                    "question": "If you are pinned to a specific tag 'v1.0.0', re-running the playbook will never report 'changed: true' once deployed.",
                    "correct": True,
                    "explanation": "Because a tag is immutable and points to a static commit SHA, `before` and `after` will match."
                },
                {
                    "type": "mcq",
                    "question": "Which parameter controls whether git submodules are checked out alongside branches?",
                    "options": ["recursive: yes", "submodules: all", "include_submodules: true", "children: fetch"],
                    "correct": "recursive: yes",
                    "explanation": "`recursive: yes` initializes and clones submodules recursively."
                },
                {
                    "type": "mcq",
                    "question": "What parameter allows checkout of pull request references (e.g. refs/pull/15/head) from GitHub?",
                    "options": ["version", "refspec", "pr_number", "pull_request"],
                    "correct": "version",
                    "explanation": "The `version` parameter supports custom Git refspecs directly."
                },
                {
                    "type": "true_false",
                    "question": "The git module supports passing a Jinja2 variable for the version parameter (e.g. version: \"{{ app_version }}\").",
                    "correct": True,
                    "explanation": "You can dynamically control versions per environment (e.g. staging vs prod) using variables."
                },
                {
                    "type": "mcq",
                    "question": "What parameter can verify GPG commit signatures during checkout?",
                    "options": ["verify_commit: yes", "gpg_check: true", "signature: required", "trust_gpg: yes"],
                    "correct": "verify_commit: yes",
                    "explanation": "`verify_commit: yes` verifies the GPG signature of the checked out commit."
                },
                {
                    "type": "true_false",
                    "question": "If a tag on the remote repository is deleted and replaced with a different commit, 'force: yes' is needed to update the local tag reference.",
                    "correct": True,
                    "explanation": "Rewriting tags requires force updating local tag references."
                },
                {
                    "type": "mcq",
                    "question": "What is the default ref used when version is omitted?",
                    "options": ["HEAD", "master", "trunk", "origin/master"],
                    "correct": "HEAD",
                    "explanation": "The default value is string 'HEAD'."
                },
                {
                    "type": "true_false",
                    "question": "Branch names in Git are case-sensitive on Linux systems.",
                    "correct": True,
                    "explanation": "Git branch references (`feature` vs `Feature`) are case-sensitive."
                },
                {
                    "type": "mcq",
                    "question": "Which command-line option in Git is used by the module when tracking a new remote branch?",
                    "options": ["--track origin/<branch>", "--bind <branch>", "--remote <branch>", "--pair origin"],
                    "correct": "--track origin/<branch>",
                    "explanation": "Git sets up tracking branches using `--track`."
                }
            ]
        }
    },
    {
        "slug": "05-authentication-and-ssh",
        "title": "05. Authentication and SSH",
        "estimated_time": 9,
        "has_hands_on": False,
        "content": """## Authentication and SSH for Private Repositories

When cloning private repositories from GitHub, GitLab, or Bitbucket, target machines must authenticate securely.

### Authentication Methods

1. **SSH Deploy Keys (Recommended)**: A dedicated SSH key pair with read-only access to the specific repository.
2. **Personal Access Tokens (PAT) via HTTPS**: HTTPS URL containing an access token.
3. **SSH Agent Forwarding**: Forwarding your local control node's SSH credentials over the connection.

---

### Method 1: Using SSH Keys with `key_file`

The cleanest approach is providing a dedicated deploy private key on the remote machine:

```yaml
- name: Clone private repository using SSH key
  ansible.builtin.git:
    repo: 'git@github.com:myorg/private-repo.git'
    dest: /var/www/private-app
    key_file: /home/deployer/.ssh/id_ed25519_deploy
    accept_hostkey: yes
```

#### Key Parameters:
- `key_file`: Path to the private SSH key file on the remote host.
- `accept_hostkey: yes`: **Crucial!** If connecting to `github.com` for the first time, SSH prompts with:
  ```text
  The authenticity of host 'github.com' can't be established. Are you sure you want to continue connecting (yes/no)?
  ```
  Setting `accept_hostkey: yes` automatically adds the remote host key to `~/.ssh/known_hosts`, preventing tasks from hanging indefinitely waiting for interactive terminal input!

---

### Method 2: Custom SSH Options (`ssh_opts`)

You can pass custom SSH flags using `ssh_opts`:

```yaml
- name: Clone with custom SSH options
  ansible.builtin.git:
    repo: 'git@gitlab.internal.corp:devops/infra.git'
    dest: /opt/infra
    ssh_opts: "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
    key_file: /etc/ssl/deploy_key
```

---

### Method 3: HTTPS with Tokens & Ansible Vault

For HTTPS clones requiring authentication, you can embed tokens into the URL:

```yaml
# In production, store the token in an encrypted vault variable!
- name: Clone private repository via HTTPS token
  ansible.builtin.git:
    repo: "https://{{ github_token }}@github.com/myorg/private-app.git"
    dest: /var/www/app
```

> **Security Warning:** When using HTTPS credentials in URLs, Git stores the full URL (including the token) in `.git/config` on the remote host. Protect the `.git` folder permissions or prefer SSH deploy keys!
""",
        "quiz": {
            "passing_score": 70,
            "questions": [
                {
                    "type": "mcq",
                    "question": "What happens if a git task attempts to clone via SSH from GitHub for the first time without 'accept_hostkey: yes' or a pre-populated known_hosts file?",
                    "options": [
                        "SSH pauses indefinitely waiting for interactive 'yes/no' confirmation, causing Ansible to hang or timeout",
                        "Ansible automatically accepts the key silently",
                        "Git switches to unencrypted HTTP automatically",
                        "The remote host deletes the SSH service"
                    ],
                    "correct": "SSH pauses indefinitely waiting for interactive 'yes/no' confirmation, causing Ansible to hang or timeout",
                    "explanation": "Unrecognized host keys prompt interactive confirmation; automated processes hang without accept_hostkey: yes."
                },
                {
                    "type": "mcq",
                    "question": "Which parameter in the git module specifies the path to a private SSH key file on the target host?",
                    "options": ["key_file", "ssh_key", "identity_file", "private_key"],
                    "correct": "key_file",
                    "explanation": "`key_file` designates the private key path on the managed host."
                },
                {
                    "type": "true_false",
                    "question": "The 'key_file' path refers to a private key on the Ansible control machine, which is transferred on demand.",
                    "correct": False,
                    "explanation": "`key_file` specifies the path to an SSH key already located on the remote target host."
                },
                {
                    "type": "mcq",
                    "question": "What does the 'accept_hostkey: yes' parameter do?",
                    "options": [
                        "Automatically accepts and appends the remote Git server's host key to the remote known_hosts file",
                        "Allows any client to connect to the server without a password",
                        "Generates a new host key for SSHD",
                        "Disables SSH encryption"
                    ],
                    "correct": "Automatically accepts and appends the remote Git server's host key to the remote known_hosts file",
                    "explanation": "`accept_hostkey: yes` automatically adds the fingerprint to known_hosts to prevent interactive prompts."
                },
                {
                    "type": "mcq",
                    "question": "Where does Git store repository URLs by default on the target system after cloning?",
                    "options": [
                        "Inside <dest>/.git/config",
                        "Inside /etc/git.conf",
                        "In the Ansible cache directory",
                        "In the Linux kernel keyring"
                    ],
                    "correct": "Inside <dest>/.git/config",
                    "explanation": "Git saves the origin URL in the repository's `.git/config` file."
                },
                {
                    "type": "true_false",
                    "question": "Embedding cleartext passwords or personal access tokens directly into playbook YAML files is a critical security risk.",
                    "correct": True,
                    "explanation": "Tokens should be stored in Ansible Vault (`ansible-vault encrypt_string`) or environment variables."
                },
                {
                    "type": "mcq",
                    "question": "What parameter passes custom arguments directly to the SSH client during git operations?",
                    "options": ["ssh_opts", "ssh_flags", "ssh_args", "extra_ssh"],
                    "correct": "ssh_opts",
                    "explanation": "`ssh_opts` allows passing arbitrary SSH options like `-o StrictHostKeyChecking=no`."
                },
                {
                    "type": "mcq",
                    "question": "Why are Git Deploy Keys preferred over developer personal access tokens for production servers?",
                    "options": [
                        "Deploy keys can be scoped to read-only access for a single specific repository",
                        "Deploy keys bypass SSH encryption for faster transfers",
                        "Personal tokens expire every 10 minutes",
                        "GitHub does not support tokens on Linux"
                    ],
                    "correct": "Deploy keys can be scoped to read-only access for a single specific repository",
                    "explanation": "Deploy keys follow the principle of least privilege: read-only access limited to one repository."
                },
                {
                    "type": "true_false",
                    "question": "The private key specified in 'key_file' must have appropriate permissions (e.g. 0600) or OpenSSH will refuse to use it.",
                    "correct": True,
                    "explanation": "OpenSSH ignores private keys that are readable by group or others (permission too open error)."
                },
                {
                    "type": "mcq",
                    "question": "Which module can be used prior to the git task to deploy an SSH private key with 0600 permissions?",
                    "options": ["ansible.builtin.copy", "ansible.builtin.ping", "ansible.builtin.user", "ansible.builtin.service"],
                    "correct": "ansible.builtin.copy",
                    "explanation": "Use `copy` with `mode: '0600'` to securely place the SSH private key."
                },
                {
                    "type": "true_false",
                    "question": "SSH Agent Forwarding can be configured in ansible.cfg by setting 'ssh_args = -o ForwardAgent=yes'.",
                    "correct": True,
                    "explanation": "Agent forwarding allows the remote target to use the control node's local SSH agent credentials."
                },
                {
                    "type": "mcq",
                    "question": "What format is used for an SSH repository URL on GitHub?",
                    "options": ["git@github.com:owner/repo.git", "ssh://github.com/owner/repo", "https://github.com/owner/repo.git", "git://github.com/owner/repo"],
                    "correct": "git@github.com:owner/repo.git",
                    "explanation": "`git@github.com:owner/repo.git` is the standard SCP-style SSH syntax for GitHub."
                },
                {
                    "type": "true_false",
                    "question": "Using 'accept_hostkey: yes' modifies the known_hosts file of the user executing the task on the target machine.",
                    "correct": True,
                    "explanation": "It appends the key to `~/.ssh/known_hosts` of the remote user."
                },
                {
                    "type": "mcq",
                    "question": "How can you securely provide a GitHub token to a git task without committing it to Git in plain text?",
                    "options": [
                        "Use Ansible Vault to encrypt the variable: {{ vault_github_token }}",
                        "Write it in a comment in the playbook",
                        "Store it in /tmp/token.txt with 0777 permissions",
                        "Include it in the git commit message"
                    ],
                    "correct": "Use Ansible Vault to encrypt the variable: {{ vault_github_token }}",
                    "explanation": "Ansible Vault encrypts sensitive strings using AES-256."
                },
                {
                    "type": "true_false",
                    "question": "If an SSH deploy key has a passphrase, Ansible will automatically detect it and prompt for it on the terminal during execution.",
                    "correct": False,
                    "explanation": "Passphrase-protected keys will fail in non-interactive Ansible tasks unless loaded into an active ssh-agent."
                },
                {
                    "type": "mcq",
                    "question": "Which SSH key algorithm is modern, highly secure, and generates compact keys recommended for deploy keys?",
                    "options": ["Ed25519", "DSA", "DES", "MD5"],
                    "correct": "Ed25519",
                    "explanation": "Ed25519 is the modern standard for fast, compact, and secure SSH keys."
                },
                {
                    "type": "true_false",
                    "question": "Setting 'ssh_opts: \"-o StrictHostKeyChecking=no\"' completely disables SSH host authenticity verification.",
                    "correct": True,
                    "explanation": "Disabling StrictHostKeyChecking skips host key validation, which is convenient but vulnerable to MITM attacks."
                },
                {
                    "type": "mcq",
                    "question": "What is the security risk of leaving personal access tokens in the .git/config on multi-tenant production servers?",
                    "options": [
                        "Any user with read access to the directory can extract the token and impersonate the developer",
                        "The token corrupts Git branches",
                        "The Linux kernel crashes upon reading the file",
                        "It makes the repository public"
                    ],
                    "correct": "Any user with read access to the directory can extract the token and impersonate the developer",
                    "explanation": "Cleartext tokens in config files can be stolen by unauthorized processes or users with local read access."
                }
            ]
        }
    },
    {
        "slug": "06-patterns-and-best-practices",
        "title": "06. Common Patterns and Best Practices",
        "estimated_time": 8,
        "has_hands_on": False,
        "content": """## Common Patterns and Production Best Practices

Implementing the `git` module in production pipelines requires adhering to established patterns for performance, reliability, and security.

---

### Pattern 1: High-Performance Shallow Clones (`depth: 1`)

For large repositories with years of Git history, downloading every historical commit on every deployment node wastes massive bandwidth and disk I/O.

Use `depth: 1` to create a **shallow clone** containing only the latest revision:

```yaml
- name: Fast shallow deployment of web app
  ansible.builtin.git:
    repo: https://github.com/myorg/huge-monorepo.git
    dest: /var/www/app
    version: production
    depth: 1
```

Benefits:
- Up to **90% reduction** in download size and deployment duration.
- Keeps deployment servers lean by storing only active application files.

---

### Pattern 2: Atomic Zero-Downtime Deployments (Symlink Pattern)

Cloning or pulling directly into an active document root (e.g. `/var/www/html`) can cause race conditions or 500 errors while files are actively being rewritten during user requests.

The standard industry pattern uses versioned release folders and an atomic symlink:

```text
/var/www/app/
   ├── releases/
   │     ├── 20261015-v1.0/
   │     └── 20261015-v1.1/   <── Cloned via Git
   └── current ───(symlink)───► /var/www/app/releases/20261015-v1.1/
```

```yaml
- name: Create release directory
  ansible.builtin.file:
    path: "/var/www/app/releases/{{ release_id }}"
    state: directory

- name: Checkout release code
  ansible.builtin.git:
    repo: https://github.com/example/app.git
    dest: "/var/www/app/releases/{{ release_id }}"
    version: "{{ app_version }}"
    depth: 1

- name: Atomically switch current symlink
  ansible.builtin.file:
    src: "/var/www/app/releases/{{ release_id }}"
    dest: /var/www/app/current
    state: link
```

---

### Pattern 3: Single Branch Clones

If your repository contains dozens of feature branches that are never needed in production, configure `single_branch: yes`:

```yaml
- name: Clone only the production branch
  ansible.builtin.git:
    repo: https://github.com/example/app.git
    dest: /opt/app
    version: main
    single_branch: yes
```

---

### Summary of Git Module Best Practices

1. **Always use absolute paths** for `dest` (e.g. `/var/www/app`, never relative paths).
2. **Pin to Git Tags or Commit SHAs** in production to prevent unintended branch drift.
3. **Use `depth: 1`** on CI/CD pipelines and deployment targets for maximum speed.
4. **Use read-only SSH Deploy Keys** rather than personal developer tokens.
5. **Combine with Handlers** to restart daemons or build assets only when `changed: true`.
""",
        "quiz": {
            "passing_score": 70,
            "questions": [
                {
                    "type": "mcq",
                    "question": "What is the primary benefit of setting 'depth: 1' in the git module?",
                    "options": [
                        "It performs a shallow clone with only the most recent commit, dramatically saving bandwidth and disk space",
                        "It prevents developers from committing bugs",
                        "It compiles Python code into binary before cloning",
                        "It enables multi-threading on the control node"
                    ],
                    "correct": "It performs a shallow clone with only the most recent commit, dramatically saving bandwidth and disk space",
                    "explanation": "`depth: 1` truncates Git history to a single commit, reducing clone time and size by up to 90%."
                },
                {
                    "type": "mcq",
                    "question": "In the atomic symlink deployment pattern, how is the active application version switched without downtime?",
                    "options": [
                        "By updating a symbolic link ('current') to point to the newly cloned release directory",
                        "By stopping the web server for 10 minutes",
                        "By renaming files one by one while the server is running",
                        "By rebooting the server after each pull"
                    ],
                    "correct": "By updating a symbolic link ('current') to point to the newly cloned release directory",
                    "explanation": "Switching a filesystem symlink is an atomic operation in POSIX operating systems, avoiding partial-write race conditions."
                },
                {
                    "type": "true_false",
                    "question": "Relative paths (e.g. dest: myapp) should always be avoided in the 'dest' parameter in production playbooks.",
                    "correct": True,
                    "explanation": "Relative paths depend on the remote user's current working directory, which can cause unpredictable placements."
                },
                {
                    "type": "mcq",
                    "question": "Which parameter ensures only the requested branch is fetched, ignoring all other remote branches?",
                    "options": ["single_branch: yes", "only_branch: true", "one_branch: yes", "exclusive_branch: true"],
                    "correct": "single_branch: yes",
                    "explanation": "`single_branch: yes` clones only the history leading to the tip of the specified branch."
                },
                {
                    "type": "mcq",
                    "question": "What is the danger of running 'git pull' directly into an active, running web document root (/var/www/html)?",
                    "options": [
                        "Visitors might request files in the middle of being overwritten, causing partial loads or 500 errors",
                        "Git will delete the web server binary",
                        "The Linux kernel will lock the filesystem into read-only mode",
                        "The SSL certificates will be revoked"
                    ],
                    "correct": "Visitors might request files in the middle of being overwritten, causing partial loads or 500 errors",
                    "explanation": "Non-atomic updates create race conditions where partial files or mismatched dependencies are served."
                },
                {
                    "type": "true_false",
                    "question": "Setting 'depth: 1' is ideal if you intend to run 'git blame' or inspect years of commit history on the production server.",
                    "correct": False,
                    "explanation": "Shallow clones lack historical commits, so historical inspection tools like git log and git blame are limited."
                },
                {
                    "type": "mcq",
                    "question": "How does Ansible know when to fire a handler attached to a git deployment task?",
                    "options": [
                        "When the git task returns 'changed: true' (meaning new code was pulled or cloned)",
                        "Handlers always execute regardless of task outcome",
                        "When git returns an error exit code",
                        "Only if the user explicitly presses Enter"
                    ],
                    "correct": "When the git task returns 'changed: true' (meaning new code was pulled or cloned)",
                    "explanation": "Handlers only execute if at least one notifying task reports a change."
                },
                {
                    "type": "true_false",
                    "question": "Shallow clones ('depth: 1') can still be updated on subsequent runs when 'update: yes' is active.",
                    "correct": True,
                    "explanation": "Git supports fetching and advancing shallow clones seamlessly."
                },
                {
                    "type": "mcq",
                    "question": "What parameter is used to checkout nested Git repositories defined in a .gitmodules file?",
                    "options": ["recursive: yes", "nested: true", "submodules: clone", "children: all"],
                    "correct": "recursive: yes",
                    "explanation": "`recursive: yes` runs `git submodule update --init --recursive`."
                },
                {
                    "type": "mcq",
                    "question": "Which of the following is an anti-pattern when using the git module in production?",
                    "options": [
                        "Deploying to dynamic branches (like 'main') without pinning to release tags",
                        "Using absolute paths for dest",
                        "Using read-only SSH deploy keys",
                        "Setting depth: 1 for faster deployment"
                    ],
                    "correct": "Deploying to dynamic branches (like 'main') without pinning to release tags",
                    "explanation": "Deploying unpinned branches allows untested commits pushed by developers to immediately reach production."
                },
                {
                    "type": "true_false",
                    "question": "Atomic symlink deployments make rolling back to a previous version as simple as pointing the symlink to the older release directory.",
                    "correct": True,
                    "explanation": "Instant rollbacks are the signature advantage of symlink release patterns."
                },
                {
                    "type": "mcq",
                    "question": "What parameter can verify the GPG signature of git commits during deployment?",
                    "options": ["verify_commit: yes", "gpg: true", "check_sig: yes", "valid_gpg: true"],
                    "correct": "verify_commit: yes",
                    "explanation": "`verify_commit: yes` verifies the commit's GPG signature against trusted public keys."
                },
                {
                    "type": "true_false",
                    "question": "Ansible's git module can checkout private repositories without credentials if the repository is marked internal on GitHub.",
                    "correct": False,
                    "explanation": "Both private and internal repositories require authentication (SSH key or token)."
                },
                {
                    "type": "mcq",
                    "question": "What parameter can be used to set the git remote tracking name if not using 'origin'?",
                    "options": ["remote", "upstream_name", "tracking", "remote_origin"],
                    "correct": "remote",
                    "explanation": "The `remote` parameter defines the remote name (default: `origin`)."
                },
                {
                    "type": "true_false",
                    "question": "Using the 'file' module to remove old release directories (keeping e.g. the last 5 releases) is a recommended maintenance practice.",
                    "correct": True,
                    "explanation": "Pruning old releases prevents deployment disks from filling up over time."
                },
                {
                    "type": "mcq",
                    "question": "Which parameter ensures the repository is archived into a tar/zip file rather than left as a git repo?",
                    "options": ["archive", "dest_format", "zip", "tarball"],
                    "correct": "archive",
                    "explanation": "`archive: /path/to/archive.tar.gz` creates a clean tarball of the checked-out version."
                },
                {
                    "type": "true_false",
                    "question": "The git module automatically reloads web servers (like Nginx) whenever it pulls code.",
                    "correct": False,
                    "explanation": "The git module only manages Git repository state. Service reloads must be configured via handlers."
                },
                {
                    "type": "mcq",
                    "question": "What is the primary reason to use SSH deploy keys instead of HTTPS with personal credentials?",
                    "options": [
                        "SSH deploy keys do not leave personal developer passwords stored in plaintext in the .git/config file",
                        "HTTPS is not supported on Linux",
                        "SSH keys are slower than HTTP",
                        "GitHub discontinued HTTPS in 2020"
                    ],
                    "correct": "SSH deploy keys do not leave personal developer passwords stored in plaintext in the .git/config file",
                    "explanation": "SSH keys are stored safely with restricted permissions, whereas HTTPS embeds tokens in `.git/config`."
                }
            ]
        }
    }
]

module_chunk_entries = []
for ch in CHUNKS:
    slug = ch["slug"]
    title = ch["title"]
    est_time = ch["estimated_time"]
    has_ho = ch["has_hands_on"]
    content = ch["content"]
    quiz = ch["quiz"]
    
    md_content = f"""---
title: "{title}"
slug: "{slug}"
estimated_time: {est_time}
has_hands_on: {str(has_ho).lower()}
---

{content}
"""
    with open(PROC_MOD_DIR / f"{slug}.md", "w", encoding="utf-8") as f:
        f.write(md_content)
        
    with open(PROC_MOD_DIR / f"{slug}.quiz.yaml", "w", encoding="utf-8") as f:
        yaml.dump(quiz, f, sort_keys=False, default_flow_style=False)
        
    module_chunk_entries.append({
        "slug": slug,
        "title": title,
        "file": f"{slug}.md",
        "estimated_time": est_time,
        "has_hands_on": has_ho
    })

mod_meta = {
    "name": "Git Integration",
    "slug": "006-git",
    "description": "Master Git integration with Ansible: repository cloning, continuous updates, branch & tag pinning, SSH deploy key authentication, and atomic zero-downtime deployment patterns.",
    "display_order": 6,
    "chunks": module_chunk_entries
}

with open(PROC_MOD_DIR / "_module.yaml", "w", encoding="utf-8") as f:
    yaml.dump(mod_meta, f, sort_keys=False, default_flow_style=False)

print(f"✅ Successfully built 006-git with {len(CHUNKS)} chunks and {sum(len(c['quiz']['questions']) for c in CHUNKS)} questions!")
