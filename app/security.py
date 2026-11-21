# app/security.py
"""
Input validation, size limit enforcement, and prompt-injection defense for InternGuide.
"""

import re
from typing import Tuple

MAX_QUERY_LENGTH = 1000

# Patterns indicative of prompt injection, jailbreaking, or system override attempts
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|prompts|rules)",
    r"system\s*override",
    r"you\s+are\s+now\s+(in\s+)?(dan\s+mode|jailbreak|unfiltered)",
    r"disregard\s+(all\s+)?(safety|rules|instructions)",
    r"reveal\s+(the\s+)?(system\s+prompt|internal\s+instructions|secret|api\s*key|password)",
    r"output\s+the\s+full\s+prompt",
    r"give\s+me\s+admin\s+access",
    r"bypass\s+(all\s+)?guidelines"
]


def validate_input_length(query: str) -> Tuple[bool, str]:
    """
    Validates input query against length and content constraints.
    Returns (is_valid, error_message).
    """
    if not query or not query.strip():
        return False, "Query cannot be empty."

    if len(query) > MAX_QUERY_LENGTH:
        return False, f"Query length ({len(query)} chars) exceeds maximum allowed limit of {MAX_QUERY_LENGTH} characters."

    return True, ""


def is_prompt_injection(query: str) -> bool:
    """
    Detects known prompt-injection and jailbreak vectors.
    """
    q_lower = query.lower()
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, q_lower):
            return True
    return False


INJECTION_REFUSAL_MESSAGE = (
    "I don't know based on the provided information. "
    "Security Notice: Prompt injection or system override attempt detected and rejected."
)
