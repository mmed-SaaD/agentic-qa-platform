from backend.app.utils.adf_parser import extract_text_from_adf

def test_extract_text_from_paragraph():
    adf = {
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Hello "},
                    {"type": "text", "text": "World!"}
                ]
            }
        ]
    }

    result = extract_text_from_adf(adf)

    assert result == "Hello World!\n"

def test_extract_text_from_none():
    result = extract_text_from_adf(None)
    
    assert result == ""

def test_extract_text_from_string():
    result = extract_text_from_adf("Simple descritpion !")

    assert result == "Simple descritpion !"

def test_extract_text_from_bullet_list():
    adf = {
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Acceptance Criteria:"
                    }
                ]
            },
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "User can log in."
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "Invalid password shows an error."
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    result = extract_text_from_adf(adf)

    assert result == (
        "Acceptance Criteria:\n"
        "- User can log in.\n"
        "- Invalid password shows an error.\n"
    )

def test_heading_followed_by_paragraph():
    adf = {
        "type": "doc",
        "content": [
            {
                "type": "heading",
                "attrs": {"level": 2},
                "content": [
                    {
                        "type": "text",
                        "text": "Acceptance Criteria",
                    }
                ],
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "AC1 — Successful Login",
                    }
                ],
            },
        ],
    }

    result = extract_text_from_adf(adf)

    assert result == (
        "Acceptance Criteria\n"
        "AC1 — Successful Login\n"
    )