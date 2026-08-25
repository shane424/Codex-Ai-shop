import re
from pathlib import Path

def safe_slug(value: str) -> str:
    return re.sub(r'-+','-',re.sub(r'[^a-z0-9]+','-',value.lower())).strip('-')[:120] or 'product'
def safe_filename(value: str, suffix: str) -> str: return safe_slug(value)+suffix
def safe_text(value: str) -> str:
    value=''.join(c for c in str(value) if c in '\n\t' or ord(c)>=32)
    return ("'"+value if value.startswith(('=','+','-','@')) else value)[:5000]
def within(root: Path, path: Path) -> bool:
    try: path.resolve().relative_to(root.resolve()); return True
    except ValueError: return False
