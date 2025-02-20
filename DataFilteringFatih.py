import pandas as pd
import numpy as np
import os
from ConvertFunctions import convert_to_int

def clear_db(db):
    DeletingRows = []

    i = 0
    while i < (len(db['test'])):
        checker = 0
        for j in range(4):
            try:
                if isinstance(db['result'].iloc[i + j], int):
                    checker += 1

            except:
                break

        if checker == 4:
            i += 4

        else:
            DeletingRows.append(i)
            i += 1

    db.drop(DeletingRows, inplace=True)
    db.dropna()

def process_fatih_file(file_path):
    # Read the Excel file
    result_df = pd.read_excel(file_path, usecols='G, F, Q, R')

    # Set column names and process
    column_names = ['age', 'gender', 'test', 'result']
    result_df.columns = column_names
    result_df['result'] = result_df['result'].astype("str").apply(convert_to_int)
    result_df.fillna(method='ffill', inplace=True)

    clear_db(result_df)
    result_df.reset_index(drop=True, inplace=True)

    # Initialize lists
    age_and_dependents = []
    LDL = []
    gender = []
    k = 2

    # Process data
    while k < len(result_df['test']):
        if result_df['result'][k - 1] < 1500:
            LDL.append(result_df['result'].iloc[k])
            age_and_dependents.append([
                result_df['age'].iloc[k],
                result_df['result'].iloc[k - 2],  # KLS
                result_df['result'].iloc[k - 1],  # TGL
                result_df['result'].iloc[k + 1]  # HDL
            ])
            gender.append(result_df['gender'].iloc[k])
            k += 4
        else:
            k += 4

    return age_and_dependents, LDL, gender


def combine_fatih_files(directory="."):  # Default to current directory if none specified
    fatih_files = [
        "01-11-2023-31-01-2024  FATİH.xlsx",
        "01-10-202330-11-2023 FATİH.xlsx",
        "01-07-2023-30-09-2023 FATİH.xlsx",
        "01-04-2023-30-06-2023 FATİH.xlsx",
        "01-01-2023-31-03-2023 FATİH.xlsx"
    ]

    # Print available files in directory for debugging
    print(f"Files in directory: {os.listdir(directory)}")

    all_age_deps = []
    all_ldl = []
    all_gender = []

    for file in fatih_files:
        file_path = os.path.abspath(os.path.join(directory, file))
        if os.path.exists(file_path):
            try:
                print(f"Processing {file}...")
                age_deps, ldl, gend = process_fatih_file(file_path)
                all_age_deps.extend(age_deps)
                all_ldl.extend(ldl)
                all_gender.extend(gend)
                print(f"Successfully processed {len(ldl)} records from {file}")
            except Exception as e:
                print(f"Error processing {file}: {str(e)}")
        else:
            print(f"File not found: {file_path}")

    # Continue with the rest of your existing code...
    # Convert to arrays
    all_age_deps = np.array(all_age_deps)
    all_ldl = np.array(all_ldl)
    all_gender = np.array(all_gender)

    # Create DataFrame for saving
    df = pd.DataFrame({
        'age': all_age_deps[:, 0],
        'KLS': all_age_deps[:, 1],
        'TGL': all_age_deps[:, 2],
        'HDL': all_age_deps[:, 3],
        'LDL': all_ldl,
        'gender': all_gender
    })

    # Save to Excel
    output_file = 'combined_fatih_data.xlsx'
    df.to_excel(output_file, index=False)
    print(f"\nAll data combined and saved to {output_file}")
    print(f"Total records processed: {len(df)}")

    return all_age_deps, all_ldl, all_gender

def load_combined_data(file_path='combined_fatih_data.xlsx'):

    df = pd.read_excel(file_path)

    # Create age_and_dependents array
    age_and_dependents = np.column_stack((
        df['age'],
        df['KLS'],
        df['TGL'],
        df['HDL']
    ))

    LDL = np.array(df['LDL'])
    gender = np.array(df['gender'])

    return age_and_dependents, LDL, gender