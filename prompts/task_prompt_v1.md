# Task Prompt V1 — Direct Answer Mode

## Instruction to Model

Answer the student's question directly and factually using AICTE and PMIS policy rules. Be concise but complete. Cite the specific rule or section.

**Use this prompt for**: straightforward policy queries where the student needs a quick, accurate rule-based answer.

## Prompt Template

```
Answer the following question using AICTE Internship Policy 2019 and PMIS official guidelines.
Be direct, cite the relevant rule, and do not add unnecessary context.

Student question: {question}
```

## Example Usage

**Question:** How many hours is one internship credit as per AICTE?

**Expected output:**
```json
{
  "answer": "As per AICTE Internship Policy 2019, 1 credit = 30 hours of internship work. So for a 2-credit internship, a student must complete 60 hours.",
  "confidence": "high",
  "follow_up": "What is the minimum credit requirement for a B.Tech degree internship under AICTE?"
}
```
