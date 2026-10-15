#!/usr/bin/env python3
"""
Builder script to process:
- 003-modules (6 chunks + extensive quizzes)
- 006-git (6 chunks + extensive quizzes)
- 007-create-user (5 chunks + extensive quizzes)
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

def clean_html_to_markdown(html_text):
    # Remove script and style
    text = re.sub(r'<script.*?</script>', '', html_text, flags=re.DOTALL)
    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
    
    # Code blocks
    def repl_pre_code(m):
        code_content = m.group(2)
        code_content = html.unescape(code_content)
        # remove inner tags
        code_content = re.sub(r'<[^>]+>', '', code_content)
        classes = m.group(1) or ""
        lang = "bash"
        if "yaml" in classes:
            lang = "yaml"
        elif "python" in classes:
            lang = "python"
        elif "json" in classes:
            lang = "json"
        elif "sh" in classes or "bash" in classes:
            lang = "bash"
        return f"\n\n```{lang}\n{code_content.strip()}\n```\n\n"
        
    text = re.sub(r'<pre[^>]*><code[^>]*class=["\']?([^"\'>]*)["\']?[^>]*>(.*?)</code></pre>', repl_pre_code, text, flags=re.DOTALL)
    text = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', lambda m: f"\n\n```bash\n{html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()}\n```\n\n", text, flags=re.DOTALL)
    
    # Inline code
    text = re.sub(r'<code[^>]*>(.*?)</code>', lambda m: f"`{html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()}`", text, flags=re.DOTALL)
    
    # Headings
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', lambda m: f"\n\n### {html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).replace('&para;', '').replace('¶', '').strip()}\n\n", text, flags=re.DOTALL)
    text = re.sub(r'<h4[^>]*>(.*?)</h4>', lambda m: f"\n\n#### {html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).replace('&para;', '').replace('¶', '').strip()}\n\n", text, flags=re.DOTALL)
    text = re.sub(r'<h5[^>]*>(.*?)</h5>', lambda m: f"\n\n##### {html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).replace('&para;', '').replace('¶', '').strip()}\n\n", text, flags=re.DOTALL)

    # Lists
    text = re.sub(r'<li[^>]*>(.*?)</li>', lambda m: f"\n- {html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()}", text, flags=re.DOTALL)
    
    # Formatting
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', lambda m: f"**{html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()}**", text, flags=re.DOTALL)
    text = re.sub(r'<b[^>]*>(.*?)</b>', lambda m: f"**{html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()}**", text, flags=re.DOTALL)
    text = re.sub(r'<em[^>]*>(.*?)</em>', lambda m: f"*{html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()}*", text, flags=re.DOTALL)
    text = re.sub(r'<p[^>]*>(.*?)</p>', lambda m: f"\n\n{html.unescape(re.sub(r'<[^>]+>', ' ', m.group(1))).strip()}\n\n", text, flags=re.DOTALL)

    # Strip remaining HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    
    # Clean up whitespace
    text = text.replace("&para;", "").replace("¶", "")
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

print("Helper functions ready.")
