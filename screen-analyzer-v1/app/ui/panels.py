from __future__ import annotations


def format_result_payload(result: dict) -> str:
    return (
        f"Screen content: {result['screen_content']}\n"
        f"Question present: {result['question_present']}\n"
        f"Main answer: {result['main_answer']}\n"
        f"Summary: {result['summary']}\n"
        f"Readability: {result['readability']}\n"
        f"Needs web search: {result['needs_web_search']}"
    )
