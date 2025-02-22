import pandas as pd
import numpy as np
from math import sqrt
import os


def calculate_friedewald(total_cholesterol, hdl, triglycerides):
    return total_cholesterol - hdl - (triglycerides / 5)


def calculate_sampson(total_cholesterol, hdl, triglycerides):
    return (total_cholesterol / 0.948) - (hdl / 0.971) - (
            triglycerides / 8.56 + triglycerides * (total_cholesterol - hdl) / 2140 - (
            triglycerides ** 2) / 16100) - 9.44


def calculate_yayla(total_cholesterol, hdl, triglycerides):
    return total_cholesterol - hdl - (np.sqrt(triglycerides) * total_cholesterol) / 100


def martin_constant(TGL_Value, non_HDL_Value, martin_data):
    """
    Find the correct divisor from Martin's table based on TG and non-HDL values
    TGL_Value: triglyceride value
    non_HDL_Value: total cholesterol - HDL
    martin_data: lookup table
    """
    # Get TG values from first column
    tg_values = martin_data[1:, 0]
    # Get non-HDL values from first row
    non_hdl_values = martin_data[0, 1:]

    # Find the row index for TG
    row_idx = len(tg_values) - 1  # Default to last row
    for i, tg in enumerate(tg_values):
        if TGL_Value <= tg:
            row_idx = i
            break

    # Find the column index for non-HDL
    col_idx = len(non_hdl_values) - 1  # Default to last column
    for i, non_hdl in enumerate(non_hdl_values):
        if non_HDL_Value <= non_hdl:
            col_idx = i
            break

    # Get the value from the table
    return martin_data[row_idx + 1, col_idx + 1]


def calculate_martin(total_cholesterol, hdl, triglycerides, martin_data):
    martin_ldl = np.zeros(len(total_cholesterol))

    for i in range(len(total_cholesterol)):
        non_hdl = total_cholesterol[i] - hdl[i]
        divisor = martin_constant(triglycerides[i], non_hdl, martin_data)
        martin_ldl[i] = total_cholesterol[i] - hdl[i] - (triglycerides[i] / divisor)

    return martin_ldl


def calculate_all_formulas(dataset, martin_data):
    tc = dataset['KLS'].values
    hdl = dataset['HDL'].values
    tg = dataset['TGL'].values

    friedewald_ldl = calculate_friedewald(tc, hdl, tg)
    sampson_ldl = calculate_sampson(tc, hdl, tg)
    yayla_ldl = calculate_yayla(tc, hdl, tg)
    martin_ldl = calculate_martin(tc, hdl, tg, martin_data)

    return friedewald_ldl, sampson_ldl, yayla_ldl, martin_ldl


def main():
    # Set data directory with forward slashes
    data_dir = 'C:/Users/alper/PycharmProjects/BioChemistry/Data'

    # Set results directory
    results_dir = 'C:/Users/alper/PycharmProjects/BioChemistry/FormulaLDLDatas'

    # Create results directory if it doesn't exist
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Read pre-sorted datasets
    beckman_sorted = pd.read_excel(f'{data_dir}/beckman_sorted.xlsx')
    fatih_sorted = pd.read_excel(f'{data_dir}/fatih_sorted.xlsx')
    roche_sorted = pd.read_excel(f'{data_dir}/roche_sorted.xlsx')

    # Read Martin dataset
    martin_path = f'C:/Users/alper/OneDrive/Masaüstü/BioChemistry/martindataset.xlsx'
    martin_df = pd.read_excel(martin_path, header=None)

    # Replace 'tg/nonhdlc' with 0 before converting to float
    martin_df.iloc[0, 0] = 0
    martin_data = martin_df.to_numpy().astype(float)

    # Calculate formulas for each dataset
    datasets = {
        'Beckman': beckman_sorted,
        'Fatih': fatih_sorted,
        'Roche': roche_sorted
    }

    for name, dataset in datasets.items():
        friedewald, sampson, yayla, martin = calculate_all_formulas(dataset, martin_data)

        # Save results
        result_df = pd.DataFrame({
            'Friedewald_LDL': friedewald,
            'Sampson_LDL': sampson,
            'Yayla_LDL': yayla,
            'Martin_LDL': martin
        })
        output_path = f'{results_dir}/{name}_LDL_results.xlsx'
        result_df.to_excel(output_path, index=False)
        print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    main()