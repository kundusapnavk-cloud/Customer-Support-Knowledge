from pathlib import Path
import yaml

from .models import SupportDocument
#This function takes a path to a markdown file, reads the content, and extracts metadata from the front matter (if present). It returns a SupportDocument object with the extracted information.
def load_markdown_document(path: Path) -> SupportDocument:
    text = path.read_text(encoding="utf-8")

    metadata = {}
    content = text

    if text.startswith("---"):
        parts = text.split("---", 2)

        if len(parts) == 3:
            metadata = yaml.safe_load(parts[1]) or {}
            content = parts[2].strip()

    return SupportDocument(
        content=content,
        title=metadata.get("title", path.stem),
        category=metadata.get("category", "unknown"),
        product=metadata.get("product"),
        plan=metadata.get("plan"),
        last_updated=metadata.get("last_updated"),
        source_type=metadata.get("source_type"),
        source_path=str(path),
    )
def load_knowledge_base(data_dir: str) -> list[SupportDocument]:
    documents = []

    for path in Path(data_dir).rglob("*.md"):
        document = load_markdown_document(path)
        documents.append(document)

    return documents