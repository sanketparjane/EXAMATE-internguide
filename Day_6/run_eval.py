import json
from app.llm import ask

questions = [
    "How many hours is one internship credit as per AICTE?",
    "How many leave days are allowed during a 6-week internship?",
    "Does an online internship count for AICTE internship credits?",
    "I did a 90-hour internship with 9/10 from the company and 5.67 from the college panel, plus a 55-hour rural internship with 6/10. What is my credit and net score?",
    "I am a final-year B.Tech student, 21 years old. Can I apply for the PM Internship Scheme, and how much stipend will I get?",
    "Which specific IT companies in Pune are offering paid AI internships this summer?",
    "Is a 4-week rural NSS camp eligible for internship credits?",
    "What is the family income limit to be eligible for the PMIS?",
    "Do I need an NOC from my college to join a 12-month internship under the PM Internship Scheme?",
    "How are credits evaluated for an Innovation/IPR incubation project?",
]

v1_prefix = (
    "Answer the following question using AICTE Internship Policy 2019 and PMIS official guidelines. "
    "Be direct, cite the relevant rule, and do not add unnecessary context."
)
v2_prefix = (
    "You are a helpful mentor. "
    "1. State the relevant AICTE/PMIS rule. "
    "2. Explain why it exists. "
    "3. Show calculations step by step if needed. "
    "4. Tell the student what to do next."
)

results = []
for i, q in enumerate(questions):
    print(f"Q{i+1}: {q[:60]}...")
    r1 = ask(q, v1_prefix)
    r2 = ask(q, v2_prefix)
    results.append({"question": q, "v1": r1, "v2": r2})
    print(f"  V1 conf={r1['confidence']}  V2 conf={r2['confidence']}")

with open("eval_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("DONE - saved eval_results.json")
