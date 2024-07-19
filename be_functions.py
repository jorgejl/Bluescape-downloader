import re

def sanitize_filename(filename):
    """
    Sanitize a string to make it a valid filename.
    
    :param filename: The input filename string.
    :return: A sanitized version of the filename string.
    """
    # Remove invalid characters
    invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'
    filename = re.sub(invalid_chars, '', filename)
    
    # Trim leading/trailing whitespace and periods
    filename = filename.strip().strip('.')
    
    # Ensure the filename is not empty
    if len(filename) == 0:
        raise ValueError("Filename cannot be empty after sanitization")
    
    # Limit the length of the filename to 255 characters
    filename = filename[:255]
    
    return filename
