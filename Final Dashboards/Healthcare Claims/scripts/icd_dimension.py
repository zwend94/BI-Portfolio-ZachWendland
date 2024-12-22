import pandas as pd
import numpy as np

def generate_icd_dimension(icd_codes):
    # Some example descriptions:
    icd_descriptions = [
        "Acute upper respiratory infection",
        "Chronic obstructive pulmonary disease",
        "Type 2 diabetes mellitus without complications",
        "Essential (primary) hypertension",
        "Chest pain, unspecified",
        "Acute bronchitis",
        "Depressive episodes",
        "Hyperlipidemia",
        "Asthma, unspecified",
        "Migraine, unspecified"
    ]
    
    # Randomly assign a description to each ICD code
    descriptions = np.random.choice(icd_descriptions, size=len(icd_codes))
    
    icd_dim = pd.DataFrame({
        "ICD-10": icd_codes,
        "ICD-10 Description": descriptions
    }).drop_duplicates(subset=["ICD-10"])
    
    return icd_dim
