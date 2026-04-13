import csv, json, math, pathlib
from collections import defaultdict

root = pathlib.Path(".")
rows = list(csv.DictReader(open(root / "out" / "compound_validation.csv")))
for r in rows:
    for k in ["phi_avg", "delta_phi", "ionicity", "phi_compound", "band_gap_eV", "epsilon_r_static"]:
        r[k] = float(r[k])

by = defaultdict(list)
for r in rows:
    by[r["true_class"]].append(r)

centroids = {}
for cls, items in by.items():
    centroids[cls] = {
        "phi_avg": sum(x["phi_avg"] for x in items) / len(items),
        "delta_phi": sum(x["delta_phi"] for x in items) / len(items),
        "n": len(items),
    }

correct = 0
compound_rows = []
for x in rows:
    dists = []
    for cls, c in centroids.items():
        d = math.hypot(x["phi_avg"] - c["phi_avg"], x["delta_phi"] - c["delta_phi"])
        dists.append((d, cls))
    dists.sort()
    nearest = dists[0][1]
    if nearest == x["true_class"]:
        correct += 1
    compound_rows.append({
        "formula": x["formula"],
        "true_class": x["true_class"],
        "phi_avg": round(x["phi_avg"], 6),
        "delta_phi": round(x["delta_phi"], 6),
        "ionicity": round(x["ionicity"], 6),
        "phi_comp": round(x["phi_compound"], 6),
        "nearest_centroid_2d": nearest,
        "distance_2d": round(dists[0][0], 6),
    })

summary = {
    "summary": {
        "total_compounds": len(rows),
        "accuracy_2d_centroid": round(correct / len(rows), 3),
        "chance_accuracy": 0.2,
        "improvement_over_chance": round((correct / len(rows)) / 0.2, 2),
        "classes": ["IONIC", "POLAR_COVALENT", "NETWORK_COVALENT", "INTERMETALLIC", "TM_OXIDE"],
    },
    "centroids_2d": centroids,
    "compounds": compound_rows,
}

out = root / "out" / "compound_validation_summary.json"
out.write_text(json.dumps(summary, indent=2))
print(out)
