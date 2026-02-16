#!/usr/bin/env python3

import re
import sys
import pandas as pd


def extract_block(data, pattern, label):
    block = re.search(pattern, data, re.DOTALL)
    if not block:
        raise ValueError(f"{label} block not found")
    return block.group(0)


def parse_hirshfeld(file):
    with open(file, "r", errors="ignore") as f:
        data = f.read()

    block = extract_block(
        data,
        r"Hirshfeld charges.*?Orbital energies",
        "Hirshfeld"
    )

    charges = []
    for line in block.splitlines():
        p = line.split()
        if len(p) >= 7 and p[0].isdigit():
            charges.append((p[1], float(p[2])))

    return charges


def parse_cm5(file):
    with open(file, "r", errors="ignore") as f:
        data = f.read()

    block = extract_block(
        data,
        r"Hirshfeld charges.*?CM5 charges.*?\n\s*\n",
        "CM5"
    )

    charges = []
    for line in block.splitlines():
        p = line.split()
        if len(p) >= 8 and p[0].isdigit():
            charges.append((p[1], float(p[-1])))

    return charges


def build_df(chN, chNp, chNm, label):

    atoms = [f"{i+1}_{chN[i][0]}" for i in range(len(chN))]

    qN  = [x[1] for x in chN]
    qNp = [x[1] for x in chNp]
    qNm = [x[1] for x in chNm]

    df = pd.DataFrame({
        "Atom": atoms,
        f"{label}(N)": qN,
        f"{label}(N+1)": qNp,
        f"{label}(N-1)": qNm
    })

    df["f+"] = df[f"{label}(N+1)"] - df[f"{label}(N)"]
    df["f-"] = df[f"{label}(N)"] - df[f"{label}(N-1)"]
    df["f0"] = (df["f+"] + df["f-"]) / 2
    df["Δf"] = df["f+"] - df["f-"]

    return df


def main():

    if len(sys.argv) != 5:
        print("Usage:")
        print("python fukui_extract.py TYPE neutral.log plus.log minus.log")
        print("TYPE = hirshfeld or cm5")
        sys.exit()

    mode, N, Np, Nm = sys.argv[1:]

    parser = parse_hirshfeld if mode == "hirshfeld" else parse_cm5

    df = build_df(parser(N), parser(Np), parser(Nm), mode.upper())

    out = f"fukui_{mode}.xlsx"
    df.to_excel(out, index=False)

    print(f"\n✅ Saved → {out}")


if __name__ == "__main__":
    main()
