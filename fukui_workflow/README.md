Reusable Fukui function workflow for Gaussian outputs.

Features:
- Hirshfeld & CM5 Fukui indices
- Dual descriptor
- Plotting + ranking
- RC vs TS comparison

Extract:
python fukui_extract.py hirshfeld N.log N+1.log N-1.log

Plot:
python fukui_plot.py fukui_hirshfeld.xlsx

Compare:
python fukui_compare.py rc.xlsx ts.xlsx
