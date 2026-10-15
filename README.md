# 🔥 OpsForge — Local DevOps Practice & Learning Dashboard

OpsForge is an offline, local-first browser-based learning platform for practicing DevOps concepts. It transforms knowledge base labs and documentation into structured, interactive learning chunks with integrated knowledge check quizzes and portable local progress tracking.

---

## ⚡ Quick Start

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Run OpsForge from your terminal
python run.py
```

OpsForge will launch locally at `http://127.0.0.1:5000` and automatically open your default browser.

To stop the server at any time, press `Ctrl + C`.

---

## 🎯 Features

- **🚀 Terminal-Launched, Browser-Rendered**: Single command startup that opens your browser immediately.
- **📚 Modular Learning Flow**:
  1. **Topic** (e.g. Ansible)
  2. **Module** (e.g. Ansible Playbooks)
  3. **Chunk** (Focused subsection, e.g. YAML Basics, Handlers & Conditionals)
  4. **Concept Review** (Rich syntax-highlighted Markdown, tables, code copy buttons)
  5. **Knowledge Check Quiz** (5–10 MCQ and True/False questions per chunk with passing threshold and explanations)
- **💾 Portable User Data (`user_data/`)**:
  - All user profiles and progress are saved in `user_data/<username>/`.
  - Progress is stored in a clean local SQLite database (`progress.db`) alongside `profile.json`.
  - To back up or move your progress to another machine, simply copy your `user_data/` folder over!
- **💻 Hands-On Lab Scope**:
  - Architecture ready for future embedded browser terminal sandbox integration.
  - Sections with practical exercises feature a dedicated **Interactive Lab Terminal** placeholder.

---

## 🛠️ Processing More Modules

To convert additional HTML lab modules from `knowledge_base/<topic>/<module>/index.html` into structured chunks:

```bash
python scripts/process_content.py --topic ansible --module <module_folder_name>
```

The processor will automatically:
1. Parse the `<div class=md-content>` content.
2. Group subsections into readable Markdown chunks with YAML frontmatter.
3. Copy supplementary files (`.yaml`, `.sh`) into `processed/<topic>/<module>/supplementary/`.
4. Generate `_module.yaml` metadata.

---

## 📂 Project Structure

```
DevOps-Practice/
├── run.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
│
├── app/                            # Flask web application
│   ├── __init__.py                 # Application factory
│   ├── config.py                   # App configuration
│   ├── database.py                 # SQLite database & profile manager
│   ├── content_loader.py           # Markdown & YAML loader
│   ├── routes/                     # Route blueprints
│   │   ├── auth.py                 # Profile selection & creation
│   │   ├── dashboard.py            # Overview & stats
│   │   ├── modules.py              # Topics, modules, and chunk reader
│   │   ├── quiz.py                 # Quiz runner & grading engine
│   │   └── progress.py             # Progress API
│   ├── templates/                  # Jinja2 HTML templates
│   │   ├── base.html               # Master layout (Dark DevOps theme)
│   │   ├── profile_select.html     # Profile picker/creator
│   │   ├── dashboard.html          # Main dashboard
│   │   ├── topic.html              # Modules list
│   │   ├── module.html             # Chunks list
│   │   ├── chunk.html              # Concept content viewer
│   │   ├── quiz.html               # Section quiz
│   │   ├── quiz_result.html        # Score & explanation review
│   │   └── 404.html                # Error page
│   └── static/
│       ├── css/style.css           # Custom styles & typography
│       └── js/app.js               # Copy code, AJAX mark-read, validation
│
├── knowledge_base/                 # Source HTML and lab exercises (Input)
│   └── ansible/
│       └── 004-playbooks/
│
├── processed/                      # Structured content consumed by app (Output)
│   └── ansible/
│       ├── _topic.yaml
│       └── 004-playbooks/
│           ├── _module.yaml
│           ├── 01-what-are-playbooks.md
│           ├── 01-what-are-playbooks.quiz.yaml
│           ├── ...
│           └── supplementary/
│
└── user_data/                      # Local portable profile databases
    └── <username>/
        ├── profile.json            # Profile metadata & preferences
        └── progress.db             # User SQLite progress database
```

---

## 🔒 Offline & Local-First

OpsForge operates completely offline without external telemetry or online account dependencies. All stylesheets and code highlighters are loaded with clean fallbacks, and user progress is kept entirely on your filesystem.
