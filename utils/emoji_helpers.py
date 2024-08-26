# emoji_helpers.py

import re

def extract_emoji(text):
    """
    Extract the first emoji from the given text.

    This function uses a regular expression to find and return the first
    emoji in the input text. It supports a wide range of Unicode emojis,
    including newer additions.

    Args:
        text (str): The text to extract emoji from.

    Returns:
        str or None: The first emoji found in the text, or None if no emoji is found.
    """
    # This regex pattern matches a wider range of Unicode emoji characters
    emoji_pattern = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251" 
        "]+"
    )
    match = emoji_pattern.search(text)
    return match.group(0) if match else None

# Test the function
if __name__ == "__main__":
    test_strings = [
        "Hello 👋",
        "Ice cube 🧊",
        "No emoji here",
        "Multiple emojis 🌟✨🌈"
    ]
    for string in test_strings:
        emoji = extract_emoji(string)
        print(f"Input: {string}")
        print(f"Extracted emoji: {emoji}")
        print()