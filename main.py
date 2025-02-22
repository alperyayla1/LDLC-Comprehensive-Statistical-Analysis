import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
import os
from DataFiltering.DataFilteringFatih import load_combined_data, combine_fatih_files
from DataFiltering.DataFilteringBeckman import combine_beckman_files, process_beckman_file
from DataFiltering.DataFilteringRocheCobas import process_roche_file


def create_ldl_distribution_plots(LDL, title="LDL Distribution Analysis"):

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(title, fontsize=14)

    # 1. Q-Q Plot
    stats.probplot(LDL, dist="norm", plot=ax1)
    ax1.set_title("Q-Q Plot")
    ax1.set_ylabel("Sample Quantiles (mg/dL)")

    # 2. Histogram with density curve
    sns.histplot(data=LDL, kde=True, ax=ax2)
    ax2.set_title("Histogram with Density Curve")
    ax2.set_xlabel("LDL Values (mg/dL)")
    ax2.set_ylabel("Count")

    # 3. Box Plot
    sns.boxplot(y=LDL, ax=ax3)
    ax3.set_title("Box Plot")
    ax3.set_ylabel("LDL Values (mg/dL)")

    # Adjust layout
    plt.tight_layout()

    # Statistical tests for normality
    shapiro_stat, shapiro_p = stats.shapiro(LDL)
    ks_stat, ks_p = stats.kstest(LDL, 'norm')

    print("\nNormality Tests:")
    print(f"Shapiro-Wilk test: statistic={shapiro_stat:.4f}, p-value={shapiro_p:.4f}")
    print(f"Kolmogorov-Smirnov test: statistic={ks_stat:.4f}, p-value={ks_p:.4f}")

    # Basic distribution statistics
    print("\nDistribution Statistics:")
    print(f"Mean: {np.mean(LDL):.2f} mg/dL")
    print(f"Median: {np.median(LDL):.2f} mg/dL")
    print(f"Std Dev: {np.std(LDL):.2f} mg/dL")
    print(f"Skewness: {stats.skew(LDL):.2f}")
    print(f"Kurtosis: {stats.kurtosis(LDL):.2f}")

    return fig


def main():
    print("Loading combined data file...")
    #age_and_dependents, LDL, gender = load_combined_data('combined_fatih_data.xlsx')
    #age_and_dependents, LDL, gender = load_combined_data('combined_beckman_data.xlsx')
    # Directory paths

    fatih_dir = "C:/Users/alper/OneDrive/Masaüstü/BioChemistry"
    beckman_dir = "C:/Users/alper/OneDrive/Masaüstü/BioChemistry"
    roche_dir = "C:/Users/alper/OneDrive/Masaüstü/BioChemistry"

    """
    # Process Fatih data
    print("Processing Fatih data...")
    combine_fatih_files(fatih_dir)
    print("Fatih data processing complete!")
    #combine_beckman_files(beckman_dir)
    #combine_fatih_files(fatih_dir)
    """
    roche_input = "C:/Users/alper/OneDrive/Masaüstü/BioChemistry/ROCHE (1).xls"

    # Output path in project's Data directory
    roche_output = "Data/ROCHE_filtered_results.xlsx"

    # Create Data directory in project if it doesn't exist
    os.makedirs("Data", exist_ok=True)
    print("Processing ROCHE data...")
    process_roche_file(roche_input, roche_output)
    print("ROCHE data processing complete!")


if __name__ == "__main__":
    main()