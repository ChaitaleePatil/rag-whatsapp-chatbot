user_sessions = {}

def get_user_memory(user_id: str):
    """
    Returns conversation history for a user.
    Stored as a list of (user, assistant) messages.
    """
    if user_id not in user_sessions:
        user_sessions[user_id] = []
    return user_sessions[user_id]

def add_to_memory(user_id: str, user_message: str, bot_message: str):
    user_sessions[user_id].append({
        "user": user_message,
        "bot": bot_message
    })
