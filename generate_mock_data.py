import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_data(num_records=1000, output_file='levitation_cleaned_experiments.csv'):
    np.random.seed(42)
    
    # Material Types
    materials = ['Graphene-YBCO', 'Quantum Flex', 'Niobium-Titanium', 
                 'Bismuth-Strontium', 'Gold-Coated Aerogel', 'Carbon Nanotubes']
    
    # Lab IDs
    labs = ['Lab-Alpha', 'Lab-Beta', 'Lab-Gamma', 'Lab-Delta', 'Lab-Epsilon']
    
    # Date generation
    start_date = datetime(2020, 1, 1)
    dates = [start_date + timedelta(days=np.random.randint(0, 1800)) for _ in range(num_records)]
    month_years = [d.strftime('%Y-%m') for d in dates]
    
    # Generating correlated data
    # Altitude depends on material, power, and temperature
    material_multiplier = {
        'Graphene-YBCO': 1.8,
        'Quantum Flex': 2.1,
        'Niobium-Titanium': 1.2,
        'Bismuth-Strontium': 1.4,
        'Gold-Coated Aerogel': 0.8,
        'Carbon Nanotubes': 1.6
    }
    
    material_col = np.random.choice(materials, num_records)
    lab_col = np.random.choice(labs, num_records)
    
    power = np.random.normal(1200, 400, num_records)
    power = np.clip(power, 200, 3000)
    
    temperature = np.random.normal(70, 15, num_records) # Kelvin
    temperature = np.clip(temperature, 4, 150)
    
    # Altitude logic: Higher power + lower temp + better material = higher altitude
    base_altitude = power * 0.005 - (temperature * 0.02)
    material_factor = np.array([material_multiplier[m] for m in material_col])
    noise = np.random.normal(0, 1.5, num_records)
    
    altitude = base_altitude * material_factor + noise
    altitude = np.clip(altitude, 0, 25) # Max 25 meters
    
    # Success Rate (proxy for stability)
    success_rate = 100 - (temperature * 0.4) + (altitude * 1.5) + np.random.normal(0, 5, num_records)
    success_rate = np.clip(success_rate, 0, 100)
    
    df = pd.DataFrame({
        'Experiment_ID': [f'EXP-{str(i).zfill(4)}' for i in range(1, num_records + 1)],
        'Month_Year': month_years,
        'Date': [d.strftime('%Y-%m-%d') for d in dates],
        'Lab_ID': lab_col,
        'Material_Type': material_col,
        'Power_Consumption_W': power,
        'Temperature_K': temperature,
        'Levitation_Altitude_m': altitude,
        'Success_Rate_Percent': success_rate
    })
    
    # Sort by date
    df = df.sort_values('Date').reset_index(drop=True)
    
    df.to_csv(output_file, index=False)
    print(f"Successfully generated {num_records} records to {output_file}")

if __name__ == "__main__":
    generate_mock_data(2500)
