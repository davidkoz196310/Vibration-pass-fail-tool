import os
import math
import pandas as pd
import matplotlib.pyplot as plt


# ----- (change later) -----
FOLDER = "Files_For_Test"

# thresholds (from your screenshot; change anytime)
THRESH_RMS = 1.50
X_HIGH = 0.80
X_LOW  = -0.80
Y_HIGH = 1.10
Y_LOW  = -1.10
Z_HIGH = 3.00
Z_LOW  = -1.00
USE_RMS = True
RMS_HIGH = THRESH_RMS
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

    df = pd.read_csv(file_path, skiprows=header_index, low_memory=False)

    # clean column names (sometimes spaces happen)
    df.columns = [c.strip() for c in df.columns]

    # make sure numeric columns are numeric
    for col in ["rms", "x", "y", "z", "time(ms)"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    x_max = df["x"].max()
    x_min = df["x"].min()
    y_max = df["y"].max()
    y_min = df["y"].min()
    z_max = df["z"].max()
    z_min = df["z"].min()
    rms_max = df["rms"].max()

    fail_reasons = []

    if x_max > X_HIGH: fail_reasons.append(f"x too high: {x_max:.3f} > {X_HIGH}")
    if x_min < X_LOW:  fail_reasons.append(f"x too low:  {x_min:.3f} < {X_LOW}")

    if y_max > Y_HIGH: fail_reasons.append(f"y too high: {y_max:.3f} > {Y_HIGH}")
    if y_min < Y_LOW:  fail_reasons.append(f"y too low:  {y_min:.3f} < {Y_LOW}")

    if z_max > Z_HIGH: fail_reasons.append(f"z too high: {z_max:.3f} > {Z_HIGH}")
    if z_min < Z_LOW:  fail_reasons.append(f"z too low:  {z_min:.3f} < {Z_LOW}")

    if USE_RMS and rms_max > RMS_HIGH:
        fail_reasons.append(f"RMS too high: {rms_max:.3f} > {RMS_HIGH}")
    if fail_reasons:
        print(f"{file_path} FAILED!")
        for r in fail_reasons:
            print("  - " + r)
        status = "FAILED"
    else:
        print(f"{file_path} PASSED!")
        status = "PASSED"
    
    return df, status, fail_reasons

def plot_one_file(df, filename, status, fail_reasons):
    # magnitude
    df["magnitude"] = (df["x"]**2 + df["y"]**2 + df["z"]**2).apply(lambda v: math.sqrt(v))

    plt.figure()
    plt.suptitle(filename)

    # plot x, y, z, magnitude
    plt.subplot(2, 2, 1)
    plt.plot(df["x"])
    plt.title("x data")
    plt.axhline(X_HIGH, linestyle="--", color="red")
    plt.axhline(X_LOW, linestyle="--", color="red")

    plt.subplot(2, 2, 2)
    plt.plot(df["y"])
    plt.title("y data")
    plt.axhline(Y_HIGH, linestyle="--", color="red")
    plt.axhline(Y_LOW, linestyle="--", color="red")

    plt.subplot(2, 2, 3)
    plt.plot(df["z"])
    plt.title("z data")
    plt.axhline(Z_HIGH, linestyle="--", color="red")
    plt.axhline(Z_LOW, linestyle="--", color="red")

    plt.subplot(2, 2, 4)
    if "rms" in df.columns:
        plt.plot(df["rms"], label="rms")
        plt.title("RMS")
        plt.axhline(RMS_HIGH, linestyle="--", linewidth=1, color="red")
    else:
        plt.plot(df["magnitude"])
        plt.title("magnitude")
        plt.axhline(RMS_HIGH, linestyle="--", lidewidth=1, color="red")
    plt.tight_layout()
    if status == "FAILED":
        reason_text = "\n".join(fail_reasons[:3])        #show 3 reasons
        plt.suptitle(f"{filename} FAILED\n{reason_text}", fontsize=10)
    else:
        plt.suptitle(f"{filename} PASSED", fontsize=10)
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

        result = load_vibration_csv(file_path)
        if result is None:
            continue
        df, status, fail_reasons = result
        print(filename, status + "!")

        plot_one_file(df, filename, status, fail_reasons)


if __name__ == "__main__":
    main()