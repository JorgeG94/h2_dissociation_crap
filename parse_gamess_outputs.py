import os
import re
import csv
from collections import defaultdict

output_dir = "outputs"
log_files = [f for f in os.listdir(output_dir) if f.endswith(".log")]

# Patterns for extracting energy
energy_patterns = {
    "fci": r"CI EIGENSTATE\s+1 TOTAL ENERGY\s+=\s+([-0-9.Ee]+)",
    "ccsdt": r"COUPLED-CLUSTER ENERGY E\(\s*CCSD\(T\)\)\s+=\s+([-0-9.Ee]+)",
    "r-use": r"FINAL R-USELIBXC ENERGY IS\s+([-0-9.Ee]+)",
    "dh": r"FINAL DOUBLE HYBRID ENERGY=\s+([-0-9.Ee]+)"
}

# Final desired column order
ordered_methods = [
    "fci",
    "ccsdt",
    "b3lyp",
    "pbe0",
    "m06-2x",
    "b2-plyp",
    "pbe0-dh",
    "scan0-dh",
    "tpss0-dh"
]

# Data collection
data = defaultdict(dict)

for log_file in log_files:
    path = os.path.join(output_dir, log_file)

    match = re.match(r"(.*?)_h2_r_([0-9.]+)\.log", log_file)
    if not match:
        print(f"Skipping unrecognized file name format: {log_file}")
        continue

    tag = match.group(1)
    R = float(match.group(2))

    # Determine method and pattern
    if tag.startswith("dft_"):
        func = tag[4:-7].replace("_", "-")
        pattern = energy_patterns["dh"] if any(k in func.lower() for k in ["dh", "b2", "tpss0", "scan0"]) else energy_patterns["r-use"]
        method_or_func = func.lower()
    elif tag.startswith("fci"):
        method_or_func = "fci"
        pattern = energy_patterns["fci"]
    elif tag.startswith("cc"):
        method_or_func = "ccsdt"
        pattern = energy_patterns["ccsdt"]
    else:
        print(f"Unknown method for: {log_file}")
        continue

    with open(path) as f:
        content = f.read()
    match_energy = re.search(pattern, content)

    if match_energy:
        energy = float(match_energy.group(1))
        data[R][method_or_func] = energy
    else:
        print(f"Energy not found in {log_file}")

# Write the CSV
all_Rs = sorted(data.keys())

with open("energies_ordered.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["R"] + ordered_methods)

    for R in all_Rs:
        row = [R] + [data[R].get(method, "") for method in ordered_methods]
        writer.writerow(row)

print("Wrote energies to energies_ordered.csv")

