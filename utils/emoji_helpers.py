import re

def extract_emoji(text):
    emoji_pattern = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]")
    match = emoji_pattern.search(text)
    return match.group(0) if match else None
