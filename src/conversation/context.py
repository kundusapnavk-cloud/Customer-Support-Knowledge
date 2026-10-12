# Why: the retriever now gets context from the previous question.
def build_contextual_query(
    current_question: str,
    history: list[dict],
) -> str:

    if not history:
        return current_question

    previous_user_questions = [
        message["content"]
        for message in history
        if message["role"] == "user"
    ]

    if not previous_user_questions:
        return current_question

    previous_question = previous_user_questions[-1]

    return (
        f"Previous topic: {previous_question}\n"
        f"Follow-up question: {current_question}"
    )