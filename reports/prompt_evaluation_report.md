# Prompt Evaluation Report: Support-Ticket Classification
*Model:* `gemini-flash-lite-latest` · *Test cases:* 10 · *Generated:* 2026-11-18 13:16

## Prompt versions tested
### `v1_zero_shot_vague`
```
What kind of customer message is this?

{text}
```

### `v2_zero_shot_constrained`
```
Classify the customer message into exactly one category: Billing, Technical, Account, Feedback.
Reply with the category name only.

Message: {text}
```

### `v3_role_few_shot_json`
```
Classify the customer message.

Categories:
- Billing: payments, refunds, invoices, charges
- Technical: bugs, errors, crashes, things not working
- Account: login, password, profile, personal details
- Feedback: praise, complaints about experience, feature requests

Examples:
"Refund not received yet" -> {{"category": "Billing", "confidence": 0.95}}
"App freezes on startup" -> {{"category": "Technical", "confidence": 0.9}}
"Update my phone number" -> {{"category": "Account", "confidence": 0.9}}

Message: "{text}"
Return JSON: {{"category": <one category>, "confidence": <0-1>}}
```

## Results
| prompt                   |   accuracy |   format_compliance |   avg_latency_s |
|:-------------------------|-----------:|--------------------:|----------------:|
| v1_zero_shot_vague       |        0.8 |                   0 |            5.75 |
| v2_zero_shot_constrained |        0.9 |                   1 |            5.71 |
| v3_role_few_shot_json    |        1   |                   1 |            3.87 |

**Best prompt:** `v3_role_few_shot_json`

## Failures
| prompt                   | input                                                         | expected   | predicted   | raw_output                                                                                                          |
|:-------------------------|:--------------------------------------------------------------|:-----------|:------------|:--------------------------------------------------------------------------------------------------------------------|
| v1_zero_shot_vague       | I was charged twice this month, please refund.                | Billing    | Billing     | This is a **Billing / Payment Dispute** customer message, specifically categorized as a **Refund Request**.         |
|                          |                                                               |            |             |                                                                                                                     |
|                          |                                                               |            |             | Here is a                                                                                                           |
| v1_zero_shot_vague       | My invoice shows the wrong GST number.                        | Billing    | Billing     | This is a **billing / invoice correction** request (specifically related to tax/compliance information).            |
|                          |                                                               |            |             |                                                                                                                     |
|                          |                                                               |            |             | Here is a bre                                                                                                       |
| v1_zero_shot_vague       | The page keeps showing a 500 error when I submit my notebook. | Technical  | Technical   | This is a **Technical Support Request** (specifically, a **bug report** or **error report**).                       |
|                          |                                                               |            |             |                                                                                                                     |
|                          |                                                               |            |             | Here is a breakdown of w                                                                                            |
| v1_zero_shot_vague       | Colab link upload button does nothing on Safari.              | Technical  | Technical   | This is a **bug report** (specifically, a technical issue/defect report).                                           |
|                          |                                                               |            |             |                                                                                                                     |
|                          |                                                               |            |             | Here is a quick breakdown of why:                                                                                   |
|                          |                                                               |            |             | * **The Pr                                                                                                          |
| v1_zero_shot_vague       | I forgot my password and the reset email never arrives.       | Account    | Technical   | This is a **Technical Support** request (specifically, an **account access** or **login issue** ticket).            |
|                          |                                                               |            |             |                                                                                                                     |
|                          |                                                               |            |             | Here is a qui                                                                                                       |
| v1_zero_shot_vague       | How do I change the email address on my profile?              | Account    | Account     | This is a **How-To / Instructional Support Request**.                                                               |
|                          |                                                               |            |             |                                                                                                                     |
|                          |                                                               |            |             | Specifically, it is:                                                                                                |
|                          |                                                               |            |             | * **Intent:** Informational / Navigational                                                                          |
| v1_zero_shot_vague       | Loved the workshop on prompt engineering, very helpful!       | Feedback   | Feedback    | This customer message is a **positive feedback** or a **compliment**.                                               |
|                          |                                                               |            |             |                                                                                                                     |
|                          |                                                               |            |             | Specifically, it falls into these categories:                                                                       |
|                          |                                                               |            |             | *                                                                                                                   |
| v1_zero_shot_vague       | It would be nice to have a dark mode on the dashboard.        | Feedback   |             | This customer message is a **Feature Request** (or **Enhancement Request**).                                        |
|                          |                                                               |            |             |                                                                                                                     |
|                          |                                                               |            |             | Specifically, it is:                                                                                                |
|                          |                                                               |            |             | * **Proactive:** The                                                                                                |
| v1_zero_shot_vague       | Payment failed but money was debited from my bank.            | Billing    | Billing     | This is a **Billing / Payment Dispute** or **Transaction Error** customer message.                                  |
|                          |                                                               |            |             |                                                                                                                     |
|                          |                                                               |            |             | Specifically, it is a **"charged bu                                                                                 |
| v1_zero_shot_vague       | I can't log in after changing my phone number.                | Account    | Account     | This customer message can be classified in a few ways depending on your categorization system, but it is primarily: |
|                          |                                                               |            |             |                                                                                                                     |
|                          |                                                               |            |             | *                                                                                                                   |
| v2_zero_shot_constrained | I can't log in after changing my phone number.                | Account    | Technical   | Technical                                                                                                           |

## Observations
- **v1 (vague)**: the model answers in free text, so it is hard to parse and its format compliance is low.
- **v2 (constrained)**: listing the allowed labels and saying 'category only' fixes most format issues.
- **v3 (role + definitions + few-shot + JSON)**: category definitions settle ambiguous cases (e.g. login vs bug), and JSON output can be parsed reliably.

## Conclusion
Explicit constraints and output formats matter more than clever wording. Few-shot examples and category definitions improve consistency on edge cases. Always evaluate prompts on a fixed test set before using them in an application.