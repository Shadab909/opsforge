#!/usr/bin/env python3
"""
Full Generator for:
- 003-modules
- 006-git
- 007-create-user
"""

import os
import re
import html
import yaml
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
KB_DIR = BASE_DIR / "knowledge_base" / "ansible"
PROC_DIR = BASE_DIR / "processed" / "ansible"

def setup_dirs(mod_name):
    mod_dir = PROC_DIR / mod_name
    mod_dir.mkdir(parents=True, exist_ok=True)
    supp_dir = mod_dir / "supplementary"
    supp_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy supplementary files from knowledge_base
    kb_mod_dir = KB_DIR / mod_name
    if kb_mod_dir.exists():
        for f in kb_mod_dir.iterdir():
            if f.is_file() and f.name != "index.html" and not f.name.startswith("."):
                shutil.copy2(f, supp_dir / f.name)
    return mod_dir

print("Generator framework initialized.")
