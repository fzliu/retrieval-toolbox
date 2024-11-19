import re


def _chunk_markdown_by_headers(text: str) -> list[str]:
    """
    Chunks markdown files into sections based on headers. This function ensures
    that all chunks are contextualized with all headers that precede them. For
    example, the document:

        # Fee
        ## Fi
        ### Fo
        This is a paragraph.
        #### Fum
        This is another paragraph.
        # Jack
        This is a third paragraph.
    
    Would result in three chunks:
    
            # Fee
            ## Fi
            ### Fo
            This is a paragraph.

            # Fee
            ## Fi
            ### Fo
            #### Fum
            This is another paragraph.
    
            # Jack
            This is a third paragraph.
    """

    headers = [None] * 6

    chunks = [""]
    for line in text.split("\n"):
        # Count the number of '#'s that the line begins with
        if m := re.search("#+", line):
            l = len(m.group(0))
            headers[l-1] = line.strip()
            headers[l:] = [None] * (6 - l)
            chunks.append("\n".join(filter(None, headers)))
        else:
            chunks[-1] += line

    # Remove the first chunk, if empty (i.e. document starts with a header)
    if not chunks[0]:
        chunks.pop(0)

    return chunks


def chunk_markdown(text: str, method="headers", **kwargs) -> list[str]:
    """
    Chunk markdown files into sections.

    Args:
        text: The markdown text to chunk.
        method: The method to use for chunking (default is "headers").
    
    Returns:
        A list of chunks in string format.
    """
    
    if method == "headers":
        return _chunk_markdown_by_headers(text, **kwargs)
    else:
        raise ValueError(f"Method {method} not supported.")

