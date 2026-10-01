import streamlit as st
import sys
import os

# Add parent directory to path so it can import backend modules directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from backend.calculator import calculate_cockcroft_gault, calculate_ckd_epi_2021
    from backend.drug_rules import evaluate_drug_dose, DRUG_DATABASE
except ImportError:
    from calculator import calculate_cockcroft_gault, calculate_ckd_epi_2021
    from drug_rules import evaluate_drug_dose, DRUG_DATABASE

st.set_page_config(
    page_title="RenalGuard - Clinical Dose Adjuster",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 RenalGuard: Renal Dose Decision Engine")
st.caption("Point-of-care renal function evaluation based on Cockcroft-Gault and CKD-EPI 2021.")
st.divider()

col1, col2 = st.columns([1, 1.2], gap="medium")

with col1:
    st.subheader("1. Patient Demographics & Labs")
    
    subcol1, subcol2 = st.columns(2)
    with subcol1:
        age = st.number_input("Age (years)", min_value=18, max_value=110, value=68, step=1)
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=250.0, value=78.0, step=0.5)
    with subcol2:
        sex = st.selectbox("Biological Sex", ["male", "female"], format_func=lambda x: x.capitalize())
        height = st.number_input("Height (cm)", min_value=100.0, max_value=230.0, value=170.0, step=0.5)

    scr = st.number_input("Serum Creatinine (mg/dL)", min_value=0.2, max_value=15.0, value=1.8, step=0.1)

    st.subheader("2. Medication Selection")
    drug_options = {v["name"]: k for k, v in DRUG_DATABASE.items()}
    selected_drug_name = st.selectbox("Select Drug", list(drug_options.keys()))
    selected_drug_id = drug_options[selected_drug_name]

    eval_button = st.button("Calculate & Evaluate", type="primary", use_container_width=True)

with col2:
    st.subheader("3. Clinical Evaluation")
    
    # Calculate patient metrics directly
    cg = calculate_cockcroft_gault(age, weight, height, scr, sex)
    egfr = calculate_ckd_epi_2021(age, scr, sex)
    guidance = evaluate_drug_dose(selected_drug_id, cg["crcl_ml_min"], egfr)

    m1, m2, m3 = st.columns(3)
    m1.metric("CrCl (Cockcroft-Gault)", f"{cg['crcl_ml_min']} mL/min")
    m2.metric("eGFR (CKD-EPI 2021)", f"{egfr} mL/min/1.73m²")
    m3.metric("Ideal Body Weight", f"{cg['ibw_kg']} kg")

    st.info(
        f"**Weight strategy applied:** {cg['weight_strategy']} "
        f"(`{cg['weight_used_kg']} kg` applied to Cockcroft-Gault)"
    )

    st.subheader("4. Actionable Guidance")
    status = guidance["status"]
    if status == "NORMAL":
        st.success(f"**Recommendation:** {guidance['recommendation']}")
    elif status == "WARNING":
        st.warning(f"**Dose Adjustment Required:** {guidance['recommendation']}")
    elif status == "CONTRAINDICATED":
        st.error(f"**CONTRAINDICATION:** {guidance['recommendation']}")

    st.markdown(f"**Indication:** {guidance['indication']}")
    st.markdown(f"**Evaluated using:** `{guidance['metric_used']}` = **{guidance['metric_value']}**")
    
    with st.expander("Clinical Pharmacology & Dosing Notes", expanded=True):
        st.caption(guidance["clinical_note"])

st.divider()
st.caption("RenalGuard CDSS | Clinical Informatics Decision Support")