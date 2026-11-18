# Prompt Library: Module 02

Reusable prompt patterns used in this project. Placeholders are in `{curly_braces}`.

## 1. The universal template (RCICO)

```
ROLE: You are a {expert role}.
CONTEXT: {who the audience is, background, why this matters}
INSTRUCTION: {the single, specific task}
CONSTRAINTS:
- {length limit}
- {what to include / avoid}
- {tone}
OUTPUT FORMAT: {plain text | numbered list | JSON with keys ...}
```

## 2. Zero-shot

```
Classify the sentiment of this review as Positive, Negative, or Mixed.
Review: {review}
Sentiment:
```

## 3. Few-shot

```
Classify the sentiment of each review as Positive, Negative, or Mixed. Answer with one word only.

Review: Absolutely love it, works perfectly!
Sentiment: Positive

Review: Broke after two days, waste of money.
Sentiment: Negative

Review: Great screen, but the battery dies by noon.
Sentiment: Mixed

Review: {review}
Sentiment:
```

## 4. Structured JSON output

```
{task description}
Return JSON only, matching this schema:
{"field_1": string, "field_2": [string], "score": number between 0 and 1}
```
Tip: also set `response_mime_type="application/json"` (or pass a Pydantic `response_schema`) and validate in code.

## 5. Classification with definitions + examples

```
Classify the message.

Categories:
- {Label A}: {definition}
- {Label B}: {definition}

Examples:
"{example 1}" -> {"category": "{Label A}"}
"{example 2}" -> {"category": "{Label B}"}

Message: "{text}"
Return JSON: {"category": <one category>, "confidence": <0-1>}
```

## 6. Debugging

```
ROLE: You are a senior {language} engineer and code reviewer.
INSTRUCTION: Find every bug and unhandled edge case, then fix it.
CONSTRAINTS: Keep function names and signatures the same. {expected edge-case behaviour}
OUTPUT FORMAT: JSON with keys "bugs" (list), "fixed_code" (string), "tests" (list of asserts).

CODE:
{code}
```

## 7. Grounded summarization (reduces hallucination)

```
Summarize the text below as {style}.
- Use only facts present in the text; do not add outside information.
- Keep numbers, names and dates exactly as written.

TEXT:
"""{text}"""
```

## Best practices checklist
- [ ] One clear task per prompt
- [ ] Audience and context stated
- [ ] Length and format constraints given
- [ ] Examples for ambiguous decisions
- [ ] Delimiters (`"""`, code fences) around input data
- [ ] Low temperature for factual or structured tasks
- [ ] Output validated in code; tested on a fixed test set
