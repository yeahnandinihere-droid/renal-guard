DRUG_DATABASE = {
    "enoxaparin": {
        "name": "Enoxaparin (Lovenox)",
        "indication": "Therapeutic Anticoagulation (DVT/PE)",
        "standard_dose": "1 mg/kg subcutaneously Q12H (or 1.5 mg/kg Q24H)",
        "evaluation_metric": "CrCl",
        "rules": [
            {
                "min": 30.0,
                "max": 999.0,
                "adjusted_dose": "1 mg/kg subcutaneously Q12H",
                "alert_level": "NORMAL",
                "notes": "Standard dosing applies."
            },
            {
                "min": 15.0,
                "max": 30.0,
                "adjusted_dose": "1 mg/kg subcutaneously Q24H",
                "alert_level": "WARNING",
                "notes": "Reduce dose frequency to Q24H due to risk of drug accumulation."
            },
            {
                "min": 0.0,
                "max": 15.0,
                "adjusted_dose": "Avoid or use Unfractionated Heparin (UFH)",
                "alert_level": "CONTRAINDICATED",
                "notes": "Severe bleeding risk. Switch to UFH monitored by aPTT or anti-Xa."
            }
        ]
    },
    "metformin": {
        "name": "Metformin",
        "indication": "Type 2 Diabetes Mellitus",
        "standard_dose": "500 mg - 1000 mg BID with meals",
        "evaluation_metric": "eGFR",
        "rules": [
            {
                "min": 45.0,
                "max": 999.0,
                "adjusted_dose": "Standard titration (up to 2000 mg/day max)",
                "alert_level": "NORMAL",
                "notes": "Monitor renal panel annually."
            },
            {
                "min": 30.0,
                "max": 45.0,
                "adjusted_dose": "Max 1000 mg/day; do NOT initiate in new patients",
                "alert_level": "WARNING",
                "notes": "Assess risk/benefit. High risk of lactic acidosis."
            },
            {
                "min": 0.0,
                "max": 30.0,
                "adjusted_dose": "CONTRAINDICATED",
                "alert_level": "CONTRAINDICATED",
                "notes": "Absolute contraindication due to high risk of metformin-associated lactic acidosis (MALA)."
            }
        ]
    },
    "apixaban": {
        "name": "Apixaban (Eliquis)",
        "indication": "Nonvalvular Atrial Fibrillation",
        "standard_dose": "5 mg BID",
        "evaluation_metric": "CrCl",
        "rules": [
            {
                "min": 25.0,
                "max": 999.0,
                "adjusted_dose": "5 mg BID (or 2.5 mg BID if 2 of: Age >= 80, Wt <= 60 kg, SCr >= 1.5)",
                "alert_level": "NORMAL",
                "notes": "Apply ABC dose reduction criteria."
            },
            {
                "min": 15.0,
                "max": 25.0,
                "adjusted_dose": "2.5 mg BID",
                "alert_level": "WARNING",
                "notes": "Clinical data limited in severe renal impairment."
            },
            {
                "min": 0.0,
                "max": 15.0,
                "adjusted_dose": "Not recommended",
                "alert_level": "CONTRAINDICATED",
                "notes": "Insufficient safety evidence."
            }
        ]
    }
}

def evaluate_drug_dose(drug_id: str, crcl: float, egfr: float) -> dict:
    drug = DRUG_DATABASE.get(drug_id.lower())
    if not drug:
        return {"error": "Drug not found in registry"}
    
    val = crcl if drug["evaluation_metric"] == "CrCl" else egfr
    
    for rule in drug["rules"]:
        if rule["min"] <= val < rule["max"]:
            return {
                "drug": drug["name"],
                "indication": drug["indication"],
                "metric_used": drug["evaluation_metric"],
                "metric_value": val,
                "recommendation": rule["adjusted_dose"],
                "status": rule["alert_level"],
                "clinical_note": rule["notes"]
            }
            
    return {"status": "UNKNOWN", "recommendation": "Consult clinical pharmacologist."}