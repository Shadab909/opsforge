import re
import yaml
from pathlib import Path
import markdown
from app.config import Config

md_parser = markdown.Markdown(extensions=[
    'fenced_code',
    'tables',
    'codehilite',
    'toc',
    'nl2br',
    'attr_list'
], extension_configs={
    'codehilite': {
        'css_class': 'highlight',
        'guess_lang': False
    }
})

def parse_frontmatter(content: str):
    """Splits YAML frontmatter from Markdown body"""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        raw_yaml = match.group(1)
        body = content[match.end():]
        try:
            meta = yaml.safe_load(raw_yaml) or {}
        except Exception:
            meta = {}
        return meta, body
    return {}, content

def get_topics():
    topics = []
    if not Config.PROCESSED_DIR.exists():
        return topics

    for t_dir in sorted(Config.PROCESSED_DIR.iterdir()):
        if t_dir.is_dir():
            topic_meta_file = t_dir / "_topic.yaml"
            if topic_meta_file.exists():
                try:
                    with open(topic_meta_file, 'r', encoding='utf-8') as f:
                        meta = yaml.safe_load(f) or {}
                        meta["slug"] = t_dir.name
                        topics.append(meta)
                except Exception:
                    pass
    return topics

def get_topic(topic_slug: str):
    t_file = Config.PROCESSED_DIR / topic_slug / "_topic.yaml"
    if t_file.exists():
        try:
            with open(t_file, 'r', encoding='utf-8') as f:
                meta = yaml.safe_load(f) or {}
                meta["slug"] = topic_slug
                return meta
        except Exception:
            return None
    return None

def get_modules(topic_slug: str):
    modules = []
    topic_dir = Config.PROCESSED_DIR / topic_slug
    if not topic_dir.exists():
        return modules

    for m_dir in sorted(topic_dir.iterdir()):
        if m_dir.is_dir() and not m_dir.name.startswith(("_", ".")):
            m_file = m_dir / "_module.yaml"
            if m_file.exists():
                try:
                    with open(m_file, 'r', encoding='utf-8') as f:
                        meta = yaml.safe_load(f) or {}
                        meta["slug"] = m_dir.name
                        modules.append(meta)
                except Exception:
                    pass
    modules.sort(key=lambda x: x.get("display_order", 999))
    return modules

def get_module(topic_slug: str, module_slug: str):
    m_file = Config.PROCESSED_DIR / topic_slug / module_slug / "_module.yaml"
    if m_file.exists():
        try:
            with open(m_file, 'r', encoding='utf-8') as f:
                meta = yaml.safe_load(f) or {}
                meta["slug"] = module_slug
                return meta
        except Exception:
            return None
    return None

def get_chunk(topic_slug: str, module_slug: str, chunk_slug: str):
    chunk_file = Config.PROCESSED_DIR / topic_slug / module_slug / f"{chunk_slug}.md"
    if not chunk_file.exists():
        return None

    try:
        with open(chunk_file, 'r', encoding='utf-8') as f:
            raw = f.read()

        meta, body = parse_frontmatter(raw)
        
        # Clean and normalize image URLs to /static/assets/images/...
        body = re.sub(r'\]\((?:\.\./)*assets/images/+', '](/static/assets/images/', body)
        body = re.sub(r'src=["\'](?:\.\./)*assets/images/+', 'src="/static/assets/images/', body)
        body = re.sub(r'/static/assets/images/+', '/static/assets/images/', body)

        # Render markdown to HTML
        md_parser.reset()
        html_content = md_parser.convert(body)

        return {
            "meta": meta,
            "title": meta.get("title", chunk_slug.replace("-", " ").title()),
            "slug": chunk_slug,
            "estimated_time": meta.get("estimated_time", 5),
            "has_hands_on": meta.get("has_hands_on", False),
            "html": html_content
        }
    except Exception as e:
        print(f"Error loading chunk {chunk_slug}: {e}")
        return None

def get_chunk_quiz(topic_slug: str, module_slug: str, chunk_slug: str):
    quiz_file = Config.PROCESSED_DIR / topic_slug / module_slug / f"{chunk_slug}.quiz.yaml"
    if not quiz_file.exists():
        return None

    try:
        with open(quiz_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Error loading quiz {chunk_slug}: {e}")
        return None
