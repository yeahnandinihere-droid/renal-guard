def compute_ibw(height_cm: float, sex: str) -> float:
    height_inches = height_cm / 2.54
    inches_over_5ft = max(0.0, height_inches - 60.0)
    if sex.lower() == "male":
        return 50.0 + (2.3 * inches_over_5ft)
    else:
        return 45.5 + (2.3 * inches_over_5ft)

def select_dosing_weight(weight_kg: float, ibw: float) -> tuple[float, str]:
    if weight_kg < ibw:
        return weight_kg, "Actual Weight (Underweight)"
    elif weight_kg >= 1.2 * ibw:
        adj_bw = ibw + 0.4 * (weight_kg - ibw)
        return round(adj_bw, 2), "Adjusted Body Weight (AdjBW - Obese)"
    return round(ibw, 2), "Ideal Body Weight (IBW)"

def calculate_cockcroft_gault(age: int, weight_kg: float, height_cm: float, scr: float, sex: str) -> dict:
    ibw = compute_ibw(height_cm, sex)
    dosing_weight, weight_type = select_dosing_weight(weight_kg, ibw)
    
    crcl = ((140.0 - age) * dosing_weight) / (72.0 * scr)
    if sex.lower() == "female":
        crcl *= 0.85
        
    return {
        "crcl_ml_min": round(crcl, 2),
        "ibw_kg": round(ibw, 2),
        "weight_used_kg": dosing_weight,
        "weight_strategy": weight_type
    }

def calculate_ckd_epi_2021(age: int, scr: float, sex: str) -> float:
    is_female = (sex.lower() == "female")
    kappa = 0.7 if is_female else 0.9
    alpha = -0.241 if is_female else -0.302
    gender_mult = 1.012 if is_female else 1.0

    scr_ratio = scr / kappa
    min_factor = min(scr_ratio, 1.0) ** alpha
    max_factor = max(scr_ratio, 1.0) ** (-1.200)
    age_factor = 0.9938 ** age

    egfr = 142.0 * min_factor * max_factor * age_factor * gender_mult
    return round(egfr, 2)