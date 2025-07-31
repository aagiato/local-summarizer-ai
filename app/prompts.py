def build_structured_prompt(text_chunk: str) -> str:
    return f"""
\n\nHuman:
You are an expert technical summarizer.

Summarize the following document segment in a structured format with the following three sections:

1. Introduction: Brief overview of what this section is about.
2. Key Points: A concise list of 3–5 main ideas or insights, formatted as bullet points.
3. Conclusion: A short wrap-up or implication of this section.

Keep each section concise and professional. Avoid repetition.
Begin your response with the phrase: "Structured Summary:"

---
Input Text:
{text_chunk}

\n\nAssistant:
"""
