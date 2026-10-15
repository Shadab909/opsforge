#!/usr/bin/env python3
"""
OpsForge Content Processor
Converts HTML modules from knowledge_base/<topic>/<module>/index.html
into processed Markdown chunks, topic/module metadata, and quiz files.
"""

import os
import re
import sys
import shutil
import argparse
from pathlib import Path
from html.parser import HTMLParser
import yaml

class MarkdownConverter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = []
        self.in_pre = False
        self.in_code = False
        self.code_lang = ""
        self.in_table = False
        self.in_tr = False
        self.in_th = False
        self.in_td = False
        self.current_cell = []
        self.row_cells = []
        self.table_rows = []
        self.list_stack = []  # ('ul', count) or ('ol', count)
        self.current_href = ""
        self.skip_tags = {'script', 'style', 'nav', 'header', 'footer', 'svg', 'button'}
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag in self.skip_tags:
            self.skip_depth += 1
            return
        if self.skip_depth > 0:
            return

        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            level = int(tag[1])
            self.output.append(f"\n\n{'#' * level} ")
        elif tag == 'p':
            self.output.append("\n\n")
        elif tag == 'br':
            self.output.append("\n")
        elif tag == 'strong' or tag == 'b':
            self.output.append("**")
        elif tag == 'em' or tag == 'i':
            self.output.append("*")
        elif tag == 'code':
            if not self.in_pre:
                self.in_code = True
                self.output.append("`")
        elif tag == 'pre':
            self.in_pre = True
            classes = attrs_dict.get('class', '')
            lang = "bash"
            if 'yaml' in classes:
                lang = "yaml"
            elif 'python' in classes:
                lang = "python"
            elif 'json' in classes:
                lang = "json"
            elif 'sh' in classes or 'bash' in classes:
                lang = "bash"
            self.code_lang = lang
            self.output.append(f"\n\n```{self.code_lang}\n")
        elif tag in ('ul', 'ol'):
            self.list_stack.append([tag, 1])
            self.output.append("\n")
        elif tag == 'li':
            indent = "  " * (len(self.list_stack) - 1)
            if self.list_stack and self.list_stack[-1][0] == 'ol':
                num = self.list_stack[-1][1]
                self.output.append(f"\n{indent}{num}. ")
                self.list_stack[-1][1] += 1
            else:
                self.output.append(f"\n{indent}- ")
        elif tag == 'table':
            self.in_table = True
            self.table_rows = []
        elif tag == 'tr':
            self.in_tr = True
            self.row_cells = []
        elif tag in ('th', 'td'):
            if tag == 'th':
                self.in_th = True
            else:
                self.in_td = True
            self.current_cell = []
        elif tag == 'a':
            self.current_href = attrs_dict.get('href', '')
            if not self.in_table:
                self.output.append("[")
        elif tag == 'img':
            src = attrs_dict.get('src', '')
            alt = attrs_dict.get('alt', 'Image')
            if not src.endswith('.svg'):
                self.output.append(f"\n\n![{alt}]({src})\n\n")

    def handle_endtag(self, tag):
        if tag in self.skip_tags and self.skip_depth > 0:
            self.skip_depth -= 1
            return
        if self.skip_depth > 0:
            return

        if tag in ('strong', 'b'):
            if self.in_th or self.in_td:
                self.current_cell.append("**")
            elif not self.in_table:
                self.output.append("**")
        elif tag in ('em', 'i'):
            if self.in_th or self.in_td:
                self.current_cell.append("*")
            elif not self.in_table:
                self.output.append("*")
        elif tag == 'code':
            if not self.in_pre:
                self.in_code = False
                if self.in_th or self.in_td:
                    self.current_cell.append("`")
                elif not self.in_table:
                    self.output.append("`")
        elif tag == 'pre':
            self.in_pre = False
            self.output.append("\n```\n\n")
        elif tag in ('ul', 'ol'):
            if self.list_stack:
                self.list_stack.pop()
            self.output.append("\n")
        elif tag == 'a':
            if not self.in_table:
                self.output.append(f"]({self.current_href})")
            self.current_href = ""
        elif tag in ('th', 'td'):
            cell_text = "".join(self.current_cell).strip().replace("\n", " ")
            self.row_cells.append(cell_text)
            self.current_cell = []
            self.in_th = False
            self.in_td = False
        elif tag == 'tr':
            if self.row_cells:
                self.table_rows.append(self.row_cells)
            self.in_tr = False
        elif tag == 'table':
            self.in_table = False
            if self.table_rows:
                # Render markdown table
                header = self.table_rows[0]
                md_table = ["\n\n| " + " | ".join(header) + " |"]
                md_table.append("| " + " | ".join(["---"] * len(header)) + " |")
                for row in self.table_rows[1:]:
                    padded_row = row + [""] * (len(header) - len(row))
                    md_table.append("| " + " | ".join(padded_row[:len(header)]) + " |")
                md_table.append("\n\n")
                self.output.append("\n".join(md_table))

    def handle_data(self, data):
        if self.skip_depth > 0:
            return
        if self.in_th or self.in_td:
            self.current_cell.append(data)
            return
        if self.in_table:
            return
        # Skip doc link anchor symbols like ¶
        clean = data.replace("¶", "")
        self.output.append(clean)

    def get_markdown(self):
        text = "".join(self.output)
        # Collapse excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()


def extract_content_div(html_path):
    """Extracts inner HTML of <div class=md-content data-md-component=content>"""
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    # Look for md-content container
    start_match = re.search(r'<div[^>]*class=["\'][^"\']*md-content[^"\']*["\'][^>]*>', html)
    if not start_match:
        start_match = re.search(r'<article[^>]*class=["\'][^"\']*md-content__inner[^"\']*["\'][^>]*>', html)

    if not start_match:
        return html

    start_idx = start_match.start()
    return html[start_idx:]


def split_into_h2_sections(html_content):
    """
    Splits the HTML content by <h2 id=...> or <h2> tags.
    Returns a list of dicts: [{'title': str, 'html': str}]
    """
    # Regex to find H2 tags and their positions
    h2_pattern = re.compile(r'<h2[^>]*>(.*?)</h2>', re.IGNORECASE | re.DOTALL)
    matches = list(h2_pattern.finditer(html_content))
    
    sections = []
    if not matches:
        return [{'title': 'Overview', 'html': html_content}]

    for i, match in enumerate(matches):
        raw_title = match.group(1)
        # Strip internal tags like <a ...>&para;</a>
        clean_title = re.sub(r'<[^>]+>', '', raw_title).replace('¶', '').strip()
        
        start_pos = match.start()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(html_content)
        sec_html = html_content[start_pos:end_pos]
        
        sections.append({
            'title': clean_title,
            'html': sec_html
        })
        
    return sections


def html_to_markdown(html_snippet):
    converter = MarkdownConverter()
    converter.feed(html_snippet)
    return converter.get_markdown()


def slugify(text):
    text = text.lower()
    text = re.sub(r'^\d+[\.\s_-]+', '', text)  # remove leading numbers like '01. '
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text).strip('-')
    return text or 'section'


def process_module(topic_slug, module_slug, kb_root, processed_root):
    kb_mod_dir = Path(kb_root) / topic_slug / module_slug
    proc_mod_dir = Path(processed_root) / topic_slug / module_slug
    proc_mod_dir.mkdir(parents=True, exist_ok=True)
    
    index_html = kb_mod_dir / "index.html"
    if not index_html.exists():
        print(f"Error: {index_html} not found")
        return False
        
    print(f"--> Processing {topic_slug}/{module_slug} from {index_html}...")
    
    # 1. Copy supplementary files (.yaml, .sh, .yml, .conf)
    supp_dir = proc_mod_dir / "supplementary"
    supp_dir.mkdir(exist_ok=True)
    supp_count = 0
    for item in kb_mod_dir.iterdir():
        if item.is_file() and item.name != "index.html" and not item.name.startswith("."):
            shutil.copy2(item, supp_dir / item.name)
            supp_count += 1
    print(f"    Copied {supp_count} supplementary files.")

    # 2. Extract content and split sections
    content_html = extract_content_div(index_html)
    sections = split_into_h2_sections(content_html)
    
    # 3. Filter and group sections
    skip_titles = {
        'what will we learn?', 'prerequisites', 'summary',
        'quiz and review', 'hands-on exercises', '`yaml'
    }
    
    chunk_list = []
    chunk_idx = 1
    
    for sec in sections:
        title = sec['title'].strip()
        title_lower = title.lower()
        if any(skip in title_lower for skip in skip_titles):
            continue
            
        slug = f"{chunk_idx:02d}-{slugify(title)}"
        md_text = html_to_markdown(sec['html'])
        
        # Word count & reading time
        words = len(md_text.split())
        est_min = max(3, round(words / 150))
        
        # Frontmatter
        frontmatter = {
            'title': title,
            'slug': slug,
            'estimated_time': est_min,
            'has_hands_on': 'exercise' in title_lower or 'demo' in title_lower
        }
        
        md_file_content = f"""---
title: "{title}"
slug: "{slug}"
estimated_time: {est_min}
has_hands_on: {str(frontmatter['has_hands_on']).lower()}
---

{md_text}
"""
        chunk_file = proc_mod_dir / f"{slug}.md"
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(md_file_content)
            
        chunk_list.append({
            'slug': slug,
            'title': title,
            'file': f"{slug}.md",
            'estimated_time': est_min,
            'has_hands_on': frontmatter['has_hands_on']
        })
        chunk_idx += 1
        print(f"    Saved chunk [{slug}]: {title} (~{est_min} mins)")

    # 4. Write _module.yaml
    mod_meta = {
        'name': module_slug.replace('-', ' ').title(),
        'slug': module_slug,
        'description': f"Comprehensive guide and hands-on concepts for {module_slug}",
        'display_order': int(module_slug.split('-')[0]) if module_slug.split('-')[0].isdigit() else 99,
        'chunks': chunk_list
    }
    with open(proc_mod_dir / "_module.yaml", 'w', encoding='utf-8') as f:
        yaml.dump(mod_meta, f, sort_keys=False, default_flow_style=False)
    print(f"    Generated _module.yaml with {len(chunk_list)} chunks.")

    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process OpsForge knowledge base modules")
    parser.add_argument('--topic', default='ansible', help="Topic name (e.g. ansible)")
    parser.add_argument('--module', default='004-playbooks', help="Module directory name")
    parser.add_argument('--kb', default='knowledge_base', help="Path to knowledge_base")
    parser.add_argument('--out', default='processed', help="Output processed directory")
    args = parser.parse_args()

    # Topic metadata
    topic_dir = Path(args.out) / args.topic
    topic_dir.mkdir(parents=True, exist_ok=True)
    topic_meta_file = topic_dir / "_topic.yaml"
    if not topic_meta_file.exists():
        topic_meta = {
            'name': args.topic.capitalize(),
            'slug': args.topic,
            'description': "Master Ansible automation — from ad-hoc commands to modular playbooks, roles, and vault security.",
            'icon': "🔧"
        }
        with open(topic_meta_file, 'w', encoding='utf-8') as f:
            yaml.dump(topic_meta, f, sort_keys=False)
        print(f"Created topic metadata at {topic_meta_file}")

    process_module(args.topic, args.module, args.kb, args.out)

