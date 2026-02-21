import pandas as pd

file_path = "vibration_data.csv"  #changable in the future

with open(file_path, "r", errors="ignore") as f:      #csv file has text lines at the top,
    lines = f.readlines()                             #so it will ignore and start with "rms"

start_row = None
for i, line in enumerate(lines):
    if line.strip().lower().startswith("rms"):
        start_row = i
        break

if start_row is None:
    print("I couldn't find the header row that starts with 'rms'")
    quit()

print("Header found at line:", start_row + 1)

df = pd.read_csv(file_path, skiprows=start_row)   #will read from start of header line

print("Columns:", list(df.columns))
print("First 5 rows:")
print(df.head())
print("How many rows:", len(df))
