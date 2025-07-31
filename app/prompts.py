def get_summary_prompt(chunk):
    return (
        "You are an analyst at a venture debt or venture capital firm. "
        "Summarize the following document chunk in a factual and concise way. "
        "Include important dates, discoveries, IP, operational processes, and key product information. "
        "Act without making assumptions.\n\n"
        f"{chunk}\n\nSummary:"
    )

def get_label_prompt(chunk):
    return (
        "You are an analyst categorizing business documents. "
        "Provide a short (max 10-word) factual label for the following document chunk. "
        "Examples: 'Oracle Corporation 10-K 2025', 'Amazon Q1 Press Release', 'Google Earnings Call Notes'. "
        "Avoid speculation. Just return the label text, don't say something like 'Here is a factual and concise summary of the', no commentary.\n\n"
        f"{chunk}\n\nLabel:"
    )
