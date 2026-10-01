import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="RenalGuard - Clinical Dose Adjuster", layout="wide")
st.title("RenalGuard: Renal Dose Decision Engine")
st.caption("Point-of-care renal dosing evaluation based on Cockcroft-Gault and CKD-EPI 2021.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Patient Demographics & Labs")
    age = st.number_input("Age (years)", min_value=18, max_value=110, value=68)
    sex = st.selectbox("Biological Sex", ["male", "female"])
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=250.0, value=78.0)
    height = st.number_input("Height (cm)", min_value=100.0, max_value=230.0, value=170.0)
    scr = st.number_input("Serum Creatinine (mg/dL)", min_value=0.2, max_value=15.0, value=1.8, step=0.1)

    st.subheader("2. Medication Selection")
    try:
        drug_res = requests.get(f"{API_URL}/drugs", timeout=5).json()
        drug_options = {d["name"]: d["id"] for d in drug_res}
        selected_drug_name = st.selectbox("Select Drug", list(drug_options.keys()))
        selected_drug_id = drug_options[selected_drug_name]
    except Exception:
        st.error("Could not reach FastAPI backend. Make sure the server is running on port 8000.")
        selected_drug_id = None

    submit_btn = st.button("Calculate & Evaluate", type="primary")

with col2:
    st.subheader("3. Clinical Evaluation")
    if submit_btn and selected_drug_id:
        payload = {
            "age": age,
            "sex": sex,
            "weight_kg": weight,
            "height_cm": height,
            "scr_mg_dl": scr,
            "drug_id": selected_drug_id
        }
        
        try:
            res = requests.post(f"{API_URL}/evaluate", json=payload, timeout=5)
            if res.status_code == 200:
                data = res.json()
                metrics = data["patient_metrics"]
                guidance = data["guidance"]

                mcol1, mcol2, mcol3 = st.columns(3)
                mcol1.metric("CrCl (Cockcroft-Gault)", f"{metrics['crcl_ml_min']} mL/min")
                mcol2.metric("eGFR (CKD-EPI)", f"{metrics['egfr_ckd_epi_2021']} mL/min/1.73m²")
                mcol3.metric("IBW", f"{metrics['ibw_kg']} kg")

                st.info(f"Weight strategy applied: **{metrics['dosing_weight_strategy']}** ({metrics['dosing_weight_kg']} kg)")

                status = guidance["status"]
                if status == "NORMAL":
                    st.success(f"**Recommendation:** {guidance['recommendation']}")
                elif status == "WARNING":
                    st.warning(f"**Dose Adjustment Required:** {guidance['recommendation']}")
                elif status == "CONTRAINDICATED":
                    st.error(f"**CONTRAINDICATION:** {guidance['recommendation']}")

                st.markdown(f"**Indication:** {guidance['indication']}")
                st.markdown(f"**Evaluated using:** `{guidance['metric_used']}` = {guidance['metric_value']}")
                st.caption(f"**Clinical Note:** {guidance['clinical_note']}")
            else:
                st.error("Error evaluating patient parameters.")
        except Exception as e:
            st.error(f"Request failed: {e}")