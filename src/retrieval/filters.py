# Why: this gives us a simple first version of metadata filtering.
def detect_category(query: str) -> str | None:
    query = query.lower()

    if any(word in query for word in ["refund", "payment", "invoice", "subscription", "price", "billing"]):
        return "billing"

    if any(word in query for word in ["password", "login", "email", "2fa", "account"]):
        return "account"

    if any(word in query for word in ["workspace", "member", "invite", "role", "permission"]):
        return "workspace"

    if any(word in query for word in ["slack", "github", "calendar", "integration"]):
        return "integrations"

    if any(word in query for word in ["not loading", "sync", "notification", "problem", "issue"]):
        return "troubleshooting"

    return None