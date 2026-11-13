# app/llm.py
"""
LLM provider wrapper for InternGuide.
Supports Gemini via google-genai SDK.
Loads API key from .env using python-dotenv.
"""

import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types

# Load .env from project root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# --- Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model fallback chain: try each in order until one works
MODEL_FALLBACK_CHAIN = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
]

SYSTEM_PROMPT = """You are InternGuide, an expert assistant that helps engineering students in India understand:
- AICTE internship policies: credit calculation (1 credit = 30 hours), evaluation (60% industry, 40% college panel), eligible activity types
- PM Internship Scheme (PMIS): eligibility (age 21-24, family income <= 8 lakh, not full-time student), stipend Rs 5000/month + Rs 6000 one-time grant
- UGC internship guidelines: credit frameworks, evidence documentation requirements
- Types of internships: industry, rural, NSS, online, innovation/IPR projects

Always answer based on AICTE rules, UGC guidelines, and PMIS official policies.
If a question is completely outside these topics, say InternGuide cannot answer it.

When answering:
1. Give a clear, direct answer to the student's question
2. Cite the relevant rule or policy if possible
3. Provide a confidence level: high (rule directly stated), medium (inference), or low (edge case)
4. Suggest a helpful follow-up question the student might ask next
"""


def get_client() -> genai.Client:
    """Create and return a configured Gemini client."""
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is not set. "
            "Copy .env.example to .env and add your key."
        )
    return genai.Client(api_key=GEMINI_API_KEY)


def ask(question: str, task_prompt: str | None = None) -> dict:
    """
    Send a question to Gemini and return structured InternGuide response.

    Args:
        question: The student's question
        task_prompt: Optional extra instruction to prepend before the question

    Returns:
        dict with keys: answer, confidence, follow_up
    """
    client = get_client()

    # Build prompt
    user_content = question
    if task_prompt:
        user_content = f"{task_prompt}\n\nStudent question: {question}"

    # Ask Gemini to reply in structured JSON
    structured_instruction = (
        "\n\nRespond ONLY with a valid JSON object (no markdown, no code fences) "
        "with exactly these three keys:\n"
        '  "answer": <your detailed answer as a string>,\n'
        '  "confidence": <"high", "medium", or "low">,\n'
        '  "follow_up": <one useful follow-up question as a string>'
    )

    full_prompt = user_content + structured_instruction

    # Try each model in fallback chain
    last_error = None
    for model_name in MODEL_FALLBACK_CHAIN:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.3,
                        max_output_tokens=1024,
                    ),
                )

                raw = response.text.strip()

                # Strip markdown code fences if the model adds them
                if raw.startswith("```"):
                    raw = raw.split("```")[1]
                    if raw.startswith("json"):
                        raw = raw[4:]
                    raw = raw.strip()

                result = json.loads(raw)
                return {
                    "answer": str(result.get("answer", raw)),
                    "confidence": str(result.get("confidence", "medium")),
                    "follow_up": str(result.get("follow_up", "")),
                    "model_used": model_name,
                }

            except Exception as e:
                last_error = e
                err_str = str(e)
                if "503" in err_str or "UNAVAILABLE" in err_str:
                    # Transient overload — wait and retry
                    time.sleep(5 * (attempt + 1))
                    continue
                elif "404" in err_str or "NOT_FOUND" in err_str:
                    # Model not available for this key — try next model
                    break
                else:
                    # JSON parse error or other — return fallback
                    return {
                        "answer": err_str,
                        "confidence": "low",
                        "follow_up": "Could you clarify your question?",
                        "model_used": model_name,
                    }

    # All models failed
    return {
        "answer": f"InternGuide AI is temporarily unavailable. Error: {last_error}",
        "confidence": "low",
        "follow_up": "Please try again in a few minutes.",
        "model_used": "none",
    }
