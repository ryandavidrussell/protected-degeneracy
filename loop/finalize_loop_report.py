"""
finalize_loop_report.py — close the brackets in LOOP_VERIFICATION_REPORT.md
from loop_results.npz, mechanically.

Pinned rule made executable: verdicts and metrics are read from the npz, never
from figures or prose. If any frozen assertion in the report is contradicted by
computed values, abort with exit 2 and write nothing.
"""
from __future__ import annotations
import argparse, math, re, sys
from pathlib import Path
import numpy as np

RET_TOL = 0.05
JUMP_THR = 0.10
GRID_N = 32

RET_KEYS = {"AF": "ret_AF", "AG": "ret_AG", "FG": "ret_FG"}
DMAX_KEYS = {"AF": "dmax_AF", "AG": "dmax_AG", "FG": "dmax_FG"}
NJ_KEYS = {"AF": "njumps_AF", "AG": "njumps_AG", "FG": "njumps_FG"}
ARR_KEYS = {"AF": "O_AF", "AG": "O_AG", "FG": "O_FG"}
EXPECTED_DMAX = {"AF": 0.699, "AG": 0.935, "FG": 0.291}
EXPECTED_NJ = {"AF": 4, "AG": 4, "FG": 4}


def load_npz(npz_path: Path):
    data = np.load(npz_path)
    obj = {k: data[k] for k in data.files}
    return obj


def recompute_metrics(arr):
    arr = np.asarray(arr, dtype=float).reshape(-1)
    if arr.size != GRID_N:
        raise ValueError(f"Expected {GRID_N} samples, got {arr.size}")
    diffs = np.abs(np.diff(np.r_[arr, arr[0]]))
    ret = float(abs(arr[0] - arr[-1]))
    dmax = float(diffs.max())
    nj = int((diffs > JUMP_THR).sum())
    return ret, dmax, nj


def consistency_gate(metrics):
    errs = []
    if not all(m[0] <= RET_TOL for m in metrics.values()):
        errs.append("MONODROMY fired unexpectedly (ret > 0.05)")
    if not any(m[2] >= 1 for m in metrics.values()):
        errs.append("PHASE-BOUNDARIES did not fire (no jumps)")
    for k in ("AF", "AG", "FG"):
        ret, dmax, nj = metrics[k]
        if not math.isclose(dmax, EXPECTED_DMAX[k], rel_tol=0, abs_tol=5e-4):
            errs.append(f"{k}: dmax mismatch: got {dmax:.6f}, expected ~{EXPECTED_DMAX[k]:.3f}")
        if nj != EXPECTED_NJ[k]:
            errs.append(f"{k}: n_jumps mismatch: got {nj}, expected {EXPECTED_NJ[k]}")
    return errs


def substitute_placeholders(report_text, metrics):
    for k in ("AF", "AG", "FG"):
        report_text = report_text.replace(f"[{RET_KEYS[k]}]", f"{metrics[k][0]:.6f}")
    return report_text


def write_cartesian_figure(npz_obj, out_png: Path):
    import matplotlib.pyplot as plt
    theta = np.linspace(0, 2*np.pi, GRID_N, endpoint=False)
    plt.figure(figsize=(9, 5))
    for key, label in (("O_AF", "AF"), ("O_AG", "AG"), ("O_FG", "FG")):
        y = np.asarray(npz_obj[key], dtype=float).reshape(-1)
        plt.plot(theta, y, marker="o", linewidth=1.5, markersize=3, label=label)
    plt.xlabel(r"$\theta$")
    plt.ylabel(r"$O(\theta)$")
    plt.title("Loop experiment: equivariant commutant along closed deformation paths")
    plt.xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi], ["0", "π/2", "π", "3π/2", "2π"])
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("npz")
    ap.add_argument("report")
    ap.add_argument("--out-report", required=True)
    ap.add_argument("--out-figure", required=True)
    args = ap.parse_args()

    npz_path = Path(args.npz)
    report_path = Path(args.report)
    out_report = Path(args.out_report)
    out_figure = Path(args.out_figure)

    obj = load_npz(npz_path)
    metrics = {}
    for k in ("AF", "AG", "FG"):
        if ARR_KEYS[k] not in obj:
            raise KeyError(f"Missing {ARR_KEYS[k]} in npz")
        metrics[k] = recompute_metrics(obj[ARR_KEYS[k]])

    errs = consistency_gate(metrics)
    if errs:
        print("CONSISTENCY GATE FAILED:", file=sys.stderr)
        for e in errs:
            print(" - " + e, file=sys.stderr)
        raise SystemExit(2)

    text = report_path.read_text(encoding="utf-8")
    text = substitute_placeholders(text, metrics)
    out_report.write_text(text, encoding="utf-8")
    write_cartesian_figure(obj, out_figure)
    print("OK")
    for k in ("AF", "AG", "FG"):
        ret, dmax, nj = metrics[k]
        print(f"{k}: ret={ret:.6f}, dmax={dmax:.6f}, n_jumps={nj}")
    print(f"wrote report: {out_report}")
    print(f"wrote figure:  {out_figure}")


if __name__ == "__main__":
    main()
