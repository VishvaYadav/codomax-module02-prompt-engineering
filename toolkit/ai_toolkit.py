"""
AI Productivity Toolkit — Codomax Internship, Module 02
=======================================================

Reusable, prompt-engineered workflows for everyday tasks:
    - summarize()        : summarize any text into a chosen format
    - draft_email()      : write a professional email from bullet points
    - improve_resume()   : rewrite resume bullets with impact + metrics
    - code_helper()      : explain, debug, or review a code snippet
    - research_brief()   : structured research brief on a topic

Each tool uses the same prompt anatomy:
    ROLE  ->  CONTEXT  ->  INSTRUCTION  ->  CONSTRAINTS  ->  OUTPUT FORMAT

Usage (Colab or local):
    export GEMINI_API_KEY="..."        # or Colab Secrets
    from toolkit.ai_toolkit import summarize
    print(summarize(long_text, style="bullets"))
"""

from __future__ import annotations

import json
import os
import time

from google import genai
from google.genai import types

MODEL = os.environ.get("GEMINI_MODEL", "gemini-flash-latest")  # free-tier alias


def _get_api_key() -> str | None:
    try:  # Colab Secrets (key icon in the left sidebar)
        from google.colab import userdata  # type: ignore
        return userdata.get("GEMINI_API_KEY")
    except Exception:
        return os.environ.get("GEMINI_API_KEY")


_client = None


def _client_once():
    global _client
    if _client is None:
        _client = genai.Client(api_key=_get_api_key())
    return _client


def ask(prompt: str, system: str | None = None, temperature: float = 0.7,
        json_mode: bool = False, schema=None, retries: int = 3) -> str:
    """Single entry point for every LLM call (with simple retry/back-off)."""
    cfg = {"temperature": temperature}
    if system:
        cfg["system_instruction"] = system
    if json_mode or schema is not None:
        cfg["response_mime_type"] = "application/json"
    if schema is not None:
        cfg["response_schema"] = schema
    for attempt in range(retries):
        try:
            resp = _client_once().models.generate_content(
                model=MODEL, contents=prompt,
                config=types.GenerateContentConfig(**cfg),
            )
            return resp.text
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(5 * 2 ** attempt)  # free-tier rate limits


# --------------------------------------------------------------------------- #
# Prompt templates                                                            #
# --------------------------------------------------------------------------- #

SUMMARY_STYLES = {
    "bullets": "5 concise bullet points, each under 20 words",
    "tldr": "a single TL;DR sentence under 30 words",
    "executive": "an executive summary: 1 headline, 3 key points, 1 recommended action",
}

SUMMARIZE_TMPL = """ROLE: You are an expert analyst who writes clear, faithful summaries.
CONTEXT: The reader is busy and needs the key information quickly.
INSTRUCTION: Summarize the text below as {style}.
CONSTRAINTS:
- Use only facts present in the text; do not add outside information.
- Keep numbers, names and dates exactly as written.
OUTPUT FORMAT: Plain text only.

TEXT:
\"\"\"{text}\"\"\""""

EMAIL_TMPL = """ROLE: You are a professional business communication assistant.
CONTEXT: Sender: {sender}. Recipient: {recipient}. Purpose: {purpose}.
INSTRUCTION: Write an email that covers every key point below.
KEY POINTS:
{points}
CONSTRAINTS:
- Tone: {tone}. Under {max_words} words.
- Clear subject line, short paragraphs, one explicit call-to-action.
OUTPUT FORMAT: JSON with keys "subject" and "body"."""

RESUME_TMPL = """ROLE: You are a senior technical recruiter and resume coach.
CONTEXT: Target role: {role}.
INSTRUCTION: Rewrite each resume bullet using the formula
Action verb + What you did + Tool/Skill + Measurable result.
CONSTRAINTS:
- Do not invent numbers. If a metric is missing, insert a placeholder like [X%].
- One line per bullet, under 25 words.
OUTPUT FORMAT: JSON list of objects with keys "original", "improved", "why".

BULLETS:
{bullets}"""

CODE_TMPL = """ROLE: You are a senior {language} engineer and patient mentor.
INSTRUCTION: {task_instruction}
CONSTRAINTS:
- Be specific: reference line numbers or variable names.
- Keep the fix minimal; do not rewrite unrelated code.
OUTPUT FORMAT: JSON with keys "summary", "issues" (list of strings),
"fixed_code" (string, empty if not applicable), "tests" (list of assert statements).

CODE:
```{language}
{code}
```"""

CODE_TASKS = {
    "explain": "Explain what the code does, step by step, for a beginner.",
    "debug": "Find every bug or edge case that will fail, then provide corrected code.",
    "review": "Review the code for readability, performance and best practices.",
}

RESEARCH_TMPL = """ROLE: You are a research assistant for a {audience}.
INSTRUCTION: Create a research brief on: "{topic}".
CONSTRAINTS:
- Separate well-established facts from open questions.
- Flag anything that may be outdated or needs verification.
- Do not fabricate citations; suggest what kinds of sources to check instead.
OUTPUT FORMAT: JSON with keys "overview" (string), "key_concepts" (list),
"open_questions" (list), "suggested_sources" (list), "next_steps" (list)."""


# --------------------------------------------------------------------------- #
# Tools                                                                       #
# --------------------------------------------------------------------------- #

def summarize(text: str, style: str = "bullets") -> str:
    style_desc = SUMMARY_STYLES.get(style, style)
    return ask(SUMMARIZE_TMPL.format(style=style_desc, text=text), temperature=0.2)


def draft_email(points: list[str], purpose: str, recipient: str = "the team",
                sender: str = "me", tone: str = "professional and friendly",
                max_words: int = 150) -> dict:
    prompt = EMAIL_TMPL.format(
        sender=sender, recipient=recipient, purpose=purpose, tone=tone,
        max_words=max_words, points="\n".join(f"- {p}" for p in points),
    )
    return json.loads(ask(prompt, temperature=0.5, json_mode=True))


def improve_resume(bullets: list[str], role: str = "Software Engineer Intern") -> list[dict]:
    prompt = RESUME_TMPL.format(role=role, bullets="\n".join(f"- {b}" for b in bullets))
    return json.loads(ask(prompt, temperature=0.4, json_mode=True))


def code_helper(code: str, task: str = "debug", language: str = "python") -> dict:
    prompt = CODE_TMPL.format(language=language, code=code,
                              task_instruction=CODE_TASKS.get(task, task))
    return json.loads(ask(prompt, temperature=0.1, json_mode=True))


def research_brief(topic: str, audience: str = "computer engineering student") -> dict:
    prompt = RESEARCH_TMPL.format(topic=topic, audience=audience)
    return json.loads(ask(prompt, temperature=0.3, json_mode=True))


if __name__ == "__main__":
    demo = ("Generative AI models predict the next token based on patterns learned "
            "from large datasets. They are powerful for drafting and coding, but can "
            "hallucinate facts, so outputs should be verified.")
    print(summarize(demo, style="tldr"))
