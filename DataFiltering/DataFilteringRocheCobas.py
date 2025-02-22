import pandas as pd
import numpy as np
import os
from AdditionalFunctions.ConvertFunctions import convert_to_float

# Global lists for storing data
TGL = []
KLS = []
LDL = []
HDL = []


def filter_sequential_groups(df):
    global TGL, KLS, LDL, HDL  # Declare using global variables
    df_copy = df.copy()
    df_copy = df_copy[~(df_copy['Sonuç'].isna() | (df_copy['Sonuç'].astype(str).str.lower() == 'nan'))].reset_index(
        drop=True)

    i = 0
    DeletingRows = []

    while i < len(df_copy) - 3:
        current_numune = df_copy['Numune No'].iloc[i]
        current_group = df_copy.iloc[i:i + 4]

        # Check if all 4 rows have the same Numune No
        if len(set(current_group['Numune No'])) == 1:
            # Check if the group contains all required tests
            tests = set(current_group['Test Adı'])
            required_tests = {'Trigliserit', 'Kolesterol, total', 'LDL-kolesterol', 'HDL-Kolesterol'}

            if tests == required_tests:
                # Get values in correct order
                group_dict = {row['Test Adı']: row['Sonuç'] for _, row in current_group.iterrows()}

                TGL.append(convert_to_float(group_dict['Trigliserit']))
                KLS.append(convert_to_float(group_dict['Kolesterol, total']))
                LDL.append(convert_to_float(group_dict['LDL-kolesterol']))
                HDL.append(convert_to_float(group_dict['HDL-Kolesterol']))
                i += 4
            else:
                DeletingRows.append(df_copy.index[i])
                i += 1
        else:
            DeletingRows.append(df_copy.index[i])
            i += 1

    # Add remaining rows to DeletingRows
    if i < len(df_copy):
        DeletingRows.extend(df_copy.index[i:])

    return df_copy.drop(DeletingRows).reset_index(drop=True)


def process_roche_file(input_file, output_file):
    global TGL, KLS, LDL, HDL  # Declare using global variables

    # Clear the lists before processing
    TGL.clear()
    KLS.clear()
    LDL.clear()
    HDL.clear()

    # Read the ROCHE Excel file
    try:
        input_path = os.path.join('Data', 'input', input_file)
        df = pd.read_excel(input_path)
        print(f"Successfully read file with {len(df)} rows")

        # Apply the filtering
        filtered_df = filter_sequential_groups(df)
        print(f"After filtering: {len(filtered_df)} rows")

        # Create new DataFrame with filtered results
        results_df = pd.DataFrame({
            'Trigliserit': TGL,
            'Kolesterol': KLS,
            'LDL': LDL,
            'HDL': HDL
        })

        # Save to new Excel file in the output directory
        output_path = os.path.join('Data', output_file)

        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        results_df.to_excel(output_path, index=False)
        print(f"Results saved to {output_path}")

        return results_df

    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return None


