# Prompt Comparison: V1 vs V2 on 10 InternGuide Questions

**Date:** 13 Nov 2026  
**Model:** gemini-3.8-flash (via `app/llm.py`)  
**System prompt:** `prompts/system_prompt.md`

---

## Prompt Versions

| | Prompt | Style |
|---|---|---|
| **V1** | `prompts/task_prompt_v1.md` | Direct answer mode — concise, rule-first, cite policy |
| **V2** | `prompts/task_prompt_v2.md` | Mentor mode — explain the rule, show calculations, give next steps |

---

## Results on 10 Test Questions

---

### Q1. How many hours is one internship credit as per AICTE?

**V1 (Direct)**
- **Answer:** As per AICTE Internship Policy 2019 (Table 2), 1 credit = 30 hours of internship work. A 2-credit internship requires 60 hours; a 4-credit one requires 120 hours.
- **Confidence:** high
- **Follow-up:** What is the minimum credit requirement for a B.Tech final-year internship?

**V2 (Mentor)**
- **Answer:** AICTE defines 1 credit = 30 hours because this aligns the internship duration with the academic credit framework used for theory courses (where 1 credit ≈ 15 lecture hours + 15 self-study hours). For a student aiming for 4 credits, that means planning a 120-hour (≈3 week full-time) engagement. Next step: Check your college's internship schedule to block the right weeks before the semester ends.
- **Confidence:** high
- **Follow-up:** Can I split the 120 hours across two different companies to earn 4 credits?

> **Winner:** V2 adds useful context. V1 is faster for quick policy lookups.

---

### Q2. How many leave days are allowed during a 6-week internship?

**V1 (Direct)**
- **Answer:** AICTE Internship Policy 2019 does not explicitly define a fixed number of leave days. It requires the student to complete the minimum required hours (30 per credit). Leave taken reduces effective hours; excess absence may require the internship to be extended.
- **Confidence:** medium
- **Follow-up:** What happens if I miss more than 10% of internship days — does it affect my credit?

**V2 (Mentor)**
- **Answer:** The AICTE policy does not set a fixed leave quota; it focuses on total hours completed. For a 6-week internship targeting 4 credits (120 hours), that is roughly 4 hours/day × 5 days × 6 weeks. If you take, say, 3 days of leave (12 hours), you must make up those hours elsewhere in the period. Rule of thumb: keep leave under 10% of total days to avoid issues with the industry mentor's attendance certificate. Next step: Confirm the leave policy with your company mentor on Day 1.
- **Confidence:** medium
- **Follow-up:** Will leave days affect the company mentor's evaluation score?

> **Winner:** V2 — gives actionable guidance on an ambiguous policy.

---

### Q3. Does an online internship count for AICTE internship credits?

**V1 (Direct)**
- **Answer:** Yes. AICTE Internship Policy 2019 recognises online/remote internships as eligible, provided the student completes the required hours and obtains a valid completion certificate from the company. The same 1 credit = 30 hours rule applies.
- **Confidence:** high
- **Follow-up:** What documents do I need from an online internship to get it recognised by my college?

**V2 (Mentor)**
- **Answer:** Yes — AICTE explicitly includes online internships. The policy was updated post-COVID to ensure students doing remote work are not disadvantaged. You need: (1) a company completion certificate on letterhead stating hours completed, (2) a daily log or work report, and (3) a mentor evaluation form with a score out of 10. Without these, your college panel may not accept it even if you completed the hours. Next step: Ask your company HR for a certificate before your last working day.
- **Confidence:** high
- **Follow-up:** Can I do an online internship with a foreign company and still get AICTE credits?

> **Winner:** V2 — surfaces the documentation risk that students commonly miss.

---

### Q4. I did a 90-hour internship (9/10 company, 5.67/10 panel) + 55-hour rural (6/10). What is my credit and net score?

**V1 (Direct)**
- **Answer:** Internship 1: 90 hours = 3 credits. Net score = (9 × 0.6) + (5.67 × 0.4) = 5.4 + 2.268 = **7.67/10**. Rural: 55 hours = 1 credit (rounded down). Score = 6/10 (single evaluator). Total: **4 credits**, combined weighted score ≈ **7.25/10**.
- **Confidence:** medium
- **Follow-up:** Does the rural internship score get weighted the same way as the industry one?

**V2 (Mentor)**
- **Answer:** Let me work through this step by step.\n\n**Internship 1 (Industry, 90 hours):**\n- Credits = 90 ÷ 30 = **3 credits**\n- AICTE uses a 60:40 split: 60% from industry mentor, 40% from college panel\n- Net score = (9 × 0.6) + (5.67 × 0.4) = 5.40 + 2.27 = **7.67/10**\n\n**Rural Internship (55 hours):**\n- Credits = 55 ÷ 30 = 1.83 → rounded to **1 credit** (AICTE rounds down)\n- Rural internships have a single evaluator (no 60:40 split): Score = **6/10**\n\n**Combined:**\n- Total credits = **4**\n- Weighted net score = (7.67 × 3 + 6 × 1) ÷ 4 = (23.01 + 6) ÷ 4 = **7.25/10**\n\nNext step: Get both completion certificates and submit the score sheet to your HOD before the exam form deadline.
- **Confidence:** medium
- **Follow-up:** Does my CGPA improve if I score above 8 in the internship?

> **Winner:** V2 — step-by-step calculation is exactly what a confused student needs.

---

### Q5. I am a final-year B.Tech student, 21 years old. Can I apply for PMIS and how much stipend?

**V1 (Direct)**
- **Answer:** Yes, you are eligible if: (1) age 21–24 ✅, (2) family income ≤ ₹8 lakh/year, (3) you are not a full-time enrolled student — but final-year students can apply with an NOC from their institute. Stipend: ₹5,000/month from the company + ₹6,000 one-time incidentals grant from the government via DBT.
- **Confidence:** high
- **Follow-up:** How do I get an NOC from my college for the PMIS?

**V2 (Mentor)**
- **Answer:** Good news — at 21, you meet the age criterion (21–24). Here is the full eligibility check:\n1. ✅ Age: 21 (eligible)\n2. ❓ Family income: Must be ≤ ₹8 lakh/year — check your family's ITR\n3. ⚠️ Full-time student rule: Final-year students CAN apply, but need an NOC from their institute\n\nIf all three are met, you get:\n- ₹5,000/month stipend paid by the company for up to 12 months\n- ₹6,000 one-time incidentals grant from the Government via DBT on joining\n\nNext step: Visit pminternship.mca.gov.in, register, and collect your NOC from your college office before applying.
- **Confidence:** high
- **Follow-up:** If I get placed before completing the 12-month PMIS internship, can I leave early?

> **Winner:** V2 — the checklist format prevents students from missing the income or NOC requirement.

---

### Q6. Which IT companies in Pune are offering paid AI internships this summer?

**V1 (Direct)**
- **Answer:** InternGuide cannot answer this question. Its knowledge base covers only AICTE internship rules and PMIS eligibility criteria. For company-specific listings, check LinkedIn Jobs, Internshala, or the PMIS portal at pminternship.mca.gov.in.
- **Confidence:** high (confident this is out of scope)
- **Follow-up:** Do AI/ML internships qualify for AICTE internship credits?

**V2 (Mentor)**
- **Answer:** This is outside InternGuide's scope — we cover policy rules, not live job listings. However, here is what I *can* tell you: (1) Any paid AI internship at a registered company qualifies for AICTE credits if it meets the hours requirement. (2) For PMIS specifically, participating companies list openings on the official portal. For current openings in Pune, check: Internshala, LinkedIn, PMIS portal, and your college's Training & Placement cell. Next step: Ask your T&P officer — they often have direct company contacts.
- **Confidence:** high (scope boundary)
- **Follow-up:** If an AI internship is at a startup, does it still count for AICTE credits?

> **Winner:** Tie — both correctly refuse but V2 adds a helpful redirect.

---

### Q7. Is a 4-week rural NSS camp eligible for internship credits?

**V1 (Direct)**
- **Answer:** Yes. AICTE Internship Policy 2019 includes rural/community service internships (Table 2: "Social Internship / NSS / NCC activities") as an eligible category. A 4-week (≈120 hours) rural NSS camp = 4 credits, evaluated by the NSS programme officer.
- **Confidence:** high
- **Follow-up:** Do I need a separate evaluation form from the NSS officer or can I use a standard AICTE form?

**V2 (Mentor)**
- **Answer:** Yes! NSS rural camps are explicitly listed in AICTE Table 2 as eligible internship activities. Here is how the credits work:\n- 4 weeks × 30 hours/week = 120 hours = **4 credits** (maximum for this category is typically 4)\n- Evaluator: NSS Programme Officer (single evaluator, no 60:40 split)\n- Document needed: NSS camp completion certificate from your District NSS Officer\n\nOne important note: some colleges cap the NSS credit at 2 credits even if you completed more hours. Check with your HOD. Next step: Get the camp completion certificate and the NSS officer's evaluation form before the semester ends.
- **Confidence:** high
- **Follow-up:** Can I combine NSS camp credits with an industry internship to reach the total required credits?

> **Winner:** V2 — the college cap caveat is a critical real-world detail.

---

### Q8. What is the family income limit to be eligible for the PMIS?

**V1 (Direct)**
- **Answer:** As per the PM Internship Scheme guidelines, the family income limit is **≤ ₹8,00,000 per annum** (₹8 lakh/year). Proof required: latest ITR or Form 16 of the family's earning members.
- **Confidence:** high
- **Follow-up:** If my father is a government employee, how is family income calculated for PMIS?

**V2 (Mentor)**
- **Answer:** The income cap is ₹8 lakh per annum for the entire family (not just one member). The government set this limit to target economically disadvantaged youth who face barriers in getting quality corporate exposure. What counts as "family income":\n- Income of parents/guardians\n- Any siblings' income if they live in the same household (check the official form)\n- Proof: Latest ITR, Form 16, or a certificate from a gazetted officer if the family is below IT filing threshold\n\nNext step: Gather the most recent ITR before you register on the portal — you will need to upload it.
- **Confidence:** high
- **Follow-up:** If my family income is exactly ₹8 lakh, am I eligible or is the limit strictly below ₹8 lakh?

> **Winner:** V2 — the documentation checklist prevents application rejections.

---

### Q9. Do I need an NOC from my college for a 12-month PMIS internship?

**V1 (Direct)**
- **Answer:** Yes. AICTE/PMIS rules require an NOC (No Objection Certificate) from your institute if you are a final-year student or enrolled in an ODL (Open/Distance Learning) programme. The NOC confirms the college has no objection to the student undertaking the internship alongside studies.
- **Confidence:** high
- **Follow-up:** What information does the NOC for PMIS need to include?

**V2 (Mentor)**
- **Answer:** Yes — the NOC is mandatory for two categories of students under PMIS:\n1. **Final-year students** (like you, if applicable) who are still enrolled\n2. **ODL/part-time students** pursuing degrees alongside work\n\nWhy is it needed? PMIS is designed for youth who have completed or nearly completed education. The NOC prevents a conflict where a student is both attending full-time college and a 12-month internship simultaneously. The NOC should be on college letterhead, signed by the Principal/HOD, and state that the college has no objection to you joining the PMIS internship.\n\nNext step: Visit your college office, explain you are applying for PMIS, and request the NOC 2–3 weeks before your expected joining date.
- **Confidence:** high
- **Follow-up:** If my college refuses to give the NOC, can I still apply for PMIS?

> **Winner:** V2 — explains *why* the NOC is needed, reducing student confusion.

---

### Q10. How are credits evaluated for an Innovation/IPR incubation project?

**V1 (Direct)**
- **Answer:** As per AICTE Internship Policy 2019 (Table 2, Category: Innovation/IPR/Entrepreneurship), an Innovation/IPR incubation project is worth **4–6 credits** for a 4–6 week engagement. Evaluator: Faculty Mentor + Cell In-Charge (Incubation Cell). Evidence: IPR filing receipt, prototype, or incubation certificate.
- **Confidence:** high
- **Follow-up:** Can a patent filing alone count as a full internship credit, or do I need the minimum hours too?

**V2 (Mentor)**
- **Answer:** Innovation/IPR projects are one of the highest-value internship categories under AICTE. Here is how it works:\n\n**Credits:** 4–6 credits for 4–6 weeks (120–180 hours)\n**Evaluators:** Two evaluators apply the 60:40 rule:\n- 60%: Faculty Mentor (guides your innovation work)\n- 40%: Cell In-Charge (Incubation/IIC Cell at your college)\n\n**What counts as evidence:**\n- Filed patent application (IPO receipt)\n- Working prototype with documentation\n- Incubation acceptance letter from a recognised incubator\n- Published paper or design registration\n\n**Why so many credits?** AICTE incentivises innovation because it aligns with the National Innovation and Startup Policy. If you file a patent, your college can also count it towards their NIRF innovation ranking.\n\nNext step: Register your project with your college's IIC (Institution's Innovation Council) first — this gives it official recognition and simplifies the evaluation paperwork.
- **Confidence:** high
- **Follow-up:** If I file a provisional patent, does it count the same as a full patent for AICTE credit purposes?

> **Winner:** V2 — the IIC registration tip is actionable and not obvious from the policy text.

---

## Summary Comparison

| # | Question | V1 Confidence | V2 Confidence | Better Prompt |
|---|---|---|---|---|
| 1 | Hours per credit | high | high | V2 (more context) |
| 2 | Leave days | medium | medium | V2 (actionable) |
| 3 | Online internship | high | high | V2 (doc risk) |
| 4 | Credit & score calc | medium | medium | V2 (step-by-step) |
| 5 | PMIS eligibility | high | high | V2 (checklist) |
| 6 | Out-of-scope query | high | high | Tie |
| 7 | NSS camp credits | high | high | V2 (college cap caveat) |
| 8 | PMIS income limit | high | high | V2 (doc list) |
| 9 | NOC for PMIS | high | high | V2 (explains why) |
| 10 | Innovation/IPR eval | high | high | V2 (IIC tip) |

### Key Finding

**V1 (Direct mode)** is best for: quick lookups, automated API calls where brevity matters, and cases where the rule is clear-cut.

**V2 (Mentor mode)** is better for: students who need to understand *why* a rule exists, multi-part calculation questions, and edge cases where missing a detail (like an NOC or a college cap) could fail the student.

**Recommendation:** Use V2 as the default system behaviour for the `/chat` endpoint, since InternGuide's target users are confused students — not policy experts.
