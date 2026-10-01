from fastapi import FastAPI
from pydantic import BaseModel, Field
from backend.calculator import calculate_cockcroft_gault, calculate_ckd_epi_2021
from backend.drug_rules import evaluate_drug_dose, DRUG_DATABASE

app = FastAPI(title="RenalGuard API", version="1.0.0")

class PatientEvaluationRequest(BaseModel):
    age: int = Field(..., ge=18, le=120)
    sex: str = Field(..., pattern="^(male|female)$")
    weight_kg: float = Field(..., gt=20.0, lt=400.0)
    height_cm: float = Field(..., gt=50.0, lt=260.0)
    scr_mg_dl: float = Field(..., gt=0.1, lt=25.0)
    drug_id: str

@app.get("/drugs")
def get_available_drugs():
    return [{"id": k, "name": v["name"]} for k, v in DRUG_DATABASE.items()]

@app.post("/evaluate")
def evaluate_patient(payload: PatientEvaluationRequest):
    cg_res = calculate_cockcroft_gault(
        payload.age, payload.weight_kg, payload.height_cm, payload.scr_mg_dl, payload.sex
    )
    egfr_res = calculate_ckd_epi_2021(
        payload.age, payload.scr_mg_dl, payload.sex
    )
    dosing_eval = evaluate_drug_dose(payload.drug_id, cg_res["crcl_ml_min"], egfr_res)
    
    return {
        "patient_metrics": {
            "ibw_kg": cg_res["ibw_kg"],
            "dosing_weight_kg": cg_res["weight_used_kg"],
            "dosing_weight_strategy": cg_res["weight_strategy"],
            "crcl_ml_min": cg_res["crcl_ml_min"],
            "egfr_ckd_epi_2021": egfr_res
        },
        "guidance": dosing_eval
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)