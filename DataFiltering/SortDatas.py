# sort_data.py
import pandas as pd


def sort_and_save_data():
    # Set data directory with forward slashes
    data_dir = 'C:/Users/alper/PycharmProjects/BioChemistry/Data'

    # File paths with forward slashes
    beckman_path = f'{data_dir}/combined_beckman_data_second.xlsx'
    fatih_path = f'{data_dir}/combined_fatih_data.xlsx'
    roche_path = f'{data_dir}/ROCHE_filtered_results.xlsx'

    # Read and sort each dataset
    print("Reading and sorting datasets...")

    # Beckman data
    beckman_data = pd.read_excel(beckman_path)
    beckman_sorted = beckman_data.sort_values(by='LDL')
    beckman_sorted.to_excel(f'{data_dir}/beckman_sorted.xlsx', index=False)
    print("Beckman data sorted and saved")

    # Fatih data
    fatih_data = pd.read_excel(fatih_path)
    fatih_sorted = fatih_data.sort_values(by='LDL')
    fatih_sorted.to_excel(f'{data_dir}/fatih_sorted.xlsx', index=False)
    print("Fatih data sorted and saved")

    # Roche data
    roche_data = pd.read_excel(roche_path)
    roche_sorted = roche_data.sort_values(by='LDL')
    roche_sorted.to_excel(f'{data_dir}/roche_sorted.xlsx', index=False)
    print("Roche data sorted and saved")

    print("\nAll datasets have been sorted and saved!")


if __name__ == "__main__":
    sort_and_save_data()