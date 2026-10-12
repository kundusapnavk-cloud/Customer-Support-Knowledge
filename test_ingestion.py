
from src.ingestion.loader import load_knowledge_base
from src.ingestion.validator import validate_document
from pathlib import Path

#This is only a test. We give it one Markdown file and check: Did our loader actually read everything correctly?
#--------------------------------------------------------------------------------------------------------------------------------#
#path = Path("data/billing/refund-policy.md")

#document = load_markdown_document(path)

#print("Title:", document.title)
#print("Category:", document.category)
#print("Plan:", document.plan)
#print("Source type:", document.source_type)
#print("Content:", document.content[:200])
#----------------------------------------------------------------------------------------------------------------------------#
#documents = load_knowledge_base("data")

#print("Total documents:", len(documents))

#for doc in documents:
#    print(doc.title, "-", doc.category)
#---------------------------------------------------------------------------------------------------------------------------------------#
# documents = load_knowledge_base("data")

# print("Total documents:", len(documents))

# for doc in documents:
#     errors = validate_document(doc)

#     if errors:
#         print(doc.title, "->", errors)
#------------------------------------------------------------------------------------------------------------------------------------------------#