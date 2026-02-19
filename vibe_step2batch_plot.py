import os
import math
import pandas as pd
import matplotlib.pyplot as plt


# ----- SETTINGS (you can change later) -----
FOLDER = "Files_For_Test"

# thresholds (from your screenshot; change anytime)
THRESH_RMS = 1.50
X_HIGH = 0.80
X_LOW  = -0.80
Y_HIGH = 1.10
Y_LOW  = -1.10
Z_HIGH = 3.00
Z_LOW  = -1.00


def find_header_line_index(file_path):
    # find which line contains the header (starts with "rms")
    with open(file_path, "r", errors="ignore") as f:
        lines = f.readlines()

    header_index = None
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("rms"):
            header_index = i
            break

    return header_index


def load_vibration_csv(file_path):
    header_index = find_header_line_index(file_path)
    if header_index is None:
        print("Could not find header in:", file_path)
        return None

    df = pd.read_csv(file_path, skiprows=header_index)

    # clean column names (sometimes spaces happen)
    df.columns = [c.strip() for c in df.columns]

    # make sure numeric columns are numeric
    for col in ["rms", "x", "y", "z", "time(ms)"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def check_pass_fail(df):
    # If any value breaks the rules => FAIL
    if df["rms"].max() > THRESH_RMS:
        return False

    if df["x"].max() > X_HIGH or df["x"].min() < X_LOW:
        return False

    if df["y"].max() > Y_HIGH or df["y"].min() < Y_LOW:
        return False

    if df["z"].max() > Z_HIGH or df["z"].min() < Z_LOW:
        return False

    return True


def plot_one_file(df, title_text):
    # magnitude
    df["magnitude"] = (df["x"]**2 + df["y"]**2 + df["z"]**2).apply(lambda v: math.sqrt(v))

    plt.figure()
    plt.suptitle(title_text)

    # plot x, y, z, magnitude
    plt.subplot(2, 2, 1)
    plt.plot(df["x"])
    plt.title("x data")
    plt.axhline(X_HIGH)
    plt.axhline(X_LOW)

    plt.subplot(2, 2, 2)
    plt.plot(df["y"])
    plt.title("y data")
    plt.axhline(Y_HIGH)
    plt.axhline(Y_LOW)

    plt.subplot(2, 2, 3)
    plt.plot(df["z"])
    plt.title("z data")
    plt.axhline(Z_HIGH)
    plt.axhline(Z_LOW)

    plt.subplot(2, 2, 4)
    plt.plot(df["magnitude"])
    plt.title("magnitude data")

    plt.tight_layout()
    plt.show()  # blocks until you close the window


def main():
    if not os.path.isdir(FOLDER):
        print("Folder not found:", FOLDER)
        print("Create it and put CSV files inside.")
        return

    files = [f for f in os.listdir(FOLDER) if f.lower().endswith(".csv")]
    if len(files) == 0:
        print("No CSV files found in:", FOLDER)
        return

    for filename in files:
        file_path = os.path.join(FOLDER, filename)
        print("\n---", filename, "---")

        df = load_vibration_csv(file_path)
        if df is None:
            continue

        passed = check_pass_fail(df)
        if passed:
            print(filename, "PASSED!")
        else:
            print(filename, "FAILED!")

        plot_one_file(df, filename)


if __name__ == "__main__":
    main()