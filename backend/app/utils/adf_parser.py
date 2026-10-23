def extract_text_from_adf(adf):
    if adf is None:
        return ""

    if isinstance(adf, str):
        return adf

    if isinstance(adf, list):
        return "".join(
            extract_text_from_adf(item)
            for item in adf
        )

    if isinstance(adf, dict):
        node_type = adf.get("type")

        if node_type == "text":
            return adf.get("text", "")

        content = adf.get("content", [])

        if node_type == "paragraph":
            return extract_text_from_adf(content) + "\n"

        if node_type == "heading":
            return extract_text_from_adf(content) + "\n"
        
        if node_type == "listItem":
            return "- " + extract_text_from_adf(content)

        return extract_text_from_adf(content)

    return ""

    


