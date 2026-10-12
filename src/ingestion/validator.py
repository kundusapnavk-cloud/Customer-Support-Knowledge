from .models import SupportDocument


def validate_document(doc: SupportDocument) -> list[str]:
    errors = []

    if not doc.title:
        errors.append("Missing title")

    if not doc.category:
        errors.append("Missing category")

    if not doc.content.strip():
        errors.append("Empty content")

    if len(doc.content.strip()) < 50:
        errors.append("Content is too short")

    return errors