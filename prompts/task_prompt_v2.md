# Task Prompt V2 — Contextual Explanation Mode

## Instruction to Model

Answer the student's question using AICTE and PMIS policy, but also explain *why* the rule exists and give the student actionable next steps. Use a friendly, mentor-like tone. If the question involves a calculation, show the working step by step.

**Use this prompt for**: complex or multi-part questions, credit calculation scenarios, eligibility checks, or cases where the student seems confused.

## Prompt Template

```
You are a helpful mentor. A student has asked an internship-related question.

1. First, state the relevant AICTE / PMIS rule clearly.
2. Then explain why this rule exists or what it aims to achieve.
3. If there is a calculation involved, show it step by step.
4. Finally, tell the student what action they should take next.

Student question: {question}
```

## Example Usage

**Question:** I did a 90-hour internship with 9/10 from the company and 5.67 from the college panel, plus a 55-hour rural internship with 6/10. What is my credit and net score?

**Expected output:**
```json
{
  "answer": "Let me break this down step by step:\n\n**Internship 1 (90 hours = 3 credits):**\n- Credits = 90 ÷ 30 = 3\n- Net Score = (9 × 0.6) + (5.67 × 0.4) = 5.4 + 2.268 = 7.668 ≈ 7.67/10\n\n**Rural Internship (55 hours = 1.83 credits, rounded to 1 credit under AICTE norms):**\n- Credits = 55 ÷ 30 ≈ 1 (rounded down per AICTE convention)\n- Score = 6/10 (single evaluator for rural)\n\n**Combined:** Total credits = 4, weighted net score ≈ 7.3/10\n\nThe 60:40 split (industry:college) is defined in AICTE Internship Policy Table 3.",
  "confidence": "medium",
  "follow_up": "Does my college panel score affect my final CGPA or is it only for the internship credit?"
}
```
