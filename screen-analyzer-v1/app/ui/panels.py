from __future__ import annotations


def format_result_payload(result: dict) -> str:
    notes = ", ".join(result.get("notes", [])) if result.get("notes") else "-"
    citations = ", ".join(result.get("citations", [])) if result.get("citations") else "-"
    return (
        f"Screen content: {result['screen_content']}\n\n"
        f"Question present: {result['question_present']}\n"
        f"Main answer: {result['main_answer']}\n\n"
        f"Summary: {result['summary']}\n"
        f"Readability: {result['readability']}\n"
        f"Needs web search: {result['needs_web_search']}\n"
        f"Notes: {notes}\n"
        f"Citations: {citations}"
    )
