import pandas as pd
import numpy as np
from datetime import datetime
from payor_dimension import generate_payor_dimension
from icd_dimension import generate_icd_dimension
from facility_dimension import generate_facility_dimension
import os 

os.chdir("C:/Users/lyyud/Documents/Website")

def generate_fixed_claims_data(total_records=377000):
    start_date = datetime(2019, 1, 1)
    end_date = datetime.now()

    claim_dates = np.random.choice(pd.date_range(start_date, end_date).to_numpy(), total_records)
    ages = np.random.randint(1, 100, total_records)

    service_start_dates = claim_dates - np.random.randint(0, 30, total_records).astype("timedelta64[D]")
    service_end_dates = service_start_dates + np.random.randint(1, 10, total_records).astype("timedelta64[D]")
    payment_dates = claim_dates + np.random.randint(1, 60, total_records).astype("timedelta64[D]")

    # 30% gov payors, 70% private
    gov_count = int(total_records * 0.3)
    private_count = total_records - gov_count

    # Government payors
    gov_payor_names = np.random.choice(["Medicare", "Medicaid"], gov_count, p=[0.5, 0.5])
    gov_payor_ids = np.where(gov_payor_names == "Medicare", "0000000001", "0000000002")

    # Private payors
    private_payors_list = [
        "United Healthcare",
        "Aetna",
        "Cigna",
        "Humana",
        "Blue Cross Blue Shield",
        "Kaiser Permanente",
        "Centene",
        "Anthem",
        "Molina Healthcare",
        "WellCare"
    ]
    private_payor_names = np.random.choice(private_payors_list, private_count)
    private_payor_ids = [f"{pid:010d}" for pid in np.random.randint(3, 10**10, private_count)]

    payor_names = np.concatenate([gov_payor_names, private_payor_names])
    payor_ids = np.concatenate([gov_payor_ids, private_payor_ids])

    idx = np.arange(total_records)
    np.random.shuffle(idx)

    payor_names = payor_names[idx]
    payor_ids = payor_ids[idx]
    claim_dates = claim_dates[idx]
    service_start_dates = service_start_dates[idx]
    service_end_dates = service_end_dates[idx]
    payment_dates = payment_dates[idx]
    ages = ages[idx]

    # Generate ICD-10 codes
    icd_code_count = 100  # number of unique ICD codes
    unique_icd_codes = [f"D{np.random.randint(100,999)}" for _ in range(icd_code_count)]
    unique_icd_codes = list(set(unique_icd_codes))
    if len(unique_icd_codes) < icd_code_count:
        needed = icd_code_count - len(unique_icd_codes)
        unique_icd_codes += [f"D{1000+i}" for i in range(needed)]

    icd_codes = np.random.choice(unique_icd_codes, total_records)

    # Generate Facility IDs
    facility_count = 500  # number of unique facilities
    unique_facility_ids = [f"{fid:010d}" for fid in np.random.randint(0, 10**10, facility_count)]
    facility_ids = np.random.choice(unique_facility_ids, total_records)

    data = {
        "Claim ID": [f"C{np.random.randint(1000000, 9999999)}" for _ in range(total_records)],
        "Claim Date": claim_dates.astype(str),
        "Provider ID": [f"{pid:010d}" for pid in np.random.randint(0, 10**10, total_records)],
        "Facility ID": facility_ids,
        "Payor ID": payor_ids,
        "Payor Name": payor_names,
        "Patient ID": [f"{patid:010d}" for patid in np.random.randint(0, 10**10, total_records)],
        "Gender": np.random.choice(["Male", "Female"], total_records),
        "Age": ages,
        "ICD-10": icd_codes,
        "Procedure Code": [f"P{np.random.randint(1000, 9999)}" for _ in range(total_records)],
        "Amount Billed": np.round(np.random.uniform(100, 5000, total_records), 2),
        "Amount Paid": np.round(np.random.uniform(0, 5000, total_records), 2),
        "Claim Status": np.random.choice(["Paid", "Denied", "Pending"], total_records, p=[0.7, 0.2, 0.1]),
        "Service Date Start": service_start_dates.astype(str),
        "Service Date End": service_end_dates.astype(str),
        "Payment Date": payment_dates.astype(str),
        "Adjustments": np.round(np.random.uniform(0, 500, total_records), 2),
        "Deductibles": np.round(np.random.uniform(0, 500, total_records), 2),
        "Co-pays": np.round(np.random.uniform(0, 500, total_records), 2),
    }

    fact_df = pd.DataFrame(data)
    return fact_df, unique_icd_codes, unique_facility_ids, private_payors_list

# Main execution
if __name__ == "__main__":
    fact_df, unique_icd_codes, unique_facility_ids, private_payors_list = generate_fixed_claims_data()

    # Generate dimension tables
    payor_dim = generate_payor_dimension()

    # Extract unique payors from fact for private payors
    private_payor_rows = fact_df[~fact_df["Payor ID"].isin(["0000000001", "0000000002"])]
    unique_private = private_payor_rows[["Payor ID", "Payor Name"]].drop_duplicates()
    unique_private["Is Government"] = False

    # Combine government and private payors
    payor_dim = pd.concat([payor_dim, unique_private], ignore_index=True).drop_duplicates(subset=["Payor ID"])

    # Generate ICD dimension
    icd_dim = generate_icd_dimension(unique_icd_codes)

    # Generate Facility dimension
    facility_dim = generate_facility_dimension(unique_facility_ids)

    # Output all to CSV
    fact_df.to_csv("fact_claims_data.csv", index=False)
    payor_dim.to_csv("dim_payor.csv", index=False)
    icd_dim.to_csv("dim_icd10.csv", index=False)
    facility_dim.to_csv("dim_facility.csv", index=False)

    print("All CSV files have been generated:")
    print("- fact_claims_data.csv")
    print("- dim_payor.csv")
    print("- dim_icd10.csv")
    print("- dim_facility.csv")
