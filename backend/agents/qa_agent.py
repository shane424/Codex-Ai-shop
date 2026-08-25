from pathlib import Path
import shutil
from backend.validation.artifacts import validate_pdf, validate_xlsx
from .provider import LLMProvider, get_provider

def review_artifact(path: Path, visible_content: str, root=Path('products'), provider: LLMProvider|None=None):
    result=validate_xlsx(path) if path.suffix.lower()=='.xlsx' else validate_pdf(path)
    review=(provider or get_provider()).review(visible_content); reasons=result.reasons+review.reasons
    destination=Path(root)/('approved' if not reasons else 'rejected')/path.name; destination.parent.mkdir(parents=True,exist_ok=True)
    shutil.move(path,destination); return destination,reasons
