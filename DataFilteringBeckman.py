import pandas as pd
import numpy as np
import os
from ConvertFunctions import convert_to_int, convert_to_float


def clear_db(db):
    DeletingRows = []

    i = 0
    while i < (len(db['test'])):
        checker = 0
        for j in range(4):
            try:
                value = db['result'].iloc[i + j]
                # Convert string value if it contains comma
                if isinstance(value, str):
                    # Replace comma with dot for decimal numbers
                    value = value.replace(',', '.')

                # Now check if it's numeric after potential comma replacement
                if isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '', 1).isdigit()):
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

def process_beckman_file(file_path):
    # Read the Excel file
    result_df = pd.read_excel(file_path, usecols='G, F, Q, R')

    # Set column names and process
    column_names = ['age', 'gender', 'test', 'result']
    result_df.columns = column_names
    result_df['result'] = result_df['result'].astype("str").apply(convert_to_float)
    result_df['result'] = result_df['result'].apply(convert_to_int)
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


def combine_beckman_files(directory="."):  # Default to current directory if none specified
    beckman_files = [
        "24December25Jan.xlsx",
        "OctoNove2024.xlsx",
        "August2024.xlsx",
        "JuneJuly2024.xlsx",
        "AprilMay2024.xlsx",
        "FebMarch2024.xlsx"
    ]

    # Print available files in directory for debugging
    print(f"Files in directory: {os.listdir(directory)}")

    all_age_deps = []
    all_ldl = []
    all_gender = []

    for file in beckman_files:
        file_path = os.path.abspath(os.path.join(directory, file))
        if os.path.exists(file_path):
            try:
                print(f"Processing {file}...")
                age_deps, ldl, gend = process_beckman_file(file_path)
                all_age_deps.extend(age_deps)
                all_ldl.extend(ldl)
                all_gender.extend(gend)
                print(f"Successfully processed {len(ldl)} records from {file}")
            except Exception as e:
                print(f"Error processing {file}: {str(e)}")
        else:
            print(f"File not found: {file_path}")

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
    output_file = 'combined_beckman_data_second.xlsx'
    df.to_excel(output_file, index=False)
    print(f"\nAll data combined and saved to {output_file}")
    print(f"Total records processed: {len(df)}")

    return all_age_deps, all_ldl, all_gender

def load_combined_beckman_data(file_path='combined_beckman_data_second.xlsx'):
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