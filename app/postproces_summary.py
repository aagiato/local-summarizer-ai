import re

def postprocess_summary(text: str) -> dict:
    """
    Extracts structured sections from a Claude-generated summary:
    - Introduction
    - Key Points (as a list of bullet points)
    - Conclusion

    Uses regex to match flexible formats like:
    1. Introduction:
    2. Key Points:
    3. Conclusion:

    Falls back gracefully if sections are mislabeled or out of order.
    """

    # Extract sections using numbered or unnumbered headings
    intro_pattern = re.compile(
        r"(?:1\.\s*)?Introduction:?\s*(.*?)(?=\n\s*2\.|Key Points:|Conclusion:|$)",
        re.DOTALL | re.IGNORECASE
    )
    keypoints_pattern = re.compile(
        r"(?:2\.\s*)?Key Points:?\s*(.*?)(?=\n\s*3\.|Conclusion:|$)",
        re.DOTALL | re.IGNORECASE
    )
    conclusion_pattern = re.compile(
        r"(?:3\.\s*)?Conclusion:?\s*(.*)",
        re.DOTALL | re.IGNORECASE
    )

    intro_match = intro_pattern.search(text)
    keypoints_match = keypoints_pattern.search(text)
    conclusion_match = conclusion_pattern.search(text)

    intro = intro_match.group(1).strip() if intro_match else ""
    keypoints_raw = keypoints_match.group(1).strip() if keypoints_match else ""
    conclusion = conclusion_match.group(1).strip() if conclusion_match else ""

    # Normalize and extract bullet points
    key_points = []
    for line in keypoints_raw.splitlines():
        bullet = line.strip()
        if bullet.startswith("-") or bullet.startswith("*"):
            key_points.append(bullet[1:].strip())
        elif bullet:
            key_points.append(bullet)

    return {
        "introduction": intro,
        "key_points": key_points,
        "conclusion": conclusion
    }
