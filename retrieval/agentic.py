import json

from retrieval.utils import AnthropicInterface


QUERY_EXPANSION_SYSTEM_PROMPT = """
You are part of an information system that processes user queries.
You expand a given query into at most 5 queries that are similar in meaning.
If the query is already detailed and specific, you can return fewer or no expansions.
The output format should be a list of strings.

Examples:

User query: "climate change effects"
Your output: ["impact of climate change", "consequences of global warming", "effects of environmental changes"]

User query: "machine learning algorithms"
Your output: ["neural networks", "clustering", "supervised learning", "deep learning"]
"""


def _expand_query_claude(query: str, model="claude-3-5-sonnet-20241022", **kwargs) -> list[str]:

    client = AnthropicInterface.get_client()

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        temperature=0,
        system=QUERY_EXPANSION_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f'"{query}"'
                    }
                ]
            }
        ]
    )

    return json.loads(message.content[0].text)


def expand_query(query: str, method="claude", **kwargs) -> list[str]:
    """
    Expands a query into a list of similar queries.
    
    Args:
        query: The query to expand.
    
    Returns:
        A list of expanded queries (includes the original).
    """

    if method == "claude":
        return _expand_query_claude(query, **kwargs)
    else:
        raise ValueError(f"Invalid query expansion method: {method}")
