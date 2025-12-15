import pandas as pd
import numpy as np

def anonymize_csv(input_file, output_file):
    df = pd.read_csv(input_file)
    
    # Create anonymized employee names
    df['First Name'] = 'Employee'
    df['Last Name'] = df.index.astype(str).str.zfill(3)
    
    # Create manager mapping for consistency
    unique_managers = df['Manager'].unique()
    manager_mapping = {mgr: f'Manager {chr(65 + i)}' for i, mgr in enumerate(unique_managers)}
    df['Manager'] = df['Manager'].map(manager_mapping)
    
    # Anonymize or remove PII fields
    if 'email' in df.columns:
        df['email'] = df.index.map(lambda x: f'employee{str(x).zfill(3)}@company.com')
    
    if 'iba-id' in df.columns:
        df['iba-id'] = df.index.map(lambda x: f'IBA{str(x).zfill(5)}')
    
    if 'hrbp' in df.columns:
        unique_hrbp = df['hrbp'].unique()
        hrbp_mapping = {hrbp: f'HRBP {chr(65 + i)}' for i, hrbp in enumerate(unique_hrbp)}
        df['hrbp'] = df['hrbp'].map(hrbp_mapping)
    
    # Save anonymized data
    df.to_csv(output_file, index=False)
    print(f"✓ Anonymized {input_file} -> {output_file}")
    print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
    return df

if __name__ == "__main__":
    # Anonymize both files
    df_2024 = anonymize_csv('utils/2024.csv', 'utils/2024.csv')
    df_2025 = anonymize_csv('utils/2025.csv', 'utils/2025.csv')
    
    print("\n✓ Anonymization complete!")
    print("\nSample data from 2024:")
    print(df_2024[['First Name', 'Last Name', 'Manager', 'Department']].head(5))
