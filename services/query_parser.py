from typing import Dict, List


# TODO: Must be rewritten to filter and return dynamic fields but
# also return the predicted fields.
def concatenate_query_results(query_results: Dict[str, any]) -> Dict[str, str]:
    """
    Concatenates all the texts from the query results and returns a string.
    Args:
        query_results (Dict[str, any]): The query results.
    Returns:
        str: The concatenated text from the query results.
    """
    business_texts: List[str] = []
    for query_result in query_results:
        for result in query_result.get("results", []):
            business_texts.append(result.get("text", ""))

    return {
        "account": " ".join(business_texts),
    }
