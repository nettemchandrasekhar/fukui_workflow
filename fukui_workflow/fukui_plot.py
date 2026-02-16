import pandas as pd
import matplotlib.pyplot as plt
import sys


def plot_column(df, col, title):

    plt.figure(figsize=(14,5))
    plt.bar(df["Atom"], df[col])
    plt.xticks(rotation=90)
    plt.title(title)
    plt.tight_layout()
    plt.show()


def main():

    if len(sys.argv) != 2:
        print("Usage: python fukui_plot.py fukui.xlsx")
        return

    df = pd.read_excel(sys.argv[1])

    plot_column(df, "f+", "Electrophilic susceptibility")
    plot_column(df, "f-", "Nucleophilic susceptibility")
    plot_column(df, "f0", "Radical susceptibility")
    plot_column(df, "Δf", "Dual descriptor")

    print("\nTop electrophilic sites:")
    print(df.sort_values("f+", ascending=False).head(10))


if __name__ == "__main__":
    main()
