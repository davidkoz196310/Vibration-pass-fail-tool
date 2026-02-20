# Vibration-pass-fail-tool
Tool that reads vibration CSV files, plots the signals and checks pass/fail status
based on configurable thresholds.

-----------------------------

## What This Tool Does

• Reads vibration CSV files  
• Detects the header row  
• Extracts RMS, X, Y, Z signals  
• Calculates magnitude  
• Plots signals in subplots  
• Applies pass/fail threshold logic  
• Processes multiple files in batch  

-----------------------------

## How to run

With Terminal:
run: vibe_step2batch_plot.py

The script will:
- Process all CSV files in the folder
- Print PASS/FAIL in the console
- Display signal plots one-by-one

Close each plot window to continue to the next file.

-------------------------------