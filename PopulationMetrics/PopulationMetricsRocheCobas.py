import numpy as np
import pandas as pd
import os

def print_iqr_stats(name, data):
    # Convert to integer using round
    data = np.round(data).astype(int)
    q1 = int(np.percentile(data, 25))
    q3 = int(np.percentile(data, 75))
    iqr = q3 - q1

    print(f"\n{name} Statistics:")
    print(f"Median: {int(np.median(data))}")
    print(f"IQR: {iqr}")
    print(f"Q1: {q1}")
    print(f"Q3: {q3}")

def print_group_stats(name, data, total_patients):
    # Convert to integer using round
    data = np.round(data).astype(int)
    print(f"\n{name} Group Distribution:")

    if name == "LDL":
        groups = [
            (0, 69, "LDL < 70"),
            (70, 99, "LDL 70-99"),
            (100, 129, "LDL 100-129"),
            (130, 159, "LDL 130-159"),
            (160, 189, "LDL 160-189"),
            (190, float('inf'), "LDL ≥ 190")
        ]
    else:  # TGL
        groups = [
            (0, 99, "TGL < 100"),
            (100, 149, "TGL 100-149"),
            (150, 199, "TGL 150-199"),
            (200, 399, "TGL 200-399"),
            (400, float('inf'), "TGL ≥ 400")
        ]

    for low, high, label in groups:
        if high == float('inf'):
            mask = data >= low
        elif low == 0:
            mask = data <= high
        else:
            mask = (data >= low) & (data <= high)
        count = np.sum(mask)
        percentage = (count / total_patients) * 100
        print(f"{label}: N={count} ({percentage:.1f}%)")

def load_roche_data():
    try:
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "ROCHE_filtered_results.xlsx")
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"Error loading ROCHE data: {str(e)}")
        return None

def calculate_roche_population_metrics():
    # Load data
    df = load_roche_data()
    if df is None:
        return None

    # Extract components and convert to integers using round
    TGL = np.round(df['Trigliserit'].astype(float)).astype(int)
    KLS = np.round(df['Kolesterol'].astype(float)).astype(int)
    LDL = np.round(df['LDL'].astype(float)).astype(int)
    HDL = np.round(df['HDL'].astype(float)).astype(int)

    # Print population overview
    total_patients = len(LDL)
    print("\nROCHE Population Statistics:")
    print(f"Total Number of Patients: {total_patients}")

    # Print IQR statistics for each measure
    print_iqr_stats("Kolesterol (KLS)", KLS)
    print_iqr_stats("LDL", LDL)
    print_iqr_stats("HDL", HDL)
    print_iqr_stats("TGL", TGL)

    # Print group statistics for LDL and TGL
    print_group_stats("LDL", LDL, total_patients)
    print_group_stats("TGL", TGL, total_patients)

    return {
        'basic_metrics': {
            'KLS': KLS,
            'TGL': TGL,
            'HDL': HDL,
            'LDL': LDL
        },
        'total_patients': total_patients
    }

if __name__ == "__main__":
    roche_metrics = calculate_roche_population_metrics()