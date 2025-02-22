import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
from DataFiltering.DataFilteringFatih import load_combined_data


def create_qq_plot(LDL, title="LDL Normal Distribution Analysis"):
    # Create figure without specifying DPI
    fig, ax = plt.subplots()

    # Create Q-Q plot with enhanced appearance
    stats.probplot(LDL, dist="norm", plot=ax)

    # Customize plot appearance
    ax.set_title("LDL-C Q-Q Plot for Abbott Test Data", fontsize=12)
    ax.set_xlabel("Theoretical Quantiles", fontsize=10)
    ax.set_ylabel("LDL-C Sample Quantiles (mg/dL)", fontsize=10)

    # Add grid with lighter lines
    ax.grid(True, linestyle='--', alpha=0.3, color='#202020')

    # Enhance the scatter points - gray and unfilled
    line = ax.get_lines()[0]
    line.set_markerfacecolor('none')  # Unfilled markers
    line.set_markeredgecolor('gray')  # Gray color
    line.set_markersize(3)
    line.set_label('Sample')

    # Enhance the reference line
    line = ax.get_lines()[1]
    line.set_color('red')
    line.set_linewidth(1)
    line.set_label('Reference Line')

    # Add legend
    ax.legend()

    # Adjust layout
    plt.tight_layout()

    # Statistical tests for normality
    k2_stat, k2_p = stats.normaltest(LDL)
    print("\nLDL-C Normality Test:")
    print(f"D'Agostino's K² test: statistic={k2_stat:.4f}, p-value={k2_p:.4f}")

    return fig


def main():
    print("Loading combined data file...")
    age_and_dependents, LDL, gender = load_combined_data('combined_fatih_data.xlsx')

    # Create Q-Q plot
    qq_plot = create_qq_plot(LDL)

    # Save plot with high DPI
    plt.savefig('ldlc_qq_plot.png', dpi=600, bbox_inches='tight')

    # Show plot
    plt.show()


if __name__ == "__main__":
    main()