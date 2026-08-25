from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from .sanitize import within

def generate_bundle(path: Path, files: list[Path], approved_root: Path) -> Path:
    path=Path(path); approved_root=Path(approved_root); path.parent.mkdir(parents=True,exist_ok=True); names=set()
    with ZipFile(path,'w',ZIP_DEFLATED) as archive:
        for item in files:
            item=Path(item)
            if not within(approved_root,item) or not item.is_file(): raise ValueError('bundle member is outside approved storage')
            name=item.name
            if name in names: raise ValueError('duplicate bundle entry')
            names.add(name); archive.write(item,name)
    return path
