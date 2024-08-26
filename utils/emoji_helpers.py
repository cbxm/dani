# emoji_helpers.py

import re

def extract_emoji(text):
    """
    Extract the first emoji from the given text.

    This function uses a regular expression to find and return the first
    emoji in the input text. It supports a wide range of Unicode emojis.

    Args:
        text (str): The text to extract emoji from.

    Returns:
        str or None: The first emoji found in the text, or None if no emoji is found.
    """
    # This regex pattern matches a wide range of Unicode emoji characters
    emoji_pattern = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]")
    match = emoji_pattern.search(text)
    return match.group(0) if match else None