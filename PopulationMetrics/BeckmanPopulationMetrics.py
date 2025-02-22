import numpy as np
from DataFiltering.DataFilteringBeckman import load_combined_beckman_data

def print_iqr_stats(name, data):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1

    print(f"\n{name} Statistics:")
    print(f"Median: {np.median(data):.2f}")
    print(f"IQR: {iqr:.2f}")
    print(f"Q1: {q1:.2f}")
    print(f"Q3: {q3:.2f}")

def print_group_stats(name, data, total_patients):
    print(f"\n{name} Group Distribution:")

    if name == "LDL":
        # LDL specific groups
        groups = [
            (0, 69, "LDL < 70"),
            (70, 99, "LDL 70-99"),
            (100, 129, "LDL 100-129"),
            (130, 159, "LDL 130-159"),
            (160, 189, "LDL 160-189"),
            (190, float('inf'), "LDL ≥ 190")
        ]
    else:  # TGL
        # TGL specific groups
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
        elif low == 0:  # For the "less than" groups
            mask = data <= high
        else:
            mask = (data >= low) & (data <= high)
        count = np.sum(mask)
        percentage = (count / total_patients) * 100
        print(f"{label}: N={count} ({percentage:.1f}%)")

def calculate_population_metrics(age_and_dependents, LDL, gender):
    # Extract components
    age = age_and_dependents[:, 0].astype(float)
    KLS = age_and_dependents[:, 1].astype(float)
    TGL = age_and_dependents[:, 2].astype(float)
    HDL = age_and_dependents[:, 3].astype(float)

    # Print population overview
    total_patients = len(LDL)
    print("\nBeckman Population Statistics:")
    print(f"Total Number of Patients: {total_patients}")

    # Print IQR statistics for each measure
    print_iqr_stats("Age", age)
    print_iqr_stats("Kolesterol (KLS)", KLS)
    print_iqr_stats("LDL", LDL)
    print_iqr_stats("HDL", HDL)
    print_iqr_stats("TGL", TGL)

    # Print group statistics for LDL and TGL
    print_group_stats("LDL", LDL, total_patients)
    print_group_stats("TGL", TGL, total_patients)

    # Gender distribution
    unique_genders, gender_counts = np.unique(gender, return_counts=True)
    print("\nGender Distribution:")
    for gender_type, count in zip(unique_genders, gender_counts):
        percentage = (count / len(gender)) * 100
        print(f"{gender_type}: {count} ({percentage:.2f}%)")

    # Return calculated values for potential further use
    return {
        'basic_metrics': {
            'age': age,
            'KLS': KLS,
            'TGL': TGL,
            'HDL': HDL,
            'LDL': LDL
        },
        'gender_distribution': dict(zip(unique_genders, gender_counts))
    }

def main():
    print("Loading combined data file...")
    age_and_dependents, LDL, gender = load_combined_beckman_data('combined_beckman_data_second.xlsx')
    calculate_population_metrics(age_and_dependents, LDL, gender)

if __name__ == "__main__":
    main()