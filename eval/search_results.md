# Semantic Search Evaluation Results

**Date:** 14 Nov 2026  
**Vectorstore:** Persistent ChromaDB (`data/chroma`)  
**Embedding Model:** all-MiniLM-L6-v2 (Chroma default ONNX)  
**Indexed Chunks:** 346 chunks across AICTE Policy, UGC Guidelines, and Curated Records  

---

## Summary Overview

| # | Question | Top Source | Page | Score | Ground Truth Status |
|---|---|---|---|---|---|
| 1 | How many hours is one internship credit as pe... | `internship_doc_1.pdf` | 7 | 0.7447 | Direct Hit |
| 2 | How many leave days are allowed during a 6-we... | `internship_doc_1.pdf` | 7 | 0.5221 | Relevant Context Found |
| 3 | Does an online internship count for AICTE int... | `internship_doc_1.pdf` | 7 | 0.6357 | Relevant Context Found |
| 4 | I did a 90-hour internship with 9/10 from the... | `internship_doc_1.pdf` | 35 | 0.593 | Relevant Context Found |
| 5 | I am a final-year B.Tech student, 21 years ol... | `internship_doc_2.pdf` | 1 | 0.5357 | Relevant Context Found |
| 6 | Which specific IT companies in Pune are offer... | `internship_doc_1.pdf` | 11 | 0.5897 | Correct Out-of-Scope (Low relevance to policy chunks) |
| 7 | Is a 4-week rural NSS camp eligible for inter... | `data/records.json` | 1 | 0.6473 | Relevant Context Found |
| 8 | What is the family income limit to be eligibl... | `data/records.json` | 1 | 0.5772 | Relevant Context Found |
| 9 | Do I need an NOC from my college to join a 12... | `data/records.json` | 1 | 0.5453 | Relevant Context Found |
| 10 | How are credits evaluated for an Innovation/I... | `data/records.json` | 1 | 0.6358 | Relevant Context Found |

---

## Detailed Search Hits by Question

### Q1. How many hours is one internship credit as per AICTE?

**Evaluation Status:** Direct Hit  

**Top Semantic Hits:**

1. **`internship_doc_1.pdf` (Page 7)** - *AICTE Internship Policy: Guidelines & Procedures (2019)*
   - **Similarity Score:** `0.7447` (Distance: `0.3429`)
   - **Snippet:** "6  CHAPTER - 2  AICTE GUIDELINES FOR ORGANIZING INTERNSHIP  2.1 INTERNSHIP DURATION AND ACADEMIC CREDENTIALS  The following framework is proposed to give academic credit for the internship undergone as part of the  programme.  • A minimum of 14-20 credits of Internship / Entrepre..."

2. **`data/records.json` (Page 1)** - *InternGuide Rule: Internship*
   - **Similarity Score:** `0.7257` (Distance: `0.3779`)
   - **Snippet:** "Activity Head: Internship Sub-Activity: Internship with Industry/Govt. / NGO/PSU/Any Micro/Small/ Medium enterprise/ Online Internship Suggested Credits: 4-6 credits Suggested Duration: 4-6 weeks (30 hours per credit per AICTE) Required Evidence: Evaluating Report Evaluated By: F..."

3. **`internship_doc_2.pdf` (Page 9)** - *UGC Guidelines for Internship/Research Internship for UG Students*
   - **Similarity Score:** `0.6958` (Distance: `0.4372`)
   - **Snippet:** "e  students enrolled in UG degree programmes.  For an internship, one credit of Internship means two-hour engagement per week.  Accordingly, in a semester of 15 weeks’ duration, one credit in this course is equivalent  to 30 hours of engagement in a semester.  B. Research Project..."

---

### Q2. How many leave days are allowed during a 6-week internship?

**Evaluation Status:** Relevant Context Found  

**Top Semantic Hits:**

1. **`internship_doc_1.pdf` (Page 7)** - *AICTE Internship Policy: Guidelines & Procedures (2019)*
   - **Similarity Score:** `0.5221` (Distance: `0.9155`)
   - **Snippet:** "nt to minimum 45 hours of work. Therefore, a full-time intern is expected to  spend 45 hours per week on Internship, Training, Project work, Seminar activities etc. This will result  in about minimum of 630 hours (i.e. 14 Credits) of total internship duration for B. Tech and mini..."

2. **`internship_doc_1.pdf` (Page 7)** - *AICTE Internship Policy: Guidelines & Procedures (2019)*
   - **Similarity Score:** `0.5095` (Distance: `0.9627`)
   - **Snippet:** "6  CHAPTER - 2  AICTE GUIDELINES FOR ORGANIZING INTERNSHIP  2.1 INTERNSHIP DURATION AND ACADEMIC CREDENTIALS  The following framework is proposed to give academic credit for the internship undergone as part of the  programme.  • A minimum of 14-20 credits of Internship / Entrepre..."

3. **`internship_doc_2.pdf` (Page 9)** - *UGC Guidelines for Internship/Research Internship for UG Students*
   - **Similarity Score:** `0.5022` (Distance: `0.9912`)
   - **Snippet:** "5.0 ACADEMIC CREDENTIALS & MONITORING OF INTERNSHIP  A. Internship  A minimum of 2 -4 credits, out of the required minimum 120/160 credits, of a 3 -year UG  degree/4-year UG degree (Honours)/4 -year UG degree (Honours with Research) can be  assigned for Internship as per the Nati..."

---

### Q3. Does an online internship count for AICTE internship credits?

**Evaluation Status:** Relevant Context Found  

**Top Semantic Hits:**

1. **`internship_doc_1.pdf` (Page 7)** - *AICTE Internship Policy: Guidelines & Procedures (2019)*
   - **Similarity Score:** `0.6357` (Distance: `0.5731`)
   - **Snippet:** "6  CHAPTER - 2  AICTE GUIDELINES FOR ORGANIZING INTERNSHIP  2.1 INTERNSHIP DURATION AND ACADEMIC CREDENTIALS  The following framework is proposed to give academic credit for the internship undergone as part of the  programme.  • A minimum of 14-20 credits of Internship / Entrepre..."

2. **`data/records.json` (Page 1)** - *InternGuide Rule: Internship*
   - **Similarity Score:** `0.6272` (Distance: `0.5945`)
   - **Snippet:** "Activity Head: Internship Sub-Activity: Internship with Industry/Govt. / NGO/PSU/Any Micro/Small/ Medium enterprise/ Online Internship Suggested Credits: 4-6 credits Suggested Duration: 4-6 weeks (30 hours per credit per AICTE) Required Evidence: Evaluating Report Evaluated By: F..."

3. **`internship_doc_1.pdf` (Page 11)** - *AICTE Internship Policy: Guidelines & Procedures (2019)*
   - **Similarity Score:** `0.6204` (Distance: `0.6117`)
   - **Snippet:** "A: Through AICTE Internship Portal"

---

### Q4. I did a 90-hour internship with 9/10 from the company and 5.67 from the college panel, plus a 55-hour rural internship with 6/10. What is my credit and net score?

**Evaluation Status:** Relevant Context Found  

**Top Semantic Hits:**

1. **`internship_doc_1.pdf` (Page 35)** - *AICTE Internship Policy: Guidelines & Procedures (2019)*
   - **Similarity Score:** `0.593` (Distance: `0.6864`)
   - **Snippet:** "Thus, Net Score of the student in Internship Evaluation in this sample case is 8.05 out of 10.00  Note: In case of Diploma Programme, Similar methodology is to be used although few sub-activities and  total credits are different for diploma programme as compared to degree program..."

2. **`internship_doc_1.pdf` (Page 35)** - *AICTE Internship Policy: Guidelines & Procedures (2019)*
   - **Similarity Score:** `0.5804` (Distance: `0.7231`)
   - **Snippet:** "Table 10.1 B  S. No. Major Head of Activity Obtained Score Maximum Score Hours Devoted Net Score in Internship  1 Inter/Intra Institutional 7.44 10 166  8.05  2 Innovation/IPR/Entrepreneurship 9.14 10 210  3 Internship 8.00 10 90  4 Rural Internship 6.00 10 55  5 NSQF Level 3,4,5..."

3. **`data/records.json` (Page 1)** - *InternGuide Rule: Rural Internship*
   - **Similarity Score:** `0.5522` (Distance: `0.8108`)
   - **Snippet:** "Activity Head: Rural Internship Sub-Activity: Long Term goals under rural Internship Suggested Credits: 4-6 credits Suggested Duration: 4-6 weeks (30 hours per credit per AICTE) Required Evidence: Evaluating Report Evaluated By: Faculty Mentor/ TPO / NSS / NCC head"

---

### Q5. I am a final-year B.Tech student, 21 years old. Can I apply for the PM Internship Scheme, and how much stipend will I get?

**Evaluation Status:** Relevant Context Found  

**Top Semantic Hits:**

1. **`internship_doc_2.pdf` (Page 1)** - *UGC Guidelines for Internship/Research Internship for UG Students*
   - **Similarity Score:** `0.5357` (Distance: `0.8666`)
   - **Snippet:** "Guidelines for Internship/Research Internship for  Under Graduate Students  University Grants Commission  Bahadur Shah Zafar Marg  New Delhi- 110002  (2023)"

2. **`internship_doc_1.pdf` (Page 7)** - *AICTE Internship Policy: Guidelines & Procedures (2019)*
   - **Similarity Score:** `0.5133` (Distance: `0.948`)
   - **Snippet:** "6  CHAPTER - 2  AICTE GUIDELINES FOR ORGANIZING INTERNSHIP  2.1 INTERNSHIP DURATION AND ACADEMIC CREDENTIALS  The following framework is proposed to give academic credit for the internship undergone as part of the  programme.  • A minimum of 14-20 credits of Internship / Entrepre..."

3. **`internship_doc_1.pdf` (Page 11)** - *AICTE Internship Policy: Guidelines & Procedures (2019)*
   - **Similarity Score:** `0.5064` (Distance: `0.9746`)
   - **Snippet:** "A.2: Institutes can register and find internship for their students: Institute ID will be handled by TPO.   Step 1: TPO can browse through available internship opportunities and nominate their students for  various opportunities accordingly.   Step 2: Industry/Organisation will..."

---

### Q6. Which specific IT companies in Pune are offering paid AI internships this summer? (Note: InternGuide cannot answer this as the data only covers AICTE rules and PMIS eligibility).

**Evaluation Status:** Correct Out-of-Scope (Low relevance to policy chunks)  

**Top Semantic Hits:**

1. **`internship_doc_1.pdf` (Page 11)** - *AICTE Internship Policy: Guidelines & Procedures (2019)*
   - **Similarity Score:** `0.5897` (Distance: `0.6958`)
   - **Snippet:** "A: Through AICTE Internship Portal"

2. **`internship_doc_1.pdf` (Page 8)** - *AICTE Internship Policy: Guidelines & Procedures (2019)*
   - **Similarity Score:** `0.5806` (Distance: `0.7222`)
   - **Snippet:** "During the summer/winter vacation after 4th/5th semester and during 6th Semester for diploma / In vacation  after 6th semester for degree course, students are ready for industrial experience. Therefore, they may choose to  undergo Internship / Innovation / Entrepreneurship relate..."

3. **`internship_doc_1.pdf` (Page 11)** - *AICTE Internship Policy: Guidelines & Procedures (2019)*
   - **Similarity Score:** `0.5695` (Distance: `0.7559`)
   - **Snippet:** "udents in industries/organization after second,  third, fourth, fifth and sixth semester(s) or as per AICTE / affiliating University guidelines. Institutions are  encouraged to use AICTE’s Internship Portal for arranging & managing internships. The procedure for  arranging intern..."

---

### Q7. Is a 4-week rural NSS camp eligible for internship credits?

**Evaluation Status:** Relevant Context Found  

**Top Semantic Hits:**

1. **`data/records.json` (Page 1)** - *InternGuide Rule: Rural Internship*
   - **Similarity Score:** `0.6473` (Distance: `0.5449`)
   - **Snippet:** "Activity Head: Rural Internship Sub-Activity: Long Term goals under rural Internship Suggested Credits: 4-6 credits Suggested Duration: 4-6 weeks (30 hours per credit per AICTE) Required Evidence: Evaluating Report Evaluated By: Faculty Mentor/ TPO / NSS / NCC head"

2. **`internship_doc_1.pdf` (Page 7)** - *AICTE Internship Policy: Guidelines & Procedures (2019)*
   - **Similarity Score:** `0.6011` (Distance: `0.6636`)
   - **Snippet:** "S.No. Suggested Schedule Suggested  Duration  (In weeks)  Activities Credits   Degree Diploma Degree Diploma Degree/Diploma Degree  (14-20)  Diploma  (10-14)  1 Summer/winter vacation after  2nd/3rd Semester 3-4 3-4 Inter/Intra Institutional  Activities  3-4 3-4  2 Summer/winter ..."

3. **`internship_doc_2.pdf` (Page 9)** - *UGC Guidelines for Internship/Research Internship for UG Students*
   - **Similarity Score:** `0.5662` (Distance: `0.7662`)
   - **Snippet:** "5.0 ACADEMIC CREDENTIALS & MONITORING OF INTERNSHIP  A. Internship  A minimum of 2 -4 credits, out of the required minimum 120/160 credits, of a 3 -year UG  degree/4-year UG degree (Honours)/4 -year UG degree (Honours with Research) can be  assigned for Internship as per the Nati..."

---

### Q8. What is the family income limit to be eligible for the PMIS?

**Evaluation Status:** Relevant Context Found  

**Top Semantic Hits:**

1. **`data/records.json` (Page 1)** - *InternGuide Rule: PMIS Candidate Rule*
   - **Similarity Score:** `0.5772` (Distance: `0.7326`)
   - **Snippet:** "Activity Head: PMIS Candidate Rule Sub-Activity: Family income below 8 Lakhs (No Govt job) Suggested Credits: N/A credits Suggested Duration: N/A weeks (30 hours per credit per AICTE) Required Evidence: Income Certificate / Ration Card Evaluated By: PMIS Portal"

2. **`data/records.json` (Page 1)** - *InternGuide Rule: PMIS Candidate Rule*
   - **Similarity Score:** `0.5017` (Distance: `0.993`)
   - **Snippet:** "Activity Head: PMIS Candidate Rule Sub-Activity: Education requirement (Not full-time employed/studying) Suggested Credits: N/A credits Suggested Duration: N/A weeks (30 hours per credit per AICTE) Required Evidence: Degree / Passing Certificate Evaluated By: PMIS Portal"

3. **`data/records.json` (Page 1)** - *InternGuide Rule: PMIS Candidate Rule*
   - **Similarity Score:** `0.5007` (Distance: `0.9973`)
   - **Snippet:** "Activity Head: PMIS Candidate Rule Sub-Activity: Age requirement between 21 and 24 years Suggested Credits: N/A credits Suggested Duration: N/A weeks (30 hours per credit per AICTE) Required Evidence: Aadhaar / DOB Proof Evaluated By: PMIS Portal"

---

### Q9. Do I need an NOC from my college to join a 12-month internship under the PM Internship Scheme?

**Evaluation Status:** Relevant Context Found  

**Top Semantic Hits:**

1. **`data/records.json` (Page 1)** - *InternGuide Rule: PMIS Candidate Rule*
   - **Similarity Score:** `0.5453` (Distance: `0.8338`)
   - **Snippet:** "Activity Head: PMIS Candidate Rule Sub-Activity: NOC required for final-year or ODL students Suggested Credits: N/A credits Suggested Duration: N/A weeks (30 hours per credit per AICTE) Required Evidence: NOC from Institute Evaluated By: Institute Panel"

2. **`internship_doc_2.pdf` (Page 9)** - *UGC Guidelines for Internship/Research Internship for UG Students*
   - **Similarity Score:** `0.5285` (Distance: `0.8922`)
   - **Snippet:** "learning in the real -life situation depending on the kind of course (e.g. law,  management, social works).  12. The students involved in the internship may continue their internship subject to  the condition that his/her academic credits do not get affected in terms of  attendan..."

3. **`internship_doc_1.pdf` (Page 11)** - *AICTE Internship Policy: Guidelines & Procedures (2019)*
   - **Similarity Score:** `0.5232` (Distance: `0.9113`)
   - **Snippet:** "A.1: Student can register and find internship   Step 1: Student can browse and apply for internships via AICTE’s Internship Portal. Industry will  select the student based on their selection criteria and will send a provisional offer letter/provisional  confirmation (by approvin..."

---

### Q10. How are credits evaluated for an Innovation/IPR incubation project?

**Evaluation Status:** Relevant Context Found  

**Top Semantic Hits:**

1. **`data/records.json` (Page 1)** - *InternGuide Rule: Innovation / IPR / entrepreneurship*
   - **Similarity Score:** `0.6358` (Distance: `0.5728`)
   - **Snippet:** "Activity Head: Innovation / IPR / entrepreneurship Sub-Activity: Participation in all the activities of Institute's Innovation Council for e.g.: IPR workshop/ Leadership Talks/ Idea/ Design/ Innovation/ Business Completion/ Technical Expos etc. Suggested Credits: 4-6 credits Sugg..."

2. **`data/records.json` (Page 1)** - *InternGuide Rule: Innovation / IPR / entrepreneurship*
   - **Similarity Score:** `0.6093` (Distance: `0.6412`)
   - **Snippet:** "Activity Head: Innovation / IPR / entrepreneurship Sub-Activity: Participation in innovation related completions for e.g. Hackathons etc. Suggested Credits: 4-6 credits Suggested Duration: 4-6 weeks (30 hours per credit per AICTE) Required Evidence: Certificate Evaluated By: Facu..."

3. **`data/records.json` (Page 1)** - *InternGuide Rule: Innovation / IPR / entrepreneurship*
   - **Similarity Score:** `0.6022` (Distance: `0.6607`)
   - **Snippet:** "Activity Head: Innovation / IPR / entrepreneurship Sub-Activity: Development of new product/ Business Plan/ registration of start-up Suggested Credits: 4-6 credits Suggested Duration: 4-6 weeks (30 hours per credit per AICTE) Required Evidence: Certificate Evaluated By: Programme..."

---
