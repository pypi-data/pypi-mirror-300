def extract_buffer_text(buffer: str) -> str:
    """
    Extracts the text representation of the HTML buffer.

    Args:
        buffer (str): The HTML buffer.

    Returns:
        str: The text representation of the HTML buffer.
    """
    ...

def extract_buffer_markdown(
    buffer: str, output_links: bool, output_images: bool
) -> str:
    """
    Extracts the Markdown representation of the HTML buffer.

    Args:
        buffer (str): The HTML buffer.
        output_links (bool): Whether to output links.
        output_images (bool): Whether to output images.

    Returns:
        str: The Markdown representation of the HTML buffer.
    """
    ...
