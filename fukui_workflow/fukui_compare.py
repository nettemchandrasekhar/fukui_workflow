import pandas as pd
import sys


def main():

    if len(sys.argv) != 3:
        print("Usage: python fukui_compare.py RC.xlsx TS.xlsx")
        return

    rc = pd.read_excel(sys.argv[1])
    ts = pd.read_excel(sys.argv[2])

    merged = rc.merge(ts, on="Atom", suffixes=("_RC", "_TS"))

    merged["Δf+"] = merged["f+_TS"] - merged["f+_RC"]
    merged["Δf-"] = merged["f-_TS"] - merged["f-_RC"]
    merged["ΔΔf"] = merged["Δf+"] - merged["Δf-"]

    merged.to_excel("RC_TS_compare.xlsx", index=False)

    print("\n✅ Comparison saved → RC_TS_compare.xlsx")


if __name__ == "__main__":
    main()
