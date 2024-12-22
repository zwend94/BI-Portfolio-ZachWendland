import pandas as pd
import numpy as np

def generate_facility_dimension(facility_ids):
    # Random city/state assignments
    cities_states = [
        ("New York", "NY"),
        ("Los Angeles", "CA"),
        ("Chicago", "IL"),
        ("Houston", "TX"),
        ("Phoenix", "AZ"),
        ("Philadelphia", "PA"),
        ("San Antonio", "TX"),
        ("San Diego", "CA"),
        ("Dallas", "TX"),
        ("San Jose", "CA"),
        ("Austin", "TX"),
        ("Jacksonville", "FL"),
        ("Fort Worth", "TX"),
        ("Columbus", "OH"),
        ("Charlotte", "NC"),
        ("San Francisco", "CA"),
        ("Indianapolis", "IN"),
        ("Seattle", "WA"),
        ("Denver", "CO"),
        ("Washington", "DC")
    ]
    
    choices = np.random.choice(len(cities_states), size=len(facility_ids))
    city = [cities_states[i][0] for i in choices]
    state = [cities_states[i][1] for i in choices]
    
    facility_dim = pd.DataFrame({
        "Facility ID": facility_ids,
        "City": city,
        "State": state
    }).drop_duplicates(subset=["Facility ID"])
    
    return facility_dim
