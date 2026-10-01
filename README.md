# renal-guard

Clinical decision support engine \& dashboard for renal dosage adjustments using Cockcroft-Gault and CKD-EPI equations.

\# 🩺 RenalGuard: Clinical Decision Support System (CDSS) for Renal Dose Adjustment



\[!\[Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

\[!\[FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)

\[!\[Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B.svg)](https://streamlit.io/)

\[!\[License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



\*\*RenalGuard\*\* is a point-of-care Clinical Decision Support System designed to mitigate medication errors and optimize drug dosing for patients with renal impairment. It pairs a decoupled \*\*FastAPI\*\* backend evaluation engine with an interactive \*\*Streamlit\*\* clinical dashboard.



\---



\## 🎯 Clinical Motivation



In clinical pharmacotherapy, inappropriate renal dose adjustments remain a major source of preventable Adverse Drug Events (ADEs). Routine lab panels typically report estimated Glomerular Filtration Rate (\*\*eGFR\*\*) via CKD-EPI, whereas the majority of FDA-approved product labeling and dosing monographs mandate Creatinine Clearance (\*\*CrCl\*\*) calculated via the Cockcroft-Gault equation.



Furthermore, applying actual body weight in obese patients frequently overestimates renal clearance, leading to supratherapeutic dosing and toxicity. RenalGuard dynamically resolves this discrepancy by calculating clearance using standardized dosing weight adjustments.



\---



\## 🔬 Pharmacokinetic \& Clearance Equations



\### 1. Ideal \& Adjusted Body Weight Selection

\* \*\*Ideal Body Weight (IBW) (Devine Formula):\*\*

&#x20; \* \*Males:\* $50.0\\text{ kg} + 2.3 \\times (\\text{Height in inches} - 60)$

&#x20; \* \*Females:\* $45.5\\text{ kg} + 2.3 \\times (\\text{Height in inches} - 60)$

\* \*\*Dosing Weight Selection Logic:\*\*

&#x20; \* If $\\text{Actual Weight} < \\text{IBW} \\implies$ \*\*Actual Weight\*\* (Underweight protection)

&#x20; \* If $\\text{Actual Weight} \\ge 1.2 \\times \\text{IBW} \\implies$ \*\*Adjusted Body Weight (AdjBW)\*\*:

&#x20;   $$\\text{AdjBW} = \\text{IBW} + 0.4 \\times (\\text{Actual Weight} - \\text{IBW})$$

&#x20; \* Otherwise $\\implies$ \*\*IBW\*\*



\### 2. Cockcroft-Gault CrCl

$$\\text{CrCl (mL/min)} = \\frac{(140 - \\text{Age}) \\times \\text{Dosing Weight (kg)}}{72 \\times \\text{SCr (mg/dL)}} \\times \[0.85\\text{ if female}]$$



\### 3. CKD-EPI 2021 (Race-Free eGFR)

$$\\text{eGFR} = 142 \\times \\min\\left(\\frac{\\text{SCr}}{\\kappa}, 1\\right)^\\alpha \\times \\max\\left(\\frac{\\text{SCr}}{\\kappa}, 1\\right)^{-1.200} \\times 0.9938^{\\text{Age}} \\times \[1.012\\text{ if female}]$$

\*Where $\\kappa = 0.7$ (female) / $0.9$ (male), and $\\alpha = -0.241$ (female) / $-0.302$ (male).\*



\---



\## 💊 Supported Medications \& Safety Rules



| Medication | Primary Metric | Evaluation Rationale \& Safety Thresholds |

|---|---|---|

| \*\*Enoxaparin (Lovenox)\*\* | CrCl (Cockcroft-Gault) | Dose interval prolongation ($Q12H \\to Q24H$) if $\\text{CrCl} < 30\\text{ mL/min}$. Contraindicated / switch to UFH if $\\text{CrCl} < 15\\text{ mL/min}$. |

| \*\*Metformin\*\* | eGFR (CKD-EPI) | Maximum $1000\\text{ mg/day}$ if $\\text{eGFR } 30\\text{--}45\\text{ mL/min/1.73m}^2$. Absolute contraindication if $\\text{eGFR} < 30$ to prevent MALA. |

| \*\*Apixaban (Eliquis)\*\* | CrCl (Cockcroft-Gault) | Evaluates ABC dose reduction criteria (Age $\\ge 80$, Weight $\\le 60\\text{ kg}$, $\\text{SCr} \\ge 1.5\\text{ mg/dL}$). Dose halved if $\\text{CrCl } 15\\text{--}25\\text{ mL/min}$. |



\---



\## 🏗️ Architecture

