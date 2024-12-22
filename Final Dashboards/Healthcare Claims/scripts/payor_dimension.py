import pandas as pd

def generate_payor_dimension():
    # Government payors
    gov_payors = [
        {"Payor ID": "0000000001", "Payor Name": "Medicare", "Is Government": True},
        {"Payor ID": "0000000002", "Payor Name": "Medicaid", "Is Government": True}
    ]
    
    payor_dim = pd.DataFrame(gov_payors)
    return payor_dim
