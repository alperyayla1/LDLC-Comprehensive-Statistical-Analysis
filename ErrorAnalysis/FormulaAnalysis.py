#C:/Users/alper/PycharmProjects/BioChemistry/Data

import pandas as pd
import numpy as np
from math import sqrt


def read_and_sort_data(beckman_path, fatih_path, roche_path):

    beckman_data = pd.read_excel(beckman_path)
    fatih_data = pd.read_excel(fatih_path)
    roche_data = pd.read_excel(roche_path)

    # Sort each dataset by LDL-C values
    beckman_sorted = beckman_data.sort_values(by='LDL-C')
    fatih_sorted = fatih_data.sort_values(by='LDL-C')
    roche_sorted = roche_data.sort_values(by='LDL-C')

    return beckman_sorted, fatih_sorted, roche_sorted


def calculate_friedewald(total_cholesterol, hdl, triglycerides):
    """Calculate LDL using Friedewald formula"""
    return total_cholesterol - hdl - (triglycerides / 5)


def calculate_sampson(total_cholesterol, hdl, triglycerides):
    """Calculate LDL using Sampson formula"""
    return total_cholesterol - hdl - (triglycerides / 5.2)


def calculate_yayla(total_cholesterol, hdl, triglycerides):
    """Calculate LDL using Yayla formula"""
    return total_cholesterol - hdl - (np.sqrt(triglycerides) * total_cholesterol) / 100


def martin_constant(TGL_Value, HDL_Value, martin_data):
    """Calculate Martin constant from lookup table"""
    row_number = 69
    column_number = 6

    for idx, row in enumerate(martin_data[1:, 0], start=1):
        if TGL_Value <= row:
            row_number = idx
            break

    for j, column in enumerate(martin_data[0, 1:]):
        if HDL_Value <= column:
            column_number = j + 1
            break

    return martin_data[row_number, column_number]


def calculate_martin(total_cholesterol, hdl, triglycerides, martin_data):
    """Calculate LDL using Martin-Hopkins formula"""
    martin_ldl = np.zeros(len(total_cholesterol))

    for i in range(len(total_cholesterol)):
        non_hdl = total_cholesterol[i] - hdl[i]
        martin_ldl[i] = non_hdl - (triglycerides[i] / martin_constant(triglycerides[i], non_hdl, martin_data))

    return martin_ldl


def calculate_all_formulas(dataset, martin_data):
    """Calculate all formulas for a given dataset"""
    tc = dataset['Total Cholesterol'].values
    hdl = dataset['HDL'].values
    tg = dataset['Triglycerides'].values

    friedewald_ldl = calculate_friedewald(tc, hdl, tg)
    sampson_ldl = calculate_sampson(tc, hdl, tg)
    yayla_ldl = calculate_yayla(tc, hdl, tg)
    martin_ldl = calculate_martin(tc, hdl, tg, martin_data)

    return friedewald_ldl, sampson_ldl, yayla_ldl, martin_ldl


def main():
    # File paths
    beckman_path = 'combined_beckman_data.second.xlsx'
    fatih_path = 'combined_fatih_data.xlsx'
    roche_path = 'ROCHE_filtered_results.xlsx'
    martin_path = 'martindataset.xlsx'

    # Read Martin dataset
    martin_data = pd.read_excel(martin_path, header=None).to_numpy().astype(float)
    martin_data[0, 0] = None  # Ignore first cell

    # Read and sort the datasets
    beckman_sorted, fatih_sorted, roche_sorted = read_and_sort_data(
        beckman_path, fatih_path, roche_path
    )

    # Calculate formulas for each dataset
    datasets = {
        'Beckman': beckman_sorted,
        'Fatih': fatih_sorted,
        'Roche': roche_sorted
    }

    results = {}
    for name, dataset in datasets.items():
        friedewald, sampson, yayla, martin = calculate_all_formulas(dataset, martin_data)
        results[name] = {
            'Friedewald': friedewald,
            'Sampson': sampson,
            'Yayla': yayla,
            'Martin': martin
        }

        # Print summary statistics
        print(f"\nResults for {name} dataset:")
        for formula, values in results[name].items():
            print(f"\n{formula} Formula Statistics:")
            print(f"Mean: {np.mean(values):.2f}")
            print(f"Std: {np.std(values):.2f}")
            print(f"Min: {np.min(values):.2f}")
            print(f"Max: {np.max(values):.2f}")

        # Optionally save results to Excel
        result_df = pd.DataFrame({
            'Friedewald_LDL': friedewald,
            'Sampson_LDL': sampson,
            'Yayla_LDL': yayla,
            'Martin_LDL': martin
        })
        result_df.to_excel(f'{name}_LDL_results.xlsx', index=False)


if __name__ == "__main__":
    main()