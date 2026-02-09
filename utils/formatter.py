import re
def format_whatsapp_response(text: str) -> str:
    """
    Format the chatbot response for WhatsApp readability.

    - Adds line breaks
    - Converts numbered or comma-separated lists to bullets
    - Optional emoji highlights
    """

    # Convert commas separating items to bullets if more than one item
    if ',' in text and len(text.split(',')) > 1:
        items = [f"• {item.strip()}" for item in text.split(',')]
        text = "\n".join(items)

    # Ensure double line breaks after sentences for readability
    text = text.replace('. ', '.\n\n')

    # Remove markdown symbols (*, **, bullets, hyphens)
    text = re.sub(r"[*•\-]", "", text)

    # Remove multiple spaces created after cleanup
    text = re.sub(r"\s+", " ", text)

    # Convert colon sections into readable blocks
    text = text.replace(":", ":\n")

    # Add spacing after sentences
    text = text.replace(". ", ".\n\n")

    return text.strip()


def add_intro(text: str) -> str:
    """
    Optionally prepend a friendly intro to messages.
    """
    return (
        "Change Networks Assistant\n"
        "Here are the details based on your query:\n\n"
        f"{text}"
    )
